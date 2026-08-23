# bgcflow completeness audit (2026-08-21)

Upstream: NBChub/bgcflow @ v1.1.2 · Port: `oxo-flow-bgcflow` (live-verified).

**Seven runnable Snakefiles** — the most entry-point-rich upstream of
the batch (plus a broken Report mode):

| snakefile | what it runs |
|---|---|
| main Snakefile | prokka annotation backbone + gtdb meta + mibig table + ~20 toggle pipelines (eggnog, mash, fastani, automlst, roary, bigslice, checkm, gtdbtk, antismash, arts, deeptfactor, cblaster×2, bigscape, gecco, amrfinderplus, seqfu) |
| BGC | BGC-id-driven selection + bigslice/bigscape/clinker/interproscan/mmseqs2/getphylo/automlst |
| Database | dbt+DuckDB warehouse builder (requires main outputs; dbt repo clone; cargo asdb-taxa) |
| Metabase | metabase jar + duckdb plugin + interactive server (hardcoded admin creds!) |
| Alleleome | hidden entry (not in wrapper list): roary → alleleome core-gene fasta |
| lsabgc | lsaBGC autoanalyze on main intermediates (Kofam OFF by default) |
| ppanggolin | 2× 15-rule ppanggolin ladders (genome + roary-based) |

## Gap tiers vs the port

**P0**: the other 6 snakefiles (BGC/Database/Alleleome/lsabgc/
ppanggolin — Metabase = P2 infra with a hardcoded-credentials
footgun); the ~15 non-ported pipelines in the main toggle set
(bigslice/query-bigslice/bigscape/clinker/interproscan/mmseqs2/
arts/deeptfactor×2/cblaster×2/gecco/amrfinderplus/roary/eggnog/
automlst/seqfu/mash/fastani); sample-source branches (ncbi/patric/
gbk-convert).

**P1**: KEGG Kofam data (license; OFF by default upstream — keep off +
document); InterProScan EULA (implicit in direct download).

**P2**: antismash v6/v7 switch, gtdbtk release/ani_screen, use_gtdb_api
offline mode, BGCFLOW_ANTISMASH_MODE env toggle, resources_path
symlinks.

Data gates (all free, some huge): GTDB API/metadata (~60-90GB for
gtdbtk), MIBiG JSON, antiSMASH DBs, eggNOG bacteria.dmnd, CheckM data,
BiG-SCAPE+Pfam-A, BiG-FAM (query-bigslice), ARTS refs, AMRFinderPlus DB,
lsaBGC annotation DBs, NCBI/PATRIC downloads, GECCO models, DeepTFactor
clone.

Upstream dead code (do not port): Report mode broken (dir not
snakefile); report.smk included by nothing; mlst/refseq_masher rules
unreachable via rule all; antismash-db-duckdb only in Database mode.

## Verdict

Largest multi-entry surface — 7 snakefiles × ~20 pipelines. The ported
default main path (prokka + antismash + gtdb) leaves the BGC-selection
mode and the warehouse/reporting stack as the biggest P0 blocks.

## Re-verification (2026-08-23, 9-mini queue 1/9)

Engine: latest main (post-v0.14.1) · Box: bioinfo-wsx · Mode: real CLI
run, not dry-run · `-j 4 --keep-going`.

**14 succeeded, 13 skipped, 0 failed, exit 0**, one round, zero repo
fixes. Coverage chain: copy_custom_fasta → gtdb_prep (bac120 metadata
pre-staged via Mac relay) → prokka ×2 → format_gbk ×2 →
get_mibig_table → **antismash 7 full DB set (pfam 293MB +
clusterblast 751MB + 8 more components, pre-staged and
sha256-accepted)** → antismash_genomes S1+S2 → overview/copy/summary
→ csv_to_parquet. All 13 skips are checkpoint reuse.
