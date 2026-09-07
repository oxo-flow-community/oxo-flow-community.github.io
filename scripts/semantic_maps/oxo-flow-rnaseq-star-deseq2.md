**RNA-seq differential-expression pipeline** (STAR alignment + DESeq2): given a reference genome and sequencing reads, it aligns, counts, and delivers per-gene expression, differential expression and PCA plots, with quality checks along the way.

**1. Inputs and reference prep** — `get_genome` fetches the reference genome and `get_annotation` the gene annotation (GTF), while `get_sra` fetches the sequencing reads. The genome also produces two auxiliary indexes: `bwa_index` (BWA index) and `genome_faidx` (FASTA index).

**2. STAR index** — `star_index` builds the alignment index from the genome + annotation; every alignment step below depends on it.

**3. Read QC + alignment (four parallel routes)** — paired-end (PE) reads are quality-trimmed by `fastp_pe` then aligned by `star_align`; single-end (SE) reads go through `fastp_se` and `star_align_se`. Two further routes align **raw, untrimmed** reads directly: `star_align_raw` (PE) and `star_align_se_raw` (SE). The run picks PE or SINGLE based on the sample configuration, so 1–2 of the 4 routes actually execute per run.

**4. Converged alignment outputs** — the four routes' BAMs converge into the analysis entry (a hidden junction in the engine), feeding counting and quality simultaneously.

**5. Counting and differential analysis** — `count_matrix` builds the per-gene expression matrix; it directly produces `gene_2_symbol_counts` (gene-symbol counts) and enters `deseq2_init`. The init step fans out to `deseq2` (the DESeq2 analysis, exported as `gene_2_symbol_diffexp` differential-expression table), `gene_2_symbol_normcounts` (normalised counts), and three PCA rules (`pca_treatment_1`, `pca_treatment_2`, `pca_jointly_handled`).

**6. Quality and aggregate reporting** — `rseqc_gtf2bed` converts the annotation to a BED the 8 RSeQC checks can read (`rseqc_junction_annotation`, `rseqc_junction_saturation`, `rseqc_stat`, `rseqc_infer`, `rseqc_innerdis`, `rseqc_readdis`, `rseqc_readdup`, `rseqc_readgc`); `multiqc` finally aggregates alignment and QC results into one report.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described product relationships follow the actual rule dependencies.*
