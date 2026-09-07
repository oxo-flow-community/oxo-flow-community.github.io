## Semantic map - how to read it

## Short names and groups (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| refprep | make_bwa_index, make_fasta_index, make_seq_dict, unzip_reference, make_bt2_index, circulargenerator, mask_reference_for_pmdtools, sexdeterrmine_prep |
| preprocess | fastp, adapter_removal, post_ar_fastq_trimming, fastqc_after_clipping, fastqc |
| align | bwa_aln, bwamem, bowtie2, circularmapper, samtools_filter_bwaaln, samtools_filter_bwamem, samtools_filter_bowtie2, samtools_filter_circularmapper, samtools_flagstat_after_filter, convert_bam, bcftools_stats, hostremoval_input_fastq |
| dedup | markduplicates, dedup, samtools_flagstat |
| genotype | genotyping_pileupcaller, eigenstrat_snp_coverage, genotyping_ug, genotyping_hc, genotyping_freebayes, genotyping_angsd, vcf2genome, multivcfanalyzer |
| ancient_damage | damageprofiler, qualimap, endor_spy, sexdeterrmine, mtnucratio, nuclear_contamination, print_nuclear_contamination, mapdamage_calculation, mapdamage_rescaling, pmdtools, bedtools_coverage, bam_trim, picard_addorreplacereadgroups, preseq |
| metagenome | metagenomic_complexity_filter, kraken, kraken_parse, kraken_merge, malt, maltextract |
| multiqc | multiqc |

Every drawn edge is a real engine edge (subset check at generation).
