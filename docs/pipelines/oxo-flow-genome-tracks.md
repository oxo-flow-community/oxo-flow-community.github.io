# Genome browser track generation from BAM files

oxo-flow port of the epigen/genome_tracks Snakemake workflow: merge BAM files per annotation group (samtools merge + index), compute bigWig coverage (deepTools bamCoverage), plot per-gene/region genome tracks (gtracks/pyGenomeTracks) and create a UCSC genome browser track hub — plus reproducibility exports of the annotation, gene list and config.

| | |
|---:|---|
| **Engine** | snakemake |
| **Source** | [epigen/genome_tracks](https://github.com/epigen/genome_tracks) |
| **Pinned version** | `v2.0.5` |
| **Ported** | 2026-08-15 |
| **Rules** | 8 |
| **Tools** | samtools@1.19.2 · deeptools@3.5.5 · pygenometracks@3.8 · gtracks@1.12.6 |
| **Domain** | genomics |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

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
- env_export — conda-runtime documentation rule for envs of non-ported branches; checked-in envs/ yamls serve the same role

## Fidelity

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `merge_bams` | `merge_bams` | samtools 1.19.2 | identical command (`samtools merge -@ N` + `samtools index -@ N -b`); the per-group BAM list comes from `{config.bam_dir}/{group}/*.bam` glob instead of the annotation CSV's `bam` column (which is still copied verbatim by `annot_export`); `threads: 4 × config.threads` baked in as `threads = 4` |
| `coverage` | `coverage` | deepTools 3.5.5 | identical command incl. `-p max --binSize 10 --normalizeUsing RPGC --effectiveGenomeSize 2407883318` default and `> {bw}.log 2>&1` redirect |
| Snakefile load-time gene annotation (`parse_gene`/`parse_region`, `gene_annot_df`) | `annotate_genes` | python3 (stdlib) | new single-instance rule; same algorithm (BED scan, min start / max end across isoforms, `base_buffer` extension for genes, no buffer for `chr:start-end` regions, `genes_not_found.csv`, `:`→`-` name replacement); upstream computes it in the Snakemake base env (numpy/pandas) — the port script uses only stdlib, so the upstream `global.yaml` env is not needed |
| `plot_tracks` | `plot_tracks` | gtracks 1.12.6, pyGenomeTracks 3.8 | identical `gtracks` invocation (coordinates, `--genes`, optional `--max ymax`, `--gene-rows`/`--genes-height` = isoform count, `--x-axis`, `--width`, `--color-palette` with `#000000` default); per-gene fan-out uses `[[pairs]]` `pair_id` (oxo-flow has no gene wildcard source); `depends_on = ["coverage"]` added because `expand_inputs` input lists do not form DAG edges in oxo-flow 0.11.0 |
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
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
