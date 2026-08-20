# oxo-flow Porting Playbook

**Porting Nextflow (nf-core DSL2) and Snakemake workflows to oxo-flow v0.12.0 TOML repositories.**

Version: 1.3 (2026-08-15)
Engine target: oxo-flow **0.12.0** (pin this; format features below are the 0.11.0+ surface)
Audience: ~20 parallel porting agents, each owning one workflow port.

v1.1 (TCASIA port, #24): `{log}` is metadata-only (never a shell
placeholder), TOML triple-quote escape semantics (§13.29), `validate
--as-include` E005 on main-file config (§13.30), directory outputs pass
output verification (§13.31), `-t` prefix targeting across include
namespaces (§13.32).

v1.2 (SRA port, #23): fan-out trigger fields (§2.3, §13.33), empty
`output` script rules (§13.34), template-name `depends_on` (§13.35),
dry-run `input ✗` semantics (§13.36), `pairs_pattern` three-wildcard
constraint (§2.4, §13.37), literal resource numbers + resource-group
syntax (§13.38), the per-sample-routing limitation (§13.39), no-license
upstream handling (§10, §13.40), and the `{sra}`-style custom-wildcard
pattern (§4.2).

v1.3 (2026-08-15): CI and install references now use the **stable latest
tarball** — `releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz`
(a byte-identical copy of the versioned CLI tarball, published by the
release pipeline since v0.12.0) — and the engine floor is **0.12.0**
(all 22 ports re-verified against the v0.12.0 release binary).

This is an execution spec. Every TOML snippet in this document was either
(a) taken verbatim from a canonical, CI-validated gallery workflow in the
oxo-flow source repo, or (b) written by the author and verified against the
real 0.11.0 binary on 2026-08-15 (marked `[V]` — verified). **Never invent
syntax.** When in doubt, copy from this document, run the verification
commands in §7.4, and if something does not pass, fix the TOML — do not
"fix" the expectation.

---

## 0. Environment facts (fixed, do not re-derive)

| Item | Value |
|---|---|
| Engine source repo | [github.com/Traitome/oxo-flow](https://github.com/Traitome/oxo-flow) — treat as a **READ-ONLY** reference; never commit to it from porting work. |
| Development binary | Any oxo-flow **≥ 0.12.0**. For development against the latest main: `cargo build -p oxo-flow-cli` and use `target/debug/oxo-flow` (referred to as `$OXO` below). |
| CI install | Release tarball `https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz` — **verified layout: the archive contains a single file `oxo-flow` at its root** (no directory prefix). Exact install steps in §8. |
| bioconda package | `oxo-flow-cli`, latest **0.10.2** — lags local 0.12.0. Mentioned in user-facing README only (`conda install -c bioconda oxo-flow-cli`); **never** used in CI. |
| License | oxo-flow is Apache-2.0 (`LICENSE` in the source repo: full Apache 2.0 text, `Copyright 2025 Traitome`, appendix notice). Ports are Apache-2.0, "Copyright (c) 2026 oxo-flow-community" (see §10, §11). |
| Scratch space | Any throwaway directory (e.g. `/tmp/pb-check/`) for verification runs. Never create files in the engine repo. |
| Docs (format authority) | In the engine repo: `docs/guide/src/reference/` (`workflow-format.md`, `wildcards.md`, `dag-engine.md`, `environment-system.md`, `execution-backends.md`) and `docs/guide/src/commands/{validate,dry-run,run,debug,lint}.md`. |
| Canonical verified TOML | In the engine repo: `examples/gallery/*.oxoflow` (16 files, CI-validated). The CLI embeds a mirrored copy (`crates/oxo-flow-cli/src/commands/project.rs` `EMBEDDED_GALLERY`, mirror in `crates/oxo-flow-cli/templates/`, drift-guarded by a unit test). Snippets below marked `[gallery]` are verbatim from these files. |

---

## 1. Purpose & audience

Each porting agent receives one upstream workflow (nf-core DSL2 Nextflow
pipeline, or Snakemake pipeline) and produces one self-contained oxo-flow
repository that:

1. Replicates the upstream **full line** — every user-selectable
   sub-workflow and branch (WGS/WES/RNA modes, fusion callers,
   single-sample variants, ...), not just the default-parameters main
   path — same tools, same versions, same command logic (flags, file
   naming), same outputs — in a single `.oxoflow` TOML file (or one main
   + `[[include]]` fragments).
2. Passes `oxo-flow validate`, `oxo-flow dry-run`, and `oxo-flow lint`
   locally and in CI, with a fixture set that makes the dry-run
   deterministic and meaningful.
3. Ships the full compliance kit: `README.md` with a fidelity table, `NOTICE.md`,
   `LICENSE` (Apache-2.0), `metadata.json`, `.github/workflows/ci.yml`.

Non-goals: re-implementing upstream cluster profiles, Tower
reporting/launchpad features, Nextflow DSL1, and upstream "dev" branches.
Branches are IN scope: every branch is either ported, absorbed as a
`[config]`-driven variant, or triaged in the fidelity table (§6).

Coverage tiers for branch gaps (recorded per branch in the fidelity table):

- **P0 portable gap** — pure software dependencies; must be ported.
- **P1 objective blocker** — commercial license, paid database, or
  unavailable reference data; declare "objectively non-portable" WITH
  evidence, never silently skip.
- **P2 config variant** — same rules, parameterized (single-end, depth
  caps, ...); absorb as `[config]`/profile keys rather than a separate
  port.

A port that cannot be made faithful (missing tool, missing format feature,
undocumented upstream behavior) is not a port — it is a draft. Return it
with the specific blocker documented in the fidelity table, per §6.

---

## 2. oxo-flow format essentials — cheat sheet

### 2.1 Minimal skeleton

Every workflow is one TOML file with the `.oxoflow` extension. `[workflow]`
and at least one `[[rules]]` entry are required (validated by `oxo-flow
validate`; also required by the JSON Schema output of `oxo-flow schema`).

```toml
[workflow]
name = "my-pipeline"
version = "1.0.0"
description = "What this pipeline does"
author = "oxo-flow-community"

[config]
reference = "/data/refs/hg38.fa"      # {config.reference} in rules
out_dir = "results"

[defaults]
threads = 4
memory = "8G"

[[sample_groups]]                     # sample source for {sample} expansion
name = "cohort"
samples = ["S1", "S2"]

[[rules]]
name = "align"
input = ["raw/{sample}_R1.fastq.gz", "raw/{sample}_R2.fastq.gz"]
output = ["{config.out_dir}/aligned/{sample}.bam"]
shell = "bwa mem -t {threads} {config.reference} {input[0]} {input[1]} > {output[0]}"

[rules.resources]
threads = 16
memory = "32G"

[rules.environment]
conda = "envs/alignment.yaml"
```

This exact skeleton — `[workflow]` + `[config]` + `[defaults]` +
`[[sample_groups]]` + `[[rules]]` with `[rules.resources]` and
`[rules.environment]` — is verbatim-shaped from the canonical
`examples/gallery/06_rnaseq_quantification.oxoflow` and
`07_wgs_germline.oxoflow` [gallery]. Field names below were double-checked
against the `oxo-flow schema` dump and the reference docs.

### 2.2 Rule fields (the ones ports use)

| Field | Type | Notes |
|---|---|---|
| `name` | string | Required, unique. Expands with `_<group>_<sample>` / `_<pair_id>` suffixes. |
| `input` | array of strings | Path patterns; wildcard-bearing patterns trigger per-value fan-out. |
| `output` | array of strings | Path patterns. **Every declared output is verified to exist after the rule succeeds**; a missing output fails the rule (exit sentinel -1). May be `[]` for script-only rules with dynamic outputs (§13.34). |
| `shell` | string | Command template; supports `{input}`, `{input[N]}`, `{output}`, `{output[N]}`, `{threads}`, `{memory}`, `{config.x}`, wildcards. Triple-quoted for multi-line. |
| `script` | string | Script path; interpreter auto-detected (`.py`→python, `.R`→Rscript, `.sh`→bash, `.smk`→snakemake, `.nextflow`→nextflow run…). `shell` runs first, then `script`. |
| `description` | string | One line on what the rule does. |
| `depends_on` | array of strings | Explicit rule dependencies. Needed whenever file-based edges cannot express ordering (see §13.3). |
| `when` | string | Condition over config; false ⇒ rule skipped (`JobStatus::Skipped`). Forms: `config.run_qc`, `config.mode == "WGS"`, `config.min_cov >= 20`, `file_exists("panel.bed")`, `!`, `&&`, `||`, parens. |
| `retries` / `retry_delay` | int / string | `retries = 3`, `retry_delay = "30s"`. |
| `pre_exec` / `on_success` / `on_failure` | string | Lifecycle hooks, same placeholder expansion as `shell`. `on_failure` runs after all retries are exhausted. |
| `checkpoint` / `checkpoint_manifest` | bool / string | Snakemake-style re-entry: rule writes a TOML manifest declaring new samples/pairs; engine re-expands mid-run (max 32 rounds). Checkpoint rules must not use `{sample}`/`{group}` (validation error E014). |
| `localrule` | bool | Never submitted to a cluster scheduler. |
| `temporary` | bool | Delete outputs after the run once every dependent completed (tombstone + lazy regeneration). |
| `temp_output` / `protected_output` / `ancient` | arrays | Clean-after-use / never-delete / never-trigger-rebuild. |
| `log` / `benchmark` | string | `log = "logs/align_{sample}.log"`, `benchmark = "benchmarks/{sample}.tsv"`. |
| `tags` | array | `["qc", "alignment"]`. |
| `optional` | bool | Missing inputs become warnings, rule skipped instead of failing. |
| `required` | bool | Rule failure fails the pipeline even without dependents. |
| `priority` / `target` | int / bool | Scheduler tie-break; default target when running without `-t`. |
| `params` | table | Rule-scoped template variables: `[rules.params] min_qual = 20`, used as `{params.min_qual}`. Precedence over config during interpolation. |
| `envvars` | table | `[rules.envvars] CUDA_VISIBLE_DEVICES = "0"`. |
| `input_function` | string | Dynamic input resolver (advanced; prefer config-driven `expand_inputs`, §2.5). |
| `extends` | string | Inherit settings from a base rule (`align_fast extends = "align_default"`), override in own `[rules.resources]`. |
| `shadow` | string | `"minimal" | "shallow" | "full"` shadow directory mode. |

**Resources** (`[rules.resources]` sub-table; the top-level `threads` /
`memory` rule fields are deprecated but accepted):

```toml
[rules.resources]
threads = 8
memory = "32G"        # "16G", "8000M", …
gpu = 1               # optional
disk = "200G"         # optional; pre-flight warning if workdir free space is short
time_limit = "48h"    # optional; SIGKILLs the whole process group after the limit
```

**Deprecation note:** the schema and docs still accept `threads`/`memory`
directly on a rule, but `docs/guide/src/reference/workflow-format.md` marks
them deprecated — ports must use `[rules.resources]`. `[defaults] threads` /
`[defaults] memory` set rule-wide defaults; a rule with no explicit threads
declares **`threads=1`** in dry-run output (the "unset" sentinel, §13.1).

### 2.3 Wildcards and fan-out

- `{sample}` in any of `input`, `output`, `shell` **clones the rule once per
  (group, sample)** across all sample sources (§13.8 double-source trap).
  Expanded names: `align_cohort_S1`; the filesystem-discovery group is
  named `auto-discovered` (`align_auto-discovered_S1`) [V].
- `{pair_id}`, `{experiment}`, `{control}` expand once per `[[pairs]]`
  entry: `mutect2_CASE_001` [V]. E003 fires when a pair wildcard appears in
  `output`/`shell` but no `[[pairs]]` block declares it and it is not in
  `input` [V] — declare pairs, or put the wildcard in `input` too.
- `{config.x}` is **text substitution only** — never clones, never splits
  lists.
- A wildcard appearing in a rule's paths with **no value source** leaves the
  rule unexpanded — it shows in the preview with literal `{...}` placeholders
  and never executes [V].
- Built-in placeholders: `{input}` (space-joined), `{input[N]}` (0-indexed),
  `{input.name}` (named_input), `{output}`, `{output[N]}`, `{output.name}`
  (named_output), `{threads}`, `{memory}`, `{config.*}`.
- **Fan-out trigger fields:** a rule clones per sample/pair only when a
  wildcard appears in `input`, `output`, or `shell` (§13.33).
- **`{log}` IS a placeholder** (engine ≥ 0.13.0): `{log}` in `shell` renders the
  rule's `log` field with every instance wildcard and `{config.x}` expanded,
  and the parent directory is created automatically — `echo ok > {log}` works.
  Keep the `log` field for metadata and the report's log column.
- `named_input` / `named_output` sub-tables exist for many-file rules:
  `[rules.named_input] reads1 = "raw/{sample}_R1.fastq.gz"` used as
  `{input.reads1}` [gallery, workflow-format.md].

### 2.4 Sample sources (choose ONE for the default path)

| Source | Syntax | Expansion |
|---|---|---|
| Filesystem discovery | `[workflow] sample_pattern = "raw/{sample}_R1.fastq.gz"` | Scans disk at load; group name `auto-discovered`. Supports `{sample}`, `{replicate}`, `{read}`; **`{config.x}` inside the pattern works** [V]. |
| Inline groups | `[[sample_groups]] name = "cohort"; samples = [...]` | Per (group, sample). |
| Groups file | `[workflow] sample_groups_file = "metadata/groups.tsv"` (or .csv/.json) | TSV: `name<TAB>samples` (comma-separated ok). |
| Pairs | `[[pairs]] pair_id/experiment/control[/experiment_type][/metadata]` or `[workflow] pairs_file = "metadata/pairs.tsv"` | Per pair. `control` may be omitted (tumor-only; `{control}` renders empty). |
| Pairs from disk | `[workflow] pairs_pattern = "aligned/{pair_id}/{experiment}_vs_{control}.bam"` | Scans disk. **The pattern MUST contain all three wildcards `{pair_id}`, `{experiment}`, `{control}`** — a single-token pattern (e.g. SRR discovery `sra/{pair_id}/{pair_id}.sra`) is rejected at load (§13.37). |
| CLI — replace | `oxo-flow run wf.oxoflow --samples @ids.tsv` | **Overrides** every source with the sheet's groups (invocation-side sample swap; pairs with dropped sides are pruned). Fails loudly on empty sheets. |
| CLI — append | `--samples +@ids.tsv` | **Appends**: same-name groups merge (union, dedup), new groups added; pairs untouched. |
| CLI — filter | `--samples S1,S2` / `--samples first:3` / `--samples ready` | **Filters** the discovered set (unknown names fail). On workflows that declare NO samples, bare names **declare** the set (template-workflow invocation). |

All sample sources merge (deduplicated, sorted, comma-joined) into
**`config.samples_list`**; per-group lists exist as
`config.samples_<group_name>`. These are engine-injected and never trigger
checkpoint invalidation. **There is no `config.pairs_list`** (§13.7) [V].

### 2.5 Fan-in (gather / collect)

A gather rule runs **once** and collects per-sample files via
`expand_inputs` — the rule itself must NOT contain `{sample}` in its paths
(that would clone it). `expand_inputs` patterns form DAG edges at BOTH
levels: the expanded concrete paths order the runtime DAG, and the raw
patterns order the template-level graph (`graph -f dot`, the catalog's
source) since they share the producers' wildcard literals — declare every
collected artifact as a pattern so the graph shows the true fan-in
(engine ≥ 0.13.2):

```toml
[[rules]]
name = "combine_gvcfs"
input = []
expand_inputs = [
    { pattern = "variants/{sample}.g.vcf.gz", variables = { sample = "config.samples_list" } }
]
output = ["variants/cohort.g.vcf.gz"]
shell = """
gatk CombineGVCFs -R {config.reference} \
    $(for f in {input}; do echo "-V $f "; done) \
    -O {output[0]}
"""
```

Verbatim from `examples/gallery/07_wgs_germline.oxoflow` [gallery];
expansion to the concrete per-sample paths verified [V]. `variables` values
resolve as: `config.<key>` (array, or comma-joined string that is split),
inline list (`"[\"1\", \"2\"]"`), or single literal. Comma-splitting
applies **only** to `config.*` references — a single-element array
`["A,B"]` is the escape hatch for comma-containing values [V].

### 2.6 Environments — one backend per rule

```toml
# Conda (env yaml with exact pins — §5)
environment = { conda = "envs/fastp.yaml" }

# Docker image (verified accepted by validate; dry-run shows env=docker)
environment = { docker = "quay.io/biocontainers/bwa:0.7.17" }

# Singularity
environment = { singularity = "docker://broadinstitute/gatk:4.5.0.0" }

# mamba/pixi/venv/modules: same shape
# environment = { mamba = "envs/qc.yaml" }
# environment = { pixi = "envs/pixi.toml" }
# environment = { venv = ".venv/", venv_requirements = "envs/dev-req.txt" }
# environment = { modules = ["gcc/11.2.0", "openmpi/4.1.1"] }
```

All eight forms (conda, mamba, pixi, docker, singularity, venv, modules,
system) documented in `docs/guide/src/reference/execution-backends.md` and
`environment-system.md`. A rule with no `environment` runs on the **system**
backend (`lint` info W008). `[env_groups]` defines named reusable specs
referenced by `env_group = "qc_env"`. `[defaults] environment` sets a
default for every rule.

**Container spec portability convention**: prefer
`singularity = "docker://quay.io/biocontainers/..."` over
`docker = "..."` for container rules — the singularity form consumes the
same image but runs on HPC clusters without a docker daemon (live
campaign: scrna-seq converted all 22 container rules, bare refs fail
apptainer with "No transport type URI supplied" [V]). Use the `docker`
form only when the workflow depends on docker-specific behavior. Note
the fallback is not symmetric: a `docker://` spec is only valid for the
singularity backend, so a rule cannot declare both and get "docker
preferred, singularity fallback".

**Container runtime wrapper** (observed in live run logs): docker rules
execute as
`docker run --rm --user $(id -u):$(id -g) -v .:. -w . <image> sh -c '<shell>'`
— the workdir is bind-mounted, the command runs as the invoking user [V].

### 2.6.1 Conda env file (envs/*.yaml)

```yaml
name: fastp
channels:
  - bioconda
  - conda-forge
dependencies:
  - fastp=0.23.4
  - fastqc=0.12.1
```

Setup command is `conda env create -f <yaml>` (mamba auto-detects
mamba/micromamba/conda). Exact-pin policy in §5.

### 2.7 Modules and composition

- `[[include]]` with `path` + optional `namespace`: included rule names
  become `namespace::rule`; internal `depends_on` in the included file is
  re-prefixed automatically; external references use the prefixed name
  (`depends_on = ["qc::trim"]`). Included fragments may carry their own
  `[workflow]` table. Verified end-to-end: `qc::fastqc_cohort_S1` etc. [V].
  Fragment files validate standalone with `validate --as-include` [V].
- `profiles/<NAME>.toml`: `--profile <NAME>` applies `[config]` values
  that **fill in keys the workflow does not set — workflow values are never
  overridden** [V]. `.toml` is tried before `.oxoflow`.
- `[defaults]`, `[report]`, `[[references]]` (auto-built indexes, incl.
  auto-derivation when `reference_dir` is set), `[wildcard_constraints]`,
  `[cluster]`, `[env_groups]`, `[resource_groups]`, `[resource_budget]`,
  `[[execution_group]]` — see workflow-format.md.

### 2.8 CLI surface ports actually use

| Command | Purpose |
|---|---|
| `oxo-flow validate wf.oxoflow` | TOML parse + DAG construction + warnings on missing inputs. Exit 0/1. |
| `oxo-flow validate --as-include frag.oxoflow` | Validate an include fragment (skips DAG + input checks). |
| `oxo-flow dry-run [wf] [KEY=VALUE]...` | Read-only preview: DAG, per-rule threads/memory/env, **fully expanded shell commands**, input ✓/✗ markers, checkpoint-aware run/skip prediction. |
| `oxo-flow debug wf.oxoflow` | Expanded commands for every rule instance (same content dry-run shows, without plan context). |
| `oxo-flow debug wf.oxoflow -r <INSTANCE_NAME>` | One expanded rule — **use the expanded instance name** (`stats_auto-discovered_sampleA`), template names error with "rule not found" [V]. |
| `oxo-flow run wf.oxoflow -j N [KEY=VALUE]...` | Execute. `-j` default 1; `--rerun`, `--samples first:N|ready`, `--resume-failed`, `--keep-going`, `--max-threads/--max-memory`, `--skip-env-setup`, `--profile`. |
| `oxo-flow lint wf.oxoflow` | validate + style linting + secret scanning; `--strict` turns warnings into exit 1 [V]. |
| `oxo-flow schema` | JSON Schema dump — **a subset of the real format** (§13.10). |
| `oxo-flow graph wf.oxoflow -f dot` | DAG visualization (dev aid). |

Flag details recorded from `--help` on the 0.11.0 binary and
`docs/guide/src/commands/{validate,dry-run,run,debug,lint}.md`.

---

## 3. Nextflow → oxo-flow mapping table

Concepts verified against the gallery and scratch runs; where a Nextflow
feature has no direct equivalent, the "Port strategy" column says exactly
what to do.

| Nextflow (nf-core DSL2) | oxo-flow | Port strategy / notes |
|---|---|---|
| `process NAME { ... }` | `[[rules]] name = "name"` | One `[[rules]]` entry per process. Lowercase snake_case rule names. |
| `input: tuple val(meta), path(reads)` | `input = ["raw/{sample}_R1.fastq.gz", "raw/{sample}_R2.fastq.gz"]` | Declare the concrete file patterns. The `meta` map's fields that the command actually uses become `{config.x}` or wildcard values; the rest move to `[rules.rule_metadata]` (informational). |
| `output: tuple val(meta), path("*.bam"), emit: bam` | `output = ["aligned/{sample}.bam"]` | Declared outputs are the contract: they are verified to exist post-run and drive DAG edges. There is no `emit`; downstream rules reference files by path pattern. |
| `script:` block | `shell = """ ... """` | Copy the command verbatim, replacing `$reads`, `params.x` with `{input}`, `{config.x}` etc. Keep flags and file naming **byte-identical**. |
| `params.foo` (incl. `params.input`, `params.genome`) | `[config] foo = "..."` + `{config.foo}` | Every `params.*` referenced by the default path becomes a config key with the upstream default as its value. |
| `nextflow run ... --foo bar` | `oxo-flow run wf.oxoflow --foo bar` (or `foo=bar` positional) | Every `[config]` key is a CLI flag automatically; positional `KEY=VALUE` after the workflow file works too [V]. |
| `Channel.fromPath('data/*_R1.fastq.gz')` | `sample_pattern = "data/{sample}_R1.fastq.gz"` | Filesystem discovery; group `auto-discovered`. |
| `Channel.fromFilePairs('data/*_{1,2}.fastq.gz')` | `sample_pattern = "data/{sample}_R1.fastq.gz"` + second input `"data/{sample}_R2.fastq.gz"` | Pattern discovers the sample set; rules take both mates as `{input[0]}`, `{input[1]}`. |
| `Channel.fromSamplesheet('samplesheet.csv')` | `[[sample_groups]]` / `sample_groups_file` / `[[pairs]]` / `pairs_file` | Column semantics decide the mapping: sample-only → groups; experiment/control → pairs. |
| `Channel.fromFilePairs` with meta columns | `[rules.rule_metadata]` + config | Static metadata → config keys or `rule_metadata`; runtime-discovered → `checkpoint` re-entry (advanced). |
| `input: path(reads)` single file | `input = ["reads/{sample}.fastq.gz"]` | Identical shape. |
| `collect()` on a channel | `expand_inputs` with `config.samples_list` | The gather rule stays a **single instance**; per-sample files become its input list (§2.5) [V]. |
| `mix()` / `join()` / `combine()` | `depends_on` + multi-input rule | Merge semantics are expressed by the input list and explicit ordering. |
| `scatter`/`gather` in a process (per-chromosome) | `transform` operator (§3.1) or legacy `scatter` field | `transform` is the recommended unified split→map→combine. |
| `publishDir 'results/'` | No equivalent — outputs are written where `output = [...]` says | Declare outputs directly at `results/...` paths; `publishDir` options (mode, overwrite, pattern) have no equivalent, note in fidelity table. |
| `container 'quay.io/biocontainers/fastp:0.23.4'` | `environment = { docker = "quay.io/biocontainers/fastp:0.23.4" }` | Copy the image string verbatim (§5). Verified syntax [V]. |
| `container 'docker://broadinstitute/gatk:4.5.0.0'` | `environment = { singularity = "docker://broadinstitute/gatk:4.5.0.0" }` | Copy verbatim. Verified syntax [V]. |
| `conda 'envs/fastp.yml'` | `environment = { conda = "envs/fastp.yaml" }` | Port the env yaml with exact pins (§5). |
| `cpus 4` | `[rules.resources] threads = 4` | |
| `memory '8.GB'` | `[rules.resources] memory = "8G"` | Convert Groovy GByte notation: `'8.GB'`→`"8G"`, `'8000.MB'`→`"8000M"`. |
| `time '2.h'` | `[rules.resources] time_limit = "2h"` | |
| `label 'process_high'` | `[rules.resources]` values or `[defaults]` | Labels are group policies; bake the actual values into resources (per-rule or defaults), record in fidelity table. |
| `withName: 'TRIM' { cpus = 8 }` | Per-rule `[rules.resources]` | The `withName`/`withLabel`/`withProcessName` scope IS the per-rule table. |
| `withParams: [foo: 'x']` | `[config]` defaults / `profiles/*.toml` | |
| `when: params.foo` | `when = "config.foo"` | Same truthiness; full expression grammar in §2.2. |
| `errorStrategy 'retry'` + `maxRetries 3` | `retries = 3` (+ `retry_delay = "30s"`) | `retry` → `retries = N`; `ignore`/`finish` → `-k`/`required` semantics; record non-default strategies in fidelity table. |
| `maxForks` | `-j <N>` | Runtime knob, not workflow metadata. |
| `executor 'slurm'`, cluster profiles | `[cluster]` / `--profile` | Out of scope for the default path; `localrule` exists for always-local steps. |
| `env` directive | `[rules.envvars]` | Same shape. |
| `module 'gcc/11.2.0'` | `environment = { modules = ["gcc/11.2.0"] }` | |
| `tag`, `label` (cosmetic) | `tags = [...]`, `description` | Cosmetic mapping. |
| `afterScript` / `onError` | `pre_exec` / `on_success` / `on_failure` | `afterScript` has no exact twin — if it produces a file the next process needs, make it part of `shell`; else `on_success`. |
| `exec` (Groovy blocks) | `script = "scripts/x.py"` | Move logic into a script file; keep `shell`/`script` declarative. |
| `params.genomes` (nf-core genome config) | `[config]` + `[config] genome = { default = "GRCh38", choices = [...] }` | Declarative config form (`{default, choices, type}`) mirrors the nf-core genome matrix. |
| `include { ... }` from modules | `[[include]] path = "modules/x.oxoflow" namespace = "x"` | Module per file; namespaces keep `x::process` names (nf-core module names) [V]. |
| `stub` runs | Not supported | Forbidden in ports anyway (§6). |
| `-resume` | Checkpoint resume (automatic) | Ports get resume for free: re-running `run` skips completed rules [V]. |

### 3.1 nf-core scatter/gather → `transform`

nf-core splits per chromosome via channel grouping. In oxo-flow the
canonical form is the unified `transform` operator (verbatim from
`examples/gallery/10_transform_operator.oxoflow` [gallery], chunk naming
verified [V]):

```toml
[[rules]]
name = "variant_calling"
input = ["aligned/sample.bam"]
output = ["variants/sample.g.vcf.gz"]

[rules.resources]
threads = 8

[rules.transform.split]
by = "chr"
values_from = "config.chromosomes"

[rules.transform]
map = "gatk HaplotypeCaller -R {config.reference} -I {input} -L {chr} -O {output} -ERC GVCF"
cleanup = true

[rules.transform.combine]
shell = "gatk GatherVcfs $(for f in {chunks}; do echo \"-I $f \"; done) -O {output}"
```

Verified expansion: map rules `variant_calling_chr1`, `variant_calling_chr2`;
chunk outputs at `.oxo-flow/chunks/chr/chr1.g.vcf.gz` (full multi-part
extension preserved); combine rule `variant_calling_combine`; combine's
`{chunks}`/`{input}` = the chunk list [V]. `cleanup = true` deletes chunks
after a fully successful run. Split priority: `values` → `values_from` →
`n` → `glob`. Aggregate mode (`aggregate = true, method = "concat"`) exists
for trivial merges. Failures retry at chunk level; combine waits for all
chunks.

---

## 4. Snakemake → oxo-flow mapping table

| Snakemake | oxo-flow | Port strategy / notes |
|---|---|---|
| `rule align:` | `[[rules]] name = "align"` | Same shape. |
| `input: "data/{sample}.fq.gz"` | `input = ["data/{sample}.fq.gz"]` | Identical wildcard semantics (fan-out). |
| `output: "aligned/{sample}.bam"` | `output = ["aligned/{sample}.bam"]` | |
| `shell: "bwa mem ..."` | `shell = "bwa mem ..."` | Same command text; `{sample}` interpolates identically. |
| `run:` (Python) / `script: "x.py"` | `script = "scripts/x.py"` | Interpreter auto-detected from extension; `run:` bodies become script files (the port must keep the script and its tool deps in the env). |
| `params: prefix=lambda wc: ...` | `[config]` or `[rules.params]` | Simple params → `{config.x}`; rule-scoped params → `[rules.params]` (`{params.min_qual}`); Python lambdas must be resolved to plain values at port time. |
| `wildcards.sample` in shell | `{sample}` | Same syntax. |
| `config["x"]`, `config.x` | `{config.x}` | Same. |
| `configfile: "config.yaml"` | `[config]` + `profiles/<NAME>.toml` | Merge the yaml into `[config]`; alternate configs become profiles (fill-in only, workflow values win [V]). |
| `threads: 8` | `[rules.resources] threads = 8` | |
| `resources: mem_mb=8000` | `[rules.resources] memory = "8000M"` | Convert `mem_mb` → `"<N>M"`, `mem_gb` → `"<N>G"`; `time_min` → `time_limit`. |
| `conda: "envs/foo.yaml"` | `environment = { conda = "envs/foo.yaml" }` | Port the yaml **with exact pins** (§5). Verified syntax [V]. |
| `container: "docker://..."` | `environment = { singularity = "docker://..." }` | Copy the URI verbatim. |
| `expand("results/{sample}.txt", sample=SAMPLES)` | `expand_inputs = [{ pattern = "results/{sample}.txt", variables = { sample = "config.samples_list" } }]` | Gather/fan-in (§2.5) [V]. |
| `input functions` (`lambda wc: ...`) | `expand_inputs` with config references, or `depends_on` | Resolve the function to the concrete list at port time; keep it config-driven so CLI overrides work. `input_function` exists but is a runtime hook — prefer declarative. |
| `checkpoint:` + `input: functions.get_sample_names` | `checkpoint = true` + `checkpoint_manifest = "manifest.toml"` | Native feature — the rule writes a TOML manifest declaring `sample = [...]` / `pairs = [...]`; engine re-expands and runs new instances in the same run (max 32 rounds, E013/E014 guards). |
| `wildcard_constraints:` | `[wildcard_constraints] sample = "[A-Z0-9]+"` | Same semantics (non-matching discovered values ignored). |
| `log: "logs/{sample}.log"` | `log = "logs/{sample}.log"` | |
| `benchmark:` | `benchmark = "benchmarks/{sample}.tsv"` | |
| `temp("...")` | `temp_output = [...]` or `temporary = true` | `temp_output`: cleaned after downstream completes. `temporary = true`: whole-rule outputs deleted after the run once dependents finished, tombstone + lazy regeneration (leaf rules keep outputs). |
| `protected("...")` | `protected_output = [...]` | |
| `ancient("...")` | `ancient = [...]` | Never triggers re-execution. |
| `localrule:` | `localrule = true` | |
| `group:` | `group = "label"` | Cluster grouping. |
| `ruleorder:` | `depends_on` + unambiguous paths | oxo-flow has no `ruleorder`; make the chain unambiguous by distinct output paths and explicit `depends_on` where the DAG cannot infer (§13.3). |
| `onerror:`/`onsuccess:` (workflow-level) | `on_failure` / `on_success` per rule | Per-rule hooks; workflow-level equivalents don't exist. |
| `shadow: "shallow"` | `shadow = "shallow"` | Same modes. |
| `priority:` | `priority = N` | Higher runs first among ready rules. |
| `latency-wait` | Not needed | File-system latency guard has no equivalent; declared outputs are verified directly. |
| `--cores` / `-j` | `-j <N>` / `--max-threads <N>` | Same knobs. |
| `--config x=y` | `x=y` positional or `--x y` | Verified [V]. |
| `--until`, `--target` | `-t <rule>` (prefix matching) | `-t final_output` runs only it plus upstream. |
| `--forceall` | `--rerun` | |
| `--rerun-incomplete` | `--resume-failed` | Resume only failed rules. |
| `--dry-run` / `--printshellcmds` | `dry-run` / `debug` | dry-run shows expanded commands; `debug -r <instance>` shows one [V]. |
| `Snakefile` includes/modules | `[[include]]` + `namespace` | Module files per include; namespaced rule names [V]. |

### 4.1 Snakemake `expand()` corner

`expand("results/{sample}.txt", sample=config["samples"])` inside an input
list is exactly `expand_inputs`. But Snakemake also uses `expand()` inside
**shell** strings (e.g. a loop); oxo-flow's `{config.samples_list}` renders
the merged list as a **comma-joined string** — the documented shell pattern
is:

```toml
shell = "for s in $(echo {config.samples_list} | tr ',' ' '); do ...; done"
```

Verified: `config.samples_list` renders comma-joined in shell expansion [V].

### 4.2 Custom per-file wildcards (e.g. `{sra}`) — the script-rule pattern

Snakemake workflows that fan out over a non-sample wildcard whose values
come from a table at load time (e.g. `{sra}` in
`auto_sra_rnaseq_pipeline`) have no direct fan-out source in oxo-flow:
only `{sample}`/`{pair_id}`/`{experiment}`/`{control}` clone rules, and
`pairs_pattern` cannot help (§13.37). Port them as **single-instance
script rules** [V, workflow #23]:

- The rule declares `output = []` (§13.34) and
  `script = "scripts/x.py …"`; the script iterates the table (pandas) and
  runs the identical per-value command.
- Downstream per-sample rules consume the dynamic paths inside their own
  scripts and order via `depends_on = ["<template-name>"]` (§13.35).
- Preserve upstream concurrency caps: a run.py-style global cap
  (`--resources limit_dump=2`) becomes an internal worker pool of 2 in the
  script; a per-job resource with a global cap becomes `[resource_groups]`
  (§13.38).
- Record the structural deviation (rule granularity change) in the
  fidelity table — the commands per value stay byte-identical.

---

## 5. Version pinning policy

## 5. Version pinning policy

**Every tool that ships in a port must carry an exact version. `latest` is
forbidden — in container tags and in conda pins.**

1. **nf-core / Nextflow processes with a container directive:** copy the
   exact image string from the module, e.g.
   `container 'quay.io/biocontainers/fastp:0.23.4--0'` →
   `environment = { docker = "quay.io/biocontainers/fastp:0.23.4--0" }`.
   Keep the full tag including the `--<build>` suffix — that is the actual
   reproducible artifact. Verified: arbitrary image strings with tags pass
   `validate` [V].
2. **nf-core processes with a conda directive:** copy the module's env
   yaml, pins included (`fastp=0.23.4`), and map it to
   `environment = { conda = "envs/<tool>.yaml" }`.
3. **Snakemake rules with `conda: "envs/foo.yaml"`:** copy the yaml
   verbatim — the pins (`- fastp=0.23.4`, `- samtools=1.19.2`) carry the
   reproducibility. If the upstream env has unpinned packages, pin them to
   the versions present in the upstream lockfile if one exists, else resolve
   at port time from bioconda and record the resolution in the fidelity
   table.
4. **Snakemake rules with `container:`:** copy the URI verbatim
   (`docker://quay.io/biocontainers/fastp:0.23.4--0`).
5. **No upstream pin at all** (rare): use the biocontainers `latest` tag at
   port time for the container, e.g. `quay.io/biocontainers/<tool>:latest`,
   and **mark it in the fidelity table** with the exact tag resolution date
   and the version observed. The reviewer (Definition of Done §14) must be
   able to see every unpinned-by-upstream tool at a glance.
6. **Inferring versions from tool output is forbidden.** If the upstream
   does not declare a version anywhere, the port records "upstream does not
   pin" in the fidelity table and applies rule 5.

---

## 6. Fidelity policy

The port's contract:

- **Replicate the default-parameters main execution path 100%**: same
  tools, same versions, same command logic — flags, orderings, file naming,
  output formats. A diff of `debug` output against the upstream command text
  should show only the mechanical substitutions (paths, params).
- **Fidelity table is mandatory** in `README.md` (§9): one row per upstream
  process/rule: `Upstream process | oxo-flow rule | Tool (version) | Notes`.
  Any deviation — renamed output, merged steps, dropped cosmetic branch,
  profile-only config — goes in the Notes column.
- **Forbidden in ports:**
  - placeholder/echo rules (`shell = "echo 'Alignment placeholder' > ..."` —
    the gallery uses these for *demonstration*; ports must not),
  - unversioned tools (`latest`),
  - silently dropped steps (a step that cannot be ported must be listed in
    the fidelity table as `not ported` with the reason),
  - reordering or re-flagging commands to "make it cleaner" — the command
    logic is the product.
- nf-core `params.*` that default to `false`/empty and gate optional
  branches: map to `[config]` with the same default; the branch is preserved
  via `when` conditions, and the fidelity table notes it as "off by default,
  same as upstream".
- If the port cannot meet the contract (missing tool, no equivalent
  feature), stop and return the blocker in the fidelity table instead of
  approximating.

---

## 7. Repo layout + test standard

### 7.1 Exact tree

Every port lives in its own repository/package directory, e.g.
`<your-workspace>/<pipeline-name>/`:

```text
<pipeline-name>/
├── main.oxoflow              # the workflow (single file unless > ~30 rules;
│                             #   then + modules/ fragments via [[include]])
├── envs/                     # conda env yamls, one per environment
│   └── <tool>.yaml
├── scripts/                  # helper scripts (only if the upstream has them)
├── profiles/                 # optional: profiles/<NAME>.toml
├── test/
│   ├── fixtures/             # tiny real input files (never synthetic blobs)
│   │   └── raw/…
│   └── run.sh                # the acceptance test (§7.3)
├── .github/
│   └── workflows/ci.yml      # §8
├── README.md                 # §9 template
├── NOTICE.md                 # §10 template
├── LICENSE                   # §11
└── metadata.json             # §12
```

Naming: `<pipeline-name>` = the upstream repo's name, kebab-case. Rule
names = upstream process/rule names in snake_case.

### 7.2 test/fixtures requirements

- Real, tiny data of the same format as upstream inputs (e.g. a 2-read
  FASTQ pair, a 10-line CSV) — **not** placeholder text files where the
  workflow does real parsing. If a step cannot run on the tiny fixture (a
  BWA index needs ~700MB), the fixture covers it up to the point where the
  tool would fail, and run.sh still exercises `validate` + `dry-run` for
  the whole DAG.
- Fixture sample names: `S1`, `S2` (or upstream example names) — recorded
  in `[[sample_groups]]` so the dry-run is deterministic without
  `sample_pattern` needing real files on CI.
- Keep fixtures checked into the repo (a few KB to a few MB).

### 7.3 test/run.sh (mandatory, exact shape)

```bash
#!/usr/bin/env bash
# Acceptance test for <pipeline-name> port.
# Usage: ./test/run.sh            (uses ./main.oxoflow)
set -euo pipefail
cd "$(dirname "$0")/.."
OXO=${OXO:-oxo-flow}

echo "==> validate"
"$OXO" validate main.oxoflow

echo "==> lint (warnings are acceptable, errors are not)"
"$OXO" lint main.oxoflow

echo "==> dry-run with default config"
"$OXO" dry-run main.oxoflow --samples first:1 > /tmp/oxo-dryrun-$$.txt
grep -q "would execute" /tmp/oxo-dryrun-$$.txt

echo "==> debug: expanded commands contain no literal {wildcards}"
"$OXO" debug main.oxoflow | grep -q '{sample}' && { echo "unexpanded wildcards in debug output"; exit 1; } || true

echo "PASS"
```

Requirements: `set -euo pipefail`; exit non-zero on any failure; run
`validate`, `lint`, `dry-run` (default config, `--samples first:1` when the
workflow is sample-scoped), and a `debug` assertion that no literal
`{sample}`/`{config.` placeholders survive expansion. Local runs use
`OXO=/path/to/oxo-flow`.

### 7.4 Iterate-to-green instructions

1. Write `main.oxoflow` + envs + fixtures.
2. `oxo-flow validate main.oxoflow` → fix TOML/DAG errors. Exit 0 required;
   warnings about missing inputs are expected pre-fixture, but note that
   `validate` warns only for inputs **not produced by any rule output**
   (literal patterns, globs, dirs, and files with no producer) [V].
3. `oxo-flow dry-run main.oxoflow` → inspect the expanded plan:
   - every sample/pair rule expanded (instance names `rule_group_sample` /
     `rule_pair_id`),
   - gather rules present exactly once with the full input list,
   - `input ✗` markers on fixture files you forgot,
   - threads/memory/env per rule as intended.
4. `oxo-flow debug main.oxoflow` → diff the expanded commands against the
   upstream command text (with `{...}` placeholders substituted by the
   dry-run values). This is the fidelity check.
5. `./test/run.sh` green locally with
   `OXO=/path/to/oxo-flow`.
6. Push → CI (§8) green.

---

## 8. CI template (`.github/workflows/ci.yml`)

ubuntu-latest; install oxo-flow from the latest release tarball (stable asset, layout
verified: single `oxo-flow` file at archive root — no directory prefix, so
`tar xzf` + `mv` of the bare file is correct); timeout 10m.

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4

      - name: Install oxo-flow (latest release tarball)
        run: |
          curl -fL -o oxo-flow.tar.gz \
            https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
          tar xzf oxo-flow.tar.gz
          sudo mv oxo-flow /usr/local/bin/
          oxo-flow --version

      - name: Validate, lint, dry-run
        run: bash ./test/run.sh
```

**CI badge** (README §9 header):

```markdown
[![CI](https://github.com/<org>/<pipeline-name>/actions/workflows/ci.yml/badge.svg)](https://github.com/<org>/<pipeline-name>/actions/workflows/ci.yml)
```

The tarball URL above is the **verified** install path: the archive is
`oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz` (a byte-identical copy of the versioned tarball) and contains exactly one
file, `oxo-flow`.

---

## 9. README.md template (~80 lines, exact skeleton)

```markdown
# <repo-name> — <catalog-style title>

[![CI](https://github.com/oxo-flow-community/<repo>/actions/workflows/ci.yml/badge.svg)](https://github.com/oxo-flow-community/<repo>/actions/workflows/ci.yml)

> ★ Verified · ⇄ Official port of [`<upstream-name>`](<upstream-repo-url>) @ `<tag-or-commit>`
> — same tools, same versions, same commands. Part of the
> [oxo-flow-community catalog](https://oxo-flow-community.github.io/).

<One-paragraph description: what a user gets — the analysis goal and main
steps. No "port" framing outside the blockquote.>

## Installation

### 1. Install oxo-flow

Requires **oxo-flow ≥ 0.12.0**. Release binary (recommended):

```bash
curl -fL -o oxo-flow.tar.gz \
  https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz
sudo mv oxo-flow /usr/local/bin/
```

Alternative: `conda install -c bioconda oxo-flow-cli` (the bioconda package
may lag behind releases; other platform binaries are on the releases page).

### 2. Get this workflow

```bash
git clone https://github.com/oxo-flow-community/<repo>.git
```

### 3. Requirements

- **Reference data**: <genome FASTA, annotation GTF, indices … — list the
  workflow's actual external inputs>
- **Compute**: <up to N threads / M GB per rule — from the workflow's own
  resource settings>
- **Tools**: <containers with pinned images OR conda envs with pinned
  versions — state which, matching the TOML environments>

## Usage

```bash
# 1. prepare data (see test/fixtures for the expected layout)
# 2. preview the plan
oxo-flow dry-run main.oxoflow
# 3. run
oxo-flow run main.oxoflow -j 8
```

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command |
| ... | | | |

Rows cover **every** upstream process/rule. "not ported" rows are allowed
only with a reason.

## Source

Ported from **[<upstream-name>](<upstream-repo-url>)**, version
`<tag-or-commit>` (<upstream license, e.g. MIT>). Created 2026-08-15; this
workflow **may lag upstream releases**. Attribution in
`NOTICE.md`.

## Test

```bash
bash test/run.sh   # validate + lint + dry-run, exits 0
```

## License

Apache-2.0. Copyright (c) 2026 oxo-flow-community.

## Community

https://oxo-flow-community.github.io/
```

---

## 10. NOTICE.md template

```text
<pipeline-name>
Copyright (c) 2026 oxo-flow-community

This pipeline is a port of <upstream-name>
(<upstream-repo-url>), version <tag-or-commit>, authored by
<upstream-authors-or-org>.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

---------------------------------------------------------------------
Upstream license

This port is derived from <upstream-name> under the <license-name>
license. The upstream LICENSE must be included **verbatim** in this
repository: fetch it from the upstream repository at the ported
<tag-or-commit> and place it at LICENSE.upstream. (Apache-2.0 §4(d):
attribution notices from the Source form must be retained.)
---------------------------------------------------------------------
```

Rule: the NOTICE instructs the port author to fetch the upstream LICENSE
from the upstream repo at the ported commit and commit it verbatim as
`LICENSE.upstream` — the porting agent must actually do this, not just
write the instruction.

**Upstream has no license file** (GitHub reports "no license"): skip
`LICENSE.upstream` and replace the NOTICE's upstream-license paragraph
with an explicit statement of the absence (§13.40).

---

## 11. LICENSE

Port repositories carry the **full Apache-2.0 text** — copy the file from
the `LICENSE` file in the engine repo (it is the standard Apache
2.0 text with the appendix, §178–190: "Copyright 2025 Traitome / Licensed
under the Apache License…"). Conventions to mirror:

1. Keep the complete Terms and Conditions text (§1–9) verbatim.
2. Replace the appendix copyright line with the port's:
   `Copyright (c) 2026 oxo-flow-community`
   (keep the "Licensed under the Apache License…" appendix boilerplate).
3. The oxo-flow source repo has **no NOTICE file**; attribution lives in
   this port's `NOTICE.md` (§10) plus the retained upstream license file.
4. Add `LICENSE.upstream` (the upstream repo's license, verbatim) per §10.

---

## 12. metadata.json — exact schema (registry v2)

Every repo ships `metadata.json` — this is the source record for the catalog
registry (`data/pipelines.json` in the site repo). Catalog v2 fields:

```json
{
  "name": "oxo-flow-rnaseq",
  "title": "RNA-seq: alignment, quantification and QC",
  "origin": "port",
  "rating": "verified",
  "coverage": "default-path",
  "engine": "nextflow",
  "source": {
    "repo": "nf-core/rnaseq",
    "url": "https://github.com/nf-core/rnaseq",
    "tag": "3.26.0",
    "sha": "<40-hex-sha-of-tag>",
    "license": "MIT"
  },
  "created": "2026-08-15",
  "domain": "bulk RNA-seq",
  "tags": ["rna-seq", "star", "quantification"],
  "description": "One catalog paragraph: what a user gets — goal and main steps.",
  "scope": ["fastqc", "trim", "star_align", "..."],
  "excluded": ["optional upstream branches, with reasons"],
  "rule_count": 44,
  "tools": ["fastqc", "star", "samtools", "..."],
  "installation": {
    "engine": "oxo-flow >= 0.12.0",
    "toolchain": "containers (Docker/Singularity) — pinned images",
    "requirements": [
      "Reference data: genome FASTA, annotation GTF, chrom sizes",
      "Compute: up to 12 threads / 72 GB per rule"
    ]
  },
  "repo_url": "https://github.com/oxo-flow-community/oxo-flow-rnaseq",
  "license": "Apache-2.0",
  "upstream_license": "MIT"
}
```

Field rules:

- `origin`: `"port"` (migration of a Nextflow/Snakemake pipeline) · `"original"`
  (built for oxo-flow) · `"curated"` (third-party repo, listed via PR).
- `rating`: `"live-verified"` (verified + real end-to-end run: exit 0, all
  rules complete, report snapshot), `"verified"` (fidelity-checked,
  CI/dry-run green — §14), or `"community"`.
- `engine`: the SOURCE engine for ports (`"nextflow"` | `"snakemake"`); omitted
  for original workflows.
- `title`/`description` are catalog copy — user-facing, no "port" framing.
- `scope`: the port's rule names — lowercase, matching the entry workflow's
  rule names (`::`-namespace stripped) — the catalog's coverage list.
  Port-added helper rules (e.g. `annot_export`, `config_export`) are
  included; they are real rules, just not upstream processes. Upstream
  module-composition detail (e.g. "BAM_SORT_STATS_SAMTOOLS (SAMTOOLS_SORT +
  ...)") belongs in the README fidelity table, not this field.
- `coverage`: the port's branch-line status — `full-line` (every upstream
  branch ported or P1-triaged with evidence), `default-path` (main path
  ported, P0 gaps remain), `partial` (draft). Displayed next to the
  rating badge; honest default for older ports is `default-path` until the
  §15 completeness audit clears them.
- `excluded`: upstream branches not ported, each with its coverage tier
  (P0/P1/P2) and reason — P1 requires the blocker evidence.
- `tools`: deduped tool names WITHOUT versions (versions live in the TOML
  pins and the README fidelity table).
- `installation`: engine floor; `toolchain` states truthfully whether the
  workflow runs tools via containers or conda (matching the TOML
  environments); `requirements` lists reference data and compute needs.
}
```

---

## 13. Gotchas — verified behaviors ports must work around

Each item is marked with what it is based on: `[V]` = observed against the
0.11.0 binary on 2026-08-15, `[docs]` = documented in
`docs/guide/src/reference/{workflow-format,wildcards,dag-engine,execution-backends}.md`
or `docs/guide/src/commands/*.md`, `[gallery]` = canonical example file.

1. **`threads` unset ⇒ sentinel 1.** A rule without `[rules.resources]
   threads` (and no `[defaults] threads`) reports `threads=1` in dry-run
   output. This is the documented "unset" convention — do not confuse it
   with an actual one-thread declaration. `[V]`
2. **Engine-internal/reserved keys.** `cleanup_chunks` is engine-internal
   (serde `skip_deserializing`): a user-set value is **silently ignored**,
   `validate` passes [V]. Chunk cleanup is controlled only by
   `[rules.transform] cleanup = true`. Engine-injected config keys:
   `config.samples_list`, `config.samples_<group>` — set by the engine,
   never trigger invalidation, and referencing them before any sample source
   exists yields a literal `config.<key>` in expanded paths (observed as
   `variants/config.pairs_list.vcf`) [V]. `[docs]` + `[V]`
3. **DAG edges are exact-string matches on file paths.** `input` string ≡
   `output` string ⇒ edge; everything else ⇒ no edge. Consequently:
   **glob inputs (`data/*.txt`) and directory inputs (`data`) form NO DAG
   edges** — a consumer may race its producer and fail (`cat: data/*.txt:
   No such file or directory` observed) [V]. Fix: `depends_on = ["producer"]`
   on the consumer. This is the single most common wiring bug in ports.
   `[docs: dag-engine.md]` + `[V]`
4. **Config list comma-splitting.** A `config.*` value referenced by
   `expand_inputs` / `transform.split.values_from` / `scatter.values_from`
   is split on commas when it is a string: `"A,B,C"` → 3 values [V]. A
   TOML array `["X","Y"]` → 2 values [V]. Escape hatch: single-element
   array `["A,B"]` → one value [V]. **Inline literals written directly in
   `variables` are never split.** `[docs: workflow-format.md]` + `[V]`
5. **Output parent directories are created by the executor** — a rule whose
   output is `out/combined.txt` runs fine with no `mkdir -p out` [V]
   (gallery still writes `mkdir -p` lines for multi-directory outputs and
   for `-o qc/`-style tools; harmless either way). Directory **inputs**,
   though, must exist or the rule fails at runtime [V].
6. **Dry-run is checkpoint-aware and read-only.** With a checkpoint
   present it classifies every rule exactly like `run` would
   (`[skip: up to date]`, `[run: input changed]`, `[rerun: downstream of
   X]`, `[skip: when condition false]`). Without one it says so and treats
   everything as never completed [V]. `[docs: commands/dry-run.md]`
7. **Plain-file input invalidation is content-based (≤64 MiB).** A `touch`
   does NOT invalidate a completed rule [V]; changing file content DOES
   (`[run: input changed]` observed) [V]. `[docs: commands/run.md]` —
   debugging "why won't my rule re-run" usually comes back to this.
8. **`sample_pattern` discovery and `[[sample_groups]]` are separate
   sources that BOTH fan out.** A rule referencing `{sample}` expands once
   per group — including the `auto-discovered` group — so declaring both
   yields duplicate instances writing the same outputs [V]. Ports must
   choose **one** sample source for the default path (§2.4). `[V]`
9. **There is no `config.pairs_list`.** Only samples are merged into an
   injected config key. To gather across pairs, add a user config array
   (`[config] pair_ids = ["CASE_001", ...]`) and reference it in
   `expand_inputs` — verified working [V]. Keep it in sync with
   `[[pairs]]`; the README must document that.
10. **`oxo-flow schema` output is a subset.** The dumped JSON Schema
    contains only `workflow`, `references`, `config`, `cluster`,
    `webhooks`, `rules` (with a reduced rule-field set) — it omits
    `defaults`, `pairs`, `sample_groups`, `env_groups`, `include`,
    `transform`, `resources`, `environment`, `expand_inputs`, and more,
    all of which `validate` accepts [V]. Use `validate` + the reference
    docs as the format authority, not the schema dump. `[V]`
11. **`debug -r` needs the expanded instance name.** `debug wf.oxoflow -r
    stats` errors "rule not found"; `-r stats_auto-discovered_sampleA`
    works [V]. Get instance names from `dry-run`/`debug` output.
12. **Expanded rule naming.** `rule_group_sample` (samples), `rule_pair_id`
    (pairs), `namespace::rule_group_sample` (included + expanded),
    `rule_<split_value>` and `rule_combine` (transform), `rule_<pair_id>`
    (pairs). `[V]` + `[docs: wildcards.md]`
13. **One backend per rule, and the backend must contain every tool in the
    rule's command.** A `bwa-mem2 … | samtools sort` pipe cannot run in a
    single-tool container — the gallery explicitly uses a combined conda
    env for this ("single-tool docker images cannot run it") [gallery:
    07_wgs_germline.oxoflow, 13_simple_variant_calling.oxoflow]. Ports must
    group tools per rule accordingly.
14. **Missing declared outputs fail the rule.** After a rule's shell exits
    0, every declared output is checked on disk; a missing one fails the
    rule with exit sentinel -1 and runs `on_failure`. This is how
    "cleanup masked a tool failure" is caught. `[docs: workflow-format.md]`
15. **`validate` exit 0 ≠ clean.** Missing-input warnings print and exit 0
    [V]; they are listed for every input not produced by an exact output
    match — globs, directories, and dead paths included. `lint --strict`
    turns warnings into exit 1 [V]. CI uses `validate` + `lint` +
    `dry-run`, not exit codes alone.
16. **E003: wildcard in output but not in input.** `{pair_id}` in `output`
    with no `[[pairs]]` block and no `{pair_id}` in `input` fails
    validation [V]. Declare the pair source or add the wildcard to an
    input path.
17. **Wildcard constraints.** `[wildcard_constraints] sample = "[A-Z0-9]+"`
    filters discovered values (non-matching ones are ignored).
    `[docs: wildcards.md]`
18. **Run flags must precede `KEY=VALUE` overrides.** `run wf.oxoflow
    min_quality=30 --json` errors with guidance; the override list is
    trailing [docs: commands/run.md]. CI/test scripts: flags first.
19. **Workflow file auto-discovery.** `dry-run`/`run` with no WORKFLOW
    argument picks `main.oxoflow` first, then the alphabetically first
    `*.oxoflow` [docs]. Ports name the file `main.oxoflow` so plain
    `oxo-flow run` works.
20. **The `.oxoflow` extension is mandatory** for validation tooling
    ([docs: workflow-format.md]).
21. **Output collisions warn but don't fail.** Two rules producing
    overlapping wildcard patterns (both `{sample}.vcf`) produce
    `detect_output_collisions` warnings — resolve by distinct output dirs.
    `[docs: dag-engine.md]`
22. **Included fragments validate standalone with `validate --as-include`**
    (skips DAG + input checks) [V]; plain `validate` on a fragment still
    checks its own internal DAG, which is fine for fragments with
    `depends_on` chains [V].
23. **Profile merge is fill-in only** — a `profiles/cluster.toml`
    `threads = "32"` does not override the workflow's `[config] threads`
    [V]. To make profiles actually switch values, the workflow config must
    leave the key unset (or use distinct keys).
24. **Checkpoint re-entry cap and guards.** Checkpoint rules can't use
    `{sample}`/`{group}` (E014), need `checkpoint_manifest` (E013), and
    re-entry is capped at 32 rounds. Missing/unparsable manifest fails the
    rule. `[docs: workflow-format.md]`
25. **`temporary = true` deletes outputs only after a fully successful
    run**, tombstone-aware (a plain re-run does NOT regenerate them; only a
    dependent needing them triggers lazy cascade-up). Failed runs keep
    outputs. Leaf rules keep outputs. `[docs: commands/run.md]`
26. **`when`-false rules are skipped, not dropped** — they stay in the DAG
    with `JobStatus::Skipped` ("condition evaluated to false") [V].
27. **Output verification counts sizes** — run summary prints
    `✓ N output files verified (X MB total)` [V]; CI failures show up as
    rule failures with exit code 1.
28. **Version pinning must survive the port.** Container tags carry the
    `--<build>` suffix; conda pins use `tool=version`. Copy both verbatim
    (§5). `[V]` for syntax acceptance; policy is §5.
29. **TOML triple-quoted string escapes.** In `"""..."""` strings: `\|` is an
    *invalid* TOML escape (parse error — double-escape as `\\|`); `\n`
    renders as a **real newline character** (printf format strings need
    `\\n` to keep the two characters); a trailing `\` at end of line triggers
    TOML line-continuation trimming — it joins the next line, which is
    semantically equivalent to the shell backslash-newline it replaced, so
    arg-continuation lines are safe as-is. Perl one-liners containing
    `{(...)}` survive engine expansion untouched. `[V]`
30. **`validate --as-include` still runs E005 config checks.** A fragment
    whose paths/shells reference `{config.*}` keys defined in the *including*
    file fails standalone `--as-include` validation ("undefined config
    variable"). When `[config]` lives in `main.oxoflow`, do not add fragment
    validation to `test/run.sh` — validate the composed workflow only. `[V]`
31. **Directory outputs pass output verification.** The post-run check uses
    `path.exists()`, which is true for directories — Snakemake
    `directory(...)` outputs (rMATS `--od`, SplAdder `--outdir`, Voila
    `-d`) port as-is with the directory path as the declared output. `[V]`
32. **`-t` prefix targeting works across include namespaces.** With
    namespaced fragments (`alignment::*` / `as_calling::*`), `-t alignment`
    runs exactly the `alignment::*` rules; `-t as_calling` additionally
    pulls upstream producers (bams) but not sibling consumers of the same
    bams (verified: 17-rule port → `-t alignment` 5 rules, `-t as_calling`
    15). Use this to mirror multi-Snakefile upstreams in one DAG. `[V]`
33. **Fan-out trigger fields are `input`/`output`/`shell` only.** A
    placeholder appearing *exclusively* in `script`, `log`, `benchmark`,
    hooks, `params`, or `when` does NOT clone the rule — it stays a single
    instance with the literal placeholder in those fields (probe wf9:
    script-only `{sample}` → no fan-out). `script` strings ARE
    placeholder-expanded **at runtime** for the executing instance (the
    same `render_shell_command` renderer as `shell`), so
    `script = "scripts/x.py --sample {sample}"` works once a wildcard in
    input/output/shell clones the rule. `debug` output renders shell
    commands only — script commands are not shown; the script file is the
    fidelity-check source. `[V]`
34. **`output = []` is valid for script-only rules.** Rules with an empty
    output list and a `script` pass `validate`, appear in dry-run, and
    execute; nothing is verified on disk afterwards — the script exit code
    is the contract. Use for metadata-driven steps whose outputs are
    dynamic (e.g. per-SRR FASTQ dumps, §4.2). `[V]`
35. **`depends_on` on a template name resolves to ALL expanded instances.**
    `depends_on = ["data_conversion_pair"]` on a per-sample rule creates
    edges from every `data_conversion_pair_<group>_<sample>` instance (the
    engine builds an original-name → expanded-names map during
    `expand_wildcards`); for single-instance rules the name matches
    directly. `[V]`
36. **dry-run `input ✗` means "file absent on disk at preview time"** — it
    is NOT a missing-producer diagnostic. Producer-owned intermediates show
    `input ✗` too in a no-checkpoint dry-run (all reference ports do);
    files present on disk (fixtures) show **no marker at all**. The §14 DoD
    input check is therefore: no `✗` for files the run consumes from disk,
    and DAG wiring verified via the `Dependencies:` lines in `debug`. `[V]`
37. **`pairs_pattern` requires `{pair_id}`, `{experiment}`, AND `{control}`.**
    A pattern missing any of the three is rejected at config load
    ("pairs_pattern must contain {pair_id}, {experiment}, and {control}") —
    single-token discovery (e.g. `sra/{pair_id}/{pair_id}.sra` for SRR
    archives) is impossible; use the §4.2 script-rule pattern instead. `[V]`
38. **`[rules.resources]` numbers are literals — no `{config.x}`.**
    `threads` is `u32`; upstream config thread keys (`fastp_threads`,
    `star_threads`) must be baked into `[rules.resources] threads` with the
    upstream default and a fidelity-table note. Shared concurrency caps:
    declare `[resource_groups] limit_merge = { max = 2 }` (optional
    `wait = "queue"|"fail"`, default queue) and claim per rule
    `[rules.resources] groups = { limit_merge = 1 }`; undeclared-group or
    over-capacity claims fail fast (`ResourceGroupExhausted`). `[V]`
39. **`when` branches are workflow-level, not per-sample.** Snakemake input
    functions that route *per sample* by a metadata column (`paired` ==
    "PAIRED"/"SINGLE") cannot be replicated — `when` evaluates config only,
    and both branches cannot coexist (outputs collide). Port the branch the
    upstream example uses and record the other as not-ported with the
    reason (precedent: rnaseq-star-deseq2 `fastp_se`, auto_sra_rnaseq
    `data_conversion_single`). `[V]`
40. **Upstream without a license file** (GitHub reports "no license"): there
    is no `LICENSE.upstream` to copy — NOTICE.md states the absence
    explicitly (repo, ported commit, "ships no LICENSE file"), metadata.json
    uses `source.license = "none"` / `upstream_license = "none"`, and the
    README Source section says so. The port itself stays Apache-2.0.
    [workflow #23]

---

## 14. Definition of done

A port is DONE only when **all** of the following hold (checked before
submission):

- [ ] `oxo-flow validate main.oxoflow` exits 0 (CI-green locally with
      `OXO=/path/to/oxo-flow`).
- [ ] `./test/run.sh` passes locally and in CI (ubuntu-latest, §8) —
      validate + lint + dry-run with default config + no unexpanded
      wildcards in `debug` output.
- [ ] `oxo-flow dry-run main.oxoflow` shows the full plan with correct
      expansion: every per-sample/per-pair rule instance present, gather
      rules single-instance with full input lists, `input ✓` for every
      fixture file, no `input ✗` other than files intentionally provided at
      run time by the user.
- [ ] `oxo-flow debug main.oxoflow` output matches the upstream command
      logic (tool flags, orderings, file naming) after placeholder
      substitution.
- [ ] Fidelity table complete — every upstream branch, process and rule
      has a row; every deviation is explained; gaps carry a coverage tier
      (P0/P1/P2, §1); nothing silently dropped.
- [ ] No unpinned tools: no `latest` container tags, no unpinned conda
      deps; any upstream-unpinned tool is pinned at port time and flagged
      in the fidelity table (§5).
- [ ] Exactly one sample source on the default path (no §13.8
      double-fan-out).
- [ ] `README.md` (catalog v2 skeleton — §9: title without "port" framing,
      ★ Verified blockquote, Installation with engine + reference-data +
      compute + toolchain, Usage, fidelity table, Source with tag/commit +
      upstream license + created-2026-08-15 + may-lag sentence, Test,
      License, Community link).
- [ ] `NOTICE.md` present; `LICENSE` = full Apache-2.0 with
      "Copyright (c) 2026 oxo-flow-community"; `LICENSE.upstream` = the
      upstream license fetched from the upstream repo at the ported commit
      (§10, §11).
- [ ] `metadata.json` follows the registry v2 schema (§12): `origin =
      "port"`, `rating = "verified"` (only when every other DoD item
      holds), truthful `installation` block, `tools` without versions,
      valid JSON.
- [ ] `.github/workflows/ci.yml` present with the latest-tarball install
      (§8); CI is green with the badge URL resolving.
- [ ] No files written into the engine repo; all scratch work stayed
      under a throwaway directory.

---

## 15. Completeness audit (full-line coverage)

The porting mandate (§1) is full-line: every user-selectable upstream
branch is ported, absorbed as a `[config]` variant, or P1-triaged with
evidence. The completeness audit enforces it per repository, including
repos stamped before this section existed (their live-verified rating is
redefined as "default-path PASS + gap list" until the audit clears them).

Audit steps per repo:

1. Anchor: `metadata.json` `source.tag` pins the upstream commit. Enumerate
   the upstream's entry points and branches from its config/entry logic,
   README usage, and profile/test matrices — NOT from the port's README.
2. Diff: per-branch rule inventory (upstream) × port rules. Reuse the
   scope verifier (`verify-upstream.py`) for name-level matching.
3. Tier every gap: P0 portable (must port), P1 objective blocker (license /
   paid data / unavailable reference — record the evidence), P2 config
   variant (absorb as config keys).
4. Update `metadata.json`: `coverage` (`full-line` only when no P0 gaps),
   `excluded` rows carry tier + reason.
5. Site registry mirrors the fields; the card shows
   `✔ Live-tested · full-line` / `· default-path` next to the rating.

Fill order: P0 gaps first (they are porting work — new rules, new envs),
then P2 absorption, P1 documentation. A repo with P0 gaps stays
`default-path` even if its main path is live-verified.

---

## Appendix A. Verification record (2026-08-15, oxo-flow 0.11.0)

Everything marked `[V]` above was reproduced in a throwaway scratch directory
with a ≥ 0.11.0 binary. Summary of
the runs:

| Scratch workflow | Verified |
|---|---|
| wf1 | `sample_pattern` discovery ("Auto-discovered 2 samples"), docker/singularity/conda env syntax accepted, `[defaults]` vs `[rules.resources]` precedence in dry-run (threads=2 default vs 4 override), debug `-r` instance-name requirement, docker wrapper command shape, positional config overrides (`greeting=hi threshold=42` → output "hi 42") |
| wf2 | Exact-string DAG edges (glob/dir inputs form no edges; consumer raced producer and failed), output parent-dir auto-creation, runtime glob/dir input behavior with `depends_on` fix, `threads=1` sentinel, missing-input warnings in validate + `input ✗` in dry-run, validate skips warnings for producer-owned files |
| wf3 | `[[pairs]]` fan-out (`pair_rule_CASE_001`), `[[sample_groups]]` fan-out (`group_rule_cohort_S1`), **absence of `config.pairs_list`** (literal `variants/config.pairs_list.vcf`) |
| wf4 | E003 (wildcard in output not in input without pair source), transform split→map→combine expansion (chunk paths `.oxo-flow/chunks/chr/chr1.g.vcf.gz`, combine command), config-array-driven `expand_inputs` gather across pairs, `config.samples_list` gather |
| wf5 | `[[include]]` + namespace (`qc::fastqc_cohort_S1`), cross-file `depends_on = ["qc::trim"]`, fragment `validate --as-include`, profile fill-in-only merge |
| wf6 | `{config.x}` inside `sample_pattern`, `cleanup_chunks` silently ignored, `config.samples_list` comma-joined in shell, auto-discovered + group double fan-out |
| wf7 | Config comma-splitting + single-element-array escape hatch, `lint` warning codes (W004/W007/W008), `lint --strict` exit 1 |
| wf8 | Checkpoint: run→skip on re-run ("0 succeeded, 2 skipped"), dry-run `[skip: up to date]`, `touch` does not invalidate, content change invalidates (`[run: input changed]`) |
| wf9 | Fan-out triggered by input/output/shell only (script-only `{sample}` stays single-instance), `output = []` accepted, `depends_on` template→all-instances, `expand_inputs` + `config.samples_list` gather, script placeholder expansion at runtime (`render_shell_command`), `[resource_groups]`/`groups` claim syntax |
| oxo-flow-tcasia (live port, #24) | `{log}` metadata-only (literal in shell, must inline path), TOML triple-quote escape semantics (§13.29), `--as-include` E005 on main-file config, directory outputs via `path.exists()`, `-t` namespace targeting (§13.32), namespaced two-stage DAG chaining |
| oxo-flow-auto-sra-rnaseq-pipeline (live port, #23) | `{sra}`-style custom wildcards → single-instance no-output script rules (§4.2, §13.34), template-name `depends_on` (§13.35), `pairs_pattern` three-wildcard constraint (§13.37), resource-group cap port (limit_dump→worker pool, limit_merge→`[resource_groups]`), no-license upstream handling (§13.40) |

## Appendix B. Doc citations

- Format authority: `docs/guide/src/reference/workflow-format.md` (all rule
  fields, config forms, pairs/groups, transform, include, checkpoint
  re-entry), `wildcards.md` (fan-out vs fan-in, expand_inputs), `dag-engine.md`
  (edge inference, collisions), `environment-system.md` +
  `execution-backends.md` (backends, setup commands), `glossary.md`.
- Commands: `docs/guide/src/commands/validate.md`, `dry-run.md`, `run.md`,
  `debug.md`, `lint.md`, `graph.md`, `schema.md`.
- Gallery (canonical TOML): `examples/gallery/{01_hello_world,
  02_file_pipeline,03_parallel_samples,04_scatter_gather,05_conda_environments,
  06_rnaseq_quantification,07_wgs_germline,08_multiomics_integration,
  09_single_cell_rnaseq,10_transform_operator,11_conditional_workflow,
  12_cohort_analysis,13_simple_variant_calling,14_paired_experiment_control,
  15_paired_experiment_control_pairs,16_16s_qiime2_amplicon}.oxoflow`;
  docs at `docs/guide/src/gallery/*.md`.
- CLI embedded gallery: `crates/oxo-flow-cli/src/commands/project.rs`
  (`EMBEDDED_GALLERY`, mirror in `crates/oxo-flow-cli/templates/`,
  drift-guarded).
- License: the engine repo `LICENSE` (Apache-2.0,
  "Copyright 2025 Traitome"; no NOTICE file exists in the repo).
