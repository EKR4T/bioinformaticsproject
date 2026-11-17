# Results summary

All numbers come from `TB_resistance_mutations.ipynb`. This file summarises them for the
presentation.

## Data after quality control

| Step | Isolates |
|---|---|
| All isolates with a phenotype | 12,287 |
| *M. tuberculosis* only (14 BCG or other species removed) | 12,273 |
| No mixed-lineage call (202 removed) | 12,071 |
| Genome not extreme in uncalled sites (99 removed) | **11,972** |

* **Mutation calls:** 591,807 → 218,658 after removing failed and uncalled (null) sites.
  Almost two-thirds of the raw rows were null calls.
* **Distinct mutations:** 8,772 in 43 genes; 60% are seen in only one isolate.
* **Phenotypes:** only HIGH-quality resistant/susceptible calls were kept (6,436 to 9,771
  isolates per drug).

## Resistance in the collection

| Drug | Resistant isolates | % resistant |
|---|---|---|
| Isoniazid | 4,339 | 46.9 |
| Rifampicin | 3,373 | 38.7 |
| Rifabutin | 3,124 | 32.0 |
| Ethambutol | 1,423 | 22.1 |
| Ethionamide | 1,161 | 14.4 |
| Levofloxacin | 1,145 | 15.1 |
| Moxifloxacin | 969 | 14.7 |
| Kanamycin | 736 | 8.1 |
| Amikacin | 578 | 6.6 |
| Clofazimine | 103 | 1.4 |
| Delamanid | 81 | 1.0 |
| Linezolid | 72 | 1.0 |
| Bedaquiline | 67 | 0.8 |

CRyPTIC over-sampled drug-resistant TB, so these are not prevalence figures.

## Mutations most strongly linked to resistance

1,113 mutation–drug tests (mutations carried by at least 5 isolates). 528 were significant
(Benjamini–Hochberg FDR < 0.05), and 312 met the "strongly linked" bar (FDR < 0.05, odds-ratio
lower bound > 1, PPV ≥ 0.8).

| Mutation | Drug(s) | Resistant / susceptible carriers | Odds ratio | PPV | Solo carriers (solo PPV) |
|---|---|---|---|---|---|
| *katG* S315T | INH | 3,403 / 35 | 500 | 0.99 | 834 (1.00) |
| *rpoB* S450L | RIF, RFB | 2,242 / 58 | 179 | 0.97 | 100 (1.00) |
| *fabG1* c-15t | INH, ETH | 798 / 20 | 54 | 0.98 | 189 (0.96) |
| *embB* M306V | EMB | 585 / 36 | 95 | 0.94 | 71 (0.94) |
| *rrs* a1401g | AMI, KAN | 487 / 27 (KAN) | 590 | 0.95 | 350 (0.93) |
| *gyrA* D94G | LEV, MXF | 444 / 44 (LEV) | 91 | 0.91 | 12 (0.83) |
| *rpoB* D435V | RIF | 398 / 14 | 49 | 0.97 | 45 (1.00) |
| *gyrA* A90V | LEV | 250 / 30 | 59 | 0.89 | 9 (1.00) |

"Solo" means the mutation is the only non-neutral mutation in that drug's genes.

**How much resistance the strongly linked mutations explain** (sensitivity / specificity of
"carries any of them"):

| | INH | RIF | RFB | EMB | ETH | LEV | MXF | AMI | KAN | LZD | BDQ | CFZ | DLM |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Sensitivity | 93% | 93% | 85% | 76% | 67% | 82% | 58% | 80% | 67% | 28% | 0% | 0% | 6% |
| Specificity | 98% | 98% | 99% | 97% | 99% | 99% | 99% | 100% | 100% | 100% | 100% | 100% | 100% |

## Things that look linked but are not causes

* **Compensatory mutations.** *rpoC* V483A, I491V and V483G have PPV 0.94–0.98 but are never
  found without an *rpoB* resistance mutation. They restore the fitness of rifampicin-resistant
  strains rather than causing resistance.
* **Hitchhikers.** *inhA* I194T and I21T (always with an inhA-promoter mutation), and *embC* A387V
  and *embB* T1082A (never seen alone).
