---
title: "Metagenome assembly, binning and taxonomic classification"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-mag</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Metagenome assembly, binning and taxonomic classification</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">metagenomics</span><span class="ox-tag">assembly</span><span class="ox-tag">binning</span><span class="ox-tag">taxonomy</span><span class="ox-tag">nf-core</span><span class="ox-tag">gtdbtk</span><span class="ox-tag">busco</span></div>
<p class="ox-desc">Turn paired-end metagenomic reads into quality-checked, taxonomically classified draft genomes: FastQC and fastp QC with phiX removal, SPAdes and MEGAHIT assembly, QUAST and Prodigal assessment, bowtie2 mapping, binning with six binners (MetaBAT2, MaxBin2, CONCOCT, COMEBin, MetaBinner, SemiBin2), BUSCO bin QC, GTDB-Tk classification with a combined summary, PROKKA annotation, ALE evaluation and a final MultiQC report. The default short-read path of nf-core/mag, faithfully ported with the same tool versions and commands. Optional upstream branches are ported as when-gated rules, all off by default: host read removal (config.host_fasta), read normalization (config.bbnorm), adapterremoval/trimmomatic clipping (config.clip_tool), DAS Tool bin refinement (config.refine_bins_dastool), CheckM bin QC (config.run_checkm), CheckM2 bin QC (config.run_checkm2), GUNC contamination QC (config.run_gunc), Tiara domain classification (config.bin_domain_classification), CAT/BAT bin classification (config.cat_db) and virus identification with geNomad (config.run_virus_identification).</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-mag" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested · default-path</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">311</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v"><span title="up to 12 CPUs / 140 GB per rule (defaults 1 thread / 6 GB)">up to 12 CPUs / 140 GB per rule (defaults 1 thread / 6 GB)</span></span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">metagenomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/mag">nf-core/mag</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>5.5.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2281.1"><code>10.48546/workflowhub.workflow.2281.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">adapterremoval</span><span class="tchip">ale</span><span class="tchip">bbmap</span><span class="tchip">bioawk</span><span class="tchip">biopython</span><span class="tchip">bowtie2</span><span class="tchip">busco</span><span class="tchip">cat</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-mag</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Metagenome assembly and binning pipeline</strong>: given paired-end metagenomic reads, it trims them, removes host and phiX contamination, assembles with SPAdES or MEGAHIT, bins with six tools, quality-checks and classifies them, and delivers a MultiQC report.</p>
<p><strong>1. Read QC and trimming</strong> — <code>fastqc_raw</code> screens raw reads while one of three clip tools trims them (<code>fastp</code> by default, <code>adapterremoval_pe</code> or <code>trimmomatic</code>). Reads pass <code>host_removal_build</code> → <code>host_removal_align</code> with a host reference, and <code>phix_build</code> → <code>phix_align</code>; <code>fastqc_trimmed</code> re-reports the reads, <code>bbnorm</code> can normalize coverage, and <code>spades</code> and <code>megahit</code> each assemble the cleaned reads.</p>
<p><strong>2. Assembly checks</strong> — <code>gunzip_spades</code> unpacks the scaffolds; <code>quast_spades</code> scores the assembly and <code>prodigal_spades</code> predicts its proteins, each with a MEGAHIT twin; <code>genomad_spades</code>/<code>genomad_megahit</code> identify viruses when enabled.</p>
<p><strong>3. Mapping and binning</strong> — <code>bowtie2_build_spades</code> indexes each assembly; <code>bowtie2_align_spades</code> maps every cohort sample's reads, and <code>depths_spades</code> → <code>convert_depths_spades</code> compute binning depths. Six binner families then cluster the contigs: <code>metabat2_spades</code>, <code>maxbin2_spades</code>, <code>comebin_spades</code>, <code>semibin_spades</code>, the CONCOCT chain <code>concoct_cutup_spades</code> → <code>concoct_table_spades</code> → <code>concoct_spades</code> → <code>concoct_merge_spades</code> → <code>concoct_extract_spades</code>, and the MetaBinner chain (<code>metabinner_kmer_spades</code> → <code>metabinner_run_spades</code> → <code>metabinner_bins_spades</code>). <code>split_fasta_metabat2_spades</code> chunks unbinned contigs and <code>seqkit_spades_metabat2</code> records bin length stats.</p>
<p><strong>4. Bin QC</strong> — <code>ale_spades</code>/<code>ale_megahit</code> evaluate each assembly against mapped reads. Per binner–assembler pair, <code>busco_spades_metabat2</code>, <code>quast_bins_spades_metabat2</code> and <code>mag_depths_spades_metabat2</code> assess the bins; optional checks: <code>checkm_lineagewf_spades_metabat2</code> → <code>checkm_qa_spades_metabat2</code>, <code>checkm2_spades_metabat2</code>, and <code>gunc_spades_metabat2</code> → <code>gunc_mergecheckm_spades_metabat2</code>. <code>concat_busco</code>, <code>concat_quast</code> and <code>mag_depths_summary</code> merge the per-pair tables.</p>
<p><strong>5. Classification and annotation</strong> — <code>gtdbtk_db_preparation</code> prepares the database; <code>gtdbtk_spades_metabat2</code> and its per-binner siblings classify bins, <code>gtdbtk_summary</code> merges results and <code>prokka_spades_metabat2</code> annotates genes. Optional, config-gated extras: DAS Tool refinement (<code>dastool_dastool_spades</code>), Tiara domain classification (<code>tiara_tiara_spades</code> → <code>tiara_classify_spades_metabat2_bins</code>), CAT/BAT (<code>cat_db_preparation</code> → <code>catpack_bins_spades_metabat2</code> → <code>catpack_addnames_spades_metabat2</code> → <code>catpack_summarise_spades_metabat2</code>, plus <code>catpack_bat_summary</code>).</p>
<p><strong>6. Summary</strong> — <code>bin_summary</code> merges the QC and taxonomy tables; <code>multiqc</code> reports them all.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-mag+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-mag
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-mag` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-mag@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-mag` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Download the GTDB-Tk database (~100 GB), set `config.gtdb_db`, then run — the default config otherwise points at committed test fixtures.

## Installation

**Engine.** oxo-flow >= 0.17.0

**Toolchain.** conda envs — pinned

**Requirements.**

