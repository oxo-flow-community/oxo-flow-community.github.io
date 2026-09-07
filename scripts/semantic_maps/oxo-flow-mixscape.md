**Pooled CRISPR perturbation pipeline** (Seurat Mixscape): given one processed Seurat object per sample of pooled CRISPR data (scCRISPR-seq / CROP-seq / Perturb-seq), it classifies perturbed cells and delivers perturbation signatures, LDA and UMAP projections, classification statistics, and reproducibility exports.

**1. Input preparation** — the run reads a processed Seurat RDS object per sample (driven by the cohort sample group) plus the annotation CSV mapping gRNA calls to samples; every analysis rule expands over the per-sample wildcard.

**2. Perturbation classification** — `mixscape` computes perturbation signatures with CalcPerturbSig, classifies perturbed cells with RunMixscape, and plots classification statistics. Its full object and metadata feed both downstream branches.

**3. Downstream analysis (two parallel branches)** — the `mixscape` output has two independent consumers. `lda` runs MixscapeLDA on perturbed plus non-targeting cells and produces a 2-D UMAP projection with filtered object and data matrices; `visualize` plots perturbation-score densities, posterior-probability violins, and optional antibody expression. With no edge between them, each runs once classification completes.

**4. Reproducibility exports (independent of the analysis)** — four standalone rules record how the run was made without consuming any analysis output: `annot_export` copies the annotation into the results, `config_export` writes the runtime configuration as YAML, and `env_export_mixscape` / `env_export_lda` export the exact conda environments behind each analysis stage (split from the upstream environment export because environments cannot be wildcarded).

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
