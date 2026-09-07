## Semantic map - how to read it

## Short names and groups (all are real rules)

| Shown | Full rule name(s) |
|---|---|
| genome | get_genome |
| annot | get_annotation |
| SRA | get_sra |
| STAR_index | star_index |
| BWA_index | bwa_index |
| faidx | genome_faidx |
| fastp_PE___fastp_SE | fastp_pe / fastp_se |
| STAR_PE | star_align (paired-end trimmed alignment) |
| STAR_PE_raw | star_align_raw (paired-end raw-read alignment) |
| STAR_SE | star_align_se (single-end trimmed alignment) |
| STAR_SE_raw | star_align_se_raw (single-end raw-read alignment) |
| rseqc_gtf2bed | rseqc_gtf2bed |
| rseqc_QC | rseqc_junction_annotation, rseqc_junction_saturation, rseqc_stat, rseqc_infer, rseqc_innerdis, rseqc_readdis, rseqc_readdup, rseqc_readgc |
| counts | count_matrix |
| DESeq2_init___DESeq2 | deseq2_init / deseq2 |
| gene2_counts___norm___diffexp | gene_2_symbol_counts / gene_2_symbol_normcounts / gene_2_symbol_diffexp |
| PCA | pca_treatment_1, pca_treatment_2, pca_jointly_handled |
| MultiQC | multiqc |

Every drawn edge is a real engine edge (subset check at generation).
