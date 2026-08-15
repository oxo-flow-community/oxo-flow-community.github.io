# Contributing

The catalog grows one workflow at a time — a port, an original design, or a
listing of a repository you already maintain.

## 1. Build the workflow

- **Porting an existing pipeline** (Nextflow or Snakemake): follow the
  [porting guide](porting.md) — mapping tables, version-pinning policy, repo
  layout, README, licensing.
- **Writing an original workflow**: same repo layout, plus your own design
  decisions. The layout is:

  ```
  workflow/            the .oxoflow file(s)
  config/              optional configuration profiles
  test/fixtures/       minimal inputs that make dry-run meaningful
  test/run.sh          validate + lint + dry-run, exit 0 on success
  README.md            what it does, Installation, usage, scope
  LICENSE              Apache-2.0 (or your choice for your own repo)
  NOTICE.md            required for ports — upstream attribution
  .github/workflows/   CI: install oxo-flow, run test/run.sh
  metadata.json        the registry entry (schema in data/pipelines.json)
  ```

## 2. Get it listed

- **In the org:** if you want the community team to co-maintain it, open a
  repository under
  [oxo-flow-community](https://github.com/oxo-flow-community) and ask for a
  review in the site repository.
- **Your own repo:** add a registry entry to `data/pipelines.json` in the
  [site repository](https://github.com/oxo-flow-community/oxo-flow-community.github.io)
  and open a pull request. The catalog links to your repository — nothing
  moves.

See [Curation &amp; ratings](curation.md) for the classification scheme and
what ★ Verified requires.
