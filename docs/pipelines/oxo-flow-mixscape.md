# Pooled CRISPR perturbation analysis (Mixscape)

oxo-flow port of the epigen/mixscape_seurat Snakemake workflow (v2.0.3): pooled CRISPR perturbation analysis (scCRISPR-seq/CROP-seq/Perturb-seq) with Seurat Mixscape — perturbation signatures (CalcPerturbSig), perturbed-cell classification (RunMixscape), LDA+UMAP of the perturbed subset (MixscapeLDA), the visualization suite, and reproducibility exports (conda envs, runtime config, annotation).

| | |
|---:|---|
| **Engine** | snakemake |
| **Source** | [epigen/mixscape_seurat](https://github.com/epigen/mixscape_seurat) |
| **Pinned version** | `v2.0.3` |
| **Ported** | 2026-08-15 |
| **Rules** | 7 |
| **Tools** | Seurat · seuratobject · matrix · irlba · mixtools · ggplot2 · scales · patchwork · data.table · pyyaml · conda |
| **Domain** | single-cell |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- mixscape
- lda
- visualize
- env_export
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
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
