# nanoseq completeness audit (2026-08-21)

Upstream: nf-core/nanoseq @ 3.1.0 · Port: `oxo-flow-nanoseq` (live-verified).

Headline: NO basecalling at this tag (guppy removed as EULA breach,
dorado never added) — pre-basecalled inputs only. No methylation/polyA.

## Mode matrix (upstream — param-driven, one entry)

| mode | selecting params |
|---|---|
| demux | `--input_path` + `--barcode_kit` → QCAT (off via --skip_demultiplexing) |
| alignment | `--aligner` minimap2(default)/graphmap2; --protocol DNA/cDNA/directRNA; BAM input via `--skip_alignment` |
| short VC (DNA only) | `--call_variants` + `--variant_caller` medaka(default)/deepvariant/pepper_margin_deepvariant |
| SV (DNA only) | `--structural_variant_caller` sniffles(default)/cutesv |
| quantification + DE | cDNA/directRNA; `--quantification_method` bambu(default)/stringtie2; DESeq2/DEXSeq |
| RNA modification | directRNA + fast5/fastq dirs; nanopolish eventalign + xpore + m6anet |
| fusion | cDNA/directRNA; JAFFAL (+ figshare ref download) |
| QC | NanoLyse / NanoPlot / FastQC / MultiQC |

## Gap tiers vs the port

**P0**: graphmap2 aligner; BAM-input mode; deepvariant + pepper_margin
callers (container-only); cutesv; stringtie2 + featureCounts quant path;
DEXSeq; RNA modification chain (nanopolish/xpore/m6anet — container-only,
fast5 inputs); JAFFAL fusion; NanoLyse; demux via QCAT + barcode kits.

**P1**: ONT basecalling EULA (user-side prerequisite — document, not
portable); deepvariant/pepper/m6anet/dexseq are container-only (conda
profile hard-fails — porting requires container path or documented
constraint).

**P2**: --skip_* gates, --stranded, qcat score options, jaffal ref dir,
nanolyse fasta, iGenomes refs. Dead params at this tag: --gpu_device,
--split_mnps, --phase_vcf, --save_align_intermeds, --trim_barcodes
(declared, unused).

External deps: figshare JAFFAL ref, GitHub lambda.fasta, nf-core test
datasets, S3 iGenomes.

## Verdict

Moderate surface: the ported default (minimap2 + medaka/sniffles + bambu)
leaves ~5 feature modes as P0, with the container-only VC callers as the
main porting constraint.

## Re-verification (2026-08-23, light group)

Engine: latest main (post-v0.14.1) · Box: tx-ubuntu · Mode: real CLI
run, not dry-run.

**29/29 rules succeeded, exit 0, one round, zero failures** at the
latest commit. No fixes needed and no new failure classes — the
default path runs clean against the reference data with no
intervention.
