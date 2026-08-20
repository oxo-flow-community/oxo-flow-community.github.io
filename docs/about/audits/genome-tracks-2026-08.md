# genome-tracks completeness audit (2026-08-21)

Upstream: epigen/genome_tracks @ v2.0.5 · Port: `oxo-flow-genome-tracks`
(live-verified).

Small snakemake workflow (12 rules): merge BAMs per group → bigWig →
per-gene/region tracks (gtracks/pyGenomeTracks) → UCSC hub + 4 export
rules.

## Mode matrix (upstream)

| mode | trigger |
|---|---|
| bulk-only | all group values are plain strings |
| single-cell branch | group value ends with `.tsv` (sinto split by barcode → merge per label) |
| mixed | both conditions coexist |
| gene vs region plot | per gene_list row (chrN:start-end regex vs BED lookup + base_buffer + isoform count) |
| igv_report | deactivated in rule all (selectable target only) |
| exports | always (3 env yamls + config + annotation + gene_list) |

## Gap tiers vs the port

**P0**: single-cell branch (sinto split + label-driven merge); igv_report
rule (exists upstream but deactivated — port decision: include or
document as non-default); mixed bulk+sc mode.

**P1**: none — MIT, no paid data, no API keys. Distribution note:
pyGenomeTracks GPL-3.0, sinto/gtracks licenses undeclared in-repo
(verify before redistribution).

**P2**: file_type, track_colors, ymax, base_buffer, x_axis, width,
bamCoverage_parameters, mem/threads, hub identity fields, QC mode
(unique groups = rename-only merge).

Silent-failure gotcha (upstream): genes not found in the genome BED are
silently dropped (genes_not_found.csv notice) — a stale gene_list yields
a successful run with missing tracks.

External: UCSC hub needs a user web server to serve (post-step); UCSC
recommended for the 12-col BED; IGV Desktop to view.

## Verdict

Near-complete port surface — the only structural P0 is the sc branch +
igv_report; everything else is config knobs.
