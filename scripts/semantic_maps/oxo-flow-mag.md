**Metagenome assembly and binning pipeline**: given paired-end metagenomic reads, it trims them, removes host and phiX contamination, assembles with SPAdES or MEGAHIT, bins with six tools, quality-checks and classifies them, and delivers a MultiQC report.

**1. Read QC and trimming** — `fastqc_raw` screens raw reads while one of three clip tools trims them (`fastp` by default, `adapterremoval_pe` or `trimmomatic`). Reads pass `host_removal_build` → `host_removal_align` with a host reference, and `phix_build` → `phix_align`; `fastqc_trimmed` re-reports the reads, `bbnorm` can normalize coverage, and `spades` and `megahit` each assemble the cleaned reads.

**2. Assembly checks** — `gunzip_spades` unpacks the scaffolds; `quast_spades` scores the assembly and `prodigal_spades` predicts its proteins, each with a MEGAHIT twin; `genomad_spades`/`genomad_megahit` identify viruses when enabled.

**3. Mapping and binning** — `bowtie2_build_spades` indexes each assembly; `bowtie2_align_spades` maps every cohort sample's reads, and `depths_spades` → `convert_depths_spades` compute binning depths. Six binner families then cluster the contigs: `metabat2_spades`, `maxbin2_spades`, `comebin_spades`, `semibin_spades`, the CONCOCT chain `concoct_cutup_spades` → `concoct_table_spades` → `concoct_spades` → `concoct_merge_spades` → `concoct_extract_spades`, and the MetaBinner chain (`metabinner_kmer_spades` → `metabinner_run_spades` → `metabinner_bins_spades`). `split_fasta_metabat2_spades` chunks unbinned contigs and `seqkit_spades_metabat2` records bin length stats.

**4. Bin QC** — `ale_spades`/`ale_megahit` evaluate each assembly against mapped reads. Per binner–assembler pair, `busco_spades_metabat2`, `quast_bins_spades_metabat2` and `mag_depths_spades_metabat2` assess the bins; optional checks: `checkm_lineagewf_spades_metabat2` → `checkm_qa_spades_metabat2`, `checkm2_spades_metabat2`, and `gunc_spades_metabat2` → `gunc_mergecheckm_spades_metabat2`. `concat_busco`, `concat_quast` and `mag_depths_summary` merge the per-pair tables.

**5. Classification and annotation** — `gtdbtk_db_preparation` prepares the database; `gtdbtk_spades_metabat2` and its per-binner siblings classify bins, `gtdbtk_summary` merges results and `prokka_spades_metabat2` annotates genes. Optional, config-gated extras: DAS Tool refinement (`dastool_dastool_spades`), Tiara domain classification (`tiara_tiara_spades` → `tiara_classify_spades_metabat2_bins`), CAT/BAT (`cat_db_preparation` → `catpack_bins_spades_metabat2` → `catpack_addnames_spades_metabat2` → `catpack_summarise_spades_metabat2`, plus `catpack_bat_summary`).

**6. Summary** — `bin_summary` merges the QC and taxonomy tables; `multiqc` reports them all.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
