# Research question and objectives

Computing for Bioinformatics, group project (Step 1 of the brief: for lecturer approval).

## Research question

**Which specific genetic mutations in *Mycobacterium tuberculosis* are most strongly linked to antibiotic resistance?**

*M. tuberculosis* does not pick up resistance genes from other bacteria. It becomes resistant
almost entirely through mutations in its own chromosome, in the genes that encode a drug's
target or the enzyme that activates the drug. That makes the question answerable from genome
data: if we know which mutations each isolate carries and whether it grew in the presence of
each drug, we can measure how strongly each mutation goes with resistance.

## How the question meets the brief

| Requirement | How it is met |
|---|---|
| Biological | It asks about mutations in a named pathogen and a named process (drug resistance). |
| Specific | For each drug, isolates that carry a mutation are compared with isolates that do not, and the outcome is resistant or susceptible. |
| Answerable with existing data | The CRyPTIC consortium data compendium: 12,287 clinical isolates, each with a whole-genome sequence and laboratory susceptibility results for 13 drugs. |
| Testable | Each mutation and drug pair gives a 2 x 2 table, an odds ratio and a p-value; resistance can also be predicted from mutations and scored against the laboratory result. |

## Objectives

1. **Build a clean dataset** that links the mutations each isolate carries in known and candidate
   resistance genes to its laboratory result (resistant or susceptible) for 13 anti-TB drugs.
2. **Measure and rank the association** between every mutation and resistance to every drug
   (odds ratio, Fisher's exact test with false discovery rate correction, positive predictive
   value), and check that the ranking holds within each lineage of the bacterium.
3. **Interpret the top-ranked mutations biologically:** which gene and protein region they fall in,
   how much they raise the minimum inhibitory concentration, which mutations travel together
   (co-occurrence network), and whether they agree with the published literature.
4. **Predict resistance from mutations with machine learning** and compare the models with two
   baselines: always predicting the majority class, and a rule that uses only the single
   strongest mutation.

## Hypothesis

Resistance to each drug is explained mostly by a small number of mutations in the gene for the
drug's target or activating enzyme (for example *rpoB* for rifampicin and *katG* for isoniazid).
These mutations will have very large odds ratios. Synonymous mutations and mutations that only
mark a lineage will show little or no association once lineage is taken into account.

## Data

| Item | Detail |
|---|---|
| Source | CRyPTIC Consortium, "A data compendium associating the genomes of 12,289 *Mycobacterium tuberculosis* isolates with quantitative resistance phenotypes to 13 antibiotics", PLOS Biology 2022, doi:10.1371/journal.pbio.3001721 |
| Where it is hosted | EMBL-EBI public FTP: `http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/` |
| Type of data | DNA: whole-genome sequence variants (mutations relative to the H37Rv reference genome), plus laboratory minimum inhibitory concentrations |
| Isolates | 12,287 clinical isolates from 23 countries |
| Drugs | Isoniazid, rifampicin, rifabutin, ethambutol, ethionamide, levofloxacin, moxifloxacin, amikacin, kanamycin, linezolid, bedaquiline, clofazimine, delamanid |
| Patient data | None. The files contain bacterial genomes and laboratory results only. |

The files used and every variable in them are described in [02_data_dictionary.md](02_data_dictionary.md).
