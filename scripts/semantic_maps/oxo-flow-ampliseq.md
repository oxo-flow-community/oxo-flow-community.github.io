**Amplicon sequencing pipeline** (16S/ITS): given raw paired-end reads, it renames, quality-checks, and trims them, denoises with DADA2 into ASVs, assigns taxonomy, and produces QIIME2 taxa barplots, diversity, and differential-abundance results.

**1. Input preparation** — `rename_raw_data_files` gives samples consistent FASTQ names; `fastqc` checks the renamed reads while `cutadapt` trims primers.

**2. Trimming and truncation** — `cutadapt_summary` collects and `cutadapt_summary_merge` merges cutadapt trimming metrics. On trimmed reads, `dada2_quality_fw`/`dada2_quality_rv` quality profiles inform truncation lengths (`trunclen_fw`, `trunclen_rv`) applied by `dada2_filtntrim`.

**3. DADA2 denoising** — `dada2_err` learns error models, `dada2_denoising` denoises and merges pairs, `dada2_rmchimera` removes bimeras; `dada2_stats` tracks reads per sample and `dada2_merge` publishes the ASV table, fasta, RDS.

**4. ITS branch** — in ITS runs, `itsx_cutasv` and `itsxrust_cutasv` are alternative ITS extractors (runtime-conditional); both feed `filter_len_itsx`, length-filtering ITS-cut ASVs.

**5. Taxonomy** — `download_taxonomy_db` fetches the SBDI-GTDB reference, `format_taxonomy` reformats it; `dada2_taxonomy` assigns 16S taxonomy while `dada2_taxonomy_its` maps taxonomy back to full ASVs.

**6. QIIME2 analysis** — `qiime2_inasv`/`qiime2_inseq` import ASV tables and sequences, ITS via `qiime2_inasv_its`/`qiime2_inseq_its`, and taxonomy via `qiime2_intax`. Sequences feed `qiime2_diversity_tree` and `qiime2_classify`; `qiime2_diversity_core` precedes `qiime2_diversity_alpha`, `qiime2_diversity_beta`, `qiime2_diversity_betaord`; `qiime2_barplot` renders taxa barplots; exports (`qiime2_export_absolute`, `qiime2_export_relasv`, `qiime2_export_reltax`) and ANCOM tests (`qiime2_ancom`, `qiime2_ancombc`, `qiime2_ancombc2`, using `qiime2_metadata_categories`) complete the output.

**7. Reporting** — `merge_stats` merges cutadapt and DADA2 statistics, `multiqc` aggregates FastQC and cutadapt reports, and `picrust` runs PICRUSt2 predictions from the ASV table.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
