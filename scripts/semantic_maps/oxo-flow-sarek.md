**oxo-flow-sarek pipeline**: WGS/WES germline variant calling from raw FASTQ to annotated VCFs and a MultiQC report — a community port of nf-core/sarek 3.10.0.

**1. Reference preparation** — `bwa_index` or `bwamem2_index` builds the aligner index, `gatk_createsequencedictionary` the sequence dictionary, and `samtools_faidx` the FASTA index; all config-gated on the prepare_reference flag.

**2. Read QC and trimming** — `fastqc` screens raw reads; `fastp` trims and splits them (multipart alternative `fastp_split`). With UMI consensus preprocessing, a fgbio chain runs first: `fgbio_fastqtobam` → `samtools_bam2fq_umi` → `bwa_mem_umi` → `fgbio_groupreadsbyumi` → `fgbio_callmolecularconsensusreads` → `samtools_bam2fq_consensus` → `fastp_umi`.

**3. Alignment (exclusive runtime routes)** — `fastp`, `fastp_split`, and `fastp_umi` feed the BWA-MEM and BWA-MEM2 aligners: `bwa_mem`/`bwa_mem2` single-part, or `bwa_mem_split`/`bwa_mem2_split` per split part, gathered by `bam_merge_index_samtools`. The aligned BAM is deduplicated by `gatk_markduplicates` (CRAM mode) or `gatk_markduplicates_bam` (BAM mode); the deduplicated file also feeds `mosdepth_md` and `samtools_stats_md`.

**4. Base quality recalibration** — `gatk_baserecalibrator` builds the recalibration table and `gatk_applybqsr` applies it; `samtools_index_recal` indexes the recalibrated alignment (required upstream of `mosdepth_recal`), while `samtools_stats_recal` summarizes it.

**5. Variant calling — parallel, config-gated** — all callers share the recalibrated alignment: default `gatk_haplotypecaller` → `gatk_cnnscorevariants` → `gatk_filtervarianttranches`; optional `freebayes` (→ `bcftools_sort_freebayes` → `tabix_freebayes`/`vcffilter_freebayes` → `tabix_freebayes_filt`), `strelka_germline`, `manta_germline`, `bcftools_mpileup_call`, `tiddit_sv` → `tabix_tiddit`, `deepvariant`; cohort checks via `samtools_reindex_bam` → `goleft_indexcov` and `bcftools_mpileup_ngscheckmate` → `ngscheckmate_ncm`. Joint germline instead chains `gatk_haplotypecaller_gvcf` → `gatk_genomicsdbimport` → `gatk_genotypegvcfs` → `bcftools_sort_joint` → `gatk_mergevcfs_joint` → `gatk_variantrecalibrator_snp`/`gatk_variantrecalibrator_indel` → `gatk_applyvqsr_snp` → `gatk_applyvqsr_indel`.

**6. QC, annotation, and aggregate reporting** — each produced VCF fans out to per-caller `bcftools_stats`, `vcftools_tstv_count`, `vcftools_tstv_qual`, and `vcftools_filter_summary` QC plus an `ensemblvep_vep` annotation (e.g. `ensemblvep_vep_freebayes`, `ensemblvep_vep_joint`); with the scatter_gatk option enabled, `create_intervals_bed` → `tabix_interval` feed per-chromosome `gatk_applybqsr_scatter` and `gatk_haplotypecaller_scatter`, gathered back by `merge_index_samtools` and `gatk_mergevcfs_scatter`. Finally `multiqc` aggregates all reports.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
