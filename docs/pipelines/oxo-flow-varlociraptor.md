---
title: "Small and structural variant calling with Varlociraptor"
---

<div class="ox-crumb"><a href="/pipelines/">Pipelines</a> / <span>oxo-flow-varlociraptor</span></div>
<div class="ox-detail-cols">
<div>
<h1>Small and structural variant calling with Varlociraptor</h1>
<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>
<p>Scenario-driven somatic small and structural variant calling with Varlociraptor: paired-end reads are aligned against the 1000 Genomes human pangenome with vg giraffe, QC&#x27;d with FastQC/MultiQC, covered with mosdepth, and used for freebayes and delly candidate calling; Varlociraptor then estimates alignment properties and calls variants under a tumor scenario (events present + somatic_tumor_high + somatic_tumor_medium, FDR 0.05), FDR is controlled per variant type (SNV/INS/DEL/MNV/BND/INV/DUP/REP) with merge and phred decoding, and the calls are annotated with VEP (LoFtool/REVEL plugins) and dbSNFP/dbSNP, filtered, turned into a 34-column variant table with oncoprint label-sorting, and rendered as interactive datavzrd variant and gene-coverage reports. All reference data (GRCh38 FASTA and GTF, VEP cache/plugins, REVEL scores, known-variants VCFs, HPRC pangenome graph) is downloaded automatically into resources/.</p>
</div>
<div>
<div class="ox-glance">
<div class="ox-glance-title">At a glance</div>
<div class="ox-kv"><span class="k">Rating</span><span class="v live">✔ Live-tested</span></div>
<div class="ox-kv"><span class="k">Rules</span><span class="v">165</span></div>
<div class="ox-kv"><span class="k">Compute</span><span class="v">up to 64 CPUs / 32 GB per rule (freebayes candidates 48 threads; vg giraffe 64 threads)</span></div>
<div class="ox-kv"><span class="k">Engine</span><span class="v"><span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></span></div>
<div class="ox-kv"><span class="k">Origin</span><span class="v">⇄ Official port</span></div>
<div class="ox-kv"><span class="k">Domain</span><span class="v">genomics</span></div>
<div class="ox-kv"><span class="k">Source</span><span class="v"><a href="https://github.com/snakemake-workflows/dna-seq-varlociraptor">snakemake-workflows/dna-seq-varlociraptor</a></span></div>
<div class="ox-kv"><span class="k">Pinned version</span><span class="v"><code>v6.10.0</code></span></div>
<div class="ox-kv"><span class="k">Ported</span><span class="v">2026-08-15</span></div>
<div class="ox-kv"><span class="k">License</span><span class="v">Apache-2.0</span></div>
<div class="ox-kv"><span class="k">Cite</span><span class="v"><a href="https://doi.org/10.48546/workflowhub.workflow.2291.1"><code>10.48546/workflowhub.workflow.2291.1</code></a></span></div>
<p class="cmd">$ oxo-flow run main.oxoflow</p>
</div>
</div>
</div>

## Run it

```bash
oxo-flow run main.oxoflow
```

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

