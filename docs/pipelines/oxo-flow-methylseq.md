# Bisulfite methylation analysis: alignment, methylation calls and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Run end-to-end bisulfite methylation analysis (WGBS, and RRBS-compatible) of paired-end reads: FastQC quality control, TrimGalore adapter trimming, alignment to the bisulfite-converted reference genome with any of the four upstream aligners — Bismark bowtie2 (default), Bismark hisat2, bwameth (bwa-meth) or BWA-MEM — PCR-deduplication, samtools sort/index, methylation calls (bismark_methylation_extractor, MethylDackel on bwameth, rastair for TAPS), per-sample and project-wide Bismark HTML reports, optional QualiMap BamQC, preseq complexity estimates and targeted-sequencing (bedtools intersect + Picard HS metrics), and a final MultiQC report. All optional branches are gated on the same config keys as the upstream params and off by default.

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 55 |
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
- paired-end raw reads: <dir>/<sample>_R1.fastq.gz and <dir>/<sample>_R2.fastq.gz (samples with >1 pair: <dir>/<sample>_<unit>_R{1,2}.fastq.gz per unit — concatenated by cat_fastq)
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
| `accel` | `false` | — | `trimgalore` |
| `aligner` | `bismark` | Only the 'bismark' (bowtie2) aligner is ported. 'bismark_hisat', 'bwameth', 'bwamem' are NOT ported (see README fidelity table). | — |
| `clip_r1` | `0` | Trimming options (upstream params with the same defaults) | `trimgalore` |
| `clip_r2` | `0` | — | `trimgalore` |
| `comprehensive` | `true` | The port's DAG consumes the merged (--comprehensive) methylation-call outputs, so the default differs from upstream (false): the per-strand split files would leave the declared outputs unmoved. | `bismark_methylationextractor` |
| `cytosine_report` | `false` | Bismark options | `bismark_coverage2cytosine` |
| `em_seq` | `false` | — | `bismark_align`, `trimgalore` |
| `fasta` | `test/fixtures/refs/genome.fa` | Reference genome (upstream: --fasta). Uncompressed FASTA; the port always builds the Bismark index from it (upstream default when --bismark_index is not supplied). Point this at your genome; the repo default ships the tiny test fixture. | `bismark_genomepreparation` |
| `ignore_3prime_r1` | `0` | — | `bismark_methylationextractor` |
| `ignore_3prime_r2` | `2` | — | `bismark_methylationextractor` |
| `ignore_r1` | `0` | — | `bismark_methylationextractor` |
| `ignore_r2` | `2` | — | `bismark_methylationextractor` |
| `length_trim` | `0` | — | `trimgalore` |
| `local_alignment` | `false` | — | `bismark_align` |
| `maxins` | `` | — | `bismark_align` |
| `meth_cutoff` | `` | — | `bismark_methylationextractor` |
| `minins` | `` | — | `bismark_align` |
| `multiqc_title` | `` | MultiQC | `multiqc` |
| `nextseq_trim` | `0` | — | `trimgalore` |
| `no_overlap` | `true` | — | `bismark_methylationextractor` |
| `nomeseq` | `false` | — | `bismark_coverage2cytosine`, `bismark_methylationextractor` |
| `non_directional` | `false` | — | `bismark_align` |
| `num_mismatches` | `0.6` | — | `bismark_align` |
| `out_dir` | `results` | — | `bismark_align`, `bismark_coverage2cytosine`, `bismark_deduplicate`, `bismark_methylationextractor`, `bismark_report`, `bismark_summary`, `fastqc`, `multiqc`, `multiqc_versions`, `samtools_index`, `samtools_sort`, `trimgalore` |
| `pbat` | `false` | — | `bismark_align`, `trimgalore` |
| `raw_dir` | `test/fixtures/raw` | Input reads directory: raw/<sample>_R1.fastq.gz + _R2.fastq.gz (paired-end). The repo default ships the tiny test fixtures; point this at your data. | `fastqc`, `trimgalore` |
| `relax_mismatches` | `false` | — | `bismark_align` |
| `rrbs` | `false` | Library presets (upstream params with the same defaults). | `bismark_deduplicate`, `trimgalore` |
| `single_cell` | `false` | — | `bismark_align`, `trimgalore` |
| `skip_deduplication` | `false` | — | `bismark_deduplicate` |
| `skip_fastqc` | `false` | Skip options (upstream: --skip_fastqc / --skip_trimming / --skip_deduplication / --skip_multiqc). Same defaults as upstream. | `fastqc` |
| `skip_multiqc` | `false` | — | `multiqc` |
| `skip_trimming` | `false` | — | `trimgalore` |
| `skip_trimming_presets` | `false` | — | `trimgalore` |
| `slamseq` | `false` | — | — |
| `three_prime_clip_r1` | `0` | — | `trimgalore` |
| `three_prime_clip_r2` | `0` | — | `trimgalore` |
| `unmapped` | `false` | — | `bismark_align` |
| `zymo` | `false` | — | `bismark_align`, `trimgalore` |

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
- trimgalore
- bismark_align
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
- picard_markduplicates
- samtools_index_deduplicated
- picard_addorreplacereadgroups
- picard_markduplicates_bwamem
- samtools_index_deduplicated_bwamem
- bismark_methylationextractor
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

