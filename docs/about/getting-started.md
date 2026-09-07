# Get started — run your first workflow in 10 minutes

The catalog is **to be used, not just read**: every workflow page ships real
commands, a live semantic walkthrough, and parameters you can copy. This
page walks one full round trip — install the engine, pick a workflow,
preview the plan, run it, read the report.

## 1. Install the engine

Pick one:

```bash
# Binary (fastest): grab the latest release for your platform
#   https://github.com/Traitome/oxo-flow/releases

# Or via Cargo
cargo install oxo-flow-cli

# Or via Conda
conda install -c bioconda oxo-flow-cli
```

Check it:

```bash
oxo-flow --version
oxo-flow --help
```

## 2. Pick a workflow — and understand it first

Every card's **Semantic overview** on the workflow page tells you what the
pipeline does *before* you run it, in plain language — each step named with
its real rule. Start with **RNA-seq: STAR alignment, DESeq2 differential
expression and QC** ([oxo-flow-rnaseq-star-deseq2](../pipelines/oxo-flow-rnaseq-star-deseq2/)):
a full RNA-seq differential-expression pipeline with built-in test data and
a live-tested rating.

## 3. Preview — or run straight from GitHub

You can skip cloning entirely — the engine fetches the repo itself:

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-rnaseq-star-deseq2
```

It checks the repo out under `.oxo-flow/repos/<name>` and keeps outputs in
your current directory. When you want to inspect first, clone for real and
preview:

```bash
git clone https://github.com/oxo-flow-community/oxo-flow-rnaseq-star-deseq2.git
cd oxo-flow-rnaseq-star-deseq2
```

**Never run blind**: preview the exact plan first — rules, samples,
instances, resources:

```bash
oxo-flow validate main.oxoflow
oxo-flow dry-run main.oxoflow
```

The workflow ships a built-in sample group (its `[[sample_groups]]`), so the
plan is fully materialized without extra input files.

## 4. Run

```bash
oxo-flow run main.oxoflow
```

The executor prints every step as it goes; tracing goes to stderr, so the
terminal stays clean. Wildcards like `{sample}` expand per sample, instances
run with environment-pinned tools, and a checkpoint lets a failed run resume
with `--resume`.

## 5. Read the results

- `results/` — count matrices, DESeq2 tables, QC reports (see the workflow's
  README for the layout).
- `oxo-flow status` / `oxo-flow inspect <run-dir>` — what ran, what awaits
  a retry, resource usage.

## Where to go next

- [Pick the right workflow](selection.md) — a decision guide by domain.
- [Curation and ratings](curation.md) — what ✔ live-tested, ★ verified and
  ☆ community actually guarantee.
- [Port a pipeline yourself](porting.md) — from a source Nextflow/Snakemake
  workflow to a catalog entry.