<p class="ox-param-usage">Parameters are consumed by rules through <code>{config.key}</code> placeholders in inputs, outputs, and shells. Set a value in the workflow's <code>[config]</code> section (edit the file), or override at run time with <code>oxo-flow run -e key=value workflow.oxoflow</code> — repeat <code>-e</code> for multiple keys. The list below names the rules that read each key.</p>
<div class="ox-params">
<div class="ox-param">
<div class="ox-param-head"><code>annotation_selection</code><span class="ox-param-default">db_annotated</span></div>
<p class="ox-param-desc">The annotated-callset selection for gather_annotated_calls (upstream<br>get_final_selected_annotation): &quot;db_annotated&quot; (annotations/vcfs active,<br>the default), &quot;dgidb_annotated&quot; when dgidb is activated, or &quot;vep_annotated&quot;<br>when annotations/vcfs is deactivated.</p>
<details class="ox-param-usedby"><summary>used by 3 rules</summary>
<div class="ox-param-rules"><code>filtering::filter_by_annotation</code> <code>population::annotated_index</code> <code>population::gather_annotated_calls</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>benchmarking_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: benchmarking (Snakefile rule benchmark / benchmarking.smk;<br>the full CHM-eval flow is ported, except the chm sample group vertical<br>slice (see module header)).</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>benchmarking::chm_eval</code> <code>benchmarking::chm_eval_kit</code> <code>benchmarking::chm_eval_sample</code> <code>benchmarking::chm_namesort</code> <code>benchmarking::chm_to_fastq</code> <code>benchmarking::chromosome_map</code> <code>benchmarking::gather_benchmark_calls</code> <code>benchmarking::rename_chromosomes</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>bwa_align_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: linear-reference (bwa) aligner branch of mapping.smk<br>(map_reads_bwa + ref.smk bwa_index). The default path aligns with vg<br>giraffe to the pangenome (ref/pangenome/activate = true upstream).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>mapping_bwa::bwa_index</code> <code>mapping_bwa::map_reads_bwa</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cadd_build</code><span class="ox-param-default">GRCh38</span></div>
<p class="ox-param-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plugins::download_cadd_scores_for_vep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cadd_variant_type</code><span class="ox-param-default">snv</span></div>
<p class="ox-param-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plugins::download_cadd_scores_for_vep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>cadd_version</code><span class="ox-param-default">v1.7</span></div>
<p class="ox-param-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plugins::download_cadd_scores_for_vep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>consensus_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: calc_consensus_reads/activate (consensus.oxoflow: rbt<br>collapse-reads-to-fragments + re-mapping to the linear bwa reference).<br>Activating it also needs the bwa reference index (bwa_align_activate or<br>primers_activate builds it) and, upstream-faithful,<br>markduplicates_extra = &quot;--TAG_DUPLICATE_SET_MEMBERS true&quot; and<br>freebayes_min_alternate_count = 1 (see those keys below).</p>
<details class="ox-param-usedby"><summary>used by 10 rules</summary>
<div class="ox-param-rules"><code>consensus::apply_bqsr_consensus</code> <code>consensus::bam_index_consensus</code> <code>consensus::calc_consensus_reads</code> <code>consensus::map_consensus_reads_pe</code> <code>consensus::map_consensus_reads_se</code> <code>consensus::merge_consensus_reads</code> <code>consensus::recalibrate_base_qualities_consensus</code> <code>consensus::sort_consensus_reads</code> <code>mapping::apply_bqsr</code> <code>mapping::recalibrate_base_qualities</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>dgidb_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: annotations/dgidb (annotate_dgidb; datasources = [DrugBank]).<br>Activating dgidb changes which annotated callset the final-calls chain<br>consumes upstream (get_final_selected_annotation): set annotation_selection<br>below to &quot;dgidb_annotated&quot; together with this key.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>annotation::annotate_dgidb</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>freebayes_min_alternate_count</code><span class="ox-param-default">2</span></div>
<p class="ox-param-desc">upstream config: params/freebayes — the min-alternate-count for candidate<br>calling (2, or 1 when calc_consensus_reads is active).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>candidate_calling::freebayes</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>fusion_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: fusion calling branch (fusion_calling.smk star_arriba<br>meta wrapper: star_index / star_align / arriba / annotate_exons /<br>convert_fusions / sort_arriba_calls / bcftools_concat_candidates).</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>fusion::annotate_exons</code> <code>fusion::arriba</code> <code>fusion::bcf_index_arriba</code> <code>fusion::bcftools_concat_candidates</code> <code>fusion::convert_fusions</code> <code>fusion::sort_arriba_calls</code> <code>fusion::star_align</code> <code>fusion::star_index</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>maf_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: maf/activate (group_bcf_to_vcf + group_vcf_to_maf).</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>maf::group_bcf_to_vcf_fusions</code> <code>maf::group_bcf_to_vcf_variants</code> <code>maf::group_vcf_to_maf_fusions</code> <code>maf::group_vcf_to_maf_variants</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>markduplicates_extra</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">upstream config: params/picard/MarkDuplicates + get_markduplicates_extra —<br>extra MarkDuplicates arguments (upstream adds<br>&quot;--TAG_DUPLICATE_SET_MEMBERS true&quot; when calc_consensus_reads is active;<br>empty by default).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>mapping::mark_duplicates</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>mutational_burden_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: mutational_burden/activate + events<br>(calculate_covered_coding_sites + estimate_mutational_burden; events are<br>comma-joined, split to space-separated in the rule shells).</p>
<details class="ox-param-usedby"><summary>used by 6 rules</summary>
<div class="ox-param-rules"><code>burden_signatures::calculate_covered_coding_sites</code> <code>burden_signatures::determine_coding_regions</code> <code>burden_signatures::estimate_mutational_burden_curve</code> <code>burden_signatures::estimate_mutational_burden_hist</code> <code>population::annotated_index</code> <code>population::gather_annotated_calls</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>mutational_burden_events</code><span class="ox-param-default">somatic_tumor_low,somatic_tumor_medium,somatic_tumor_high</span></div>
<p class="ox-param-desc">upstream config: mutational_burden/activate + events<br>(calculate_covered_coding_sites + estimate_mutational_burden; events are<br>comma-joined, split to space-separated in the rule shells).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>burden_signatures::estimate_mutational_burden_curve</code> <code>burden_signatures::estimate_mutational_burden_hist</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>mutational_signatures_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: mutational_signatures/activate<br>(create_mutational_context_file ... plot_mutational_signatures; upstream<br>default events = [some_id], samples = [tumor], frozen in the module).</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>burden_signatures::annotate_descriptions</code> <code>burden_signatures::annotate_mutational_signatures</code> <code>burden_signatures::bcf_index_final</code> <code>burden_signatures::create_mutational_context_file</code> <code>burden_signatures::determine_coding_regions</code> <code>burden_signatures::download_cosmic_signatures</code> <code>burden_signatures::join_mutational_signatures</code> <code>burden_signatures::plot_mutational_signatures</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>plugins_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: plugins (download_cadd_scores_for_vep; download_revel and<br>process_revel_scores are already ported in ref.oxoflow). cadd_build /<br>cadd_version / cadd_variant_type are the upstream wildcards of the same<br>rule with their upstream defaults.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>plugins::download_cadd_scores_for_vep</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>population_db_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>population::annotated_index</code> <code>population::bcf_index_cleaned_db</code> <code>population::bcf_index_population_filtered</code> <code>population::clean_population_db</code> <code>population::gather_annotated_calls</code> <code>population::population_db_update</code> <code>population::population_filter_variants</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>population_db_alias</code><span class="ox-param-default">tumor</span></div>
<p class="ox-param-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>population::population_filter_variants</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>population_db_events</code><span class="ox-param-default">somatic_tumor_high,somatic_tumor_medium</span></div>
<p class="ox-param-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>population::population_filter_variants</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>population_db_fdr</code><span class="ox-param-default">0.05</span></div>
<p class="ox-param-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>population::population_filter_variants</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>population_db_path</code><span class="ox-param-default">resources/population_db.variants.bcf</span></div>
<p class="ox-param-desc">upstream config: population/db/activate + path/alias/fdr/events<br>(rules clean_population_db / population_filter_variants / population_db_update).</p>
<details class="ox-param-usedby"><summary>used by 2 rules</summary>
<div class="ox-param-rules"><code>population::clean_population_db</code> <code>population::population_db_update</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>primers_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: primers/trimming (rules assign_primers ... build_primer_regions).<br>primers_fa1/primers_fa2 are the upstream primers/trimming/primers_fa{1,2} fasta<br>files (empty upstream default = primers flow off); fa2 empty means single-end<br>primer fasta.</p>
<details class="ox-param-usedby"><summary>used by 8 rules</summary>
<div class="ox-param-rules"><code>mapping_bwa::bwa_index</code> <code>primers::assign_primers</code> <code>primers::build_primer_regions</code> <code>primers::filter_primerless_reads</code> <code>primers::filter_unmapped_primers</code> <code>primers::map_primers</code> <code>primers::primer_to_bed</code> <code>primers::trim_primers</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>primers_fa1</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">upstream config: primers/trimming (rules assign_primers ... build_primer_regions).<br>primers_fa1/primers_fa2 are the upstream primers/trimming/primers_fa{1,2} fasta<br>files (empty upstream default = primers flow off); fa2 empty means single-end<br>primer fasta.</p>
<details class="ox-param-usedby"><summary>used by 1 rules</summary>
<div class="ox-param-rules"><code>primers::map_primers</code></div>
</details>
</div>
<div class="ox-param ox-param-unused">
<div class="ox-param-head"><code>primers_fa2</code><span class="ox-param-default"></span></div>
<p class="ox-param-desc">upstream config: primers/trimming (rules assign_primers ... build_primer_regions).<br>primers_fa1/primers_fa2 are the upstream primers/trimming/primers_fa{1,2} fasta<br>files (empty upstream default = primers flow off); fa2 empty means single-end<br>primer fasta.</p>
<details class="ox-param-usedby"><summary>not referenced by any rule</summary>
<div class="ox-param-rules">A ported upstream parameter kept for compatibility: no rule reads this key (no <code>{config.*}</code> placeholder in any input, output, or shell), so overriding it has no effect on this workflow.</div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>reads_dir</code><span class="ox-param-default">test/fixtures/raw</span></div>
<p class="ox-param-desc">Path to the raw paired-end FASTQs of the single sample (upstream<br>config/units.tsv points at absolute /projects/... paths; the port reads<br>from the repository fixtures instead).</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>mapping::merge_trimmed_fastqs_r1</code> <code>mapping::merge_trimmed_fastqs_r2</code> <code>qc::fastqc_r1</code> <code>qc::fastqc_r2</code> <code>trimming::fastp_pe</code> <code>trimming::fastp_pipe</code> <code>trimming::fastp_se</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>skip_ref_downloads</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">Skip the ref:: download rules (genome, annotation, VEP cache/plugins,<br>pangenome, REVEL, known variants — ~5 GB of public databases). Set to<br>true when you have pre-placed the files at the resource paths the rules<br>declare (see README &quot;Reference databases&quot;); the downloads are hardcoded<br>upstream URLs and need unimpeded network access.</p>
<details class="ox-param-usedby"><summary>used by 7 rules</summary>
<div class="ox-param-rules"><code>ref::download_revel</code> <code>ref::get_annotation</code> <code>ref::get_genome</code> <code>ref::get_known_variants</code> <code>ref::get_pangenome</code> <code>ref::get_vep_cache</code> <code>ref::get_vep_plugins</code></div>
</details>
</div>
<div class="ox-param">
<div class="ox-param-head"><code>trimming_activate</code><span class="ox-param-default">false</span></div>
<p class="ox-param-desc">upstream config: trimming (get_sra / fastp rules). The default path has no<br>trimming configured — reads pass through mapping::merge_trimmed_fastqs.</p>
<details class="ox-param-usedby"><summary>used by 4 rules</summary>
<div class="ox-param-rules"><code>trimming::fastp_pe</code> <code>trimming::fastp_pipe</code> <code>trimming::fastp_se</code> <code>trimming::get_sra</code></div>
</details>
</div>
</div>

