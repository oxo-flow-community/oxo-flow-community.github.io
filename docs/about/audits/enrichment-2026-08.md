# enrichment_analysis completeness audit (2026-08-21)

Upstream: epigen/enrichment_analysis @ v3.0.1 · Port: `oxo-flow-enrichment`
(live-verified).

Single-Snakefile module, 15 rules, 6 analysis tools. Input-type-driven
branching: `.bed` → region branch (LOLA/GREAT/pycisTarget + derived
ORA/RcisTarget on GREAT-associated genes); `.txt` → gene branch
(ORA_GSEApy/RcisTarget); `.csv` → preranked branch (preranked_GSEApy).
Tool branches toggle by database-dict config keys (empty path = skip).

## Mode matrix (upstream)

| tool | db config key | inputs |
|---|---|---|
| LOLA | lola_databases | region (.bed) |
| GREAT + region→gene association | local_databases | region |
| pycisTarget | pycistarget_parameters.databases | region |
| ORA_GSEApy | local_databases | gene + region-derived |
| RcisTarget | rcistarget_parameters.databases | gene + region-derived |
| preranked_GSEApy | local_databases | ranked (.csv) |
| summaries/plots | — | per group×tool×db |

No differential-enrichment or multi-factor mode upstream.

## Gap tiers vs the port

**P0**: pycisTarget (HDF5 + process-results chain); RcisTarget; LOLA
(databio regionDB); GREAT region→gene association step (feeds the
derived ORA/RcisTarget paths); preranked branch. Whichever of the 6
tools the port omitted = P0.

**P1**: none — all DBs user-supplied, no paid services. License-adjacent
notes: MSigDB/Enrichr/cisTarget terms (free for academic use).

**P2**: great_parameters (mode/basal/extension/map_associated_regions),
adjp thresholds per tool, top_n, caps, cluster_summary, top_terms_n,
pycisTarget/RcisTarget hyperparams, genome→org.db selection.

External gates: rGREAT runtime download (GREAT server TSS/gap
annotation), LOLA regionDB download, conda/container provisioning.

Upstream fail-open design (CAUTION for port): empty/erroring analyses
write empty files + exit 0 (pycisTarget/RcisTarget soft-fail) — the
port's live-verified claim must not rely on non-empty outputs alone.
Known upstream bug: "mm11" typo in species mapping → mm10 pycisTarget
soft-fails; genome key unvalidated.

## Verdict

Mid-size: 6 tools × 3 input types. Port scope check = which tool
branches exist in the port (metadata scope 38 rules after
normalization suggests partial tool coverage).

## Re-verification (2026-08-23, 9-mini queue 7/9)

Engine: latest main (post-v0.14.1) · Box: bioinfo-wsx · Mode: real CLI
run, not dry-run · `-j 4 --keep-going`.

**First run 43/12/2 + resume 6/51/0 — full chain green.** Coverage
(real): prepare_databases (Azimuth + Reactome real downloads) →
GSEApy preranked ×2 → **GREAT (region_gene_association + Reactome
Bcell/Ery + ATAC aggregate)** → **LOLA (Bcell/Ery + plot +
visualize, Fisher scores computed)** → summary.

**Real repo fix (c7f194c)**: the LOLA fixture index lacked the
`filename` header — LOLA ≥1.22's loadRegionDB evaluates that column
by name and errored with "object 'filename' not found". Adding the
header row fixed it. Box-side only: the region env's 7 bioconda data
packages post-link downloads were proxy-truncated; solved by Mac
relay + rewriting the pkgs-cache dataURLs.json to `file://` (patch
the pkgs cache, not the env dir — rebuilds wipe env-dir patches).
