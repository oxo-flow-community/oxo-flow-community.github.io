# ampliseq completeness audit (2026-08-21)

Upstream: nf-core/ampliseq @ 2.18.0 · Port: `oxo-flow-ampliseq`
(live-verified).

## Mode matrix (upstream — one workflow, huge param surface)

| axis | options |
|---|---|
| inputs | samplesheet / ASV fasta (`--input_fasta`) / folder / multiregion sheet |
| platforms | illumina PE/SE, `--pacbio`, `--iontorrent` |
| amplicon DBs | 16S: silva/gtdb/sbdi-gtdb/rdp/greengenes2 · 18S: pr2 · COI: coidb/midori2-co1 · ITS: unite-fungi/unite-alleuk · nifH: zehr-nifh |
| ITS | `--illumina_pe_its`, `--cut_its` full/its1/its2, `--its_extractor` itsx/itsxrust |
| denoiser | DADA2 ONLY (no UNOISE/QIIME2 denoise at this tag) |
| taxonomy | 6 classifiers: DADA2 (default) / SINTAX / Kraken2 / QIIME2 / VSEARCH LCA / phylogenetic placement (EPA-NG/GAPPA, single-tree + multi-tree phyloplace) / SIDLE (multiregion) |
| post-ASV | vsearch clustering, decontam, SSU barrnap filter, length/codon filters, ITSx cut |
| QIIME2 downstream | automatic: diversity core/alpha/beta, barplots, ANCOM/ANCOM-BC/ANCOM-BC2 |
| features | PICRUSt2, SBDI export, phyloseq/TSE R objects, Rmd report |

17 test profiles covering the matrix.

## Gap tiers vs the port

**P0**: the 5 non-default taxonomy classifiers (SINTAX, Kraken2, QIIME2,
VSEARCH LCA, pplace/phylogenetic placement incl. the multi-tree
phyloplace HMM chain); SIDLE multiregion (12-process chain); ITS branch
(cut_its + itsx/itsxrust + readthrough cutadapt); pacbio/iontorrent
input modes; input_fasta mode; decontam; SSU/length/codon filters;
QIIME2 downstream suite (diversity + ANCOM trio + barplots); PICRUSt2;
SBDI export; double-primer cutadapt.

**P1**: SILVA + UNITE DB licenses (non-commercial/academic; ARB SILVA
terms; figshare SH files) — document, offer free alternatives
(greengenes2, gtdb, pr2, midori2). Not blockers for non-commercial use
but must be flagged.

**P2**: all skip flags, mergepairs/sample-inference strategies,
quality_type, cutadapt params, vsearch cluster id, assign taxlevels,
failure-tolerance toggles, tax_agglom ranges.

Resource gate: EPANG_PLACE/GAPPA_ASSIGN need ≥60GB RAM (matches the
mag-gtdbtk hardware-contract precedent — document per-branch).

## Verdict

Largest param surface of the nf-core batch: 6 classifiers + SIDLE +
QIIME2 analytics beyond the ported DADA2 default. Big P0, mostly
free-software; the license story is limited to SILVA/UNITE DB terms.
