# Individual reflection: guide

Each member submits their own reflection as a **PDF of at most one page**. The brief asks for
three things, about **you as an individual**. Write it in your own words about what *you*
actually did. The prompts below are only there to help you remember; do not copy them into the
reflection.

## 1. Your role in the group project

Which parts did you work on? The project had these pieces you can point to:

* choosing and wording the research question and objectives;
* finding the dataset and judging whether it could answer the question (Stage 2);
* quality control and the decisions behind it (Stage 3), e.g. removing null calls, mixed
  lineages, low-quality phenotypes;
* exploratory plots (Stage 4);
* the association analysis, lineage adjustment and solo analysis (Stage 5);
* the biological interpretation, network and literature comparison (Stage 6);
* the machine-learning models and baselines (Stage 7);
* conclusions, the GitHub repository, the presentation slides.

## 2. Challenges you experienced

Be specific, and say how you dealt with each one. Examples of things that came up in this
project:

* the full mutation table was 1.4 GB, too big for a notebook, so a script had to reduce it to the
  candidate genes;
* about two-thirds of the mutation rows were uncalled sites, which would have looked like
  thousands of fake mutations;
* lineage made unrelated mutations look linked to resistance;
* some strongly linked mutations (*rpoC*) turned out to be compensatory, not causes;
* ML models learned a shortcut (an isoniazid mutation used to "predict" ethambutol);
* the newer drugs gave a negative result.

## 3. Achievements and what you gained

What can you do now that you could not before? Examples: reading a 2 x 2 table and an odds
ratio; why FDR correction is needed when you run 1,113 tests; confounding by population
structure; why a baseline matters and why accuracy is misleading with imbalanced classes;
working from a real public dataset; Git/GitHub.

## Format checklist

* One page maximum, PDF.
* Your name and admission number at the top.
* About you, not a summary of the whole project.
