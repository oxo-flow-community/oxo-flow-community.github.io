# mixscape completeness audit (2026-08-21)

Upstream: epigen/mixscape_seurat @ v2.0.3 · Port: `oxo-flow-mixscape`
(live-verified).

Smallest workflow of the batch (7 rules): per-sample Seurat .rds →
mixscape.R → {lda.R, visualize.R} + 3 export rules. No FASTQ processing
(upstream module scrnaseq_processing_seurat is the external input stage).

## Mode matrix (upstream — config keys inside one rule set)

| toggle | effect |
|---|---|
| variable_features_only | feature subset for PRTB/DE |
| assay SCT/RNA | assay selection through the chain |
| CalcPerturbSig.split_by_col | split PRTB calc + extra plot sets |
| RunMixscape.split_by_col | split classification + plot splits |
| mixscape_fine_mode | guide-level fine mode |
| prtb_type (KO) | perturbed-class label for LDA/plots |
| Antibody_Capture | ONLY rule-output-graph toggle (adds antibody expression plots + CLR normalization) |
| grna_split_symbol / lfc_th / min_de_genes / min_cells / nt_term / MixscapeLDA.npcs | parameter knobs |
| --report CLI | materializes report()-wrapped outputs |

Hardcoded upstream (not configurable): iter.num=10, seed=42.

## Gap tiers vs the port

**P0**: essentially none structurally — the port covers the 3-analysis-
rule chain; the audit question is whether the config-key surface
(split_by_col ×2, fine_mode, Antibody_Capture branch) is exposed. If
the port pins all config keys, mark P0 = Antibody_Capture + split_by_col
variants (they multiply plot outputs and one changes the output graph).

**P1**: none — MIT, fully offline, no paid DBs. r-seurat 4.4.0 GPL-3
(dependency license note).

**P2**: all remaining config knobs; the --report flag; global.yaml
(dead upstream — never used).

## Verdict

Trivial audit surface — full-line = the single chain + config exposure.
The likely port gap is config-key coverage, not rules.

## Re-verification (2026-08-23, 24h full campaign batch 1)

Latest-commit re-run on tx-ubuntu (latest engine main, conda envs
pre-built on /data): exit 0 — mixscape 9/9 rules, unsupervised 27/27
rules, real CLI execution with fixtures. Env-side fixes only
(umap_leiden missing on first box build; stale env-cache entry cleared;
envs migrated to the data volume after root-disk ENOSPC). No engine
defects found.
