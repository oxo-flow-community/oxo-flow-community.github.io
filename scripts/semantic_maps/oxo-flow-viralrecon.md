## Semantic map - how to read it

## Short names and groups (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| ref | gunzip_fasta, gunzip_gff, gunzip_primer_bed, prepare_genome, untar_kraken2_db, kraken2_build, build_bowtie2_index, get_nextclade_dataset, make_blast_db, build_snpeff_db, build_snpeff_db_additional, collapse_primers, get_primer_fasta, prepare_primer_fasta |
| reads | cat_fastq, fastqc_raw |
| trim | fastp, fastqc_trim |
| kraken | kraken2 |
| align | align_bowtie2 |
| bam | bam_sort_index, ivar_trim, bam_sort_index_trimmed |
| dedup | markduplicates, markduplicates_wgs, picard_metrics, picard_metrics_wgs |
| depth | mosdepth_genome, mosdepth_genome_wgs, plot_mosdepth_genome, mosdepth_amplicon, plot_mosdepth_amplicon |
| freyja | freyja_variants, freyja_variants_wgs, freyja_demix, freyja_boot, freyja_update, freyja_demix_updated, freyja_boot_updated |
| call | call_variants_ivar, call_variants_bcftools, call_variants_bcftools_wgs, ivar_to_vcf, norm_vcf_bcftools |
| vcf | sort_vcf |
| annot | snpeff_ann, snpsift_extract, additional_annotation |
| consensus | consensus_filter, consensus_filter_bcftools, consensus_call, consensus_call_wgs, consensus_ivar, consensus_ivar_wgs |
| clade | quast_consensus, pangolin, pangolin_updatedata, pangolin_run_updated, nextclade, plot_base_density, nextclade_clade_mqc |
| tables | variants_long_table, variants_long_table_bcftools |
| assembly | assembly_fastq |
| cut | cutadapt, fastqc_primers |
| assemblers | assemble_spades, assemble_unicycler, assemble_minia |
| assemblyqc | bandage, blast_assembly, quast_assembly, abacas, plasmidid, bandage_unicycler, blast_assembly_unicycler, quast_assembly_unicycler, abacas_unicycler, plasmidid_unicycler, blast_assembly_minia, quast_assembly_minia, abacas_minia, plasmidid_minia |
| report | multiqc |

Every drawn edge is a real engine edge (subset check at generation).
