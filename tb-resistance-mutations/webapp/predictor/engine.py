"""Resistance prediction from a list of mutations.

Loads the logistic-regression weights exported by scripts/export_model.py and scores them in plain
Python: for each drug, probability = sigmoid(intercept + sum of the weights of the mutations the
isolate carries). No scikit-learn is needed at run time.
"""
import json
import math
import re
from functools import lru_cache
from pathlib import Path

MODEL_PATH = Path(__file__).resolve().parent / "data" / "model.json"

# A model is "reliable" for a drug only if it ranks isolates well (AUC) and keeps its balanced
# accuracy on laboratories it never saw. The four newer drugs fail this test (see the notebook).
RELIABLE_AUC = 0.90
RELIABLE_UNSEEN_LAB = 0.80

EXAMPLES = [
    {"label": "MDR-TB with ethambutol resistance",
     "mutations": ["katG_S315T", "rpoB_S450L", "embB_M306V"]},
    {"label": "MDR-TB plus fluoroquinolone and aminoglycoside",
     "mutations": ["katG_S315T", "rpoB_S450L", "gyrA_D94G", "rrs_a1401g"]},
    {"label": "inhA promoter only (isoniazid + ethionamide)",
     "mutations": ["fabG1_c-15t"]},
    {"label": "Lineage markers only (no resistance mutation)",
     "mutations": ["gyrA_E21Q", "gyrA_S95T"]},
]


@lru_cache(maxsize=1)
def load_model():
    data = json.loads(MODEL_PATH.read_text(encoding="utf-8"))
    data["by_id"] = {f["id"]: f for f in data["features"]}
    data["by_lower"] = {f["id"].lower(): f["id"] for f in data["features"]}
    data["genes_lower"] = {f["gene"].lower() for f in data["features"]}
    return data


def parse_mutations(text):
    """Split free text into mutation tokens.

    Accepts commas, semicolons or new lines between mutations, and either an underscore or a space
    between gene and mutation: "katG_S315T, rpoB S450L" gives ["katG_S315T", "rpoB_S450L"].
    """
    genes = load_model()["genes_lower"]
    tokens = []
    for chunk in re.split(r"[,;\n\r]+", text or ""):
        words = chunk.split()
        i = 0
        while i < len(words):
            if words[i].lower() in genes and i + 1 < len(words):
                tokens.append(f"{words[i]}_{words[i + 1]}")
                i += 2
            else:
                tokens.append(words[i])
                i += 1
    seen, out = set(), []
    for t in tokens:
        if t and t.lower() not in seen:
            seen.add(t.lower())
            out.append(t)
    return out


def resolve(tokens):
    """Match tokens to model features (case-insensitive). Returns (known ids, unknown tokens)."""
    lookup = load_model()["by_lower"]
    known, unknown = [], []
    for t in tokens:
        fid = lookup.get(t.lower())
        if fid and fid not in known:
            known.append(fid)
        elif not fid:
            unknown.append(t)
    return known, unknown


def sigmoid(z):
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


def predict(mutations):
    """Predict resistance to every drug for an isolate carrying `mutations` (feature ids)."""
    model = load_model()
    threshold = model["threshold"]
    results = []
    for code, d in model["drugs"].items():
        coef = d["coef"]
        z = d["intercept"] + sum(coef[m] for m in mutations)
        prob = sigmoid(z)
        contributions = sorted(
            ({"id": m, "gene": model["by_id"][m]["gene"], "weight": coef[m],
              "own_gene": model["by_id"][m]["gene"] in d["genes"]} for m in mutations),
            key=lambda c: -abs(c["weight"]))
        cv, lab = d["cv_random"], d["cv_unseen_lab"]
        results.append({
            "drug": code,
            "name": d["name"],
            "probability": round(prob, 4),
            "call": "R" if prob >= threshold else "S",
            "reliable": cv["auc"] >= RELIABLE_AUC and lab["balanced_accuracy"] >= RELIABLE_UNSEEN_LAB,
            "contributions": [c for c in contributions if abs(c["weight"]) >= 0.05][:4],
            "metrics": {"auc": cv["auc"], "balanced_accuracy": cv["balanced_accuracy"],
                        "sensitivity": cv["sensitivity"], "specificity": cv["specificity"],
                        "unseen_lab_balanced_accuracy": lab["balanced_accuracy"]},
        })
    return results


def metrics_table():
    model = load_model()
    rows = []
    for code, d in model["drugs"].items():
        cv, lab = d["cv_random"], d["cv_unseen_lab"]
        rows.append({"drug": code, "name": d["name"], "n_isolates": d["n_isolates"],
                     "n_resistant": d["n_resistant"], **cv,
                     "unseen_lab": lab["balanced_accuracy"],
                     "reliable": cv["auc"] >= RELIABLE_AUC and lab["balanced_accuracy"] >= RELIABLE_UNSEEN_LAB})
    return rows
