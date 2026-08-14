# Genomic region set and gene set enrichment

oxo-flow port of epigen/enrichment_analysis v3.0.1: region overlap enrichment (LOLA), genomic region enrichment of annotated terms (rGREAT), region TFBS motif enrichment (pycisTarget), gene over-representation analysis and preranked GSEA (GSEApy), with multiple-test correction inside each tool, per-set enrichment plots, per-group summary plots and reproducibility exports.

| | |
|---:|---|
| **Engine** | snakemake |
| **Source** | [epigen/enrichment_analysis](https://github.com/epigen/enrichment_analysis) |
| **Pinned version** | `v3.0.1` |
| **Ported** | 2026-08-15 |
| **Rules** | 38 |
| **Tools** | gseapy · pandas · pycistarget · bioconductor-lola · bioconductor-rgreat · r-base · r-ggplot2 · r-pheatmap · r-svglite · r-reshape2 · r-data.table · bioconductor-rtracklayer · bioconductor-org.hs.eg.db |
| **Domain** | genomics |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- prepare_databases
- region_enrichment_analysis_LOLA
- region_enrichment_analysis_GREAT
- region_gene_association_GREAT
- region_motif_enrichment_analysis_pycisTarget
- process_results_pycisTarget
- gene_ORA_GSEApy
- gene_preranked_GSEApy
- plot_enrichment_result
- aggregate
- visualize
- config_export
- annot_export

**Excluded**

- gene_motif_enrichment_analysis_RcisTarget — zero instances on the default path: RcisTarget needs .txt gene sets in the annotation; the default annotation has none (region sets + ranked gene sets only)
- env_export — conda env export requires the conda CLI inside the runtime environment; exact pins are already declared in envs/*.yaml
- report rendering — oxo-flow has no report module; the reproducibility exports (configs/, envs) are kept as upstream rules
- note: the anticipated exclusion names liftover/enrichr/gost/single_region_mode do not exist in v3.0.1 (grep-verified; Enrichr appears only as a database-source reference in config comments)

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| prepare_databases | `prepare_databases_Azimuth_2023`, `prepare_databases_Reactome` | gseapy 1.1.3 | identical command; database fan-out baked as static blocks (2 default-path databases) |
| region_enrichment_analysis_LOLA | `region_enrichment_analysis_LOLA` | bioconductor-lola 1.32.0 | identical command; database fan-out baked as static block (1 default-path database) |
| region_enrichment_analysis_GREAT | `region_enrichment_analysis_GREAT_Azimuth_2023`, `region_enrichment_analysis_GREAT_Reactome` | bioconductor-rgreat 2.4.0 | identical command; upstream `great_parameters` nested dict flattened into `great_*` config keys |
| region_gene_association_GREAT | `region_gene_association_GREAT` | bioconductor-rgreat 2.4.0 | identical command; uses the first database (Azimuth_2023) as upstream |
| region_motif_enrichment_analysis_pycisTarget | `region_motif_enrichment_analysis_pycisTarget` | pycistarget 1.1 | command text verbatim (incl. upstream error-tolerance wrapper); threads=10 as upstream |
| process_results_pycisTarget | `process_results_pycisTarget` | pycistarget 1.1 | identical command |
| gene_motif_enrichment_analysis_RcisTarget | not ported | RcisTarget | zero instances on the default path: needs `.txt` gene sets in the annotation, the default annotation has none (region sets + ranked sets only) |
| gene_ORA_GSEApy | `gene_ORA_GSEApy_Azimuth_2023`, `gene_ORA_GSEApy_Reactome` | gseapy 1.1.3 | identical command; upstream genes_dict fan-out has zero default-path members, region-set fan-out kept |
| gene_preranked_GSEApy | `gene_preranked_GSEApy_Azimuth_2023`, `gene_preranked_GSEApy_Reactome` | gseapy 1.1.3 | identical command |
| plot_enrichment_result | `plot_enrichment_result_*` (8 blocks) | r-ggplot2 3.5.0, r-svglite 2.1.0 | identical command; upstream wildcard fan-out (tool × db × feature_set) baked as per-(tool,db) scatter blocks |
| aggregate | `aggregate_*` (8 blocks) | pandas 1.1.4 / 1.5.3 | identical logic; upstream wildcards group/tool/db passed as CLI args |
| visualize | `visualize_*` (8 blocks) | r-ggplot2 3.5.0, r-pheatmap 1.0.12 | identical command/logic; `cluster_summary` config key kept as upstream numeric flag |
| config_export | `config_export` | — | upstream dumps the in-memory config dict; the port copies `config/config.yaml` (effective-config mirror) |
| annot_export | `annot_export` | — | identical command |
| env_export | not ported | — | `conda env export` needs the conda CLI inside the runtime env; exact pins are already declared in `envs/*.yaml` |
| report rendering | not ported | — | oxo-flow has no report module; reproducibility exports (configs/, envs) are kept as upstream rules |

Script ports: upstream scripts run inside snakemake's `snakemake@input/...`
namespace; the port passes the same values as positional CLI arguments
(`scripts/*`), keeping every analysis step and output byte-identical.
`utils.R` is copied verbatim. Fidelity conventions: `{config.a.b}` nested
access does not exist in oxo-flow — all upstream nested config dicts
(`great_parameters`, `pycistarget_parameters`, `column_names`, `adjp_th`,
caps) are flattened into prefixed top-level keys; the pycisTarget
`annotations_to_use` list is carried as a python-list literal string so the
rendered command is byte-identical to upstream.

## Links

- Repository: [oxo-flow-enrichment](https://github.com/oxo-flow-community/oxo-flow-enrichment)
- Upstream: [epigen/enrichment_analysis](https://github.com/epigen/enrichment_analysis) @ `v3.0.1`
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
