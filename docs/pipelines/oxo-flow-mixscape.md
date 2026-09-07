---
title: "Pooled CRISPR perturbation analysis with Seurat Mixscape"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-mixscape</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Pooled CRISPR perturbation analysis with Seurat Mixscape</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · full-line</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">crispr</span><span class="ox-tag">scrna-seq</span><span class="ox-tag">mixscape</span><span class="ox-tag">perturbation</span><span class="ox-tag">seurat</span><span class="ox-tag">snakemake</span></div>
<p class="ox-desc">Pooled CRISPR perturbation analysis (scCRISPR-seq / CROP-seq / Perturb-seq) with Seurat Mixscape: per-cell perturbation signatures (CalcPerturbSig), perturbed vs. non-perturbed classification (RunMixscape), LDA + UMAP projection of the perturbed subset, the full visualization suite (classification statistics, perturbation-score density, posterior-probability and optional antibody-expression violin plots), and reproducibility exports (exact conda envs, runtime config, annotation file). Input is one processed Seurat object per sample.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-mixscape" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · full-line</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">7</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v"><span title="mixscape 8 CPUs / 32 GB; lda, visualize 1 CPU / 32 GB each; export rules 1 CPU / 1 GB">mixscape 8 CPUs / 32 GB; lda, visualize 1 CPU / 32 GB each; e…</span></span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">single-cell</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/epigen/mixscape_seurat">epigen/mixscape_seurat</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v2.0.3</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2295.1"><code>10.48546/workflowhub.workflow.2295.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">Seurat</span><span class="tchip">seuratobject</span><span class="tchip">irlba</span><span class="tchip">matrix</span><span class="tchip">mixtools</span><span class="tchip">ggplot2</span><span class="tchip">scales</span><span class="tchip">patchwork</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-mixscape</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Pooled CRISPR perturbation pipeline</strong> (Seurat Mixscape): given one processed Seurat object per sample of pooled CRISPR data (scCRISPR-seq / CROP-seq / Perturb-seq), it classifies perturbed cells and delivers perturbation signatures, LDA and UMAP projections, classification statistics, and reproducibility exports.</p>
<p><strong>1. Input preparation</strong> — the run reads a processed Seurat RDS object per sample (driven by the cohort sample group) plus the annotation CSV mapping gRNA calls to samples; every analysis rule expands over the per-sample wildcard.</p>
<p><strong>2. Perturbation classification</strong> — <code>mixscape</code> computes perturbation signatures with CalcPerturbSig, classifies perturbed cells with RunMixscape, and plots classification statistics. Its full object and metadata feed both downstream branches.</p>
<p><strong>3. Downstream analysis (two parallel branches)</strong> — the <code>mixscape</code> output has two independent consumers. <code>lda</code> runs MixscapeLDA on perturbed plus non-targeting cells and produces a 2-D UMAP projection with filtered object and data matrices; <code>visualize</code> plots perturbation-score densities, posterior-probability violins, and optional antibody expression. With no edge between them, each runs once classification completes.</p>
<p><strong>4. Reproducibility exports (independent of the analysis)</strong> — four standalone rules record how the run was made without consuming any analysis output: <code>annot_export</code> copies the annotation into the results, <code>config_export</code> writes the runtime configuration as YAML, and <code>env_export_mixscape</code> / <code>env_export_lda</code> export the exact conda environments behind each analysis stage (split from the upstream environment export because environments cannot be wildcarded).</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-mixscape+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-mixscape
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-mixscape` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-mixscape@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-mixscape` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Point `data_dir=` and `annotation=` at your inputs (see README); the shipped fixtures preview the plan.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned (r-seurat 4.4.0, r-seuratobject 4.1.4, r-irlba 2.3.5.1, r-matrix, r-mixtools 2.0.0, r-ggplot2 3.5.2, r-scales 1.3.0, r-patchwork 1.2.0, r-data.table 1.14.10, pyyaml 6.0.1); conda/mamba required at runtime, conda binary on PATH for env export

**Requirements.**

- One processed Seurat object per sample, as {data_dir}/{sample}.rds (already normalized/integrated — QC/normalization run upstream)
- Annotation CSV (name, data columns) mapping sample names to object paths
- Optional: 10X Antibody_Capture assay 'AB' for antibody-expression violin plots
- Compute: mixscape up to 8 CPUs / 32000 MB (32 GB); lda, visualize 1 CPU / 32 GB each; export rules 1 CPU / 1 GB; -j controls parallelism

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli
#    NOTE: bioconda currently ships 0.10.2, older than the >= 0.12.0
#    minimum of every catalog entry — prefer the release binary.

