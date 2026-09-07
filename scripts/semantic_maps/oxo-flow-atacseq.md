**ATAC-seq peak calling and QC pipeline** (BWA-MEM + MACS2): given a reference genome and FASTQ reads, it trims adapters, aligns, deduplicates, calls peaks, annotates them, and aggregates all QC into a MultiQC report — a port of nf-core/atacseq 2.1.2.

**1. Input QC and trimming** — `fastqc` reports raw-read quality; `trimgalore` trims adapters and re-runs FastQC, feeding every alignment route.

**2. Alignment** — single-end reads are aligned by `bwa_mem` against `ref::bwa_index`, or by one runtime-selected alternative (`alt::bowtie2_align`, `alt::chromap_align`, `alt::star_align`); paired-end reads take `pe::trimgalore_pe` → `pe::bwa_mem_pe`. All routes converge on `samtools_sort_stats`.

**3. Merge, deduplicate, filter** — `picard_mergesamfiles` and `picard_markduplicates` consolidate libraries and mark duplicates (paired reads re-enter via `pe::bamtools_filter_pe` → `pe::pe_name_sort_remove_orphans`); `bamtools_filter` drops unmapped, secondary, and low-quality reads, and, when replicate samples are declared, `merge_replicates` merges the per-replicate filtered BAMs per sample.

**4. Peaks, annotation, FRiP** — `macs2_callpeak` calls broad peaks; `homer_annotatepeaks` annotates them, while `frip_score` measures the fraction of reads in peaks.

**5. Tracks and enrichment plots** — `bedtools_genomecov` writes a million-read-normalized bedGraph (`pe::bedtools_genomecov_pe` paired-end); `ucsc_bedgraphtobigwig` converts it to bigWig for `deeptools_plots`, and `plotfingerprint` (`pe::plotfingerprint_pe`) plots coverage fingerprints.

**6. Consensus peaks (gated)** — `cons::macs2_consensus` merges peak sets into a consensus BED, annotated by `cons::homer_annotatepeaks_consensus` and quantified by `cons::subread_featurecounts`; `cons::deseq2_qc` runs DESeq2 QC.

**7. Extra QC and reports (gated)** — optional branches add `qce::preseq_lcextrap`, `qce::picard_collectmultiplemetrics`, ATAQV (`qce::ataqv` on `qce::get_autosomes`, indexed by `qce::mkarv`), peak QC (`qce::plot_macs2_qc`, `qce::plot_homer_annotatepeaks`, `qce::multiqc_custom_peaks`) and `qce::igv`; `multiqc` (single-end) or `pe::multiqc_pe` (paired-end) aggregates the run.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
