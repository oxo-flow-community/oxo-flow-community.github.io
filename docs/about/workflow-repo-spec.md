# Workflow repository specification

Every catalog repository must follow the same structure so the catalog,
the website and the live-testing harness stay consistent. The site
generator checks the essentials at build time (see
[`check_sem_texts` in scripts/regen-configs.py](../scripts/regen-configs.py));
this page is the contract.

## Repository layout

```
oxo-flow-<name>/
├── main.oxoflow          # entry point: [workflow] + [config] (+ includes)
├── modules/              # module fragments, one per stage (optional)
│   └── <stage>.oxoflow   #   includes carry `namespace = "<stage>"`
├── test/
│   └── fixtures/         # tiny synthetic data + sample sheets
├── metadata.json         # catalog truth — see schema below
├── README.md             # required sections — see below
├── LICENSE               # Apache-2.0 unless upstream dictates otherwise
├── NOTICE.md             # upstream attribution (every port)
└── .github/              # optional CI: validate + dry-run on PRs
```

### `main.oxoflow` rules

- Rule names are **snake_case**, no module prefix unless the rule lives in
  an included module file (then `namespace::rule` — the engine's namespaced
  form).
- Every rule carries a `description` — the *site Parameters table uses it
  verbatim*.
- **Parameters are documented in-place**: a `#` comment directly above
  `key = value` in `[config]` becomes that key's description on the site.
  No schema file to maintain.
- The default sample data ships as an **inline `[[sample_groups]]`** so a
  bare `oxo-flow run main.oxoflow` works out of the box (this is what the
  site's "Try it" panel relies on). Test files mirroring it live in
  `test/fixtures/`.

### `test/fixtures`

Tiny synthetic inputs (a few KB — never real datasets except small
probing stubs): `test/fixtures/samples.tsv`-style sample sheets, a
miniature reference, and the exact files the unit fixtures reference.
The path is what the site's "Try it" note points at.

## `metadata.json` schema

| Field | Required | Notes |
|---|---|---|
| `name` | ✅ | `oxo-flow-<name>`, must equal the repo name |
| `title` | ✅ | one-line human title |
| `description` | ✅ | 2–5 sentences: what it does, for which input |
| `origin` | ✅ | `port` \| `original` \| `curated` |
| `rating` | ✅ | `live-verified` \| `verified` \| `community` |
| `coverage` | — | `full-line` \| `default-path` (ports) |
| `engine` | ports only | `nextflow` \| `snakemake` (source engine); originals omit it |
| `source` | ports only | `{repo, url, tag, sha, license}` |
| `created` | ✅ | catalog date `YYYY-MM-DD` |
| `domain` | ✅ | one primary domain (see catalog list) |
| `tags` | ✅ | free-form searchable tags, kebab-case, lowercase |
| `tools` | ✅ | pinned tools (first 8 show on the site card) |
| `rule_count` | ✅ | engine `graph` node count of `main.oxoflow` |
| `scope` / `excluded` | ✅ | ported-in vs genuinely blocked upstream items |
| `installation` | ✅ | `{engine: "oxo-flow >= X.Y.Z", toolchain, requirements[]}` |
| `repo_url` | ✅ | `https://github.com/oxo-flow-community/<name>` |
| `license` | ✅ | workflow license |
| `upstream_license` | — | source license (ports) |

**Consistency rules**

1. `title`/`domain`/`tags` on the site cards come from `metadata.json`.
   Update the file, re-run `scripts/regen-configs.py` + `scripts/generate.py`
   in the site repo, commit the generated pages in the same PR.
2. `rule_count` must equal `oxo-flow graph`'s node count of the staged
   `main.oxoflow` — the site's regen script re-derives DAGs from the staged
   copy of the repo, so a drift means the staged copy is stale.
3. Semantic overviews (`site-work/scripts/semantic_maps/oxo-flow-<name>.md`)
   name only **real rules of the current workflow** — this is machine-gated
   (any unknown name fails regeneration). When rules change, update both the
   workflow and the overview in the same commit.

## `README.md` required sections

1. **What it does** (mirrors `metadata.json` description).
2. **Quick start** — `clone` → `oxo-flow validate` → `oxo-flow dry-run` →
   `oxo-flow run main.oxoflow`.
3. **Test data** — where `test/fixtures` sits; how to run the built-in
   sample group.
4. **Requirements** — engine version, toolchain (containers/conda/pixi),
   reference data, network, compute, disk.
5. **Fidelity** — the porting notes table (rule-by-rule mapping highlights,
   deviations, upstream version + sha).
6. **NOTICE** attribution to the upstream license holders.

## Adding or updating a workflow

1. Build or port the workflow in a fresh `oxo-flow-<name>` repository
   (start from an existing catalog repo — they are the reference layout).
2. Fill `metadata.json` completely; run the site's consistency checks
   locally (`scripts/regen-configs.py` against your staged copy).
3. Open the catalog PR: add the repo to
   `site-work/scripts/regen-configs.py`'s pipeline list (via
   `site-work/data/pipelines.json`), regenerate, commit.
4. Add the **Semantic overview** text (English, rule-name-verified) —
   see the paradigm files in `site-work/scripts/semantic_maps/`.
5. CI gate: `validate` + `dry-run` must pass; for `live-verified`, attach
   the live-test evidence in the repo (see
   [live-testing.md](live-testing.md)).
6. **Updates**: bump `metadata.json` (tag/sha, created, scope) and the
   README fidelity notes together; the semantic overview must be updated
   when rules change — the site gate refuses staged rule-name drift.
