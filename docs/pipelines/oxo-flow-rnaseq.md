# RNA-seq: alignment, quantification and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

End-to-end bulk RNA-seq analysis for paired-end reads: fq lint and FastQC raw-read QC, TrimGalore adapter/quality trimming, STAR alignment, Picard MarkDuplicates, Salmon alignment-mode quantification with tximport-merged gene/transcript count tables and SummarizedExperiment R objects, StringTie reference-guided assembly and quantification, featureCounts gene counts with biotype tables, RSeQC / dupRadar / Qualimap QC, DESeq2 sample-level QC (PCA, sample distances, size factors), strand-specific bigWig tracks, and one final MultiQC report with the nf-core/rnaseq custom content (fail_trimmed / fail_mapped tables, strandedness checks, software versions). A faithful port of the nf-core/rnaseq 3.26.0 default star_salmon path — same tools, same versions, same commands.

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | transcriptomics |
| **Rules** | 132 |
| **Compute** | up to 12 CPUs / 72 GB per rule (STAR align) |
| **Tools** | fastqc · trim-galore · fq · star · salmon · stringtie · python · samtools · htslib · gawk · picard · subread · rseqc · r-base · bioconductor-dupradar · qualimap · bedtools · ucsc-bedclip · ucsc-bedgraphtobigwig · bioconductor-tximeta · bioconductor-summarizedexperiment · r-optparse · r-ggplot2 · r-rcolorbrewer · r-pheatmap · bioconductor-deseq2 · bioconductor-biocparallel · bioconductor-tximport · bioconductor-complexheatmap · multiqc |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/rnaseq](https://github.com/nf-core/rnaseq) |
| **Pinned version** | `3.26.0` |

## Run it

```bash
oxo-flow run main.oxoflow
```

The default config ships with `test/fixtures/` so the plan previews with no data; a real run needs your reads plus the reference artifacts under Requirements (STAR index, GTF, transcriptome, gene BED, chrom.sizes). Preview first: `oxo-flow dry-run main.oxoflow --samples first:1`.

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
#    NOTE: bioconda currently ships 0.10.2, older than the >= 0.12.0
#    minimum of every catalog entry — prefer the release binary.

# 2. get this workflow (clones the repo, auto-discovers the workflow,
#    sanity-parses it with the engine)
oxo-flow pull gh:oxo-flow-community/oxo-flow-rnaseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-rnaseq
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `aligner` | `star_salmon` | Aligner: only the upstream default 'star_salmon' path is ported. | — |
| `chrom_sizes` | `test/fixtures/reference/chrom_sizes.txt` | — | `bigwig::bedclip_combined`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_combined`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev` |
| `deseq2_vst` | `true` | DESeq2 QC transform: variance stabilizing transformation (upstream --deseq2_vst default true). | `quantification::deseq2_qc` |
| `extra_fqlint_args` | `--disable-validator P001` | fq lint extra args (upstream: --extra_fqlint_args). | `fastq_qc::fq_lint_raw`, `fastq_qc::fq_lint_trimmed` |
| `fasta` | `test/fixtures/reference/genome.fa` | Reference artifacts (upstream: --fasta / --gtf / --gene_bed / --chrom_sizes / --transcript_fasta / STAR index). PREPARE_GENOME is not ported: the STAR index is an input. transcript_fasta feeds Salmon alignment-mode quant and StringTie. | `alignment::picard_markduplicates`, `alignment::samtools_sort`, `alignment::samtools_stats_markdup`, `alignment::samtools_stats_sorted`, `bam_qc::samtools_sort_qualimap` |
| `featurecounts_feature_type` | `exon` | — | `bam_qc::featurecounts` |
| `featurecounts_group_type` | `gene_biotype` | featureCounts settings (upstream params with the same defaults). | `bam_qc::featurecounts` |
| `gene_bed` | `test/fixtures/reference/gene.bed` | — | `bam_qc::rseqc_infer_experiment`, `bam_qc::rseqc_inner_distance`, `bam_qc::rseqc_junction_annotation`, `bam_qc::rseqc_junction_saturation`, `bam_qc::rseqc_read_distribution` |
| `gtf` | `test/fixtures/reference/genes.gtf` | — | `alignment::star_align`, `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `quantification::salmon_quant`, `quantification::stringtie`, `quantification::tx2gene` |
| `min_mapped_reads` | `5` | — | `multiqc_custom_content` |
| `min_trimmed_reads` | `10000` | Thresholds (upstream params with the same defaults). | `multiqc_custom_content` |
| `out_dir` | `results` | Output directory (upstream: --outdir). | `alignment::picard_markduplicates`, `alignment::samtools_flagstat_markdup`, `alignment::samtools_flagstat_sorted`, `alignment::samtools_idxstats_markdup`, `alignment::samtools_idxstats_sorted`, `alignment::samtools_index_markdup`, `alignment::samtools_index_sorted`, `alignment::samtools_sort`, `alignment::samtools_stats_markdup`, `alignment::samtools_stats_sorted`, `alignment::star_align`, `bam_qc::biotype_multiqc`, `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `bam_qc::rseqc_bam_stat`, `bam_qc::rseqc_infer_experiment`, `bam_qc::rseqc_inner_distance`, `bam_qc::rseqc_junction_annotation`, `bam_qc::rseqc_junction_saturation`, `bam_qc::rseqc_read_distribution`, `bam_qc::rseqc_read_duplication`, `bam_qc::samtools_sort_qualimap`, `bigwig::bedclip_combined`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_combined`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev`, `bigwig::genomecov_combined`, `bigwig::genomecov_fw`, `bigwig::genomecov_rev`, `fastq_qc::fastqc_raw`, `fastq_qc::fq_lint_raw`, `fastq_qc::fq_lint_trimmed`, `fastq_qc::trimgalore`, `multiqc`, `multiqc_custom_content`, `quantification::deseq2_qc`, `quantification::salmon_quant`, `quantification::stringtie`, `quantification::summarizedexperiment`, `quantification::tx2gene`, `quantification::tximport` |
| `reads_dir` | `test/fixtures/raw` | Input reads directory: reads_dir/<sample>_R1.fastq.gz + _R2.fastq.gz (paired-end). The repo default ships the tiny committed fixtures; point this at your data. | `fastq_qc::fastqc_raw`, `fastq_qc::fq_lint_raw`, `fastq_qc::trimgalore`, `multiqc_custom_content` |
| `salmon_quant_libtype` | `` | Salmon quantification (upstream default path, alignment mode on the STAR toTranscriptome BAM). --libType is derived from config.strandedness (forward -> ISF, reverse -> ISR, unstranded -> IU); set salmon_quant_libtype to override (e.g. "A" for auto-detection). | `quantification::salmon_quant` |
| `save_align_intermeds` | `false` | — | — |
| `save_trimmed` | `false` | Publication controls (upstream: --save_trimmed / --save_align_intermeds). The port keeps trimmed FASTQs and intermediate BAMs at results/ paths regardless (they double as checkpoints); these keys are accepted for upstream parity and reserved for future use. | — |
| `skip_bigwig` | `false` | — | `bigwig::bedclip_combined`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_combined`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev`, `bigwig::genomecov_combined`, `bigwig::genomecov_fw`, `bigwig::genomecov_rev` |
| `skip_deseq2_qc` | `false` | DESeq2 sample-level QC (PCA / sample distances / size factors; upstream default path, runs on salmon.merged.gene_counts_length_scaled.tsv). | `quantification::deseq2_qc` |
| `skip_fastqc` | `false` | Skip options (upstream: --skip_fastqc / --skip_linting / --skip_trimming / --skip_markduplicates / --skip_qc / --skip_bigwig). Same defaults as upstream. NOTE: skip_trimming=true and skip_markduplicates=true break the downstream chain (trimmed reads / markdup BAM are inputs of later rules); unlike upstream there is no per-branch rewire, see README fidelity table. | `fastq_qc::fastqc_raw` |
| `skip_linting` | `false` | — | `fastq_qc::fq_lint_raw`, `fastq_qc::fq_lint_trimmed` |
| `skip_markduplicates` | `false` | — | `alignment::picard_markduplicates`, `alignment::samtools_flagstat_markdup`, `alignment::samtools_idxstats_markdup`, `alignment::samtools_index_markdup`, `alignment::samtools_stats_markdup` |
| `skip_qc` | `false` | — | `bam_qc::biotype_multiqc`, `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `bam_qc::rseqc_bam_stat`, `bam_qc::rseqc_infer_experiment`, `bam_qc::rseqc_inner_distance`, `bam_qc::rseqc_junction_annotation`, `bam_qc::rseqc_junction_saturation`, `bam_qc::rseqc_read_distribution`, `bam_qc::rseqc_read_duplication`, `bam_qc::samtools_sort_qualimap`, `quantification::deseq2_qc` |
| `skip_quantification_merge` | `false` | Cross-sample tximport merge + SummarizedExperiment RDS objects. | `quantification::deseq2_qc`, `quantification::summarizedexperiment`, `quantification::tximport` |
| `skip_stringtie` | `false` | StringTie reference-guided assembly/quantification (-G gtf, -e, ballgown). | `quantification::stringtie` |
| `skip_trimming` | `false` | — | `fastq_qc::trimgalore` |
| `star_index` | `test/fixtures/reference/star_index` | — | `alignment::star_align` |
| `stranded_threshold` | `0.8` | — | `multiqc_custom_content` |
| `strandedness` | `unstranded` | Library strandedness. Upstream reads this per-sample from the samplesheet ('auto' supported); the port is pipeline-level and supports the three explicit values only. Used by featureCounts (-s), Qualimap (-p), dupRadar and the forward/reverse bigWig gates. | `bam_qc::dupradar`, `bam_qc::featurecounts`, `bam_qc::qualimap_rnaseq`, `bigwig::bedclip_fw`, `bigwig::bedclip_rev`, `bigwig::bigwig_fw`, `bigwig::bigwig_rev`, `bigwig::genomecov_fw`, `bigwig::genomecov_rev`, `multiqc_custom_content`, `quantification::salmon_quant`, `quantification::stringtie` |
| `transcript_fasta` | `test/fixtures/reference/transcripts.fa` | — | `quantification::salmon_quant` |
| `unstranded_threshold` | `0.1` | — | `multiqc_custom_content` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-rnaseq rule-level DAG](../assets/dag/oxo-flow-rnaseq.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- bedclip_combined
- bedclip_fw
- bedclip_rev
- bigwig_combined
- bigwig_fw
- bigwig_rev
- biotype_multiqc
- deseq2_qc
- dupradar
- fastqc_raw
- featurecounts
- fq_lint_raw
- fq_lint_trimmed
- genomecov_combined
- genomecov_fw
- genomecov_rev
- multiqc
- multiqc_custom_content
- picard_markduplicates
- qualimap_rnaseq
- rseqc_bam_stat
- rseqc_infer_experiment
- rseqc_inner_distance
- rseqc_junction_annotation
- rseqc_junction_saturation
- rseqc_read_distribution
- rseqc_read_duplication
- salmon_quant
- samtools_flagstat_markdup
- samtools_flagstat_sorted
- samtools_idxstats_markdup
- samtools_idxstats_sorted
- samtools_index_markdup
- samtools_index_sorted
- samtools_sort
- samtools_sort_qualimap
- samtools_stats_markdup
- samtools_stats_sorted
- star_align
- stringtie
- summarizedexperiment
- trimgalore
- tx2gene
- tximport

**Excluded**

- RSEM as_quantification mode — port runs the upstream default --alignments mode
- PREPARE_GENOME reference-artifact prep — fasta/gtf/transcript_fasta/gene_bed/chrom_sizes are pipeline inputs; the branch index builders ARE ported
- per-sample min_trimmed_reads filtering — data-dependent per-sample state; only the MultiQC fail_trimmed table is produced
- cat_fastq — one-pair-per-sample model
- auto strandedness inference — inferred strandedness has no static-DAG consumer
- DESeq2 QC group decomposition — Nextflow-rendered
- workflow_summary_mqc.yaml / methods_description_mqc.yaml — Nextflow-rendered; static version manifest shipped instead

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
| 2 | `PREPARE_GENOME` prepares the reference artifacts (fasta, gtf, transcript_fasta, gene_bed, chrom_sizes) and builds the branch indexes (STAR / HISAT2 / RSEM / Salmon) | The artifacts are inputs; the index BUILDERS are ported: STAR via the `[[references]]` builder, HISAT2 / RSEM / Salmon via when-gated builder rules that build from the shipped fixtures when the config key is empty and symlink a user-supplied directory otherwise | The artifact prep stays excluded as infra; index building is now part of the run (see the fidelity rows below) |
| 3 | Non-default branches: `star_rsem`, `hisat2`, `bowtie2_salmon`, `--with_umi`, `--pseudo_aligner salmon`, `--pseudo_aligner kallisto` | Ported — see rows 16-27 for their deviations | Only the RSEM `as_quantification` mode remains excluded |
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
| 15 | UMI extraction (`umitools`), BBSplit, SortMeRNA/Bowtie2 rRNA removal | Ported as when-gated rules (off by default, same gates as upstream: `with_umi` / `!skip_bbsplit` / `remove_ribo_rna` + `ribo_removal_tool`) | The four trimmed-read variants each feed the aligners, quantification and MultiQC exactly like upstream; `cat_fastq` (multi-fastq-sample branch) remains excluded |
| 16 | UMI transcriptome intermediates are unpublished Nextflow work-dir files (`{id}.bam`, `{id}.sorted.bam`, `{id}.filtered.bam` from `bam_dedup_umi`'s SAMTOOLS_SORT / UMITOOLS_PREPAREFORRSEM) | Stable canonical names: `{sample}.transcriptome.sorted.bam` → `{sample}.umi_dedup.transcriptome.sorted.bam` → `{sample}.umi_dedup.transcriptome.bam` → `{sample}.umi_dedup.transcriptome.filtered.bam` | oxo-flow has no work dirs; every intermediate is a declared output. Published names are unchanged upstream (logs, stats, prepared BAM) |
| 17 | UMI dedup outputs are tool-specific upstream (`{prefix}.dedup.bam` from UMITOOLS_DEDUP, `{prefix}.UMICollapse.bam` from UMICOLLAPSE) | All four umitools variants and the umicollapse variant write the shared path `{sample}.markdup.sorted.bam` (exclusive when-gates; downstream rules resolve one path) | Duplicate-output exclusive-gate idiom — same published artifact set per config; the `.log` / `_UMICollapse.log` logs keep their tool-specific names |
| 18 | Transcriptome-side BAM stats (`samtools_stats` for `{prefix}.umi_dedup.transcriptome.sorted.bam`) | Only the dedup-side stats are ported (`{aligner}/samtools_stats/{sample}.umi_dedup.transcriptome.sorted.bam.{stats,flagstat,idxstats}`); the coordinate-sorted index + sort-side stats are not | Sort-side stats and the index are unpublished upstream unless `--save_umi_intermeds`; dedup-side stats publish unconditionally. MultiQC excludes the transcriptome stats upstream too (`bam_dedup_umi` never mixes them into `multiqc_files`) — the port mirrors that |
| 19 | `RSEM_PREPAREREFERENCE` emits `transcripts.fa` next to the index | The `rsem_index` builder does not emit it | Nothing in the RSEM chain consumes `transcripts.fa`; the align-mode RSEM input is the toTranscriptome BAM |
| 20 | `STAR_ALIGN` passes no `--limitBAMsortRAM` | The port adds `--limitBAMsortRAM $(( effective_memory_mb * 1000000 ))` | Without it STAR's 50 GB default sort-RAM cap can fail on small hosts; the value is derived from the rule's memory like every other engine resource |
| 21 | `HISAT2_EXTRACTSPLICESITES` names the splice-site file after the GTF (`{gtf.baseName}.splice_sites.txt`) | Fixed canonical path `reference/genes.splice_sites.txt` | The port's hisat2 index builder and align rules consume it; the align command's `--rna-strandness` is rendered via a shell branch (FR forward / RF reverse / omitted unstranded — same values as the upstream `meta.strandedness` branch) |
| 22 | `SALMON_QUANT` (alignment mode) runs without `--no-version-check` | The port adds `--no-version-check` | Pre-existing port-wide deviation kept for consistency across all salmon quant rules (bam / umi / pseudo) |
| 23 | RSEM tximport reads the flat per-sample `*.isoforms.results` files; `DESEQ2_QC_RSEM` passes `--id_col 1 --sample_suffix '' --count_col 3` via the rsem deseq2 config | `tx2gene_rsem` stages the first sample's `isoforms.results` into a flat dir (same first-sample semantics as the salmon tx2gene); `deseq2_qc_rsem` passes the three args explicitly | The args equal the port script defaults but are passed explicitly for parity; the flat staging preserves the upstream first-sample `.first()` semantics |
| 24 | `bowtie2_salmon` aligner: `BOWTIE2_ALIGN` (sort_bam=false → `samtools view` keeps the query-grouped orig_bam) → `BAM_SORT_STATS_SAMTOOLS` → `QUANTIFY_BAM_SALMON` on the orig_bam; the BAM-chain prefix is hardcoded `salmon.merged` | Ported as `alignment::bowtie2_index` + `bowtie2_align` (+3 read-source variants) + `samtools_sort_bowtie2`; `quantification::salmon_quant_bowtie2` quantifies the orig_bam (`-t transcript_fasta -a orig_bam`); tx2gene/tximport/SE/DESeq2 share the star_salmon rules via widened when-gates | The upstream `salmon.merged` prefix quirk is preserved (quantify_bam_salmon.config hardcodes it for both aligners); the UMI transcriptome chain (`bam_sort_transcriptome_bowtie2` → dedup → `salmon_quant_umi`) mirrors the STAR chain; the MultiQC fail_mapped table keeps the hardcoded `STAR uniquely mapped reads (%)` header with the percent parsed from `{id}.bowtie2.log` ("N% overall alignment rate") — an upstream quirk of multiqc_rnaseq |
| 25 | `kallisto` pseudo-aligner: `KALLISTO_INDEX` (`kallisto index -k 31 -i kallisto tx.fa`, process_medium) + `KALLISTO_QUANT` (process_high, `--gtf`, `--fr/--rf-stranded` from strandedness, `2> >(tee log)`) | Ported as `quantification::kallisto_index` + `kallisto_quant_pseudo` (+3 read-source variants) reusing the salmon pseudo branch's when gates; tx2gene/tximport/SE/DESeq2 pseudo rules are shared via widened when-gates with the tool label (`--quant-type`, MultiQC `KALLISTO DESeq2 ...` labels) | The port scripts (tx2gene.py / tximport.r) already handle kallisto (`abundance.tsv`, `dropInfReps=TRUE`); `-k` comes from `config.pseudo_aligner_kmer_size` (upstream default 31); extra_kallisto_quant_args stays at the upstream default (null) |
| 26 | `KALLISTO_QUANT` logs: upstream publishes the work-dir `{prefix}.log` (the `.run_info.json` and `.log` copies are unpublished, saveAs null) and feeds MultiQC from the work dir | The port declares `{pseudo_aligner}/<id>/kallisto_quant.log` as a rule output and stages it into MultiQC as `<id>.kallisto_quant.log` | oxo-flow has no work dirs, so the log must be a declared output to reach MultiQC; the MultiQC kallisto module matches by content ("[quant] finding pseudoalignments for the reads"), so the per-sample rename is safe |
| 27 | `DESEQ2_QC_PSEUDO` MultiQC labels come from `params.pseudo_aligner` (SALMON / KALLISTO) | The port derives the label from `config.pseudo_aligner` at render time (`tr [:lower:] [:upper:]`) | Config-derived label — same value as upstream's param-derived label |

**Not ported (metadata `excluded`):**

The RSEM `as_quantification` mode (upstream `--aligner star_rsem --rsem_as_quantification`: a mode-level rewrite of the whole quantification branch, not a composable branch); `PREPARE_GENOME` reference-artifact prep (fasta, gtf, transcript_fasta, gene_bed, chrom_sizes are inputs; the branch index builders ARE ported — see row 2); per-sample `min_trimmed_reads` filtering (data-dependent per-sample state; only the MultiQC fail_trimmed table is produced); `cat_fastq` (only active for samples with more than one fastq pair — not expressible in the port's one-pair-per-sample sample model); `auto` strandedness (per-sample inference from the samplesheet — the inferred per-sample value has no consumer in a static DAG); the DESeq2 QC sample-name group decomposition (Group columns for PCA-by-group plots); the Nextflow-param-rendered MultiQC sections (`workflow_summary_mqc.yaml` / `methods_description_mqc.yaml`).

**Test fixtures** (reworked live, engine 0.15.0): 60 genes (DESeq2's dispersion fit needs gene support — 4 genes x 6 samples still failed `estimateDispersionsFit`) spread 100x apart (contiguous aligners like bowtie2 collide on packed genes — live: 64% Picard duplicates, dupRadar density NaN); unique read fragments only (random draws over 400 bp exons collided massively — 64% duplicates live, dupRadar bandwidth NaN); log-normal expression-weighted reads with PCR duplicates biased to high-expression genes (~5% overall, like real data — a uniform dup rate collapsed dupRadar's density bandwidth); FR-oriented mates with identical read names (`@S1_1` — forward-forward mates made STAR classify every pair as 'too short'). bowtie2_salmon live note (engine 0.15.0): under a contiguous aligner the ~30% spliced fixture reads map clipped and their positional collisions dominate dupRadar's density plot — `duprateExpDensPlot` dies with a NaN bandwidth (upstream script unchanged); alignment, Salmon quant and DESeq2 all pass; the dupRadar density plot needs real-library data.

## Links

- Repository: [oxo-flow-rnaseq](https://github.com/oxo-flow-community/oxo-flow-rnaseq)
- Upstream: [nf-core/rnaseq](https://github.com/nf-core/rnaseq) @ `3.26.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
