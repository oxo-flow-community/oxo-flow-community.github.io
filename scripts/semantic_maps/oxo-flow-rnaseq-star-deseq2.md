## Short names used in the semantic map (all are real rules of this workflow)

| Shown | Full rule name(s) |
|---|---|
| genome | get_genome |
| annot | get_annotation |
| SRA | get_sra |
| STAR index | star_index |
| BWA index | bwa_index |
| faidx | genome_faidx |
| fastp PE / fastp SE | fastp_pe / fastp_se |
| STAR PE | star_align (paired-end trimmed alignment) |
| STAR PE raw | star_align_raw (paired-end raw-read alignment) |
| STAR SE | star_align_se (single-end trimmed alignment) |
| STAR SE raw | star_align_se_raw (single-end raw-read alignment) |
| rseqc gtf2bed | rseqc_gtf2bed |
| rseqc QC | rseqc_junction_annotation, rseqc_junction_saturation, rseqc_stat, rseqc_infer, rseqc_innerdis, rseqc_readdis, rseqc_readdup, rseqc_readgc |
| counts | count_matrix |
| DESeq2 init / DESeq2 | deseq2_init / deseq2 |
| gene2 counts / norm / diffexp | gene_2_symbol_counts / gene_2_symbol_normcounts / gene_2_symbol_diffexp |
| PCA | pca_treatment_1, pca_treatment_2, pca_jointly_handled |
| MultiQC | multiqc |

The `_aligned` junction is a hidden routing point: all four STAR alignment
lanes converge there, and its in- and out-edges are exactly the real DAG
edges of those lanes.

## Path-level aggregation (edges elided on the map, all real in the DAG)

- annot feeds all four STAR lanes directly; the map aggregates this to
  `annot → STAR index` (the reference-prep route the lanes share).
- STAR index feeds the two raw-read lanes; shown via the shared index hop.
- rseqc gtf2bed feeds 5 of the 8 rseqc QC checks (junction/infer/innerdis/
  readdis-related checks); kept as the rseqc QC group, per-check edges are
  visible in the rule-level detail card.
- get_sra → STAR PE raw is the raw-read entry for the PE raw lane (added).
