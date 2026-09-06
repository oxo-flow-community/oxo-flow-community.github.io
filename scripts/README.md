# Site regeneration scripts

Every pipeline artifact on the site is **generated**, never hand-edited
(single-source rule): the staged workflow repos under `../staging` are the
source of truth, and these scripts derive the site's data and figures from
them.

## The update loop (site issue #16)

Whenever a staged workflow changes (a port PR lands), run:

```bash
OXO_FLOW=/path/to/oxo-flow ./scripts/regen-all.sh
```

which in turn runs:

1. **`regen-configs.py`** — walks every staged workflow:
   - `data/configs.json`: per-pipeline parameters with descriptions
     (comment-derived via `oxo-flow info --json`), defaults, and the rules
     that read each key (`used_by`);
   - `docs/assets/dag/<name>.svg`: the workflow graph, exported with
     `oxo-flow graph -f metro` and rendered with nf-metro through the
     **render ladder** in `metro_tiers.py`.
2. **`generate.py`** — regenerates `docs/pipelines/<name>.md` (parameters
   tables, fidelity sections, figure captions) and `pipelines-data.js`
   from `configs.json` + the staged repos' `metadata.json`.

Commit scripts and generated files together; the CI validates that the
committed pages are drift-free.

## The render ladder (`metro_tiers.py`)

nf-metro 1.1.0 renders clean transit maps but aborts on dense graphs with
strict routing invariants. The ladder walks increasingly coarse,
structurally-safe representations of **the same engine export** — no
per-pipeline data, no hand-authored maps:

1. `rule-sections` — rule-level with module sections (engine canonical export)
2. `rule-flat` — rule-level without sections
3. `module-stage` — one station per (module, stage)
4. `module` — one station per module, the engine's native
   `--granularity module` export (guaranteed fallback: renders for every
   workflow)

Tiers are tried in order; the first that renders **and** clears the
landscape gate (aspect ≥ 1.15) wins; rule-level tiers are skipped past 80
stations. The chosen tier is recorded in `configs.json` so pages can label
each map (rule-level vs overview).

## Requirements

- `oxo-flow` ≥ 0.17.3 (needs `graph --granularity module`)
- nf-metro 1.1.0 in the repo-local `.regen-venv` (created on first run)