- input: paired-end reads as {sample}_R1.fastq.gz / {sample}_R2.fastq.gz in config.input_dir (default test/fixtures/raw); uniform single-end libraries runnable via config.sample_pattern override; interleaved and mixed-library samplesheets not ported
- compute: up to 12 CPUs / 140 GB RAM per rule (SPAdes 10 CPUs/72 GB/24 h; GTDB-Tk classifywf 2 CPUs/140 GB/12 h; defaults 1 thread/6 GB)
- reference: GTDB-Tk database — download gtdbtk_data.tar.gz (~100 GB) or unpacked directory and set config.gtdb_db (oxo-flow cannot download it mid-run)
- reference: phiX genome FASTA bundled in the repo (assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz) — no download needed
- reference (optional): host genome FASTA for config.host_fasta (host read removal branch); CheckM lineage database comes with the conda env (config.run_checkm branch, ~1.1 GB unpacked); Tiara downloads its model on first run (config.bin_domain_classification branch)
- reference (optional, per gated branch): CheckM2 database — checkm2 database --download (~8 GB, config.run_checkm2); GUNC reference database — gunc download_db (~21 GB, config.run_gunc); CAT-nr database — CAT_pack download + prepare, archive or unpacked directory with db/ and tax/ subdirectories (config.cat_db); geNomad database — genomad download-database (~10 GB, config.run_virus_identification); each branch fails fast with a clear message when its database is not set
- software: conda or mamba with the pinned envs/*.yaml environments (one per tool, no container layer)
- optional: disk — hundreds of GB for real datasets (GTDB-Tk database plus per-sample assemblies and bins)

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-mag
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-mag
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adapterremoval_adapter1 = value" data-copy="adapterremoval_adapter1 = AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNATCTCGTATGCCGTCTTCTGCTTG">adapterremoval_adapter1</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>AGATCGGAAGAGCACACGTCTGAACTCCAGTCACNNNNNNATCTCGTATGCCGTCTTCTGCTTG</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adapterremoval_adapter2 = value" data-copy="adapterremoval_adapter2 = AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT">adapterremoval_adapter2</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTAGATCTCGGTGGTCGCCGTATCATT</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adapterremoval_minquality = value" data-copy="adapterremoval_minquality = 2">adapterremoval_minquality</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy adapterremoval_trim_quality_stretch = value" data-copy="adapterremoval_trim_quality_stretch = false">adapterremoval_trim_quality_stretch</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ale_per_base_output = value" data-copy="ale_per_base_output = false">ale_per_base_output</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">ALE (upstream --ale_per_base_output default false -&gt; --metagenome --nout)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bbnorm = value" data-copy="bbnorm = false">bbnorm</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Read normalization (upstream --bbnorm; runs between phiX removal and assembly)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bbnorm_min = value" data-copy="bbnorm_min = 5">bbnorm_min</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>5</code></td>
<td class="ox-p-desc">Read normalization (upstream --bbnorm; runs between phiX removal and assembly)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bbnorm_target = value" data-copy="bbnorm_target = 100">bbnorm_target</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">Read normalization (upstream --bbnorm; runs between phiX removal and assembly)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bin_concoct_chunksize = value" data-copy="bin_concoct_chunksize = 10000">bin_concoct_chunksize</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10000</code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bin_concoct_donotconcatlast = value" data-copy="bin_concoct_donotconcatlast = false">bin_concoct_donotconcatlast</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bin_concoct_overlap = value" data-copy="bin_concoct_overlap = 0">bin_concoct_overlap</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bin_domain_classification = value" data-copy="bin_domain_classification = false">bin_domain_classification</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Domain classification with Tiara (upstream --bin_domain_classification / --tiara_min_length)<br><span class="ox-param-usedby">used by <code>39</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bin_max_size = value" data-copy="bin_max_size = ">bin_max_size</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Bin size filtering (upstream --bin_min_size / --bin_max_size; defaults<br>0/null make the seqkit-based filter a no-op)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bin_metabinner_scale = value" data-copy="bin_metabinner_scale = large">bin_metabinner_scale</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>large</code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bin_min_size = value" data-copy="bin_min_size = 0">bin_min_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">Bin size filtering (upstream --bin_min_size / --bin_max_size; defaults<br>0/null make the seqkit-based filter a no-op)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cat_allow_unofficial_lineages = value" data-copy="cat_allow_unofficial_lineages = false">cat_allow_unofficial_lineages</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">CAT/BAT bin classification (upstream --cat_db; the CAT_prepare database<br>is user-provided — CAT_pack download + prepare, or the archive/directory<br>itself; db/ and tax/ directories are discovered inside it)<br><span class="ox-param-usedby">used by <code>24</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cat_db = value" data-copy="cat_db = ">cat_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">CAT/BAT bin classification (upstream --cat_db; the CAT_prepare database<br>is user-provided — CAT_pack download + prepare, or the archive/directory<br>itself; db/ and tax/ directories are discovered inside it)<br><span class="ox-param-usedby">used by <code>38</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy checkm2_db = value" data-copy="checkm2_db = ">checkm2_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">CheckM2 bin QC (upstream --run_checkm2; the ~10GB .dmnd database is<br>user-provided — checkm2 database --download; fails fast when empty)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy checkm_db = value" data-copy="checkm_db = ">checkm_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">CheckM bin QC (upstream --run_checkm; the 1.1GB lineage database is<br>downloaded at env creation and unpacked at run time — see README)<br><span class="ox-param-usedby">used by <code>24</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy clip_tool = value" data-copy="clip_tool = fastp">clip_tool</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>fastp</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cohort_samples = value" data-copy="cohort_samples = S1 S2">cohort_samples</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>S1 S2</code></td>
<td class="ox-p-desc">Space-separated list of sample ids used by the binning-preparation<br>bowtie2 alignment rules (binning_map_mode=&#x27;group&#x27;: every assembly is<br>aligned against every sample&#x27;s reads). Keep in sync with the sample<br>group below.<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fastp_cut_mean_quality = value" data-copy="fastp_cut_mean_quality = 15">fastp_cut_mean_quality</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fastp_qualified_quality = value" data-copy="fastp_qualified_quality = 15">fastp_qualified_quality</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fastp_trim_polyg = value" data-copy="fastp_trim_polyg = false">fastp_trim_polyg</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy genomad_db = value" data-copy="genomad_db = ">genomad_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Virus identification (upstream --run_virus_identification; the geNomad<br>database is user-provided — genomad download-database; fails fast when empty)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdb_db = value" data-copy="gtdb_db = ">gtdb_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">GTDB-Tk database: local path to the release .tar.gz or an unpacked<br>directory (upstream --gtdb_db, ~100GB). oxo-flow cannot download it<br>mid-run (the prep rule only unpacks), so the default is empty and<br>run_gtdbtk=true fails fast until a local path is set.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdbtk_max_contamination = value" data-copy="gtdbtk_max_contamination = 10.0">gtdbtk_max_contamination</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>10.0</code></td>
<td class="ox-p-desc">GTDB-Tk (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdbtk_min_af = value" data-copy="gtdbtk_min_af = 0.65">gtdbtk_min_af</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.65</code></td>
<td class="ox-p-desc">GTDB-Tk (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdbtk_min_completeness = value" data-copy="gtdbtk_min_completeness = 50.0">gtdbtk_min_completeness</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>50.0</code></td>
<td class="ox-p-desc">GTDB-Tk (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdbtk_min_perc_aa = value" data-copy="gtdbtk_min_perc_aa = 10">gtdbtk_min_perc_aa</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>10</code></td>
<td class="ox-p-desc">GTDB-Tk (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdbtk_place_species = value" data-copy="gtdbtk_place_species = false">gtdbtk_place_species</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">GTDB-Tk (upstream params with the same defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdbtk_pplacer_cpus = value" data-copy="gtdbtk_pplacer_cpus = 1">gtdbtk_pplacer_cpus</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">GTDB-Tk (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gtdbtk_use_full_tree = value" data-copy="gtdbtk_use_full_tree = false">gtdbtk_use_full_tree</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">GTDB-Tk (upstream params with the same defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gunc_db = value" data-copy="gunc_db = ">gunc_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">GUNC contamination QC (upstream --run_gunc; the reference database is<br>user-provided — gunc download_db; fails fast when empty)<br><span class="ox-param-usedby">used by <code>12</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy host_fasta = value" data-copy="host_fasta = ">host_fasta</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Host read removal (upstream --host_fasta / --host_fasta_bowtie2index; the<br>reference fasta is required, the prebuilt bowtie2 index is optional and<br>skips the build rule)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy host_fasta_bowtie2index = value" data-copy="host_fasta_bowtie2index = ">host_fasta_bowtie2index</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Host read removal (upstream --host_fasta / --host_fasta_bowtie2index; the<br>reference fasta is required, the prebuilt bowtie2 index is optional and<br>skips the build rule)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy host_removal_verysensitive = value" data-copy="host_removal_verysensitive = false">host_removal_verysensitive</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Host read removal (upstream --host_fasta / --host_fasta_bowtie2index; the<br>reference fasta is required, the prebuilt bowtie2 index is optional and<br>skips the build rule)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy input_dir = value" data-copy="input_dir = test/fixtures/raw">input_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/raw</code></td>
<td class="ox-p-desc">Input directory containing {sample}_R1.fastq.gz / {sample}_R2.fastq.gz<br>paired-end read files (upstream --input samplesheet; single-end and<br>multi-library lanes are not ported). The repo default ships tiny test<br>fixtures; point this at your data.<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy max_unbinned_contigs = value" data-copy="max_unbinned_contigs = 100">max_unbinned_contigs</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">Bin size filtering (upstream --bin_min_size / --bin_max_size; defaults<br>0/null make the seqkit-based filter a no-op)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy metabat_rng_seed = value" data-copy="metabat_rng_seed = 1">metabat_rng_seed</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_contig_size = value" data-copy="min_contig_size = 1500">min_contig_size</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1500</code></td>
<td class="ox-p-desc">Bin size filtering (upstream --bin_min_size / --bin_max_size; defaults<br>0/null make the seqkit-based filter a no-op)<br><span class="ox-param-usedby">used by <code>18</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_length_unbinned_contigs = value" data-copy="min_length_unbinned_contigs = 1000000">min_length_unbinned_contigs</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000000</code></td>
<td class="ox-p-desc">Bin size filtering (upstream --bin_min_size / --bin_max_size; defaults<br>0/null make the seqkit-based filter a no-op)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">Input directory containing {sample}_R1.fastq.gz / {sample}_R2.fastq.gz<br>paired-end read files (upstream --input samplesheet; single-end and<br>multi-library lanes are not ported). The repo default ships tiny test<br>fixtures; point this at your data.<br><span class="ox-param-usedby">used by <code>276</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy phix_reference = value" data-copy="phix_reference = assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz">phix_reference</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz</code></td>
<td class="ox-p-desc">phiX reference (upstream --phix_reference default =<br>projectDir/assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy prokka_fast_mode = value" data-copy="prokka_fast_mode = false">prokka_fast_mode</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">PROKKA (upstream params with the same defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy prokka_with_compliance = value" data-copy="prokka_with_compliance = false">prokka_with_compliance</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">PROKKA (upstream params with the same defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reads_minlength = value" data-copy="reads_minlength = 15">reads_minlength</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>15</code></td>
<td class="ox-p-desc">Clipping (upstream params with the same defaults; --clip_tool selects the<br>adapter trimmer, fastp is the upstream default)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy refine_bins_dastool = value" data-copy="refine_bins_dastool = false">refine_bins_dastool</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">DAS Tool bin refinement (upstream --refine_bins_dastool / --refine_bins_dastool_threshold)<br><span class="ox-param-usedby">used by <code>28</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy refine_bins_dastool_threshold = value" data-copy="refine_bins_dastool_threshold = 0.5">refine_bins_dastool_threshold</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.5</code></td>
<td class="ox-p-desc">DAS Tool bin refinement (upstream --refine_bins_dastool / --refine_bins_dastool_threshold)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_checkm = value" data-copy="run_checkm = false">run_checkm</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">CheckM bin QC (upstream --run_checkm; the 1.1GB lineage database is<br>downloaded at env creation and unpacked at run time — see README)<br><span class="ox-param-usedby">used by <code>38</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_checkm2 = value" data-copy="run_checkm2 = false">run_checkm2</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">CheckM2 bin QC (upstream --run_checkm2; the ~10GB .dmnd database is<br>user-provided — checkm2 database --download; fails fast when empty)<br><span class="ox-param-usedby">used by <code>13</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_gtdbtk = value" data-copy="run_gtdbtk = true">run_gtdbtk</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">GTDB-Tk gate: the ~100GB reference database is user-provided (see the<br>README requirements); run_gtdbtk=false runs the full pipeline minus the<br>GTDB-Tk classification (the documented live-test contract).<br><span class="ox-param-usedby">used by <code>14</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_gunc = value" data-copy="run_gunc = false">run_gunc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">GUNC contamination QC (upstream --run_gunc; the reference database is<br>user-provided — gunc download_db; fails fast when empty)<br><span class="ox-param-usedby">used by <code>26</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy run_virus_identification = value" data-copy="run_virus_identification = false">run_virus_identification</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Virus identification (upstream --run_virus_identification; the geNomad<br>database is user-provided — genomad download-database; fails fast when empty)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy semibin_environment = value" data-copy="semibin_environment = global">semibin_environment</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>global</code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy semibin_rng_seed = value" data-copy="semibin_rng_seed = 1">semibin_rng_seed</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1</code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy shortread_percentidentity = value" data-copy="shortread_percentidentity = ">shortread_percentidentity</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Binning options (upstream params with the same defaults)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy tiara_min_length = value" data-copy="tiara_min_length = 3000">tiara_min_length</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>3000</code></td>
<td class="ox-p-desc">Domain classification with Tiara (upstream --bin_domain_classification / --tiara_min_length)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-mag-rules.svg?v=2de5a88219" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-mag-rules.svg?v=2de5a88219" alt="oxo-flow-mag rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-mag.svg?v=98ac7cc136" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-mag.svg?v=98ac7cc136" alt="oxo-flow-mag pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-mag — Turn paired-end metagenomic reads into quality-checked, taxonomically classified draft genomes: FastQC and fastp QC with phiX removal, SPAdes and MEGAHIT assembly, QUAST and Prodigal assessment, bowtie2 mapping, binning with six binners (MetaBAT2, MaxBin2, CONCOCT, COMEBin, MetaBinner, SemiBin2), BUSCO bin QC, GTDB-Tk classification with a combined summary, PROKKA annotation, ALE evaluation and a final MultiQC report.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- adapterremoval_pe
- ale_megahit
- ale_spades
- bbnorm
- bin_summary
- bowtie2_align_megahit
- bowtie2_align_spades
- bowtie2_build_megahit
- bowtie2_build_spades
- busco_megahit_comebin
- busco_megahit_concoct
- busco_megahit_maxbin2
- busco_megahit_metabat2
- busco_megahit_metabinner
- busco_megahit_semibin2
- busco_spades_comebin
- busco_spades_concoct
- busco_spades_maxbin2
- busco_spades_metabat2
- busco_spades_metabinner
- busco_spades_semibin2
- cat_db_preparation
- catpack_addnames_megahit_comebin
- catpack_addnames_megahit_concoct
- catpack_addnames_megahit_maxbin2
- catpack_addnames_megahit_metabat2
- catpack_addnames_megahit_metabinner
- catpack_addnames_megahit_semibin2
- catpack_addnames_spades_comebin
- catpack_addnames_spades_concoct
- catpack_addnames_spades_maxbin2
- catpack_addnames_spades_metabat2
- catpack_addnames_spades_metabinner
- catpack_addnames_spades_semibin2
- catpack_bat_summary
- catpack_bins_megahit_comebin
- catpack_bins_megahit_concoct
- catpack_bins_megahit_maxbin2
- catpack_bins_megahit_metabat2
- catpack_bins_megahit_metabinner
- catpack_bins_megahit_semibin2
- catpack_bins_spades_comebin
- catpack_bins_spades_concoct
- catpack_bins_spades_maxbin2
- catpack_bins_spades_metabat2
- catpack_bins_spades_metabinner
- catpack_bins_spades_semibin2
- catpack_summarise_megahit_comebin
- catpack_summarise_megahit_concoct
- catpack_summarise_megahit_maxbin2
- catpack_summarise_megahit_metabat2
- catpack_summarise_megahit_metabinner
- catpack_summarise_megahit_semibin2
- catpack_summarise_spades_comebin
- catpack_summarise_spades_concoct
- catpack_summarise_spades_maxbin2
- catpack_summarise_spades_metabat2
- catpack_summarise_spades_metabinner
- catpack_summarise_spades_semibin2
- checkm2_megahit_comebin
- checkm2_megahit_concoct
- checkm2_megahit_maxbin2
- checkm2_megahit_metabat2
- checkm2_megahit_metabinner
- checkm2_megahit_semibin2
- checkm2_spades_comebin
- checkm2_spades_concoct
- checkm2_spades_maxbin2
- checkm2_spades_metabat2
- checkm2_spades_metabinner
- checkm2_spades_semibin2
- checkm_lineagewf_megahit_comebin
- checkm_lineagewf_megahit_concoct
- checkm_lineagewf_megahit_maxbin2
- checkm_lineagewf_megahit_metabat2
- checkm_lineagewf_megahit_metabinner
- checkm_lineagewf_megahit_semibin2
- checkm_lineagewf_spades_comebin
- checkm_lineagewf_spades_concoct
- checkm_lineagewf_spades_maxbin2
- checkm_lineagewf_spades_metabat2
- checkm_lineagewf_spades_metabinner
- checkm_lineagewf_spades_semibin2
- checkm_qa_megahit_comebin
- checkm_qa_megahit_concoct
- checkm_qa_megahit_maxbin2
- checkm_qa_megahit_metabat2
- checkm_qa_megahit_metabinner
- checkm_qa_megahit_semibin2
- checkm_qa_spades_comebin
- checkm_qa_spades_concoct
- checkm_qa_spades_maxbin2
- checkm_qa_spades_metabat2
- checkm_qa_spades_metabinner
- checkm_qa_spades_semibin2
- comebin_megahit
- comebin_spades
- concat_busco
- concat_checkm2_tsv
- concat_checkm_tsv
- concat_gunc_checkm_tsv
- concat_gunc_tsv
- concat_quast
- concat_tiara_tsv
- concoct_cutup_megahit
- concoct_cutup_spades
- concoct_extract_megahit
- concoct_extract_spades
- concoct_megahit
- concoct_merge_megahit
- concoct_merge_spades
- concoct_spades
- concoct_table_megahit
- concoct_table_spades
- convert_depths_megahit
- convert_depths_spades
- dastool_dastool_megahit
- dastool_dastool_spades
- dastool_fastatocontig2bin_megahit_comebin
- dastool_fastatocontig2bin_megahit_concoct
- dastool_fastatocontig2bin_megahit_maxbin2
- dastool_fastatocontig2bin_megahit_metabat2
- dastool_fastatocontig2bin_megahit_metabinner
- dastool_fastatocontig2bin_megahit_semibin2
- dastool_fastatocontig2bin_spades_comebin
- dastool_fastatocontig2bin_spades_concoct
- dastool_fastatocontig2bin_spades_maxbin2
- dastool_fastatocontig2bin_spades_metabat2
- dastool_fastatocontig2bin_spades_metabinner
- dastool_fastatocontig2bin_spades_semibin2
- dastool_rename_post_megahit
- dastool_rename_post_spades
- dastool_rename_pre_megahit_comebin
- dastool_rename_pre_megahit_concoct
- dastool_rename_pre_megahit_maxbin2
- dastool_rename_pre_megahit_metabat2
- dastool_rename_pre_megahit_metabinner
- dastool_rename_pre_megahit_semibin2
- dastool_rename_pre_spades_comebin
- dastool_rename_pre_spades_concoct
- dastool_rename_pre_spades_maxbin2
- dastool_rename_pre_spades_metabat2
- dastool_rename_pre_spades_metabinner
- dastool_rename_pre_spades_semibin2
- depths_megahit
- depths_spades
- fastatocontig2bin_tiara_megahit_comebin_bins
- fastatocontig2bin_tiara_megahit_concoct_bins
- fastatocontig2bin_tiara_megahit_maxbin2_bins
- fastatocontig2bin_tiara_megahit_maxbin2_unbins
- fastatocontig2bin_tiara_megahit_metabat2_bins
- fastatocontig2bin_tiara_megahit_metabat2_unbins
- fastatocontig2bin_tiara_megahit_metabinner_bins
- fastatocontig2bin_tiara_megahit_metabinner_unbins
- fastatocontig2bin_tiara_megahit_semibin2_bins
- fastatocontig2bin_tiara_spades_comebin_bins
- fastatocontig2bin_tiara_spades_concoct_bins
- fastatocontig2bin_tiara_spades_maxbin2_bins
- fastatocontig2bin_tiara_spades_maxbin2_unbins
- fastatocontig2bin_tiara_spades_metabat2_bins
- fastatocontig2bin_tiara_spades_metabat2_unbins
- fastatocontig2bin_tiara_spades_metabinner_bins
- fastatocontig2bin_tiara_spades_metabinner_unbins
- fastatocontig2bin_tiara_spades_semibin2_bins
- fastp
- fastqc_raw
- fastqc_trimmed
- genomad_db_preparation
- genomad_megahit
- genomad_spades
- gtdbtk_db_preparation
- gtdbtk_megahit_comebin
- gtdbtk_megahit_concoct
- gtdbtk_megahit_maxbin2
- gtdbtk_megahit_metabat2
- gtdbtk_megahit_metabinner
- gtdbtk_megahit_semibin2
- gtdbtk_spades_comebin
- gtdbtk_spades_concoct
- gtdbtk_spades_maxbin2
- gtdbtk_spades_metabat2
- gtdbtk_spades_metabinner
- gtdbtk_spades_semibin2
- gtdbtk_summary
- gunc_megahit_comebin
- gunc_megahit_concoct
- gunc_megahit_maxbin2
- gunc_megahit_metabat2
- gunc_megahit_metabinner
- gunc_megahit_semibin2
- gunc_mergecheckm_megahit_comebin
- gunc_mergecheckm_megahit_concoct
- gunc_mergecheckm_megahit_maxbin2
- gunc_mergecheckm_megahit_metabat2
- gunc_mergecheckm_megahit_metabinner
- gunc_mergecheckm_megahit_semibin2
- gunc_mergecheckm_spades_comebin
- gunc_mergecheckm_spades_concoct
- gunc_mergecheckm_spades_maxbin2
- gunc_mergecheckm_spades_metabat2
- gunc_mergecheckm_spades_metabinner
- gunc_mergecheckm_spades_semibin2
- gunc_spades_comebin
- gunc_spades_concoct
- gunc_spades_maxbin2
- gunc_spades_metabat2
- gunc_spades_metabinner
- gunc_spades_semibin2
- gunzip_megahit
- gunzip_spades
- host_removal_align
- host_removal_build
- mag_depths_megahit_comebin
- mag_depths_megahit_concoct
- mag_depths_megahit_maxbin2
- mag_depths_megahit_metabat2
- mag_depths_megahit_metabinner
- mag_depths_megahit_semibin2
- mag_depths_spades_comebin
- mag_depths_spades_concoct
- mag_depths_spades_maxbin2
- mag_depths_spades_metabat2
- mag_depths_spades_metabinner
- mag_depths_spades_semibin2
- mag_depths_summary
- maxbin2_megahit
- maxbin2_spades
- megahit
- metabat2_megahit
- metabat2_spades
- metabinner_bins_megahit
- metabinner_bins_spades
- metabinner_kmer_megahit
- metabinner_kmer_spades
- metabinner_run_megahit
- metabinner_run_spades
- metabinner_tooshort_megahit
- metabinner_tooshort_spades
- multiqc
- phix_align
- phix_build
- prodigal_megahit
- prodigal_spades
- prokka_megahit_comebin
- prokka_megahit_concoct
- prokka_megahit_maxbin2
- prokka_megahit_metabat2
- prokka_megahit_metabinner
- prokka_megahit_semibin2
- prokka_spades_comebin
- prokka_spades_concoct
- prokka_spades_maxbin2
- prokka_spades_metabat2
- prokka_spades_metabinner
- prokka_spades_semibin2
- quast_bins_megahit_comebin
- quast_bins_megahit_concoct
- quast_bins_megahit_maxbin2
- quast_bins_megahit_metabat2
- quast_bins_megahit_metabinner
- quast_bins_megahit_semibin2
- quast_bins_spades_comebin
- quast_bins_spades_concoct
- quast_bins_spades_maxbin2
- quast_bins_spades_metabat2
- quast_bins_spades_metabinner
- quast_bins_spades_semibin2
- quast_megahit
- quast_spades
- semibin_megahit
- semibin_spades
- seqkit_megahit_comebin
- seqkit_megahit_concoct
- seqkit_megahit_maxbin2
- seqkit_megahit_metabat2
- seqkit_megahit_metabinner
- seqkit_megahit_semibin
- seqkit_spades_comebin
- seqkit_spades_concoct
- seqkit_spades_maxbin2
- seqkit_spades_metabat2
- seqkit_spades_metabinner
- seqkit_spades_semibin
- spades
- split_fasta_maxbin2_megahit
- split_fasta_maxbin2_spades
- split_fasta_metabat2_megahit
- split_fasta_metabat2_spades
- split_fasta_metabinner_megahit
- split_fasta_metabinner_spades
- tiara_classify_megahit_comebin_bins
- tiara_classify_megahit_concoct_bins
- tiara_classify_megahit_maxbin2_bins
- tiara_classify_megahit_maxbin2_unbins
- tiara_classify_megahit_metabat2_bins
- tiara_classify_megahit_metabat2_unbins
- tiara_classify_megahit_metabinner_bins
- tiara_classify_megahit_metabinner_unbins
- tiara_classify_megahit_semibin2_bins
- tiara_classify_spades_comebin_bins
- tiara_classify_spades_concoct_bins
- tiara_classify_spades_maxbin2_bins
- tiara_classify_spades_maxbin2_unbins
- tiara_classify_spades_metabat2_bins
- tiara_classify_spades_metabat2_unbins
- tiara_classify_spades_metabinner_bins
- tiara_classify_spades_metabinner_unbins
- tiara_classify_spades_semibin2_bins
- tiara_tiara_megahit
- tiara_tiara_spades
- trimmomatic
- fastqc_trimmed_sheet
- fastqc_raw_sheet
- fastp_sheet
- fastp_single_sheet
- phix_align_sheet
- spades_interleaved_sheet
- megahit_interleaved_sheet
- megahit_single_sheet
- bowtie2_align_spades_sheet
- bowtie2_align_megahit_sheet
- depths_spades_sheet
- depths_megahit_sheet
- catpack_unbinned_spades_metabat2
- catpack_unbinned_megahit_metabat2
- catpack_unbinned_spades_maxbin2
- catpack_unbinned_megahit_maxbin2
- catpack_unbinned_spades_concoct
- catpack_unbinned_megahit_concoct
- catpack_unbinned_spades_comebin
- catpack_unbinned_spades_metabinner
- catpack_unbinned_megahit_metabinner
- catpack_unbinned_spades_semibin2
- catpack_unbinned_megahit_semibin2
- catpack_unbinned_megahit_comebin
- pydamage_analyze_spades
- pydamage_analyze_megahit
- pydamage_filter_spades
- pydamage_filter_megahit
- ancient_consensus_spades
- ancient_consensus_megahit
- pydamage_bins_summary
- flye_lr
- metamdbg_lr
- minimap2_align_lr_flye
- minimap2_align_lr_metamdbg
- metabat2_lr_flye
- maxbin2_lr_flye
- concoct_lr_flye
- metabat2_lr_metamdbg
- maxbin2_lr_metamdbg
- concoct_lr_metamdbg

**Excluded**

- Long-read preprocessing QC (chopper / nanoq / nanolyse / porechop(+abi) / filtlong / nanoplot — upstream `preprocessing_longread`, default ON via skip_longread_qc=false) — not ported; the port long-read branch starts from QC-passed FASTQ (see the 12_longreads header note)
- Long-read host removal (minimap2 + samtools chain, upstream hostremoval_longread — runs when host_fasta is supplied) — not ported; short-read host removal is ported, long-read is not
- SPAdesHybrid / METASPADESHYBRID hybrid assembly (upstream assembly_hybrid, skip_spadeshybrid=false default) and pypolca short-read polish of long-read assemblies (workflows/mag.nf pypolca on ch_longread_assemblies) — not ported
- metaeuk / mmseqs (eukaryotic bin gene prediction + metaeuk_mmseqs_db database download, upstream mmseqs/databases + metaeuk/easypredict) — not ported
- seqtk mergepe multi-library lane merge (upstream preprocessing_shortread Run/Lane merging) — not ported; the port reads_sheet covers one stream per row (see README Multi-library lanes)
- BigMAG summary (generate_bigmag_file / prepare_bigmag_summary.py, upstream mag.nf PREPARE_BIGMAG_SUMMARY, default off) — not ported

**Not applicable** (upstream-absent features, boilerplate, dead code, deliberate non-goals — see the excluded-key taxonomy in [Traitome/oxo-flow#267](https://github.com/Traitome/oxo-flow/issues/267))

- kaiju — taxonomic profiling with kaiju; not portable: the process is absent from upstream nf-core/mag 5.5.0 entirely (removed upstream), so there is no module script to translate
- diamond — taxonomic profiling with diamond; upstream 5.5.0 has no standalone diamond profiling process — the only diamond reference is an optional `diamond_table` input the CAT/BAT modules accept but the upstream workflow never supplies, so there is no user-facing diamond feature to port
- nf-core boilerplate files (pipeline_summary/methods_description) — not part of the analysis. Not

## Fidelity

| Upstream | Port | Notes |
|----------|------|-------|
| Process-per-(assembler, binner) with `meta` tuples | One rule per (assembler, binner, ...) combination, names hard-coded | oxo-flow has no assembler/binner wildcard; `04_binning` has 48 rules, `05_binqc` 66, `06_taxonomy` 28, `07_refinement` 28, `08_domain` 39 (231 rules total) |
| Nextflow task workdir per process | Shared workflow dir + per-rule `.tmp/` scratch dirs | Tools that write generic-named files (spades, megahit, busco, quast, prokka, gtdbtk) run inside a scratch subdir and move outputs out |
| bash task scripts | `sh -c` executor | Process substitution (`2> >(tee ...)` in fastp) replaced with a plain redirect; brace expansion (`short_summary.*.{txt,json}`) split into two `mv` commands |
| Two BUSCO/GTDB-Tk/QUAST_BINS/MAG_DEPTHS runs per group (bins + chunks) | One rule per group that runs the tool twice in separate scratch subdirs | The two upstream runs share output names (`S1-auto-busco.*`); they are kept apart by the publish dirs `...-unclassified-unrefined-{sample}/` and `...-unclassified-unrefined_unbinned-{sample}/` |
| GTDB-Tk QC filter (Groovy) | `scripts/filter_bins_by_qc.py` | Same semantics: negative readings dropped, bins without metrics dropped, pass iff any reading clears both thresholds; BUSCO `Duplicated` is the contamination column |
| `gtdbtk_single_job` option | Not ported | Off by default upstream |
| `gtdbtk_use_full_tree` / `gtdbtk_place_species` | Config keys not exposed | Off by default upstream |
| Empty bin groups crash upstream (BUSCO on no input) | Empty groups produce empty/touched outputs and skip downstream classification | The pipeline never fails on empty groups |
| nf-core boilerplate (`versions.yml`) | engine-native export: `oxo-flow report --versions-yml <file> main.oxoflow` | oxo-flow ≥ 0.17.0 exports an nf-core-style `versions.yml` derived statically from the workflow declarations: one entry per rule (352 rules) with the pinned conda environment, or a `system` entry with an explicit "no software versions declared" note where no env is declared. Deviation: it is a standalone CI-diff artifact, not a per-process runtime capture — per-rule `versions.yml` emission inside every command is deliberately not replicated (it would change every rule's command while the default plan stays byte-identical). |
| nf-core boilerplate (pipeline_summary, methods_description) | Not ported | Not analysis output |
| `*-busco.batch_summary.failed.txt` | Produced on failure | The port reproduces the upstream failure-only artifact: when BUSCO yields no `batch_summary.txt` the rule copies the empty summary to `*-busco.batch_summary.failed.txt` (upstream exits non-zero at process level; the port keeps the marker and lets consumers skip) |
| `results/GenomeBinning/QC/BUSCO/` flat short_summaries | Published into the same per-group dir as upstream | Same publish pattern `*{.txt,.json,.log}` |
| Conda environments | `envs/*.yaml` with the same pins | `tar` added to `gunzip`/`gtdbtk_db_preparation` because there is no container layer; `split_fasta` and `mag_depths` pin `conda-forge::pandas=1.1.5` exactly like upstream (the other pins use the `bioconda::` channel prefix instead of `conda-forge::` — same package, same version) |
| QUAST_BINS / BUSCO / GTDB-Tk file names | `{assembler}-{binner}-unclassified-unrefined-{sample}[-unbinned]-...` in summary names, QC dirs and input globs | Matches upstream meta naming (`domain=unclassified`, `refinement=unrefined`/`unrefined_unbinned`); the port previously omitted `{sample}` from QUAST summary names and used `-unclassified-unrefined-` in bin input globs, where the files are actually named `{assembler}-{binner}-{sample}*` — the globs matched nothing (fixed) |
| METABAT2 `-m` clamp | `<1500` is clamped to `1500` in the rule shell | Upstream clamps in `conf/modules.config` (`ext.args`); port replicates it with a shell guard |
| METABAT2 / METABINNER_BINS discarded bins | tooShort/lowDepth moved to `GenomeBinning/{binner}/discarded/`; METABINNER unbinned also copied to `GenomeBinning/MetaBinner/unbinned/` | Matches the upstream `publishDir` patterns; the lowDepth move is guarded because `create_metabinner_bins.py` never emits that file |
| CONCOCT stats | clustering/merged CSV and coverage TSV copied to `GenomeBinning/CONCOCT/stats/` | Matches the upstream `*.{txt,csv,tsv}` publish pattern |
| COMEBin | no `-s large` argument | Upstream `COMEBIN_RUNCOMEBIN` passes no `ext.args` (the `-s` scale flag belongs to MetaBinner, which does pass it) |
| SemiBin2 `--environment` | passed only for single-sample cohorts | Matches upstream `meta.sample_count == 1` in `ext.args2` |
| METABINNER coverage profile | contig length filter uses `{config.min_contig_size}` (was hardcoded 1500) | Upstream passes `val_min_contig_size` to the awk filter |
| SPAdes (METASPADES) resources | 10 cpu / 72 GB / 24 h (was 12 cpu / 16 h) | Matches upstream `base.config` (`cpus = 10 * attempt`, `time = 24.h * attempt`); the `--memory 72` flag matches `memory = 72.GB` |
| MultiQC | report published to `multiqc/` (lowercase) with `--force` | Matches upstream publishDir and the nf-core multiqc module script |
| Convert-depths / split_fasta scratch | per-sample scratch dirs and guarded sample-scoped globs | oxo-flow executes rules in one shared working directory (upstream gives every task its own); the generic `mv *.abund` / `mv *.pooled.fa.gz *.remaining.fa.gz` would otherwise race or fail when a sample produces no such files |
| BINNING_REFINEMENT (DAS Tool) | `07_refinement.oxoflow`, 28 rules gated on `config.refine_bins_dastool` | RENAME_PREDASTOOL -> FASTATOCONTIG2BIN -> DASTOOL_DASTOOL -> RENAME_POSTDASTOOL mirror the upstream wiring; empty binner groups are dropped before DAS Tool exactly like upstream (`binners with no bins never reach DAS Tool`); the `_DASTool_bins`, log/summary/eval/seqlength aux files and `_DASToolUnbinned` gz are published to `GenomeBinning/DASTool/` |
| DAS Tool contig2bin join (upstream bash quirk) | `IFS=\t'` (ANSI-C) instead of upstream `IFS=$"\t"` | Verified empirically: `IFS=$"\t"` splits on the letter `t`, not tabs, so the upstream tiara_classify while-loop is broken for bin names containing `t` (e.g. MetaBAT2); the port uses the ANSI-C form |
| CHECKM_LINEAGEWF / CHECKM_QA (--run_checkm) | `05_binqc.oxoflow` + 25 rules, gated on `config.run_checkm` | `run_checkm()` shell function (gunzip-to-scratch with `-x fa`, `--pplacer_threads`, empty-group touched artifacts), then `checkm qa` with `-o 2 --tab_table`; both per-(assembler, binner) runs cover bins and unbinned chunks; outputs land in `GenomeBinning/QC/CheckM/` with the `-unclassified-unrefined[-_unbinned]` naming; a qsv rowskey concat produces `checkm_summary.tsv` |
| CheckM metrics into the GTDB-Tk filter | `filter_bins_by_qc.py --checkm-qa-file` on both gtdbtk rules; `bin_summary` passes `--checkm_summary` | Matches upstream: with `--run_checkm` the GTDB-Tk filter uses CheckM completeness/contamination instead of BUSCO; without it (the default) the BUSCO-only filter matches the upstream default config |
| CHECKM2_PREDICT / CONCAT_CHECKM2_TSV (--run_checkm2) | `05_binqc.oxoflow` + 13 rules gated on `config.run_checkm2` | `checkm2 predict --input input_bins/*` per (assembler, binner) group (gunzip-to-scratch like the CheckM branch), report copied to `QC/CheckM2/{prefix}_checkm2_report.tsv`, qsv rowskey concat into `checkm2_summary.tsv`; `config.checkm2_db` points at the local `.dmnd` database (the upstream module environment, `checkm2=1.1.0` + keras/numpy/pandas/scikit-learn/scipy/tensorflow pins, is in `envs/checkm2.yaml`); fails fast when unset |
| CheckM2 metrics into the GTDB-Tk filter | `filter_bins_by_qc.py --checkm2-qa-file` on both gtdbtk rules; `bin_summary` passes `--checkm2_summary` | Matches upstream: CheckM2 'Name' column is matched to the bin files with '.fa' appended (upstream appends the extension after CheckM2 strips `.gz`/`.fa`); with `--run_checkm2` the filter uses CheckM2 completeness/contamination (BUSCO/CheckM readings are still merged in exactly like upstream's `[busco, checkm2, checkm]` column list) |
| GUNC_RUN / CONCAT_GUNC_TSV (--run_gunc) | `05_binqc.oxoflow` + 13 rules gated on `config.run_gunc` | `gunc run --input_file` per (assembler, binner) group (bins + unbinned chunks, gunzip-to-scratch), per-database outputs renamed to `{prefix}_maxCSS_level.tsv` and moved under `QC/GUNC/raw/{prefix}/` like the upstream publishDir, qsv rowskey concat into `gunc_summary.tsv`; `config.gunc_db` points at the local reference database (`gunc=1.1.0` in `envs/gunc.yaml`); fails fast when unset |
| GUNC_MERGECHECKM (--run_gunc + --run_checkm) | `05_binqc.oxoflow` + 13 rules gated on `config.run_gunc && config.run_checkm` | `gunc merge_checkm -g <gunc> -c <checkm> -o .` per group, guarded on both inputs being non-empty (upstream `if (params.run_gunc)` requires CheckM output); `gunc_merge_checkm.tsv` moved to `QC/GUNC/checkmmerged/{prefix}/` like the upstream publishDir, qsv rowskey concat into `gunc_checkm_summary.tsv` |
| CATPACK_BINS / ADDNAMES / SUMMARISE (--cat_db) | `09_catpack.oxoflow`, 38 rules gated on `config.cat_db` | `cat_db_preparation` unpacks the archive/directory and locates the `db/` + `tax/` directories; `CAT_pack bins` per (assembler, binner) group with the upstream `-d -t -s .fa` args (input bins decompressed to a scratch `input_bins/`), results published to `Taxonomy/CAT/{assembler}/{binner}/{sample}/bins/`; `CAT_pack add_names` (with `--only_official` unless `cat_allow_unofficial_lineages=true`) and `CAT_pack summarise` (only with the official-lineage default, as upstream) per group; a header-keeping sorted `bat_summary.tsv` replicates upstream `collectFile keepHeader + sort 'deep'`; `cat=6.0.1` + `gzip=1.14` in `envs/catpack.yaml` |
| GENOMAD_ENDTOEND (--run_virus_identification) | `10_virus_identification.oxoflow`, 3 rules gated on `config.run_virus_identification` | `genomad_db_preparation` unpacks the archive/directory; `genomad end-to-end` per assembly (SPAdes scaffolds + MEGAHIT contigs) with the upstream default args `--cleanup --min-score 0.7 --splits 1`, output `.fna`/`.faa` gzipped and the whole per-sample dir moved to `VirusIdentification/geNomad/{sample}/` like the upstream publishDir; degenerate empty results touch the declared outputs instead of crashing; `genomad=1.11.2` in `envs/genomad.yaml` |
| TIARA_TIARA / TIARA_CLASSIFY (--bin_domain_classification) | `08_domain.oxoflow`, 39 rules gated on `config.bin_domain_classification` | `tiara --probabilities` per assembly, FASTATOCONTIG2BIN per (assembler, binner, bins/unbins) group, `domain_classification.R --join_prokaryotes` per group, one qsv-concatenated `tiara_summary.tsv`; unbins groups exist only for the three binners upstream splits (MetaBAT2, MaxBin2, MetaBinner); only the classification tables are published (as upstream) |

### Gated branches (all off by default, one config key each)

| Branch | Config key | Rules | Upstream process |
|--------|-----------|-------|------------------|
| AdapterRemoval clipping | `clip_tool = "adapterremoval"` | 1 | `ADAPTERREMOVAL` (nf-core/adapterremoval 2.3.2) |
| Trimmomatic clipping | `clip_tool = "trimmomatic"` | 1 | `TRIMMOMATIC` (nf-core/trimmomatic 0.39) |
| Host read removal | `host_fasta = "path/to/host.fna"` | 2 | `HOST_REMOVAL_BUILD`, `HOST_REMOVAL_ALIGN` (bowtie2; `host_fasta_bowtie2index` skips the build, `host_removal_verysensitive` toggles `--very-sensitive`) |
| Read normalization | `bbnorm = true` | 1 | `BBNORM` (bbmap 39.18, params `bbnorm_target`/`bbnorm_min`) |
| DAS Tool bin refinement | `refine_bins_dastool = true` | 28 | `BINNING_REFINEMENT` subworkflow (`refine_bins_dastool_threshold`) |
| CheckM bin QC | `run_checkm = true` | 25 | `CHECKM_LINEAGEWF` + `CHECKM_QA` (checkm-genome 1.2.5); feeds the GTDB-Tk filter (`checkm_db` optional local lineage DB) |
| CheckM2 bin QC | `run_checkm2 = true` | 13 | `CHECKM2_PREDICT` + `CONCAT_CHECKM2_TSV` (checkm2 1.1.0, `checkm2_db`); feeds the GTDB-Tk filter |
| GUNC contamination QC | `run_gunc = true` | 13 | `GUNC_RUN` + `CONCAT_GUNC_TSV` (gunc 1.1.0, `gunc_db`); with `run_checkm` also 13 `GUNC_MERGECHECKM` rules + `CONCAT_GUNC_CHECKM_TSV` |
| Tiara domain classification | `bin_domain_classification = true` | 39 | `TIARA` subworkflow (tiara 1.0.3, `tiara_min_length`) |
| CAT/BAT bin classification | `cat_db = "path/to/db.tar.gz"` | 38 | `CAT/BAT` subworkflow bins column (cat 6.0.1; `cat_allow_unofficial_lineages` toggles `--only_official`) |
| Virus identification | `run_virus_identification = true` | 3 | `GENOMAD_ENDTOEND` (genomad 1.11.2, `genomad_db`) |
| Long-read assembly and binning | `long_reads = "reads.fastq.gz"` (+ `long_reads_platform`) | 10 | `FLYE` + `MetaMDBG` + minimap2 binning prep + MetaBAT2/MaxBin2/CONCOCT (see `modules/12_longreads.oxoflow`; the QC/polish/host-removal wrappers upstream runs around this are not ported — see Not ported) |
| Ancient DNA | `ancient_dna = true` | 7 | pydamage analyze/filter (megahit + spades), freebayes/bcftools ancient consensus (`modules/11_ancient_dna.oxoflow`) |
| CAT/BAT unbinned-contigs classification | `cat_db` + `cat_classify_unbinned = true` | 16 | second `CAT_pack` pass over the chunked contigs (`modules/09_catpack.oxoflow`) |

Each gate activates exactly its own branch: with the default config the executed plan (134 rules of 352 total) is identical to the pre-branch port, and toggling one key adds only that branch's rules (verified by `dry-run` per key).

### Not ported (with reasons)

- **Long-read preprocessing QC** (chopper / nanoq / nanolyse / porechop(+abi) / filtlong / nanoplot; upstream `preprocessing_longread`, QC on by default — `skip_longread_qc=false`): upstream long-read path trims/filters/QC-reports raw reads before assembly; the port long-read branch (`config.long_reads`) takes QC-passed FASTQ instead.
- **Long-read host removal** (upstream `hostremoval_longread`, minimap2 + samtools chain): runs upstream when `host_fasta` is supplied; the port removes hosts on the short-read path only.
- **SPAdesHybrid / pypolca** (upstream hybrid assembly `assembly_hybrid` + short-read polish `PYPOLCA_RUN` of long-read assemblies): not ported.
- **metaeuk / mmseqs** (upstream `metaeuk/easypredict` gene prediction + `mmseqs/databases` download): not ported.
- **BigMAG summary** (`generate_bigmag_file`, upstream `PREPARE_BIGMAG_SUMMARY`): not ported.
- **Kaiju**: absent from upstream 5.5.0 entirely (removed upstream) — there is no module script to translate. **Diamond**: no standalone diamond profiling process exists upstream (only an optional `diamond_table` input the CAT/BAT modules accept but the workflow never supplies) — nothing user-facing to port.
- **Multi-library lanes** (upstream `--input` samplesheet rows listing several FASTQ pairs per sample; upstream merges lanes with `seqtk mergepe`): the port's reads_sheet covers one stream per row (`pe` / `single` / `interleaved`); a sample assembled from multiple paired libraries would need lane-concatenation rules that the port does not ship.
- **Pydamage report page**: not part of the 7-rule ancient DNA branch above; the CheckM2 and GUNC report pages are ported with their tools.
- **nf-core boilerplate files** (pipeline_summary, methods_description): not analysis output. The `versions.yml` half is covered by the engine-native export (`oxo-flow report --versions-yml <file> main.oxoflow`, see table).

## Links

- Repository: [oxo-flow-mag](https://github.com/oxo-flow-community/oxo-flow-mag)
- Upstream: [nf-core/mag](https://github.com/nf-core/mag) @ `5.5.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
