---
title: "Fetching public sequencing data: FastQ download, metadata and samplesheets"
description: "Fetching public sequencing data: FastQ download, metadata and samplesheets — the verified (★) entry, genomics, nextflow workflow, 17 rules, 8 tools."
---
---
title: "Fetching public sequencing data: FastQ download, metadata and samplesheets"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-fetchngs</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Fetching public sequencing data: FastQ download, metadata and samplesheets</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot" aria-hidden="true"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">sra</span><span class="ox-tag">ena</span><span class="ox-tag">ddbj</span><span class="ox-tag">geo</span><span class="ox-tag">fetch</span><span class="ox-tag">fastq-download</span><span class="ox-tag">samplesheet</span><span class="ox-tag">nf-core</span></div>
<p class="ox-desc">Fetch metadata and raw FastQ files from public sequence databases (SRA/ENA/DDBJ/GEO). Given a list of database identifiers — run accessions (SRR/ERR/DRR), experiments, studies, biosamples or GEO series — the pipeline retrieves the ENA run metadata, downloads the FastQ files over FTP, validates every download against its ENA md5 sum, and auto-creates a samplesheet plus sample id-mappings and a MultiQC mappings config, ready for downstream nf-core pipelines such as rnaseq, atacseq or taxprofiler.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-fetchngs" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v">★ Verified</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">17</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v"><span title="up to 2 CPUs / 12 GB per rule (download)">up to 2 CPUs / 12 GB per rule (download)</span></span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot" aria-hidden="true"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/fetchngs">nf-core/fetchngs</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>1.13.0</code></span></div>
<div class="ox-kv"><span class="k">Last verified</span><span class="v">2026-11-19</span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2289.1"><code>10.48546/workflowhub.workflow.2289.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">python</span><span class="tchip">wget</span><span class="tchip">coreutils</span><span class="tchip">curl</span><span class="tchip">sra-tools</span><span class="tchip">pigz</span><span class="tchip">fastq-dl</span><span class="tchip">aspera-cli</span></div></div>
<p class="cmd">$ oxo-flow pull \
  gh:oxo-flow-community/oxo-flow-fetchngs</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>SRA data fetch pipeline</strong>: give it a list of SRA/ENA/DDBJ accessions (e.g. <code>SRR9984183</code>) and it validates them, fetches run metadata, downloads FASTQ through several backends, and emits a standard samplesheet ready for nf-core pipelines — plus a MultiQC config.</p>
