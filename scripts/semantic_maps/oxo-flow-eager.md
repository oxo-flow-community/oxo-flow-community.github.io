**Ancient-DNA (aDNA) pipeline**: given a reference and raw reads, it clips adapters, maps and deduplicates, estimates damage, runs QC, and optionally genotypes or screens metagenomically — all feeding one MultiQC report.

**1. Reference preparation** — `make_fasta_index`, `make_seq_dict` and `make_bwa_index` index the reference (conditional `unzip_reference` decompresses gzipped input first); branch builders `circulargenerator`, `sexdeterrmine_prep` and `mask_reference_for_pmdtools` draw from the same processed reference.

**2. Read QC and cleanup** — `fastqc` checks raw reads; `fastp` optionally filters poly-G; `adapter_removal` clips adapters and merges the ends, feeding `fastqc_after_clipping` and optional `post_ar_fastq_trimming`.

**3. Mapping and deduplication** — `bwa_aln` maps the merged reads, `samtools_flagstat` reports stats, and either `markduplicates` or alternative `dedup` removes duplicates. When configured, `bwamem` (with optional `hostremoval_input_fastq`), `bowtie2` (with `make_bt2_index`) or `circularmapper` replaces `bwa_aln`.

**4. Ancient-DNA analytics** — the mapped BAM feeds `preseq`; the deduplicated BAM feeds `damageprofiler` (with the indexed reference), `qualimap`, and optional `bedtools_coverage`, `bam_trim`, `picard_addorreplacereadgroups`, `mapdamage_calculation`, `mapdamage_rescaling`, `pmdtools`, `mtnucratio`, `sexdeterrmine`, `nuclear_contamination` → `print_nuclear_contamination`; `endor_spy` follows the flagstat stats.

**5. Optional genotyping** — `genotyping_pileupcaller` → `eigenstrat_snp_coverage`; alternatively `genotyping_ug`, `genotyping_hc`, `genotyping_freebayes` or `genotyping_angsd`, with `vcf2genome` and `multivcfanalyzer` consuming the UnifiedGenotyper VCFs.

**6. Optional metagenomics** — the four mapper filters (`samtools_filter_bwaaln`, `samtools_filter_bwamem`, `samtools_filter_bowtie2`, `samtools_filter_circularmapper`) feed `samtools_flagstat_after_filter`, and unmapped reads flow through `metagenomic_complexity_filter` into either `kraken` → `kraken_parse` → `kraken_merge` or `malt` → `maltextract`.

**7. Reporting** — `multiqc` aggregates every route into one report.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
