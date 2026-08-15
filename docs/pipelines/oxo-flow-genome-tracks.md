# Genome browser tracks: coverage, gene plots and UCSC hub

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

Merge BAM files per experimental group with samtools, compute normalized bigWig coverage with deepTools bamCoverage (RPGC by default), plot isoform-aware per-gene and per-region genome tracks with gtracks/pyGenomeTracks, and publish a UCSC genome browser track hub — end-to-end track generation for RNA-seq, ATAC-seq and other aligned BAM data.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 8 |
| **Tools** | samtools · deeptools · pygenometracks · gtracks |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [epigen/genome_tracks](https://github.com/epigen/genome_tracks) |
| **Pinned version** | `v2.0.5` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned

**Requirements.**
- BAM files per group at <bam_dir>/<group>/*.bam (aligned/mapped data, e.g. RNA-seq or ATAC-seq; input BAMs need no index — merge_bams produces merged, indexed BAMs)
- sample annotation CSV with a group column (sample_annotation; group values drive merge/coverage/hub fan-out)
- gene list CSV with gene_region,ymax columns (gene_list; gene symbols or chr:start-end regions)
- 12-column genome BED for gene annotation (genome_bed, e.g. ref.bed.gz); no genome FASTA or annotation GTF required
- compute: up to 4 CPUs / 4 GB per rule (samtools merge and bamCoverage at threads=4/4000M); helper rules need 1 CPU / 1 GB
- conda/mamba to build the pinned environment (samtools 1.19.2, deepTools 3.5.5, pyGenomeTracks 3.8, python 3.10.13, gtracks 1.12.6); helper rules need only a system python3
- disk: results/ for merged BAMs, bigWigs, track plots and the UCSC hub

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-genome-tracks
```

## Parameters

| Parameter | Default | Used by |
|---:|---|---|
| `bamCoverage_parameters` | `-p max --binSize 10  --normalizeUsing RPGC --effectiveGenomeSize 2407883318` | `coverage` |
| `bam_dir` | `test/fixtures/bams` | `merge_bams` |
| `base_buffer` | `2000` | `annotate_genes` |
| `email` | `sreichl@cemm.at` | `ucsc_hub` |
| `file_type` | `pdf` | `plot_tracks` |
| `gene_list` | `test/fixtures/genes.csv` | `annotate_genes`, `gene_list_export`, `plot_tracks` |
| `genome` | `mm10` | `ucsc_hub` |
| `genome_bed` | `test/fixtures/genome_bed/ref.bed.gz` | `annotate_genes`, `plot_tracks` |
| `project_name` | `myData` | `annot_export`, `config_export`, `ucsc_hub` |
| `result_path` | `results` | `annot_export`, `annotate_genes`, `config_export`, `coverage`, `gene_list_export`, `merge_bams`, `plot_tracks`, `ucsc_hub` |
| `sample_annotation` | `test/fixtures/annotation.csv` | `annot_export` |
| `track_colors` | `untreated=#800080,treated=#00FFFF` | `plot_tracks`, `ucsc_hub` |
| `width` | `20` | `plot_tracks` |
| `x_axis` | `bottom` | `plot_tracks` |

Derived from the workflow's `[config]` section — no schema file to maintain.

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- merge_bams
- coverage
- annotate_genes
- plot_tracks
- ucsc_hub
- annot_export
- gene_list_export
- config_export

**Excluded**

- split_sc_bam — single-cell sinto branch, not on the default path
- igv_report — temporarily deactivated upstream (commented out of rule all)
- make_bed — only feeds the deactivated igv_report rule
- env_export — conda-runtime documentation rule for envs of non-ported branches; envs/ yamls serve the same role

## Fidelity

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `merge_bams` | `merge_bams` | samtools 1.19.2 | identical command (`samtools merge -@ N` + `samtools index -@ N -b`); the per-group BAM list comes from `{config.bam_dir}/{group}/*.bam` glob instead of the annotation CSV's `bam` column (which is still copied verbatim by `annot_export`); `threads: 4 × config.threads` baked in as `threads = 4` |
| `coverage` | `coverage` | deepTools 3.5.5 | identical command incl. `-p max --binSize 10 --normalizeUsing RPGC --effectiveGenomeSize 2407883318` default and `> {bw}.log 2>&1` redirect |
| Snakefile load-time gene annotation (`parse_gene`/`parse_region`, `gene_annot_df`) | `annotate_genes` | python3 (stdlib) | new single-instance rule; same algorithm (BED scan, min start / max end across isoforms, `base_buffer` extension for genes, no buffer for `chr:start-end` regions, `genes_not_found.csv`, `:`→`-` name replacement); upstream computes it in the Snakemake base env (numpy/pandas) — the port script uses only stdlib, so the upstream `global.yaml` env is not needed |
| `plot_tracks` | `plot_tracks` | gtracks 1.12.6, pyGenomeTracks 3.8 | identical `gtracks` invocation (coordinates, `--genes`, optional `--max ymax`, `--gene-rows`/`--genes-height` = isoform count, `--x-axis`, `--width`, `--color-palette` with `#000000` default); per-gene fan-out uses `[[pairs]]` `pair_id` (oxo-flow has no gene wildcard source); `depends_on = ["coverage"]` added because `expand_inputs` input lists do not form DAG edges in oxo-flow 0.12.0 |
| `ucsc_hub` | `ucsc_hub` | python3 (stdlib) | identical hub content (hub.txt, genomes.txt, trackDb.txt with hex→RGB colors, `../{group}.bw` relative symlinks) ported from the Python run block to `scripts/ucsc_hub.py`; the per-group symlinks are side effects (outputs declared only for the three text files) |
| `env_export` | not ported | — | upstream requests `conda env export` for the pygenometracks/igv_reports/sinto envs; needs a conda runtime and documents envs of branches not ported — the checked-in `envs/pygenometracks.yaml` serves the same reproducibility role |
| `config_export` | `config_export` | python3 (stdlib) | `json.dump(config)` equivalent: `scripts/export_config.py` dumps the workflow's `[config]` table |
| `annot_export` | `annot_export` | cp | identical (`cp` of the annotation CSV) |
| `gene_list_export` | `gene_list_export` | cp | identical (`cp` of the gene list CSV) |
| `make_bed` | not ported | — | only feeds the deactivated `igv_report` rule (not in the default target) |
| `split_sc_bam` | not ported | — | single-cell branch (sinto 0.10.0); not on the default path (no `.tsv` `group` entries in the default annotation) |
| `igv_report` | not ported | — | **temporarily deactivated upstream** (commented out of `rule all` at v2.0.5) |
| Snakemake `report()` wrappers | — | — | no equivalent in oxo-flow; the report artifacts are written as plain files |

Configuration mapping: upstream `config/config.yaml` keys became `[config]`
keys with upstream defaults, except `result_path` (placeholder path →
`results`), `mem`/`threads` (→ per-rule `[rules.resources]`; upstream's
`4 × threads` for merge/coverage baked in as `threads = 4`), and
`track_colors` (YAML dict → comma-joined `group=#hex` string with the same
`#000000` default). Group fan-out uses `[[sample_groups]]` (one `{sample}`
per annotation group), gene fan-out uses `[[pairs]]`. Sample annotation,
gene list, genome BED and BAM files must be kept in sync with `[[sample_groups]]`/
`[[pairs]]` and `config.bam_dir`; the annotation CSV itself remains the
documentation record (`annot_export`).

## Links

- Repository: [oxo-flow-genome-tracks](https://github.com/oxo-flow-community/oxo-flow-genome-tracks)
- Upstream: [epigen/genome_tracks](https://github.com/epigen/genome_tracks) @ `v2.0.5`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
