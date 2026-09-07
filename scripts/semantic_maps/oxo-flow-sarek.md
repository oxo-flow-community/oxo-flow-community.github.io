## Semantic map - how to read it

## Short names and groups (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| prep | bwa_index, bwamem2_index, gatk_createsequencedictionary, samtools_faidx |
| fq | fastqc |
| trim | fastp, fastp_split |
| umi | fgbio_fastqtobam, samtools_bam2fq_umi, bwa_mem_umi, fgbio_groupreadsbyumi, fgbio_callmolecularconsensusreads, samtools_bam2fq_consensus, fastp_umi |
| aligners | bwa_mem, bwa_mem2, bwa_mem_split, bwa_mem2_split |
| dedup | bam_merge_index_samtools, gatk_markduplicates, gatk_markduplicates_bam, mosdepth_md, samtools_stats_md |
| bqsr | gatk_baserecalibrator, gatk_applybqsr, samtools_index_recal, mosdepth_recal, samtools_stats_recal, samtools_reindex_bam, goleft_indexcov |
| scatter | create_intervals_bed, tabix_interval, gatk_baserecalibrator_scatter, gatk_gatherbqsrreports, gatk_applybqsr_scatter, merge_index_samtools |
| callers | gatk_haplotypecaller, gatk_cnnscorevariants, gatk_filtervarianttranches, freebayes, bcftools_sort_freebayes, tabix_freebayes, vcffilter_freebayes, tabix_freebayes_filt, strelka_germline, manta_germline, bcftools_mpileup_call, tiddit_sv, tabix_tiddit, deepvariant, bcftools_mpileup_ngscheckmate, ngscheckmate_ncm, gatk_haplotypecaller_scatter, gatk_mergevcfs_scatter |
| joint | gatk_haplotypecaller_gvcf, gatk_genomicsdbimport, gatk_genotypegvcfs, bcftools_sort_joint, gatk_mergevcfs_joint, gatk_variantrecalibrator_snp, gatk_variantrecalibrator_indel, gatk_applyvqsr_snp, gatk_applyvqsr_indel, gatk_haplotypecaller_gvcf_scatter, gatk_genomicsdbimport_scatter, gatk_genotypegvcfs_scatter, bcftools_sort_joint_scatter, gatk_mergevcfs_joint_scatter |
| stats | bcftools_stats, vcftools_tstv_count, vcftools_tstv_qual, vcftools_filter_summary, ensemblvep_vep, bcftools_stats_freebayes, vcftools_tstv_count_freebayes, vcftools_tstv_qual_freebayes, vcftools_filter_summary_freebayes, ensemblvep_vep_freebayes, bcftools_stats_strelka, vcftools_tstv_count_strelka, vcftools_tstv_qual_strelka, vcftools_filter_summary_strelka, ensemblvep_vep_strelka, bcftools_stats_mpileup, vcftools_tstv_count_mpileup, vcftools_tstv_qual_mpileup, vcftools_filter_summary_mpileup, ensemblvep_vep_mpileup, bcftools_stats_deepvariant, vcftools_tstv_count_deepvariant, vcftools_tstv_qual_deepvariant, vcftools_filter_summary_deepvariant, ensemblvep_vep_deepvariant, bcftools_stats_manta, vcftools_tstv_count_manta, vcftools_tstv_qual_manta, vcftools_filter_summary_manta, ensemblvep_vep_manta, bcftools_stats_tiddit, vcftools_tstv_count_tiddit, vcftools_tstv_qual_tiddit, vcftools_filter_summary_tiddit, ensemblvep_vep_tiddit, bcftools_stats_joint, vcftools_tstv_count_joint, vcftools_tstv_qual_joint, vcftools_filter_summary_joint, ensemblvep_vep_joint |
| report | multiqc |

Every drawn edge is a real engine edge (subset check at generation).
