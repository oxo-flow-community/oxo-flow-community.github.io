# Bisulfite methylation analysis: alignment, methylation calls and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Run end-to-end bisulfite methylation analysis (WGBS, and RRBS-compatible) of paired-end reads (default) and single-end reads (upstream single_end samplesheet column, via the engine metadata binding): FastQC quality control, TrimGalore adapter trimming, alignment to the bisulfite-converted reference genome with any of the four upstream aligners — Bismark bowtie2 (default), Bismark hisat2, bwameth (bwa-meth) or BWA-MEM — PCR-deduplication, samtools sort/index, methylation calls (bismark_methylation_extractor, MethylDackel on bwameth, rastair for TAPS), per-sample and project-wide Bismark HTML reports, optional QualiMap BamQC, preseq complexity estimates and targeted-sequencing (bedtools intersect + Picard HS metrics), and a final MultiQC report. All optional branches are gated on the same config keys as the upstream params and off by default.

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 61 |
| **Compute** | up to 12 CPUs / 72 GB per rule (genome preparation, index builds, trimgalore, aligners, deduplicate, extractor) |
| **Tools** | fastqc · trim-galore · cutadapt · pigz · bismark · samtools · htslib · bwa · bwameth · picard · methyldackel · rastair · qualimap · preseq · bedtools · multiqc · gzip · tar · coreutils · r-base |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/methylseq](https://github.com/nf-core/methylseq) |
| **Pinned version** | `4.2.0` |

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs reference genome and reads — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.17.0

**Toolchain.** conda envs — pinned versions (conda-forge/bioconda)

**Requirements.**
- reference genome FASTA (a .gz FASTA is decompressed automatically before indexing) — the Bismark bowtie2 index is built automatically on first run; a prebuilt index archive (--bismark_index) is also supported
- paired-end raw reads: <dir>/<sample>_R1.fastq.gz and <dir>/<sample>_R2.fastq.gz (samples with >1 pair: <dir>/<sample>_<unit>_R{1,2}.fastq.gz per unit — concatenated by cat_fastq); single-end samples: <dir>/<sample>_R1.fastq.gz only, listed as SE in metadata/samples.tsv with config.single_end_mode = true
- compute: up to 12 CPUs / 72 GB RAM per rule (bismark_genomepreparation, trimgalore, bismark_align, bismark_deduplicate, bismark_methylationextractor, bwameth_index, bwameth_align, bwa_mem)
- conda or mamba to create the pinned per-rule environments
- disk: space in config.out_dir (default results/) for aligned BAMs, methylation calls and reports

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-methylseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-methylseq
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `accel` | `false` | — | `trimgalore`, `trimgalore_se` |
| `aligner` | `bismark` | Aligner (upstream: --aligner, default 'bismark'). One of: 'bismark'       - bowtie2, the default main path 'bismark_hisat' - hisat2 (needs a --known_splices GTF for splice sites) 'bwameth'       - bwa-meth (needs a --use_mem2 flag to use the mem2 index) 'bwamem'        - BWA-MEM (TAPS-optimized) | `bedtools_intersect`, `bedtools_intersect_bwameth`, `bedtools_intersect_bwameth_chg`, `bedtools_intersect_bwameth_chh`, `bismark_align`, `bismark_align_se`, `bismark_coverage2cytosine`, `bismark_deduplicate`, `bismark_deduplicate_se`, `bismark_genomepreparation`, `bismark_methylationextractor`, `bismark_methylationextractor_se`, `bismark_report`, `bismark_report_se`, `bismark_summary`, `bismark_untar`, `bwa_index`, `bwa_mem`, `bwameth_align`, `bwameth_index`, `methyldackel_extract`, `methyldackel_extract_allcontexts`, `methyldackel_extract_methylkit`, `methyldackel_mbias`, `multiqc`, `multiqc_bwamem`, `multiqc_bwameth`, `picard_addorreplacereadgroups`, `picard_collecthsmetrics`, `picard_collecthsmetrics_alt`, `picard_markduplicates`, `picard_markduplicates_bwamem`, `preseq_lcextrap`, `preseq_lcextrap_alt`, `qualimap_bamqc`, `qualimap_bamqc_alt`, `rastair_call_bwamem`, `rastair_call_bwameth`, `rastair_mbias_bwamem`, `rastair_mbias_bwameth`, `rastair_mbiasparser`, `rastair_methylkit`, `samtools_faidx`, `samtools_flagstat`, `samtools_idxstats`, `samtools_index`, `samtools_index_alignment`, `samtools_index_deduplicated`, `samtools_index_deduplicated_bwamem`, `samtools_sort`, `samtools_sort_alignment`, `samtools_stats` |
| `all_contexts` | `false` | Methyldackel options (upstream params with the same defaults, active on the bwameth branch when TAPS is off) | `bedtools_intersect_bwameth_chg`, `bedtools_intersect_bwameth_chh`, `methyldackel_extract`, `methyldackel_extract_allcontexts`, `methyldackel_extract_methylkit`, `methyldackel_mbias` |
| `bamqc_regions_file` | `` | — | `qualimap_bamqc`, `qualimap_bamqc_alt` |
| `bismark_index` | `` | Prebuilt Bismark index archive (.tar.gz/.tar.bz2, as produced by bismark_genome_preparation). Empty string (default) = build the index from config.fasta (upstream default). When set, the archive is untarred into refs/BismarkIndex and the build is skipped, like the upstream UNTAR module. | `bismark_genomepreparation`, `bismark_untar` |
| `cat_fastq` | `true` | Concatenate multi-pair fastqs (upstream: CAT_FASTQ — always active for samples with >1 fastq pair; upstream has no param for it). Set to false only when every sample has a single pair: multi-pair samples would then lack the merged reads the downstream rules consume. | `cat_fastq_r1`, `cat_fastq_r2` |
| `clip_r1` | `0` | Trimming options (upstream params with the same defaults) | `trimgalore`, `trimgalore_se` |
| `clip_r2` | `0` | — | `trimgalore` |
| `collecthsmetrics` | `false` | Collect Picard HS metrics within the targeted-sequencing branch (upstream: --collecthsmetrics, default false) | `multiqc`, `multiqc_bwameth`, `picard_bedtointervallist`, `picard_collecthsmetrics`, `picard_collecthsmetrics_alt`, `picard_createsequencedictionary`, `samtools_faidx` |
| `comprehensive` | `true` | The port's DAG consumes the merged (--comprehensive) methylation-call outputs, so the default differs from upstream (false): the per-strand split files would leave the declared outputs unmoved. | `bismark_methylationextractor`, `bismark_methylationextractor_se` |
| `cytosine_report` | `false` | Bismark options | `bismark_coverage2cytosine` |
| `em_seq` | `false` | — | `bismark_align`, `trimgalore`, `trimgalore_se` |
| `fasta` | `test/fixtures/refs/genome.fa` | Reference genome (upstream: --fasta). Uncompressed FASTA (a .gz FASTA is decompressed automatically before indexing, like the upstream GUNZIP module). The Bismark index is built from it automatically (upstream default when --bismark_index is not supplied). Point this at your genome; the repo default ships the tiny test fixture. | `bismark_genomepreparation`, `bwa_index`, `bwameth_align`, `bwameth_index`, `samtools_faidx` |
| `ignore_3prime_r1` | `0` | — | `bismark_methylationextractor`, `bismark_methylationextractor_se` |
| `ignore_3prime_r2` | `2` | — | `bismark_methylationextractor` |
| `ignore_flags` | `false` | — | `methyldackel_extract`, `methyldackel_extract_allcontexts`, `methyldackel_extract_methylkit`, `methyldackel_mbias` |
| `ignore_r1` | `0` | — | `bismark_methylationextractor`, `bismark_methylationextractor_se` |
| `ignore_r2` | `2` | — | `bismark_methylationextractor` |
| `known_splices` | `` | bismark_hisat splice-site GTF (upstream: --known_splices, default empty). When set and aligner = 'bismark_hisat', bismark is given the splice sites extracted from this file (upstream uses process substitution for the same data). | `bismark_align`, `bismark_align_se` |
| `length_trim` | `0` | — | `trimgalore`, `trimgalore_se` |
| `local_alignment` | `false` | — | `bismark_align`, `bismark_align_se` |
| `maxins` | `` | — | `bismark_align` |
| `merge_context` | `false` | — | `methyldackel_extract`, `methyldackel_extract_allcontexts`, `methyldackel_extract_methylkit` |
| `meth_cutoff` | `` | — | `bismark_methylationextractor`, `bismark_methylationextractor_se` |
| `methyl_kit` | `false` | — | `methyldackel_extract_methylkit` |
| `min_depth` | `0` | — | `methyldackel_extract`, `methyldackel_extract_allcontexts`, `methyldackel_extract_methylkit` |
| `minins` | `` | — | `bismark_align` |
| `multiqc_title` | `` | MultiQC | `multiqc`, `multiqc_bwamem`, `multiqc_bwameth` |
| `nextseq_trim` | `0` | — | `trimgalore`, `trimgalore_se` |
| `no_overlap` | `true` | — | `bismark_methylationextractor` |
| `nomeseq` | `false` | — | `bismark_coverage2cytosine`, `bismark_methylationextractor`, `bismark_methylationextractor_se` |
| `non_directional` | `false` | — | `bismark_align`, `bismark_align_se` |
| `num_mismatches` | `0.6` | — | `bismark_align`, `bismark_align_se` |
| `out_dir` | `results` | — | `bedtools_intersect`, `bedtools_intersect_bwameth`, `bedtools_intersect_bwameth_chg`, `bedtools_intersect_bwameth_chh`, `bismark_align`, `bismark_align_se`, `bismark_coverage2cytosine`, `bismark_deduplicate`, `bismark_deduplicate_se`, `bismark_methylationextractor`, `bismark_methylationextractor_se`, `bismark_report`, `bismark_report_se`, `bismark_summary`, `bwa_mem`, `bwameth_align`, `cat_fastq_r1`, `cat_fastq_r2`, `fastqc`, `fastqc_se`, `methyldackel_extract`, `methyldackel_extract_allcontexts`, `methyldackel_extract_methylkit`, `methyldackel_mbias`, `multiqc`, `multiqc_bwamem`, `multiqc_bwameth`, `multiqc_versions`, `picard_addorreplacereadgroups`, `picard_bedtointervallist`, `picard_collecthsmetrics`, `picard_collecthsmetrics_alt`, `picard_markduplicates`, `picard_markduplicates_bwamem`, `preseq_lcextrap`, `preseq_lcextrap_alt`, `qualimap_bamqc`, `qualimap_bamqc_alt`, `rastair_call_bwamem`, `rastair_call_bwameth`, `rastair_mbias_bwamem`, `rastair_mbias_bwameth`, `rastair_mbiasparser`, `rastair_methylkit`, `samtools_flagstat`, `samtools_idxstats`, `samtools_index`, `samtools_index_alignment`, `samtools_index_deduplicated`, `samtools_index_deduplicated_bwamem`, `samtools_sort`, `samtools_sort_alignment`, `samtools_stats`, `trimgalore`, `trimgalore_se` |
| `pbat` | `false` | — | `bismark_align`, `bismark_align_se`, `trimgalore`, `trimgalore_se` |
| `raw_dir` | `test/fixtures/raw` | Input reads directory: raw/<sample>_R1.fastq.gz + _R2.fastq.gz (paired-end). The repo default ships the tiny test fixtures; point this at your data. | `fastqc`, `fastqc_se`, `trimgalore`, `trimgalore_se` |
| `relax_mismatches` | `false` | — | `bismark_align`, `bismark_align_se` |
| `rrbs` | `false` | Library presets (upstream params with the same defaults). | `bismark_deduplicate`, `bismark_deduplicate_se`, `multiqc_bwameth`, `picard_markduplicates`, `samtools_index_deduplicated`, `trimgalore`, `trimgalore_se` |
| `run_preseq` | `false` | — | `multiqc`, `multiqc_bwamem`, `multiqc_bwameth`, `preseq_lcextrap`, `preseq_lcextrap_alt` |
| `run_qualimap` | `false` | Optional QC branches (upstream params, all off by default) | `multiqc`, `multiqc_bwamem`, `multiqc_bwameth`, `qualimap_bamqc`, `qualimap_bamqc_alt` |
| `run_targeted_sequencing` | `false` | — | `bedtools_intersect`, `bedtools_intersect_bwameth`, `bedtools_intersect_bwameth_chg`, `bedtools_intersect_bwameth_chh`, `multiqc`, `multiqc_bwameth`, `picard_bedtointervallist`, `picard_collecthsmetrics`, `picard_collecthsmetrics_alt`, `picard_createsequencedictionary` |
| `single_cell` | `false` | — | `bismark_align`, `bismark_align_se`, `trimgalore`, `trimgalore_se` |
| `single_end_mode` | `false` | Single-end reads (upstream: the samplesheet `single_end` column, absent fastq_2 -> single_end). Off by default (all samples paired-end, the byte-identical default). Set to true AND uncomment [workflow] metadata_file to route samples per-row: metadata/samples.tsv lists each sample's `endedness` (SE or PE); a sample without a row — or with no metadata_file at all — stays paired-end. The SE branches are separate gated rules mirroring the upstream per-sample routing (bismark chain: fastqc_se -> trimgalore_se -> bismark_align_se -> bismark_deduplicate_se -> bismark_methylationextractor_se -> bismark_report_se; the bwameth/ bwamem aligners take the trimmed single read directly). Requires oxo-flow >= 0.17.0: on older engines `{meta.*}` is inert, so the SE rules stay closed while this key is false. | `bismark_align_se`, `bismark_deduplicate_se`, `bismark_methylationextractor_se`, `bismark_report_se`, `fastqc_se`, `trimgalore_se` |
| `skip_deduplication` | `false` | — | `bismark_deduplicate`, `bismark_deduplicate_se`, `multiqc_bwamem`, `multiqc_bwameth`, `picard_addorreplacereadgroups`, `picard_markduplicates`, `picard_markduplicates_bwamem`, `samtools_index_deduplicated`, `samtools_index_deduplicated_bwamem` |
| `skip_fastqc` | `false` | Skip options (upstream: --skip_fastqc / --skip_trimming / --skip_deduplication / --skip_multiqc). Same defaults as upstream. | `fastqc`, `fastqc_se` |
| `skip_multiqc` | `false` | — | `multiqc`, `multiqc_bwamem`, `multiqc_bwameth` |
| `skip_trimming` | `false` | — | `trimgalore`, `trimgalore_se` |
| `skip_trimming_presets` | `false` | — | `trimgalore`, `trimgalore_se` |
| `slamseq` | `false` | — | `bismark_genomepreparation` |
| `taps` | `false` | TAPS protocol (upstream: --taps, default false). Runs rastair conversion on the alignments. Only meaningful with the bwameth or bwamem aligners (upstream builds no fasta index for TAPS on the bismark aligners, so rastair silently produces nothing there — replicated). | `bedtools_intersect`, `bedtools_intersect_bwameth`, `bedtools_intersect_bwameth_chg`, `bedtools_intersect_bwameth_chh`, `methyldackel_extract`, `methyldackel_extract_allcontexts`, `methyldackel_extract_methylkit`, `methyldackel_mbias`, `picard_collecthsmetrics`, `picard_collecthsmetrics_alt`, `rastair_call_bwameth`, `rastair_mbias_bwameth`, `rastair_mbiasparser`, `rastair_methylkit` |
| `target_regions_file` | `` | Targeted-sequencing inputs (upstream: --target_regions_file / --bamqc_regions_file, default empty) | `bedtools_intersect`, `bedtools_intersect_bwameth`, `bedtools_intersect_bwameth_chg`, `bedtools_intersect_bwameth_chh`, `picard_bedtointervallist` |
| `three_prime_clip_r1` | `0` | — | `trimgalore`, `trimgalore_se` |
| `three_prime_clip_r2` | `0` | — | `trimgalore` |
| `unmapped` | `false` | — | `bismark_align`, `bismark_align_se` |
| `use_mem2` | `false` | bwameth index variant (upstream: --use_mem2, default false). | `bwameth_index` |
| `zymo` | `false` | — | `bismark_align`, `bismark_align_se`, `trimgalore`, `trimgalore_se` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-methylseq rule-level DAG](../assets/dag/oxo-flow-methylseq.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- bismark_genomepreparation
- bismark_untar
- bwameth_index
- bwa_index
- samtools_faidx
- cat_fastq_r1
- cat_fastq_r2
- fastqc
- fastqc_se
- trimgalore
- trimgalore_se
- bismark_align
- bismark_align_se
- bwameth_align
- bwa_mem
- samtools_sort
- samtools_sort_alignment
- samtools_index
- samtools_index_alignment
- samtools_flagstat
- samtools_stats
- samtools_idxstats
- bismark_deduplicate
- bismark_deduplicate_se
- picard_markduplicates
- samtools_index_deduplicated
- picard_addorreplacereadgroups
- picard_markduplicates_bwamem
- samtools_index_deduplicated_bwamem
- bismark_methylationextractor
- bismark_methylationextractor_se
- methyldackel_extract
- methyldackel_extract_allcontexts
- methyldackel_extract_methylkit
- methyldackel_mbias
- rastair_mbias_bwameth
- rastair_mbias_bwamem
- rastair_mbiasparser
- rastair_call_bwameth
- rastair_call_bwamem
- rastair_methylkit
- bismark_coverage2cytosine
- bismark_report
- bismark_report_se
- bismark_summary
- qualimap_bamqc
- qualimap_bamqc_alt
- preseq_lcextrap
- preseq_lcextrap_alt
- picard_createsequencedictionary
- picard_bedtointervallist
- bedtools_intersect
- bedtools_intersect_bwameth
- bedtools_intersect_bwameth_chg
- bedtools_intersect_bwameth_chh
- picard_collecthsmetrics
- picard_collecthsmetrics_alt
- multiqc_versions
- multiqc
- multiqc_bwameth
- multiqc_bwamem

**Excluded**

- none

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|
| CAT_FASTQ | `cat_fastq_r1` / `cat_fastq_r2` | coreutils 9.5 | ported via the engine's `input_groups` primitive (issue #227, oxo-flow >= 0.17.0): one instance per sample with >1 fastq pair, R1s and R2s concatenated into `results/fastq/<sample>_R{1,2}.fastq.gz`; single-pair samples pass through unchanged (downstream falls back to the raw pair). Upstream's single process is split into two rules (one per read); see deviations |
--|
| FASTQC | `fastqc` / `fastqc_se` | fastqc 0.12.1 | identical command; `--memory` derived from task resources. The `_se` variant runs the single-end chain (reads named `{sample}.fastq.gz`, outputs `{sample}_fastqc.*`) when `single_end_mode` is on |
| TRIMGALORE | `trimgalore` / `trimgalore_se` | trim-galore 0.6.10, cutadapt 4.9, pigz 2.8 | identical command incl. library-preset clipping and `--cores` clamp. The `_se` variant is the upstream SE module: R1-side clipping only, `--cores cpus-3` clamped to [1, 8] |
| BISMARK_GENOMEPREPARATION | `bismark_genomepreparation` | bismark 0.25.1, gzip 1.13 | `--bowtie2` (or `--hisat2` for bismark_hisat, `--slam` for slamseq); runs when no prebuilt index is supplied (upstream default) |
| GUNZIP | (merged into the index-preparation shells) | gzip 1.13 | a gzipped reference FASTA is decompressed before index building, as in the upstream fasta_index_methylseq subworkflow |
| UNTAR | `bismark_untar` | tar 1.34 | active only when a prebuilt `--bismark_index` archive is supplied; strips a single top-level directory, like upstream |
| BISMARK_ALIGN | `bismark_align` / `bismark_align_se` | bismark 0.25.1 | identical flag order (pbat/non_directional/unmapped/score_min/local/minins/maxins/multicore); hisat2 splice sites via `known_splices` (see deviations). The `_se` variant drops `--minins`/`--maxins` (upstream `!meta.single_end` gate), keeps `--multicore` and the hisat2 rename |
| BISMARK_DEDUPLICATE | `bismark_deduplicate` / `bismark_deduplicate_se` | bismark 0.25.1 | identical command (`-s` for single-end, `-p` paired-end); skipped with `skip_deduplication`/`rrbs` like upstream |
| SAMTOOLS_SORT | `samtools_sort` | samtools 1.22.1, htslib 1.22.1 | upstream prefix `${sample}.deduplicated.sorted`; takes the SE deduplicated BAM when the sample is single-end |
| SAMTOOLS_INDEX | `samtools_index` | samtools 1.22.1 | identical command |
| BISMARK_METHYLATIONEXTRACTOR | `bismark_methylationextractor` / `bismark_methylationextractor_se` | bismark 0.25.1 | identical flag order on the **deduplicated** BAM; `--multicore`/`--buffer_size` derived from resources. The `_se` variant uses `-s` and drops `--no_overlap`/`--ignore_r2`/`--ignore_3prime_r2` (upstream `!meta.single_end` gate) |
| BISMARK_COVERAGE2CYTOSINE | `bismark_coverage2cytosine` | bismark 0.25.1 | off by default; runs with `cytosine_report`/`nomeseq`; takes the SE coverage file when the sample is single-end |
| BISMARK_REPORT | `bismark_report` / `bismark_report_se` | bismark 0.25.1 | bismark2report run with the four reports co-located, as in the upstream workdir; the `_se` variant feeds the `*_SE_report.txt` files |
| BISMARK_SUMMARY | `bismark_summary` | bismark 0.25.1 | bismark2summary with upstream BAM-name arguments; per-sample SE/PE detection via a `[ -f ]` probe on the SE alignment report (no per-sample binding) |
| BWAMETH_INDEX | `bwameth_index` | bwameth 0.2.9 | `bwameth.py index`, or `index-mem2` with `use_mem2`; index dir `refs/BwamethIndex` |
| BWAMETH_ALIGN | `bwameth_align` | bwameth 0.2.9 | identical command (reference symlink re-created in the index dir, `samtools view -bhS`); one or two reads are passed positionally per sample (SE/PE from its metadata row) |
| BWA_INDEX | `bwa_index` | bwa 0.7.19 | `bwa index -p`; upstream sizes memory dynamically (5.37x FASTA) — the port uses a fixed 4 threads/24G/24h budget (see deviations) |
| BWA_MEM | `bwa_mem` | bwa 0.7.19, samtools 1.22.1 | upstream `sort_bam = true`: `bwa mem \| samtools sort`; index prefix found by globbing `*.amb`; one or two reads passed positionally per sample (SE/PE) |
| SAMTOOLS_INDEX_ALIGNMENTS | `samtools_index_alignment` | samtools 1.22.1 | index of the sorted alignment BAM (bwameth/bwamem) |
| SAMTOOLS_FLAGSTAT | `samtools_flagstat` | samtools 1.22.1 | identical command |
| SAMTOOLS_STATS | `samtools_stats` | samtools 1.22.1 | identical command |
| SAMTOOLS_IDXSTATS | `samtools_idxstats` | samtools 1.22.1 | bwamem branch; `--threads cpus-1` as upstream |
| PICARD_MARKDUPLICATES | `picard_markduplicates` / `picard_markduplicates_bwamem` | picard 3.4.0 | identical args (ASSUME_SORTED/REMOVE_DUPLICATES/LENIENT/PROGRAM_RECORD_ID null/TMP_DIR); -Xmx = 0.8 x memory |
| PICARD_ADDORREPLACEREADGROUPS | `picard_addorreplacereadgroups` | picard 3.4.0 | identical args; upstream does not publish this BAM — the port declares it so the DAG can consume it |
| SAMTOOLS_INDEX_DEDUPLICATED | `samtools_index_deduplicated` / `samtools_index_deduplicated_bwamem` | samtools 1.22.1 | index of the deduplicated BAM |
| METHYLDACKEL_EXTRACT | `methyldackel_extract` (+ `_allcontexts`, `_methylkit`) | methyldackel 0.6.1 | same flags (CHG/CHH, mergeContext, ignoreFlags, minDepth, methylKit); the methylKit table and the all-contexts bedGraphs are separate gated rules (see deviations) |
| METHYLDACKEL_MBIAS | `methyldackel_mbias` | methyldackel 0.6.1 | identical command |
| RASTAIR_MBIAS | `rastair_mbias_bwameth` / `rastair_mbias_bwamem` | rastair 0.8.2 | active with `taps` on bwameth and always on bwamem, exactly like the upstream `if (params.taps \|\| aligner == 'bwamem')` |
| RASTAIR_MBIASPARSER | `rastair_mbiasparser` | rastair 0.8.2, r-base 4.4.0 | plot_mbias.R + parse_mbias.R |
| RASTAIR_CALL | `rastair_call_bwameth` / `rastair_call_bwamem` | rastair 0.8.2 | trim values flow from the mbiasparser CSV (see deviations) |
| RASTAIR_METHYLKIT | `rastair_methylkit` | rastair 0.8.2 | `rastair_call_to_methylkit.sh \| gzip` |
| QUALIMAP_BAMQC | `qualimap_bamqc` / `qualimap_bamqc_alt` | qualimap 2.3 | `-p non-strand-specific`, `--gff` with `bamqc_regions_file`, `_JAVA_OPTIONS` tmpdir; `--collect-overlap-pairs` only for paired-end samples (upstream `!meta.single_end` gate) |
| PRESEQ_LCEXTRAP | `preseq_lcextrap` / `preseq_lcextrap_alt` | preseq 3.2.0 | `-verbose -bam`, `-pe` only for paired-end samples (upstream `!meta.single_end` gate); the `*.command.log` is preseq's own stderr (see deviations) |
| PICARD_CREATESEQUENCEDICTIONARY | `picard_createsequencedictionary` | picard 3.4.0 | runs only when `collecthsmetrics` is requested, like upstream |
| PICARD_BEDTOINTERVALLIST | `picard_bedtointervallist` | picard 3.4.0 | output named `target_regions.intervallist` (fixed name; see deviations) |
| BEDTOOLS_INTERSECT | `bedtools_intersect` (+ `_bwameth`, `_chg`, `_chh`) | bedtools 2.31.1 | prefix = the bedGraph basename, suffix `targeted.bedGraph`, as upstream; the bismark variant takes the SE bedGraph when the sample is single-end |
| PICARD_COLLECTHSMETRICS | `picard_collecthsmetrics` / `picard_collecthsmetrics_alt` | picard 3.4.0 | same intervals for bait and target; excluded on the taps/bwamem branches, like the upstream rastair error |
| SAMTOOLS_FAIDX | `samtools_faidx` | samtools 1.22.1, htslib 1.22.1, gzip 1.13 | stages the reference at `refs/FastaRef/reference.fa`; upstream gate (bwameth/bwamem/collecthsmetrics) reproduced |
| MULTIQC | `multiqc` / `multiqc_bwameth` / `multiqc_bwamem` | multiqc 1.32 | one rule per aligner branch; same search space as upstream (fastqc zips, trimgalore logs, samtools stats/flagstat/idxstats, picard metrics + qualimap/preseq/HS extras), plus the single-end report names (`{sample}_fastqc.zip`, `{sample}.fastq.gz_trimming_report.txt`, `*_SE_report.txt`, ...) which are picked up exactly when present; the methyldackel/rastair outputs are not fed to MultiQC, exactly like upstream |
| softwareVersionsToYAML + collectFile | `multiqc_versions` | — | upstream extracts versions at runtime; port pins the module versions statically |

Additional notes: single-end samples are supported via the engine's
metadata binding (`[workflow] metadata_file` + `{meta.endedness}`, gated on
`config.single_end_mode`, oxo-flow >= 0.17.0); `--save_*` / `publish_dir_mode`
params are N/A (oxo-flow publishes every declared output); per-process
`withName:` resource overrides are baked into `[rules.resources]` (upstream
labels process_single/low/medium/high + BISMARK_ALIGN 8d / DEDUPLICATE 2d /
METHYLATIONEXTRACTOR 1d time limits).

## Links

- Repository: [oxo-flow-methylseq](https://github.com/oxo-flow-community/oxo-flow-methylseq)
- Upstream: [nf-core/methylseq](https://github.com/nf-core/methylseq) @ `4.2.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
