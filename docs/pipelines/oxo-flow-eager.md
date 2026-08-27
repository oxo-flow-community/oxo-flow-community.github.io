# Ancient DNA (aDNA): QC, mapping, damage estimation and genotyping

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Ancient DNA (aDNA) analysis in one run: FastQC raw QC, optional fastp poly-G filtering (2-colour chemistry), AdapterRemoval adapter clipping and paired-end read merging, BWA aln mapping with ancient-DNA parameters, picard MarkDuplicates (or DeDup) deduplication, preseq library-complexity curves, DamageProfiler damage estimation, Qualimap BAM QC, optional pileupCaller genotyping with eigenstrat SNP coverage, optional metagenomic screening of the unmapped reads (bbduk entropy complexity filter, MALT or kraken2 classification with kraken_parse/kraken_merge tables, MaltExtract aDNA evaluation), and a final MultiQC report — every rule pinned to the nf-core/eager 2.5.3 tool versions in the upstream container (MALT 0.61 and HOPs 0.35 ship in the pinned nfcore/eager:2.5.3 image).

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 54 |
| **Compute** | up to 4 CPUs / 8 GB per rule (bwa_aln) |
| **Tools** | fastqc · adapterremoval · adapterremovalfixprefix · bwa · samtools · picard · dedup · preseq · damageprofiler · qualimap · sequencetools · eigenstratdatabasetools · fastp · bbduk · kraken2 · malt · hops · pigz · multiqc · rename · python |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/eager](https://github.com/nf-core/eager) |
| **Pinned version** | `2.5.3` |

## Run it

```bash
oxo-flow run main.oxoflow
```

Needs reference genome and reads — see Requirements.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** containers (Docker/Singularity) — pinned image nfcore/eager:2.5.3 for all rules (bundles the pinned conda env from envs/eager.yaml)

**Requirements.**
- reference genome FASTA, plain and uncompressed (.gz references are not supported — upstream's unzip_reference step is not ported); the workflow builds the .fai / .dict / BWA indices itself
- paired-end FASTQ pairs named <sample>_R1.fastq.gz / <sample>_R2.fastq.gz in a directory (directory input mode; sample = text before the _R1/_R2 suffix); single-end is not supported
- optional — pileupCaller genotyping (run_genotyping=true genotyping_tool='pileupcaller') requires pileupcaller_snpfile and pileupcaller_bedfile; the rule fails fast without them
- optional — metagenomic screening (run_metagenomic_screening=true, bam_unmapped_type='fastq') requires metagenomic_tool='kraken' with a kraken2_db (kraken2 database directory or .tar.gz bundle, unpacked by the kraken rule) or metagenomic_tool='malt' with a malt_db (MALT database directory); maltextract additionally requires maltextract_taxon_list and maltextract_ncbifiles. The chain is validate/dry-run-tested but not yet live-verified
- compute: up to 4 CPUs / 8 GB RAM per rule (bwa_aln: 4 threads / 8G; kraken: 4 threads / 8G — upstream's mc_huge label is 32 cpus / 256 GB, tune via CLI overrides; reference-index and MultiQC rules up to 8 GB; base default 1 CPU / 7 GB / 24 h)
- Docker or Singularity to run the pinned container nfcore/eager:2.5.3 (not needed for validate / lint / dry-run)
- disk: results/ holds reference indices, mapped BAMs and reports — size grows with the reference genome and number of samples

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-eager
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-eager
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `angsd_fasta_arg` | `` | — | `genotyping_angsd` |
| `angsd_glformat` | `4` | — | `genotyping_angsd` |
| `angsd_glmodel` | `1` | — | `genotyping_angsd` |
| `angsd_majorminor_arg` | `` | — | `genotyping_angsd` |
| `anno_file` | `` | — | `bedtools_coverage` |
| `anno_file_is_unsorted_neg` | `-sorted` | — | `bedtools_coverage` |
| `bam_input` | `false` | — | `convert_bam` |
| `bam_mapping_quality_threshold` | `0` | — | `samtools_filter_bowtie2`, `samtools_filter_bwaaln`, `samtools_filter_bwamem`, `samtools_filter_circularmapper` |
| `bam_unmapped_type` | `discard` | — | `kraken`, `kraken_merge`, `kraken_parse`, `malt`, `metagenomic_complexity_filter`, `samtools_filter_bowtie2`, `samtools_filter_bwaaln`, `samtools_filter_bwamem`, `samtools_filter_circularmapper` |
| `bamutils_clip_double_stranded_none_udg_left` | `1` | — | `bam_trim` |
| `bamutils_clip_double_stranded_none_udg_right` | `1` | — | `bam_trim` |
| `bamutils_softclip_arg` | `` | — | `bam_trim` |
| `bcftools_stats_source` | `haplotypecaller` | — | `bcftools_stats` |
| `bt2_preset` | `` | — | `bowtie2` |
| `bwaalnk` | `2` | — | `bwa_aln`, `circularmapper` |
| `bwaalnl` | `1024` | — | `bwa_aln`, `circularmapper` |
| `bwaalnn` | `0.01` | — | `bwa_aln`, `circularmapper` |
| `bwaalno` | `2` | — | `bwa_aln` |
| `circularextension` | `100` | — | `circulargenerator`, `circularmapper` |
| `circularfilter_arg` | `` | — | `circularmapper` |
| `circulartarget` | `chrMT` | — | `circulargenerator` |
| `clip_forward_adaptor` | `AGATCGGAAGAGCACACGTCTGAACTCCAGTCAC` | read clipping / merging | `adapter_removal` |
| `clip_min_read_quality` | `20` | — | `adapter_removal` |
| `clip_readlength` | `30` | — | `adapter_removal` |
| `clip_reverse_adaptor` | `AGATCGGAAGAGCGTCGTGTAGGGAAAGAGTGTA` | — | `adapter_removal` |
| `colour_chemistry` | `4` | — | `fastp` |
| `complexity_filter_poly_g` | `false` | complexity (poly-G) filter | `fastp` |
| `complexity_filter_poly_g_min` | `10` | — | `fastp` |
| `damage_calculation_tool` | `damageprofiler` | damage estimation | `damageprofiler`, `mapdamage_calculation` |
| `damageprofiler_length` | `100` | — | `damageprofiler` |
| `damageprofiler_threshold` | `15` | — | `damageprofiler` |
| `damageprofiler_yaxis` | `0.30` | — | `damageprofiler` |
| `dedup_all_merged` | `false` | — | — |
| `dedupper` | `markduplicates` | deduplication | `dedup`, `markduplicates` |
| `fasta` | `test/fixtures/reference/genome.fa` | input / library metadata (directory-input mode defaults) | `make_bwa_index`, `make_fasta_index`, `make_seq_dict`, `unzip_reference` |
| `freebayes_C` | `2` | — | `genotyping_freebayes` |
| `freebayes_g_arg` | `` | — | `genotyping_freebayes` |
| `freebayes_p` | `1` | — | `genotyping_freebayes` |
| `gatk_call_conf` | `30` | — | `genotyping_hc`, `genotyping_ug` |
| `gatk_downsample` | `250` | — | `genotyping_ug` |
| `gatk_hc_emitrefconf` | `NONE` | — | `genotyping_hc` |
| `gatk_hc_out_mode` | `EMIT_VARIANTS_ONLY` | — | `genotyping_hc` |
| `gatk_ploidy` | `2` | — | `genotyping_hc`, `genotyping_ug` |
| `gatk_ug_defaultbasequalities_arg` | `` | — | `genotyping_ug` |
| `gatk_ug_genotype_model` | `SNP` | — | `genotyping_ug` |
| `gatk_ug_out_mode` | `EMIT_VARIANTS_ONLY` | — | `genotyping_ug` |
| `genotyping_source` | `raw` | — | — |
| `genotyping_tool` | `` | — | `eigenstrat_snp_coverage`, `genotyping_angsd`, `genotyping_freebayes`, `genotyping_hc`, `genotyping_pileupcaller`, `genotyping_ug`, `multivcfanalyzer`, `picard_addorreplacereadgroups` |
| `hostremoval_input_fastq` | `false` | — | `hostremoval_input_fastq` |
| `hostremoval_mode` | `mapped` | — | `hostremoval_input_fastq` |
| `input_bam` | `` | — | `convert_bam` |
| `kraken2_db` | `` | — | `kraken` |
| `lane` | `0` | — | `adapter_removal`, `bwa_aln`, `fastp`, `fastqc_after_clipping`, `post_ar_fastq_trimming` |
| `large_ref` | `false` | — | — |
| `malt_alignment_mode` | `SemiGlobal` | — | `malt` |
| `malt_db` | `` | — | `malt` |
| `malt_max_queries` | `100` | — | `malt` |
| `malt_memory_mode` | `load` | — | `malt` |
| `malt_min_support_mode` | `percent` | — | `malt` |
| `malt_min_support_percent` | `0.01` | — | `malt` |
| `malt_mode` | `BlastN` | — | `malt` |
| `malt_sam_output` | `false` | — | `malt` |
| `malt_top_percent` | `1` | — | `malt` |
| `maltextract_destackingoff` | `false` | — | `maltextract` |
| `maltextract_downsamplingoff` | `false` | — | `maltextract` |
| `maltextract_duplicateremovaloff` | `false` | — | `maltextract` |
| `maltextract_filter` | `def_anc` | — | `maltextract` |
| `maltextract_matches` | `false` | — | `maltextract` |
| `maltextract_megansummary` | `false` | — | `maltextract` |
| `maltextract_ncbifiles` | `` | — | `maltextract` |
| `maltextract_percentidentity` | `85.0` | — | `maltextract` |
| `maltextract_taxon_list` | `` | — | `maltextract` |
| `maltextract_topalignment` | `false` | — | `maltextract` |
| `maltextract_toppercent` | `0.01` | — | `maltextract` |
| `mapdamage_downsample_arg` | `` | — | `mapdamage_calculation` |
| `mapdamage_singlestranded_arg` | `` | — | `mapdamage_calculation`, `mapdamage_rescaling` |
| `mapdamage_yaxis` | `0.25` | — | `mapdamage_calculation` |
| `mapper` | `bwaaln` | mapping | `bowtie2`, `bwa_aln`, `bwamem`, `circulargenerator`, `circularmapper`, `make_bt2_index`, `samtools_filter_bowtie2`, `samtools_filter_bwaaln`, `samtools_filter_bwamem`, `samtools_filter_circularmapper` |
| `mergedonly` | `false` | — | — |
| `metagenomic_complexity_entropy` | `0.3` | — | `metagenomic_complexity_filter` |
| `metagenomic_complexity_filter` | `false` | — | `kraken`, `malt`, `metagenomic_complexity_filter` |
| `metagenomic_min_support_reads` | `1` | — | `kraken_parse`, `malt` |
| `metagenomic_tool` | `` | — | `kraken`, `kraken_merge`, `kraken_parse`, `malt`, `maltextract` |
| `min_adap_overlap` | `1` | — | `adapter_removal` |
| `min_allele_freq_het` | `0.2` | — | `multivcfanalyzer` |
| `min_allele_freq_hom` | `0.8` | — | `multivcfanalyzer` |
| `min_base_coverage` | `0` | — | `multivcfanalyzer` |
| `min_genotype_quality` | `0` | — | `multivcfanalyzer` |
| `mtnucratio_header` | `MT` | — | `mtnucratio` |
| `multivcf_samples` | `'S1', 'S2'` | — | — |
| `nuclear_contamination_header` | `` | — | `nuclear_contamination` |
| `out_dir` | `results` | — | — |
| `percent_identity` | `85` | — | `malt` |
| `pileupcaller_bedfile` | `` | — | `genotyping_pileupcaller` |
| `pileupcaller_method` | `randomHaploid` | — | — |
| `pileupcaller_min_base_quality` | `30` | — | `genotyping_pileupcaller` |
| `pileupcaller_min_map_quality` | `30` | — | `genotyping_pileupcaller` |
| `pileupcaller_snpfile` | `` | — | `genotyping_pileupcaller` |
| `pileupcaller_transitions_mode` | `AllSites` | — | — |
| `pmdtools_mask_bed` | `` | — | `mask_reference_for_pmdtools` |
| `pmdtools_max_reads` | `1000000` | — | `pmdtools` |
| `pmdtools_platypus_arg` | `` | — | `pmdtools` |
| `pmdtools_range` | `10` | — | `pmdtools` |
| `pmdtools_reference_mask` | `false` | — | `mask_reference_for_pmdtools` |
| `pmdtools_threshold` | `3` | — | `pmdtools` |
| `pmdtools_treatment_arg` | `--UDGminus` | — | `pmdtools` |
| `post_ar_trim_front` | `0` | — | `post_ar_fastq_trimming` |
| `post_ar_trim_front2` | `0` | — | — |
| `post_ar_trim_tail` | `0` | — | `post_ar_fastq_trimming` |
| `post_ar_trim_tail2` | `0` | — | — |
| `preseq_bootstrap` | `100` | — | — |
| `preseq_cval` | `0.95` | — | — |
| `preseq_maxextrap` | `10000000000` | — | — |
| `preseq_mode` | `c_curve` | — | — |
| `preseq_step_size` | `1000` | preseq | `preseq` |
| `preseq_terms` | `100` | — | — |
| `preserve5p` | `false` | — | — |
| `qualitymax` | `41` | — | `adapter_removal` |
| `reference_gff_annotations` | `` | — | `multivcfanalyzer` |
| `reference_gff_exclude` | `` | — | `multivcfanalyzer` |
| `rescale_length_3p_arg` | `` | — | `mapdamage_rescaling` |
| `rescale_length_5p_arg` | `` | — | `mapdamage_rescaling` |
| `rescale_seqlength` | `12` | — | `mapdamage_rescaling` |
| `run_bam_filtering` | `false` | — | `kraken`, `kraken_merge`, `kraken_parse`, `malt`, `metagenomic_complexity_filter`, `samtools_filter_bowtie2`, `samtools_filter_bwaaln`, `samtools_filter_bwamem`, `samtools_filter_circularmapper`, `samtools_flagstat_after_filter` |
| `run_bcftools_stats` | `false` | — | `bcftools_stats` |
| `run_bedtools_coverage` | `false` | — | `bedtools_coverage` |
| `run_endor_spy` | `false` | — | `endor_spy` |
| `run_genotyping` | `false` | genotyping (pileupCaller branch) | `eigenstrat_snp_coverage`, `genotyping_angsd`, `genotyping_freebayes`, `genotyping_hc`, `genotyping_pileupcaller`, `genotyping_ug`, `multivcfanalyzer`, `picard_addorreplacereadgroups` |
| `run_maltextract` | `false` | — | `maltextract` |
| `run_mapdamage_rescaling` | `false` | — | `mapdamage_rescaling` |
| `run_metagenomic_screening` | `false` | — | `kraken`, `kraken_merge`, `kraken_parse`, `malt` |
| `run_mtnucratio` | `false` | — | `mtnucratio` |
| `run_multivcfanalyzer` | `false` | — | `multivcfanalyzer`, `picard_addorreplacereadgroups` |
| `run_nuclear_contamination` | `false` | — | `nuclear_contamination`, `print_nuclear_contamination` |
| `run_pmdtools` | `false` | — | `mask_reference_for_pmdtools`, `pmdtools` |
| `run_post_ar_trimming` | `false` | — | `post_ar_fastq_trimming` |
| `run_sexdeterrmine` | `false` | — | `sexdeterrmine`, `sexdeterrmine_prep` |
| `run_trim_bam` | `false` | — | `bam_trim` |
| `run_vcf2genome` | `false` | — | `vcf2genome` |
| `save_reference` | `false` | — | — |
| `seqtype` | `PE` | — | `bwa_aln` |
| `sexdeterrmine_prep_s` | `1000000` | — | `sexdeterrmine_prep` |
| `sexdeterrmine_s` | `1000000` | — | `sexdeterrmine` |
| `single_end` | `false` | — | — |
| `single_stranded` | `false` | — | `maltextract` |
| `skip_adapterremoval` | `false` | — | `adapter_removal`, `fastqc_after_clipping` |
| `skip_collapse` | `false` | — | — |
| `skip_damage_calculation` | `false` | — | `damageprofiler`, `mapdamage_calculation` |
| `skip_deduplication` | `false` | — | `dedup`, `markduplicates` |
| `skip_fastqc` | `false` | skipping (upstream defaults: run everything except optional branches) | `fastqc`, `fastqc_after_clipping` |
| `skip_preseq` | `false` | — | `preseq` |
| `skip_qualimap` | `false` | — | `qualimap` |
| `skip_trim` | `false` | — | — |
| `snp_eff_results` | `` | — | `multivcfanalyzer` |
| `udg_type` | `none` | — | — |
| `unzip_reference` | `false` | see rules/branches.oxoflow for the ported rules + the structural exclusions (lane/library merging, nf-core boilerplate). | `unzip_reference` |
| `vcf2genome_minc` | `5` | — | `vcf2genome` |
| `vcf2genome_minfreq` | `0.5` | — | `vcf2genome` |
| `vcf2genome_minq` | `30` | — | `vcf2genome` |
| `write_allele_frequencies_arg` | `F` | — | `multivcfanalyzer` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-eager rule-level DAG](../assets/dag/oxo-flow-eager.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- make_fasta_index
- make_seq_dict
- make_bwa_index
- fastqc
- fastp
- adapter_removal
- fastqc_after_clipping
- bwa_aln
- samtools_flagstat
- markduplicates
- dedup
- preseq
- damageprofiler
- qualimap
- genotyping_pileupcaller
- eigenstrat_snp_coverage
- multiqc
- unzip_reference
- bwamem
- make_bt2_index
- bowtie2
- circulargenerator
- circularmapper
- convert_bam
- hostremoval_input_fastq
- samtools_filter
- samtools_flagstat_after_filter
- endor_spy
- bedtools_coverage
- post_ar_fastq_trimming
- bam_trim
- picard_addorreplacereadgroups
- genotyping_ug
- genotyping_hc
- genotyping_freebayes
- genotyping_angsd
- bcftools_stats
- vcf2genome
- multivcfanalyzer
- sexdeterrmine_prep
- sexdeterrmine
- mtnucratio
- nuclear_contamination
- print_nuclear_contamination
- mapdamage_calculation
- mapdamage_rescaling
- mask_reference_for_pmdtools
- pmdtools
- metagenomic_complexity_filter
- kraken
- kraken_parse
- kraken_merge
- malt
- maltextract

**Excluded**

- lanemerge / lanemerge_hostremoval_fastq, library_merge / additional_library_merge, seqtype_merge — structural: oxo-flow instances are driven by wildcard combinations (one fastq pair per sample row); expand_inputs only fans files INTO one cohort instance, there is no per-sample multi-file grouping primitive (remediation: pre-concatenate or separate sample rows)
- output_documentation, get_software_versions — nf-core boilerplate (unconditional upstream would change the default plan; versions.yml has no oxo-flow equivalent)

## Fidelity

Every upstream process of nf-core/eager 2.5.3 (63 total: 56 top-level
processes plus 7 conditional/indented ones — `makeBWAIndex`,
`makeBT2Index`, `unzip_reference`, `seqtype_merge`, `mtnucratio`,
`nuclear_contamination`, `decomp_kraken`) is listed below.
The 17 processes on the default-parameters main path (directory input,
paired-end, `mapper=bwaaln`, `dedupper=markduplicates`) are ported
byte-faithfully. The non-default branches are ported as `rules/branches.oxoflow`
(each gated on its upstream param, off by default) — including the full
metagenomic screening chain (bbduk complexity filter, kraken, kraken_parse,
kraken_merge, malt, maltextract; note the old "needs the upstream's bundled
MALT install (no conda package)" exclusion reason was wrong — the upstream
`environment.yml` pins `bioconda::malt=0.61` and `bioconda::hops=0.35`, so
MALT and MaltExtract ship inside the pinned `nfcore/eager:2.5.3` container).
The remaining `not ported` rows are structural (multi-lane/library channel
merges — oxo-flow has no per-sample multi-file grouping primitive), the
unported BAM pass-through mode (`indexinputbam`), or nf-core boilerplate
(`output_documentation`, `get_software_versions`).

| Upstream process | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| unzip_reference | `unzip_reference` | pigz 2.6 | `gunzip -c` into the canonical reference path; `when = config.unzip_reference` (default false — pass a plain FASTA as before) |
| makeFastaIndex | `make_fasta_index` | samtools 1.12 | `samtools faidx` verbatim. Port copies the input to `results/reference_genome/fasta_index/reference.fa` (canonical name; upstream publishes `<fasta-base>.fai` only when `--save_reference`) |
| makeSeqDict | `make_seq_dict` | picard 2.26.0 | `picard -Xmx8192M CreateSequenceDictionary` verbatim; output named `reference.dict` (upstream `<fasta-base>.dict`) |
| makeBWAIndex | `make_bwa_index` | bwa 0.7.17 | `cp` into `BWAIndex/` + `bwa index` verbatim; canonical file name `reference.fa` |
| fastqc | `fastqc` | fastqc 0.11.9 | `fastqc -t N -q r1 r2` + rename `*_fastqc.zip` → `*_raw_fastqc.zip` verbatim (per-instance scoped rename; zips moved to `zips/` like the upstream publishDir saveAs) |
| fastp | `fastp` | fastp 0.20.1 | Off by default, same as upstream (`complexity_filter_poly_g=false`). PE branch flags verbatim. **Upstream feeds fastp only the 2-colour-chemistry branch** (`ch_input_for_fastp.twocol`, main.nf lines 723-746): with the default `colour_chemistry=4` fastp runs on zero samples even when the flag is on. The port mirrors this gate (`when = complexity_filter_poly_g && colour_chemistry == 2`); use `colour_chemistry=2` to actually filter poly-G |
| adapter_removal | `adapter_removal` | adapterremoval 2.3.2, adapterremovalfixprefix 0.0.5, pigz 2.6 | Default PE collapse branch verbatim: `--collapse --trimns --trimqualities`, cat of the 5 gz parts (`<base>.pe.collapsed.gz` etc. — the `.pe` basename AR writes, as upstream), `AdapterRemovalFixPrefix \| pigz -p <cpus-1>`. The `cat` operands are explicit per-sample names (shared results dir; upstream globs the workdir). When fastp is enabled the input switches to the fastp outputs (upstream channel mix); the AR basename stays the default-path one (`{r1.baseName}_L0` with the `_R1` suffix as upstream derives it) |
| fastqc_after_clipping | `fastqc_after_clipping` | fastqc 0.11.9 | Verbatim; zips to `zips/` |
| bwa | `bwa_aln` | bwa 0.7.17, samtools 1.12 | Verbatim PE branch: `bwa aln -n/-l/-k/-o` (Oliva 2021 defaults), `bwa samse` with the eager `@RG` string, `samtools sort -@ <cpus-1>`, `samtools index`. `.sai` written into the mapping dir (upstream workdir-local) |
| bwamem | `bwamem` | bwa 0.7.17, samtools 1.12 | `bwa mem -t N` + sort + index with the eager @RG string; `when = config.mapper == 'bwamem'` |
| bowtie2 | `bowtie2` | bowtie2 2.4.4, samtools 1.12 | `bowtie2 -x reference -1/-2` + sort + index; `when = config.mapper == 'bowtie2'` |
| makeBT2Index | `make_bt2_index` | bowtie2 2.4.4 | `bowtie2-build` into `results/reference_genome/bt2_index/`; `when = config.mapper == 'bowtie2'` |
| circulargenerator | `circulargenerator` | circularmapper 1.93.5, bwa | `circulargenerator -e -i -s` + `bwa index` on the elongated fasta; `when = config.mapper == 'circularmapper'` |
| circularmapper | `circularmapper` | bwa + circularmapper 1.93.5 | `bwa aln` on the elongated reference + `realignsamfile` + sort/index; `when = config.mapper == 'circularmapper'` |
| convertBam | `convert_bam` | samtools 1.12, pigz | `samtools bam2fq | pigz`; `when = config.bam_input` (default false — the fixture is FASTQ) |
| indexinputbam | — | samtools 1.12 | not ported — indexes the input BAM for upstream's BAM pass-through mode (`bam != 'NA' && !run_convertinputbam`, main.nf 657); the port's BAM-input mode routes through `convert_bam` (bam2fq) instead and nothing downstream consumes the input BAM directly, so no index is needed |
| hostremoval_input_fastq | `hostremoval_input_fastq` | extract_map_reads.py (bundled) | PE branch verbatim (`-m`, `-of`/`-or`, `-t`); `when = config.hostremoval_input_fastq` |
| samtools_flagstat | `samtools_flagstat` | samtools 1.12 | Verbatim: `samtools flagstat > {libraryid}_flagstat.stats` |
| samtools_filter | `samtools_filter_{bwaaln,bwamem,bowtie2,circularmapper}` | samtools 1.12, pigz 2.6 | Four per-mapper rules sharing ONE output set; each is gated `when = config.run_bam_filtering && config.mapper == '<mapper>'` (mutually exclusive, so the released engine needs no any-mode semantics) and takes its mapper's mapped BAM as `BAM="{input[0]}"` (`results/mapping/bwa/{sample}_PE.mapped.bam` / `results/mapping/bwa/{sample}.mapped.bam` / `results/mapping/bt2/{sample}.mapped.bam` / `results/mapping/circularmapper/{sample}.mapped.bam`). The shared body carries the minreadlength-0 branches selected by `bam_unmapped_type`: `discard` (`-F4 -q <thr>`, default) and `fastq` (upstream `-f4` / `-F4 -q` + `samtools fastq -tN \| pigz -p <cpus-1>` + `rm`, the metagenomic-chain producer), both verbatim. The discard branch additionally writes an EMPTY `{sample}.unmapped.fastq.gz` placeholder — the engine requires every declared output to exist, and it is never consumed (the metagenomic rules are gated on `bam_unmapped_type == 'fastq'`). The `keep`/`bam`/`both` branches fail fast with a clear error; bwaaln variant live-verified on tx-ubuntu 2026-08-27 (run_bam_filtering=true, 15 succeeded / 0 failed) |
| samtools_flagstat_after_filter | `samtools_flagstat_after_filter` | samtools 1.12 | `samtools flagstat` on the filtered BAM; `when = config.run_bam_filtering` |
| picard_addorreplacereadgroups | `picard_addorreplacereadgroups` | picard 2.26.0, samtools | verbatim RG replacement for MultiVCFAnalyzer; `when = run_genotyping && genotyping_tool == 'ug' && run_multivcfanalyzer` |
| markduplicates | `markduplicates` | picard 2.26.0, samtools 1.12 | Default dedupper. picard MarkDuplicates verbatim (`-Xmx4096M`, `REMOVE_DUPLICATES=TRUE AS=TRUE`, `VALIDATION_STRINGENCY=SILENT`) + `samtools index`. INPUT points at the mapped BAM directly instead of upstream's workdir-local `mv {bam} {libraryid}.bam` rename (the shared results dir must keep the mapped BAM for preseq/flagstat) |
| dedup | `dedup` | dedup 0.12.8, samtools 1.12 | Alternative dedupper (off by default, `dedupper='dedup'`). Verbatim: `dedup -Xmx4g -i ... -o . -u`, `mv *.log dedup.log`, in-place `samtools sort`, index. Upstream's `mv {bam} {libraryid}.bam` becomes a `cp` (shared-results-dir equivalent, same effect) |
| preseq | `preseq` | preseq 3.1.2 | Verbatim default branch: `preseq c_curve -s 1000 -o <base>.preseq -B <mapped bam>`. The `-H` (dedup mode) and `lc_extrap` branches are the alternate `preseq_mode`/`dedupper` combinations |
| bedtools | `bedtools_coverage` | bedtools 2.30.0, pigz | verbatim genome.txt + `bedtools coverage` breadth/depth; `when = config.run_bedtools_coverage` |
| damageprofiler | `damageprofiler` | damageprofiler 0.4.9 | Verbatim: `-Xmx4g -i <rmdup bam> -r <fasta> -l 100 -t 15 -o . -yaxis_damageplot 0.30`; output lands in `results/damageprofiler/<bam-basename>/` as upstream |
| mapdamage_calculation | `mapdamage_calculation` | mapdamage2 2.2.1 | verbatim `mapDamage -i -r --ymax --no-stats`; `when = !skip_damage_calculation && damage_calculation_tool == 'mapdamage'` |
| mapdamage_rescaling | `mapdamage_rescaling` | mapdamage2 2.2.1, samtools | verbatim `--rescale --rescale-out --seq-length` + index; `when = config.run_mapdamage_rescaling` |
| mask_reference_for_pmdtools | `mask_reference_for_pmdtools` | bedtools 2.30.0 | `bedtools maskfasta`; `when = pmdtools_reference_mask && run_pmdtools` |
| pmdtools | `pmdtools` | pmdtools 0.60, samtools | verbatim calmd|pmdtools filter + range chain incl. the 141 trap; `when = config.run_pmdtools` |
| bam_trim | `bam_trim` | bamutil 1.0.15, samtools | `bam trimBam -L -R` (double-stranded none-UDG clip values) + sort/index; `when = config.run_trim_bam` |
| post_ar_fastq_trimming | `post_ar_fastq_trimming` | fastp 0.20.1 | PE branch verbatim (`--trim_front1/2 --trim_tail1/2`); `when = config.run_post_ar_trimming` |
| lanemerge | — | — | not ported — structural: multi-lane merging groups N per-lane fastq pairs into one sample; oxo-flow rule instances are driven by wildcard combinations (one fastq pair per sample row), and `expand_inputs` only fans several files INTO one cohort instance — there is no primitive that groups several files of one sample into a single per-sample instance. Pre-concatenate the lanes (or declare the merged pair) before running |
| lanemerge_hostremoval_fastq | — | — | not ported — structural: multi-lane + host removal combination (same constraint as lanemerge) |
| library_merge | — | — | not ported — structural: multi-library merging (same constraint as lanemerge — one fastq pair per sample row); merge libraries before the run or declare each library as its own sample |
| additional_library_merge | — | — | not ported — structural: multi-library merging (same constraint) |
| seqtype_merge | — | samtools 1.12 | not ported — structural: PE/SE mixed-input merge (main.nf line 1597) needs per-sample multi-file grouping; the port is pure-PE. Convert SE samples to PE or run SE-only samples separately |
| qualimap | `qualimap` | qualimap 2.2.2d | Default path, ported: `qualimap bamqc -bam <rmdup bam> -nt 2 -outdir . -outformat "HTML" --java-mem-size=4G` verbatim; output lands in `results/qualimap/<bam-base>_bamqc/` as upstream |
| genotyping_pileupcaller | `genotyping_pileupcaller` | samtools 1.12, sequencetools 1.5.2 | Off by default, same as upstream (`run_genotyping=false`). Verbatim: `samtools mpileup -B --ignore-RG -q 30 -Q 30 [-l <bed>] -f <fasta> <bams> \| pileupCaller --randomHaploid --sampleNames <csv> [-f <snp>] -e pileupcaller.double` (single-instance fan-in; `-e` prefix `pileupcaller.double` = PE strandedness). `-l`/`-f` render only when `pileupcaller_bedfile`/`pileupcaller_snpfile` are set, exactly as upstream's dummy-file check (main.nf lines 2608-2609); without them the rule fails fast with upstream's error message — upstream exits 1 at workflow start (main.nf lines 74-78), the port's guard lives in the rule shell because oxo-flow has no params-validation stage |
| genotyping_ug | `genotyping_ug` | gatk3 3.5, bgzip | verbatim RealignerTargetCreator → IndelRealigner → UnifiedGenotyper → bgzip; `when = run_genotyping && genotyping_tool == 'ug'` |
| genotyping_hc | `genotyping_hc` | gatk4 4.2.0.0, bgzip | verbatim HaplotypeCaller flags + bgzip; `when = run_genotyping && genotyping_tool == 'hc'` |
| genotyping_freebayes | `genotyping_freebayes` | freebayes 1.3.5, bgzip | verbatim `freebayes -f -p -C [-g]` + bgzip; `when = run_genotyping && genotyping_tool == 'freebayes'` |
| genotyping_angsd | `genotyping_angsd` | angsd 0.935 | verbatim bam.filelist + `angsd -GL -doGlF`; `when = run_genotyping && genotyping_tool == 'angsd'` |
| bcftools_stats | `bcftools_stats` | bcftools 1.12 | `bcftools stats <vcf.gz> -F <fasta>`; `when = config.run_bcftools_stats` (source VCF via `bcftools_stats_source`) |
| eigenstrat_snp_coverage | `eigenstrat_snp_coverage` | eigenstratdatabasetools 1.0.2, python 3.9.4 | Off by default, same as upstream. Verbatim: `eigenstrat_snp_coverage -i pileupcaller.double >double_eigenstrat_coverage.txt` + `parse_snp_cov.py` (bundled upstream script, called via `python3 scripts/parse_snp_cov.py` — oxo-flow does not auto-add `bin/` to PATH) |
| metagenomic_complexity_filter | `metagenomic_complexity_filter` | bbduk 38.92 | verbatim `bbduk.sh -Xmx<g>g in=... threads=N entropymask=f entropy=<entropy> out=<in>_lowcomplexityremoved.fq.gz 2> <in>_bbduk.stats` — the output keeps upstream's `${input}_lowcomplexityremoved.fq.gz` naming; `when = metagenomic_complexity_filter && run_bam_filtering && bam_unmapped_type == 'fastq'` (upstream validates the same combination at workflow start, main.nf 115-122) |
| malt | `malt` | malt 0.61 | verbatim `malt-run -J-Xmx<g>g -t N -v -o . -d <db> [-a . -f SAM] -id -m -at -top <min-supp> -mq --memoryMode -i <all fastqs>` — one instance over ALL samples' unmapped reads (upstream `collect()`); reads the entropy-filtered fastqs when the complexity filter is on (upstream channel switch); `--database` is split into `malt_db` + `kraken2_db`; the percent/reads min-support exclusivity check (main.nf 129-134) is a shell guard; the per-input `.rma6` outputs are undeclared (no fixed template) — only `malt.log` is declared; NOT yet live-verified; `when = run_metagenomic_screening && run_bam_filtering && bam_unmapped_type == 'fastq' && metagenomic_tool == 'malt'` |
| maltextract | `maltextract` | hops 0.35 | verbatim `MaltExtract -Xmx<g>g -t <taxon_list> -i <rma6s> -o results/ -r <ncbifiles> -p N -f -a --minPI <flags>` + `postprocessing.AMPS.r -r results/ -m -t N -n <taxon_list> -j`; requires `maltextract_taxon_list` + `maltextract_ncbifiles` (fail-fast guard); consumes the rma6s via glob with a DAG edge through `malt.log`; NOT yet live-verified; `when = run_maltextract && metagenomic_tool == 'malt'` (upstream verbatim) |
| kraken | `kraken` | kraken2 2.1.2 | verbatim `kraken2 --db <db> --threads N --output <prefix>.kraken.out --report-minimizer-data --report <prefix>.kraken2_report <fastq>` + `cut -f1-3,6-8 > <prefix>.kreport`; reads the entropy-filtered fastq when the complexity filter is on (upstream channel switch); the output prefix is normalized to `{sample}.unmapped.fastq` in both branches (upstream prefixes by the input basename — see deviations); NOT yet live-verified; `when = run_metagenomic_screening && run_bam_filtering && bam_unmapped_type == 'fastq' && metagenomic_tool == 'kraken'` |
| kraken_parse | `kraken_parse` | python 3.9.4 | verbatim `kraken_parse.py -c <min_support_reads> -or <read csv> -ok <kmer csv> <kreport>` (upstream script bundled in `scripts/`, called via `python3 scripts/kraken_parse.py` — oxo-flow does not auto-add `bin/` to PATH); gated on the same `when` as kraken (upstream no-ops the process via an empty channel); NOT yet live-verified |
| kraken_merge | `kraken_merge` | python 3.9.4 | verbatim `merge_kraken_res.py -or kraken_read_count.csv -ok kraken_kmer_duplication.csv` (upstream script bundled in `scripts/`; it scans the working dir for the per-sample CSVs, which the fan-in gathers into one instance); gated on the same `when` as kraken; NOT yet live-verified |
| decomp_kraken | `kraken` (folded in) | kraken2 2.1.2 | folded into the kraken shell: a `.tar.gz` `kraken2_db` is unpacked in place (`tar xzf`, `mkdir -p <db>`, `mv *.k2d <db>/`) — no when-expression can test a filename suffix (deviation, documented below) |
| sexdeterrmine | `sexdeterrmine` | sexdeterrmine 1.1.2 | verbatim sexdeterrmine.py run; `when = config.run_sexdeterrmine` |
| sexdeterrmine_prep | `sexdeterrmine_prep` | sexdeterrmine 1.1.2 | verbatim sexdeterrmine_prep.py; `when = config.run_sexdeterrmine` |
| mtnucratio | `mtnucratio` | sequencetools 1.5.2 | verbatim `mtnucratio -Xmx`; `when = config.run_mtnucratio` |
| nuclear_contamination | `nuclear_contamination` | angsd 0.935 (contaminationX) | verbatim contaminationX invocation; `when = config.run_nuclear_contamination` |
| endorSpy | `endor_spy` | endorSpy | `endorS.py -o json -n <sample> <flagstat>`; `when = config.run_endor_spy` (upstream runs it unconditionally; the port gates it to keep the default path unchanged) |
| print_nuclear_contamination | `print_nuclear_contamination` | grep | report row extraction; `when = config.run_nuclear_contamination` |
| multivcfanalyzer | `multivcfanalyzer` | multivcfanalyzer 0.85.2, pigz | verbatim cohort run over all UG VCFs (expand_inputs over `multivcf_samples`); `when = run_genotyping && genotyping_tool == 'ug' && run_multivcfanalyzer` |
| vcf2genome | `vcf2genome` | vcf2genome 0.91, pigz | verbatim consensus call incl. refMod/uncertainty fastas; `when = config.run_vcf2genome` |
| multiqc | `multiqc` | multiqc 1.16 | `multiqc -f --config assets/multiqc_config.yaml .` (the upstream `--title/--filename` run-name flags are nf-core boilerplate and are dropped). Module files are staged into per-module subdirs mirroring the upstream multiqc process inputs; staging is guarded so skipped modules are simply absent. Report at `results/multiqc/multiqc_report.html` |
| output_documentation | — | — | not ported — nf-core boilerplate docs process (markdown_to_html.py of static run docs); upstream runs it unconditionally, so porting it would change the default plan for zero analytical value |
| get_software_versions | — | — | not ported — nf-core boilerplate versions process (scrapes `$workflow`/`$nextflow` native variables into a versions.yml; a versions.yml has no oxo-flow equivalent, and `scrape_software_versions.py` targets Nextflow env vars) |

Additional deviations from upstream (all on the default path):

- The `publishDir` mechanism has no oxo-flow equivalent: outputs are written
  directly at the `results/...` paths upstream publishes to (see
  `output = [...]` in `main.oxoflow`); `publish_dir_mode`/`saveAs` are
  folded into the shells where they rename files.
- Reference files use the canonical name `reference.fa` (and
  `reference.dict`) in `results/reference_genome/` instead of the input
  fasta basename; all reference-consuming rules point at those copies.
- Upstream labels are baked into per-rule `[rules.resources]`:
  `sc_tiny` 1 cpu/1G/4h, `sc_small` 1/4G, `sc_medium` 1/8G, `mc_small`
  2/4G, `mc_medium` 4/8G, plus the base-process default (1 cpu/7G/24h)
  used by the undefined `mc_tiny` label (eigenstrat_snp_coverage).
  JVM heaps are byte-identical (`-Xmx8192M`, `-Xmx4096M`, `-Xmx4g`,
  `--java-mem-size=4G`).
- Metagenomic-chain deviations (`rules/branches.oxoflow` B32-B37, all off by
  default):
  - upstream's run-level validation (main.nf 115-137) becomes rule gates +
    fail-fast shell guards (oxo-flow has no params-validation stage).
  - `kraken_parse`/`kraken_merge` carry the same `when` as `kraken`
    (upstream no-ops them via empty channels).
  - `decomp_kraken` (`.tar.gz` kraken2 DB unpack) is folded into the
    `kraken` shell — no when-expression can test a filename suffix.
  - the kraken output prefix is normalized to `{sample}.unmapped.fastq`
    in both filter branches (upstream prefixes by the input basename,
    which differs when the complexity filter is on).
  - MALT `.rma6` outputs are undeclared (per-input names, no fixed
    template; `.sai` precedent); only `malt.log` is declared and
    `maltextract` consumes the rma6s via glob with a DAG edge through
    `malt.log`.
  - upstream's single `--database` param is split into `malt_db` and
    `kraken2_db`.
  - each `samtools_filter_<mapper>` variant writes an empty `{sample}.unmapped.fastq.gz`
    placeholder in discard mode (engine output-existence contract; never
    consumed — the metagenomic rules are gated on `bam_unmapped_type == 'fastq'`).
  - the metagenomic chain passes `validate`/`dry-run` but is NOT yet
    live-verified on tx-ubuntu (no MALT/kraken databases on the test
    server at port time; E15+ steps pending).
- A `.gz`-compressed reference FASTA is not supported (upstream's
  `unzip_reference` pigz pre-step is not ported): pass a plain FASTA.
- Upstream's startup parameter validation (e.g. the pileupCaller
  bed/snp exit-1 check, main.nf lines 74-78) has no oxo-flow
  equivalent: the checks live as fail-fast guards at the top of the
  affected rule shells (`genotyping_pileupcaller`), so an invalid
  invocation fails when the rule runs rather than at workflow start.
- Upstream `errorStrategy retry` (signals 143/137/104/134/139/140, max 3)
  and the exit-1 retry on dedup/markduplicates/damageprofiler/qualimap are
  not ported (oxo-flow has no signal-based retry); `preseq`'s
  `errorStrategy 'ignore'` is likewise not ported.
- The conditional `preserve5p`/`mergedonly` AR branches (both off by
  default) are not ported; their config keys are kept with upstream
  defaults.
- `run_pmdtools`, `run_trim_bam`, `run_post_ar_trimming`,
  `run_mapdamage_rescaling`, `run_bedtools_coverage`, `run_vcf2genome`,
  `run_multivcfanalyzer`, `run_sexdeterrmine`, `run_mtnucratio`,
  `run_nuclear_contamination`, `run_endorSpy`, `run_convertinputbam`,
  `run_hostremoval` and the non-default mapper/dedupper/damage-tool/
  genotyping-tool choices are all ported as the gated branch rules above
  (the port's keys are `run_endor_spy`, `bam_input` and
  `hostremoval_input_fastq` where the upstream names `run_endorSpy`,
  `run_convertinputbam` and `hostremoval_input_fastq` differ);
  `run_bam_filtering` (incl. the metagenomic screening chain under
  `run_metagenomic_screening` with `metagenomic_tool` = `kraken`/`malt`) IS
  ported. Default values are kept in `[config]` where a config key exists.

## Links

- Repository: [oxo-flow-eager](https://github.com/oxo-flow-community/oxo-flow-eager)
- Upstream: [nf-core/eager](https://github.com/nf-core/eager) @ `2.5.3`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
