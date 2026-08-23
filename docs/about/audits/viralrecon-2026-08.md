# viralrecon completeness audit (2026-08-21)

Upstream: nf-core/viralrecon @ 3.0.0 · Port: `oxo-flow-viralrecon`
(live-verified).

## Mode matrix (upstream — one workflow, platform × protocol branches)

| platform | protocol | chain |
|---|---|---|
| illumina | amplicon | fastp → kraken2 dehost → bowtie2 → ivar trim → markdup/picard → mosdepth → ivar/bcftools variants → freyja → ivar/bcftools consensus → quast/pangolin/nextclade → cutadapt primer trim → spades/unicycler/minia assembly → BLAST/quast/abacas/plasmidid → snpeff/snpsift → multiqc |
| illumina | metagenomic (SISPA) | same minus primer steps; forces bcftools variant_caller |
| nanopore | amplicon (ARTIC always) | pycoqc → artic guppyplex → kraken2 → nanoplot → artic minion (Clair3) → vcfuniq → filter_bam → mosdepth → pangolin/nextclade/freyja/quast → snpeff/snpsift → multiqc |

## Gap tiers vs the port

**P0**: nanopore platform (entire ARTIC chain — guppyplex/minion/vcfuniq
plus its QC set); illumina metagenomic mode; bcftools variant_caller +
consensus_caller chains (maskfasta consensus path); unicycler + minia
assemblers; freyja demix/boot chain; nextclade + pangolin + plasmidid +
abacas + bandage extras; cutadapt primer-trim path; additional_annotation
subworkflow.

**P1**: none — all tools free (snpEff DB built locally from fasta+gff,
no GISAID, no paid DBs; ARTIC/pangolin-data/Nextstrain datasets free).

**P2**: the ~30 skip flags, caller choices, spades_mode enum (9 values),
kraken2 host-filter toggles, min_reads thresholds, save_* gates,
primer_set/version matrix, artic_minion_model, sequencing_summary.

Network deps (all with explicit local-db escape hatches): NCBI taxonomy
for kraken2 build, Nextstrain datasets, pangolin-data GitHub, freyja
UShER barcodes, nf-core genomes.config, S3 kraken2_human test DB.

Footgun (do not port): profile `test_full_sispa` references a missing
conf file — errors at startup.

## Verdict

Two-platform surface; the ported illumina-amplicon default leaves the
nanopore platform and the bcftools caller chains as the main P0.

## Re-verification (2026-08-23, batch 3)

Engine: latest main (post-v0.14.1) · Box: tx-ubuntu · Mode: real CLI
run, not dry-run.

**7+76 rules exit 0** (prep + main chain), zero failures at the latest
commit. The 27-env build (pangolin/nextclade/kraken2 heavy deps) was
the slow part (~2h); the run itself passed in one round with no fixes
needed.
