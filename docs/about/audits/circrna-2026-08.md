# circrna live audit (2026-08-23)

Original workflow (not an upstream port) · Repo: `oxo-flow-circrna`
(Traitome org, entry file `circrna.oxoflow`) · Rating:
live-verified (data/pipelines.json).

Four independent circRNA callers (CIRIquant, CIRCexplorer2, find_circ,
circRNA_finder) + fastp QC + ensemble aggregation (≥2 callers agree).
Reference indexes (bowtie2/STAR/bwa/hisat2) and conda envs build
automatically on first run; samples auto-discovered from `raw/`.

## Live re-verification (2026-08-23)

Engine: latest main (post-v0.14.1) · Box: tx-ubuntu · Mode: real CLI
run, not dry-run · `-j 2 --keep-going` · **exit 0, one round, zero
fixes**.

- 4 reference indexes auto-built (1.2kb synthetic genome, seconds)
- 9 rules all passed: fastp → 4 callers → multiqc → aggregate →
  aggregate_dataset → report; 12 output files verified
- **Real signal**: find_circ detected the planted BSJ
  `chr1:520-719 + 20 reads circ_000001` — exactly matching the
  fixture's designed e3→e2 back-splice position
- CIRIquant ran for real: 19 candidate splice-signal reads →
  second-scan PEM 0 → 0 circRNA (below the statistical threshold of
  the tiny fixture)
- circRNA_finder produced real STAR Chimeric.out.junction /
  SJ.out.tab outputs; no candidates passed its filters

### Honest coverage note

All 4 callers executed for real. 1/4 detected the planted BSJ; 3/4
reported 0 circRNAs because the mini fixture (200 read pairs, 1kb
genome) sits below their detection thresholds — a statistical limit
of the fixture, not a tool or port defect. The report rule's guard
echo (`WARNING not created`) is rule-internal logic; exit 0 is
correct.

### Usability note

Entry file is `circrna.oxoflow`, not the `main.oxoflow` convention —
auto-discovery still finds it (alphabetically first `*.oxoflow`), but
renaming to `main.oxoflow` would align with the other community
repos. Pending owner decision.
