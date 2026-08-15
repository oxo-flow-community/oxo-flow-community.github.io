# Selection Report — the founding twenty

**Date:** 2026-08-15 · **Method:** GitHub API data + snakemake catalog, scored by a selection
committee agent against pre-registered criteria, then reviewed by the maintainer.

> This report documents how the first twenty entries in the catalog were chosen. The
> catalog has since opened to original workflows and community submissions — see
> [Curation &amp; ratings](curation.md).

## Method

Data was collected from the live GitHub API on 2026-08-15:

- **nf-core:** `org:nf-core fork:false archived:false`, sorted by stars (30 analysis pipelines
  after excluding infrastructure repos: modules 424★, tools 319★, test-datasets 164★,
  configs 110★, website 98★).
- **Snakemake:** GitHub search `snakemake workflow in:name,description stars:>30` merged with the
  official workflows.snakemake.org catalog listing.

## Criteria (pre-registered weights)

| Criterion | Weight | Definition |
|---|---|---|
| Usage & adoption | 40% | GitHub stars; snakemake-catalog presence |
| Maintenance health | 20% | pushed_at within ~18 months, not archived |
| Portability | 25% | default-parameters main path ≈ 5–45 rules, expressible in oxo-flow |
| Domain diversity | 15% | library-wide coverage across omics domains |

Fidelity scope for every port: the **default-parameters main execution path** is replicated 100%
(tools, versions, command logic); optional/alternate paths are documented as exclusions in each
repo's README fidelity table.

## Selection (20)

| Port repo | Source (engine) @ tag | ★ | Domain | Rules† | Verify |
|---|---|---|---|---|---|
| oxo-flow-rnaseq | nf-core/rnaseq @ 3.26.0 | 1349 | bulk RNA-seq | 14 | ✓ |
| oxo-flow-sarek | nf-core/sarek @ 3.10.0 | 592 | WGS/WES germline | 12 | ✓ |
| oxo-flow-scrnaseq | nf-core/scrnaseq @ 4.2.0 | 349 | single-cell RNA-seq | 8 | |
| oxo-flow-mag | nf-core/mag @ 5.5.0 | 314 | metagenomics | 10 | ✓ |
| oxo-flow-ampliseq | nf-core/ampliseq @ 2.18.0 | 256 | amplicon (16S/ITS) | 8 | |
| oxo-flow-chipseq | nf-core/chipseq @ 2.1.0 | 242 | ChIP-seq | 10 | ✓ |
| oxo-flow-nanoseq | nf-core/nanoseq @ 3.1.0 | 228 | nanopore long-read | 6 | |
| oxo-flow-atacseq | nf-core/atacseq @ 2.1.2 | 226 | ATAC-seq | 9 | |
| oxo-flow-eager | nf-core/eager @ 2.5.3 | 212 | ancient DNA | 12 | ✓ |
| oxo-flow-fetchngs | nf-core/fetchngs @ 1.12.0 | 200 | fetch/QC utility | 6 | |
| oxo-flow-methylseq | nf-core/methylseq @ 4.2.0 | 197 | WGBS methylation | 8 | |
| oxo-flow-viralrecon | nf-core/viralrecon @ 3.0.0 | 167 | viral genomics | 12 | ✓ |
| oxo-flow-rnaseq-star-deseq2 | snakemake-workflows/rna-seq-star-deseq2 @ v3.1.1 | 370 | bulk RNA-seq | 7 | |
| oxo-flow-snparcher | harvardinformatics/snparcher @ v2.2 | 95 | non-model variant calling | 9 | |
| oxo-flow-varlociraptor | snakemake-workflows/dna-seq-varlociraptor @ v6.10.0 | 90 | small & structural variants | 8 | |
| oxo-flow-enrichment | epigen/enrichment_analysis @ v3.0.1 | 77 | functional enrichment | 6 | |
| oxo-flow-unsupervised | epigen/unsupervised_analysis @ v4.0.2 | 67 | post-analysis statistics | 7 | |
| oxo-flow-genome-tracks | epigen/genome_tracks @ v2.0.5 | 57 | genome-browser tracks | 6 | |
| oxo-flow-mixscape | epigen/mixscape_seurat @ v2.0.3 | 56 | CRISPR perturbation | 7 | |
| oxo-flow-bgcflow | NBChub/bgcflow @ v1.1.2 | 55 | biosynthetic gene clusters | 6 | |

† Estimated rule count of the default main path. ✓ = fidelity verification agent assigned.

## Notable non-selections (and why)

- **snakemake-workflows/dna-seq-gatk-variant-calling** (267★) — the canonical GATK best-practices
  tutorial, but unmaintained since 2023-06; maintenance criterion (20%) disqualified it, and
  variant-calling is covered by sarek/snparcher/varlociraptor.
- **Hoohm/dropSeqPipe** (149★) and **snakemake-workflows/single-cell-rna-seq** (107★) — stale
  (2023 / 2022); single-cell covered by scrnaseq.
- **maxplanck-ie/snakepipes** (407★) — actively maintained but a *collection* of ~20 pipelines,
  not one workflow; unsuitable as a single template repo.
- **snakemake/snakemake** (2847★) — the engine itself, not a workflow.
- **csoneson/ARMOR** (168★) — RNA-seq preprocessing is covered by both rnaseq ports.

## Domain coverage

bulk RNA-seq (rnaseq, rnaseq-star-deseq2) · single-cell (scrnaseq) · WGS/WES (sarek) ·
metagenomics + amplicon (mag, ampliseq) · epigenetics ChIP/ATAC/methyl (chipseq, atacseq,
methylseq) · viral (viralrecon) · long-read (nanoseq) · ancient DNA (eager) · variant calling
non-model/SV (snparcher, varlociraptor) · microbial natural products (bgcflow) · CRISPR
perturbation (mixscape) · post-analysis (enrichment, unsupervised, genome-tracks) ·
fetch/QC (fetchngs).

**Known gap:** proteomics — the only strong candidate (nf-core/proteinfold) has a GPU-heavy
few-rule default path with poor portability value; left for a future round.

## Chair review notes

1. All 20 sources are MIT-licensed, none archived, every one pushed within ~13 months of the
   selection date.
2. All tags/commit SHAs in `pipeline-specs.json` were fetched live from the GitHub API at
   selection time — no invented versions.
3. The snakemake half draws 4/8 entries from the maintained MrBiomics (epigen) suite: provenance
   is concentrated, but the four cover four distinct domains and each is catalog-listed and
   actively maintained. Accepted with this note.
4. The 6 highest-complexity ports (rnaseq, sarek, viralrecon, eager, mag, chipseq) carry a
   mandatory fidelity-verification stage against upstream source.
