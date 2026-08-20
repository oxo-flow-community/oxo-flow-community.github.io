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
