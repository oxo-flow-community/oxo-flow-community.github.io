---
title: "Genome browser tracks: coverage, gene plots and UCSC hub"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-genome-tracks</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Genome browser tracks: coverage, gene plots and UCSC hub</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">epigenomics</span><span class="ox-tag">genome-tracks</span><span class="ox-tag">bigwig</span><span class="ox-tag">coverage</span><span class="ox-tag">visualization</span><span class="ox-tag">ucsc-hub</span><span class="ox-tag">deeptools</span><span class="ox-tag">pygenometracks</span><span class="ox-tag">snakemake</span><span class="ox-tag">single-cell</span><span class="ox-tag">sinto</span><span class="ox-tag">igv</span></div>
<p class="ox-desc">Merge BAM files per experimental group with samtools, compute normalized bigWig coverage with deepTools bamCoverage (RPGC by default), plot isoform-aware per-gene and per-region genome tracks with gtracks/pyGenomeTracks, and publish a UCSC genome browser track hub — end-to-end track generation for RNA-seq, ATAC-seq and other aligned BAM data, plus the single-cell branch (sinto per-cell-barcode splitting of sc BAMs into per-group BAMs), an opt-in IGV report of all merged BAMs over the annotated gene regions, and opt-in conda environment export rules (env_export_*, conda env export).</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-genome-tracks" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow --samples first:1</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">16</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 4 CPUs / 4 GB per rule (opt-in igv_report: 8 GB)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/epigen/genome_tracks">epigen/genome_tracks</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v2.0.5</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2294.1"><code>10.48546/workflowhub.workflow.2294.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">samtools</span><span class="tchip">deeptools</span><span class="tchip">pygenometracks</span><span class="tchip">gtracks</span><span class="tchip">sinto</span><span class="tchip">igv-reports</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-genome-tracks</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Genome browser track generation pipeline</strong>: given aligned BAMs, it merges sample groups, computes bigWig coverage, and renders genomic track plots plus a UCSC genome browser hub — with an optional single-cell split path and an opt-in IGV report.</p>
<p><strong>1. Inputs and documentation exports</strong> — <code>annot_export</code>, <code>gene_list_export</code>, and <code>config_export</code> copy the sample annotation, gene list, and workflow config into the results configs dir; <code>annotate_genes</code> extracts gene coordinates, isoform counts, and y-max from the gene list and the genome BED.</p>
<p><strong>2. Bulk coverage chain</strong> — <code>merge_bams</code> merges the BAMs of each annotation group with samtools and indexes the merged BAM; <code>coverage</code> generates one bigWig per group with bamCoverage.</p>
<p><strong>3. Single-cell chain (runtime-conditional)</strong> — when sc_enabled is set, <code>split_sc_bam</code> splits each single-cell BAM into per-group BAMs by cell barcode (sinto filterbarcodes), <code>merge_sc_bams</code> merges those splits, and <code>coverage_sc</code> yields the bigWig per sc group. Both routes write bigWigs into the same directory, which the plots and hub read by group name.</p>
<p><strong>4. Plotting and hub</strong> — <code>plot_tracks</code> renders gene/region track plots via gtracks and <code>ucsc_hub</code> assembles the hub files; both run after <code>coverage</code>, and <code>annotate_genes</code> feeds the plot directly.</p>
<p><strong>5. Opt-in reporting</strong> — with igv_report_enabled set, <code>make_bed</code> projects the annotated genes to BED4, then <code>igv_report</code> builds the self-contained HTML report over the merged BAMs; <code>env_export_pygenometracks</code>, <code>env_export_sinto</code>, and <code>env_export_igv_reports</code> export pinned conda environments when enabled.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-genome-tracks+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-genome-tracks --samples first:1
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-genome-tracks` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-genome-tracks@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-genome-tracks` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Lightweight; `--samples first:1` keeps the first run small.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned

**Requirements.**

