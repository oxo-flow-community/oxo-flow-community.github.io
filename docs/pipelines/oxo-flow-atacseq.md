# ATAC-seq: peak calling and QC

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

ATAC-seq peak calling and QC: FastQC raw-read QC, Trim Galore adapter trimming, BWA-MEM alignment, Picard mark-duplicates, BAMTools filtering, MACS2 broad-peak calling, HOMER peak annotation, FRiP scoring, normalised bigWig tracks, deepTools QC plots and a combined MultiQC report. Default plan is the upstream single-end aligner=bwa main path (15 rules); when-gated branches port the paired-end path, Bowtie2/Chromap/STAR aligners, reference preparation, mitochondrial filtering, consensus peaks/DESeq2, preseq, Picard metrics, ataqv, IGV and R QC plots (27 further rules, 42 total).

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | epigenomics |
| **Rules** | 42 |
| **Compute** | up to 12 CPUs / 72 GB per rule |
| **Tools** | fastqc · trim-galore · bwa · samtools · picard · bamtools · macs2 · homer · bedtools · ucsc-bedgraphtobigwig · deeptools · multiqc · bowtie2 · chromap · star · preseq · ataqv · subread · r |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/atacseq](https://github.com/nf-core/atacseq) |
| **Pinned version** | `2.1.2` |

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs reference genome and peak-calling inputs — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker/Singularity) — 41/42 rules in pinned biocontainer images, plus one pinned conda env for picard_markduplicates

