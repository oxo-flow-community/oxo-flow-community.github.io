## Semantic map — how to read it

Atac-seq can start from several inputs at once (trimmed reads, reference
index/prep, PE replicates) and ends in two collector hubs (the report
collection vs the QC/metrics suite) — the route drawing below the module
overview keeps the hub structure exact while the Overview card gives the
compact module-level story. Main pipeline (grey): reads → align → sort +
merge → dedup → peak calling → annotation → QC/bigwig → reports.
Coloured routes: orange PE track, green alt aligners, blue references,
yellow reporting.

## Short names and groups on this map (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| trimgalore | trimgalore |
| bwa_mem | bwa_mem |
| sort+merge | samtools_sort_stats, picard_mergesamfiles, merge_replicates |
| markdup+filter | picard_markduplicates, bamtools_filter |
| peaks | macs2_callpeak |
| annotate | homer_annotatepeaks |
| frip | frip_score |
| cov+bigwig | bedtools_genomecov, ucsc_bedgraphtobigwig |
| plots | deeptools_plots |
| fingerprint | plotfingerprint |
| alt_aligners | alt::bowtie2_align, alt::chromap_align, alt::star_align |
| ref | ref::bwa_index, ref::custom_getchromsizes |
| PE_track | pe::fastqc_pe, pe::trimgalore_pe, pe::bwa_mem_pe, pe::bamtools_filter_pe, pe::pe_name_sort_remove_orphans, pe::bedtools_genomecov_pe, pe::plotfingerprint_pe, pe::multiqc_pe |
| consensus | cons::macs2_consensus, cons::homer_annotatepeaks_consensus, cons::subread_featurecounts, cons::deseq2_qc |
| qce | qce::preseq_lcextrap, qce::picard_collectmultiplemetrics, qce::get_autosomes, qce::ataqv, qce::mkarv, qce::plot_macs2_qc, qce::plot_homer_annotatepeaks, qce::multiqc_custom_peaks, qce::igv |
| mito | mito::genome_blacklist_regions |
| multiqc | multiqc |
| fastqc | fastqc |

(Every drawn edge is a real engine edge; subset checks run at generation.
No invented connections.)