Descriptions are the workflow's own `#` comments from its `[config]` section (and the `[config]` sections of its included modules), surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

<img src="../assets/dag/oxo-flow-varlociraptor.svg?v=1788704947" alt="oxo-flow-varlociraptor pipeline overview" loading="lazy">

<p class="ox-dag-caption">figure · oxo-flow-varlociraptor — Scenario-driven somatic small and structural variant calling with Varlociraptor: paired-end reads are aligned against the 1000 Genomes human pangenome with vg giraffe, QC&#x27;d with FastQC/MultiQC, covered with mosdepth, and used for freebayes and delly candidate calling; Varlociraptor then estimates alignment properties and calls variants under a tumor scenario (events present + somatic_tumor_high + somatic_tumor_medium, FDR 0.05), FDR is controlled per variant type (SNV/INS/DEL/MNV/BND/INV/DUP/REP) with merge and phred decoding, and the calls are annotated with VEP (LoFtool/REVEL plugins) and dbSNFP/dbSNP, filtered, turned into a 34-column variant table with oncoprint label-sorting, and rendered as interactive datavzrd variant and gene-coverage reports.</p>

</div>

<p class="ox-dag-note">Read: stations are rules (or module groups); a line is a data dependency; stations without any line are <em>off-track</em> inputs/terminal exports with no dataflow edge; separate groups of lines are independent chains (e.g. a quantifier reading raw reads while the alignment chain runs aside — live: tcasia salmon_quant). The map shows the template DAG; <code>oxo-flow graph --expanded</code> adds one node per sample instance.</p>

