"""Export the Stage 7 logistic-regression models for the web app.

Rebuilds the mutation matrix exactly as TB_resistance_mutations.ipynb does (Stages 3 and 4),
fits one L2 logistic regression per drug on all isolates, and writes the coefficients to
webapp/predictor/data/model.json. The web app then predicts with plain Python, so it does not
need scikit-learn at run time.

The script also re-runs the notebook's 5-fold stratified cross-validation (random split) and a
leave-laboratory-out cross-validation for the same model, and stores those scores in the JSON so
the app reports honest out-of-sample performance.

Usage (from the tb-resistance-mutations folder):
    pip install scikit-learn pandas numpy
    python scripts/export_model.py
"""
import json
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd
import sklearn
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, roc_auc_score
from sklearn.model_selection import GroupKFold, StratifiedKFold

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "webapp" / "predictor" / "data" / "model.json"
SEED = 42

DRUGS = {
    "INH": "Isoniazid", "RIF": "Rifampicin", "RFB": "Rifabutin", "EMB": "Ethambutol",
    "ETH": "Ethionamide", "LEV": "Levofloxacin", "MXF": "Moxifloxacin", "AMI": "Amikacin",
    "KAN": "Kanamycin", "LZD": "Linezolid", "BDQ": "Bedaquiline", "CFZ": "Clofazimine",
    "DLM": "Delamanid",
}
DRUG_GENES = {
    "RIF": ["rpoB", "rpoA", "rpoC"],
    "RFB": ["rpoB", "rpoA", "rpoC"],
    "INH": ["katG", "inhA", "fabG1", "ahpC", "ndh", "kasA", "mshA"],
    "ETH": ["ethA", "ethR", "inhA", "fabG1", "ndh", "mshA"],
    "EMB": ["embA", "embB", "embC", "embR", "ubiA", "aftA", "aftB"],
    "LEV": ["gyrA", "gyrB"],
    "MXF": ["gyrA", "gyrB"],
    "AMI": ["rrs", "eis", "whiB7", "tlyA"],
    "KAN": ["rrs", "eis", "whiB7", "tlyA"],
    "LZD": ["rplC", "rrl"],
    "BDQ": ["Rv0678", "atpE", "pepQ", "mmpL5", "mmpS5"],
    "CFZ": ["Rv0678", "pepQ", "mmpL5", "mmpS5"],
    "DLM": ["ddn", "fgd1", "fbiA", "fbiB", "fbiC", "Rv2983"],
}
DRUG_ORDER = list(DRUGS)


def load():
    pheno_raw = pd.read_csv(DATA / "cryptic_phenotypes.csv.gz", low_memory=False)
    genomes_raw = pd.read_csv(DATA / "cryptic_genomes.csv.gz", dtype={"SITEID": str}, low_memory=False)
    muts_raw = pd.read_csv(DATA / "cryptic_candidate_gene_mutations.csv.gz", low_memory=False)
    return pheno_raw, genomes_raw, muts_raw


def isolate_qc(pheno_raw, genomes_raw):
    # Stage 3, isolate filters (notebook cells 8-9)
    iso = pheno_raw[["UNIQUEID"]].merge(genomes_raw, on="UNIQUEID", how="left")
    iso = iso[iso.SPECIES == "M. tuberculosis"]
    iso = iso[~iso.MYKROBE_LINEAGE_NAME_1.isin(["Mixed"])]
    q1, q3 = iso.N_NULL.quantile([0.25, 0.75])
    iso = iso[iso.N_NULL <= q3 + 3 * (q3 - q1)]
    return iso.set_index("UNIQUEID")


def effect(row):
    if row.IS_INDEL:
        return "indel"
    if row.IN_PROMOTER:
        return "promoter"
    if row.ELEMENT_TYPE == "RNA":
        return "rRNA"
    if row.IS_SYNONYMOUS:
        return "synonymous"
    if str(row.MUTATION).endswith("!"):
        return "stop gained"
    return "missense"


