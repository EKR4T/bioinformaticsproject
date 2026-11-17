# Mutations linked to antibiotic resistance in *Mycobacterium tuberculosis*

Computing for Bioinformatics, group project (Group C).

**Research question:** Which specific genetic mutations in *Mycobacterium tuberculosis* are most
strongly linked to antibiotic resistance?

We link the mutations in 43 known and candidate resistance genes to laboratory drug-susceptibility
results for 13 antibiotics in 11,972 clinical isolates from the CRyPTIC consortium. For each
mutation we measure its association with resistance, check it against lineage and co-occurring
mutations, interpret the top hits biologically, and predict resistance with machine learning.

## Main finding

A handful of mutations explain most resistance to the first- and second-line drugs:

| Drug | Top mutation | Share of resistant isolates carrying it | PPV |
|---|---|---|---|
| Isoniazid | *katG* S315T | 78% | 0.99 |
| Rifampicin | *rpoB* S450L | 67% | 0.97 |
| Amikacin | *rrs* a1401g | 80% | 0.94 |
| Ethionamide | *fabG1* c-15t (inhA promoter) | 53% | 0.92 |
| Ethambutol | *embB* M306V | 41% | 0.94 |
| Moxifloxacin | *gyrA* D94G | 43% | 0.88 |

No small set of mutations explains resistance to bedaquiline, clofazimine, delamanid or linezolid.
Full results are in [docs/03_results_summary.md](docs/03_results_summary.md).

## Repository contents

| Path | What it is |
|---|---|
| `TB_resistance_mutations.ipynb` | **The analysis notebook** (all eight stages of the brief, with outputs saved) |
| `data/` | The three data files the notebook reads (about 5 MB in total) |
| `scripts/build_dataset.py` | Rebuilds `data/` from the original CRyPTIC tables on the EMBL-EBI FTP |
| `docs/01_research_question_and_objectives.md` | Research question, objectives, hypothesis, dataset (for lecturer approval) |
| `docs/02_data_dictionary.md` | Description of every file and variable |
| `docs/03_results_summary.md` | Results and conclusions in plain text, for the presentation |
| `docs/04_reflection_guide.md` | Prompts for the individual one-page reflection |
| `docs/Bioinformatics Project Brief.pdf` | The project brief |
| `requirements.txt` | Python packages (all preinstalled in Google Colab) |

## How to run

**Google Colab**

1. Open `TB_resistance_mutations.ipynb` in Colab (File → Open notebook → GitHub, paste this repository's URL).
2. In the Stage 2 code cell, set `REPO_URL` to this repository's GitHub URL. The cell clones the
   repository to get the data files.
3. Runtime → Run all. It takes about 6–8 minutes, most of it in the machine-learning stage.

**Locally**

```bash
pip install -r requirements.txt
jupyter notebook TB_resistance_mutations.ipynb
```

**Rebuilding the data from source (optional).** The files in `data/` are already included.
To regenerate them from the original CRyPTIC release (downloads about 1.5 GB):

```bash
python scripts/build_dataset.py
```

## Data source and citation

The CRyPTIC Consortium (2022). A data compendium associating the genomes of 12,289
*Mycobacterium tuberculosis* isolates with quantitative resistance phenotypes to 13 antibiotics.
*PLOS Biology* 20(8): e3001721. https://doi.org/10.1371/journal.pbio.3001721

Data: http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/

The data contain bacterial genomes and laboratory results only, with no patient information.

## Team

| Admission no. | Name |
|---|---|
| 144861 | Kiome Ian Mutuma |
| 103023 | Mbai Njeke Silver |
| 169275 | Louis Muiyuro Karanja |
| 134976 | Kipngetich Emmanuel Keter |
| 158716 | Mwangi Mary Queenvine Muthoni |
| 167612 | James Trevor |
| 146414 | Wesly Ryan Mugele |
