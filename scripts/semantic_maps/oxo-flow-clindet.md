**clindet pipeline**: one entry point (`wes`/`wgs` = DNA, `rna` = RNA) calling somatic, germline and tumor-only variants, copy-number, SV, fusion and QC analysis, ending in merged VCF/MAF, case report and MultiQC.

**Shared inputs** — pairs split into tumor/normal: `fastp_tumor_sample`/`fastp_normal_sample` trim, BWA mem aligns (`map_reads_tumor`, `map_reads_normal`), `mark_duplicates_tumor`/`mark_duplicates_normal` deduplicate, and `recal_link_tumor`/`recal_link_normal` (or `recalibrate_base_qualities_tumor` → `apply_base_quality_recalibration_tumor`, BQSR on) feed DNA rules.

**DNA module**

1. **Sequencing quality** — `bam_flagstat_tumor`/`bam_flagstat_normal`; `bed_to_interval_list` feeds `picard_collect_wes_tumor`/`picard_collect_wes_normal` (WGS: `picard_collect_wgs_tumor`, `picard_flength_wgs_tumor`); `prep_multiqc_data` and WGS/tumor-only variants lead to `combined_multiqc_prep_multiqc_data` → `combined_multiqc`.

2. **Somatic and germline calling** — `call_variants_HaplotypeCaller`, `vardict_paired_mode` → `vardict_filter_somatic`, `varscan2_mpileup` → `varscan2_call` → `varscan2_som_filter` → `varscan2_merge_somatic`, MuSE `muse_call` → `muse_sump`, Mutect2 (`mutect2`, `M2_ST`/`M2_SNC` → `M2_contam` → `M2_filter`), CaVEMan `CM_call` → `CM_flag`/`CM_germ_flag`; germline: `call_config_strelka` → `call_strelka_manta_germline`/`call_strelka_somatic_manta` → `merge_strelka_manta`/`merge_strelka_somatic_manta`; WGS reruns them on whole-genome data.

3. **Tumor-only calling** — control-less pairs run `unpaired_mutect2_call` → `M2_filter_unpaired`, `unpaired_call_config_strelka` → `unpaired_call_strelka_manta` → `unpaired_strelka_filter`, `unpaired_vardict_single_mode` → `unpaired_filter_vardict`, `lofreq_somatic_unpaired` → `unpair_lofreq_filter`, `varscan2_mpileup_unpaired` → `varscan2_merge_unpaired` (via `varscan2_call_unpaired_snp`/indel twin), plus `unpaired_call_variants_HaplotypeCaller`/`unpaired_freebayes`; `merge_unpaired_vcf` → `all_unpaired`.

4. **Normalization and outputs** — `vcf_norm_Mutect2`/`vcf_norm_vardict` and twins precede MAF conversion (`vcf2maf_Mutect2` and siblings); `merge_paired_vcf` → `all_vcf`; `merge_paired_maf` feeds `flag_mutation_pairead_maf` (`make_region_bed_list`) and `run_cancer_report`. CNV (`freec_config` → `freec_call_paired` → `plot_freec`; `sequenza_bam2seqz` → `sequenza_seqz_binning` → `sequenza_call`; `CNA_ASCAT` → `ASCAT_EXTRACT_PURITYPLOIDY`, `CNA_exomedepth`) fills `all_cnv`; WGS SVs (`SV_delly` → `SV_delly_filter_somatic` → `SV_delly_to_vcf` → `delly_filter` → `delly2bnd`, `SV_svaba` → `SV_sansa_anno_svaba`, Manta via `call_config_strelka_wgs`) fill `all_sv`.

**RNA module**

1. **QC, alignment, quant** — `fastp_trim`; `STAR_1_pass`, then `STAR_arriba_map`/`STAR_mut_map` re-align (plus `STAR_isofox_map` → `isofox_call`, `cal_exp_RSEM` → `RSEM_sort_genome`).
2. **Fusion and immune receptors** — `arriba_fusion` → `arriba_draw` (plus RSEM BAM) and `TRUST4_TBCR`.
3. **Mutation and MAF** — `link_bam` → `SplitNCigarReads` unlocks `mutect2_call` → `M2_filter_unpaired_rna`, `call_variants_HaplotypeCaller_rna`, `unpaired_freebayes_rna`, `unpaired_call_config_strelka_rna` → `unpaired_call_strelka_manta_rna` → `unpaired_strelka_filter_rna`, `lofreq_call_up` → `lofreq_norm_filter`, `unpaired_vardict_single_mode_rna` → `unpaired_filter_vardict_rna`, and the varscan2 RNA chain (`varscan2_mpileup_unpaired_rna` → SNP/indel calls → `varscan2_filter_snp` and the indel twin → `varscan2_merge_unpaired_rna`); each converts to MAF (`vcf2maf_rna_freebayes`, `vcf2maf_rna_Mutect2` and siblings).

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
