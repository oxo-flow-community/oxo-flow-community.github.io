**ChIP-seq peak calling and differential analysis pipeline** (nf-core/chipseq port): given reads and a reference genome, it aligns, filters, deduplicates, calls broad or narrow peaks, quantifies the per-antibody consensus, and reports via MultiQC and IGV.

**1. Read QC and reference prep** — `fastqc` reports raw-read quality; `trimgalore` trims adapters, feeding every aligner. Gated steps `gtf2bed`, `blacklist_regions`, `getchromsizes` and index builders `bwa_index_build`, `bowtie2_index_build`, `chromap_index_build`, `star_genomegenerate` feed their own aligner only.

**2. Alignment** — one of `bwa_mem`, `star_align`, `bowtie2_align`, `chromap_align` runs per sample; all converge into `sort_align`, fanning out to the `index_align`/`stats_align`/`flagstat_align`/`idxstats_align` quartet and `mergesamfiles`; Picard `markduplicates` follows.

**3. Filtering and library QC** — `bamtools_filter` → `sort_name` → `bam_remove_orphans` → `sort_filter` → `index_filter`/`stats_filter`/`flagstat_filter`/`idxstats_filter`, while `preseq`, `picard_collectmultiplemetrics`, `phantompeakqualtools` → `multiqc_custom_phantompeakqualtools` run in parallel.

**4. Tracks and peak calling** — `bedtools_genomecov` scales coverage, `ucsc_bedgraphtobigwig` makes bigWigs, `deeptools_computematrix` feeds `deeptools_plotprofile`/`deeptools_plotheatmap`, `deeptools_plotfingerprint` contrasts IP/control, `khmer` estimates genome size; `macs3_callpeak`/`macs3_callpeak_narrow` call peaks, with `frip_score`, `multiqc_custom_peaks`, `homer_annotatepeaks`, `plot_macs3_qc`, `plot_homer_annotatepeaks`.

**5. Consensus, quantification and reporting** — `macs3_consensus` merges IP peaks into a per-antibody consensus feeding `homer_annotate_consensus` → `annotate_boolean_peaks` and `subread_featurecounts` → `deseq2_qc`; per-antibody siblings `macs3_consensus_multi`/`deseq2_qc_multi` run in multi-antibody mode. Finally `multiqc` aggregates QC and consensus into a report, and `igv` builds an IGV session over bigWigs and peaks.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
