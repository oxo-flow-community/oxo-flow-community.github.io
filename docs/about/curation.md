# Curation &amp; ratings

The catalog is more than a list of repositories: every entry is classified,
rated, and documented against the same criteria, so "listed here" means
something you can rely on.

## Classification

**By domain.** Each workflow carries one primary domain (bulk RNA-seq,
single-cell, variant calling, metagenomics, epigenetics, …) plus free-form
tags. Domains and tags are searchable on the [catalog page](../pipelines/index.md).

**By origin.** Where a workflow came from, shown on every card:

| Origin | Meaning |
|---|---|
| ⇄ Official port | A migration of an established Nextflow or Snakemake pipeline, produced and maintained by the community team. Tool versions and commands are pinned to the source; a per-rule fidelity table documents the mapping. |
| ✦ Original | A workflow designed for oxo-flow from the start, by the community team or by its author. |
| ♺ Community listing | A workflow hosted in any public GitHub repository, included in the catalog via pull request. The catalog links to the repository — it never copies or forks it. |

## Ratings

| Rating | Badge | Requirements |
|---|---|---|
| **Live-tested** | ✔ | Everything **Verified** requires, PLUS a real end-to-end execution on reference data with the released engine: exit 0, every rule completed, report snapshot written. Live evidence is the strongest proof a workflow actually runs. |
| **Verified** | ★ | Official or community-team maintained; every rule pinned to a tool version; `validate` and `dry-run` green in CI; ports additionally carry a complete fidelity table and have passed rule-by-rule review against the source. |
| **Community** | ☆ | Public repository; the workflow validates with the released oxo-flow engine; installation and usage documented; maintained by its author. |

The badge is an **evidence ladder**, not a quality judgement: `dry-run` proves
the graph and commands resolve, a live run proves the tools actually work
end-to-end. Live-test verdicts are tracked by the community test bench (tx
cluster); a workflow drops back to **Verified** when a material change
invalidates its last live evidence, until the next live run re-confirms it.
Verified status is re-checked when a workflow changes materially — CI runs on
every push, and the fidelity review is repeated for significant updates.

## Getting a workflow listed

The canonical registry is `data/pipelines.json` in the
[website repository](https://github.com/oxo-flow-community/oxo-flow-community.github.io).
To list a workflow that lives **in your own repository**:

1. Make sure it validates and dry-runs with the released oxo-flow engine and
   documents installation and usage in its README.
2. Add one registry entry with the workflow's metadata (see an existing entry
   for the schema — name, title, origin, domain, tags, tools, rule count,
   installation notes, repository URL, license).
3. Open a pull request to this repository. Entries are checked with
   `validate` + `dry-run` before they are merged.

Workflows the community team maintains directly live in the
[oxo-flow-community organization](https://github.com/oxo-flow-community)
under the same layout and criteria.

## Machine-derived content

Three parts of every workflow page are not hand-written — they are derived
from the workflow file itself, so they cannot drift from the code:

- **Parameters table.** Every run-notes page lists the workflow's `[config]`
  section: parameter, default value, the rules that use it, and — when the
  workflow comments the key — its *Description* taken verbatim from the
  `[config]` section's `#` comments (contiguous comment block above the key,
  or a trailing comment on the key line). A `—` in the *Used by* column means
  the key is defined but not wired into any rule — a documented knob kept for
  fidelity with the source pipeline. No schema file to maintain.
- **Workflow graph.** Each page embeds a metro-map figure rendered by the
  adaptive ladder in `scripts/metro_tiers.py` (site issue #16): the ladder
  walks rule-level (sectioned → flat) to the overview tiers
  (module-stage → engine-native module), picking the finest tier that
  nf-metro renders **and** stays readable at site card width — a
  publication-grade map for every pipeline, no per-pipeline curation.
  Wildcard `{sample}` instances expand at run time when sample data is
  discovered, so the static graph shows the structural DAG (the runtime
  view is `oxo-flow graph --expanded`).
- **Multi-workflow repositories.** One repo = one card, driven by the
  workflow's *primary entry* (`main.oxoflow` convention): the entry is a
  single interface whose module includes carry every omics flow (live:
  clindet — somatic + germline calling, tumor-only, CNV, WGS and the
  conditional RNA sub-workflow are `[[include]]` modules of `main.oxoflow`,
  not separate entry files). Only a genuinely separate entry — an
  alternative CLI entry shipped as its own artifact — is listed under
  `extra_workflows` with a label naming the entry file; split entry files
  that have been merged back into the primary entry are removed from the
  catalog together with their old cards.
- **Metadata cross-checks.** `rule_count`, tools, resources, and environments
  are derived the same way and diffed against the hand-maintained registry
  entry when a workflow is listed or reviewed.

The derived data is committed (`data/configs.json` plus
`docs/assets/dag/<name>.svg`) and regenerated locally (never in CI) with:

```bash
scripts/regen-configs.py    # staged clones → data/configs.json + DAG SVGs
                            # (needs an oxo-flow binary and nf-metro 1.1.0)
scripts/generate.py         # regenerates the run-notes pages (CI checks for drift)
```

Run both whenever a staged workflow changes and commit the result — site CI
never regenerates these artifacts itself (the catalog stays hermetic): PR
checks run the drift gate and `mkdocs build --strict`, and the deploy
workflow additionally spot-checks three representative repositories against
the release engine before publishing.

### Reader levels and how the maps serve them

The catalog adopts one reading model per figure group (site-wide), so the
"one point = one rule on one page, one point = one module on the next"
confusion never appears:

- **Bioinformatics newcomer** reads the FIRST line of a station label —
  the *analysis stage* ("Read Trimming", "Variant Calling") — and the
  colored lines as stage tracks; the module set on the second line is
  detail they can ignore.
- **Expert** reads the second line (module set: "Somatic · Germline ·
  WGS Callers") and the off-track stations (conditional or auxiliary
  inputs/exports), then opens "Rule-level detail (exact DAG)" for the
  full rule graph.
- **UI/design** keeps the figure area contract: no station label wider
  than two wrapped lines, the legend pinned to the card surface, and the
  primary figure always at module/module-stage granularity with
  rule-level figures behind a collapsed card.
