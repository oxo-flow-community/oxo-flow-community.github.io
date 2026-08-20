# scrnaseq completeness audit (2026-08-21)

Upstream: nf-core/scrnaseq @ 4.2.0 · Port: `oxo-flow-scrnaseq` (23 rules,
cellranger-based path, live-verified).

## Mode matrix (upstream)

Single workflow, 6 aligner modes via `--aligner` (default `simpleaf`),
protocol matrix via `--protocol` (10XV1-4/dropseq/smartseq/custom), plus
per-mode samplesheet columns (cellrangerarc `sample_type`, cellrangermulti
`feature_type`).

| mode | 10x 3' | Drop-seq | Smart-seq3 | ATAC/Multiome | VDJ | Multi-modal |
|---|---|---|---|---|---|---|
| simpleaf (default) | ✓ | ✓ | — | — | — | — |
| kallisto (kb) | ✓ | ✓ | ✓ | — | — | — |
| star (STARsolo) | ✓ | ✓ | ✓ | — | — | — |
| cellranger | ✓ auto/SC3Pv1-4 | — | — | — | — | — |
| cellrangerarc | — | — | — | ✓ | — | — |
| cellrangermulti | ✓ auto | — | — | — | ✓ | ✓ (gex/vdj/ab/crispr/cmo) |

Smart-seq2 explicitly routed to nf-core/rnaseq; cell hashing not supported.

## Gap tiers vs the port

**P0** (portable, must port):
- **simpleaf** (upstream DEFAULT): SIMPLEAF_INDEX (piscem) / SIMPLEAF_QUANT
  (alevin-fry, unfiltered-pl) / QCATCH empty-drop QC — all OSS.
- **kallisto**: KALLISTOBUSTOOLS_REF / COUNT (kb_workflow standard|lamanno|
  nac) — OSS.
- **star**: STAR_GENOMEGENERATE / STAR_ALIGN (STARsolo; --star_feature
  Gene|GeneFull|Velocyto) + STAR_GENOMEPARAMS_UPGRADE legacy-index path —
  OSS.
- **cellrangerarc** (10x ATAC/Multiome): CELLRANGERARC_MKGTF/MKREF/COUNT.
- **cellrangermulti**: PARSE_CELLRANGERMULTI_SAMPLESHEET,
  CELLRANGER_MKVDJREF, CELLRANGER_MULTI + optional refs
  (--gex_frna_probe_set/--gex_target_panel/--gex_cmo_set/--fb_reference/
  --vdj_inner_enrichment_primers).

**P1** (license): Cell Ranger container is 10x-EULA'd AND container-only
(hard-fails under conda profiles). The port's existing cellranger path
already accepts this constraint — document it uniformly across all
cellranger-family modes.

**P2** (config variants): protocol matrix, --skip_fastqc/--skip_qcatch/
--skip_cellbender/--skip_multiqc, index pre-supply (--*_index/--txp2gene),
--barcode_whitelist, --save_align_intermeds, cellbender GPU toggle,
iGenomes --genome entries, cellranger-multi per-type channels.

Shared tail (all modes): FASTQC, GUNZIP_FASTA/GTF, GTF_GENE_FILTER,
GTF_SOURCE_FIX (cellranger family + iGenomes), MTX_TO_H5AD,
CONCAT_H5AD, ANNDATAR_CONVERT, CELLBENDER_REMOVEBACKGROUND (raw-only,
not cellrangerarc), MULTIQC.

Dead at this tag: GFFREAD_TRANSCRIPTOME, gffread, unzip modules.

## Notes

- The port's live-verified path = cellranger, which is NOT upstream's
  default mode (simpleaf). Coverage verdict: `default-path` with a large
  P0 surface (5 of 6 aligner modes).
- Cellbender CPU fallback exists (GPU image only with ext.use_gpu).
- External deps: iGenomes AWS S3 refs, Seqera Wave/community containers
  (mtx_to_h5ad/anndatar_convert/qcatch) — registry dependency, not a gate.
