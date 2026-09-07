## Semantic map - how to read it

## Short names and groups (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| refs+aligners | reference::bwa_index_build, reference::star_genomegenerate, reference::bowtie2_index_build, reference::chromap_index_build, reference::blacklist_regions, reference::getchromsizes, reference::gtf2bed, align::bwa_mem, align::star_align, align::bowtie2_align, align::chromap_align |
| sort+merge | align::sort_align, align::mergesamfiles |
| markdup+filter | align::markduplicates, filter::bamtools_filter, filter::sort_filter, filter::sort_name, filter::bam_remove_orphans |
| stats | align::index_align, align::stats_align, align::flagstat_align, align::idxstats_align, align::index_markdup, align::stats_markdup, align::flagstat_markdup, align::idxstats_markdup, filter::index_filter, filter::stats_filter, filter::flagstat_filter, filter::idxstats_filter |
| peaks | peaks::macs3_callpeak, peaks::macs3_callpeak_narrow, peaks::multiqc_custom_peaks, peaks::multiqc_custom_peaks_narrow, peaks::plot_macs3_qc, peaks::plot_macs3_qc_narrow |
| annotate | peaks::homer_annotatepeaks, peaks::homer_annotatepeaks_narrow, peaks::plot_homer_annotatepeaks, peaks::plot_homer_annotatepeaks_narrow |
| frip | peaks::frip_score, peaks::frip_score_narrow |
| tracks | tracks::bedtools_genomecov, tracks::ucsc_bedgraphtobigwig, tracks::deeptools_computematrix, tracks::deeptools_plotprofile, tracks::deeptools_plotfingerprint, tracks::deeptools_plotheatmap, tracks::khmer |
| consensus | consensus::subread_featurecounts, consensus::subread_featurecounts_multi, consensus::homer_annotate_consensus_narrow, consensus::annotate_boolean_peaks_multi, consensus::annotate_boolean_peaks, consensus::macs3_consensus_narrow_multi, consensus::macs3_consensus_narrow, consensus::macs3_consensus, consensus::homer_annotate_consensus_narrow_multi, consensus::deseq2_qc, consensus::deseq2_qc_narrow, consensus::macs3_consensus_multi, consensus::homer_annotate_consensus, consensus::deseq2_qc_multi, consensus::annotate_boolean_peaks_narrow_multi, consensus::deseq2_qc_narrow_multi, consensus::subread_featurecounts_narrow_multi, consensus::annotate_boolean_peaks_narrow, consensus::homer_annotate_consensus_multi, consensus::subread_featurecounts_narrow |
| QC | qc::fastqc, qc::trimgalore, filter::preseq, filter::picard_collectmultiplemetrics, filter::phantompeakqualtools, filter::multiqc_custom_phantompeakqualtools |
| multiqc | report::multiqc, report::multiqc_narrow, report::multiqc_multi, report::multiqc_narrow_multi |
| igv | report::igv, report::igv_narrow, report::igv_multi, report::igv_narrow_multi |

Every drawn edge is a real engine edge (subset check at generation).