# 2. get this workflow (clones the repo, auto-discovers the workflow,
#    sanity-parses it with the engine)
oxo-flow pull gh:oxo-flow-community/oxo-flow-mixscape
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-mixscape
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy annotation = value" data-copy="annotation = test/fixtures/annotation.csv">annotation</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/annotation.csv</code></td>
<td class="ox-p-desc">GENERAL<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy antibody_capture = value" data-copy="antibody_capture = ">antibody_capture</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">VISUALIZATION<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy assay = value" data-copy="assay = SCT">assay</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>SCT</code></td>
<td class="ox-p-desc">assay to analyse (&quot;SCT&quot; or &quot;RNA&quot;) — upstream default &quot;SCT&quot;<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cps_split_by_col = value" data-copy="cps_split_by_col = ">cps_split_by_col</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">CalcPerturbSig (upstream nested keys flattened; values identical)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy data_dir = value" data-copy="data_dir = test/fixtures/data">data_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/data</code></td>
<td class="ox-p-desc">per-sample Seurat .rds inputs: {data_dir}/{sample}.rds<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fine_mode = value" data-copy="fine_mode = FALSE">fine_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>FALSE</code></td>
<td class="ox-p-desc">RunMixscape (flattened)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gene_col = value" data-copy="gene_col = KOcall">gene_col</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>KOcall</code></td>
<td class="ox-p-desc">CalcPerturbSig (upstream nested keys flattened; values identical)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy grna_col = value" data-copy="grna_col = gRNAcall">grna_col</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>gRNAcall</code></td>
<td class="ox-p-desc">CalcPerturbSig (upstream nested keys flattened; values identical)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy grna_split_symbol = value" data-copy="grna_split_symbol = -">grna_split_symbol</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>-</code></td>
<td class="ox-p-desc">MIXSCAPE<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy lda_npcs = value" data-copy="lda_npcs = 10">lda_npcs</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>10</code></td>
<td class="ox-p-desc">LDA<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy lfc_th = value" data-copy="lfc_th = 0.1">lfc_th</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>0.1</code></td>
<td class="ox-p-desc">RunMixscape (flattened)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mem = value" data-copy="mem = 32000">mem</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>32000</code></td>
<td class="ox-p-desc">RESOURCES (upstream config/config.yaml)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_cells = value" data-copy="min_cells = 5">min_cells</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">RunMixscape (flattened)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_de_genes = value" data-copy="min_de_genes = 5">min_de_genes</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">RunMixscape (flattened)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mixscape_split_by_col = value" data-copy="mixscape_split_by_col = ">mixscape_split_by_col</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">RunMixscape (flattened)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy n_neighbors = value" data-copy="n_neighbors = 30">n_neighbors</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>30</code></td>
<td class="ox-p-desc">CalcPerturbSig (upstream nested keys flattened; values identical)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ndims = value" data-copy="ndims = 40">ndims</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>40</code></td>
<td class="ox-p-desc">CalcPerturbSig (upstream nested keys flattened; values identical)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nt_term = value" data-copy="nt_term = NonTargeting">nt_term</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>NonTargeting</code></td>
<td class="ox-p-desc">CalcPerturbSig (upstream nested keys flattened; values identical)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy project_name = value" data-copy="project_name = myCROPseq">project_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>myCROPseq</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy prtb_type = value" data-copy="prtb_type = KO">prtb_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>KO</code></td>
<td class="ox-p-desc">RunMixscape (flattened)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy result_path = value" data-copy="result_path = results">result_path</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">upstream result_path; results land under result_path/mixscape_seurat<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy threads = value" data-copy="threads = 1">threads</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">upstream threads; mixscape rule runs 8x<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy variable_features_only = value" data-copy="variable_features_only = 0">variable_features_only</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">(objects carry SCTransform normalization; the bundled fixtures<br>are generated that way via make_fixtures.R)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-mixscape.svg?v=8f9a0a18df" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-mixscape.svg?v=8f9a0a18df" alt="oxo-flow-mixscape pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-mixscape — Pooled CRISPR perturbation analysis (scCRISPR-seq / CROP-seq / Perturb-seq) with Seurat Mixscape: per-cell perturbation signatures (CalcPerturbSig), perturbed vs.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- mixscape
- lda
- visualize
- env_export_mixscape
- env_export_lda
- config_export
- annot_export

**Excluded**

- none

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- demultiplexing — verified at v2.0.3 (sha bcf72d5): no demultiplexing rule in the repo — the Snakefile includes only common/mixscape/visualize/envs_export (DAG rulegraph: 7 rules); upstream README §Resources delegates pre-processing to the separate epigen/scrnaseq_processing_seurat module
- scdna — verified at v2.0.3 (sha bcf72d5): zero references anywhere in the repo; single-cell DNA is a different MrBiomics recipe domain, not a mixscape_seurat module
- normalization — verified at v2.0.3 (sha bcf72d5): no QC/normalization/integration rule; the input contract is a processed Seurat object (upstream delegates processing to epigen/scrnaseq_processing_seurat). The in-script NormalizeData fallbacks inside mixscape.R/visualize.R ARE ported
- differential_test — verified at v2.0.3 (sha bcf72d5): no DE rule; per-gene DE runs inside Seurat::RunMixscape (config min_de_genes/lfc_th, both ported); separate downstream DE module is epigen/dea_seurat

