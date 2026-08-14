# Contributing

The catalog grows one faithful port at a time. To add workflow #21:

1. **Pick a source pipeline** (Nextflow or Snakemake) that is widely used and
   actively maintained by its community.
2. **Follow the [porting guide](porting.md)** — it is the executable spec:
   engine mapping tables, version-pinning policy, repo layout, CI, README,
   NOTICE and licensing conventions.
3. **Create a repo** `oxo-flow-<name>` under
   [oxo-flow-community](https://github.com/oxo-flow-community) with the standard
   layout (`workflow/`, `config/`, `test/`, `README.md`, `LICENSE`, `NOTICE.md`,
   `.github/workflows/ci.yml`, `metadata.json`) and green `validate` + `dry-run`
   in CI.
4. **Add its metadata** to `data/pipelines.json` in the
   [site repository](https://github.com/oxo-flow-community/oxo-flow-community.github.io)
   and re-run `scripts/generate.py` to refresh the catalog pages.
5. **Open a pull request** to publish the entry.

## Selection criteria

New entries are evaluated with the same pre-registered criteria as the first
twenty: usage & adoption (40%), maintenance health (20%), portability (25%),
domain diversity (15%). See the full [selection report](selection.md).