The graph is derived at catalog-build time from `oxo-flow graph -f metro` through the adaptive render ladder (`scripts/metro_tiers.py`): each workflow gets the finest metro tier that nf-metro renders while staying readable at site width — rule-level stations for smaller workflows, module-stage or moduleoverview stations for dense ones. Colored transit lines group stations by analysis stage. Wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- annotate_candidate_variants_delly
- annotate_candidate_variants_freebayes
- annotate_descriptions
- annotate_dgidb
- annotate_exons
- annotate_mutational_signatures
- annotate_variants
- annotate_vcfs
- annotated_index
- apply_bqsr
- apply_bqsr_consensus
- arriba
- assign_primers
- bam_index_consensus
- bam_index_dedup
- bcf_index_arriba
- bcf_index_candidate_delly
- bcf_index_candidate_freebayes
- bcf_index_cleaned_db
- bcf_index_delly
- bcf_index_fdr_BND
- bcf_index_fdr_BND_fusions
- bcf_index_fdr_DEL
- bcf_index_fdr_DUP
- bcf_index_fdr_INS
- bcf_index_fdr_INV
- bcf_index_fdr_MNV
- bcf_index_fdr_REP
- bcf_index_fdr_SNV
- bcf_index_filtered
- bcf_index_final
- bcf_index_freebayes
- bcf_index_fusions_callset
- bcf_index_population_filtered
- bcf_index_vep_annotated
- bcftools_concat
- bcftools_concat_candidates
- bcftools_concat_fusions
- bedtools_merge
- build_primer_regions
- build_sample_regions
- bwa_index
- calc_consensus_reads
- calculate_covered_coding_sites
- chm_eval
- chm_eval_kit
- chm_eval_sample
- chm_namesort
- chm_to_fastq
- chromosome_map
- clean_population_db
- control_fdr_BND
- control_fdr_BND_fusions
- control_fdr_DEL
- control_fdr_DUP
- control_fdr_INS
- control_fdr_INV
- control_fdr_MNV
- control_fdr_REP
- control_fdr_SNV
- convert_fusions
- convert_phred_scores
- convert_phred_scores_fusions
- coverage_table
- create_mutational_context_file
- datavzrd_coverage
- datavzrd_variants_calls
- delly
- determine_coding_regions
- download_cadd_scores_for_vep
- download_cosmic_signatures
- download_delly_excluded_regions
- download_revel
- estimate_mutational_burden_curve
- estimate_mutational_burden_hist
- fastp_pe
- fastp_pipe
- fastp_se
- fastqc_r1
- fastqc_r2
- filter_by_annotation
- filter_candidates_by_annotation_delly
- filter_candidates_by_annotation_freebayes
- filter_group_regions_covered
- filter_group_regions_expanded
- filter_offtarget_variants_delly
- filter_offtarget_variants_freebayes
- filter_primerless_reads
- filter_unmapped_primers
- fix_delly_calls
- freebayes
- gather_annotated_calls
- gather_annotated_calls_fusions
- gather_benchmark_calls
- gather_calls
- genome_dict
- genome_faidx
- get_annotation
- get_genome
- get_known_variants
- get_pangenome
- get_reference_paths
- get_sra
- get_target_regions
- get_vep_cache
- get_vep_plugins
- group_bcf_to_vcf_fusions
- group_bcf_to_vcf_variants
- group_vcf_to_maf_fusions
- group_vcf_to_maf_variants
- join_mutational_signatures
- map_consensus_reads_pe
- map_consensus_reads_se
- map_primers
- map_reads_bwa
- map_reads_vg
- mark_duplicates
- merge_calls
- merge_calls_fusions
- merge_consensus_reads
- merge_covered_group_regions
- merge_expanded_group_regions
- merge_trimmed_fastqs_r1
- merge_trimmed_fastqs_r2
- multiqc
- pangenome_autoindex
- plot_mutational_signatures
- population_db_update
- population_filter_variants
- postprocess_vg_alignments
- prepare_oncoprint
- primer_to_bed
- process_call_tables
- process_revel_scores
- recalibrate_base_qualities
- recalibrate_base_qualities_consensus
- remove_iupac_codes
- rename_chromosomes
- render_scenario
- samtools_idxstats
- samtools_stats
- scatter_candidates_delly
- scatter_candidates_freebayes
- sort_alignments
- sort_arriba_calls
- sort_calls_arriba
- sort_calls_delly
- sort_calls_freebayes
- sort_consensus_reads
- star_align
- star_index
- tabix_noiupac
- tabix_revel
- tabix_variation
- transform_gene_annotations
- trim_primers
- varlociraptor_alignment_properties
- varlociraptor_call_arriba
- varlociraptor_call_delly
- varlociraptor_call_freebayes
- varlociraptor_preprocess_arriba
- varlociraptor_preprocess_delly
- varlociraptor_preprocess_freebayes
- vembrane_table

**Excluded**

- fusions report and table exports (report.smk / table.smk fusions instances) — the ported fusions FDR-control chain (filtering.oxoflow) ends at the fdr-controlled/normal-probs callsets; the fusions vembrane table, oncoprints and report datasets need calling mode fusions + fusion_activate = true end-to-end data to verify

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