* **Lineage markers.** *katG* R463L: crude OR 1.7 for isoniazid, lineage-adjusted OR 0.16.
  *rpoB* A1075A: 2.3 → 0.67. *gyrA* E21Q, S95T and G668D: not linked. All 78 significant
  negative associations are markers of less-resistant Lineage 4 and Lineage 1 sub-groups.

## Biological interpretation

* **MIC.** *rpoB* mutations raise the rifampicin MIC over 100-fold. *katG* S315T gives
  high-level isoniazid resistance; inhA-promoter mutations give low-level resistance just above
  the ECOFF.
* **Cross-resistance follows the mechanism.** *katG* S315T: 99% INH-resistant but only 24%
  ETH-resistant (KatG activates isoniazid only). *fabG1* c-15t: 98% INH and 92% ETH (InhA is the
  shared target).
* **Hotspots.** The RRDR of *rpoB* (codons 426–452), *katG* codon 315, *embB* codon 306 and the
  QRDR of *gyrA* (codons 88–94).
* **Network.** The drug–mutation network splits into 6 groups, one per mechanism: RIF+RFB,
  INH+ETH, LEV+MXF, AMI+KAN, EMB, LZD. No mutation links two groups.
* **Literature.** 22 of the 26 top-3 mutations per drug are published resistance mutations, 3 are
  published compensatory mutations, and 1 (*embC* A387V) is not established.

## Machine learning (balanced accuracy, 5-fold cross-validation)

| Drug | Majority | Single mutation | Stage 5 rule | Logistic regression | Random forest | RF, unseen laboratories |
|---|---|---|---|---|---|---|
| INH | 0.50 | 0.89 | 0.95 | 0.96 | 0.96 | 0.95 |
| RIF | 0.50 | 0.83 | 0.95 | 0.96 | 0.95 | 0.94 |
| RFB | 0.50 | 0.85 | 0.92 | 0.95 | 0.94 | 0.93 |
| EMB | 0.50 | 0.85 | 0.85 | 0.94 | 0.94 | 0.89 |
| ETH | 0.50 | 0.76 | 0.80 | 0.89 | 0.88 | 0.85 |
| LEV | 0.50 | 0.77 | 0.90 | 0.90 | 0.88 | 0.87 |
| MXF | 0.50 | 0.77 | 0.79 | 0.90 | 0.88 | 0.87 |
| AMI | 0.50 | 0.90 | 0.90 | 0.90 | 0.90 | 0.88 |
| KAN | 0.50 | 0.83 | 0.83 | 0.88 | 0.87 | 0.84 |
| LZD | 0.50 | 0.64 | 0.64 | 0.67 | 0.65 | 0.50 |
| BDQ | 0.50 | 0.63 | 0.50 | 0.62 | 0.63 | 0.49 |
| CFZ | 0.50 | 0.62 | 0.50 | 0.68 | 0.67 | 0.54 |
| DLM | 0.50 | 0.51 | 0.51 | 0.59 | 0.57 | 0.51 |

* ML clearly beats the majority-class and single-mutation baselines. It improves on the simple
  mutation rule mainly for ethambutol, ethionamide and moxifloxacin.
* Part of the gain is co-resistance. For ethambutol, the fluoroquinolones and bedaquiline, the
  best single feature is the isoniazid mutation *katG* S315T, which marks MDR strains.
* For the newer drugs, performance falls to chance on laboratories the model never saw.

## Conclusions

* The mutations most strongly linked to resistance are *katG* S315T (isoniazid), *rpoB* S450L
  (rifamycins), *fabG1* c-15t (isoniazid and ethionamide), *embB* M306V (ethambutol), *rrs* a1401g
  (aminoglycosides), *gyrA* D94G and A90V (fluoroquinolones) and *rpoB* D435V and H445Y.
* The hypothesis is supported for 9 of the 13 drugs. It is not supported for bedaquiline,
  clofazimine, delamanid and linezolid.

**Limitations**

* Not a prevalence sample.
* Association is not proof of cause.
* Rare mutations are excluded.
* Phenotype labels are noisy near the ECOFF.
* Only 43 candidate genes were analysed.
* Co-resistance leaks into ML predictions.

**Future steps**

* Group loss-of-function mutations by gene for the newer drugs.
* Run a genome-wide association study with population-structure correction.
* Validate on Kenyan and other African isolates.
* Map the top mutations onto protein structures.
