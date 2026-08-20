# auto-sra-rnaseq completeness audit (2026-08-21)

Upstream: xuzhougeng/auto_sra_rnaseq_pipeline @ main — **pin weakness**:
the port pinned `main` without a SHA; audited at commit `923b9e986`
(2025-09-19). Repo has NO release tags and NO LICENSE file (reuse terms
undefined — flag to the author). Port: `oxo-flow-auto-sra-rnaseq-pipeline`
(verified; live run in progress on tx-ubuntu).

## Mode matrix (upstream)

| mode | entry | notes |
|---|---|---|
| batch driver | run.py (loop over metadata *.txt; pre-check SRA files; temp config; --unlock + run; finished/failed dirs; bark/feishu/QQ-mail notifications) | recommended upstream path |
| single dataset | snakemake -s Snakefile | 12 rules + hooks |
| ENCODE schema | Snakefile_ENCODE | 7 rules, pre-downloaded fastq, paired-only in practice |
| slurm overlay | --executor slurm + profile | set-threads per rule |
| standalone | scripts/update_json.py, utilize.py | ORPHANS (legacy GPSAdb tooling) |
| docker | Docker/Dockerfile | TUNA-mirrored env build only |

Branches: single/paired per-sample (metadata `paired` col); multi-SRR
comma-merge (paired module honors `srr_separator`, single module
hardcodes `,` — inconsistency); DESeq2 design HARDCODED
(~group, treat vs control, ashr) — not config-driven.

## Gap tiers vs the port

**P0**: ENCODE-schema Snakefile; single-end branch (data_conversion_
single/merge_data/data_clean_single); multi-SRR merging; batch driver
semantics (finished/failed bookkeeping, --unlock pre-pass, notifications).

**P1**: none (no licenses, pre-downloaded SRA only) — but upstream has
NO LICENSE file: port's NOTICE must state it.

**P2**: srr_separator, thread counts, mail/bark/feishu toggles (bark is
a stub upstream — never sends), slurm profile (data_downloader entry
is dead).

Upstream dead/drift (do not port): pigz_threads dead (merges use cat);
use_download dead; docs document nonexistent preload_star_index/
cleanup_star_index rules; save() into .Rds-named file (intended quirk);
KeyError risk on hand-rolled configs.

Gates: SRA archives pre-staged by the user (never downloaded in-pipeline),
STAR index + GTF user-built, GRCh38 hardcoding (effectiveGenomeSize,
ENSG filter), R 4.3.2 + DESeq2/data.table/ashr.

## Verdict

Small surface — 2 schema modes + single/paired branches. The ported
paired-SRA path leaves ENCODE mode + single-end + the batch driver as
the full-line targets.
