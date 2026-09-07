---
title: "Viral assembly and intrahost variant calling for Illumina amplicon data"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-viralrecon</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Viral assembly and intrahost variant calling for Illumina amplicon data</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span><span class=ox-tag-sep></span><span class="ox-tag">viral</span><span class="ox-tag">sars-cov-2</span><span class="ox-tag">amplicon</span><span class="ox-tag">metagenomic</span><span class="ox-tag">variant-calling</span><span class="ox-tag">assembly</span><span class="ox-tag">nf-core</span><span class="ox-tag">illumina</span></div>
<p class="ox-desc">Turns paired-end Illumina reads into a complete viral genomics report: read QC and trimming (FastQC, fastp), host-sequence removal (Kraken2), alignment to a user-provided reference genome (Bowtie2), primer trimming for amplicon runs, intrahost variant calling and annotation (iVar or bcftools, snpEff/SnpSift), consensus building with low-coverage masking (bcftools or ivar), lineage assignment and deconvolution (Pangolin, Nextclade, Freyja), de novo assembly with QC (SPAdes, Unicycler, minia, Bandage, BLAST, QUAST, ABACAS, plasmidID), and a single MultiQC report. The amplicon + iVar path is the default; the bcftools caller, ivar consensus, metagenomic protocol, alternative assemblers (any comma-separated combination of spades/unicycler/minia in one run), MarkDuplicates, plasmidID, network-driven database updates and additional annotation are ported as gated branches off by default.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-viralrecon" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow --samples first:1</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">84</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 12 CPUs / 72 GB per rule</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/nf-core/viralrecon">nf-core/viralrecon</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>3.0.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2287.1"><code>10.48546/workflowhub.workflow.2287.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">abacas</span><span class="tchip">bandage</span><span class="tchip">bcftools</span><span class="tchip">bedtools</span><span class="tchip">blast</span><span class="tchip">bowtie2</span><span class="tchip">cutadapt</span><span class="tchip">fastp</span></div></div>
<p class="cmd">$ oxo-flow run main.oxoflow --samples first:1</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>Viral genome reconstruction pipeline</strong> (nf-core/viralrecon port): given Illumina amplicon reads plus a viral FASTA, GFF, and primer scheme, it trims, aligns, calls and annotates intrahost variants, calls consensus and lineages, assembles de novo, and reports it all in MultiQC.</p>
<p><strong>1. Reference preparation</strong> — <code>gunzip_fasta</code>, <code>gunzip_gff</code>, and <code>gunzip_primer_bed</code> uncompress gzipped references; <code>prepare_genome</code> indexes the FASTA while <code>build_bowtie2_index</code>, <code>build_snpeff_db</code>, <code>make_blast_db</code>, and <code>get_nextclade_dataset</code> build the alignment, snpEff, BLAST, and Nextclade databases. <code>collapse_primers</code> and <code>get_primer_fasta</code> prepare amplicon intervals and primer sequences; <code>untar_kraken2_db</code> or <code>kraken2_build</code> supplies the host database.</p>
<p><strong>2. Read QC and alignment</strong> — <code>cat_fastq</code> concatenates per-sample reads, <code>fastp</code> trims them, and <code>fastqc_raw</code>/<code>fastqc_trim</code> check pre- and post-trim quality. <code>kraken2</code> strips host reads, <code>align_bowtie2</code> maps the trimmed reads, <code>bam_sort_index</code> sorts and indexes the BAM, and the amplicon branch's <code>ivar_trim</code> → <code>bam_sort_index_trimmed</code> removes primer sequences.</p>
<p><strong>3. Coverage and lineage deconvolution</strong> — <code>picard_metrics</code> collects alignment metrics, <code>mosdepth_genome</code> → <code>plot_mosdepth_genome</code> and <code>mosdepth_amplicon</code> → <code>plot_mosdepth_amplicon</code> plot coverage, and <code>freyja_variants</code> feeds <code>freyja_demix</code> and <code>freyja_boot</code>; if the database must be downloaded, <code>freyja_update</code> feeds <code>freyja_demix_updated</code>/<code>freyja_boot_updated</code> instead.</p>
<p><strong>4. Variant calling, annotation, and consensus</strong> — <code>call_variants_ivar</code> → <code>ivar_to_vcf</code> → <code>sort_vcf</code> is the amplicon default; the metagenomic <code>call_variants_bcftools</code> → <code>norm_vcf_bcftools</code> covers untrimmed runs. Both converge on <code>snpeff_ann</code> → <code>snpsift_extract</code>, and after <code>consensus_filter</code>/<code>consensus_filter_bcftools</code>, <code>consensus_call</code> (or <code>consensus_ivar</code>) emits the consensus feeding <code>quast_consensus</code>, <code>nextclade</code> → <code>nextclade_clade_mqc</code>, <code>pangolin</code>, and <code>plot_base_density</code>.</p>
<p><strong>5. Variant long table and assembly</strong> — <code>variants_long_table</code> and its bcftools counterpart <code>variants_long_table_bcftools</code> merge called variants, snpEff fields, and Pangolin lineages. In parallel, <code>cutadapt</code> primer-trims the host-stripped reads that <code>assemble_spades</code> (or <code>assemble_unicycler</code>, <code>assemble_minia</code>) scaffolds; each assembler branch adds BLAST, QUAST, and ABACAS rules (<code>blast_assembly</code>, <code>quast_assembly_minia</code>) plus Bandage and plasmidID.</p>
<p><strong>6. Report aggregation</strong> — <code>multiqc</code> collates quality, alignment, coverage, variant, and lineage metrics into one HTML report.</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-viralrecon+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>


<div class="ox-tryit">
<div class="ox-tryit-title">⬡ Try it — clone &amp; run</div>
<pre class="ox-tryit-cmd" data-copy="git clone https://github.com/oxo-flow-community/oxo-flow-viralrecon.git &amp;&amp; cd oxo-flow-viralrecon &amp;&amp; oxo-flow run main.oxoflow --samples first:1">git clone https://github.com/oxo-flow-community/oxo-flow-viralrecon.git
cd oxo-flow-viralrecon
oxo-flow run main.oxoflow --samples first:1</pre>
<p class="ox-tryit-note">The repository ships test fixtures (e.g. <code>test/fixtures/generate_fixtures.py</code>, <code>test/fixtures/raw/S1_R1.fastq.gz</code>, <code>test/fixtures/raw/S1_R2.fastq.gz</code>, <code>test/fixtures/raw/S2_R1.fastq.gz</code>) — point <code>input</code> at them or use the built-in sample group to <code>dry-run</code> first.</p>
</div>


## Run it

```bash
oxo-flow run main.oxoflow --samples first:1
```

Needs a reference genome bundle — see Requirements; `--samples first:1` runs a single sample.

