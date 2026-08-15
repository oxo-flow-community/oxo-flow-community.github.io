# Curation &amp; ratings

The catalog is more than a list of repositories: every entry is classified,
rated, and documented against the same criteria, so "listed here" means
something you can rely on.

## Classification

**By domain.** Each workflow carries one primary domain (bulk RNA-seq,
single-cell, variant calling, metagenomics, epigenetics, …) plus free-form
tags. Domains and tags are searchable on the [catalog page](../pipelines/).

**By origin.** Where a workflow came from, shown on every card:

| Origin | Meaning |
|---|---|
| ⇄ Official port | A migration of an established Nextflow or Snakemake pipeline, produced and maintained by the community team. Tool versions and commands are pinned to the source; a per-rule fidelity table documents the mapping. |
| ✦ Original | A workflow designed for oxo-flow from the start, by the community team or by its author. |
| ♺ Community listing | A workflow hosted in any public GitHub repository, included in the catalog via pull request. The catalog links to the repository — it never copies or forks it. |

## Ratings

| Rating | Badge | Requirements |
|---|---|---|
| **Verified** | ★ | Official or community-team maintained; every rule pinned to a tool version; `validate` and `dry-run` green in CI; ports additionally carry a complete fidelity table and have passed rule-by-rule review against the source. |
| **Community** | ☆ | Public repository; the workflow validates with the released oxo-flow engine; installation and usage documented; maintained by its author. |

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
