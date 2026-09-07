---
title: "Amplicon sequencing (16S/ITS): DADA2 denoising, taxonomy assignment, QIIME2 diversity/ANCOM, PICRUSt, SBDI export, phyloseq/TSE objects and QC"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-ampliseq</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Amplicon sequencing (16S/ITS): DADA2 denoising, taxonomy assignment, QIIME2 diversity/ANCOM, PICRUSt, SBDI export, phyloseq/TSE objects and QC</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">amplicon</span><span class="ox-tag">16s</span><span class="ox-tag">its</span><span class="ox-tag">dada2</span><span class="ox-tag">qiime2</span><span class="ox-tag">picrust</span><span class="ox-tag">sbdi</span><span class="ox-tag">phyloseq</span><span class="ox-tag">nf-core</span></div>
<p class="ox-desc">Amplicon sequencing analysis (16S/ITS) that takes raw paired-end reads through FastQC quality control, cutadapt primer trimming (incl. the illumina_pe_its read-through pass), DADA2 denoising (quality profiles, filterAndTrim, learnErrors, denoise, chimera removal, read tracking, optional multi-run merge), taxonomy assignment against the SBDI-GTDB reference (or the ITS-cut length-filtered branch), a QIIME2 taxa barplot over sample metadata, optional QIIME2 downstream analyses (phylogenetic tree, alpha/beta diversity, abundance table exports, ANCOM/ANCOM-BC/ANCOM-BC2, classifier training/prediction), optional PICRUSt2 functional predictions, an overall summary table and a MultiQC report. Optional post-analysis branches cover the SBDI Sweden biodiversity submission export (event/dna/emof/asv-table/annotation tables), phyloseq and TreeSummarizedExperiment R objects, and an Rmd-based HTML summary report (results/summary_report/summary_report.html) that aggregates QC plots, DADA2 stats, taxonomy references and the optional branch artifacts into one self-contained document.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-ampliseq" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">49</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 10 CPUs / 20 GB per rule (DADA2 rules; qiime2_preptax/qiime2_classify 10c/20G, 24h limits); picrust 10 CPUs / 50 GB / 24h; QIIME2 rules need the qiime2 container (~20GB unpacked)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">amplicon</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/ampliseq">nf-core/ampliseq</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>2.18.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2282.1"><code>10.48546/workflowhub.workflow.2282.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">fastqc</span><span class="tchip">cutadapt</span><span class="tchip">python</span><span class="tchip">pandas</span><span class="tchip">r-base</span><span class="tchip">dada2</span><span class="tchip">bioconductor-digest</span><span class="tchip">bioconductor-biostrings</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-ampliseq</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Amplicon sequencing pipeline</strong> (16S/ITS): given raw paired-end reads, it renames, quality-checks, and trims them, denoises with DADA2 into ASVs, assigns taxonomy, and produces QIIME2 taxa barplots, diversity, and differential-abundance results.</p>
<p><strong>1. Input preparation</strong> — <code>rename_raw_data_files</code> gives samples consistent FASTQ names; <code>fastqc</code> checks the renamed reads while <code>cutadapt</code> trims primers.</p>
<p><strong>2. Trimming and truncation</strong> — <code>cutadapt_summary</code> collects and <code>cutadapt_summary_merge</code> merges cutadapt trimming metrics. On trimmed reads, <code>dada2_quality_fw</code>/<code>dada2_quality_rv</code> quality profiles inform truncation lengths (<code>trunclen_fw</code>, <code>trunclen_rv</code>) applied by <code>dada2_filtntrim</code>.</p>
<p><strong>3. DADA2 denoising</strong> — <code>dada2_err</code> learns error models, <code>dada2_denoising</code> denoises and merges pairs, <code>dada2_rmchimera</code> removes bimeras; <code>dada2_stats</code> tracks reads per sample and <code>dada2_merge</code> publishes the ASV table, fasta, RDS.</p>
<p><strong>4. ITS branch</strong> — in ITS runs, <code>itsx_cutasv</code> and <code>itsxrust_cutasv</code> are alternative ITS extractors (runtime-conditional); both feed <code>filter_len_itsx</code>, length-filtering ITS-cut ASVs.</p>
<p><strong>5. Taxonomy</strong> — <code>download_taxonomy_db</code> fetches the SBDI-GTDB reference, <code>format_taxonomy</code> reformats it; <code>dada2_taxonomy</code> assigns 16S taxonomy while <code>dada2_taxonomy_its</code> maps taxonomy back to full ASVs.</p>
<p><strong>6. QIIME2 analysis</strong> — <code>qiime2_inasv</code>/<code>qiime2_inseq</code> import ASV tables and sequences, ITS via <code>qiime2_inasv_its</code>/<code>qiime2_inseq_its</code>, and taxonomy via <code>qiime2_intax</code>. Sequences feed <code>qiime2_diversity_tree</code> and <code>qiime2_classify</code>; <code>qiime2_diversity_core</code> precedes <code>qiime2_diversity_alpha</code>, <code>qiime2_diversity_beta</code>, <code>qiime2_diversity_betaord</code>; <code>qiime2_barplot</code> renders taxa barplots; exports (<code>qiime2_export_absolute</code>, <code>qiime2_export_relasv</code>, <code>qiime2_export_reltax</code>) and ANCOM tests (<code>qiime2_ancom</code>, <code>qiime2_ancombc</code>, <code>qiime2_ancombc2</code>, using <code>qiime2_metadata_categories</code>) complete the output.</p>
<p><strong>7. Reporting</strong> — <code>merge_stats</code> merges cutadapt and DADA2 statistics, <code>multiqc</code> aggregates FastQC and cutadapt reports, and <code>picrust</code> runs PICRUSt2 predictions from the ASV table.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-ampliseq+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-ampliseq
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-ampliseq` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-ampliseq@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-ampliseq` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Default config runs the DADA2 path (denoising, taxonomy against the auto-downloaded SBDI-GTDB reference, read-tracking summary, MultiQC); the QIIME2 (barplot + downstream diversity/ANCOM/classifier), ITS, multi-run and PICRUSt branches are opt-in toggles — see Fidelity. Preview with `oxo-flow dry-run main.oxoflow`.