## Installation

**Engine.** oxo-flow >= 0.17.0

**Toolchain.** conda envs — pinned versions (envs/*.yaml, conda-forge + bioconda channels; no containers)

**Requirements.**

- reference genome FASTA and annotation GFF (config.fasta / config.gff) — uncompressed by default, or set fasta_ends_gz / gff_ends_gz
- primer scheme BED for the amplicon protocol (config.primer_bed)
- Kraken2 host-removal database as a tar.gz (config.kraken2_db)
- Pangolin data directory (config.pango_database) and Freyja barcodes/lineages CSVs (config.freyja_barcodes / config.freyja_lineages)
- Nextclade dataset: downloaded automatically by default; set config.nextclade_dataset to a local dataset directory to skip the download
- paired-end Illumina FASTQs at <raw_dir>/<sample>_R1.fastq.gz and _R2.fastq.gz (config.raw_dir)
- compute: up to 12 CPUs / 72 GB per rule (resource pool queues rather than oversubscribes)
- conda or mamba to build the pinned per-rule environments

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-viralrecon
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-viralrecon
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy additional_annotation = value" data-copy="additional_annotation = ">additional_annotation</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">--- Additional annotation (upstream params.additional_annotation; empty =<br>off. A GFF/GTF to annotate the variants with in addition to the main<br>reference annotation, run through snpEff + SnpSift + the variants long<br>table. .gz files are gunzipped by build_snpeff_db_additional.) ---<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy assemblers = value" data-copy="assemblers = spades">assemblers</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>spades</code></td>
<td class="ox-p-desc">--- Assembly (upstream params.assemblers is a comma-separated list, e.g.<br>&#x27;spades,unicycler&#x27;; the port&#x27;s when-language has no &#x27;in&#x27; operator, so<br>every combination of the three assemblers is enumerated with explicit<br>equality tests. Give the canonical lowercase form, commas with no<br>spaces: &#x27;spades&#x27; | &#x27;unicycler&#x27; | &#x27;minia&#x27; | &#x27;spades,unicycler&#x27; | ... ) ---<br><span class="ox-param-usedby">used by <code>17</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy consensus_caller = value" data-copy="consensus_caller = bcftools">consensus_caller</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>bcftools</code></td>
<td class="ox-p-desc">--- Consensus caller (upstream params.consensus_caller; both the bcftools<br>and ivar branches are ported as when-gated rules) ---<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta = value" data-copy="fasta = reference/genome.fa">fasta</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>reference/genome.fa</code></td>
<td class="ox-p-desc">The port expects uncompressed files at these paths. Set the *_ends_gz keys<br>to true to run the upstream GUNZIP_* steps first (outputs land at the same<br>fixed reference/ paths).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fasta_ends_gz = value" data-copy="fasta_ends_gz = false">fasta_ends_gz</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">The port expects uncompressed files at these paths. Set the *_ends_gz keys<br>to true to run the upstream GUNZIP_* steps first (outputs land at the same<br>fixed reference/ paths).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy filter_duplicates = value" data-copy="filter_duplicates = false">filter_duplicates</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream params.filter_duplicates (default false) — passed to<br>PICARD_MARKDUPLICATES as REMOVE_DUPLICATES=true when set<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freyja_barcodes = value" data-copy="freyja_barcodes = test/fixtures/refs/freyja_barcodes.csv">freyja_barcodes</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/freyja_barcodes.csv</code></td>
<td class="ox-p-desc">--- Freyja (upstream --freyja_barcodes / --freyja_lineages. When either is<br>left empty the gated rules freyja_update + freyja_demix_updated /<br>freyja_boot_updated download and use the upstream DB instead.) ---<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freyja_db_name = value" data-copy="freyja_db_name = reference/freyja_db">freyja_db_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>reference/freyja_db</code></td>
<td class="ox-p-desc">upstream params.freyja_db_name — where FREYJA_UPDATE writes its download<br>(upstream default &#x27;freyja_db&#x27;; the port points into reference/)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freyja_depthcutoff = value" data-copy="freyja_depthcutoff = 0">freyja_depthcutoff</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>0</code></td>
<td class="ox-p-desc">freyja&#x27;s meta format is the curated_lineages JSON (buildLineageMap<br>json.loads it — live: the CSV default died in freyja boot with<br>JSONDecodeError); the CSV sibling is kept as the barcodes-side table<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freyja_lineages = value" data-copy="freyja_lineages = test/fixtures/refs/freyja_lineages.json">freyja_lineages</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/freyja_lineages.json</code></td>
<td class="ox-p-desc">freyja&#x27;s meta format is the curated_lineages JSON (buildLineageMap<br>json.loads it — live: the CSV default died in freyja boot with<br>JSONDecodeError); the CSV sibling is kept as the barcodes-side table<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freyja_repeats = value" data-copy="freyja_repeats = 100">freyja_repeats</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>100</code></td>
<td class="ox-p-desc">freyja&#x27;s meta format is the curated_lineages JSON (buildLineageMap<br>json.loads it — live: the CSV default died in freyja boot with<br>JSONDecodeError); the CSV sibling is kept as the barcodes-side table<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gff = value" data-copy="gff = reference/genome.gff">gff</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>reference/genome.gff</code></td>
<td class="ox-p-desc">The port expects uncompressed files at these paths. Set the *_ends_gz keys<br>to true to run the upstream GUNZIP_* steps first (outputs land at the same<br>fixed reference/ paths).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy gff_ends_gz = value" data-copy="gff_ends_gz = false">gff_ends_gz</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">The port expects uncompressed files at these paths. Set the *_ends_gz keys<br>to true to run the upstream GUNZIP_* steps first (outputs land at the same<br>fixed reference/ paths).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ivar_trim_noprimer = value" data-copy="ivar_trim_noprimer = false">ivar_trim_noprimer</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream params.min_mapped_reads — the per-sample channel DROP is a<br>documented runtime-filter deviation (no dynamic DAG); the reporting half<br>(fail_mapped_samples_mqc.tsv in the MultiQC data) is ported inside the<br>multiqc rule<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy ivar_trim_offset = value" data-copy="ivar_trim_offset = ">ivar_trim_offset</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream params.min_mapped_reads — the per-sample channel DROP is a<br>documented runtime-filter deviation (no dynamic DAG); the reporting half<br>(fail_mapped_samples_mqc.tsv in the MultiQC data) is ported inside the<br>multiqc rule<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kraken2_assembly_host_filter = value" data-copy="kraken2_assembly_host_filter = true">kraken2_assembly_host_filter</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">upstream params.kraken2_db_name — the library KRAKEN2_BUILD downloads when<br>kraken2_db is left empty (gated rule kraken2_build)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kraken2_db = value" data-copy="kraken2_db = reference/kraken2_db.tar.gz">kraken2_db</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>reference/kraken2_db.tar.gz</code></td>
<td class="ox-p-desc">Kraken2 host-removal database (upstream --kraken2_db, tar.gz)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kraken2_db_name = value" data-copy="kraken2_db_name = human">kraken2_db_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>human</code></td>
<td class="ox-p-desc">upstream params.kraken2_db_name — the library KRAKEN2_BUILD downloads when<br>kraken2_db is left empty (gated rule kraken2_build)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy kraken2_variants_host_filter = value" data-copy="kraken2_variants_host_filter = false">kraken2_variants_host_filter</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream params.kraken2_db_name — the library KRAKEN2_BUILD downloads when<br>kraken2_db is left empty (gated rule kraken2_build)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_contig_length = value" data-copy="min_contig_length = 200">min_contig_length</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>200</code></td>
<td class="ox-p-desc">Consensus QC<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_mapped_reads = value" data-copy="min_mapped_reads = 1000">min_mapped_reads</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>1000</code></td>
<td class="ox-p-desc">upstream params.min_mapped_reads — the per-sample channel DROP is a<br>documented runtime-filter deviation (no dynamic DAG); the reporting half<br>(fail_mapped_samples_mqc.tsv in the MultiQC data) is ported inside the<br>multiqc rule<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy min_perc_contig_aligned = value" data-copy="min_perc_contig_aligned = 0.7">min_perc_contig_aligned</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.7</code></td>
<td class="ox-p-desc">Consensus QC<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy multiqc_title = value" data-copy="multiqc_title = ">multiqc_title</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">MultiQC<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nextclade_dataset = value" data-copy="nextclade_dataset = ">nextclade_dataset</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">Nextclade dataset (upstream genome config for MN908947.3)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nextclade_dataset_name = value" data-copy="nextclade_dataset_name = sars-cov-2">nextclade_dataset_name</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>sars-cov-2</code></td>
<td class="ox-p-desc">Nextclade dataset (upstream genome config for MN908947.3)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy nextclade_dataset_tag = value" data-copy="nextclade_dataset_tag = 2024-10-17--16-48-48Z">nextclade_dataset_tag</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>2024-10-17--16-48-48Z</code></td>
<td class="ox-p-desc">Nextclade dataset (upstream genome config for MN908947.3)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy out_dir = value" data-copy="out_dir = results">out_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>results</code></td>
<td class="ox-p-desc">Directory holding raw/&lt;sample&gt;_R1.fastq.gz + raw/&lt;sample&gt;_R2.fastq.gz.<br>The repo default ships the tiny test fixtures; point this at your data.<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy pango_database = value" data-copy="pango_database = test/fixtures/refs/pangolin_db">pango_database</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/refs/pangolin_db</code></td>
<td class="ox-p-desc">--- Pangolin (upstream --pango_database; a directory. When left empty the<br>gated rules pangolin_updatedata + pangolin_run_updated download the<br>data directory instead, mirroring upstream PANGOLIN_UPDATEDATA.) ---<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy platform = value" data-copy="platform = illumina">platform</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>illumina</code></td>
<td class="ox-p-desc">Platform / protocol<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy primer_bed = value" data-copy="primer_bed = reference/primers.bed">primer_bed</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>reference/primers.bed</code></td>
<td class="ox-p-desc">The port expects uncompressed files at these paths. Set the *_ends_gz keys<br>to true to run the upstream GUNZIP_* steps first (outputs land at the same<br>fixed reference/ paths).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy primer_bed_ends_gz = value" data-copy="primer_bed_ends_gz = false">primer_bed_ends_gz</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">The port expects uncompressed files at these paths. Set the *_ends_gz keys<br>to true to run the upstream GUNZIP_* steps first (outputs land at the same<br>fixed reference/ paths).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy primer_left_suffix = value" data-copy="primer_left_suffix = _LEFT">primer_left_suffix</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>_LEFT</code></td>
<td class="ox-p-desc">Primer trimming for assembly<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy primer_right_suffix = value" data-copy="primer_right_suffix = _RIGHT">primer_right_suffix</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>_RIGHT</code></td>
<td class="ox-p-desc">Primer trimming for assembly<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy protocol = value" data-copy="protocol = amplicon">protocol</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>amplicon</code></td>
<td class="ox-p-desc">Platform / protocol<br><span class="ox-param-usedby">used by <code>31</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy raw_dir = value" data-copy="raw_dir = test/fixtures/raw">raw_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/raw</code></td>
<td class="ox-p-desc">Directory holding raw/&lt;sample&gt;_R1.fastq.gz + raw/&lt;sample&gt;_R2.fastq.gz.<br>The repo default ships the tiny test fixtures; point this at your data.<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy save_mpileup = value" data-copy="save_mpileup = false">save_mpileup</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream params.save_mpileup — when true, call_variants_ivar tees the<br>samtools mpileup stream to variants/ivar/{sample}.mpileup (off by<br>default, exactly like upstream; the port emits an empty placeholder when<br>false so the declared output stays present)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy save_trimmed_fail = value" data-copy="save_trimmed_fail = false">save_trimmed_fail</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream params.save_trimmed_fail — when true, fastp keeps the<br>reads that failed filtering (--failed_out + --unpaired1/2); off by<br>default, exactly like upstream (empty placeholders when false)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy save_unaligned = value" data-copy="save_unaligned = false">save_unaligned</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream params.save_unaligned — NOT ported as a gate: the Kraken2<br>unclassified reads feed the assembly branch (upstream channel wiring),<br>so they always land in results/kraken2/ — the flag is effectively always<br>on in the port (benign over-emission vs upstream&#x27;s default publish)<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_abacas = value" data-copy="skip_abacas = false">skip_abacas</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_assembly = value" data-copy="skip_assembly = false">skip_assembly</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>22</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_assembly_quast = value" data-copy="skip_assembly_quast = false">skip_assembly_quast</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_bandage = value" data-copy="skip_bandage = false">skip_bandage</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_blast = value" data-copy="skip_blast = false">skip_blast</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_consensus = value" data-copy="skip_consensus = false">skip_consensus</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>14</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_consensus_plots = value" data-copy="skip_consensus_plots = false">skip_consensus_plots</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_cutadapt = value" data-copy="skip_cutadapt = false">skip_cutadapt</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastp = value" data-copy="skip_fastp = false">skip_fastp</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_fastqc = value" data-copy="skip_fastqc = false">skip_fastqc</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_freyja = value" data-copy="skip_freyja = false">skip_freyja</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_freyja_boot = value" data-copy="skip_freyja_boot = false">skip_freyja_boot</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_ivar_trim = value" data-copy="skip_ivar_trim = false">skip_ivar_trim</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_kraken2 = value" data-copy="skip_kraken2 = false">skip_kraken2</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_markduplicates = value" data-copy="skip_markduplicates = true">skip_markduplicates</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_mosdepth = value" data-copy="skip_mosdepth = false">skip_mosdepth</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_nextclade = value" data-copy="skip_nextclade = false">skip_nextclade</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_noninternal_primers = value" data-copy="skip_noninternal_primers = false">skip_noninternal_primers</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_pangolin = value" data-copy="skip_pangolin = false">skip_pangolin</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_picard_metrics = value" data-copy="skip_picard_metrics = false">skip_picard_metrics</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_plasmidid = value" data-copy="skip_plasmidid = true">skip_plasmidid</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>true</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_snpeff = value" data-copy="skip_snpeff = false">skip_snpeff</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>5</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_variants = value" data-copy="skip_variants = false">skip_variants</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>33</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_variants_long_table = value" data-copy="skip_variants_long_table = false">skip_variants_long_table</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_variants_quast = value" data-copy="skip_variants_quast = false">skip_variants_quast</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip flags (identical defaults to upstream params)<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy spades_mode = value" data-copy="spades_mode = rnaviral">spades_mode</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>rnaviral</code></td>
<td class="ox-p-desc">--- Assembly (upstream params.assemblers is a comma-separated list, e.g.<br>&#x27;spades,unicycler&#x27;; the port&#x27;s when-language has no &#x27;in&#x27; operator, so<br>every combination of the three assemblers is enumerated with explicit<br>equality tests. Give the canonical lowercase form, commas with no<br>spaces: &#x27;spades&#x27; | &#x27;unicycler&#x27; | &#x27;minia&#x27; | &#x27;spades,unicycler&#x27; | ... ) ---<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy threeprime_adapters = value" data-copy="threeprime_adapters = false">threeprime_adapters</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Primer trimming for assembly<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy variant_caller = value" data-copy="variant_caller = ivar">variant_caller</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>ivar</code></td>
<td class="ox-p-desc">--- Variant calling (upstream params.variant_caller defaults to &#x27;ivar&#x27; for<br>the amplicon protocol and &#x27;bcftools&#x27; otherwise; both branches are<br>ported as when-gated rules). The metagenomic branch auto-runs the<br>bcftools caller regardless of this key — upstream derives<br>variant_caller in nextflow.config (params.variant_caller = protocol ==<br>&#x27;metagenomic&#x27; ? &#x27;bcftools&#x27; : &#x27;ivar&#x27;), and the port mirrors that<br>derivation in the wgs rules&#x27; when conditions, so a metagenomic run<br>needs no extra --arg ---<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view">
<summary>Exact rule DAG (multi-route truth — operational view)</summary>
<div class="ox-dag-card ox-dag-card--wide">
<a href="/assets/dag/oxo-flow-viralrecon-rules.svg?v=7012af587b" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-viralrecon-rules.svg?v=7012af587b" alt="oxo-flow-viralrecon rule-level detail" loading="lazy"></a>
</div>
</details>
<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card" markdown="1">

<a href="/assets/dag/oxo-flow-viralrecon.svg?v=6492441e7b" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-viralrecon.svg?v=6492441e7b" alt="oxo-flow-viralrecon pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-viralrecon — Turns paired-end Illumina reads into a complete viral genomics report: read QC and trimming (FastQC, fastp), host-sequence removal (Kraken2), alignment to a user-provided reference genome (Bowtie2), primer trimming for amplicon runs, intrahost variant calling and annotation (iVar or bcftools, snpEff/SnpSift), consensus building with low-coverage masking (bcftools or ivar), lineage assignment and deconvolution (Pangolin, Nextclade, Freyja), de novo assembly with QC (SPAdes, Unicycler, minia, Bandage, BLAST, QUAST, ABACAS, plasmidID), and a single MultiQC report.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- gunzip_fasta
- gunzip_gff
- gunzip_primer_bed
- prepare_genome
- untar_kraken2_db
- kraken2_build
- collapse_primers
- get_primer_fasta
- build_bowtie2_index
- get_nextclade_dataset
- make_blast_db
- build_snpeff_db
- cat_fastq
- fastqc_raw
- fastp
- fastqc_trim
- kraken2
- align_bowtie2
- bam_sort_index
- ivar_trim
- bam_sort_index_trimmed
- markduplicates
- markduplicates_wgs
- picard_metrics
- picard_metrics_wgs
- mosdepth_genome
- mosdepth_genome_wgs
- plot_mosdepth_genome
- mosdepth_amplicon
- plot_mosdepth_amplicon
- freyja_variants
- freyja_variants_wgs
- freyja_demix
- freyja_boot
- freyja_update
- freyja_demix_updated
- freyja_boot_updated
- call_variants_ivar
- ivar_to_vcf
- sort_vcf
- call_variants_bcftools
- call_variants_bcftools_wgs
- norm_vcf_bcftools
- snpeff_ann
- snpsift_extract
- consensus_filter
- consensus_filter_bcftools
- consensus_call
- consensus_call_wgs
- consensus_ivar
- consensus_ivar_wgs
- quast_consensus
- pangolin
- pangolin_updatedata
- pangolin_run_updated
- nextclade
- plot_base_density
- nextclade_clade_mqc
- variants_long_table
- variants_long_table_bcftools
- build_snpeff_db_additional
- additional_annotation
- assembly_fastq
- prepare_primer_fasta
- cutadapt
- fastqc_primers
- assemble_spades
- bandage
- blast_assembly
- quast_assembly
- abacas
- assemble_unicycler
- bandage_unicycler
- blast_assembly_unicycler
- quast_assembly_unicycler
- abacas_unicycler
- assemble_minia
- blast_assembly_minia
- quast_assembly_minia
- abacas_minia
- plasmidid
- plasmidid_unicycler
- plasmidid_minia
- multiqc

**Excluded**

- nanopore platform branch (ARTIC_GUPPYPLEX, ARTIC_MINION, NANOPLOT, PYCOQC, VCFLIB_VCFUNIQ, PREPARE_GENOME_NANOPORE) — upstream discovers per-barcode read directories (fastq_dir/barcode* + sequencing_summary, workflows/viralrecon.nf:693-920) with single-end meta flags, requires ONT reads basecalled by the commercial guppy_basecaller/guppy_barcoder, and no port-side nanopore fixture exists (upstream ships nanopore nf-tests: tests/test_nanopore.nf.test); the port is paired-end Illumina filesystem discovery only (structural)
- channel-level runtime filters, partially adopted — the fastp empty-after-filtering drop IS ported as `reads_count('fastp/{sample}_1.fastp.fastq.gz') > 0` gates on the trimmed-reads consumers (kraken2, align_bowtie2, assembly_fastq; engine 0.17.0 `when` runtime functions). The remaining DROPS are documented deviations: the min_mapped_reads flagstat gate (a strict `>` on the mapped count parsed out of samtools flagstat text — no engine runtime fn can extract it, so only the reporting half is ported as fail_mapped_samples_mqc.tsv inside the multiqc rule) and the zero-variant-sample filters (ivar: `wc_lines(tsv) > 1` is expressible but the port deliberately keeps zero-variant samples flowing downstream with a placeholder-header VCF for live-fixture robustness; bcftools: the record count needs a regex over `bcftools stats` output — fail_mapped_reads_mqc.tsv reports fastp failures inside the multiqc rule)

## Fidelity

Every upstream process and subworkflow on the default path, and what happened
to it in this port:

| Upstream process (module) | Port rule | Notes |
| --- | --- | --- |
| CAT_FASTQ | `cat_fastq` | `cat` to `fastp/{sample}_{1,2}.fastq.gz` |
| FASTQC_RAW | `fastqc_raw` | same args; upstream input-rename step kept (reads symlinked to `{sample}_{1,2}.fastq.gz` before FastQC so output names match), then renamed into `results/fastqc/raw/` |
| FASTP | `fastp` | `ext.args` baked in verbatim (cut_front/cut_tail/trim_poly_x/cut_mean_quality 30/...) + `--detect_adapter_for_pe`, `2>| >(tee log >&2)`; `save_trimmed_fail=true` adds upstream's `--failed_out {sample}.paired.fail.fastq.gz --unpaired1/2 {sample}_{1,2}.fail.fastq.gz` (off by default — empty placeholders) |
| FASTQC_TRIM | `fastqc_trim` | same args; upstream input-rename step kept (trimmed reads symlinked to `{sample}_{1,2}.fastq.gz` before FastQC), then renamed into `results/fastqc/trim/` |
| KRAKEN2_KRAKEN2 | `kraken2` | `--db` (local), `--report-zero-counts`, pigz of classified/unclassified pairs; gated on `skip_kraken2` + the fastp empty-reads drop (`reads_count(...) > 0` when-gate) |
| (channel wiring) | `assembly_fastq` | passthrough of fastp reads to `kraken2/{sample}.unclassified_*.fastq.gz` when host filtering is off — replaces upstream `ch_assembly_fastq = ch_variants_fastq`; see deviations |
| BOWTIE2_ALIGN | `align_bowtie2` | index found by `find -L` on `*.rev.1.bt2[l]`, `--local --very-sensitive-local --seed 1`, unmapped-filtered `samtools view -F4`, log tee'd; carries the fastp empty-reads drop when-gate |
| IVAR_TRIM | `ivar_trim` | `-m 30 -q 20 -e` (noprimer-gated), optional `-x offset`, log captured; gated amplicon |
| BAM_SORT_STATS_SAMTOOLS | `bam_sort_index_trimmed` | merged: `samtools cat` (single input, dropped) → sort → index → stats/flagstat/idxstats |
| (align branch) | `bam_sort_index` | same merged trio for the untrimmed BAM |
| PICARD_MARKDUPLICATES | `markduplicates` / `markduplicates_wgs` | gated `skip_markduplicates=false`; `--ASSUME_SORTED true --VALIDATION_STRINGENCY LENIENT --TMP_DIR tmp` + `REMOVE_DUPLICATES=true` when `filter_duplicates`; samtools index + stats/flagstat/idxstats; upstream replaces `ch_bam` with the marked BAM, the port keeps the pre-dedup BAM in the pipeline and publishes the marked BAM alongside (see deviations) |
| PICARD_COLLECTMULTIPLEMETRICS | `picard_metrics` | `-Xmx4800M` (= 6 GB task × 0.8), LENIENT, `--TMP_DIR tmp`, all 5 metric files + pdf |
| MOSDEPTH_AMPLICON | `mosdepth_amplicon` | `--fast-mode --use-median --thresholds 0,1,10,50,100,500 --by collapsed.bed` |
| MOSDEPTH_GENOME | `mosdepth_genome` | `--fast-mode --by 200` |
| PLOT_MOSDEPTH_REGIONS (×2) | `plot_mosdepth_genome` / `plot_mosdepth_amplicon` | glob-gather over `*.regions.bed.gz`, `all_samples.mosdepth.*` outputs |
| FREYJA_VARIANTS | `freyja_variants` | `--ref --variants --depths` |
| FREYJA_DEMIX | `freyja_demix` | `--output --barcodes --meta`, `--depthcutoff` when non-zero |
| FREYJA_BOOT | `freyja_boot` | `--nt --nb {freyja_repeats} --boxplot pdf`, boot outputs renamed to `{sample}.lineages.csv` / `{sample}_summarized.csv` |
| IVAR_VARIANTS | `call_variants_ivar` | `samtools mpileup` (`--ignore-overlaps --count-orphans --no-BAQ --max-depth 0 --min-BQ 0`) \| `ivar variants -t 0.25 -q 20 -m 10 -g -r -p`; `save_mpileup=true` tees the mpileup stream to `variants/ivar/{sample}.mpileup` (off by default — empty placeholder) |
| IVAR_VARIANTS_TO_VCF | `ivar_to_vcf` | `--ignore_strand_bias`, variant-counts log + header-cat MQC tsv |
| BCFTOOLS_SORT | `sort_vcf` | `--output --temp-dir .` (default `--output-type z`); process_medium label (6c/36 GB/8 h) |
| VCF_TABIX_STATS | `sort_vcf` | merged: tabix (`--threads -p vcf -f`) + `bcftools stats` |
| VARIANTS_BCFTOOLS | `call_variants_bcftools` / `call_variants_bcftools_wgs` + `norm_vcf_bcftools` | gated `variant_caller='bcftools'` (amplicon) or `protocol='metagenomic'` (auto, mirroring upstream's derived default — see deviations); mpileup (`--ignore-overlaps --count-orphans --no-BAQ --max-depth 0 --min-BQ 20`) \| `bcftools call` (`--ploidy 1 --multiallelic-caller`) \| reheader \| view `--include 'INFO/DP>=10'`, then `bcftools norm` (`--do-not-normalize --multiallelics -any`) merged with tabix + `bcftools stats` (VCF_TABIX_STATS); canonical `variants/ivar/` VCF paths shared with the ivar caller — 3.0.0 has no BCFTOOLS_MPILEUP_FILTER process, filtering lives in the BCFTOOLS_FILTER consensus-branch process |
| SNPEFF_ANN | `snpeff_ann` | `-Xmx36g`, `-config/-dataDir` locals, `-csvStats`, summary html move |
| VCF_BGZIP_TABIX_STATS | `snpeff_ann` | merged: bgzip + tabix + `bcftools stats` |
| SNPSIFT_EXTRACTFIELDS | `snpsift_extract` | same ANN[*]/EFF[*] field list, `-s "," -e "."` |
| BCFTOOLS_FILTER | `consensus_filter` / `consensus_filter_bcftools` | ivar-caller branch `--include 'FORMAT/ALT_FREQ >= 0.75'`; bcftools-caller branch `--include 'FORMAT/AD[:1] / FORMAT/DP >= 0.75'` (upstream ext.args, both filtered to the same canonical VCF) |
| TABIX_TABIX | `consensus_filter` | merged |
| IVAR_CONSENSUS (CONSENSUS_IVAR) | `consensus_ivar` / `consensus_ivar_wgs` | gated `consensus_caller='ivar'`; `samtools mpileup --count-orphans --no-BAQ --max-depth 0 --min-BQ 0 -aa` \| `ivar consensus -t 0.75 -q 20 -m 10 -n N`; writes the canonical `consensus/bcftools/{sample}.consensus.fa` path so downstream consensus-QC rules are shared (see deviations) |
| MAKE_BED_MASK | `consensus_call` | merged: mpileup `-a` + awk low-coverage (<10) positions + `make_bed_mask.py` |
| BEDTOOLS_MERGE | `consensus_call` | merged |
| BEDTOOLS_MASKFASTA | `consensus_call` | merged |
| BCFTOOLS_CONSENSUS | `consensus_call` | `cat fasta \| bcftools consensus` |
| RENAME_FASTA_HEADER | `consensus_call` | `sed "s/>/>{sample} /g"` (byte-identical to upstream) |
| QUAST (consensus) | `quast_consensus` | `-r --features --threads`, report.tsv symlink; batch run over the whole cohort into one `quast.consensus/` dir — upstream runs one QUAST per sample (`ext.prefix` → per-sample dirs), so MultiQC shows one aggregated sample row here instead of per-sample rows (numeric results equivalent) |
| PANGOLIN_RUN | `pangolin` | `XDG_CACHE_HOME=/tmp/.cache`, `--datadir --outfile --threads` |
| PANGOLIN_UPDATEDATA | `pangolin_updatedata` + `pangolin_run_updated` | gated `pango_database=''`; `pangolin --update-data --datadir reference/pangolin_db` then the same PANGOLIN_RUN shell against the downloaded data |
| NEXTCLADE_RUN | `nextclade` | `--jobs --input-dataset --output-all --output-basename` |
| PLOT_BASE_DENSITY | `plot_base_density` | same script args, `base_qc/` outputs |
| (channel code) | `nextclade_clade_mqc` | upstream builds `nextclade_clade_mqc.tsv` in Nextflow channel code (`getNextcladeFieldMapFromCsv` + `multiqcTsvFromList`); ported as an inline python gather over the per-sample CSVs |
| BCFTOOLS_QUERY | `variants_long_table` | `-H -f '%CHROM\t%POS...'` per sample |
| MAKE_VARIANTS_LONG_TABLE | `variants_long_table` / `variants_long_table_bcftools` | merged with query; symlink-collect pattern, `--variant_caller {config.variant_caller}`; bcftools-caller query reads the AD field (`[%AD\t]`), ivar query reads REF_DP/ALT_DP |
| FREYJA_UPDATE | `freyja_update` + `freyja_demix_updated` / `freyja_boot_updated` | gated when `freyja_barcodes` or `freyja_lineages` is empty; `freyja update --outdir {config.freyja_db_name}` then the same demix/boot shells against the downloaded DB |
| ADDITIONAL_ANNOTATION | `build_snpeff_db_additional` + `additional_annotation` | gated `additional_annotation` non-empty (off by default upstream); snpEff `-gff3` build of the extra annotation in a scratch dir, then per-sample snpEff ann + bgzip/tabix + SnpSift extract + query + `make_variants_long_table.py --variant_caller {config.variant_caller} --output_file additional_variants_long_table.csv` |
| PREPARE_PRIMER_FASTA | `prepare_primer_fasta` | `sed -r '/^[ACTGactg]+$/ s/^/X/g'` |
| CUTADAPT | `cutadapt` | `-Z --cores --overlap 5 --minimum-length 30 --error-rate 0.1 -g file: -G file:` |
| FASTQC (assembly) | `fastqc_primers` | prefix `{sample}.primer_trim` via symlink rename |
| SPADES | `assemble_spades` | `--{config.spades_mode} --memory 72` (upstream `ext.args`; default `rnaviral`), output renames (scaffolds/contigs/gfa gzipped, spades.log) |
| BANDAGE_IMAGE | `bandage` | `--height 1000`, png + svg; upstream GUNZIP_GFA merged in (Bandage 0.9.0 cannot read `.gz` graphs — `gzip -cd` to `{sample}.assembly.gfa` first) |
| BLAST_BLASTN | `blast_assembly` | `-outfmt '6 stitle staxids std slen qlen qcovs'`, DB `find -L *.nin`, header-cat |
| FILTER_BLASTN | `blast_assembly` | merged: awk `$16 > min_contig_length && $18 > min_perc_contig_aligned && $1 !~ /phage/` + header-cat |
| QUAST (assembly) | `quast_assembly` | gunzip of scaffolds in shell, `quast.spades/` dir + tsv symlink; batch run over the whole cohort into one `quast.spades/` dir — upstream runs one QUAST per sample (per-sample `S1.spades/` dirs), so MultiQC shows one aggregated sample row here instead of per-sample rows (numeric results equivalent) |
| ABACAS | `abacas` | `-m -p nucmer`, sorted `.bin`, nucmer delta/filtered/tiling + unused contigs moves |
| UNICYCLER | `assemble_unicycler` | gated on `assemblers` containing `unicycler`; `--threads` in a per-sample scratch dir (unicycler writes generic-named files), `mv assembly.fasta {sample}.scaffolds.fa` + gzip, `assembly.gfa` + log kept; BANDAGE/BLAST/QUAST/ABACAS QC chained as `bandage_unicycler` / `blast_assembly_unicycler` / `quast_assembly_unicycler` / `abacas_unicycler` |
| MINIA | `assemble_minia` | gated on `assemblers` containing `minia`; `-kmer-size 31 -abundance-min 20 -nb-cores {threads} -in input_files.txt`; BLAST/QUAST/ABACAS QC chained as `blast_assembly_minia` / `quast_assembly_minia` / `abacas_minia` (no Bandage: minia has no graph file, upstream runs Bandage only on the unicycler gfa) |
| PLASMIDID | `plasmidid` / `plasmidid_unicycler` / `plasmidid_minia` | gated `skip_plasmidid=false`; one rule per assembler branch, mirroring upstream ASSEMBLY_QC; `--only-reconstruct -C 47 -S 47 -i 60 --no-trim -k 0.80 -d reference/genome.fa` — plasmidID needs no database download (verified: only the reference fasta) |
| KRAKEN2_BUILD | `kraken2_build` | gated `kraken2_db=''`; `kraken2-build --download-taxonomy` + `--download-library {config.kraken2_db_name}` + `--build --threads` into `reference/kraken2_db` (upstream `params.kraken2_db_name`, default `human`) |
| (metagenomic branch) | `mosdepth_genome_wgs` / `picard_metrics_wgs` / `freyja_variants_wgs` / `consensus_call_wgs` / `markduplicates_wgs` / `call_variants_bcftools_wgs` / `consensus_ivar_wgs` | gated `protocol='metagenomic'`; the same shells as their amplicon counterparts running on the untrimmed `sorted.bam`, writing the same canonical outputs (exclusive gates; upstream 3.0.0 protocol enum has no `wgs` value — the port maps the non-amplicon branch to `metagenomic` and calls it `wgs` in rule names) |
| GUNZIP_FASTA/GFF/PRIMER_BED | `gunzip_fasta/gff/primer_bed` | gated on `*_ends_gz`; output to fixed `reference/` paths |
| UNTAR_KRAKEN2_DB | `untar_kraken2_db` | upstream single-top-level-dir strip logic kept + upstream `ext.args2 --no-same-owner` on both tar invocations |
| CUSTOM_GETCHROMSIZES | `prepare_genome` | `samtools faidx` + `cut -f 1,2` |
| COLLAPSE_PRIMERS | `collapse_primers` | `--left_primer_suffix/--right_primer_suffix`; process_medium label (6c/36 GB/8 h) |
| BEDTOOLS_GETFASTA | `get_primer_fasta` | `-s -nameOnly` |
| BOWTIE2_BUILD | `build_bowtie2_index` | `--seed 1 --threads`; process_high label (12c/72 GB/16 h) |
| NEXTCLADE_DATASETGET | `get_nextclade_dataset` | `--name sars-cov-2 --tag 2024-10-17--16-48-48Z` (v3pl tag of the MN908947.3 genome config); skips when a local `nextclade_dataset` path is set |
| BLAST_MAKEBLASTDB | `make_blast_db` | `-parse_seqids -dbtype nucl` |
| SNPEFF_BUILD | `build_snpeff_db` | `-Xmx12g`, `-gff3`, genomes/genome symlinks, `snpeff.config` echo |
| MULTIQC | `multiqc` | both passes kept (parse pass + `-e general_stats --ignore *nextclade_clade_mqc.tsv` final pass), `grep -q ">skip_assembly<"` / `>skip_variants<` / `platform=illumina` rm rules, `multiqc_config_illumina.yml`; inputs mirror upstream `ch_multiqc_files` — snpeff `-csvStats` per-sample csv added (SnpEff section), mosdepth fed as genome `global.dist.txt` (distribution plots) + amplicon `all_samples.mosdepth.coverage.tsv` (heatmap), with the genome `summary.txt` additionally kept for the General Stats table (the inert genome coverage.tsv and amplicon per-sample summary.txt are not fed); the runtime-filter reporting half is ported (fail_mapped_reads_mqc.tsv / fail_mapped_samples_mqc.tsv custom content, same headers/rows as upstream `multiqcTsvFromList`, written only when samples fail) |
| multiqc_to_custom_csv.py | `multiqc` | merged, `--platform illumina` → `variants_metrics_mqc.csv` / `assembly_metrics_mqc.csv` |

Ported branches (all gated off by default, mirroring the upstream
`params` defaults; the default run is byte-for-byte the amplicon ivar path):

- `variant_caller='bcftools'` — VARIANTS_BCFTOOLS (`call_variants_bcftools`,
  `norm_vcf_bcftools`), BCFTOOLS_FILTER (`consensus_filter_bcftools`) and the
  bcftools long table (`variants_long_table_bcftools`); activates with
  `--arg variant_caller=bcftools`, deactivating the ivar caller chain
- `consensus_caller='ivar'` — CONSENSUS_IVAR (`consensus_ivar`) with
  `--arg consensus_caller=ivar`
- non-amplicon (shotgun / "wgs") protocol — `--arg protocol=metagenomic`;
  the untrimmed-BAM counterparts `mosdepth_genome_wgs`, `picard_metrics_wgs`,
  `freyja_variants_wgs`, `consensus_call_wgs`, `markduplicates_wgs`,
  `call_variants_bcftools_wgs`, `consensus_ivar_wgs`; upstream derives
  `variant_caller='bcftools'` for non-amplicon runs (nextflow.config), and the
  port mirrors that derivation in the wgs rules' when conditions — a
  metagenomic run needs no extra `--arg`, the bcftools caller chain
  (`call_variants_bcftools_wgs`, `norm_vcf_bcftools`,
  `consensus_filter_bcftools`, `variants_long_table_bcftools`) runs
  automatically and the iVar caller chain stays amplicon-gated
- alternative assemblers — `--arg assemblers=unicycler` /
  `--arg assemblers=minia` or any comma-separated combination
  (`--arg assemblers=spades,unicycler` runs both in one run, like upstream)
  with their full QC chains (Bandage for spades and unicycler, matching
  upstream; plasmidID per assembler like upstream ASSEMBLY_QC)
- PICARD_MARKDUPLICATES — `--arg skip_markduplicates=false`
- PLASMIDID — `--arg skip_plasmidid=false` (no database download; verified
  upstream uses only the reference fasta)
- network downloads — `kraken2_build` (leave `kraken2_db` empty),
  `freyja_update` (leave `freyja_barcodes`/`freyja_lineages` empty),
  `pangolin_updatedata` (leave `pango_database` empty)
- ADDITIONAL_ANNOTATION — `--arg additional_annotation=path/to.gff`

Still excluded (see metadata.json): the nanopore platform
(ARTIC_GUPPYPLEX/ARTIC_MINION/NANOPLOT/PYCOQC/VCFLIB_VCFUNIQ — upstream
wires per-barcode read channels with single-end meta flags, guppybasecaller
is a commercial ONT tool and no port-side nanopore fixture exists (upstream ships its own nanopore nf-tests — tests/test_nanopore.nf.test, conf/test_full_nanopore.config); structural) and the
remaining runtime-filter DROPS — the `min_mapped_reads` flagstat gate and the
zero-variant-sample filters (their reporting half is ported inside the
multiqc rule — see deviations).

### Documented deviations

Everything below has no oxo-flow equivalent and is the closest faithful
approximation; none silently change results:

1. **`config.assemblers` is a comma-separated list in canonical lowercase
   form (commas, no spaces).** The upstream `params.assemblers` accepts any
   comma-separated combination — e.g. `spades,unicycler` runs SPAdes AND
   Unicycler in the same run — trimming and lowercasing each entry. oxo-flow
   `when` conditions have no `in`/contains operator, so the port enumerates
   every combination of the three assemblers with explicit equality tests:
   each assembler family (`assemble_*` plus its Bandage/BLAST/QUAST/ABACAS/
   plasmidID QC chain) is gated on a disjunction of the four combinations
   that contain it. Spelling the list with spaces (`spades, unicycler`) is
   not accepted — upstream's trim is not reproducible without an `in`
   operator. (Negative equality gates were rejected as incorrect:
   `!= 'spades'` would wrongly enable `minia` for
   `assemblers = 'spades,unicycler'`.)
2. **Runtime-filter DROPS are partially ported (engine 0.17.0 `when`
   runtime functions).** The upstream fastp filter (drop samples with 0
   reads after trimming, wrapped in `if (!params.skip_fastp)`) IS ported:
   the consumers of the trimmed reads (`kraken2`, `align_bowtie2`,
   `assembly_fastq`) carry a
   `!config.skip_fastp && reads_count('fastp/{sample}_1.fastp.fastq.gz') > 0`
   gate, matching upstream's per-sample channel drop with the same
   short-circuit. The `min_mapped_reads` flagstat gate (a strict `>` on the
   mapped count parsed out of samtools flagstat text) and the
   zero-variant-sample filters still run in Nextflow channel code with no
   engine equivalent — a sample cannot be dropped mid-DAG from a flagstat
   regex or a `bcftools stats` record count. The reporting half IS ported:
   the multiqc rule regenerates upstream's custom-content TSVs
   (`fail_mapped_reads_mqc.tsv` from the fastp JSONs, `fail_mapped_samples_mqc.tsv`
   from the Bowtie2 flagstats, same headers/rows as `multiqcTsvFromList`),
   written only when samples fail. `min_mapped_reads` config feeds that
   flagstat comparison. Placeholder artifacts (`: > {sample}.scaffolds.fa`
   etc.) stand in where upstream would drop an empty assembly from the
   channel; zero-variant samples keep flowing downstream with a
   placeholder-header VCF (see `ivar_to_vcf`).
3. **MarkDuplicates does not replace `ch_bam`.** Upstream
   `BAM_MARKDUPLICATES_PICARD` swaps `ch_bam` so mosdepth, picard metrics and
   variant calling all consume the marked BAM. The port publishes the marked
   BAM (bam/bai/stats/flagstat/idxstats/metrics) as standalone rules
   (`markduplicates`, `markduplicates_wgs`) while the pipeline keeps the
   pre-dedup BAM — the upstream module itself forbids same-name in/out, and a
   canonical-path swap is impossible in oxo-flow (the rule would read and
   write the same path).
4. **Consensus paths are canonicalised across callers.** Upstream ivar
   consensus publishes under `consensus/ivar/` and bcftools under
   `consensus/bcftools/`. The port's ivar caller writes the canonical
   `variants/ivar/consensus/bcftools/{sample}.consensus.fa` path so
   QUAST/Pangolin/Nextclade/base-density/MultiQC rules are shared across
   both callers with no duplicate outputs.
5. **Kraken2 host-filter routing.** When Kraken2 runs with
   `kraken2_assembly_host_filter=false`, upstream routes the assembly branch
   to the fastp reads (channel wiring) while Kraken2 still writes its
   unclassified FASTQs. The port models this with the `assembly_fastq`
   passthrough rule, which overwrites the `kraken2/` unclassified paths with
   copies of the fastp reads; it carries `depends_on = ["kraken2"]` so the
   overwrite is ordered (deterministic) whenever both rules are active, and
   when `skip_kraken2=true` it is the sole producer of those paths.
6. **`nextclade_clade_mqc.tsv`** is built by inline python instead of Nextflow
   channel code (same input CSVs, same output columns).
7. **`min_contig_length` / `min_perc_contig_aligned`** are used directly in the
   BLAST filter awk expression (upstream interpolates the same params).
8. **Condensed environments.** Rules that merge several upstream processes
   consolidate their conda envs. Exact pins are kept; only conflicts are
   resolved: `sed` 4.8 (cat/fastq, gunzip, untar) vs 4.9 (prepare_primer_fasta,
   filter_blastn, rename_fasta_header) → 4.8 in `coreutils.yaml`, 4.9 in
   `blast.yaml`/`consensus.yaml`; make_bed_mask's samtools 1.14 → 1.22.1 in
   `consensus.yaml`; tabix's htslib 1.21 → 1.22.1 in `bcftools.yaml`;
   r-base 4.2 → 4.2.0 in `r.yaml`; mosdepth's build string
   `=0.3.11=h0ec343a_1` → `=0.3.11` for cross-platform resolution.
9. **QUAST/ABACAS/Bandage inputs** gated by upstream `file(...)` existence
   checks (e.g. empty scaffolds) run unconditionally in the port; on the
   fixture and real data the files always exist.
10. **`save_unaligned` / `save_reference` are effectively always on.** The
    Kraken2 unclassified reads feed the assembly branch via upstream channel
    wiring (not a publish gate), so they always land in `kraken2/`; the
    reference files feed every rule and always publish. Both flags are kept as
    config for documentation. (`save_ivar_trimmed_bam` does not exist at
    3.0.0 — only `save_reference`, `save_trimmed_fail`, `save_unaligned` and
    `save_mpileup` do; the latter two are now ported as in-rule switches.)
11. **The upstream `multiqc_data/versions.yml` and `*_plots` outputs are not
    emitted — at parity, not a deviation.** Verified at the pinned 3.0.0 tag:
    the MULTIQC call receives no versions channel and the config has no
    software_versions dict; MultiQC 1.31's search pattern for the software
    table is `.+_mqc_versions\.(yaml|yml)` (plain `versions.yml` is not
    picked up), and `export_plots` defaults false (flat threshold 2000), so
    upstream emits neither artifact on its default path — matching the port.

### Resources

Resource labels map 1:1 to upstream `withLabel` profiles: `process_single`
(1c/6 GB/4 h), `process_low` (2c/12 GB/4 h), `process_medium`
(6c/36 GB/8 h), `process_high` (12c/72 GB/16 h). Fastp/SPAdes memory and
`-Xmx` JVM sizes are derived from the same values as upstream.

## Links

- Repository: [oxo-flow-viralrecon](https://github.com/oxo-flow-community/oxo-flow-viralrecon)
- Upstream: [nf-core/viralrecon](https://github.com/nf-core/viralrecon) @ `3.0.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