- single_end — paired-end only; the upstream samplesheet 'single_end' column is not ported

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|
| CAT_FASTQ | `cat_fastq_r1` / `cat_fastq_r2` | coreutils 9.5 | ported via the engine's `input_groups` primitive (issue #227, oxo-flow >= 0.17.0): one instance per sample with >1 fastq pair, R1s and R2s concatenated into `results/fastq/<sample>_R{1,2}.fastq.gz`; single-pair samples pass through unchanged (downstream falls back to the raw pair). Upstream's single process is split into two rules (one per read); see deviations |
--|
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command; `--memory` derived from task resources |
| TRIMGALORE | `trimgalore` | trim-galore 0.6.10, cutadapt 4.9, pigz 2.8 | identical command incl. library-preset clipping and `--cores` clamp |
| BISMARK_GENOMEPREPARATION | `bismark_genomepreparation` | bismark 0.25.1, gzip 1.13 | `--bowtie2` (or `--hisat2` for bismark_hisat, `--slam` for slamseq); runs when no prebuilt index is supplied (upstream default) |
| GUNZIP | (merged into the index-preparation shells) | gzip 1.13 | a gzipped reference FASTA is decompressed before index building, as in the upstream fasta_index_methylseq subworkflow |
| UNTAR | `bismark_untar` | tar 1.34 | active only when a prebuilt `--bismark_index` archive is supplied; strips a single top-level directory, like upstream |
| BISMARK_ALIGN | `bismark_align` | bismark 0.25.1 | identical flag order (pbat/non_directional/unmapped/score_min/local/minins/maxins/multicore); hisat2 splice sites via `known_splices` (see deviations) |
| BISMARK_DEDUPLICATE | `bismark_deduplicate` | bismark 0.25.1 | identical command; skipped with `skip_deduplication`/`rrbs` like upstream |
| SAMTOOLS_SORT | `samtools_sort` | samtools 1.22.1, htslib 1.22.1 | upstream prefix `${sample}.deduplicated.sorted` |
| SAMTOOLS_INDEX | `samtools_index` | samtools 1.22.1 | identical command |
| BISMARK_METHYLATIONEXTRACTOR | `bismark_methylationextractor` | bismark 0.25.1 | identical flag order on the **deduplicated** BAM; `--multicore`/`--buffer_size` derived from resources |
| BISMARK_COVERAGE2CYTOSINE | `bismark_coverage2cytosine` | bismark 0.25.1 | off by default; runs with `cytosine_report`/`nomeseq` |
| BISMARK_REPORT | `bismark_report` | bismark 0.25.1 | bismark2report run with the four reports co-located, as in the upstream workdir |
| BISMARK_SUMMARY | `bismark_summary` | bismark 0.25.1 | bismark2summary with upstream BAM-name arguments |
| BWAMETH_INDEX | `bwameth_index` | bwameth 0.2.9 | `bwameth.py index`, or `index-mem2` with `use_mem2`; index dir `refs/BwamethIndex` |
| BWAMETH_ALIGN | `bwameth_align` | bwameth 0.2.9 | identical command (reference symlink re-created in the index dir, `samtools view -bhS`) |
| BWA_INDEX | `bwa_index` | bwa 0.7.19 | `bwa index -p`; upstream sizes memory dynamically (5.37x FASTA) — the port uses a fixed 4 threads/24G/24h budget (see deviations) |
| BWA_MEM | `bwa_mem` | bwa 0.7.19, samtools 1.22.1 | upstream `sort_bam = true`: `bwa mem \| samtools sort`; index prefix found by globbing `*.amb` |
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
| QUALIMAP_BAMQC | `qualimap_bamqc` / `qualimap_bamqc_alt` | qualimap 2.3 | `-p non-strand-specific --collect-overlap-pairs`, `--gff` with `bamqc_regions_file`, `_JAVA_OPTIONS` tmpdir |
| PRESEQ_LCEXTRAP | `preseq_lcextrap` / `preseq_lcextrap_alt` | preseq 3.2.0 | `-verbose -bam -pe`; the `*.command.log` is preseq's own stderr (see deviations) |
| PICARD_CREATESEQUENCEDICTIONARY | `picard_createsequencedictionary` | picard 3.4.0 | runs only when `collecthsmetrics` is requested, like upstream |
| PICARD_BEDTOINTERVALLIST | `picard_bedtointervallist` | picard 3.4.0 | output named `target_regions.intervallist` (fixed name; see deviations) |
| BEDTOOLS_INTERSECT | `bedtools_intersect` (+ `_bwameth`, `_chg`, `_chh`) | bedtools 2.31.1 | prefix = the bedGraph basename, suffix `targeted.bedGraph`, as upstream |
| PICARD_COLLECTHSMETRICS | `picard_collecthsmetrics` / `picard_collecthsmetrics_alt` | picard 3.4.0 | same intervals for bait and target; excluded on the taps/bwamem branches, like the upstream rastair error |
| SAMTOOLS_FAIDX | `samtools_faidx` | samtools 1.22.1, htslib 1.22.1, gzip 1.13 | stages the reference at `refs/FastaRef/reference.fa`; upstream gate (bwameth/bwamem/collecthsmetrics) reproduced |
| MULTIQC | `multiqc` / `multiqc_bwameth` / `multiqc_bwamem` | multiqc 1.32 | one rule per aligner branch; same search space as upstream (fastqc zips, trimgalore logs, samtools stats/flagstat/idxstats, picard metrics + qualimap/preseq/HS extras); the methyldackel/rastair outputs are not fed to MultiQC, exactly like upstream |
| softwareVersionsToYAML + collectFile | `multiqc_versions` | — | upstream extracts versions at runtime; port pins the module versions statically |

Additional notes: paired-end only (`single_end` samplesheet column is not
ported); `--save_*` / `publish_dir_mode` params are N/A (oxo-flow publishes
every declared output); per-process `withName:` resource overrides are baked
into `[rules.resources]` (upstream labels process_single/low/medium/high +
BISMARK_ALIGN 8d / DEDUPLICATE 2d / METHYLATIONEXTRACTOR 1d time limits).

## Links

- Repository: [oxo-flow-methylseq](https://github.com/oxo-flow-community/oxo-flow-methylseq)
- Upstream: [nf-core/methylseq](https://github.com/nf-core/methylseq) @ `4.2.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
