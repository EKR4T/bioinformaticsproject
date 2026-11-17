"""Build the compact analysis tables from the public CRyPTIC release.

The CRyPTIC MUTATIONS table is 1.4 GB compressed (every mutation in every gene of every
isolate), which is too large to download each time the notebook runs. This script downloads
it once, keeps only the rows in the candidate drug-resistance genes listed below, and writes
small files into data/ that are committed to the repository and read by the notebook.

Source (EMBL-EBI FTP, CRyPTIC release June 2022):
    http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/

Run from the project folder:
    python scripts/build_dataset.py

Outputs:
    data/cryptic_phenotypes.csv.gz              one row per isolate, 13 drugs
    data/cryptic_genomes.csv.gz                 one row per isolate, lineage and sequencing QC
    data/cryptic_candidate_gene_mutations.csv.gz  one row per isolate x mutation
"""
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import pandas as pd
import requests

BASE = "http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022"
TABLES = f"{BASE}/reproducibility/data_tables/cryptic-analysis-group"
ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data"
RAW = DATA / "raw"          # large downloads, not committed (see .gitignore)

# Genes with a documented or proposed role in resistance to the drugs CRyPTIC tested
# (WHO mutation catalogue 2021/2023 tier 1 and tier 2 genes for these drugs).
CANDIDATE_GENES = {
    "rpoB", "rpoA", "rpoC",                                    # rifampicin, rifabutin
    "katG", "inhA", "fabG1", "ahpC", "ndh", "kasA", "mshA",   # isoniazid, ethionamide
    "ethA", "ethR",                                            # ethionamide
    "embA", "embB", "embC", "embR", "ubiA", "aftA", "aftB",   # ethambutol
    "gyrA", "gyrB",                                            # levofloxacin, moxifloxacin
    "rrs", "eis", "tlyA", "whiB7",                             # amikacin, kanamycin
    "rplC", "rrl",                                             # linezolid
    "Rv0678", "atpE", "pepQ", "mmpL5", "mmpS5",                # bedaquiline, clofazimine
    "ddn", "fgd1", "fbiA", "fbiB", "fbiC", "Rv2983",           # delamanid
    "pncA", "rpsA", "panD", "rpsL", "gid",                     # pyrazinamide, streptomycin
}

MUTATION_COLUMNS = [
    "UNIQUEID", "GENE", "MUTATION", "POSITION", "IS_SNP", "IS_INDEL", "IN_CDS", "IN_PROMOTER",
    "IS_SYNONYMOUS", "IS_NONSYNONYMOUS", "IS_HET", "IS_NULL", "IS_FILTER_PASS",
    "ELEMENT_TYPE", "MUTATION_TYPE", "INDEL_LENGTH", "INDEL_1",
]
GENOME_COLUMNS = [
    "UNIQUEID", "SITEID", "SPECIES", "LINEAGE_NAME", "MYKROBE_LINEAGE_NAME_1",
    "MYKROBE_LINEAGE_NAME_2", "SNP_DISTANCE_TO_H37rV", "N_NULL", "N_SNP", "N_INDEL",
    "N_FILTER_FAIL", "N_HET", "TB_TYPE_1", "WGS_PREDICTION_STRING",
]


def download(url, dest, parts=16):
    """Download url to dest using several ranged requests in parallel; resumes finished parts."""
    if dest.exists():
        print(f"  already have {dest.name}")
        return
    size = int(requests.head(url, timeout=60).headers["Content-Length"])
    step = -(-size // parts)

    def fetch(i):
        part = dest.with_suffix(dest.suffix + f".part{i:02d}")
        start, end = i * step, min((i + 1) * step, size) - 1
        if part.exists() and part.stat().st_size == end - start + 1:
            return part
        for attempt in range(8):
            try:
                with requests.get(url, headers={"Range": f"bytes={start}-{end}"},
                                  stream=True, timeout=120) as r:
                    r.raise_for_status()
                    with open(part, "wb") as fh:
                        for chunk in r.iter_content(1 << 20):
                            fh.write(chunk)
                if part.stat().st_size == end - start + 1:
                    return part
            except requests.RequestException as err:
                print(f"  part {i} attempt {attempt + 1} failed: {err}")
        raise RuntimeError(f"could not download part {i} of {url}")

    print(f"  downloading {dest.name} ({size / 1e6:.0f} MB) in {parts} parts")
    with ThreadPoolExecutor(parts) as pool:
        part_files = list(pool.map(fetch, range(parts)))
    with open(dest, "wb") as out:
        for part in part_files:
            out.write(part.read_bytes())
    for part in part_files:
        part.unlink()


def main():
    RAW.mkdir(parents=True, exist_ok=True)

    print("1. Phenotypes (reuse table)")
    download(f"{BASE}/reuse/CRyPTIC_reuse_table_20240917.csv", RAW / "CRyPTIC_reuse_table_20240917.csv", parts=1)
    pheno = pd.read_csv(RAW / "CRyPTIC_reuse_table_20240917.csv", low_memory=False)
    pheno = pheno.drop(columns=["VCF", "REGENOTYPED_VCF"])        # FTP paths, not needed
    pheno.to_csv(DATA / "cryptic_phenotypes.csv.gz", index=False)
    print(f"  {len(pheno):,} isolates")

    print("2. Genomes (lineage and sequencing QC)")
    download(f"{TABLES}/GENOMES.csv.gz", RAW / "GENOMES.csv.gz", parts=1)
    genomes = pd.read_csv(RAW / "GENOMES.csv.gz", usecols=GENOME_COLUMNS, low_memory=False,
                          dtype={"SITEID": str})
    genomes = genomes[genomes.UNIQUEID.isin(pheno.UNIQUEID)]
    genomes.to_csv(DATA / "cryptic_genomes.csv.gz", index=False)
    print(f"  {len(genomes):,} isolates with a phenotype")

    print("3. Mutations (filter 1.4 GB table to candidate genes)")
    download(f"{TABLES}/MUTATIONS.csv.gz", RAW / "MUTATIONS.csv.gz")
    keep_ids = set(pheno.UNIQUEID)
    kept, total, isolates_seen = [], 0, set()
    for chunk in pd.read_csv(RAW / "MUTATIONS.csv.gz", usecols=MUTATION_COLUMNS,
                             chunksize=2_000_000, low_memory=False):
        total += len(chunk)
        isolates_seen.update(chunk.UNIQUEID.unique())
        kept.append(chunk[chunk.GENE.isin(CANDIDATE_GENES) & chunk.UNIQUEID.isin(keep_ids)])
        print(f"  read {total:,} rows, kept {sum(map(len, kept)):,}", flush=True)
    mutations = pd.concat(kept, ignore_index=True)[MUTATION_COLUMNS]
    mutations.to_csv(DATA / "cryptic_candidate_gene_mutations.csv.gz", index=False)
    print(f"  source table: {total:,} rows from {len(isolates_seen):,} isolates")
    print(f"  kept: {len(mutations):,} rows, {mutations.UNIQUEID.nunique():,} isolates, "
          f"{mutations.GENE.nunique()} genes")


if __name__ == "__main__":
    main()