<p><strong>1. Input validation</strong> — the <code>ids</code> sample group defines the accessions to fetch; <code>check_ids</code> validates them against the SRA/ENA/DDBJ/GEO accession patterns and deduplicates; everything downstream is gated on this list, and <code>sra_ids_to_runinfo</code> pulls the ENA run metadata (runinfo) for each validated id.</p>
<p><strong>2. Download manifest</strong> — <code>sra_runinfo_to_ftp</code> turns the metadata into one download manifest per sample; this is the common entry point of every download route.</p>
<p><strong>3. FASTQ download (parallel tool backends)</strong> — from the manifest the pipeline fans out several download routes: <code>sra_fastq_ftp</code> over FTP; <code>sra_prefetch</code> prefetches and <code>sra_fastq_sratools</code> converts to FASTQ; <code>sra_fastq_aspera</code> over Aspera; plus a fallback chain (<code>sra_prefetch_fallback</code> → <code>sra_fastq_sratools_fallback</code>, and <code>sra_fastq_ftp_aspera_fallback</code>) and a dbGaP-specific chain (<code>sra_prefetch_dbgap</code> → <code>sra_fastq_sratools_dbgap</code>). Which route actually runs depends on the data source and runtime conditions — the results converge into the same samplesheet generation step.</p>
<p><strong>4. Samplesheet assembly and aggregation</strong> — <code>sra_to_samplesheet</code> consolidates metadata and all FASTQ routes into the downstream samplesheet; <code>combine_samplesheets</code> and <code>combine_mappings</code> then merge per-sample sheets and mappings (the <code>nf_core_pipeline</code> config can tailor row format for a specific downstream nf-core pipeline).</p>
<p><strong>5. Reporting</strong> — after the mappings are combined, <code>multiqc_mappings_config</code> generates the MultiQC configuration used by the downstream aggregate report.</p>
<p><em>Verified: every rule name above is a real rule of <code>main.oxoflow</code> (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-fetchngs+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-fetchngs
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-fetchngs` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-fetchngs@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-fetchngs` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Downloads public data by SRA/ENA accessions (network required) — configure your IDs first.

## Installation

**Engine.** oxo-flow >= 0.17.0

**Toolchain.** containers (Docker) — pinned images (quay.io/biocontainers and community.wave.seqera.io, identical to upstream)

**Requirements.**

- ids file: one SRA/ENA/DDBJ/GEO accession per line (config.input, default test/fixtures/ids.txt), kept in sync with the [[sample_groups]] sample source
- reference data: none — the workflow downloads data from public archives; no genome FASTA, annotation or indices required
- network: outbound access to ENA over FTP (wget -t 5 -nv -w 5 --random-wait -c -T 60, 2 retries); the sratools branch needs NCBI SRA outbound access (prefetch/fasterq-dump) plus the NCBI locate endpoint (locate.ncbi.nlm.nih.gov) for md5 verification of checksum-less prefetch archives; the aspera branch needs ENA fasp on port 33001 and outbound internet at runtime (the 4.20.0 image downloads the ascp client via `ascli conf ascp install`); the fastq-dl branch queries ENA and downloads from ENA's own mirrors
- compute: up to 2 CPUs / 12 GB per rule (FastQ download 2 threads/12G; metadata fetch 1 thread/6G; 4 h time limits on thirteen rules)
- disk: results/fastq/ grows with downloaded FastQ files plus md5/ checksums (depends on input size); metadata/ holds the runinfo tables and, for the fastq-dl branch, the per-run *-run-info.tsv / *-run-mergers.tsv; samplesheet/ stays small

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (bioconda's oxo-flow-cli tracks releases with a lag):
#    conda install -c bioconda oxo-flow-cli
#    Check `oxo-flow --version` against the Engine minimum above — if
#    bioconda trails it, use the release binary instead.

# 2. get this workflow (clones the repo, auto-discovers the workflow,
#    sanity-parses it with the engine)
oxo-flow pull gh:oxo-flow-community/oxo-flow-fetchngs
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-fetchngs
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dbgap_key = value" aria-label="Copy dbgap_key =  to clipboard" data-copy="dbgap_key = ">dbgap_key</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">dbGaP authorized-access certificate for the sratools branch (upstream<br>--dbgap_key): path to a .ngc or .jwt file. Empty = public data only — the<br>public sratools branch works without it; when set, the certificate is<br>passed through verbatim (prefetch/fasterq-dump --ngc or --perm).<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy download_method = value" aria-label="Copy download_method = ftp to clipboard" data-copy="download_method = ftp">download_method</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>ftp</code></td>
<td class="ox-p-desc">Download method, one of &#x27;ftp&#x27; (upstream default), &#x27;sratools&#x27; or &#x27;aspera&#x27;.<br>Each method gates its own branch of download rules; the default &#x27;ftp&#x27;<br>plan is unchanged when the other branches are off.<br><span class="ox-param-usedby">used by <code>9</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy email = value" aria-label="Copy email =  to clipboard" data-copy="email = ">email</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Completion notifications (upstream PIPELINE_COMPLETION, --email /<br>--email_on_fail / --hook_url; upstream defaults are null, here &quot;&quot;):<br>- email          address the completion summary is mailed to (sendmail/mail<br>on the host) after a run without failed rules<br>- email_on_fail  address mailed after a failed run; falls back to <code>email</code><br>when empty (nf-core sends the failure mail to email_on_fail,<br>or to email when only that is set)<br>- hook_url       webhook URL receiving a JSON notification (curl POST) with<br>the run counters, on completion and failure alike<br>These drive the [workflow] on_complete / on_error hooks above (engine &gt;=<br>0.17.0). With all three empty (the default) both hooks are no-ops, matching<br>upstream&#x27;s null params; older engines ignore the [workflow] keys entirely.<br>sraCurateSamplesheetWarn (the upstream end-of-run &quot;double-check the<br>samplesheet&quot; log note) has no hook: the auto-created samplesheet curation<br>caveat is documented in README.md instead.<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy email_on_fail = value" aria-label="Copy email_on_fail =  to clipboard" data-copy="email_on_fail = ">email_on_fail</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Completion notifications (upstream PIPELINE_COMPLETION, --email /<br>--email_on_fail / --hook_url; upstream defaults are null, here &quot;&quot;):<br>- email          address the completion summary is mailed to (sendmail/mail<br>on the host) after a run without failed rules<br>- email_on_fail  address mailed after a failed run; falls back to <code>email</code><br>when empty (nf-core sends the failure mail to email_on_fail,<br>or to email when only that is set)<br>- hook_url       webhook URL receiving a JSON notification (curl POST) with<br>the run counters, on completion and failure alike<br>These drive the [workflow] on_complete / on_error hooks above (engine &gt;=<br>0.17.0). With all three empty (the default) both hooks are no-ops, matching<br>upstream&#x27;s null params; older engines ignore the [workflow] keys entirely.<br>sraCurateSamplesheetWarn (the upstream end-of-run &quot;double-check the<br>samplesheet&quot; log note) has no hook: the auto-created samplesheet curation<br>caveat is documented in README.md instead.<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ena_metadata_fields = value" aria-label="Copy ena_metadata_fields =  to clipboard" data-copy="ena_metadata_fields = ">ena_metadata_fields</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Comma-separated ENA metadata fields; empty = upstream default field list.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy hook_url = value" aria-label="Copy hook_url =  to clipboard" data-copy="hook_url = ">hook_url</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Completion notifications (upstream PIPELINE_COMPLETION, --email /<br>--email_on_fail / --hook_url; upstream defaults are null, here &quot;&quot;):<br>- email          address the completion summary is mailed to (sendmail/mail<br>on the host) after a run without failed rules<br>- email_on_fail  address mailed after a failed run; falls back to <code>email</code><br>when empty (nf-core sends the failure mail to email_on_fail,<br>or to email when only that is set)<br>- hook_url       webhook URL receiving a JSON notification (curl POST) with<br>the run counters, on completion and failure alike<br>These drive the [workflow] on_complete / on_error hooks above (engine &gt;=<br>0.17.0). With all three empty (the default) both hooks are no-ops, matching<br>upstream&#x27;s null params; older engines ignore the [workflow] keys entirely.<br>sraCurateSamplesheetWarn (the upstream end-of-run &quot;double-check the<br>samplesheet&quot; log note) has no hook: the auto-created samplesheet curation<br>caveat is documented in README.md instead.<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy input = value" aria-label="Copy input = test/fixtures/ids.txt to clipboard" data-copy="input = test/fixtures/ids.txt">input</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/ids.txt</code></td>
<td class="ox-p-desc">File containing SRA/ENA/GEO/DDBJ identifiers, one per line (upstream --input).<br>Keep in sync with the [[sample_groups]] list below: check_ids validates this<br>file, the sample source drives the per-id expansion. Add extra ids on the<br>CLI with <code>oxo-flow run main.oxoflow --sample &lt;ID&gt;</code>.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nf_core_pipeline = value" aria-label="Copy nf_core_pipeline =  to clipboard" data-copy="nf_core_pipeline = ">nf_core_pipeline</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">nf-core pipeline to tailor the samplesheet for (rnaseq/atacseq/taxprofiler); empty = none.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nf_core_rnaseq_strandedness = value" aria-label="Copy nf_core_rnaseq_strandedness = auto to clipboard" data-copy="nf_core_rnaseq_strandedness = auto">nf_core_rnaseq_strandedness</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>auto</code></td>
<td class="ox-p-desc">nf-core pipeline to tailor the samplesheet for (rnaseq/atacseq/taxprofiler); empty = none.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" aria-label="Copy out_dir = results to clipboard" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">File containing SRA/ENA/GEO/DDBJ identifiers, one per line (upstream --input).<br>Keep in sync with the [[sample_groups]] list below: check_ids validates this<br>file, the sample source drives the per-id expansion. Add extra ids on the<br>CLI with <code>oxo-flow run main.oxoflow --sample &lt;ID&gt;</code>.<br><span class="ox-param-usedby">used by <code>16</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sample_mapping_fields = value" aria-label="Copy sample_mapping_fields = experiment_accession,run_accession,sample_accession,experiment_alias,run_alias,sample_alias,experiment_title,sample_title,sample_description to clipboard" data-copy="sample_mapping_fields = experiment_accession,run_accession,sample_accession,experiment_alias,run_alias,sample_alias,experiment_title,sample_title,sample_description">sample_mapping_fields</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>experiment_accession,run_accession,sample_accession,experiment_alias,run_alias,sample_alias,experiment_title,sample_title,sample_description</code></td>
<td class="ox-p-desc">nf-core pipeline to tailor the samplesheet for (rnaseq/atacseq/taxprofiler); empty = none.<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastq_download = value" aria-label="Copy skip_fastq_download = false to clipboard" data-copy="skip_fastq_download = false">skip_fastq_download</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Download method, one of &#x27;ftp&#x27; (upstream default), &#x27;sratools&#x27; or &#x27;aspera&#x27;.<br>Each method gates its own branch of download rules; the default &#x27;ftp&#x27;<br>plan is unchanged when the other branches are off.<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy sra_tools_fallback = value" aria-label="Copy sra_tools_fallback = false to clipboard" data-copy="sra_tools_fallback = false">sra_tools_fallback</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Per-run fallback (upstream SRA workflow <code>branch</code>), off by default so the<br>default &#x27;ftp&#x27; plan stays byte-identical; enable to match upstream&#x27;s<br>per-run triage for both methods:<br>- download_method = &#x27;ftp&#x27;: runs whose ENA metadata has NEITHER an FTP<br>link (fastq_1) NOR a fasp link (fastq_aspera) are routed to prefetch<br>+ fasterq-dump at runtime (sra_prefetch_fallback +<br>sra_fastq_sratools_fallback);<br>- download_method = &#x27;aspera&#x27;: runs without a fasp link are routed to<br>the FTP branch when they have an FTP link (fastq_1,<br>sra_fastq_ftp_aspera_fallback) and to prefetch + fasterq-dump<br>otherwise (the same fallback rules).<br>Without it, such runs are skipped with a warning.<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card ox-dag-card--wide" markdown="1">

<a href="/assets/dag/oxo-flow-fetchngs.svg?v=d71e35fef1" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-fetchngs.svg?v=d71e35fef1" alt="oxo-flow-fetchngs pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-fetchngs — Fetch metadata and raw FastQ files from public sequence databases (SRA/ENA/DDBJ/GEO).</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- check_ids
- sra_ids_to_runinfo
- sra_runinfo_to_ftp
- sra_fastq_ftp
- sra_prefetch
- sra_fastq_sratools
- sra_fastq_fastqdl
- sra_fastq_aspera
- sra_fastq_ftp_aspera_fallback
- sra_prefetch_fallback
- sra_fastq_sratools_fallback
- sra_prefetch_dbgap
- sra_fastq_sratools_dbgap
- sra_to_samplesheet
- combine_samplesheets
- combine_mappings
- multiqc_mappings_config

**Excluded**

- none

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- nf-core/untar module: already unreachable in 1.12.0 (no workflow/subworkflow included it) and removed from the upstream tree entirely in 1.13.0; the port never carried a rule for it
- adaptivecard/slackreport webhook assets + hook_url/imNotification: removed by upstream in 1.13.0, so there is nothing to port (see the README fidelity table)

## Fidelity

Default-parameters main execution path (`--download_method ftp`,
`--skip_fastq_download false`). Rows cover every upstream process/subworkflow
that the default path touches.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| PIPELINE_INITIALISATION (id validation + id channel) | `check_ids` | python 3.9.5 | In 1.12.0 this was the `isSraId` Groovy check of PIPELINE_INITIALISATION; in 1.13.0 upstream validates `--input` against the items pattern of `assets/schema_input.json` via the nf-schema plugin's `samplesheetToList` — the regex is byte-identical in both, and oxo-flow has no schema plugin, so `scripts/check_ids.py` remains the port-side enforcement point: validation regex, mixture/empty errors and deduplication ported 1:1; outputs `results/pipeline_info/input_ids.txt`. The ids channel itself is expanded from the workflow sample source (`[[sample_groups]]`, add ids via `--sample`); keep `[config] input` in sync. |
| SRA_IDS_TO_RUNINFO | `sra_ids_to_runinfo` | python 3.9.5 (`quay.io/biocontainers/python:3.9--1`) | Upstream `echo ${id} > id.txt; sra_ids_to_runinfo.py id.txt <id>.runinfo.tsv` verbatim; `--ena_metadata_fields` flag emitted only when set (same conditional), and since 1.13.0 (PR 381) upstream quotes the list and collapses whitespace around the commas — ported as a quoted bash array so field lists cannot word-split. One instance per input id (upstream: one process per id). The intermediate `.runinfo.tsv` lands in `results/metadata/` (upstream leaves it unpublished in the workdir; oxo-flow requires declared outputs for the DAG contract). |
| SRA_RUNINFO_TO_FTP | `sra_runinfo_to_ftp` | python 3.9.5 | `sra_runinfo_to_ftp.py` verbatim; output `<id>.runinfo_ftp.tsv` → `results/metadata/` (published upstream). |
| SRA_FASTQ_FTP | `sra_fastq_ftp` | wget 1.25.0 (`community.wave.seqera.io/library/gzip_wget:041a8ba200c3fa3f`, the upstream 1.13.0 Seqera Wave image bundling gzip 1.14 + wget 1.25.0), md5sum (coreutils, in the same image) | wget flags `-t 5 -nv -w 5 --random-wait -c -T 60` (1.13.0 added the `-w 5 --random-wait` wait flags, PR 325), `-O <exp>_<run>[_1|_2].fastq.gz` naming and `echo md5 … | md5sum -c` verification byte-identical; fastq → `results/fastq/`, md5 → `results/fastq/md5/` (upstream publishDir patterns). Per-run row parsing replaces the Groovy channel `branch`; **no outputs declared** because the produced file set (single- vs paired-end, per-run names) is data-dependent — md5 verification in the command is the correctness gate (same as upstream). Runs without FTP links are skipped with a warning in the default config; with `sra_tools_fallback = true` they are handled by the per-run sratools fallback rules below (the upstream `branch` triage, ported as a when-gated branch — off by default so the default plan is unchanged). |
| FASTQDL (nf-core/fastqdl, added in 1.13.0) | `sra_fastq_fastqdl` | fastq-dl 4.0.1 (`community.wave.seqera.io/library/fastq-dl:4.0.1--fd5420f75c055a44`, the upstream pin) | When-gated on `download_method = "fastq-dl"` (new in 1.13.0, off by default — the default plan is unchanged). `fastq-dl --prefix <id> --accession <run> --cpus 2 --outdir .` — the upstream script with `task.ext.args` empty (no `withName` block adds args for this process) and the upstream 2-cpu label. Runs with neither FTP nor fasp link are triaged to the sratools fallback rules (upstream `branch`), which this method enables unconditionally. The tool's own `<run>[_1|_2].fastq.gz` outputs move to `results/fastq/`, the `<id>-run-info.tsv` (+ paired-run `<id>-run-mergers.tsv`, upstream `optional: true`) to `results/metadata/` (upstream publishDirs). Deviations: `retries = 1` (the module carries no `error_retry` label; the base config's `maxRetries = 1` on infra-status retries is the port-side equivalent), and upstream's `--cpus` follows the label's cpus; the tool's own checksum verification is the integrity gate (upstream adds no md5sum pass for this branch). |
| SRA_TO_SAMPLESHEET (1.12.0) → CHANNEL_SRA_CREATE_CSV (1.13.0, subworkflows/local/channel_sra_create_csv) | `sra_to_samplesheet` | python 3.9.5 | Ported 1:1 from the upstream logic — in 1.13.0 the Groovy moved from the SRA_TO_SAMPLESHEET `exec` block into the CHANNEL_SRA_CREATE_CSV subworkflow (`buildPipelineMap`): removed keys (`id`, `md5_1/2`, `single_end`, `fastq_1/2`), `sample` = `<id>` without its trailing `_<run>` segment, `fastq_1/2` = `<outdir>/fastq/<file>` named per the 1.13.0 `branch` arm the run is routed to (ftp/aspera `<id>[_1|_2].fastq.gz`; sratools `<id>.fastq[_1|_2].fastq.gz` — the `--outfile <id>.fastq` split-file names; fastq-dl `<run>[_1|_2].fastq.gz`), ENA columns appended, the `pipeline_extras` of `buildPipelineMap` (rnaseq→strandedness, atacseq→replicate=1, taxprofiler→fasta='', ampliseq→run='', mag→group='' / short_reads_platform='ILLUMINA' / long_reads_platform='', sarek→patient=sample_accession; metatdenovo/viralrecon add no columns) and the `--sample_mapping_fields` validation with upstream error text. `localrule`, 100 MB memory, `executor 'local'` mapped to `localrule = true`. Runs only when `skip_fastq_download` is false (upstream: channel empty when skipped). |
| `collectFile('samplesheet.csv')` | `combine_samplesheets` | system (bash + coreutils) | Gather via `expand_inputs` over `config.samples_list`; 1.13.0 CHANNEL_SRA_CREATE_CSV collects the per-run strings with `newLine: true, keepHeader: true, sort: true` — header kept once, value rows in lexicographic order (`LC_ALL=C sort`, identical for the ASCII rows); `results/samplesheet/samplesheet.csv`. |
| `collectFile('id_mappings.csv')` | `combine_mappings` | system (bash + coreutils) | Same gather + `sort: true` semantics; `results/samplesheet/id_mappings.csv`. |
| MULTIQC_MAPPINGS_CONFIG | `multiqc_mappings_config` | python 3.9.5 | `multiqc_mappings_config.py` byte-identical to the upstream bin script — adopted verbatim with the 1.13.0 change (proper `csv.reader` parsing of the mappings csv, newline-safe quoting). Output `results/samplesheet/multiqc_config.yml` (upstream publishDir). Gated on `sample_mapping_fields` being set — on by default, same as upstream (1.13.0 gates per-element via `ch_mappings.filter { sample_mapping_fields }`). |
| softwareVersionsToYAML + `versions.yml` | engine-native export: `oxo-flow report --versions-yml <file> main.oxoflow` | — | oxo-flow ≥ 0.17.0 exports an nf-core-style `versions.yml` derived statically from the workflow declarations: one entry per rule (17 rules) with the pinned container image (registry + tag), or a `system` entry with an explicit "no software versions declared" note for the host-tool gather rules. Deviation: it is a standalone CI-diff artifact, not a per-process runtime capture — upstream 1.13.0 emits per-process version tuples on the `versions` topic (the 1.12.0 per-process `versions.yml` heredocs are gone) and collects them via the nf-core-utils plugin's `softwareVersionsToYAML` + `collectFile` into `pipeline_info/nf_core_fetchngs_software_versions.yml` (1.13.0 renamed the file, dropping the stale `_mqc`); the export reflects the pinned versions in the definition (resolved runtime package versions depend on the execution environment). The topic/plugin machinery has no oxo-flow equivalent — the export serves the same purpose, and its file name matches the upstream collected name. Per-rule version emission inside every command is deliberately not replicated (it would change every rule's command while the default plan stays byte-identical). The collected file has no consumer in fetchngs itself (no MultiQC process; the mappings config targets downstream pipelines) — upstream ships it as boilerplate, here the export serves the same CI-diff purpose. |
| PIPELINE_COMPLETION (`workflow.onComplete`: completionEmail / completionSummary / sraCurateSamplesheetWarn; `workflow.onError` note — 1.13.0 removed the 1.12.0 `hook_url` / `imNotification` branch together with `assets/adaptivecard.json` + `assets/slackreport.json`) | `[workflow] on_complete` + `on_error` hooks (`scripts/pipeline_completion.sh`) | sendmail / mail (host tools) | Ported onto the engine's workflow-level terminal hooks (engine >= 0.17.0): `email` mails the run-summary on completion, `email_on_fail` after a failed run (falling back to `email`, like upstream). Both default empty (upstream's null params), so the hooks no-op; older engines ignore the `[workflow]` keys entirely, keeping the default plan unchanged. The upstream `workflow.onError` troubleshooting line (`Pipeline failed. Please refer to troubleshooting docs …`) is echoed by the script on the failed path. `completionSummary`'s stdout line is covered by the engine's own "Done: N succeeded..." line, and `sraCurateSamplesheetWarn` is a static log note (see Known limitations). Hooks are best-effort: a missing mail tool only warns and never changes the run status. |
| CUSTOM_SRATOOLSNCBISETTINGS + SRATOOLS_PREFETCH | `sra_prefetch` | sra-tools 3.2.1 (`quay.io/biocontainers/sra-tools:3.2.1--h4304569_1`, the upstream 1.13.0 pin) | When-gated branch, off by default (`download_method = "sratools"` + `dbgap_key` empty): per-run `prefetch` under the upstream `retry_with_backoff` policy (5 attempts / 1 s base / 100 s max, `scripts/retry_with_backoff.sh` verbatim — the helper body is byte-identical to the 1.13.0 template, which also echoes the effective retry policy + final prefetch args) + the 1.13.0 integrity gate: `vdb-validate <run>` on the per-run output directory (sra-tools 3.2.1 emits ETL directories — upstream `path("${id}", type: 'dir')` — the 1.12.0 `.sralite` branch is gone) and, when the archive carries no checksums, an md5 comparison against the NCBI locate endpoint (PR 305). Fresh NCBI settings file per id (upstream CUSTOM_SRATOOLSNCBISETTINGS GUID config). SRA records land in `results/sra/<id>/` (upstream publishDir `results/sra`, `enabled: false` — intermediates). Applies to **all** runs, matching upstream's explicit `--download_method sratools` mode; with `dbgap_key` set, the dbGaP variant below takes over. |
| SRATOOLS_FASTERQDUMP | `sra_fastq_sratools` | sra-tools 3.2.1 + pigz 2.8 (`community.wave.seqera.io/library/sra-tools_pigz:4a694d823f6f7fcf`, the upstream 1.13.0 Seqera Wave image — the 1.12.0 patched mulled image and its local sratools-fasterqdump.diff are gone) | When-gated on `download_method = "sratools"` (+ `dbgap_key` empty); depends on `sra_prefetch`. Consumes the per-run prefetch **directories** of sra-tools 3.2.1. `fasterq-dump --split-files --include-technical --threads --outfile <id>.fastq` + the 1.13.0 paired-run guard `mv <id>.fastq <id> || echo 'No third file'` (keeping the "third file" out of the `pigz *.fastq` glob; workaround for the '.'-in-path bug, ncbi/sra-tools#865) + `pigz --no-name --processes`, translated from the module. Files land in `results/fastq/`; paired runs now come out as `<id>.fastq_1.fastq.gz` / `<id>.fastq_2.fastq.gz` (the 1.12.0 module's `<id>_1/2.fastq.gz` names changed with the `--outfile <id>.fastq` adoption) — the samplesheet references the actual per-branch names (see `sra_to_samplesheet`). |
| Per-run sratools fallback (upstream FETCHNGS `branch`, runs without FTP/fasp links — for `download_method = "ftp"` / `"aspera"` gated on `sra_tools_fallback`, and unconditionally for `"fastq-dl"`) | `sra_prefetch_fallback` + `sra_fastq_sratools_fallback` | sra-tools 3.2.1 + the Wave sra-tools_pigz image (same images as above) | When-gated on `sra_tools_fallback = true` + `download_method = "ftp"` or `"aspera"` (off by default — the default plan is unchanged); for `download_method = "fastq-dl"` the two rules carry the upstream triage unconditionally (1.13.0 routes runs without download links to the sratools subworkflow for every method). Mirrors the sratools-method rules but processes only the runs upstream's `branch` sends to sra-tools: rows whose metadata has neither `fastq_1` nor `fastq_aspera` (branch condition `!meta.fastq_aspera && !meta.fastq_1`, re-derived from the runinfo tsv by `scripts/sra_prefetch_runs.sh` / `scripts/sra_fastq_sratools_runs.sh`). Prefetch + the 1.13.0 vdb-validate/md5-locate gate, then fasterq-dump (`--outfile <id>.fastq` + the paired-run guard) + pigz into `results/fastq/` with the per-branch naming so the samplesheet matches; the FTP rule keeps downloading the runs that do have links. Like upstream (which passes `params.dbgap_key` to the sratools subworkflow for every download method), a configured dbGaP certificate flows into the triage too — the public path (empty `dbgap_key`) is unchanged. |
| dbGaP (`--dbgap_key`) | `sra_prefetch_dbgap` + `sra_fastq_sratools_dbgap` | sra-tools 3.2.1 + the Wave sra-tools_pigz image (same images) | When-gated on `download_method = "sratools"` + `dbgap_key` set (off by default: `dbgap_key = ""`; the plain sratools rules are gated off in that case). The certificate is passed through verbatim like upstream: `.ngc` → `prefetch --ngc` / `fasterq-dump --ngc`, `.jwt` → `--perm` (SRATOOLS_PREFETCH cert_arg and SRATOOLS_FASTERQDUMP key_file logic, same rules for both tools); the 1.13.0 modules key the choice off `certificate.name`/`toString().endsWith`, same effect. Still requires the user's own NIH authorized-access credentials at runtime — the port itself needs nothing, and the public path (empty `dbgap_key`) is unchanged. |
| ASPERA_CLI (Aspera CLI 4.20.0, `fasp` links) | `sra_fastq_aspera` | aspera-cli 4.20.0 (`quay.io/biocontainers/aspera-cli:4.20.0--hdfd78af_0`, the upstream 1.13.0 image). BREAKING vs 1.12.0 (4.14.0): the image no longer bundles the `ascp` client — the upstream script header bootstraps it at runtime via `ascli conf ascp install` (idempotent; needs outbound internet on the compute node) and locates it via `find ${HOME}/.aspera/sdk`; and the download now authenticates with the RSA bypass key `assets/aspera_bypass_rsa.pem` (the upstream module asset, shipped byte-identical — the 1.12.0 in-image DSA key is deprecated) | When-gated on `download_method = "aspera"`: `"$ASCP" -QT -l 300m -P33001 -i "$BYPASS_KEY"` (upstream ext.args) against the `fastq_aspera` fasp links with user `era-fasp`, md5-verified like the FTP branch. No credentials needed — the anonymous ENA fasp endpoint is what upstream uses. Deviation: upstream also sends runs without fasp links to the ftp/sra-tools branches per run; that triage is ported as when-gated branches (`sra_fastq_ftp_aspera_fallback` + `sra_prefetch_fallback` / `sra_fastq_sratools_fallback`, all on `sra_tools_fallback = true`), so with the fallback off such runs are skipped with a warning. |
| Per-run FTP fallback for the aspera method (upstream FETCHNGS `branch`: with `download_method = "aspera"`, runs with an FTP link but no fasp link go to the FTP process) | `sra_fastq_ftp_aspera_fallback` | wget 1.25.0 (same Wave image as `sra_fastq_ftp`) | When-gated on `download_method = "aspera"` + `sra_tools_fallback = true` (off by default — the default plan is unchanged). `scripts/sra_fastq_ftp_aspera_runs.sh` carries the same wget `-t 5 -nv -w 5 --random-wait -c -T 60` download + md5 verification loop as the frozen `sra_fastq_ftp` command, applied to exactly the rows upstream's `branch` sends to the FTP arm: `fastq_1` set, `fastq_aspera` empty (branch condition `meta.fastq_1 && !meta.fastq_aspera`, re-derived from the runinfo tsv). Together with `sra_prefetch_fallback` / `sra_fastq_sratools_fallback` (same toggle) the runinfo tsv is fully partitioned — every run is downloaded exactly once by whichever branch upstream's `branch` would pick, with the FTP-branch naming so the samplesheet is method-agnostic. |
| `params.nf_core_pipeline` (1.13.0 schema enum: `ampliseq`/`atacseq`/`mag`/`metatdenovo`/`rnaseq`/`sarek`/`taxprofiler`/`viralrecon`) | `sra_to_samplesheet` | — | Off by default (empty), same as upstream; the `buildPipelineMap` column logic (see that row) is ported and activates when `nf_core_pipeline` is set. |
| publishDir / `--publish_dir_mode` | n/a | — | oxo-flow has no publishDir; outputs are declared directly at their `results/…` paths. |

Known limitations: the ids used for per-id expansion must be declared in the
sample source (`[[sample_groups]]`, or `--sample` on the CLI) and should match
`[config] input` validated by `check_ids`. The sra-tools, Aspera and fastq-dl
download methods are ported as when-gated branches (`download_method =
"sratools"` / `"aspera"` / `"fastq-dl"`); the upstream **per-run** triage is
ported as when-gated branches too, off by default (except for `fastq-dl`,
where upstream routes link-less runs to sra-tools unconditionally and the
two fallback rules run with the method) so the default plan is
byte-identical: `sra_tools_fallback = true` restores upstream's per-run
routing — with `ftp`, runs without FTP/fasp links go to prefetch/fasterq-dump;
with `aspera`, runs without a fasp link go to the FTP branch when they have an
FTP link (`sra_fastq_ftp_aspera_fallback`) and to prefetch/fasterq-dump
otherwise; with `fastq-dl`, runs without FTP/fasp links always go to
prefetch/fasterq-dump — and `dbgap_key` enables the dbGaP certificate path of
the sratools branch and the triage (the certificate is passed through
verbatim; the port itself needs no credentials). Remaining deviations: with
`ftp` or `aspera` and the fallback off, runs whose metadata lacks the
matching download links are skipped with a warning (upstream would route
them per run; enable `sra_tools_fallback` to restore the triage), and the
`aspera` branch needs outbound internet on the compute nodes at runtime
(runtime `ascli conf ascp install` download of the ascp client) — isolated
HPC clusters without direct egress should use `ftp`, `sratools` or
`fastq-dl`. The sratools-branch paired-end file names changed with 1.13.0
(`<id>.fastq_1.fastq.gz` / `<id>.fastq_2.fastq.gz`, driven by the
`--outfile <id>.fastq` adoption) and the samplesheet references the actual
per-branch names. The auto-created samplesheet should be double-checked
before downstream use (the upstream `sraCurateSamplesheetWarn` end-of-run
note): public databases don't reliably hold information such as strandedness
or controls, and all sample metadata from the ENA is appended as additional
columns to help manual curation. The nf-core boilerplate (`versions.yml`
collection) is covered by the engine-native export
(`oxo-flow report --versions-yml <file> main.oxoflow`, see table).

<details class="ox-evidence" markdown="1"><summary>Verification evidence</summary>

17 rules (default + sra fastq-dl / aspera / sratools / fallback / dbGaP branch arms; branch-override dry-runs render in CI). The 2026-11-19 re-port to upstream 1.13.0 is validate/lint/dry-run green in CI with the pinned engine 0.31.0 (0 errors). The historical live-verified bench runs (SRA-download paths on the 1.12.0-era port) predate this re-port, so the badge rests at Verified per the ratings policy until the community test bench re-confirms end-to-end.

</details>

## Links

- Repository: [oxo-flow-fetchngs](https://github.com/oxo-flow-community/oxo-flow-fetchngs)
- Upstream: [nf-core/fetchngs](https://github.com/nf-core/fetchngs) @ `1.13.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 · last catalog sync 2026-11-19. See the repository's NOTICE for full attribution.