- BAM files per group at <bam_dir>/<group>/*.bam (aligned/mapped data, e.g. RNA-seq or ATAC-seq; input BAMs need no index — merge_bams produces merged, indexed BAMs)
- sample annotation CSV with a group column (sample_annotation; group values drive merge/coverage/hub fan-out)
- gene list CSV with gene_region,ymax columns (gene_list; gene symbols or chr:start-end regions)
- 12-column genome BED for gene annotation (genome_bed, e.g. ref.bed.gz); no genome FASTA or annotation GTF required
- single-cell samples (optional): one CB-tagged BAM per sc sample at <sc_bam_dir>/<sc_id>.bam + a 2-column barcode TSV (barcode<TAB>group, no header) at <sc_metadata>/<sc_id>.tsv; group values of TSV col 2 must be declared in config.sc_groups and [[values]] sc_group
- compute: up to 4 CPUs / 4 GB per rule (samtools merge, bamCoverage and sinto filterbarcodes at threads=4/4000M); helper rules need 1 CPU / 1 GB; igv_report is fixed at the upstream 8000 MB minimum
- conda/mamba to build the pinned environments (samtools 1.19.2, deepTools 3.5.5, pyGenomeTracks 3.8, python 3.10.13, gtracks 1.12.6, sinto 0.10.0; igv-reports 1.14.1 / python 3.8 / pysam 0.22.0 for the opt-in IGV report); helper rules need only a system python3
- disk: results/ for merged BAMs, bigWigs, track plots, the UCSC hub and the IGV report

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-genome-tracks
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-genome-tracks
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bamCoverage_parameters = value" data-copy="bamCoverage_parameters = -p max --binSize 10  --normalizeUsing RPGC --effectiveGenomeSize 2407883318">bamCoverage_parameters</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>-p max --binSize 10  --normalizeUsing RPGC --effectiveGenomeSize 2407883318</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bam_dir = value" data-copy="bam_dir = test/fixtures/bams">bam_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/bams</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy base_buffer = value" data-copy="base_buffer = 2000">base_buffer</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>2000</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy email = value" data-copy="email = sreichl@cemm.at">email</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>sreichl@cemm.at</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy env_export_enabled = value" data-copy="env_export_enabled = false">env_export_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">export the built conda environments as results/genome_tracks/envs/*.yaml<br>(upstream &#x27;env_export&#x27; runs in rule all; the port keeps it opt-in so the<br>default graph is unchanged — the checked-in envs/*.yaml already document<br>the pinned versions; see README &quot;Fidelity&quot;)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy file_type = value" data-copy="file_type = pdf">file_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>pdf</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gene_list = value" data-copy="gene_list = test/fixtures/genes.csv">gene_list</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genes.csv</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genome = value" data-copy="genome = mm10">genome</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>mm10</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genome_bed = value" data-copy="genome_bed = test/fixtures/genome_bed/ref.bed.gz">genome_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/genome_bed/ref.bed.gz</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy igv_report_enabled = value" data-copy="igv_report_enabled = false">igv_report_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">IGV report (igv-reports), deactivated upstream (commented out of rule all)<br>— opt-in: set igv_report_enabled = true, then <code>-t igv_report</code>.<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy igv_report_memory = value" data-copy="igv_report_memory = 8000M">igv_report_memory</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>8000M</code></td>
<td class="ox-p-desc">upstream&#x27;s dynamic <code>max(2 * input.size_mb, 8000)</code> memory is not expressible<br>statically in oxo-flow — fixed at the upstream 8000 MB minimum<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy plot_enabled = value" data-copy="plot_enabled = true">plot_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">pair-level gtracks plots: needs gene-named bigWigs (upstream&#x27;s data<br>layout); set false for the generic-named mini fixtures.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy project_name = value" data-copy="project_name = myData">project_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>myData</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy result_path = value" data-copy="result_path = results">result_path</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>16</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sample_annotation = value" data-copy="sample_annotation = test/fixtures/annotation.csv">sample_annotation</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/annotation.csv</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sc_bam_dir = value" data-copy="sc_bam_dir = test/fixtures/sc_bams">sc_bam_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/sc_bams</code></td>
<td class="ox-p-desc">one aligned BAM per sc sample: {sc_bam_dir}/{sc_id}.bam (BAMs need a CB<br>cell-barcode tag per read, see test/fixtures/make_sc_fixtures.py)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sc_enabled = value" data-copy="sc_enabled = true">sc_enabled</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">Single-cell mode (upstream: any annotation &#x27;group&#x27; value ending in .tsv<br>switches that sample to sinto barcode splitting). oxo-flow cannot discover<br>groups from TSV contents at load time, so the sc samples, their BAM/metadata<br>paths and the sc groups are declared explicitly. Set sc_enabled = false if<br>you have no single-cell samples.<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sc_groups = value" data-copy="sc_groups = g1,g2">sc_groups</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>g1,g2</code></td>
<td class="ox-p-desc">unique group values of the sc metadata TSV col-2 (merged + sorted into<br>samples_list above)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sc_metadata = value" data-copy="sc_metadata = test/fixtures/sc_metadata">sc_metadata</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/sc_metadata</code></td>
<td class="ox-p-desc">one 2-column barcode TSV (barcode&lt;TAB&gt;group, no header) per sc sample:<br>{sc_metadata}/{sc_id}.tsv — the group values of col 2 become the sc groups<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy track_colors = value" data-copy="track_colors = untreated=#800080,treated=#00FFFF">track_colors</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>untreated=#800080,treated=#00FFFF</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy width = value" data-copy="width = 20">width</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>20</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy x_axis = value" data-copy="x_axis = bottom">x_axis</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>bottom</code></td>
<td class="ox-p-desc">upstream config/config.yaml defaults, adapted paths<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card ox-dag-card--wide" markdown="1">

<a href="/assets/dag/oxo-flow-genome-tracks.svg?v=0ea0380792" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-genome-tracks.svg?v=0ea0380792" alt="oxo-flow-genome-tracks pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-genome-tracks — Merge BAM files per experimental group with samtools, compute normalized bigWig coverage with deepTools bamCoverage (RPGC by default), plot isoform-aware per-gene and per-region genome tracks with gtracks/pyGenomeTracks, and publish a UCSC genome browser track hub — end-to-end track generation for RNA-seq, ATAC-seq and other aligned BAM data, plus the single-cell branch (sinto per-cell-barcode splitting of sc BAMs into per-group BAMs), an opt-in IGV report of all merged BAMs over the annotated gene regions, and opt-in conda environment export rules (env_export_*, conda env export).</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- merge_bams
- coverage
- annotate_genes
- plot_tracks
- ucsc_hub
- split_sc_bam
- merge_sc_bams
- coverage_sc
- make_bed
- igv_report
- annot_export
- gene_list_export
- config_export
- env_export_pygenometracks
- env_export_sinto
- env_export_igv_reports

**Excluded**

- none

## Fidelity

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `merge_bams` | `merge_bams` | samtools 1.19.2 | identical command (`samtools merge -@ N` + `samtools index -@ N -b`); the per-group BAM list comes from `{config.bam_dir}/{group}/*.bam` glob instead of the annotation CSV's `bam` column (which is still copied verbatim by `annot_export`); `threads: 4 × config.threads` baked in as `threads = 4` |
| `coverage` | `coverage` | deepTools 3.5.5 | identical command incl. `-p max --binSize 10 --normalizeUsing RPGC --effectiveGenomeSize 2407883318` default and `> {bw}.log 2>&1` redirect |
| Snakefile load-time gene annotation (`parse_gene`/`parse_region`, `gene_annot_df`) | `annotate_genes` | python3 (stdlib) | new single-instance rule; same algorithm (BED scan, min start / max end across isoforms, `base_buffer` extension for genes, no buffer for `chr:start-end` regions, `genes_not_found.csv`, `:`→`-` name replacement); upstream computes it in the Snakemake base env (numpy/pandas) — the port script uses only stdlib, so the upstream `global.yaml` env is not needed |
| `plot_tracks` | `plot_tracks` | gtracks 1.12.6, pyGenomeTracks 3.8 | identical `gtracks` invocation (coordinates, `--genes`, optional `--max ymax`, `--gene-rows`/`--genes-height` = isoform count, `--x-axis`, `--width`, `--color-palette` with `#000000` default); per-gene fan-out uses `[[pairs]]` `pair_id` (oxo-flow has no gene wildcard source); `depends_on = ["coverage"]` added because `expand_inputs` input lists do not form DAG edges in oxo-flow 0.12.0 |
| `ucsc_hub` | `ucsc_hub` | python3 (stdlib) | identical hub content (hub.txt, genomes.txt, trackDb.txt with hex→RGB colors, `../{group}.bw` relative symlinks) ported from the Python run block to `scripts/ucsc_hub.py`; the per-group symlinks are side effects (outputs declared only for the three text files) |
| `env_export` | `env_export_pygenometracks` / `env_export_sinto` / `env_export_igv_reports` | conda | upstream fans `{env}` over the three envs; oxo-flow cannot wildcard `[rules.environment]`, so one rule per env — identical `conda env export` shell, each rule exports its own activated env (the engine's `conda run -n <env>` wrapper + `conda env export` = the upstream semantics, verified live with conda 26.1.1). Upstream runs it in `rule all`; the port gates it on `env_export_enabled` (default off) so the default graph is unchanged — the checked-in `envs/*.yaml` serve the same reproducibility role. DRAFT (mechanics live-verified; the three real env builds not yet run) |
| `config_export` | `config_export` | python3 (stdlib) | `json.dump(config)` equivalent: `scripts/export_config.py` dumps the workflow's `[config]` table |
| `annot_export` | `annot_export` | cp | identical (`cp` of the annotation CSV) |
| `gene_list_export` | `gene_list_export` | cp | identical (`cp` of the gene list CSV) |
| `split_sc_bam` | `split_sc_bam` | sinto 0.10.0 | live-verified 2026-08-23 (tx-ubuntu, exit 0 — see the site audit): same `sinto filterbarcodes -b -c --outdir -p` command + upstream's touch-empty-bam fallback for groups absent in a sample (replaced by a header-only-BAM fallback for modern samtools); fan-out via `[[values]]` `sc_sample` × `sc_group` (upstream derives them from the metadata TSVs at load time; oxo-flow declares them — keep `[[values]] sc_sample`/`sc_group` in sync with `sc_bam_dir`/`sc_metadata`/`sc_groups`); upstream's `{sample}` = BAM-path md5 is replaced by readable sc ids |
| `merge_bams` (sc variant) | `merge_sc_bams` | samtools 1.19.2 | live-verified 2026-08-23: upstream switches `merge_bams` inputs per wildcard (sc groups read `sc_bams/`, bulk groups the annotation BAM column); oxo-flow cannot switch inputs per wildcard, so the sc variant is a separate rule writing the same `merged_bams/` namespace, gated on `sc_enabled` |
| `coverage` (sc variant) | `coverage_sc` | deepTools 3.5.5 | live-verified 2026-08-23: same `bamCoverage` command as bulk `coverage`; sc groups' bigWigs join `plot_tracks`/`ucsc_hub` via `config.samples_list` |
| `make_bed` | `make_bed` | awk | DRAFT: upstream projects `gene_annot_df` to `chr,start,end,name` in Python; the port uses an awk projection of `genes_annotated.tsv` (name,chr,start,end → BED4); gated on `igv_report_enabled` like the rule it feeds |
| `igv_report` | `igv_report` | igv-reports 1.14.1 | DRAFT: **temporarily deactivated upstream** (commented out of `rule all` at v2.0.5), ported as opt-in (`igv_report_enabled = true` + `-t igv_report`); same `create_report --genome --tracks --output` + the upstream `Variants`→`Genes and genomic regions` sed; track list = `config.samples_list` BAMs; memory fixed at the upstream 8000 MB minimum (oxo-flow resources are static) |
| Snakemake `report()` wrappers | — | — | no equivalent in oxo-flow; the report artifacts are written as plain files |

Configuration mapping: upstream `config/config.yaml` keys became `[config]`
keys with upstream defaults, except `result_path` (placeholder path →
`results`), `mem`/`threads` (→ per-rule `[rules.resources]`; upstream's
`4 × threads` for merge/coverage baked in as `threads = 4`), and
`track_colors` (YAML dict → comma-joined `group=#hex` string with the same
`#000000` default). New keys for the ported sc/IGV branches: `sc_enabled`,
`sc_bam_dir`, `sc_metadata` (directory keys — oxo-flow rule inputs cannot
index comma-joined config lists), `sc_groups` (merged + sorted into
`samples_list`), `igv_report_enabled`, `igv_report_memory` (documented mirror;
the rule's `memory` is the fixed upstream minimum), `env_export_enabled`
(opt-in, default off — upstream runs `env_export` in `rule all`; the checked-in
`envs/*.yaml` serve the same reproducibility role, so the port keeps the
default graph unchanged). Group fan-out uses
`[[sample_groups]]` (one `{sample}` per annotation group) + `[[values]]`
`sc_sample` × `sc_group`, gene fan-out uses `[[pairs]]`. Sample annotation,
gene list, genome BED, metadata TSVs and BAM files must be kept in sync with
those tables and `config.bam_dir`; the annotation CSV itself remains the
documentation record (`annot_export`).

## Links

- Repository: [oxo-flow-genome-tracks](https://github.com/oxo-flow-community/oxo-flow-genome-tracks)
- Upstream: [epigen/genome_tracks](https://github.com/epigen/genome_tracks) @ `v2.0.5`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
