---
title: "Small and structural variant calling with Varlociraptor"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-varlociraptor</span></div>
<div class="ox-detail-cols">
<div class="ox-detail-main">
<h1>Small and structural variant calling with Varlociraptor</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span><span class=ox-tag-sep></span><span class="ox-tag">variant-calling</span><span class="ox-tag">structural-variants</span><span class="ox-tag">varlociraptor</span><span class="ox-tag">vg</span><span class="ox-tag">freebayes</span><span class="ox-tag">delly</span><span class="ox-tag">pangenome</span><span class="ox-tag">snakemake-workflows</span></div>
<p class="ox-desc">Scenario-driven somatic small and structural variant calling with Varlociraptor: paired-end reads are aligned against the 1000 Genomes human pangenome with vg giraffe, QC&#x27;d with FastQC/MultiQC, covered with mosdepth, and used for freebayes and delly candidate calling; Varlociraptor then estimates alignment properties and calls variants under a tumor scenario (events present + somatic_tumor_high + somatic_tumor_medium, FDR 0.05), FDR is controlled per variant type (SNV/INS/DEL/MNV/BND/INV/DUP/REP) with merge and phred decoding, and the calls are annotated with VEP (LoFtool/REVEL plugins) and dbSNFP/dbSNP, filtered, turned into a 34-column variant table with oncoprint label-sorting, and rendered as interactive datavzrd variant and gene-coverage reports. All reference data (GRCh38 FASTA and GTF, VEP cache/plugins, REVEL scores, known-variants VCFs, HPRC pangenome graph) is downloaded automatically into resources/.</p>
<div class="ox-hero-cta"><a class="ox-btn ox-btn--run" href="#run-it">▶ Run it</a><a class="ox-btn" href="https://github.com/oxo-flow-community/oxo-flow-varlociraptor" rel="noopener">GitHub ↗</a><code class="ox-hero-cmd">$ oxo-flow run main.oxoflow</code></div>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">149</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v"><span title="up to 64 CPUs / 32 GB per rule (freebayes candidates 48 threads; vg giraffe 64 threads)">up to 64 CPUs / 32 GB per rule (freebayes candidates 48 threa…</span></span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/snakemake-workflows/dna-seq-varlociraptor">snakemake-workflows/dna-seq-varlociraptor</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v6.10.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2291.1"><code>10.48546/workflowhub.workflow.2291.1</code></a></span></div>
<div class="ox-glance-tools"><span class="k">Tools</span><div class="chips"><span class="tchip">altair</span><span class="tchip">arriba</span><span class="tchip">bcftools</span><span class="tchip">bedtools</span><span class="tchip">biopython</span><span class="tchip">bwa</span><span class="tchip">curl</span><span class="tchip">datavzrd</span></div></div>
<p class="cmd">$ oxo-flow pull gh:oxo-flow-community/oxo-flow-varlociraptor</p>
</div>
</div>
</div>

<nav class="ox-tabs" aria-label="Page sections"><a href="#semantic-overview">Introduction</a><a href="#run-it">Usage</a><a href="#parameters">Parameters</a><a href="#workflow-graph">Workflow graph</a><a href="#scope">Scope</a><a href="#fidelity">Fidelity</a></nav>

<details class="ox-flow-view" open id="semantic-overview">
<summary>Semantic overview — plain-language walkthrough <span class="ox-badge ox-badge--sem">text</span></summary>
<div class="ox-sem-text">
<p><strong>VarLociRaptor small-and-structural variant calling</strong>: one tumor sample's reads are pangenome-mapped, candidates called with freebayes and delly, re-filtered by Varlociraptor scenario, FDR-controlled per event type, and delivered as annotated calls plus interactive reports.</p>
<p><strong>1. Reference and read preparation</strong> — <code>get_genome</code>/<code>get_annotation</code> fetch the genome and annotation, feeding genome indexes (<code>genome_faidx</code>, <code>genome_dict</code>), the pangenome (<code>get_pangenome</code> → <code>pangenome_autoindex</code> → <code>get_reference_paths</code>), VEP cache/plugins (<code>get_vep_cache</code>, <code>get_vep_plugins</code>) and REVEL scores (<code>download_revel</code> → <code>process_revel_scores</code> → <code>tabix_revel</code>). Reads enter alignment through merged trimmed FASTQs (<code>merge_trimmed_fastqs_r1</code>/<code>merge_trimmed_fastqs_r2</code>), with <code>fastp_pe</code>/<code>fastp_se</code>/<code>fastp_pipe</code> trimming optional.</p>
<p><strong>2. Alignment, BQSR and QC</strong> — <code>map_reads_vg</code> aligns to the pangenome, then <code>postprocess_vg_alignments</code> → <code>sort_alignments</code> → <code>mark_duplicates</code> → <code>bam_index_dedup</code> → <code>recalibrate_base_qualities</code> → <code>apply_bqsr</code> yields the calibrated BAM; <code>multiqc</code> gathers <code>fastqc_r1</code>/<code>fastqc_r2</code>, <code>samtools_stats</code>/<code>samtools_idxstats</code>. A gated consensus branch (<code>calc_consensus_reads</code> → <code>map_consensus_reads_pe</code>/<code>map_consensus_reads_se</code> → <code>apply_bqsr_consensus</code>) reconverges downstream.</p>
<p><strong>3. Regions and primers</strong> — <code>build_sample_regions</code> computes per-base coverage; <code>merge_expanded_group_regions</code> → <code>filter_group_regions_expanded</code> and <code>merge_covered_group_regions</code> → <code>filter_group_regions_covered</code> restrict candidate calling. The primer chain (<code>map_primers</code> → <code>filter_unmapped_primers</code> → <code>primer_to_bed</code> → <code>build_primer_regions</code> → <code>assign_primers</code> → <code>filter_primerless_reads</code> → <code>trim_primers</code>) filters reads by primer.</p>
<p><strong>4. Candidates and Varlociraptor</strong> — <code>freebayes</code>/<code>delly</code> call candidates (<code>delly</code> also uses <code>download_delly_excluded_regions</code>); <code>fix_delly_calls</code> cleans delly output; <code>scatter_candidates_freebayes</code>/<code>scatter_candidates_delly</code> split callsets for <code>annotate_candidate_variants_freebayes</code>/<code>annotate_candidate_variants_delly</code> (VEP) and <code>filter_candidates_by_annotation_freebayes</code>/<code>filter_candidates_by_annotation_delly</code>. After <code>varlociraptor_alignment_properties</code>, the <code>varlociraptor_preprocess_freebayes</code>/<code>varlociraptor_preprocess_delly</code> observations feed <code>varlociraptor_call_freebayes</code>/<code>varlociraptor_call_delly</code> under the <code>render_scenario</code> scenario, converging at <code>bcftools_concat</code>.</p>
<p><strong>5. Annotation, FDR control and reporting</strong> — <code>bcftools_concat</code> output is VEP-annotated (<code>annotate_variants</code> → <code>bcf_index_vep_annotated</code> → <code>annotate_vcfs</code>, optional <code>annotate_dgidb</code>); after <code>filter_by_annotation</code> and <code>gather_calls</code>, per-type FDR control (<code>control_fdr_SNV</code>, <code>control_fdr_INS</code>, <code>control_fdr_DEL</code>, <code>control_fdr_MNV</code>, <code>control_fdr_BND</code>, <code>control_fdr_INV</code>, <code>control_fdr_DUP</code>, <code>control_fdr_REP</code>) leads to <code>merge_calls</code> → <code>convert_phred_scores</code> → <code>vembrane_table</code> → <code>process_call_tables</code>, alongside <code>prepare_oncoprint</code> → <code>datavzrd_variants_calls</code> and <code>bedtools_merge</code> → <code>coverage_table</code> → <code>datavzrd_coverage</code>.</p>
<p><strong>6. Gated branches</strong> — population-DB filtering (<code>gather_annotated_calls</code>, <code>population_filter_variants</code>), MAF export (<code>group_bcf_to_vcf_variants</code>, <code>group_vcf_to_maf_variants</code>), COSMIC signatures (<code>create_mutational_context_file</code>, <code>annotate_mutational_signatures</code>, <code>plot_mutational_signatures</code>), fusion calling (<code>star_index</code>, <code>star_align</code>, <code>arriba</code>, <code>sort_arriba_calls</code>) and CHM benchmarking (<code>chm_eval</code>).</p>
<p><em>Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.</em></p>
<p class="ox-sem-line"><a class="ox-issue-mini" href="https://github.com/oxo-flow-community/oxo-flow-community.github.io/issues/new?title=%5Boverview%5D+oxo-flow-varlociraptor+semantic+text+correction&body=Which step or rule name looks wrong (paste the step/rule names)">Report a correction to this overview</a></p>
</div>
</details>

## Run it

```bash
oxo-flow run gh:oxo-flow-community/oxo-flow-varlociraptor
```

Runs straight from the catalog — `oxo-flow` checks the repo out under `.oxo-flow/repos/oxo-flow-varlociraptor` and keeps outputs/checkpoints in the current directory, no manual clone. Pin a revision with `gh:oxo-flow-community/oxo-flow-varlociraptor@<branch-or-tag>`.

Preview the plan first: `oxo-flow pull gh:oxo-flow-community/oxo-flow-varlociraptor` fetches the repo, then `oxo-flow dry-run main.oxoflow`.


Needs reference data — see Requirements; preview with `oxo-flow dry-run main.oxoflow --samples first:1`.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned versions (no containers)

**Requirements.**

- paired-end FASTQ reads at reads_dir/<sample>_1.fastq.gz / _2.fastq.gz; sample cohort declared in [[sample_groups]] (one group = one tumor sample); fixtures bundled for dry-run
- reference data: downloaded automatically into resources/ — GRCh38 primary assembly FASTA (Ensembl release 111) + .fai/.dict, Ensembl release 111 GTF, VEP cache and plugins (release 111), REVEL scores, Ensembl known-variants VCFs, HPRC v1.1 human pangenome graph
- compute: up to 64 CPUs / 32 GB per rule (freebayes candidates 48 threads — upstream 96, scaled; vg giraffe 64 threads; samtools sort 16 threads/32G; Varlociraptor call 8G; consensus/bam-name sorting 16 threads/64G when the gated branches are on)
- tools: conda envs with pinned versions (envs/*.yaml, one env per tool pin set); conda/mamba required at runtime
- disk: multi-GB reference downloads under resources/ (pangenome graph, VEP cache, known-variants VCFs) plus results/ for BAMs, BCFs, tables and reports

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-varlociraptor
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-varlociraptor
```

## Parameters

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. Copy a row to paste the key directly. Click any parameter name to copy <code>key = value</code>; clicking <code>default</code> copies just the value.</p>
<table class="ox-params">
<thead><tr><th>Parameter</th><th>Type</th><th>Default</th><th>Description</th></tr></thead>
<tbody>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy annotation_selection = value" data-copy="annotation_selection = db_annotated">annotation_selection</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>db_annotated</code></td>
<td class="ox-p-desc">The annotated-callset selection for gather_annotated_calls (upstream<br>get_final_selected_annotation): &quot;db_annotated&quot; (annotations/vcfs active,<br>the default), &quot;dgidb_annotated&quot; when dgidb is activated, or &quot;vep_annotated&quot;<br>when annotations/vcfs is deactivated.<br><span class="ox-param-usedby">used by <code>3</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy benchmarking_activate = value" data-copy="benchmarking_activate = false">benchmarking_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: benchmarking (Snakefile rule benchmark / benchmarking.smk;<br>the full CHM-eval flow is ported, except the chm sample group vertical<br>slice (see module header)).<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy bwa_align_activate = value" data-copy="bwa_align_activate = false">bwa_align_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: linear-reference (bwa) aligner branch of mapping.smk<br>(map_reads_bwa + ref.smk bwa_index). The default path aligns with vg<br>giraffe to the pangenome (ref/pangenome/activate = true upstream).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cadd_build = value" data-copy="cadd_build = GRCh38">cadd_build</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>GRCh38</code></td>
<td class="ox-p-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cadd_variant_type = value" data-copy="cadd_variant_type = snv">cadd_variant_type</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>snv</code></td>
<td class="ox-p-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy cadd_version = value" data-copy="cadd_version = v1.7">cadd_version</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>v1.7</code></td>
<td class="ox-p-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy consensus_activate = value" data-copy="consensus_activate = false">consensus_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: calc_consensus_reads/activate (consensus.oxoflow: rbt<br>collapse-reads-to-fragments + re-mapping to the linear bwa reference).<br>Activating it also needs the bwa reference index (bwa_align_activate or<br>primers_activate builds it) and, upstream-faithful,<br>markduplicates_extra = &quot;--TAG_DUPLICATE_SET_MEMBERS true&quot; and<br>freebayes_min_alternate_count = 1 (see those keys below).<br><span class="ox-param-usedby">used by <code>10</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy dgidb_activate = value" data-copy="dgidb_activate = false">dgidb_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: annotations/dgidb (annotate_dgidb; datasources = [DrugBank]).<br>Activating dgidb changes which annotated callset the final-calls chain<br>consumes upstream (get_final_selected_annotation): set annotation_selection<br>below to &quot;dgidb_annotated&quot; together with this key.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy freebayes_min_alternate_count = value" data-copy="freebayes_min_alternate_count = 2">freebayes_min_alternate_count</button></td>
<td class="ox-p-t"><code>int</code></td>
<td class="ox-p-d"><code>2</code></td>
<td class="ox-p-desc">upstream config: params/freebayes — the min-alternate-count for candidate<br>calling (2, or 1 when calc_consensus_reads is active).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy fusion_activate = value" data-copy="fusion_activate = false">fusion_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: fusion calling branch (fusion_calling.smk star_arriba<br>meta wrapper: star_index / star_align / arriba / annotate_exons /<br>convert_fusions / sort_arriba_calls / bcftools_concat_candidates).<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy maf_activate = value" data-copy="maf_activate = false">maf_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: maf/activate (group_bcf_to_vcf + group_vcf_to_maf).<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy markduplicates_extra = value" data-copy="markduplicates_extra = ">markduplicates_extra</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream config: params/picard/MarkDuplicates + get_markduplicates_extra —<br>extra MarkDuplicates arguments (upstream adds<br>&quot;--TAG_DUPLICATE_SET_MEMBERS true&quot; when calc_consensus_reads is active;<br>empty by default).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mutational_burden_activate = value" data-copy="mutational_burden_activate = false">mutational_burden_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: mutational_burden/activate + events<br>(calculate_covered_coding_sites + estimate_mutational_burden; events are<br>comma-joined, split to space-separated in the rule shells).<br><span class="ox-param-usedby">used by <code>6</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mutational_burden_events = value" data-copy="mutational_burden_events = somatic_tumor_low,somatic_tumor_medium,somatic_tumor_high">mutational_burden_events</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>somatic_tumor_low,somatic_tumor_medium,somatic_tumor_high</code></td>
<td class="ox-p-desc">upstream config: mutational_burden/activate + events<br>(calculate_covered_coding_sites + estimate_mutational_burden; events are<br>comma-joined, split to space-separated in the rule shells).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy mutational_signatures_activate = value" data-copy="mutational_signatures_activate = false">mutational_signatures_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: mutational_signatures/activate<br>(create_mutational_context_file ... plot_mutational_signatures; upstream<br>default events = [some_id], samples = [tumor], frozen in the module).<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy plugins_activate = value" data-copy="plugins_activate = false">plugins_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy population_db_activate = value" data-copy="population_db_activate = false">population_db_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy population_db_alias = value" data-copy="population_db_alias = tumor">population_db_alias</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>tumor</code></td>
<td class="ox-p-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy population_db_events = value" data-copy="population_db_events = somatic_tumor_high,somatic_tumor_medium">population_db_events</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>somatic_tumor_high,somatic_tumor_medium</code></td>
<td class="ox-p-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy population_db_fdr = value" data-copy="population_db_fdr = 0.05">population_db_fdr</button></td>
<td class="ox-p-t"><code>float</code></td>
<td class="ox-p-d"><code>0.05</code></td>
<td class="ox-p-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy population_db_path = value" data-copy="population_db_path = resources/population_db.variants.bcf">population_db_path</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>resources/population_db.variants.bcf</code></td>
<td class="ox-p-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).<br><span class="ox-param-usedby">used by <code>2</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy primers_activate = value" data-copy="primers_activate = false">primers_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: primers/trimming (rules assign_primers ... build_primer_regions).<br>primers_fa1/primers_fa2 are the upstream primers/trimming/primers_fa{1,2} fasta<br>files (empty upstream default = primers flow off); fa2 empty means single-end<br>primer fasta.<br><span class="ox-param-usedby">used by <code>8</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy primers_fa1 = value" data-copy="primers_fa1 = ">primers_fa1</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream config: primers/trimming (rules assign_primers ... build_primer_regions).<br>primers_fa1/primers_fa2 are the upstream primers/trimming/primers_fa{1,2} fasta<br>files (empty upstream default = primers flow off); fa2 empty means single-end<br>primer fasta.<br><span class="ox-param-usedby">used by <code>1</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy primers_fa2 = value" data-copy="primers_fa2 = ">primers_fa2</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code></code></td>
<td class="ox-p-desc">upstream config: primers/trimming (rules assign_primers ... build_primer_regions).<br>primers_fa1/primers_fa2 are the upstream primers/trimming/primers_fa{1,2} fasta<br>files (empty upstream default = primers flow off); fa2 empty means single-end<br>primer fasta.<br><span class="ox-param-unused">not referenced by any rule (ported for upstream compatibility — overriding has no effect here)</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy reads_dir = value" data-copy="reads_dir = test/fixtures/raw">reads_dir</button></td>
<td class="ox-p-t"><code>string</code></td>
<td class="ox-p-d"><code>test/fixtures/raw</code></td>
<td class="ox-p-desc">Path to the raw paired-end FASTQs of the single sample (upstream<br>config/units.tsv points at absolute /projects/... paths; the port reads<br>from the repository fixtures instead).<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy skip_ref_downloads = value" data-copy="skip_ref_downloads = false">skip_ref_downloads</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">Skip the ref:: download rules (genome, annotation, VEP cache/plugins,<br>pangenome, REVEL, known variants — ~5 GB of public databases). Set to<br>true when you have pre-placed the files at the resource paths the rules<br>declare (see README &quot;Reference databases&quot;); the downloads are hardcoded<br>upstream URLs and need unimpeded network access.<br><span class="ox-param-usedby">used by <code>7</code> rules</span></td>
</tr>
<tr>
<td class="ox-p-k"><button class="ox-p-copy" type="button" title="Copy trimming_activate = value" data-copy="trimming_activate = false">trimming_activate</button></td>
<td class="ox-p-t"><code>bool</code></td>
<td class="ox-p-d"><code>false</code></td>
<td class="ox-p-desc">upstream config: trimming (get_sra / fastp rules). The default path has no<br>trimming configured — reads pass through mapping::merge_trimmed_fastqs.<br><span class="ox-param-usedby">used by <code>4</code> rules</span></td>
</tr>
</tbody>
</table>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<details class="ox-flow-view" open>
<summary>Overview — all modules</summary>
<div class="ox-dag-card ox-dag-card--wide" markdown="1">

<a href="/assets/dag/oxo-flow-varlociraptor.svg?v=4de87fc1a0" target="_blank" rel="noopener" title="Open at native resolution"><img src="/assets/dag/oxo-flow-varlociraptor.svg?v=4de87fc1a0" alt="oxo-flow-varlociraptor pipeline overview" loading="lazy"></a>

<p class="ox-dag-caption">figure · oxo-flow-varlociraptor — Scenario-driven somatic small and structural variant calling with Varlociraptor: paired-end reads are aligned against the 1000 Genomes human pangenome with vg giraffe, QC&#x27;d with FastQC/MultiQC, covered with mosdepth, and used for freebayes and delly candidate calling; Varlociraptor then estimates alignment properties and calls variants under a tumor scenario (events present + somatic_tumor_high + somatic_tumor_medium, FDR 0.05), FDR is controlled per variant type (SNV/INS/DEL/MNV/BND/INV/DUP/REP) with merge and phred decoding, and the calls are annotated with VEP (LoFtool/REVEL plugins) and dbSNFP/dbSNP, filtered, turned into a 34-column variant table with oncoprint label-sorting, and rendered as interactive datavzrd variant and gene-coverage reports.</p>

</div>
</details>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- annotate_candidate_variants_delly
- annotate_candidate_variants_freebayes
- annotate_variants
- annotate_vcfs
- apply_bqsr
- bam_index_dedup
- bcf_index_arriba
- bcf_index_candidate_delly
- bcf_index_candidate_freebayes
- bcf_index_delly
- bcf_index_fdr_BND
- bcf_index_fdr_DEL
- bcf_index_fdr_DUP
- bcf_index_fdr_INS
- bcf_index_fdr_INV
- bcf_index_fdr_MNV
- bcf_index_fdr_REP
- bcf_index_fdr_SNV
- bcf_index_filtered
- bcf_index_freebayes
- bcf_index_fusions_callset
- bcf_index_vep_annotated
- bcftools_concat
- bcftools_concat_fusions
- bcf_index_fdr_BND_fusions
- bedtools_merge
- build_sample_regions
- control_fdr_BND
- control_fdr_BND_fusions
- control_fdr_DEL
- control_fdr_DUP
- control_fdr_INS
- control_fdr_INV
- control_fdr_MNV
- control_fdr_REP
- control_fdr_SNV
- convert_phred_scores
- convert_phred_scores_fusions
- coverage_table
- datavzrd_coverage
- datavzrd_variants_calls
- delly
- download_delly_excluded_regions
- download_revel
- fastqc_r1
- fastqc_r2
- filter_by_annotation
- filter_candidates_by_annotation_delly
- filter_candidates_by_annotation_freebayes
- filter_group_regions_covered
- filter_group_regions_expanded
- filter_offtarget_variants_delly
- filter_offtarget_variants_freebayes
- fix_delly_calls
- freebayes
- gather_calls
- gather_annotated_calls_fusions
- genome_dict
- genome_faidx
- get_annotation
- get_genome
- get_known_variants
- get_pangenome
- get_reference_paths
- get_target_regions
- get_vep_cache
- get_vep_plugins
- map_reads_vg
- mark_duplicates
- merge_calls
- merge_calls_fusions
- merge_covered_group_regions
- merge_expanded_group_regions
- merge_trimmed_fastqs_r1
- merge_trimmed_fastqs_r2
- multiqc
- pangenome_autoindex
- postprocess_vg_alignments
- prepare_oncoprint
- process_call_tables
- process_revel_scores
- recalibrate_base_qualities
- remove_iupac_codes
- render_scenario
- samtools_idxstats
- samtools_stats
- scatter_candidates_delly
- scatter_candidates_freebayes
- sort_alignments
- sort_calls_arriba
- sort_calls_delly
- sort_calls_freebayes
- tabix_noiupac
- tabix_revel
- tabix_variation
- transform_gene_annotations
- varlociraptor_alignment_properties
- varlociraptor_call_arriba
- varlociraptor_call_delly
- varlociraptor_call_freebayes
- varlociraptor_preprocess_arriba
- varlociraptor_preprocess_delly
- varlociraptor_preprocess_freebayes
- vembrane_table
- annotate_dgidb
- gather_benchmark_calls
- chm_eval_sample
- chm_namesort
- chm_to_fastq
- chm_eval_kit
- chromosome_map
- rename_chromosomes
- chm_eval
- determine_coding_regions
- bcf_index_final
- calculate_covered_coding_sites
- estimate_mutational_burden_curve
- estimate_mutational_burden_hist
- create_mutational_context_file
- download_cosmic_signatures
- annotate_mutational_signatures
- join_mutational_signatures
- annotate_descriptions
- plot_mutational_signatures
- calc_consensus_reads
- map_consensus_reads_pe
- map_consensus_reads_se
- merge_consensus_reads
- sort_consensus_reads
- bam_index_consensus
- recalibrate_base_qualities_consensus
- apply_bqsr_consensus
- star_index
- star_align
- arriba
- annotate_exons
- convert_fusions
- sort_arriba_calls
- bcftools_concat_candidates
- group_bcf_to_vcf_variants
- group_bcf_to_vcf_fusions
- group_vcf_to_maf_variants
- group_vcf_to_maf_fusions
- bwa_index
- map_reads_bwa
- download_cadd_scores_for_vep
- clean_population_db
- gather_annotated_calls
- annotated_index
- bcf_index_cleaned_db
- population_filter_variants
- bcf_index_population_filtered
- population_db_update
- assign_primers
- filter_primerless_reads
- trim_primers
- map_primers
- filter_unmapped_primers
- primer_to_bed
- build_primer_regions
- get_sra
- fastp_pipe
- fastp_se
- fastp_pe
- bcf_index_arriba_candidates

**Excluded**

- fusions report and table exports (upstream datavzrd.smk: `datavzrd_fusion_calls` + `process_fusion_call_tables`; and the fusions instance of the single wildcard `vembrane_table` rule) — the ported fusions FDR-control chain (filtering.oxoflow) ends at the fdr-controlled/normal-probs callsets; the port's `vembrane_table` hardcodes the variants path, so the fusions table/report datasets are missing. `fusion_activate` is the port's config key (upstream gates on the `types: ["variants","fusions"]` list). Note: upstream has no fusions oncoprint output — `get_oncoprint_input` is variants-only, so nothing to port there
- annotate_umis (upstream mapping.smk:77, UMI branch via umi_tools group; activates for samples with a non-empty `umi_read` column) and splitncigarreads (upstream mapping.smk:173, RNA-datatype branch in get_recalibrate_quality_input) — not ported; the port models DNA data with the default empty samples columns
- upstream testcase.smk debug module (`gather_observations` + `testcase`: varlociraptor call --testcase-prefix/--testcase-locus mode, results/testcases/) — not ported. (The upstream `bcf_to_vcf_gz`, `vg2svg` and `only_alignment` tools have no consumers/producers in the upstream tree at the pinned tag — dead tools, intentionally not ported)

## Fidelity

The port aims for byte-identical commands on the default path. Known,
deliberate deviations:

| upstream | port | reason |
|---|---|---|
| `scatter.calling(16)` (rules run 16x, once per scatter item) | single chunk, `scatteritem=0` | the port freezes `scatteritem=0`; `rbt vcf-split` with one output chunk writes the whole callset, so the chunk content is identical to upstream's 16 chunks gathered with `bcftools concat -a` before `control_fdr` (oxo-flow does have a scatter construct; it is not exercised because the port's single sample makes the split work-identical) |
| rule outputs that are directories (VEP cache/plugins, oncoprint `label_sortings/`/`variant-oncoprints/` dirs) | directory + `.completed` marker file output | oxo-flow targets files, not directories |
| scenario rendered at run time from `config/scenario.yaml` (yte template) | pre-rendered `resources/scenarios/SRR702070_group.yaml` for the default sample group; the template is kept verbatim at `config/scenario.yaml` | one scenario (purity 1.0) in the default path |
| `download_vep_plugins.py` with a hard-coded Ensembl variation FTP list and fallback | the `--release`/`--output`/`--log` argv variant of the same wrapper port | one release (111), one output dir; the FTP fallback list was dropped as dead code in the default path |
| wrapper-utils based rules (calls, tables, report) | plain `python scripts/*.py` argv ports of the same wrappers | wrapper-utils is a Snakemake runtime; the ported scripts keep the wrapper logic verbatim |
| `filter_odds` | not ported | not reachable in the default path (`filter: present` only); the population/burden branches consume `gather_annotated_calls` instead (ported in `population.oxoflow`) |
| template oncoprint views (`gene_oncoprint` / `variant_oncoprints` datasets) | empty (upstream defaults with a single group) | `prepare_oncoprint` itself runs and feeds the label-sorting table, exactly like upstream |
| vembrane filter/table expressions evaluated from Python at run time | precomputed literal expression/header (34 columns) | same semantics, evaluated once |
| upstream `config/units.tsv` absolute `/projects/...` read paths | `config.reads_dir` + sample group fixture paths | portability |
| Snakemake `temp()` outputs | `temporary = true` | engine equivalent |
| per-rule conda environments | one env per tool pin set (`envs/`) | same packages, same pins, consolidated |
| snakemake `before_update`/`update` flags (population db) | no input edge; the db path is read/written as-is | oxo-flow has no such flags; a declared input would create a DAG cycle (`validate` rejects it) |
| snakemake `temp()` outputs of the gated branch modules | plain outputs (`temporary = true` where the default path used it) | see the module headers; `join_mutational_signatures` writes with `>` instead of the upstream `>>` because the engine does not pre-delete outputs |
| snakemake script API (`snakemake.input/output/params`) in the 6 branch scripts | argv ports (`--output`/`--log` flags, comma-joined lists) | same logic verbatim, cf. the default-path script ports |
| chm sample group vertical slice (benchmarking) | not ported | the ported CHM-eval flow (`chm_eval_sample` ... `chm_eval`) re-derives the CHM1 FASTQs, but the chm sample is not in the port's `config/samples.tsv`, so the chm reads do not flow through mapping -> calling -> `control_fdr`; `rename_chromosomes`/`chm_eval` keep orphan inputs (validate warns, like upstream without the chm sample) |
| consensus-read calling (`calc_consensus_reads` flow) | `consensus.oxoflow`, gated on `consensus_activate` | upstream switches the `recalibrate_base_qualities`/`apply_bqsr` input via `get_recalibrate_quality_input`; the port models this as gated duplicate rules with the same outputs and exclusive `when` gates (`!consensus_activate` vs `consensus_activate`) |
| `annotate_dgidb` | `annotation::annotate_dgidb`, gated on `dgidb_activate` + `annotation_selection` | upstream `get_final_selected_annotation` switches the annotated callset consumed by filtering and the final-calls chain; the port exposes the same selection as `config.annotation_selection` |
| `filter_offtarget_variants` (wrapper v2.3.2/bio/bcftools/filter, `params.extra=""`) | pass-through `bcftools filter -o/-O b` on the fixed calls; the `regions`/index inputs are declared (as upstream) so `get_target_regions` and the candidate indexes exist pre-scatter | the pinned wrapper consumes only `input[0]` (verified against its source); the actual target-region restriction is the `filter_group_regions` bedtools intersect below |
| `target_regions` list config | single BED path (`config.target_regions`) | upstream merges one or more files; the port freezes one path |
| `filter_group_regions` `get_filter_targets` (bedtools intersect) | same command inline in the two `filter_group_regions_*` rules | byte-identical output; intersect branch only when `target_regions` is set |
| per-group `calling` column of `config/samples.tsv` | `[sample_groups.metadata] calling` on each group | fusions continuation rules gate on `wildcard.calling == "fusions" || "variants,fusions"` |
| `get_candidate_calls` for caller=arriba (UNFILTERED group concat) + `get_varlociraptor_params` (propagate-info-fields extra) | `calling::varlociraptor_preprocess_arriba`/`varlociraptor_call_arriba` consuming `results/candidate-calls/arriba/{group}/{group}.bcf` | command text identical; the arriba path has no scatter fan-out (no scatteritem) |
| `scatter_candidates`/`filter_group_regions` conditional inputs (Python `if config.get("target_regions", None)`) | `optional = "any"` input pairs + `if [ -n "{config.target_regions}" ]` shell switch | engine equivalent of the upstream input selection |
| upstream `get_target_regions` chr-strip (`awk '{sub("^chr","",$0); print}'`) | verbatim | target BEDs must be chr-less (Ensembl GRCh38 primary assembly); chr-prefixed files fail closed, exactly as upstream |

## Links

- Repository: [oxo-flow-varlociraptor](https://github.com/oxo-flow-community/oxo-flow-varlociraptor)
- Upstream: [snakemake-workflows/dna-seq-varlociraptor](https://github.com/snakemake-workflows/dna-seq-varlociraptor) @ `v6.10.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
