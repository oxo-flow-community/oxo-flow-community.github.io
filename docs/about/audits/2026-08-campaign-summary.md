# 24h full-campaign summary (2026-08-23)

One-round live re-verification of **all 24 workflow repos** against the
latest engine main (post-v0.14.1) on tx-ubuntu + bioinfo-wsx. Every
verdict below is a REAL CLI run, not a dry-run — checkpoints were
cleared to force real execution (see the checkpoint no-op lesson in
the failure catalog).

## The matrix (24/24)

| repo | coverage this round | verdict | evidence |
|---|---|---|---|
| ampliseq | DADA2 full chain + SBDI-GTDB taxonomy | 16/0/14 exit 0 | site 1bfad3c |
| atacseq | default bwa arm full chain | 29/0 exit 0 | site 85b6d1f |
| auto-sra-rnaseq-pipeline | 4-sample 2v2 real SRA, STAR full-GRCh38 + DESeq2 | exit 0 (mini21) | site 5f37dbd |
| bgcflow | prokka + antismash 7 full DB set + gtdb | 14/0/13 exit 0 | site 5d6d1bf |
| chipseq | bwa→macs3→FRiP→homer full chain | 143/0/11 exit 0 | site def8453 |
| circrna | 4 callers real; find_circ planted-BSJ hit | 9/0 exit 0 | site 39ee9f3 |
| clindet | RNA port 26 rules (arriba BSJ detected) | 26 real/0 failed | site f1aae9c |
| eager | nfcore/eager:2.5.3 single-container chain | 22/0/6 exit 0 | site f67f54a |
| enrichment | GSEApy + GREAT + LOLA (Fisher real) | 43/12/2 + 6/51/0 | site 87b5fdb |
| fetchngs | 3 real ENA ids, md5-guard verified | 7/0/9 exit 0 | site fe8a5c9 |
| genome-tracks | full-line-sc: sc + bulk + ucsc_hub | exit 0 (5-fix chain) | site f458708 + PR #2 |
| mag | 295 rules; 5 binners + QUAST/BUSCO + ALE | 224/32/4 → resume green | site 4fcde83 |
| methylseq | bismark default chain | 19/0/3 exit 0 | site 2fe1170 |
| mixscape | full chain | 9/9 exit 0 | site 9d5b90e |
| nanoseq | minimap2+medaka default chain | 29/0 exit 0 | site 0da8165 |
| rnaseq | STAR + tximport + DESeq2 (heavy) | 68 real/0 failed | site 40ec98d |
| rnaseq-star-deseq2 | STAR+GeneCounts + live biomaRt 3-step | 56/0/48 exit 0 | site 31212a0 |
| sarek | GATK haplotypecaller + vep germline | 165/0 + 1/38/0 | site 97f25b2 |
| scrnaseq | cellranger S1+S2 real + cellbender | 22/0/10 exit 0 | site 6466481 |
| snparcher | gatk intervals + fastq default | 21/21 exit 0 | site f458708 |
| tcasia | rmats + spladder + MAJIQ/voila | 24/0/10 exit 0 | site 31f0d2e |
| unsupervised | full chain | 27/27 exit 0 | site 9d5b90e |
| varlociraptor | vg giraffe pangenome chain | 17 + 38/50/0 | site f9f7045 |
| viralrecon | illumina-amplicon chain, 27-env build | 7+76 exit 0 | site 6d3ac37 |

## Repo fixes pushed this round

| repo | commit | fix |
|---|---|---|
| genome-tracks | 2ae877e..fdfeec6 | sc-branch runtime fixes ×5 (index fixtures, setuptools<81, header-only BAM, symlink idempotence, plot gating) |
| genome-tracks | 80adcbc | test instance list follows the mini fixture (PR #2 CI) |
| mag | 2554bde | build_ale.sh GCC≥14 legacy-C compatibility |
| fetchngs | 0a118df | id.txt concurrency race (shared workdir) |
| fetchngs | 9a9f09f | wget -c corruption → md5-first idempotence guard |
| enrichment | c7f194c | LOLA fixture index `filename` header |
| varlociraptor | 6fda195 | delly download ghfast.top mirror fallback |

## Engine-side work

Merged: #152 (CLI↔docs consistency ×6), #154 (macOS .app icon + launcher +
ad-hoc codesign), #155 (Linux deb/rpm/AppImage menu entry + icon), #156
(env-cache hit re-verifies on disk; vanished envs invalidate + rebuild).
Filed: #159 (env identity — same-name cross-workflow collisions), #162
(singularity URI→IMG %3A naming).

## Web lane

#149 (dev-mode role derivation fix + serve.md correction) + #151
(deployment + 3-role simulation matrix, 450 lines: RBAC, ownership
isolation, SQLite restart persistence, base-path). Local gate green,
both merged.

## Methodology lessons (in the failure catalog)

Checkpoint no-op trap (force real runs), honest coverage labeling
(chr21-subset reference, gtdbtk=false, DRAFT constraints), China-network
DB pre-staging pattern (sha256-accepted), conda post-link proxy
pathologies (two endgames), docker storage exhaustion, env-cache family
(three dimensions).

## Resource evidence (honest: peak RSS not recorded — the engine does
not emit per-rule peak RSS; wall-clock is run start→end)

tx-ubuntu (4 vCPU / 3.7GB, clamp constant): nanoseq 13:55, circrna
3:24, chipseq 31:45 (docker --memory 3723M + 1881 clamps), methylseq
16:00 (bismark 12→4 threads), rnaseq-star-deseq2 3:41 (+biomart env
~1.5h proxy battle), eager 0:56, scrna-seq 11:14 (cellranger 72GB
declared → clamped, runs anyway), sarek ~40min, rnaseq ~1.1h,
ampliseq 2:36 (+dada2 env ~2h). bioinfo-wsx (64c/1.4TB, ZERO clamps):
bgcflow ~1.4h (DB staging dominated), mag ~2h (26 envs ~50min),
tcasia ~30min (rmats 3s + spladder 339s parallel), enrichment ~1.8h
(env battle), varlociraptor ~15min, auto-sra mini21 (STAR ~6min/sample,
full-index build 48 threads ~32min — the heaviest scheduling point).

Unified observations: (1) tx-ubuntu clamp + "run alone" serialization
is CORRECT degradation, cost = wall-clock; (2) bioinfo-wsx zero clamps
but network is the bottleneck — env/DB downloads are 40-60% of total
wall time; (3) conservative -j (2 / 4-8) was already throughput-
saturated by env+network constraints. Engine candidate (post-campaign):
per-rule peak RSS in the run report.