**Requirements.**
- reference data: genome FASTA with .fai, BWA index prefix (.amb/.ann/.bwt/.pac/.sa), chrom sizes file, GTF annotation, gene BED, TSS BED (optional blacklist BED)
- input: single-end <sample>.fastq.gz reads, declared in [[sample_groups]]
- compute: up to 12 CPUs / 72 GB per rule
- runtime: Docker or Singularity for the 14 container rules; conda/mamba for the picard_markduplicates env

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-atacseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-atacseq
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `blacklist` | `` | params.blacklist — include-regions BED (complement of ENCODE | `bamtools_filter` |
| `broad_cutoff` | `0.1` | — | `macs2_callpeak` |
| `bwa_index` | `test/fixtures/genome/genome.fa` | params.bwa — index prefix (.amb/.ann/.bwt/.pac/.sa beside it) | `bwa_mem` |
| `chrom_sizes` | `test/fixtures/genome/genome.fa.sizes` | CUSTOM_GETCHROMSIZES output | `ucsc_bedgraphtobigwig` |
| `fingerprint_bins` | `500000` | — | `plotfingerprint` |
| `fragment_size` | `200` | — | `bedtools_genomecov`, `plotfingerprint` |
| `gene_bed` | `test/fixtures/genome/gene.bed` | params.gene_bed | `deeptools_plots` |
| `gtf` | `test/fixtures/genome/genes.gtf` | params.gtf | `homer_annotatepeaks` |
| `keep_dups` | `false` | — | — |
| `keep_multi_map` | `false` | — | — |
| `macs_gsize` | `2.7e9` | blacklist + chrM when keep_mito=false); empty = no -L filter | `macs2_callpeak` |
| `min_trimmed_reads` | `10000` | — | — |
| `narrow_peak` | `false` | Upstream default params (kept as config so CLI overrides work) | — |
| `out_dir` | `results` | params.outdir | `bamtools_filter`, `bedtools_genomecov`, `bwa_mem`, `deeptools_plots`, `fastqc`, `frip_score`, `homer_annotatepeaks`, `macs2_callpeak`, `multiqc`, `picard_markduplicates`, `picard_mergesamfiles`, `plotfingerprint`, `samtools_sort_stats`, `trimgalore`, `ucsc_bedgraphtobigwig` |
| `picard_xmx_gb` | `8` | GB passed to picard -Xmx. Previously derived from the rule's 36G resource budget (Xmx≈30G), which thrash-killed the JVM on a 3.7 GB machine (live run); the resource budget still drives scheduling. | `picard_markduplicates` |
| `raw_dir` | `test/fixtures/raw` | input fastqs (raw/<sample>.fastq.gz for single-end) | `fastqc`, `trimgalore` |
| `reference` | `test/fixtures/genome/genome.fa` | Reference inputs. Upstream obtains these from nf-core iGenomes (--genome); this port expects pre-built files (see README "References"). | `bamtools_filter`, `homer_annotatepeaks`, `picard_markduplicates`, `samtools_sort_stats` |
| `save_trimmed` | `false` | — | — |
| `skip_fastqc` | `false` | — | `fastqc` |
| `skip_multiqc` | `false` | — | `multiqc` |
| `skip_plot_fingerprint` | `false` | — | `plotfingerprint` |
| `skip_plot_profile` | `false` | — | `deeptools_plots` |
| `skip_qc` | `false` | — | `fastqc` |
| `skip_trimming` | `false` | — | `trimgalore` |
| `tss_bed` | `test/fixtures/genome/tss.bed` | params.tss_bed | `deeptools_plots` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-atacseq rule-level DAG](../assets/dag/oxo-flow-atacseq.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastqc
- trimgalore
- bwa_mem
- samtools_sort_stats
- picard_mergesamfiles
- picard_markduplicates
- bamtools_filter
- macs2_callpeak
- homer_annotatepeaks
- frip_score
- bedtools_genomecov
- ucsc_bedgraphtobigwig
- deeptools_plots
- plotfingerprint
- multiqc
- pe::fastqc_pe, pe::trimgalore_pe, pe::bwa_mem_pe, pe::bamtools_filter_pe, pe::pe_name_sort_remove_orphans, pe::bedtools_genomecov_pe, pe::plotfingerprint_pe, pe::multiqc_pe (paired-end branch, when config.paired)
- alt::bowtie2_align, alt::chromap_align, alt::star_align (alternative aligners, when config.aligner != 'bwa'; SE only)
- ref::bwa_index, ref::custom_getchromsizes (reference preparation, when config.prepare_reference)
- mito::genome_blacklist_regions (mitochondrial filtering, when config.mito_name or config.raw_blacklist set)
- qce::preseq_lcextrap (when skip_preseq=false)
- qce::picard_collectmultiplemetrics (when skip_picard_metrics=false)
- qce::get_autosomes, qce::ataqv, qce::mkarv (when skip_ataqv=false)
- qce::plot_macs2_qc, qce::plot_homer_annotatepeaks (when skip_peak_qc=false)
- qce::multiqc_custom_peaks (when multiqc_custom_peaks=true)
- qce::igv (when skip_igv=false)
- cons::macs2_consensus, cons::homer_annotatepeaks_consensus, cons::subread_featurecounts, cons::deseq2_qc (consensus peaks/DESeq2, when skip_consensus_peaks=false; needs >= 2 samples)

**Excluded**

- merged-replicate analysis (SAMTOOLS_MERGE, BAM_MERGED_REPLICATE_PICARD, BAM_FILTER_MERGED_REPLICATE, BAM_MERGE_REPLICATES_AND_PEAKS_BEDTOOLS) — structural Nextflow pattern: groupTuple(by: [0]) folds per-replicate BAMs keyed _REP\d+ into sets; oxo-flow has no replicate-grouping primitive, so the _REP merge and replicate-level tracks cannot be expressed
- INPUT_CHECK (samplesheet_check) — pipeline plumbing; oxo-flow provides native [[sample_groups]] declaration + validate
- DUMP_SOFTWARE_VERSIONS — pipeline plumbing; oxo-flow has native version/audit mechanisms
- UMITOOLS_EXTRACT (umi branch) — dead code at 2.1.2: the workflow hardcodes with_umi=false so the branch can never fire
- nucleosome_analysis / genrich — not present at tag 2.1.2 (checked workflows/, conf/, subworkflows/)

## Fidelity

## Fidelity

Ported with upstream defaults: `aligner=bwa`, single-end, `narrow_peak=false`
(broad peaks), no control. One row per upstream process; steps not ported are
listed with reasons. `when`-gated rules carry the gate in the Notes column.

| Upstream process | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` / `pe::fastqc_pe` | fastqc 0.11.9 | identical command (`--quiet --threads`); PE variant in the paired branch |
| TRIMGALORE | `trimgalore` / `pe::trimgalore_pe` | trim-galore 0.6.7 | identical command (`--fastqc --cores 8 --gzip`); PE variant uses `--paired` + `_val_1/2` outputs |
| FASTQ_FASTQC_UMITOOLS_TRIMGALORE (UMITOOLS_EXTRACT) | — | — | **not ported** — dead code at 2.1.2: the workflow hardcodes `with_umi=false`, the branch can never fire |
| BWA_MEM | `bwa_mem` / `pe::bwa_mem_pe` | bwa 0.7.17, samtools 1.17 | identical (`-M -R '@RG...'`, secondary-alignment filter `-F 0x0100`), mulled container; PE variant merges read groups |
| BOWTIE2_ALIGN | `alt::bowtie2_align` | bowtie2 2.5.1, samtools 1.17 | identical (end-to-end, `--very-sensitive`, `-k 4`, SAM→BAM filter); when `aligner = "bowtie2"` |
| CHROMAP_CHROMAP | `alt::chromap_align` | chromap 0.2.5, samtools 1.17 | identical (`-l 2000 --Tn5-shift --low-mem`); when `aligner = "chromap"` |
| STAR_ALIGN | `alt::star_align` | star 2.6.1d | identical (EndToEnd, `--alignIntronMax 1`, unsorted BAM); when `aligner = "star"` |
| BAM_SORT_STATS_SAMTOOLS (SAMTOOLS_SORT + SAMTOOLS_INDEX + SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS) | `samtools_sort_stats` / `pe::pe_name_sort_remove_orphans` | samtools 1.17 | identical commands, folded into one rule (same env); PE adds name sort → `bampe_rm_orphan.py --only_fr_pairs` → coordinate sort (upstream BAM_SORT_STATS_ORPHANS) |
| PICARD_MERGESAMFILES_LIBRARY | `picard_mergesamfiles` / `pe::bwa_mem_pe` | picard 3.0.0 | upstream symlink branch for single-library samples replicated; multi-library merge (actual MergeSamFiles) not expressible — no library source in oxo-flow |
| BAM_MARKDUPLICATES_PICARD (PICARD_MARKDUPLICATES + SAMTOOLS_INDEX + SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS) | `picard_markduplicates` | picard 3.0.0, samtools 1.17 | identical commands (`--ASSUME_SORTED --REMOVE_DUPLICATES false`, `XMX` heap sizing); combined conda env |
| BAMTOOLS_FILTER + SAMTOOLS_INDEX + BAM_STATS_SAMTOOLS (SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS) | `bamtools_filter` / `pe::bamtools_filter_pe` | bamtools 2.5.2, samtools 1.17 | identical (`-F 0x004 -F 0x0400 -q 1`, optional `-L blacklist`, `assets/bamtools_filter_{se,pe}.json`); PE adds `-f 0x001 -F 0x0008` |
| MACS2_CALLPEAK | `macs2_callpeak` | macs2 2.2.7.1 | identical (`--keep-dup all --nomodel --broad --broad-cutoff 0.1`, `gsize` from config, `--format BAM`) |
| HOMER_ANNOTATEPEAKS | `homer_annotatepeaks` / `cons::homer_annotatepeaks_consensus` | homer 4.11 | identical (`-gid -gtf`); consensus variant annotates the consensus BED, when `skip_consensus_peaks = false` |
| FRIP_SCORE | `frip_score` | bedtools 2.30.0, samtools 1.17 | identical (intersectBed `-f 0.20`, flagstat `mapped` fraction) |
| BEDTOOLS_GENOMECOV | `bedtools_genomecov` / `pe::bedtools_genomecov_pe` | bedtools 2.30.0 | identical (`-bg -scale 1e6/reads -fs fragment_size`, sort); PE uses `-pc` instead of `-fs` (upstream) |
| UCSC_BEDGRAPHTOBIGWIG | `ucsc_bedgraphtobigwig` | ucsc-bedgraphtobigwig 445 | identical |
| BIGWIG_PLOT_DEEPTOOLS (COMPUTEMATRIX scale-regions + reference-point, PLOTPROFILE, PLOTHEATMAP) | `deeptools_plots` | deeptools 3.5.1 | identical args (regionBodyLength 1000, ±3000, `--missingDataAsZero --skipZeros --smartLabels`) |
| MERGED_LIBRARY_DEEPTOOLS_PLOTFINGERPRINT | `plotfingerprint` / `pe::plotfingerprint_pe` | deeptools 3.5.1 | identical (`--extendReads fragment_size`); PE omits `--extendReads` (upstream) |
| MULTIQC | `multiqc` / `pe::multiqc_pe` | multiqc 1.13 | upstream mechanism replicated: `multiqc_config.yml` staged in cwd, `multiqc -f .`; config `path_filters` adapted to this port's `results/` layout; PE adds the PE fastqc/trimgalore patterns |
| BWA_INDEX | `ref::bwa_index` | bwa 0.7.17 | identical (`bwa index -p`); when `prepare_reference = true` (default false — port takes pre-built indexes) |
| CUSTOM_GETCHROMSIZES / CUSTOM_GENOME_FASTA_INDEX (prepare_genome) | `ref::custom_getchromsizes` | samtools 1.16.1 | `samtools faidx` + `cut -f 1,2` into `config.chrom_sizes`; when `prepare_reference = true` |
| GENOME_BLACKLIST_REGIONS (mitochondrial filtering) | `mito::genome_blacklist_regions` | bedtools 2.30.0 | sortBed/complementBed over `config.raw_blacklist`, then optional chrM drop (`config.mito_name`, `keep_mito`); when `mito_name`/`raw_blacklist` set; consumed via `-L` by `bamtools_filter` |
| PRESEQ_LCEXTRAP | `qce::preseq_lcextrap` | preseq 3.1.2 | identical (`-verbose -bam -seed 1`; `-pe` when paired); when `skip_preseq = false` |
| PICARD_COLLECTMULTIPLEMETRICS | `qce::picard_collectmultiplemetrics` | picard 3.0.0 | identical (5 metrics + PDFs into `picard_metrics/{,pdf}/`); when `skip_picard_metrics = false` |
| GET_AUTOSOMES + ATAQV_ATAQV + ATAQV_MKARV | `qce::get_autosomes`, `qce::ataqv`, `qce::mkarv` | python 3.8.3, ataqv 1.3.1 | identical commands (`--ignore-read-groups`, mitochondrial-reference-name when `mito_name`; mkarv HTML index); when `skip_ataqv = false` |
| PLOT_MACS2_QC / PLOT_HOMER_ANNOTATEPEAKS | `qce::plot_macs2_qc` / `qce::plot_homer_annotatepeaks` | mulled R image | scripts copied verbatim from upstream `bin/`; when `skip_peak_qc = false` |
| MULTIQC_CUSTOM_PEAKS | `qce::multiqc_custom_peaks` | multiqc headers | identical count/FRiP TSVs (`assets/multiqc/` headers copied verbatim); when `multiqc_custom_peaks = true` (port-only switch; upstream always emits) |
| IGV | `qce::igv` | python 3.8.3 | `igv_files_to_session.py` copied verbatim, `--path_prefix '../../'`; when `skip_igv = false`; per-library tracks only (no merged-replicate sets, see below) |
| MACS2_CONSENSUS_PEAKS | `cons::macs2_consensus` | mulled (macs2 + bedtools + R) | `sort + mergeBed -c 2,3,4,5,6,7,8,9 -o collapse...` → `macs2_merged_expand.py --min_replicates` → BED/SAF/UpSet plot (bin scripts verbatim); when `skip_consensus_peaks = false`, needs ≥ 2 samples |
| SUBREAD_FEATURECOUNTS | `cons::subread_featurecounts` | subread 2.0.1 | identical (`-F SAF -O --fracOverlap 0.2 -s 0`, `-p` when paired); when `skip_consensus_peaks = false` |
| DESEQ2_QC | `cons::deseq2_qc` | mulled (R + DESeq2) | `deseq2_qc.r` verbatim (`--id_col 1 --count_col 7`, `--vst TRUE` when `deseq2_vst`); when `skip_consensus_peaks = false` and `skip_deseq2_qc = false` |
| SAMTOOLS_MERGE / BAM_MERGED_REPLICATE_PICARD / BAM_FILTER_MERGED_REPLICATE / BAM_MERGE_REPLICATES_AND_PEAKS_BEDTOOLS | — | — | **not ported** — merged-replicate analysis is a structural Nextflow pattern: `groupTuple(by: [0])` folds per-replicate BAMs keyed `_REP\d+` into sets, then the merged set drives replicate-level filtering/peaks/QC. oxo-flow has no replicate-grouping primitive over globbed inputs, so the `_REP` merge (and the replicate tracks in IGV/FRiP) cannot be expressed |
| INPUT_CHECK (samplesheet_check) | — | — | **not ported** — pipeline plumbing; oxo-flow provides native `[[sample_groups]]` declaration + `validate` |
| DUMP_SOFTWARE_VERSIONS | — | — | **not ported** — pipeline plumbing; oxo-flow has native version/audit mechanisms |

### Known divergences

- **Branches that upstream runs by default ship OFF here**: ataqv,
  Picard metrics, IGV, consensus peaks/DESeq2 and the R QC plots all run on
  the upstream default path; this port gates them behind
  `skip_ataqv`/`skip_picard_metrics`/`skip_igv`/`skip_consensus_peaks`/
  `skip_peak_qc` (default `true` = off) so the default plan stays the
  minimal main path. `skip_preseq = true` matches the upstream default
  (preseq is off there too). Enabling a branch is a single config flag.
- **Reference inputs**: upstream builds/derives the reference from
  `--genome` (iGenomes) at runtime; this port consumes pre-built files
  (`reference`, `bwa_index` prefix, `gtf`, `gene_bed`, `tss_bed`,
  `chrom_sizes`, optional `blacklist`). `prepare_reference = true` instead
  generates the BWA index and chrom sizes from the FASTA (the fixture
  already ships them, so the rules report up-to-date there).
- **Alternative aligners are single-end only** (`when` adds
  `!config.paired`): the paired branch is bwa-only, matching upstream's
  paired alignment options. Misconfigurations (e.g. `paired=true` with
  `aligner="star"`) surface as validation warnings via missing inputs.
- **PE requires `bwa_index` and produces `bwa/library/` outputs**: the
  paired branch's `bwa_mem_pe` merges read groups (`-R '@RG\tID:{sample}\tSM:{sample}'`)
  as upstream does; the default SE path keeps the original `@RG` handling.
- **Broad peaks are hardcoded**: the port's `macs2_callpeak` and all
  consumers use `--broad`; `narrow_peak = true` is honoured by
  `macs2_callpeak` but the downstream rules in this port read
  `*_peaks.broadPeak` only.
- **MultiQC config**: `path_filters`/`module_order` were trimmed to the
  ported steps; preseq/featureCounts/ataqv/DESeq2 sections appear when
  their branches are enabled (the PE MultiQC adds the PE fastqc/trimgalore
  logs). Report comment points at the upstream pipeline.
- **`macs_gsize`**: upstream derives it from the read length keyed genome
  block; the port exposes it as `config.macs_gsize` (default `2.7e9`, the
  upstream GRCh37/38 @ 50 bp value).
- **IGV tracks are per-library (`mLb_*`) only**: upstream additionally
  emits merged-replicate tracks; replicate merging is not ported (above).
- **featureCounts is unstranded**: `-s 0` is passed explicitly (the
  upstream default); a `[SCI-FEATURECOUNTS-STRAND]` preflight hint may
  appear for the gated rule — informational.
- **`size_factors/` stays in the workdir**: upstream DESeq2_QC publishes
  the `size_factors` directory; the port leaves it in the rule workdir
  (not declared as an output) — documented, not lost.
- **Consensus branch needs ≥ 2 samples**: upstream filters the peak
  channel to `size() > 1`; with one sample the consensus rules would
  produce degenerate output.

## Links

- Repository: [oxo-flow-atacseq](https://github.com/oxo-flow-community/oxo-flow-atacseq)
- Upstream: [nf-core/atacseq](https://github.com/nf-core/atacseq) @ `2.1.2`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
