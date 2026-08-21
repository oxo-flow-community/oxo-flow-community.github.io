# varlociraptor completeness audit (2026-08-21)

Upstream: snakemake-workflows/dna-seq-varlociraptor @ v6.10.0
(b65c3350) · Port: `oxo-flow-varlociraptor` (verified; full Tier A run
in progress on bioinfo-wsx).

## Mode matrix (upstream — config × sample-sheet driven)

| axis | options |
|---|---|
| entry points | rule all / only_alignment (BROKEN upstream) / benchmark / testcase |
| calling type | variants / fusions / fusions,variants (samples.tsv calling col) |
| datatype | dna (bwa/vg) / rna (STAR+arriba) |
| callers | freebayes / delly (both on → parallel chains) / arriba (fusions) |
| scenario | YTE-rendered per group (default scenario.yaml; per-group override via groups table scenario column) |
| alignment | bwa-mem (default) / vg giraffe pangenome (ref/pangenome/activate; hprc v1.1/v2.0) |
| reads | local fq / SRA auto-download; adapters; UMI branch; per-sample primer panels |
| scatter | calling=16 scatteritems + 4 gather points |
| downstream | tables (vembrane) / oncoprint / datavzrd reports (stratify) / MAF / mutational burden / mutational signatures / population DB update / CHM-eval benchmarking |

## Gap tiers vs the port

**P0**: RNA fusion calling (STAR+arriba+splitncigarreads, unannotated
FDR path); delly caller chain; UMI/consensus-reads branch; primer
trimming/panel mode; per-group scenario overrides; custom alignment
properties; benchmarking mode (CHM-eval); testcase generation;
mutational signatures + burden + population DB + MAF branches; SRA
read source; target_regions/off-target filtering.

**P1**: none license-wise (MIT; CADD/REVEL/DGIdb/COSMIC free with own
terms — DGIdb = live web API dependency).

**P2**: fdr-control modes (local/global smart/strict), retain-artifacts,
infer_genotypes, VEP plugin set (LoFtool/REVEL/CADD/SpliceAI/
AlphaMissense — CADD needs score download; SpliceAI/AlphaMissense
user-supplied), report stratification, tables options, scatter count.

Port deviations already documented in its README fidelity table
(scatter 16→1, single pre-rendered scenario, wrapper-utils→plain
scripts, gather_annotated_calls/filter_odds not ported — benchmarking-
only upstream) — the audit now re-labels those as P0 under the
full-line mandate (scatter = engine capability; multi-scenario
rendering = P0 porting work).

Upstream dead code: only_alignment unsatisfiable; get_haplotype_args/
get_count_group_kmers_input unused; vg2svg producer-less; tables
output keys superseded.

## Verdict

The live Tier A run covers the DNA-variants default path fully; the
full-line gap = fusions (RNA), delly, UMI/primers, scenario matrix,
and the downstream branch set.

## Live evidence (2026-08-22 — verdict #24, LIVE-PASS)

Full Tier A end-to-end on bioinfo-wsx (64c / 1.4TB, NFS /data): 88-rule
DAG completed with **exit 0, 0 failed** — `✓ 91 output files verified
(45.8GB total)` + report snapshot written. Engine v0.13.1 release
binary; reference data (Ensembl 111 genome/GTF/VEP cache+plugins,
REVEL, known-variants VCFs, 4.4GB pangenome gbz) relayed to the server
and pre-placed; every compute rule executed for real including
pangenome autoindex (45.8GB), freebayes candidate calling, BQSR,
varlociraptor estimate/call/FDR, VEP + dbNSFP annotation, oncoprint,
and both datavzrd reports.

Final run: 26 rules executed fresh + 62 checkpoint-verified (rule
fingerprints and input manifests confirmed unchanged since their last
successful run), 0 failed. Fix chain of the campaign: 16 commits
`cd54fcb..71bf729` — fixture window re-selection (repeat-rich →
uniquely-mapping, MAPQ 60), conda-forge version removals re-pinned
(vega-lite-cli/datavzrd), vg env + samtools, freebayes 96→48 threads +
region-list sed repair (delimiters, 3-col BED, empty-region guard),
oncoprint empty-call guards, yte SimpleNamespace + recursive
frame-encoded dict rebuild, plus server-side conda cache/zombie
recovery. New failure classes archived in the live-test failure
catalog; engine-side notes: none new (resource fast-fail behavior is
by design — over-capacity requests clamp).
