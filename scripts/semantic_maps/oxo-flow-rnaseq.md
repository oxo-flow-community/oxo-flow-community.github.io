**RNA-seq analysis pipeline** (oxo-flow port of nf-core/rnaseq): given raw reads plus a genome FASTA and GTF, it trims, aligns, marks duplicates, quantifies expression and runs BAM QC, all unified in a MultiQC report; config keys pick branches (aligner, skip_bbsplit, remove_ribo_rna, with_umi, pseudo_aligner), defaulting to star_salmon.

**1. Reference preparation** — `prepare_genome::gene_bed`, `prepare_genome::chrom_sizes` and `prepare_genome::transcript_fasta` derive the gene BED, chromosome sizes and transcript FASTA from genome + GTF feeding RSeQC, the bigWig chain and Salmon/Kallisto/Bowtie2 steps.

**2. Read QC and trimming** — `fastq_qc::fq_lint_raw` lints raw FASTQs and `fastq_qc::fastqc_raw` runs FastQC; `fastq_qc::trimgalore` trims adapters (internal FastQC) and `fastq_qc::fq_lint_trimmed` lints trimmed reads. In UMI mode `fastq_qc::umitools_extract_umis` runs first, feeding `fastq_qc::trimgalore_umi`.

**3. Optional read filters** — trimmed reads may go to BBSplit (`fastq_qc::bbsplit_index` → `fastq_qc::bbsplit`) and rRNA removal — SortMeRNA (`fastq_qc::rrna_fastas_prepare` → `fastq_qc::sortmerna_index` → `fastq_qc::sortmerna`) or the Bowtie2 route (`fastq_qc::bowtie2_align_rrna` → `fastq_qc::samtools_view_rrna` → `fastq_qc::samtools_fastq_rrna`).

**4. Alignment** — star_salmon (default) aligns trimmed reads with `alignment::star_align`; star_rsem picks `alignment::star_align_rsem`; HISAT2/Bowtie2 modes use `alignment::hisat2_align` / `alignment::bowtie2_align` after `alignment::hisat2_index` (`alignment::hisat2_splicesites`) and `alignment::bowtie2_index`. BAMs are sorted (`alignment::samtools_sort`, `alignment::samtools_sort_hisat2`, `alignment::samtools_sort_bowtie2`), indexed (`alignment::samtools_index_sorted`), statted (`alignment::samtools_stats_sorted`), and marked (`alignment::picard_markduplicates` → `alignment::samtools_index_markdup`); UMI mode uses `alignment::bam_dedup_genome_umitools` / `alignment::bam_dedup_genome_umicollapse`.

**5. Quantification** — `quantification::salmon_quant` quantifies the STAR transcriptome BAM; `quantification::tx2gene` → `quantification::tximport` → `quantification::summarizedexperiment` merge to RDS objects; `quantification::stringtie` assembles reference transcripts. RSEM (`quantification::rsem_calculateexpression` → `quantification::rsem_merge_counts`) and pseudo-alignment (`quantification::salmon_quant_pseudo` / `quantification::kallisto_quant_pseudo`) routes mirror it, each ending in a DESeq2 QC (`quantification::deseq2_qc`, `quantification::deseq2_qc_rsem`, `quantification::deseq2_qc_pseudo`).

**6. BAM QC and tracks** — `bam_qc::featurecounts` counts reads (`bam_qc::biotype_multiqc` table); the RSeQC suite (`bam_qc::rseqc_infer_experiment`, `bam_qc::rseqc_read_distribution`), `bam_qc::dupradar` and `bam_qc::samtools_sort_qualimap` → `bam_qc::qualimap_rnaseq` profile the BAM; `bigwig::genomecov_fw` / `bigwig::genomecov_rev` / `bigwig::genomecov_combined` become the `bigwig::bigwig_fw` / `bigwig::bigwig_rev` / `bigwig::bigwig_combined` tracks.

**7. Reporting** — `multiqc_custom_content` builds fail_trimmed/fail_mapped tables and strand-check JSONs; `multiqc` aggregates everything into one report.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
