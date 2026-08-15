# Pooled CRISPR perturbation analysis with Seurat Mixscape

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

Pooled CRISPR perturbation analysis (scCRISPR-seq / CROP-seq / Perturb-seq) with Seurat Mixscape: per-cell perturbation signatures (CalcPerturbSig), perturbed vs. non-perturbed classification (RunMixscape), LDA + UMAP projection of the perturbed subset, the full visualization suite (classification statistics, perturbation-score density, posterior-probability and optional antibody-expression violin plots), and reproducibility exports (exact conda envs, runtime config, annotation file). Input is one processed Seurat object per sample.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | single-cell |
| **Rules** | 7 |
| **Tools** | Seurat · seuratobject · irlba · matrix · mixtools · ggplot2 · scales · patchwork · data.table · pyyaml · conda |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [epigen/mixscape_seurat](https://github.com/epigen/mixscape_seurat) |
| **Pinned version** | `v2.0.3` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned (r-seurat 4.4.0, r-seuratobject 4.1.4, r-irlba 2.3.5.1, r-matrix, r-mixtools 2.0.0, r-ggplot2 3.5.2, r-scales 1.3.0, r-patchwork 1.2.0, r-data.table 1.14.10, pyyaml 6.0.1); conda/mamba required at runtime, conda binary on PATH for env export

**Requirements.**
- One processed Seurat object per sample, as {data_dir}/{sample}.rds (already normalized/integrated — QC/normalization run upstream)
- Annotation CSV (name, data columns) mapping sample names to object paths
- Optional: 10X Antibody_Capture assay 'AB' for antibody-expression violin plots
- Compute: up to 8 CPUs / 32000 MB (32 GB) per rule (mixscape, lda, visualize); export rules 1 CPU / 1 GB; -j controls parallelism

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-mixscape
```

## Parameters

| Parameter | Default | Used by |
|---:|---|---|
| `annotation` | `test/fixtures/annotation.csv` | `annot_export`, `config_export` |
| `antibody_capture` | `AB` | `config_export`, `visualize` |
| `assay` | `SCT` | `config_export`, `lda`, `mixscape` |
| `cps_split_by_col` | `` | `config_export`, `mixscape`, `visualize` |
| `data_dir` | `test/fixtures/data` | `mixscape` |
| `fine_mode` | `FALSE` | `config_export`, `mixscape` |
| `gene_col` | `KOcall` | `config_export`, `lda`, `mixscape`, `visualize` |
| `grna_col` | `gRNAcall` | `config_export`, `mixscape` |
| `grna_split_symbol` | `-` | `config_export`, `mixscape` |
| `lda_npcs` | `10` | `config_export`, `lda`, `mixscape` |
| `lfc_th` | `0.1` | `config_export`, `lda`, `mixscape` |
| `mem` | `32000` | `config_export` |
| `min_cells` | `5` | `config_export`, `mixscape` |
| `min_de_genes` | `5` | `config_export`, `mixscape` |
| `mixscape_split_by_col` | `` | `config_export`, `mixscape`, `visualize` |
| `n_neighbors` | `30` | `config_export`, `mixscape` |
| `ndims` | `40` | `config_export`, `mixscape` |
| `nt_term` | `NonTargeting` | `config_export`, `lda`, `mixscape`, `visualize` |
| `project_name` | `myCROPseq` | `annot_export`, `config_export` |
| `prtb_type` | `KO` | `config_export`, `lda`, `mixscape`, `visualize` |
| `result_path` | `results` | `annot_export`, `config_export`, `env_export_lda`, `env_export_mixscape`, `lda`, `mixscape`, `visualize` |
| `threads` | `1` | `config_export` |
| `variable_features_only` | `0` | `config_export`, `mixscape` |

Derived from the workflow's `[config]` section — no schema file to maintain.

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- mixscape
- lda
- visualize
- env_export_mixscape
- env_export_lda
- config_export
- annot_export

**Excluded**

- demultiplexing — upstream module (scrnaseq_processing_seurat), not part of mixscape_seurat v2.0.3
- scdna — upstream module, not part of mixscape_seurat v2.0.3
- normalization — QC/normalization/integration are upstream MrBiomics recipe modules; the input is a processed Seurat object
- differential_test — perturbation DE runs inside Seurat RunMixscape (min.de.genes/logfc.threshold), no separate rule

## Fidelity

Default-parameters main execution path only. The upstream annotation CSV maps
each sample name to the path of its processed Seurat object; the port reads
the same per-sample `.rds` inputs from `{config.data_dir}/{sample}.rds` and
writes all results under `{config.result_path}/mixscape_seurat/` with the
upstream file names.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `mixscape` | `mixscape` | Seurat 4.4.0 (r-seurat) | identical R script logic (CalcPerturbSig, RunMixscape, stats plots, ALL_* outputs); `snakemake@` I/O/config access replaced with CLI args. Threads 8 = upstream `8 * threads` (threads=1), mem 32000 MB. |
| `lda` | `lda` | Seurat 4.4.0 (r-seurat) | identical R script logic (MixscapeLDA, RunUMAP, FILTERED_*/LDA_data outputs). |
| `visualize` | `visualize` | Seurat 4.4.0 (r-seurat) | identical R script logic (PerturbScore, PosteriorProbability, optional `{Antibody_Capture}_expression` violin plots). The antibody-expression plot dir is produced by the script (same guard as upstream) but is not a declared rule output — oxo-flow cannot declare conditionally-enabled outputs. |
| `env_export` | `env_export_mixscape`, `env_export_lda` | conda (user's install) | upstream's single rule with an `{env}` wildcard split into two explicit rules (environments cannot be wildcarded); `conda env export > {output}` verbatim. `conda` itself is unpinned, exactly as upstream. |
| `config_export` | `config_export` | pyyaml 6.0.1 | upstream `run:` block (`yaml.dump(config)`) ported to `scripts/export_config.py`; runtime config values passed as CLI args. pyyaml pinned at port time (2026-08-15) — upstream relied on the unpinned Snakemake runtime env. |
| `annot_export` | `annot_export` | — | `cp {input} {output}` verbatim. |
| `all` (target) | — | — | not ported: oxo-flow's target is implicit (all rules are targets). |
| demultiplexing | — | — | not ported: upstream module (scrnaseq_processing_seurat), outside this repo. |
| scdna | — | — | not ported: upstream module, outside this repo. |
| normalization (QC/normalization/integration) | — | — | not ported: performed upstream of this workflow by the MrBiomics recipe modules; the input is a processed Seurat object. |
| differential_test (perturbation DE) | — | — | not ported: the per-gene DE runs inside `Seurat::RunMixscape` (min.de.genes / logfc.threshold), not as a separate rule. |

Other deviations: (1) sample input paths come from the `{config.data_dir}`
convention instead of per-row CSV paths — the annotation CSV is retained as
the reproducibility artifact (copied by `annot_export`); (2) the upstream
nested config keys (`CalcPerturbSig.*`, `RunMixscape.*`, `MixscapeLDA.npcs`,
`Antibody_Capture`) are flattened in `[config]` — values and defaults are
identical; (3) `test/fixtures/*.rds` are tiny genuine Seurat objects generated
with Seurat 5.4.0 (local toolchain) for dry-run validation only — upstream
pins r-seurat 4.4.0; (4) the `snakemake@` object access in the R scripts is
replaced with positional CLI args (the ported scripts document the arg
order); (5) a commented-out draft plotting block in upstream `mixscape.R`
was dropped.

## Links

- Repository: [oxo-flow-mixscape](https://github.com/oxo-flow-community/oxo-flow-mixscape)
- Upstream: [epigen/mixscape_seurat](https://github.com/epigen/mixscape_seurat) @ `v2.0.3`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
