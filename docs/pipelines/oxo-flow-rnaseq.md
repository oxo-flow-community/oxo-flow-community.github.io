# RNA-seq with STAR + gene/isoform counts

oxo-flow port of the nf-core/rnaseq pipeline (default star_salmon + trimgalore main path): fq lint, FastQC, TrimGalore, STAR alignment, samtools sort/index/stats, Picard MarkDuplicates, featureCounts gene counts with biotype MultiQC tables, RSeQC + dupRadar + Qualimap QC, strand-specific bigWig tracks, and a final MultiQC report with the upstream custom content (fail_trimmed / fail_mapped tables, strandedness checks, sample merge, versions). 38 rules, commands byte-for-byte upstream under default parameters, all tools pinned to the exact upstream conda versions.

| | |
|---:|---|
| **Engine** | nf-core |
| **Source** | [nf-core/rnaseq](https://github.com/nf-core/rnaseq) |
| **Pinned version** | `3.26.0` |
| **Ported** | 2026-08-15 |
| **Rules** | 38 |
| **Tools** | fastqc@0.12.1 · trim-galore@2.1.0 · fq@0.12.0 · star@2.7.11b · samtools@1.23.1 · htslib@1.23.1 · gawk@5.1.0 · picard@3.4.0 · subread@2.0.6 · rseqc@5.0.4 · r-base@4.3 · bioconductor-dupradar@1.38.0 · qualimap@2.3 · bedtools@2.31.1 · ucsc-bedclip@377 · ucsc-bedgraphtobigwig@469 · multiqc@1.33 · python@3.12.12 |
| **Domain** | transcriptomics |

## Run it

```bash
oxo-flow run workflow/rnaseq.toml
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastqc
- fq_lint
- trimgalore
- star_align
- samtools_sort
- samtools_index
- samtools_stats
- samtools_flagstat
- samtools_idxstats
- picard_markduplicates
- featurecounts
- biotype_multiqc
- rseqc_bam_stat
- rseqc_infer_experiment
- rseqc_inner_distance
- rseqc_junction_annotation
- rseqc_junction_saturation
- rseqc_read_distribution
- rseqc_read_duplication
- dupradar
- qualimap_rnaseq
- bedtools_genomecov
- ucsc_bedclip
- ucsc_bedgraphtobigwig
- multiqc_custom_content
- multiqc

**Excluded**

- salmon / rsem / hisat2 / stringtie / umicollapse quantification and as_quantification — non-default aligner branches
- PREPARE_GENOME — reference artifacts (fasta, gtf, gene_bed, chrom_sizes, star_index) are inputs
- per-sample min_trimmed_reads filtering — data-dependent per-sample state; only the MultiQC fail_trimmed table is produced
- UMI extraction (umitools) — with_umi branch, off by default
- BBSplit — skip_bbsplit default path only
- SortMeRNA / Bowtie2 rRNA removal — off by default
- cat_fastq — only active for multi-fastq samples
- DESeq2 QC — optional post-run branch
- auto strandedness (per-sample inference) — pipeline-level config.strandedness only
- workflow_summary_mqc.yaml / methods_description_mqc.yaml — Nextflow-param-rendered MultiQC sections

## Fidelity

Commands mirror the upstream modules byte-for-byte under default parameters
(flag-for-flag, including upstream quirks such as `samtools stats` receiving
the `.bai` as a positional argument and RSeQC's stdout redirections). Upstream
process labels are reproduced as `[rules.resources]`. Every tool is pinned to
the exact upstream conda version (see `envs/`).

Known, documented deviations:

| # | upstream (3.26.0) | port | reason |
|---|---|---|---|
| 1 | Per-sample strandedness from the samplesheet (`auto` supported) | Pipeline-level `config.strandedness`, three explicit values only | oxo-flow has one config per run; `auto` needs a Salmon inference branch |
| 2 | `PREPARE_GENOME` builds the STAR index | Reference artifacts (incl. STAR index) are inputs | Excluded as infra; build once and point `config.star_index` at it |
| 3 | RSEM / HISAT2 / UMIcollapse quantification and `as_quantification` | Not ported | Non-default aligner branches (scope: default `star_salmon` main path) |
| 4 | SALMON_QUANT (alignment mode) + CUSTOM_TX2GENE + TXIMETA_TXIMPORT + SUMMARIZEDEXPERIMENT_* — the default-path quantification chain | Ported as `quantification::salmon_quant` / `tx2gene` / `tximport` / `summarizedexperiment` | The upstream 4-process chain is mirrored as 4 rules; tx2gene runs on the first sample's quant dir (upstream `.first()`); the SE process runs twice (gene + transcript) inside one rule with the upstream `--assay_names` values |
| 5 | `min_trimmed_reads` gate drops failing samples from the downstream chain | Only the MultiQC fail_trimmed table is produced | The filter is data-dependent per-sample state (n of trimmed reads), not expressible as a static DAG |
| 6 | `skip_trimming` / `skip_markduplicates` rewire the downstream inputs (QC runs on raw / sorted BAM) | `skip_trimming=true` / `skip_markduplicates=true` break the downstream chain (trimmed reads / markdup BAM are rule inputs) | oxo-flow inputs are static paths; use the defaults |
| 7 | `save_trimmed` / `save_align_intermeds` control publication; intermediates live in workdir | Trimmed FASTQs and intermediate BAMs are always kept at `results/` paths (they double as run checkpoints) | oxo-flow re-executes from declared outputs |
| 8 | RSeQC PDFs are published upstream: `*.pdf` outputs of RSEQC_JUNCTIONANNOTATION (`splicing_events_pie.pdf`, `splicing_junction_pie.pdf`), RSEQC_JUNCTIONSATURATION (`junctionSaturation_plot.pdf`), read_duplication and inner_distance — plus two zero-byte touch placeholders (`junction.pdf`, `events.pdf`) | The same PDFs are kept under `junction_annotation/pdf/`, `junction_saturation/pdf/`, `read_duplication/pdf/`, `inner_distance/pdf/` with `<id>.`-prefixed names (e.g. `<id>.junction_events.pdf`); the zero-byte `junction.pdf` / `events.pdf` touch placeholders are not produced | Layout only — the published artifact set is the same; the touch placeholders are upstream artifacts MultiQC ignores |
| 9 | `BEDTOOLS_GENOMECOV_FW/REV` swap their prefixes between forward and reverse libraries | `genomecov_fw` always emits `<id>.forward` (strand `+`), `genomecov_rev` always `<id>.reverse` (strand `-`) | With pipeline-level strandedness both rules never run together; the published artifact set is identical |
| 10 | `workflow_summary_mqc.yaml` and `methods_description_mqc.yaml` MultiQC sections (Nextflow-param rendered) | Not generated | Nextflow-specific param rendering |
| 11 | Merged-mode software versions are runtime-collated from per-process `versions.yml` | Static `nf_core_rnaseq_software_mqc_versions.yml` pinned to the env versions | Tools are pinned in `envs/*.yaml`; there are no per-process version captures in oxo-flow |
| 12 | `CUSTOM_MULTIQCCUSTOMBIOTYPE` supports `--max_biotypes` via `ext.args` | Fixed at the upstream default `100` | The upstream pipeline never sets it |
| 13 | STRINGTIE_STRINGTIE (default path, runs on the markdup BAM with `-G gtf -e`) | Ported as `quantification::stringtie` (`--fr`/`--rf` from strandedness like upstream) | The `<id>.ballgown/` directory is moved into `results/` but is not declared as a rule output (upstream emits it) |
| 14 | DESEQ2_QC (default path, runs on `salmon.merged.gene_counts_length_scaled.tsv` with `--id_col 1 --sample_suffix '' --count_col 3`, `--vst TRUE` by default) | Ported as `quantification::deseq2_qc` with the upstream header sed (label `star_salmon`) | Blind design (`design=~1`, as upstream); upstream's sample-name group decomposition (Group columns for PCA-by-group plots) is not ported — coldata is the sample IDs only; the `star_salmon.*_mqc.tsv` tables are kept in `results/` (upstream feeds them to MultiQC without publishing). Like `skip_qc` for the other QC files, `skip_deseq2_qc=true` / `skip_quantification_merge=true` leave the MultiQC rule's DESeq2 inputs missing — use the defaults |
| 15 | UMI extraction (`umitools`), BBSplit, SortMeRNA/Bowtie2 rRNA removal, `cat_fastq` | Not ported | `with_umi` / `--skip_bbsplit` (default) / ribo-removal (off by default) / multi-fastq-sample branches |

## Links

- Repository: [oxo-flow-rnaseq](https://github.com/oxo-flow-community/oxo-flow-rnaseq)
- Upstream: [nf-core/rnaseq](https://github.com/nf-core/rnaseq) @ `3.26.0`
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