def mutation_qc(muts_raw, iso):
    # Stage 3, mutation filters (notebook cell 10)
    m = muts_raw[muts_raw.UNIQUEID.isin(iso.index)].copy()
    m = m[m.IS_FILTER_PASS.astype(bool)]
    m = m[~m.IS_NULL.astype(bool)]
    m = m[~m.IS_HET.astype(bool)]
    m = m.drop_duplicates(["UNIQUEID", "GENE", "MUTATION"])
    m["effect"] = [effect(r) for r in m.itertuples()]
    m["mut_id"] = m.GENE + "_" + m.MUTATION
    return m


def labels(pheno_raw, iso):
    # Stage 3, HIGH-quality R/S calls only (notebook cell 11)
    pheno = pheno_raw.set_index("UNIQUEID").loc[iso.index]
    y_all = {}
    for d in DRUG_ORDER:
        b, q = pheno[f"{d}_BINARY_PHENOTYPE"], pheno[f"{d}_PHENOTYPE_QUALITY"]
        keep = (q == "HIGH") & b.isin(["R", "S"])
        y_all[d] = (b[keep] == "R").astype(int)
    return y_all


def matrix(m, iso):
    # Stage 4, mutation matrix (notebook cell 15)
    M = (m.assign(v=1).pivot_table(index="UNIQUEID", columns="mut_id", values="v", aggfunc="max",
                                   fill_value=0).reindex(iso.index, fill_value=0).astype(np.int8))
    info = m.drop_duplicates("mut_id").set_index("mut_id")[["GENE", "MUTATION", "effect"]]
    info["carriers"] = M.sum()
    return M, info


def model():
    # Stage 7, same settings as the notebook
    return LogisticRegression(C=1.0, class_weight="balanced", max_iter=2000)


def cv_scores(X, y, splitter, groups=None):
    prob = pd.Series(0.0, index=y.index)
    for tr, te in splitter.split(X, y, groups):
        prob.iloc[te] = model().fit(X.iloc[tr], y.iloc[tr]).predict_proba(X.iloc[te])[:, 1]
    pred = (prob >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    sens, spec = tp / (tp + fn), tn / (tn + fp)
    return {"sensitivity": round(sens, 3), "specificity": round(spec, 3),
            "balanced_accuracy": round((sens + spec) / 2, 3), "auc": round(roc_auc_score(y, prob), 3)}


def main():
    pheno_raw, genomes_raw, muts_raw = load()
    iso = isolate_qc(pheno_raw, genomes_raw)
    m = mutation_qc(muts_raw, iso)
    y_all = labels(pheno_raw, iso)
    M, info = matrix(m, iso)
    feat = info.index[(info.effect != "synonymous") & (info.carriers >= 5)]
    print(f"{len(iso):,} isolates, {M.shape[1]:,} mutations, {len(feat):,} features")

    skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=SEED)
    gkf = GroupKFold(n_splits=5)
    drugs = {}
    for d in DRUG_ORDER:
        y = y_all[d]
        X = M.loc[y.index, feat]
        random_split = cv_scores(X, y, skf)
        site_split = cv_scores(X, y, gkf, iso.loc[y.index, "SITEID"].values)
        lr = model().fit(X, y)
        coef = {f: round(float(c), 5) for f, c in zip(feat, lr.coef_[0])}
        drugs[d] = {
            "name": DRUGS[d],
            "genes": DRUG_GENES[d],
            "n_isolates": int(len(y)),
            "n_resistant": int(y.sum()),
            "intercept": round(float(lr.intercept_[0]), 5),
            "coef": coef,
            "cv_random": random_split,
            "cv_unseen_lab": site_split,
        }
        print(f"{d}: AUC {random_split['auc']:.3f}  balanced acc {random_split['balanced_accuracy']:.3f}  "
              f"unseen labs {site_split['balanced_accuracy']:.3f}")

    out = {
        "model": "L2 logistic regression (C=1, class_weight=balanced), one per drug",
        "threshold": 0.5,
        "trained_at": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "sklearn_version": sklearn.__version__,
        "n_isolates": int(len(iso)),
        "features": [{"id": f, "gene": info.at[f, "GENE"], "mutation": info.at[f, "MUTATION"],
                      "effect": info.at[f, "effect"], "carriers": int(info.at[f, "carriers"])}
                     for f in feat],
        "drugs": drugs,
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(out, separators=(",", ":")), encoding="utf-8")
    print(f"Wrote {OUT} ({OUT.stat().st_size / 1e3:.0f} kB)")


if __name__ == "__main__":
    main()
