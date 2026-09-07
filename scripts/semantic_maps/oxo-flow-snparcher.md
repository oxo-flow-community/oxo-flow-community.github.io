## Semantic map - how to read it

## Short names and groups (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| refprep | prepare_reference, index_reference, picard_intervals, filter_picard_intervals, create_gvcf_intervals, create_db_intervals, create_db_mapfile |
| reads | download_sra, fastp, fastp_srr, stage_external_bam |
| align_dedup | bwa_mem, merge_library_bams, merge_library_level_bams, markdup_library, merge_dedup_libraries, index_bam_csi, index_bam_csi_markdup, index_bam_csi_external |
| callers | postprocess_basic_filter, generate_coords_file, gatk_haplotypecaller_external, mappability_bed, deepvariant_call_markdup, postprocess_strict_filter, mosdepth_external, deepvariant_call_external, glnexus_joint, bam_stats, bam_stats_markdup, bcftools_regions, coverage_bed, genmap_mappability, normalize_external_gvcf_for_gatk, clam_loci, postprocess_drop_indel_snps, postprocess_update_bed, gatk_haplotypecaller_interval_external, gatk_haplotypecaller_markdup, postprocess_subset_snps, deepvariant_call, clam_collect, postprocess_subset_indels, gatk_haplotypecaller, parse_bam_stats, mosdepth_markdup, gatk_genotype_gvcfs_interval, variant_filtration, mosdepth, bcftools_concat_regions, gatk_haplotypecaller_interval_markdup, bam_stats_external, gatk_genomics_db_import_interval, callable_coverage_thresholds, callable_sites_bed, genmap_index, gatk_haplotypecaller_interval, postprocess_filter_individuals, bcftools_call |
| db_import | joint_genomics_db_import, normalize_external_gvcf_for_gatk, create_db_intervals, concat_interval_gvcfs, gatk_genomics_db_import_interval, gatk_genotype_gvcfs_interval |
| genotype | joint_genotype_gvcfs, concat_interval_vcfs, gatk_genomics_db_import_interval, gatk_genotype_gvcfs_interval, gatk_haplotypecaller_interval, gatk_haplotypecaller_interval_markdup, normalize_external_gvcf_for_gatk, gatk_haplotypecaller_interval_external, gatk_haplotypecaller_markdup, gatk_haplotypecaller, gatk_haplotypecaller_external |
| qc | postprocess_drop_indel_snps, collect_fastp_stats, qc_vcftools_individuals, postprocess_basic_filter, qc_prepare_plink_inputs, qc_setup_admixture, qc_contig_map, qc_dashboard, postprocess_subset_indels, qc_plink, postprocess_update_bed, qc_admixture, combine_qc_metrics, qc_subsample_snps, postprocess_subset_snps, qc_copy_qc_report, postprocess_strict_filter, postprocess_filter_individuals |

Every drawn edge is a real engine edge (subset check at generation).
