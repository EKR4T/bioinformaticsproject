# Team roles

Computing for Bioinformatics, group project (Group C).

Each of the six members led at least one part of the project and presents that part. Everyone reviewed the final
notebook, the conclusions and the slides. Use your row as the starting point for your
individual reflection (see [04_reflection_guide.md](04_reflection_guide.md)).

| Admission no. | Name | Lead role | Notebook stage(s) | Files | Presents slides |
|---|---|---|---|---|---|
| 134976 | Kipngetich Emmanuel Keter | Coordination, GitHub repository, Python environment and Colab setup; machine learning | 7 | `TB_resistance_mutations.ipynb` (Stage 7), `README.md`, `requirements.txt` | Cover, Machine learning, Team |
| 167612 | James Trevor | Research question, objectives and hypothesis; conclusions and limitations | 1, 8 | `docs/01_research_question_and_objectives.md`, `docs/03_results_summary.md` (Conclusions) | Question, Objectives, Hypothesis verdict, Conclusions, Limitations |
| 144861 | Kiome Ian Mutuma | Data acquisition and documentation; biological interpretation: MIC, cross-resistance, co-occurrence network, literature comparison | 2, 6 | `scripts/build_dataset.py`, `data/`, `docs/02_data_dictionary.md`, `TB_resistance_mutations.ipynb` (Stage 6) | Data, Signals that are not causes, Mechanism, Network and literature |
| 169275 | Louis Muiyuro Karanja | Preprocessing and quality control | 3 | `TB_resistance_mutations.ipynb` (Stage 3) | Quality control |
| 158716 | Mwangi Mary Queenvine Muthoni | Exploratory data analysis; slide design | 4 | `TB_resistance_mutations.ipynb` (Stage 4), presentation slides | Exploratory analysis |
| 146414 | Wesly Ryan Mugele | Core analysis: association tests, FDR correction, lineage adjustment, solo analysis | 5 | `TB_resistance_mutations.ipynb` (Stage 5) | Top mutations, How much resistance is explained |
## What each role covered

* **Coordination and machine learning (Kipngetich Emmanuel Keter).** Set up the GitHub
  repository and the Python environment, made sure the notebook runs top to bottom in Colab,
  and built the Stage 7 models: logistic regression and random forest, compared with the
  majority-class, single-mutation and Stage 5 rule baselines, with balanced accuracy, 5-fold
  cross-validation and a held-out-laboratory test.
* **Question and conclusions (James Trevor).** Wrote the research question, the four objectives
  and the hypothesis for lecturer approval, and wrote Stage 8: one conclusion per objective,
  the limitations and the future steps.
* **Data and biological interpretation (Kiome Ian Mutuma).** Found the CRyPTIC data compendium,
  judged that it can answer the question, wrote the script that reduces the 1.4 GB mutation table
  to the 43 candidate genes, and documented every file and variable. Then interpreted the results
  biologically: MIC shifts, cross-resistance by mechanism, resistance hotspots, the NetworkX
  co-occurrence network and the comparison with the published literature.
* **Quality control (Louis Muiyuro Karanja).** Removed non-*M. tuberculosis* isolates, mixed
  lineages, poor genomes, failed and null mutation calls and low-quality phenotypes, with
  before/after counts and checks against known biology.
* **Exploratory analysis (Mwangi Mary Queenvine Muthoni).** Resistance per drug, co-resistance,
  MIC distributions, lineage composition and the PCA of mutation profiles; designed the slides.
* **Core analysis (Wesly Ryan Mugele).** Fisher's exact test, odds ratios and PPV for 1,113
  mutation–drug pairs, Benjamini–Hochberg FDR correction, lineage-adjusted odds ratios and the
  "solo" analysis.