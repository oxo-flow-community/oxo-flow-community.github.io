# ChIP-seq: peak calling, QC and differential analysis

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

ChIP-seq peak calling, QC and differential analysis for paired-end reads: FastQC and Trim Galore read QC, BWA-MEM alignment, library merge and Picard mark-duplicates, BAMTools filtering against a blacklist with orphan-read removal, preseq and phantompeakqualtools library complexity QC, bigWig tracks and deepTools QC plots, MACS3 broad-peak calling with input controls, HOMER peak annotation, FRiP scoring, consensus peaks across replicates (MACS3 merge, featureCounts quantification, DESeq2 QC), an IGV session and a MultiQC report.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 46 |
| **Tools** | fastqc · trim-galore · bwa · samtools · picard · bamtools · preseq · r-base · phantompeakqualtools · bedtools · ucsc-bedgraphtobigwig · deeptools · khmer · macs3 · homer · subread · multiqc · python |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/chipseq](https://github.com/nf-core/chipseq) |
| **Pinned version** | `2.1.0` |

## Run it

```bash
oxo-flow dry-run main.oxoflow       # prints the 154-instance plan
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker/Singularity) — pinned images

**Requirements.**
- genome FASTA and FASTA index (fasta, fai)
- annotation GTF (gtf)
- gene-body regions BED, derived upstream via GTF2BED (gene_bed)
- chromosome sizes file (chrom_sizes)
- blacklist regions BED (blacklist)
- BWA index directory for the reference FASTA (bwa_index: *.amb, *.ann, *.bwt, *.pac, *.sa)
- raw paired-end FASTQ reads named raw/{pair_id}_R{1,2}.fastq.gz with sample metadata in [[pairs]] and ip_ids
- compute: up to 12 CPUs / 72 GB per rule (bwa_mem, trimgalore); most rules request 6 CPUs / 36 GB
- disk: several GB of pinned container images pulled by Docker/Singularity

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/download/v0.11.0/oxo-flow-v0.11.0-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-chipseq
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- FASTQ_FASTQC_UMITOOLS_TRIMGALORE (FASTQC + TRIMGALORE)
- BWA_MEM
- BAM_SORT_STATS_SAMTOOLS (library: SAMTOOLS_SORT + SAMTOOLS_INDEX + SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS)
- PICARD_MERGESAMFILES_LIBRARY
- BAM_MARKDUPLICATES_PICARD (PICARD_MARKDUPLICATES + SAMTOOLS_INDEX + SAMTOOLS_STATS + SAMTOOLS_FLAGSTAT + SAMTOOLS_IDXSTATS)
- BAM_FILTER_BAMTOOLS (BAMTOOLS_FILTER + SAMTOOLS_SORT name-sort + BAM_REMOVE_ORPHANS + BAM_SORT_STATS_SAMTOOLS + SAMTOOLS_INDEX + BAM_STATS_SAMTOOLS)
- PRESEQ_LCEXTRAP
- PICARD_COLLECTMULTIPLEMETRICS
- PHANTOM_PEAK_QUALTOOLS
- MULTIQC_CUSTOM_PHANTOM_PEAK_QUALTOOLS
- BEDTOOLS_GENOMECOV
- UCSC_BEDGRAPHTOBIGWIG
- DEEPTOOLS_COMPUTEMATRIX (scale-regions) + DEEPTOOLS_PLOTPROFILE + DEEPTOOLS_PLOTHEATMAP
- DEEPTOOLS_PLOTFINGERPRINT
- KHMER_UNIQUEKMERS
- MACS2_CALLPEAK (MACS3, broad mode)
- FRIP_SCORE
- MULTIQC_CUSTOM_PEAKS
- HOMER_ANNOTATEPEAKS
- PLOT_MACS3_QC
- PLOT_HOMER_ANNOTATEPEAKS
- BED_CONSENSUS_QUANTIFY_QC_BEDTOOLS_FEATURECOUNTS_DESEQ2 (MACS3_CONSENSUS + HOMER_ANNOTATEPEAKS + ANNOTATE_BOOLEAN_PEAKS + SUBREAD_FEATURECOUNTS + DESEQ2_QC)
- IGV
- MULTIQC

**Excluded**

- UMITOOLS_EXTRACT / umi_extract — with_umi defaults to false upstream
- narrow-peak mode (narrow_peak=true) — port covers the broad-peak default only
- GTF2BED / GENOME_BLACKLIST_REGIONS / prepare_genome / samplesheet_check — reference derivation and pipeline plumbing; the port takes pre-built references (fasta, gtf, gene_bed, chrom_sizes, blacklist, bwa_index)
- multi-antibody consensus grouping (consensus_cluster) — port assumes a single antibody (config.antibody)
- save_align_intermeds / save_mapped / save_tracks / save_macs_pileup publish branches — all off by default upstream
- multiqc_data / multiqc_plots directory publication and pipeline summary / software versions MultiQC sections — Nextflow plumbing
- multi-library MergeSamFiles branch — single-library default path only (upstream symlinks for single-library samples, replicated exactly)
- STAR aligner alternative — aligner=bwa is the default
- DUMP_SOFTWARE_VERSIONS — Nextflow plumbing (oxo-flow has no nf-core pipelines version dump)

## Fidelity

Ported with upstream defaults: `aligner=bwa`, paired-end, `narrow_peak=false`
(broad peaks), `with_umi=false`. One row per upstream process; steps not
ported are listed with reasons.

| Upstream process | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQ_FASTQC_UMITOOLS_TRIMGALORE → FASTQC | `fastqc` | fastqc 0.12.1 | identical command (`--quiet --threads --memory`, 10GB cap); UMITOOLS_EXTRACT branch not ported (`with_umi=false` by default) |
| FASTQ_FASTQC_UMITOOLS_TRIMGALORE → TRIMGALORE | `trimgalore` | trim-galore 0.6.7 | identical (`--fastqc --cores n-4 --paired --gzip`, conditional `--nextseq/--clip_r1/--clip_r2/--three_prime_clip_*`) |
| BWA_MEM | `bwa_mem` | bwa 0.7.17, samtools 1.17 | identical (`-M -R '@RG...'`, secondary filter `-F 0x0100`, `-t` cores, `sort -T`); index lookup via `find` over `config.bwa_index`, same as upstream |
| BAM_SORT_STATS_SAMTOOLS (library, SAMTOOLS_SORT + SAMTOOLS_INDEX + BAM_STATS_SAMTOOLS) | `sort_align` + `index_align` + `stats_align`/`flagstat_align`/`idxstats_align` | samtools 1.17 | identical commands (`samtools cat \| samtools sort` pipeline, `samtools index -@`, stats/flagstat/idxstats) |
| PICARD_MERGESAMFILES_LIBRARY | `mergesamfiles` | picard 3.2.0 | upstream symlink branch for single-library samples replicated exactly (`ln -s`); the multi-library MergeSamFiles branch is off the default path |
| BAM_MARKDUPLICATES_PICARD (PICARD_MARKDUPLICATES + SAMTOOLS_INDEX + BAM_STATS_SAMTOOLS) | `markduplicates` + `index_markdup` + `stats_markdup`/`flagstat_markdup`/`idxstats_markdup` | picard 3.2.0, samtools 1.17 | identical (`--ASSUME_SORTED true --REMOVE_DUPLICATES false --VALIDATION_STRINGENCY LENIENT --TMP_DIR tmp`, `XMX = memory*1024*8/10` heap) |
| BAM_FILTER_BAMTOOLS → BAMTOOLS_FILTER | `bamtools_filter` | samtools 1.17, bamtools 2.5.2 | identical (`-F 0x004 -F 0x0008 -f 0x001`, conditional `-F 0x0400`/`-q 1` on `keep_dups`/`keep_multi_map`, `-L blacklist`, `assets/bamtools_filter_pe.json`) |
| BAM_FILTER_BAMTOOLS → SAMTOOLS_SORT (name sort) | `sort_name` | samtools 1.17 | identical (`samtools cat \| samtools sort -n`, prefix `.mLb.flT.name_sorted`) |
| BAM_REMOVE_ORPHANS | `bam_remove_orphans` | python 3.8 | identical (`bampe_rm_orphan.py ... --only_fr_pairs`) |
| BAM_FILTER_BAMTOOLS → BAM_SORT_STATS_SAMTOOLS | `sort_filter` + `index_filter` + `stats_filter`/`flagstat_filter`/`idxstats_filter` | samtools 1.17 | identical commands, prefix `.mLb.clN.sorted` |
| PRESEQ_LCEXTRAP | `preseq` | preseq 3.2.0 | identical (`lc_extrap -verbose -bam -seed 1 -pe`, command log to stderr) |
| PICARD_COLLECTMULTIPLEMETRICS | `picard_collectmultiplemetrics` | picard 3.2.0 | identical (`-Xmx` heap, `--VALIDATION_STRINGENCY LENIENT --TMP_DIR tmp`, reference, `mv *.CollectMultipleMetrics.*`) |
| PHANTOM_PEAK_QUALTOOLS | `phantompeakqualtools` | r-base 3.5.1, phantompeakqualtools 1.2.2 | identical (`RUN_SPP=which run_spp.R`, `Rscript --max-ppsize=500000 -e "library(caTools); source(..)" -c= -savp= -savd= -out= -p=threads`) |
| MULTIQC_CUSTOM_PHANTOM_PEAK_QUALTOOLS | `multiqc_custom_phantompeakqualtools` | r-base 3.5.1 | identical (cross.correlation RData table, `$9`/`$10` NSC/RSC awk, header concat) |
| BEDTOOLS_GENOMECOV | `bedtools_genomecov` | bedtools 2.30.0 | identical (`-bg -scale 1e6/mapped -pc`, sort, scale-factor file) |
| UCSC_BEDGRAPHTOBIGWIG | `ucsc_bedgraphtobigwig` | ucsc-bedgraphtobigwig 445 | identical |
| DEEPTOOLS_COMPUTEMATRIX (scale-regions) | `deeptools_computematrix` | deeptools 3.5.5 | identical (regionBodyLength 1000, ±3000, `--missingDataAsZero --skipZeros --smartLabels`) |
| DEEPTOOLS_PLOTPROFILE / DEEPTOOLS_PLOTHEATMAP | `deeptools_plotprofile` / `deeptools_plotheatmap` | deeptools 3.5.5 | identical |
| DEEPTOOLS_PLOTFINGERPRINT | `deeptools_plotfingerprint` | deeptools 3.5.5 | identical (`--skipZeros --numberOfSamples 500000 --labels ip control`, paired bamfiles); control-only samples skipped like upstream |
| KHMER_UNIQUEKMERS | `khmer` | khmer 3.0.0a3 | identical (`unique-kmers.py -k read_length -R report`, `grep ^number`); gated on `macs_gsize` being empty, same as upstream |
| MACS2_CALLPEAK (nf-core) | `macs3_callpeak` | macs3 3.0.1 | identical flags (`--keep-dup all --broad --broad-cutoff 0.1`, conditional `--bdg --SPMR` on `save_macs_pileup`, gsize from khmer or config); treatment/control pairs map the upstream `ch_ip`/`ch_ip_control_bam` join — control-only samples are skipped via `optional = true` |
| FRIP_SCORE | `frip_score` | bedtools 2.30.0, samtools 1.17 | identical (intersectBed `-c -f 0.20`, flagstat `mapped (` non-primary fraction) |
| MULTIQC_CUSTOM_PEAKS | `multiqc_custom_peaks` | bash, awk | identical (`wc -l` peak count, FRiP header concat); peak-count for control-only samples skipped like upstream |
| HOMER_ANNOTATEPEAKS | `homer_annotatepeaks` | homer 4.11 | identical (`-gid -gtf -cpu`) |
| PLOT_MACS3_QC | `plot_macs3_qc` | r-base 3.5.1, macs3 3.0.1 | identical (`-i` comma paths, `-s` paths minus `_peaks.broadPeak`, `-o qc -p macs3_peak`) |
| PLOT_HOMER_ANNOTATEPEAKS | `plot_homer_annotatepeaks` | r-base 3.5.1, homer 4.11 | identical (comma paths, summary + MQC header concat) |
| BED_CONSENSUS_QUANTIFY_QC_BEDTOOLS_FEATURECOUNTS_DESEQ2 → MACS3_CONSENSUS (local) | `macs3_consensus` | bedtools 2.30.0, macs3 3.0.1 | identical (mergeBed collapse, `macs3_merged_expand.py --min_replicates`, awk BED/SAF conversion, `plot_peak_intersect.r`, antibody.txt) |
| BED_CONSENSUS_QUANTIFY_QC_BEDTOOLS_FEATURECOUNTS_DESEQ2 → HOMER_ANNOTATEPEAKS (consensus) | `homer_annotate_consensus` | homer 4.11 | identical |
| ANNOTATE_BOOLEAN_PEAKS (local) | `annotate_boolean_peaks` | ubuntu 20.04 | identical (`cut -f2-`, sorted paste) |
| SUBREAD_FEATURECOUNTS | `subread_featurecounts` | subread 2.0.1 | identical (`-F SAF -O --fracOverlap 0.2 -p -s 0`, counts IP-sample BAMs only) |
| DESEQ2_QC (local) | `deseq2_qc` | mulled DESeq2 1.38.0 | identical (`--id_col 1 --sample_suffix .mLb.clN.sorted.bam --count_col 7 --vst TRUE`, header sed `_1` suffixes, mv to deseq2/) |
| IGV (local) | `igv` | python 3.8.3 | identical (bigWig/Peak/bed find, consensus guard, antibody.txt, `igv_files_to_session.py ... --path_prefix '../../'`, genome.fa publish) |
| MULTIQC (local) | `multiqc` | multiqc 1.23 | upstream mechanism replicated: `multiqc_config.yml` staged in cwd, `multiqc -f .`; config `path_filters`/`report_section_order` adapted to this port's `results/` layout |
| GTF2BED | — | — | **not ported** — upstream derives `gene_bed` from the GTF; the port takes `gene_bed` directly as an input |
| GENOME_BLACKLIST_REGIONS / GTF2BED / samplesheet_check | — | — | **not ported** — pipeline plumbing / reference derivation; the port takes pre-built references |
| UMI handling (UMITOOLS_EXTRACT, umi_extract) | — | — | **not ported** — `with_umi=false` by default |
| narrow-peak mode (`narrow_peak=true`, `--narrow-cutoff`) | — | — | **not ported** — port covers the broad-peak default (`narrow_peak=false`) |
| save_macs_pileup / save_align_intermeds / save_mapped / save_tracks outputs | — | — | intermediate BAM/bedGraph publish branches are `false` by default upstream; only the default-published files are produced here |
| DUMP_SOFTWARE_VERSIONS / pipeline summary sections of MultiQC | — | — | **not ported** — Nextflow plumbing / report plumbing (multiqc_data, multiqc_plots not published) |
| Multi-antibody consensus (`consensus_cluster` grouping) | — | — | single antibody (`config.antibody`) per run; upstream multi-antibody grouping is out of scope |

### Known divergences

- **Sample metadata**: nf-core reads a samplesheet (`--input`); oxo-flow uses
  `[[pairs]]` in `main.oxoflow` (pair_id, experiment, control). `ip_ids`
  (samples that receive peak calling) must be kept in sync with `[[pairs]]`.
  Upstream runs MACS3/FRiP/plotFingerprint only for samples that have a
  control; the port mirrors this exactly: per-pair rules whose `{control}`
  input is empty for control-only samples are skipped at run time
  (`optional = true`).
- **Reference inputs**: upstream derives references from `--genome`/iGenomes
  (GTF2BED for gene body regions, blacklist check); this port consumes
  pre-built files (`fasta`, `fai`, `gtf`, `gene_bed`, `chrom_sizes`,
  `blacklist`, `bwa_index` prefix).
- **MultiQC config**: `path_filters` and `report_section_order` were adapted
  to the port's `results/` layout and the single-antibody assumption;
  module order and custom-content sections are otherwise identical.
- **known limitation**: with `skip_consensus_peaks = true` the IGV/MultiQC
  consensus inputs (`consensus_peaks.bed`, featureCounts summary) are absent;
  keep the default (`false`) or set `skip_igv`/`skip_multiqc` together.

## Links

- Repository: [oxo-flow-chipseq](https://github.com/oxo-flow-community/oxo-flow-chipseq)
- Upstream: [nf-core/chipseq](https://github.com/nf-core/chipseq) @ `2.1.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
