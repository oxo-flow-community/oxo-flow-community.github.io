# RNA-seq: alignment, quantification and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

End-to-end bulk RNA-seq analysis for paired-end reads: fq lint and FastQC raw-read QC, TrimGalore adapter/quality trimming, STAR alignment, Picard MarkDuplicates, Salmon alignment-mode quantification with tximport-merged gene/transcript count tables and SummarizedExperiment R objects, StringTie reference-guided assembly and quantification, featureCounts gene counts with biotype tables, RSeQC / dupRadar / Qualimap QC, DESeq2 sample-level QC (PCA, sample distances, size factors), strand-specific bigWig tracks, and one final MultiQC report with the nf-core/rnaseq custom content (fail_trimmed / fail_mapped tables, strandedness checks, software versions). A faithful port of the nf-core/rnaseq 3.26.0 default star_salmon path — same tools, same versions, same commands.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | transcriptomics |
| **Rules** | 44 |
| **Tools** | fastqc · trim-galore · fq · star · salmon · stringtie · python · samtools · htslib · gawk · picard · subread · rseqc · r-base · bioconductor-dupradar · qualimap · bedtools · ucsc-bedclip · ucsc-bedgraphtobigwig · bioconductor-tximeta · bioconductor-summarizedexperiment · r-optparse · r-ggplot2 · r-rcolorbrewer · r-pheatmap · bioconductor-deseq2 · bioconductor-biocparallel · bioconductor-tximport · bioconductor-complexheatmap · multiqc |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/rnaseq](https://github.com/nf-core/rnaseq) |
| **Pinned version** | `3.26.0` |

## Run it

```bash
oxo-flow run workflow/rnaseq.toml
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned (envs/*.yaml, versions pinned to the upstream nf-core/rnaseq 3.26.0 module environments; requires conda or mamba)

**Requirements.**
- paired-end FASTQ reads: reads_dir/<sample>_R1.fastq.gz + _R2.fastq.gz, cohort declared in [[sample_groups]]
- reference genome FASTA (uncompressed)
- gene annotation GTF
- transcriptome FASTA (Salmon alignment-mode quant + StringTie)
- 12-column gene BED (RSeQC input)
- UCSC chrom.sizes file
- STAR genome index built from the same FASTA/GTF (PREPARE_GENOME is not ported; build once with STAR --runMode genomeGenerate)
- compute: up to 12 CPUs / 72 GB per rule (STAR align); most rules run on 6 CPUs / 36 GB or 1 CPU / 6 GB
- conda or mamba to create the pinned per-rule environments (envs/)

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-rnaseq
```

## Parameters

| Parameter | Default | Used by |
|---:|---|---|
| `aligner` | `star_salmon` | — |
| `chrom_sizes` | `test/fixtures/reference/chrom_sizes.txt` | `bigwig::bedclip_combined`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_combined`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev` |
| `deseq2_vst` | `true` | `quantification::deseq2_qc` |
| `extra_fqlint_args` | `--disable-validator P001` | `fastq_qc::fq_lint_raw`, `fastq_qc::fq_lint_trimmed` |
| `fasta` | `test/fixtures/reference/genome.fa` | `alignment::picard_markduplicates`, `alignment::samtools_sort`, `alignment::samtools_stats_markdup`, `alignment::samtools_stats_sorted`, `bam_qc::samtools_sort_qualimap` |
| `featurecounts_feature_type` | `exon` | `bam_qc::featurecounts` |
| `featurecounts_group_type` | `gene_biotype` | `bam_qc::featurecounts` |
| `gene_bed` | `test/fixtures/reference/gene.bed` | `bam_qc::rseqc_infer_experiment`, `bam_qc::rseqc_inner_distance`, `bam_qc::rseqc_junction_annotation`, `bam_qc::rseqc_junction_saturation`, `bam_qc::rseqc_read_distribution` |
| `gtf` | `test/fixtures/reference/genes.gtf` | `alignment::star_align`, `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `quantification::salmon_quant`, `quantification::stringtie`, `quantification::tx2gene` |
| `min_mapped_reads` | `5` | `multiqc_custom_content` |
| `min_trimmed_reads` | `10000` | `multiqc_custom_content` |
| `out_dir` | `results` | `alignment::picard_markduplicates`, `alignment::samtools_flagstat_markdup`, `alignment::samtools_flagstat_sorted`, `alignment::samtools_idxstats_markdup`, `alignment::samtools_idxstats_sorted`, `alignment::samtools_index_markdup`, `alignment::samtools_index_sorted`, `alignment::samtools_sort`, `alignment::samtools_stats_markdup`, `alignment::samtools_stats_sorted`, `alignment::star_align`, `bam_qc::biotype_multiqc`, `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `bam_qc::rseqc_bam_stat`, `bam_qc::rseqc_infer_experiment`, `bam_qc::rseqc_inner_distance`, `bam_qc::rseqc_junction_annotation`, `bam_qc::rseqc_junction_saturation`, `bam_qc::rseqc_read_distribution`, `bam_qc::rseqc_read_duplication`, `bam_qc::samtools_sort_qualimap`, `bigwig::bedclip_combined`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_combined`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev`, `bigwig::genomecov_combined`, `bigwig::genomecov_fw`, `bigwig::genomecov_rev`, `fastq_qc::fastqc_raw`, `fastq_qc::fq_lint_raw`, `fastq_qc::fq_lint_trimmed`, `fastq_qc::trimgalore`, `multiqc`, `multiqc_custom_content`, `quantification::deseq2_qc`, `quantification::salmon_quant`, `quantification::stringtie`, `quantification::summarizedexperiment`, `quantification::tx2gene`, `quantification::tximport` |
| `reads_dir` | `test/fixtures/raw` | `fastq_qc::fastqc_raw`, `fastq_qc::fq_lint_raw`, `fastq_qc::trimgalore`, `multiqc_custom_content` |
| `salmon_quant_libtype` | `` | `quantification::salmon_quant` |
| `save_align_intermeds` | `false` | — |
| `save_trimmed` | `false` | — |
| `skip_bigwig` | `false` | `bigwig::bedclip_combined`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_combined`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev`, `bigwig::genomecov_combined`, `bigwig::genomecov_fw`, `bigwig::genomecov_rev` |
| `skip_deseq2_qc` | `false` | `quantification::deseq2_qc` |
| `skip_fastqc` | `false` | `fastq_qc::fastqc_raw` |
| `skip_linting` | `false` | `fastq_qc::fq_lint_raw`, `fastq_qc::fq_lint_trimmed` |
| `skip_markduplicates` | `false` | `alignment::picard_markduplicates`, `alignment::samtools_flagstat_markdup`, `alignment::samtools_idxstats_markdup`, `alignment::samtools_index_markdup`, `alignment::samtools_stats_markdup` |
| `skip_qc` | `false` | `bam_qc::biotype_multiqc`, `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `bam_qc::rseqc_bam_stat`, `bam_qc::rseqc_infer_experiment`, `bam_qc::rseqc_inner_distance`, `bam_qc::rseqc_junction_annotation`, `bam_qc::rseqc_junction_saturation`, `bam_qc::rseqc_read_distribution`, `bam_qc::rseqc_read_duplication`, `bam_qc::samtools_sort_qualimap`, `quantification::deseq2_qc` |
| `skip_quantification_merge` | `false` | `quantification::deseq2_qc`, `quantification::summarizedexperiment`, `quantification::tximport` |
| `skip_stringtie` | `false` | `quantification::stringtie` |
| `skip_trimming` | `false` | `fastq_qc::trimgalore` |
| `star_index` | `test/fixtures/reference/star_index` | `alignment::star_align` |
| `stranded_threshold` | `0.8` | `multiqc_custom_content` |
| `strandedness` | `unstranded` | `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev`, `bigwig::genomecov_fw`, `bigwig::genomecov_rev`, `multiqc_custom_content`, `quantification::salmon_quant`, `quantification::stringtie` |
| `transcript_fasta` | `test/fixtures/reference/transcripts.fa` | `quantification::salmon_quant` |
| `unstranded_threshold` | `0.1` | `multiqc_custom_content` |

Derived from the workflow's `[config]` section — no schema file to maintain.

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
- salmon_quant
- tx2gene
- tximport
- summarizedexperiment
- stringtie
- deseq2_qc
- multiqc_custom_content
- multiqc

**Excluded**

- rsem / hisat2 / umicollapse quantification and as_quantification — non-default aligner branches, not ported
- PREPARE_GENOME — reference artifacts (fasta, gtf, transcript_fasta, gene_bed, chrom_sizes, star_index) are inputs
- per-sample min_trimmed_reads filtering — data-dependent per-sample state; only the MultiQC fail_trimmed table is produced
- UMI extraction (umitools) — --with_umi branch, off by default
- BBSplit — --skip_bbsplit default path only
- SortMeRNA / Bowtie2 rRNA removal — ribo-removal is off by default
- cat_fastq — only active for samples with more than one fastq pair
- DESeq2 QC sample-name group decomposition (Group columns for PCA-by-group plots) — coldata is the sample IDs only
- auto strandedness (per-sample inference from the samplesheet) — pipeline-level config.strandedness with forward/reverse/unstranded values only
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
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
