# Data dictionary

All data come from the public CRyPTIC release of June 2022 on the EMBL-EBI FTP server:
`http://ftp.ebi.ac.uk/pub/databases/cryptic/release_june2022/`

The three files in `data/` are produced by `scripts/build_dataset.py`. The script downloads the
original tables, keeps the columns and rows this project needs, and changes no values.

Every file is keyed on `UNIQUEID`, the CRyPTIC identifier of one cultured isolate
(format `site.SITE.subj.SUBJECT.lab.LABID.iso.N`).

## 1. `cryptic_phenotypes.csv.gz`: laboratory drug susceptibility

Original file: `reuse/CRyPTIC_reuse_table_20240917.csv`. One row per isolate.

Each isolate was grown on a 96-well plate that holds a dilution series of every drug. The lowest
concentration that stops growth is the minimum inhibitory concentration (MIC).

| Column | Meaning |
|---|---|
| `UNIQUEID` | Isolate identifier (key) |
| `ENA_RUN`, `ENA_SAMPLE` | European Nucleotide Archive accessions of the raw sequencing reads |
| `XXX_BINARY_PHENOTYPE` | `R` (resistant), `S` (susceptible) or missing, for drug `XXX`. Set by comparing the MIC with the drug's epidemiological cut-off value. |
| `XXX_MIC` | MIC in mg/L, as text. `<=0.06` means no growth even at the lowest concentration on the plate; `>8` means growth at the highest. |
| `XXX_PHENOTYPE_QUALITY` | `HIGH`, `MEDIUM` or `LOW`: how well the independent plate-reading methods agreed on the MIC |

Drug codes (`XXX`):

| Code | Drug | Code | Drug |
|---|---|---|---|
| INH | Isoniazid | AMI | Amikacin |
| RIF | Rifampicin | KAN | Kanamycin |
| RFB | Rifabutin | LZD | Linezolid |
| EMB | Ethambutol | BDQ | Bedaquiline |
| ETH | Ethionamide | CFZ | Clofazimine |
| LEV | Levofloxacin | DLM | Delamanid |
| MXF | Moxifloxacin | | |

## 2. `cryptic_genomes.csv.gz`: lineage and sequencing quality

Original file: `reproducibility/data_tables/cryptic-analysis-group/GENOMES.csv.gz`, limited to
isolates that have a phenotype row. One row per isolate.

| Column | Meaning |
|---|---|
| `UNIQUEID` | Isolate identifier (key) |
| `SITEID` | Code of the laboratory that contributed the isolate |
| `SPECIES` | Species call from the sequence data |
| `LINEAGE_NAME` | Lineage call from the SNP-IT tool |
| `MYKROBE_LINEAGE_NAME_1` | Main lineage call from Mykrobe (Lineage 1 to 6 and animal lineages) |
| `MYKROBE_LINEAGE_NAME_2` | Sub-lineage call from Mykrobe, e.g. `lineage2.2.1` |
| `SNP_DISTANCE_TO_H37rV` | Number of single-nucleotide differences from the H37Rv reference genome |
| `N_NULL` | Number of sites where no confident base call could be made |
| `N_SNP`, `N_INDEL` | Number of SNP and insertion/deletion calls |
| `N_FILTER_FAIL` | Number of calls that failed the variant caller's quality filter |
| `N_HET` | Number of mixed (heterozygous) calls, which in a haploid bacterium mean a mixed population |
| `TB_TYPE_1` | CRyPTIC's summary resistance class predicted from the genome |
| `WGS_PREDICTION_STRING` | CRyPTIC's per-drug genetic prediction (not used in the analysis) |

## 3. `cryptic_candidate_gene_mutations.csv.gz`: mutations

Original file: `reproducibility/data_tables/cryptic-analysis-group/MUTATIONS.csv.gz`
(1.4 GB compressed), limited to isolates that have a phenotype row and to 43 candidate
resistance genes. One row per isolate and mutation.

Mutations are differences from the H37Rv reference genome (NC_000962.3), called by the CRyPTIC
Clockwork pipeline.

| Column | Meaning |
|---|---|
| `UNIQUEID` | Isolate identifier |
| `GENE` | Gene name |
| `MUTATION` | The mutation. `S450L`: amino acid 450 changed from serine to leucine. `c-15t`: nucleotide 15 bases upstream of the gene changed from C to T (promoter). `a1401g`: nucleotide 1401 of an RNA gene. `97_indel`: an insertion or deletion at nucleotide 97. A final `!` is a stop codon. |
| `POSITION` | Amino acid number (protein-coding changes) or nucleotide number (promoter, RNA and indel) |
| `IS_SNP`, `IS_INDEL` | Whether the change is a single-nucleotide change or an insertion/deletion |
| `IN_CDS`, `IN_PROMOTER` | Whether it lies in the coding sequence or in the upstream promoter region |
| `IS_SYNONYMOUS`, `IS_NONSYNONYMOUS` | Whether the encoded amino acid stays the same or changes |
| `IS_HET` | Mixed call: only part of the bacterial population carries the mutation |
| `IS_NULL` | No confident base call at this site, so it is not known whether a mutation is present |
| `IS_FILTER_PASS` | Whether the call passed the variant caller's quality filter |
| `ELEMENT_TYPE` | `GENE` (protein-coding), `LOCUS` or `RNA` (ribosomal RNA gene) |
| `MUTATION_TYPE` | `AAM` (amino acid mutation), `SNP` (nucleotide change) or `INDEL` |
| `INDEL_LENGTH` | Number of bases inserted (positive) or deleted (negative) |
| `INDEL_1` | Position and type of the indel, e.g. `97_ins` |

### The 43 candidate genes

Chosen because the WHO catalogue of *M. tuberculosis* mutations lists them as known or candidate
resistance genes for the drugs CRyPTIC tested (plus pyrazinamide and streptomycin genes, kept as
genes that should show no direct link to the tested drugs).

| Drug group | Genes |
|---|---|
| Rifampicin, rifabutin | *rpoB*, *rpoA*, *rpoC* |
| Isoniazid, ethionamide | *katG*, *inhA*, *fabG1*, *ahpC*, *ndh*, *kasA*, *mshA*, *ethA*, *ethR* |
| Ethambutol | *embA*, *embB*, *embC*, *embR*, *ubiA*, *aftA*, *aftB* |
| Levofloxacin, moxifloxacin | *gyrA*, *gyrB* |
| Amikacin, kanamycin | *rrs*, *eis*, *tlyA*, *whiB7* |
| Linezolid | *rplC*, *rrl* |
| Bedaquiline, clofazimine | *Rv0678*, *atpE*, *pepQ*, *mmpL5*, *mmpS5* |
| Delamanid | *ddn*, *fgd1*, *fbiA*, *fbiB*, *fbiC*, *Rv2983* |
| Not tested by CRyPTIC | *pncA*, *rpsA*, *panD* (pyrazinamide); *rpsL*, *gid* (streptomycin) |

## Citation

The CRyPTIC Consortium (2022). A data compendium associating the genomes of 12,289
*Mycobacterium tuberculosis* isolates with quantitative resistance phenotypes to 13 antibiotics.
*PLOS Biology* 20(8): e3001721. https://doi.org/10.1371/journal.pbio.3001721