## Fidelity


Default-parameters main execution path only. The upstream annotation CSV maps
each sample name to the path of its processed Seurat object; the port reads
the same per-sample `.rds` inputs from `{config.data_dir}/{sample}.rds` and
writes all results under `{config.result_path}/mixscape_seurat/` with the
upstream file names.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `mixscape` | `mixscape` | Seurat 4.4.0 (r-seurat) | identical R script logic (CalcPerturbSig, RunMixscape, stats plots, ALL_* outputs); `snakemake@` I/O/config access replaced with CLI args. Threads 8 = upstream `8 * threads` (threads=1), mem 32000 MB. |
| `lda` | `lda` | Seurat 4.4.0 (r-seurat) | identical R script logic (MixscapeLDA, RunUMAP, FILTERED_*/LDA_data outputs). |
| `visualize` | `visualize` | Seurat 4.4.0 (r-seurat) | identical R script logic (PerturbScore, PosteriorProbability, optional `{Antibody_Capture}_expression` violin plots). The antibody-expression plot dir is produced by the script (same guard as upstream) but is not a declared rule output — oxo-flow cannot declare conditionally-enabled outputs. |
| `env_export` | `env_export_mixscape`, `env_export_lda` | conda (user's install) | upstream's single rule with an `{env}` wildcard split into two explicit rules (environments cannot be wildcarded); `conda env export > {output}` verbatim. `conda` itself is unpinned, exactly as upstream. |
| `config_export` | `config_export` | pyyaml 6.0.1 | upstream `run:` block (`yaml.dump(config)`) ported to `scripts/export_config.py`; runtime config values passed as CLI args. pyyaml pinned at port time (2026-08-15) — upstream relied on the unpinned Snakemake runtime env. |
| `annot_export` | `annot_export` | — | `cp {input} {output}` verbatim. |
| `all` (target) | — | — | not ported: oxo-flow's target is implicit (all rules are targets). |
| demultiplexing | — | — | not ported: not present at v2.0.3 — the Snakefile includes only `common`/`mixscape`/`visualize`/`envs_export` (DAG: 7 rules); pre-processing lives in the separate [epigen/scrnaseq_processing_seurat](https://github.com/epigen/scrnaseq_processing_seurat) module (upstream README §Resources). |
| scdna | — | — | not ported: not present at v2.0.3 (zero references in the repo); single-cell DNA is a separate MrBiomics recipe domain, not a mixscape_seurat module. |
| normalization (QC/normalization/integration) | — | — | not ported: no QC/normalization/integration rule at v2.0.3; the input is a processed Seurat object (upstream delegates processing to `scrnaseq_processing_seurat`). The in-script `NormalizeData` fallbacks (`mixscape.R`, `visualize.R`) are ported. |
| differential_test (perturbation DE) | — | — | not ported: no DE rule at v2.0.3; the per-gene DE runs inside `Seurat::RunMixscape` (`min_de_genes` / `lfc_th` config, both ported); the separate downstream DE module is [epigen/dea_seurat](https://github.com/epigen/dea_seurat). |

Other deviations: (1) sample input paths come from the `{config.data_dir}`
convention instead of per-row CSV paths — the annotation CSV is retained as
the reproducibility artifact (copied by `annot_export`); (2) the upstream
nested config keys (`CalcPerturbSig.*`, `RunMixscape.*`, `MixscapeLDA.npcs`,
`Antibody_Capture`) are flattened in `[config]` — values identical; defaults
identical except `antibody_capture` (port default `""` = disabled, because the
bundled fixtures carry no CITE-seq assay; upstream default `"AB"` — set
`antibody_capture = "AB"` for the upstream behavior); (3) `test/fixtures/*.rds` are tiny genuine Seurat objects generated
with Seurat 5.4.0 (local toolchain) for dry-run validation only — upstream
pins r-seurat 4.4.0; (4) the `snakemake@` object access in the R scripts is
replaced with positional CLI args (the ported scripts document the arg
order); (5) a commented-out draft plotting block in upstream `mixscape.R`
was dropped.

## Links

- Repository: [oxo-flow-mixscape](https://github.com/oxo-flow-community/oxo-flow-mixscape)
- Upstream: [epigen/mixscape_seurat](https://github.com/epigen/mixscape_seurat) @ `v2.0.3`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