## Installation

**Engine.** oxo-flow >= 0.17.0

**Toolchain.** containers (Docker/Singularity) — pinned images

**Requirements.**

- raw paired-end FASTQ reads per sample (raw/<sample>_R1.fastq.gz / _R2.fastq.gz) plus a sample groups file (default test/fixtures/groups.tsv)
- sample metadata TSV for the QIIME2 analyses (config metadata_file, default test/fixtures/metadata.tsv); the SBDI-GTDB taxonomy reference database is downloaded automatically
- compute: up to 10 CPUs / 20 GB per rule (dada2_denoising with 48h limit, dada2_taxonomy/dada2_taxonomy_its/qiime2_preptax/qiime2_classify with 24h limits); the QIIME2 rules need the qiime2 container (~20GB unpacked), picrust needs 10 CPUs / 50 GB
- host: Docker or Singularity to run the pinned container images, curl for the taxonomy-database download rule, and network access to figshare / data.qiime2.org
- optional: disk for intermediates/ and results/ plus the auto-downloaded SBDI-GTDB reference database and SILVA classifier inputs

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-ampliseq
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-ampliseq
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy FW_primer = value" data-copy="FW_primer = ">FW_primer</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">--- primers (upstream default null renders literal &quot;null&quot; adapters;<br>port uses empty strings — see README fidelity table) ---<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy RV_primer = value" data-copy="RV_primer = ">RV_primer</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">--- primers (upstream default null renders literal &quot;null&quot; adapters;<br>port uses empty strings — see README fidelity table) ---<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ancom = value" data-copy="ancom = false">ancom</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ancombc = value" data-copy="ancombc = false">ancombc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ancombc2 = value" data-copy="ancombc2 = false">ancombc2</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ancombc2_formula = value" data-copy="ancombc2_formula = ">ancombc2_formula</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ancombc_effect_size = value" data-copy="ancombc_effect_size = 1">ancombc_effect_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ancombc_formula = value" data-copy="ancombc_formula = ">ancombc_formula</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">comma-separated formulas<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ancombc_significance = value" data-copy="ancombc_significance = 0.05">ancombc_significance</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.05</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy classifier = value" data-copy="classifier = ">classifier</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">--- QIIME2 taxonomy classifier (upstream params.qiime_ref_taxonomy /<br>params.classifier — off by default; DADA2 taxonomy is the<br>default path). qiime_ref_taxonomy trains a Naive-Bayes<br>classifier on the primer-extracted reference below; classifier<br>is a path to a pre-trained .qza (skips training). ---<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cut_its = value" data-copy="cut_its = none">cut_its</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>none</code></td>
<td class="ox-p-desc">truncation (truncLen=0) + a second cutadapt<br>read-through pass removing revcomp primers<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cutadapt_max_error_rate = value" data-copy="cutadapt_max_error_rate = 0.1">cutadapt_max_error_rate</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.1</code></td>
<td class="ox-p-desc">cutadapt<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cutadapt_min_overlap = value" data-copy="cutadapt_min_overlap = 3">cutadapt_min_overlap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>3</code></td>
<td class="ox-p-desc">cutadapt<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_addspecies_allowmultiple = value" data-copy="dada_addspecies_allowmultiple = false">dada_addspecies_allowmultiple</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_assign_chunksize = value" data-copy="dada_assign_chunksize = 10000">dada_assign_chunksize</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10000</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_assign_taxlevels = value" data-copy="dada_assign_taxlevels = Domain,Kingdom,Phylum,Class,Order,Family,Genus,Species">dada_assign_taxlevels</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Domain,Kingdom,Phylum,Class,Order,Family,Genus,Species</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_min_boot = value" data-copy="dada_min_boot = 50">dada_min_boot</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>50</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_ref_taxonomy = value" data-copy="dada_ref_taxonomy = sbdi-gtdb=R11-RS232-1">dada_ref_taxonomy</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>sbdi-gtdb=R11-RS232-1</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_ref_taxonomy_citation = value" data-copy="dada_ref_taxonomy_citation = Lundin D, Andersson A. SBDI Sativa curated 16S GTDB database. FigShare. doi: 10.17044/scilifelab.14869077.v12">dada_ref_taxonomy_citation</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Lundin D, Andersson A. SBDI Sativa curated 16S GTDB database. FigShare. doi: 10.17044/scilifelab.14869077.v12</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_ref_taxonomy_dbversion = value" data-copy="dada_ref_taxonomy_dbversion = SBDI-GTDB-R11-RS232-1 (https://figshare.scilifelab.se/articles/dataset/SBDI_Sativa_curated_16S_GTDB_database/14869077/10)">dada_ref_taxonomy_dbversion</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>SBDI-GTDB-R11-RS232-1 (https://figshare.scilifelab.se/articles/dataset/SBDI_Sativa_curated_16S_GTDB_database/14869077/10)</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_ref_taxonomy_title = value" data-copy="dada_ref_taxonomy_title = SBDI-GTDB - Sativa curated 16S GTDB database - Release R11-RS232-1">dada_ref_taxonomy_title</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>SBDI-GTDB - Sativa curated 16S GTDB database - Release R11-RS232-1</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_ref_taxonomy_urls = value" data-copy="dada_ref_taxonomy_urls = https://ndownloader.figshare.com/files/64711203,https://ndownloader.figshare.com/files/64711218">dada_ref_taxonomy_urls</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>https://ndownloader.figshare.com/files/64711203,https://ndownloader.figshare.com/files/64711218</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dada_taxonomy_rc = value" data-copy="dada_taxonomy_rc = false">dada_taxonomy_rc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">DADA2 taxonomy assignment<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy diversity_rarefaction_depth = value" data-copy="diversity_rarefaction_depth = 500">diversity_rarefaction_depth</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>500</code></td>
<td class="ox-p-desc">floor for core-metrics depth<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy illumina_pe_its = value" data-copy="illumina_pe_its = false">illumina_pe_its</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">--- ITS branch (upstream params.illumina_pe_its / cut_its /<br>its_partial / its_extractor — all default off -&gt; 16S path) ---<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy its_extractor = value" data-copy="its_extractor = itsx">its_extractor</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>itsx</code></td>
<td class="ox-p-desc">&quot;itsx&quot; | &quot;itsxrust&quot;<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy its_partial = value" data-copy="its_partial = 0">its_partial</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">keep partial ITS hits (ITSx --partial N)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy max_ee = value" data-copy="max_ee = 2">max_ee</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy max_len = value" data-copy="max_len = Inf">max_len</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Inf</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy merge_runs = value" data-copy="merge_runs = false">merge_runs</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">--- multi-run merge (upstream DADA2_MERGE globs *.stats.tsv /<br>*.ASVtable.rds when several --run_ids are given) ---<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mergepairs_strategy = value" data-copy="mergepairs_strategy = merge">mergepairs_strategy</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>merge</code></td>
<td class="ox-p-desc">&quot;merge&quot; | &quot;consensus&quot; | &quot;concatenate&quot;<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy metadata_file = value" data-copy="metadata_file = test/fixtures/metadata.tsv">metadata_file</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/metadata.tsv</code></td>
<td class="ox-p-desc">run / metadata<br><span class="ox-param-usedby">used by <code>11</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_len = value" data-copy="min_len = 50">min_len</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>50</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy picrust = value" data-copy="picrust = false">picrust</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">picrust (upstream params.picrust, default false)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qiime_adonis_formula = value" data-copy="qiime_adonis_formula = ">qiime_adonis_formula</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">comma-separated, e.g. &quot;group&quot;<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qiime_ref_taxonomy = value" data-copy="qiime_ref_taxonomy = ">qiime_ref_taxonomy</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">--- QIIME2 taxonomy classifier (upstream params.qiime_ref_taxonomy /<br>params.classifier — off by default; DADA2 taxonomy is the<br>default path). qiime_ref_taxonomy trains a Naive-Bayes<br>classifier on the primer-extracted reference below; classifier<br>is a path to a pre-trained .qza (skips training). ---<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy qiime_ref_taxonomy_urls = value" data-copy="qiime_ref_taxonomy_urls = https://data.qiime2.org/2023.7/common/silva-138-99-seqs.qza,https://data.qiime2.org/2023.7/common/silva-138-99-tax.qza">qiime_ref_taxonomy_urls</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>https://data.qiime2.org/2023.7/common/silva-138-99-seqs.qza,https://data.qiime2.org/2023.7/common/silva-138-99-tax.qza</code></td>
<td class="ox-p-desc">--- QIIME2 taxonomy classifier (upstream params.qiime_ref_taxonomy /<br>params.classifier — off by default; DADA2 taxonomy is the<br>default path). qiime_ref_taxonomy trains a Naive-Bayes<br>classifier on the primer-extracted reference below; classifier<br>is a path to a pre-trained .qza (skips training). ---<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy quality_type = value" data-copy="quality_type = Auto">quality_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>Auto</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_id = value" data-copy="run_id = 1">run_id</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">run / metadata<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_qiime2 = value" data-copy="run_qiime2 = false">run_qiime2</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">the four qiime2 rules run in the quay.io/qiime2/amplicon container<br>(~20GB unpacked — needs ~25GB free disk for the pull; there is no<br>conda qiime2 on common mirrors). Upstream runs qiime2 always; the<br>port gates it (default false) so a fresh clone completes the DADA2<br>analysis without the container. Set true (with the disk) to enable.<br><span class="ox-param-usedby">used by <code>22</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sample_inference = value" data-copy="sample_inference = independent">sample_inference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>independent</code></td>
<td class="ox-p-desc">&quot;independent&quot; | &quot;pooled&quot; | &quot;pseudo&quot;<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy seed = value" data-copy="seed = 100">seed</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_abundance_tables = value" data-copy="skip_abundance_tables = false">skip_abundance_tables</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">feature-table exports (abs/rel)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_alpha_rarefaction = value" data-copy="skip_alpha_rarefaction = false">skip_alpha_rarefaction</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip alpha rarefaction (upstream --skip_alpha_rarefaction) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_barplot = value" data-copy="skip_barplot = false">skip_barplot</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skip flags (upstream params.skip_*, all default false -&gt; full default path)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_dada_taxonomy = value" data-copy="skip_dada_taxonomy = false">skip_dada_taxonomy</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skip flags (upstream params.skip_*, all default false -&gt; full default path)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_diversity_indices = value" data-copy="skip_diversity_indices = false">skip_diversity_indices</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip diversity indices (upstream --skip_diversity_indices) <span class="ox-param-inferred">inferred</span><br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastqc = value" data-copy="skip_fastqc = false">skip_fastqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skip flags (upstream params.skip_*, all default false -&gt; full default path)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_multiqc = value" data-copy="skip_multiqc = false">skip_multiqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skip flags (upstream params.skip_*, all default false -&gt; full default path)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_qiime = value" data-copy="skip_qiime = false">skip_qiime</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skip flags (upstream params.skip_*, all default false -&gt; full default path)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_qiime_downstream = value" data-copy="skip_qiime_downstream = false">skip_qiime_downstream</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">--- QIIME2 downstream analyses beyond the taxa barplot (upstream<br>params.skip_qiime_downstream default false; the port gates all<br>of these on run_qiime2 as well) ---<br><span class="ox-param-usedby">used by <code>14</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_taxonomy = value" data-copy="skip_taxonomy = false">skip_taxonomy</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">skip flags (upstream params.skip_*, all default false -&gt; full default path)<br><span class="ox-param-usedby">used by <code>14</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy tax_agglom_max = value" data-copy="tax_agglom_max = 6">tax_agglom_max</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>6</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy tax_agglom_min = value" data-copy="tax_agglom_min = 2">tax_agglom_min</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">—<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy trunc_qmin = value" data-copy="trunc_qmin = 25">trunc_qmin</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>25</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy trunc_rmin = value" data-copy="trunc_rmin = 0.75">trunc_rmin</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.75</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy truncq = value" data-copy="truncq = 2">truncq</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">DADA2 filtering / denoising<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-ampliseq-rules.svg?v=ab829f5c0f" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-ampliseq-rules.svg?v=ab829f5c0f" alt="oxo-flow-ampliseq rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-ampliseq.svg?v=c158105bb1" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-ampliseq.svg?v=c158105bb1" alt="oxo-flow-ampliseq pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-ampliseq — Amplicon sequencing analysis (16S/ITS) that takes raw paired-end reads through FastQC quality control, cutadapt primer trimming (incl.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- rename_raw_data_files
- fastqc
- cutadapt
- cutadapt_summary
- cutadapt_summary_merge
- dada2_quality_fw
- dada2_quality_rv
- trunclen_fw
- trunclen_rv
- dada2_filtntrim
- dada2_quality_fw_preprocessed
- dada2_quality_rv_preprocessed
- dada2_err
- dada2_denoising
- dada2_rmchimera
- dada2_stats
- dada2_merge
- merge_stats
- itsx_cutasv
- itsxrust_cutasv
- filter_len_itsx
- download_taxonomy_db
- format_taxonomy
- dada2_taxonomy
- dada2_taxonomy_its
- qiime2_inasv
- qiime2_inseq
- qiime2_inasv_its
- qiime2_inseq_its
- qiime2_intax
- qiime2_barplot
- qiime2_metadata_categories
- qiime2_diversity_tree
- qiime2_alphararefaction
- qiime2_diversity_core
- qiime2_diversity_alpha
- qiime2_diversity_beta
- qiime2_diversity_betaord
- qiime2_diversity_adonis
- qiime2_export_absolute
- qiime2_export_relasv
- qiime2_export_reltax
- qiime2_ancom
- qiime2_ancombc
- qiime2_ancombc2
- qiime2_preptax
- qiime2_classify
- multiqc
- picrust
- sbdiexport
- sbdiexportreannotate
- phyloseq
- treesummarizedexperiment
- summary_report

**Excluded**

- PPLACE phylogenetic placement (clustalo / gappa / epa-ng / hmmer / mafft; upstream `fasta_newick_epang_gappa` + `fasta_hmmsearch_rank_fastas` + seqtk) — not ported; the port has no phylogeny branch (the tree arg is the upstream `none.tree` placeholder)
- Kraken2 / VSEARCH / SIDLE / SINTax alternative classification — upstream `kraken2_taxonomy_wf`, vsearch (cluster + LCA taxonomy), `sidle_wf`, SINTax taxonomy chain — not ported; each needs its own reference-taxonomy download, env and fixtures

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- nanopore: nanopore sequencing branch (params.nanopore) — absent from the 2.18.0 codebase (grep-verified; only docs/usage.md mentions Nanopore re ITSxRust long reads)
- syncom: synthetic community controls branch (params.syncom) — absent from the 2.18.0 codebase (grep-verified)
- PIGZ_UNCOMPRESS / UNTAR — internal decompression details of the ported `qiime2_preptax` (qza download path) and of the excluded Kraken2 branch; not user-facing gaps

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| RENAME_RAW_DATA_FILES | `rename_raw_data_files` | nf-core/ubuntu 20.04 | identical command (soft links) |
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command; upstream publishes only `*.html` — the port also declares the `*.zip` files because MultiQC consumes them |
| CUTADAPT_BASIC | `cutadapt` | cutadapt 5.2 | identical `ext.args` (`-O 3 -e 0.1 -g/-G --discard-untrimmed`) |
| CUTADAPT_SUMMARY | `cutadapt_summary` | python 3.8.3 | verbatim `bin/cutadapt_summary.py`, `paired_end` mode |
| CUTADAPT_SUMMARY_MERGE | `cutadapt_summary_merge` | — | copy action |
| DADA2_QUALITY1 / DADA2_QUALITY2 | `dada2_quality_fw`, `dada2_quality_rv`, `dada2_quality_fw_preprocessed`, `dada2_quality_rv_preprocessed` | r-base 4.0.3 / dada2 1.26.0 | upstream runs the same process twice per stage with different prefixes; the port splits each into one rule per prefix |
| TRUNCLEN | `trunclen_fw`, `trunclen_rv` | pandas 1.1.5 | verbatim `bin/trunclen.py` |
| DADA2_FILTNTRIM | `dada2_filtntrim` | dada2 1.26.0 | identical `filterAndTrim` args; args file renamed `{sample}.filterAndTrim.args.txt` (all oxo-flow rules share one workdir, upstream name would collide); `ID` column uses the file basename so read-tracking sample names match upstream |
| DADA2_ERR | `dada2_err` | dada2 1.26.0 | identical `learnErrors` args + `checkConvergence`/`plotErrors` outputs |
| DADA2_DENOISING | `dada2_denoising` | dada2 1.26.0 | identical `dada` (incl. `getDadaOpt` defaults) + `mergePairs` + `makeSequenceTable`; `params.sample_inference` wired to `pool =` (upstream only records it in the args file); retries=3 (upstream `error_retry`), 48h limit (`process_long`) |
| DADA2_RMCHIMERA | `dada2_rmchimera` | dada2 1.26.0 | identical `removeBimeraDenovo` args |
| DADA2_STATS | `dada2_stats` | dada2 1.26.0 | identical read-tracking table |
| DADA2_MERGE | `dada2_merge` | dada2 1.26.0 / digest 0.6.27 | both branches: single-run path, and `merge_runs = true` merges all run-level stats/ASV tables (unique rbind + `mergeSequenceTables` `repeats="error", orderBy="abundance", tryRC=FALSE`); the port passes the run-level files as argv (upstream globs `*.stats.tsv`/`*.ASVtable.rds` in its cwd) — see `scripts/dada2_merge.R` |
| ITSX_CUTASV | `itsx_cutasv` | itsx 1.1.3 | identical `ITSx` call (`--save_regions` from `cut_its`, `--partial` from `its_partial`); the config-dependent outfile is copied to the fixed `intermediates/itsx/ASV_ITS_seqs.fasta` so downstream rules have static inputs |
| ITSXRUST_CUTASV | `itsxrust_cutasv` | itsxrust 0.2.2 | identical `itsxrust extract` (HMM from `share/itsxrust/hmm/F.hmm`), same region outputs + `sed` header cleanup |
| FILTER_LEN_ITSX | `filter_len_itsx` | biostrings 2.66.0 (R 4.2 build; upstream 2.58.0 on R 4.0.3) | verbatim `bin/filter_len.R` with the ITSX `ext.args` (min 50 / max 1000000) |
| DADA2_TAXONOMY_WF (ITS) | `dada2_taxonomy_its` | dada2 1.26.0 | same chunked assignTaxonomy/addSpecies machinery as `dada2_taxonomy`, on the ITS-cut length-filtered fasta with the `.ASV_ITS_tax.<ref>` suffix, then `bin/add_full_sequence_to_taxfile.py` maps the taxonomy back onto the full ASV fasta — same published `ASV_tax.<ref>.tsv` / `ASV_tax_species.<ref>.tsv` paths as the default branch (the two rules are mutually exclusive via their gates) |
| QIIME2_INASV / QIIME2_INSEQ (ITS) | `qiime2_inasv_its`, `qiime2_inseq_its` | qiime2 2026.4 | same imports as the default variants but over the ITS-cut length-filtered table/seqs; they share the `intermediates/qiime2/table.qza` / `rep-seqs.qza` output paths with the default rules (mutually exclusive gates) |
| METADATA_ALL / METADATA_PAIRWISE | `qiime2_metadata_categories` | r-base 4.2 | verbatim `bin/metadata_all.r` / `bin/metadata_pairwise.r` in a conda rule (the qiime2 image has no Rscript); runs only when the QIIME2 downstream analyses need categories |
| QIIME2_TREE | `qiime2_diversity_tree` | qiime2 2026.4 | identical mafft → mask → fasttree → midpoint-root chain; rooted tree exported as `tree.nwk` |
| QIIME2_ALPHARAREFACTION | `qiime2_alphararefaction` | qiime2 2026.4 | identical: max-depth = min-read-count of `results/overall_summary.tsv` (via `bin/count_table_minmax_reads.py`, same file format as upstream MERGE_STATS_STD output) capped at 75000, steps 250 or maxdepth/20, 10 iterations |
| QIIME2_DIVERSITY_CORE | `qiime2_diversity_core` | qiime2 2026.4 | identical core-metrics (sampling depth = min-read-count with `diversity_rarefaction_depth` floor, `UNIFRAC_USE_GPU=N`); the qza outputs feed the alpha/beta/betaord/adonis rules, the 4 distance matrices are exported as tsv |
| QIIME2_DIVERSITY_ALPHA / BETA / BETAORD / ADONIS | `qiime2_diversity_alpha`, `qiime2_diversity_beta`, `qiime2_diversity_betaord`, `qiime2_diversity_adonis` | qiime2 2026.4 | identical commands (beta: `--p-pairwise` per distance × metadata category; adonis: `--p-n-jobs 1`, `--p-formula` per comma-separated `qiime_adonis_formula`); upstream fans channels out, the port loops over the category/formula lists in-shell — **data-dependent outputs**: the declared file sets assume the default fixture metadata ("group") / configured formulas |
| QIIME2_EXPORT_ABSOLUTE / RELASV / RELTAX | `qiime2_export_absolute`, `qiime2_export_relasv`, `qiime2_export_reltax` | qiime2 2026.4 | identical export + biom convert + collapse/relative-frequency loops over `tax_agglom_min`..`tax_agglom_max` (default 2..6, so the declared outputs cover that range) |
| QIIME2_ANCOM / ANCOMBC / ANCOMBC2 | `qiime2_ancom`, `qiime2_ancombc`, `qiime2_ancombc2` | qiime2 2026.4 | identical per-category filtering (`--p-where "${cat}<>''"`), ASV + per-level analyses, `<2`-taxa WARNING branch, ANCOMBC `--p-prv-cut 0.1 --p-lib-cut 500 --p-alpha 0.05 --p-conserve` + da-barplot thresholds, ANCOMBC2 `--p-p-adjust-method "holm" --p-prevalence-cutoff 0.1 --p-alpha 0.05` + `bin/ancombc_volcanoplot.r`; `ancombc_formula`/`ancombc2_formula` variants run on the unfiltered table like upstream. Upstream's error-ignore WARNING files become `<...>.WARNING.txt` next to the export dirs |
| QIIME2_PREPTAX (incl. EXTRACT + TRAIN) | `qiime2_preptax` | qiime2 2026.4 | identical: downloads the `qiime_ref_taxonomy_urls` qza pair, `bin/taxref_reformat_qiime_silva138.sh`, imports, `extract-reads` with `FW_primer`/`RV_primer`, `fit-classifier-naive-bayes` → `intermediates/qiime2/classifier.qza` |
| QIIME2_TAXONOMY (classify) | `qiime2_classify` | qiime2 2026.4 | identical `classify-sklearn --p-n-jobs` + tabulate + export to `results/qiime2/taxonomy/`; a user-supplied `classifier` is copied in-shell (skips training); in classifier mode the DADA2-taxonomy import (`qiime2_intax`) is gated off and the classifier taxonomy takes over the same `intermediates/qiime2/taxonomy.qza` path |
| PICRUST | `picrust` | picrust2 2.6.3 | identical `picrust2_pipeline.py -t epa-ng --remove_intermediate --in_traits EC,KO` + `add_descriptions.py` ×3 (EC/KO/METACYC); the upstream source-message file (filename == message text) is written as `picrust_message.txt`; resource hint process_high + process_medium_memory = 10 cpus / 50G |
| — (not ported) | — | — | nanopore branch (`params.nanopore` — absent from the 2.18.0 codebase, docs only), syncom controls (`params.syncom` — absent from the 2.18.0 codebase); PPLACE phylogenetic placement (clustalo / gappa / epa-ng / hmmer / mafft via `fasta_newick_epang_gappa` + `fasta_hmmsearch_rank_fastas`/seqtk — no phylogeny branch, `none.tree` placeholder), Kraken2 taxonomy (`kraken2_taxonomy_wf`), VSEARCH cluster + LCA taxonomy, SIDLE long-read species identification, SINTax taxonomy — present upstream, not ported; each needs its own env / reference-taxonomy download / fixtures |
| softwareVersionsToYAML + `versions.yml` collection (`pipeline_info/nf_core_ampliseq_software_mqc_versions.yml`, mixed into MultiQC inputs) | engine-native export: `oxo-flow report --versions-yml <file> main.oxoflow` | — | oxo-flow ≥ 0.17.0 exports an nf-core-style `versions.yml` derived statically from the workflow declarations: one entry per rule with the pinned container tag or conda env file + its sha256, plus a `references:` section fed by the workflow's `[[reference_db]]` blocks (SBDI-GTDB R11-RS232-1 here). Deviation: it is a standalone CI-diff artifact, not a per-process runtime capture — upstream records each tool's runtime version at execution time and mixes the collected file into MultiQC, while the export reflects the pinned versions in the definition (resolved runtime package versions depend on the execution environment). Per-rule `versions.yml` emission inside every command is deliberately not replicated (it would change every rule's command while the default plan stays byte-identical). |
| MERGE_STATS_STD | `merge_stats` | r-base 4.2 (envs/dada2.yaml pin; upstream declares the Wave image bioconductor-dada2_r-base_r-digest_tbb, no visible pin) | identical merge by `sample` |
| DB download (launcher) | `download_taxonomy_db` | curl | upstream downloads the reference DB in the Nextflow launcher (`file(url)`); the port makes it an explicit system-backend rule |
| FORMAT_TAXONOMY | `format_taxonomy` | nf-core/ubuntu 20.04 | verbatim `bin/taxref_reformat_sbdi-gtdb.sh`; runs in a scratch dir (the script globs `*`). Upstream declares the `biocontainers:v1.2.0_cv1` container but the port runs the script in `quay.io/nf-core/ubuntu:20.04` |
| DADA2_TAXONOMY + DADA2_ADDSPECIES + collectFile | `dada2_taxonomy` | dada2 1.26.0 | **merged**: upstream splits `ASV_seqs.fasta` into 10000-sequence chunks (`splitFasta by: 10000`) and runs assignTaxonomy + addSpecies per chunk, then concatenates chunk tables with header + sorted rows (`collectFile keepHeader, skip 1, sort`). The port replicates chunking with `awk` + per-chunk `Rscript` calls + `head`/`tail -n +2 | sort` concatenation — same chunk files, same args, same outputs. addSpecies resource hint (1 cpu/50G) becomes rule-level 10 cpus/20G, 24h limit |
| QIIME2_INASV | `qiime2_inasv` | qiime2 2026.4 | identical: biom convert + `tools import` `BIOMV210Format` |
| QIIME2_INSEQ | `qiime2_inseq` | qiime2 2026.4 | identical `FeatureData[Sequence]` import |
| QIIME2_INTAX | `qiime2_intax` | qiime2 2026.4 | verbatim `bin/parse_dada2_taxonomy.r` (porting change: output path is argv[2]) + `HeaderlessTSVTaxonomyFormat` import |
| QIIME2_BARPLOT | `qiime2_barplot` | qiime2 2026.4 | identical `taxa barplot` + `tools export` |
| MULTIQC | `multiqc` | multiqc 1.34 | identical command in a scratch dir (`multiqc` scans cwd `.`); verbatim `assets/multiqc_config.yml` |
| SBDIEXPORT | `sbdiexport` | r-base + SBDI export scripts (sbdiexport 1.2.1) | identical `sbdiexport()` call (paired mode, `FW_primer`/`RV_primer`, dada2 taxmethod); writes `results/SBDI/{event,dna,emof,asv-table}.tsv` |
| SBDIEXPORTREANNOTATE | `sbdiexportreannotate` | r-base + SBDI export scripts | identical re-annotation table (`annotation.tsv`); the barrnap-prediction arg is omitted (no barrnap branch in the port — the R script treats it as `NA`, same as upstream when no predictions exist) |
| PHYLOSEQ | `phyloseq` | phyloseq 1.50.0 (upstream biocontainers/bioconductor-phyloseq:1.50.0--r44hdfd78af_0, env pin 1.50.0) | identical inline R (`make_phyloseq` path); prefix literal `dada2`, tree arg = nonexistent `none.tree` (no phylogeny branch in the port — `file.exists` guard skips it, as upstream when no tree is staged) |
| TREESUMMARIZEDEXPERIMENT | `treesummarizedexperiment` | TreeSummarizedExperiment 2.10.0 (upstream biocontainers/bioconductor-treesummarizedexperiment:2.10.0--r43hdfd78af_0, env pin 2.10.0) | identical inline R; referenceSeq slot filled from the taxonomy `sequence` column; same `none.tree` convention |
| SUMMARY_REPORT | `summary_report` | r-base 4.2 + rmarkdown | identical `rmarkdown::render` of `assets/report_template.Rmd` with the upstream params-list contract (params_list_named, all string values single-quoted); SBDI/phyloseq/TSE/ITS sections are `[ -f ]`-conditional in-shell (their artifacts are not declared inputs — see deviations); `mqc_plot`/picrust sections omitted (see deviations) |

Other notes:

- `params.FW_primer`/`RV_primer` default to `null` upstream, which renders
  a literal `null` adapter into the cutadapt command; the port defaults
  them to empty strings (`-g ""`/`-G ""` = no 5'/3' adapter trimming), the
  behavior the upstream docs describe.
- All skip flags map 1:1 to `params.skip_*` (default false = full path).
  `skip_fastqc` requires `skip_multiqc` too — the MultiQC rule consumes the
  FastQC zips. `skip_taxonomy`/`skip_dada_taxonomy` additionally gate the
  QIIME2 taxonomy import and barplot, mirroring upstream's empty-taxonomy
  channel handling.
- `metadata_file` is a config key (default `test/fixtures/metadata.tsv`);
  upstream takes it from the samplesheet.
- The workflow declares an `[[reference_db]]` block for the SBDI-GTDB
  taxonomy (R11-RS232-1), which the engine's versions.yml export
  (`oxo-flow report --versions-yml <file> main.oxoflow`) surfaces in its
  `references:` section; upstream records the equivalent in its
  `workflow_manifest`/summary report instead.
- Deviations: the QIIME2 rules pin the container at
  `quay.io/qiime2/amplicon:2026.1` (upstream modules use `2026.4` — the
  version the port was built and live-tested against); `skip_qiime_downstream`
  scopes to the newly ported downstream rules (diversity, exports, ANCOM,
  classifier) and does not turn off the taxonomy import/barplot;
  data-dependent outputs (metadata categories, `tax_agglom_min`/`max`,
  adonis formulas, `<2`-taxa WARNING branches) declare the file set for the
  default fixture/parameters; PICRUSt always uses the DADA2 source
  (upstream switches to the QIIME2-filtered table when `run_qiime2` +
  abundance tables + a taxonomy are available — the port documents the
  DADA2 basis in `results/picrust/picrust_message.txt`); the rarefaction
  WARNING txt files (upstream `error_ignore` emits) are not declared as
  rule outputs; the phyloseq/TSE/summary-report gates default to `true`
  (i.e. off) while upstream runs them by default — flip
  `skip_phyloseq`/`skip_tse`/`skip_report` to `false` to match upstream;
  the summary report's optional sections (SBDI, phyloseq, TSE, ITS-cut) are
  `[ -f ]`-conditional in-shell rather than declared inputs, so a cold run
  with those gates enabled may race the report (re-run once the upstream
  rules finish — the engine's staleness check re-triggers the report);
  the summary report omits the upstream `mqc_plot` and picrust sections
  (`mqc_plot` has no ported counterpart wiring; the upstream picrust
  report section references a params list that is dead in 2.18.0);
  the report's `workflow_manifest_version` is the constant `'2.18.0'`
  and its taxonomy title is "Release R11-RS232-1" (upstream hardcodes the
  typo "R10"); no barrnap branch exists in the port, so
  `sbdiexportreannotate` omits the prediction-file arg (R treats it as
  `NA`, the same path upstream takes when no predictions exist).

## Links

- Repository: [oxo-flow-ampliseq](https://github.com/oxo-flow-community/oxo-flow-ampliseq)
- Upstream: [nf-core/ampliseq](https://github.com/nf-core/ampliseq) @ `2.18.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
