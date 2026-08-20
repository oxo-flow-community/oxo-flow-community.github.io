# Variant calling for non-model organisms: trimming, alignment and per-sample gVCFs

<div class="ox-page-badges"><span class="ox-badge ox-badge--live">✔ Live-tested · default-path</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

Variant calling for non-model organisms: paired FASTQ reads are trimmed and filtered with fastp, aligned with BWA-MEM, and called to per-sample gVCFs with GATK HaplotypeCaller (low-coverage defaults: -ploidy 2, --min-pruning 1), alongside a cohort QC metrics report aggregating fastp and samtools stats.

| | |
|---:|---|
| **Rating** | ✔ Live-tested |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 12 |
| **Compute** | up to 8 CPUs / 8 GB per rule (bwa_mem) |
| **Tools** | fastp · bwa · samtools · gatk4 · python |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [harvardinformatics/snparcher](https://github.com/harvardinformatics/snparcher) |
| **Pinned version** | `v2.2` |

## Run it

```bash
oxo-flow run main.oxoflow reference_source=/path/to/genome.fa.gz
```

Set your reference genome as shown; preview with `oxo-flow dry-run main.oxoflow`.

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned versions (fastp 1.3.6, bwa 0.7.19, samtools 1.24, gatk4 4.6.2.0; conda-forge + bioconda)

**Requirements.**
- reference genome FASTA (plain or gzip), passed as reference_source at run time — bgzip-compressed and indexed by the workflow itself (no pre-built indices)
- paired-end reads at raw/<sample>_1.fastq.gz and raw/<sample>_2.fastq.gz for each sample in the [[sample_groups]] list
- compute: up to 8 CPUs / 8 GB per rule (bwa_mem 8 threads, fastp 4, gatk_haplotypecaller 7 GB Java heap)
- conda or mamba at runtime to create the pinned envs/*.yaml environments

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
oxo-flow pull gh:oxo-flow-community/oxo-flow-snparcher
#    (alternative: plain git clone)
#    git clone https://github.com/oxo-flow-community/oxo-flow-snparcher
```

## Parameters

| Parameter | Default | Description | Used by |
|---:|---|---|---|
| `expected_coverage` | `low` | — | — |
| `intervals_enabled` | `false` | — | — |
| `mark_duplicates` | `false` | — | — |
| `ploidy` | `2` | — | `gatk_haplotypecaller` |
| `reference_name` | `my_organism` | — | `bwa_mem`, `gatk_haplotypecaller`, `index_reference`, `prepare_reference` |
| `reference_source` | `test/fixtures/ref/genome.fa` | — | `prepare_reference` |

Descriptions are the workflow's own `#` comments from its `[config]` section, surfaced by `oxo-flow info` — no schema file to maintain.

## Workflow graph

<div class="ox-dag-card" markdown="1">

![oxo-flow-snparcher rule-level DAG](/assets/dag/oxo-flow-snparcher.svg)

</div>

The graph is derived at catalog-build time from `oxo-flow graph -f dot` and rendered with Graphviz. It shows the workflow at rule level: wildcard `{sample}` instances expand at run time when sample data is discovered (the runtime view is `oxo-flow graph --expanded`).

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- prepare_reference
- index_reference
- fastp
- bwa_mem
- merge_library_bams
- merge_library_level_bams
- index_bam_csi
- gatk_haplotypecaller
- collect_fastp_stats
- bam_stats
- parse_bam_stats
- combine_qc_metrics

**Excluded**

- markdup (sambamba markdup + merge_dedup_libraries) — committee exclusion; port default mark_duplicates=false
- joint_genotyping (GenomicsDBImport/GenotypeGVCFs + interval scatter machinery) — committee exclusion
- denovo — no such step in upstream v2.2 (v2 redesign)
- structural_variants — no such step in upstream v2.2
- variant_filtration — requires the excluded joint-genotyping raw VCF
- download_sra — srr input type out of scope
- stage_external_bam — bam input type out of scope
- callable_sites (mosdepth/clam/genmap/bedtools chain) — out of scope
- non-gatk callers (bcftools/deepvariant/glnexus/parabricks/sentieon rules) — config-selected only
- modules qc and postprocess — disabled by default upstream

## Fidelity

Port scope: the default-parameters main execution path (FASTQ inputs,
`variant_calling.tool = gatk`), with the committee-approved exclusions
`markdup`, `joint_genotyping`, `denovo`, and `structural_variants` (the
latter two do not exist as steps in upstream v2.2). Intermediate machinery
that only serves excluded branches (interval scatter, GenomicsDB,
callable-sites, SRA downloads, optional modules, non-GATK callers) is listed
as "not ported" below.

| Upstream rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| `prepare_reference` (local branch) | `prepare_reference` | samtools 1.24 (bgzip) | identical command; url/accession branches not ported (config `reference_source` is a local path) |
| `index_reference` | `index_reference` | samtools 1.24, bwa 0.7.19 | identical command (faidx + dict + bwa index) |
| `fastp` | `fastp` | fastp 1.3.6 | identical flags; per (sample, library, input_unit) fan-out modeled as `{sample}/{sample}/u1` — the upstream default for single-row-per-sample sheets with empty `library_id` |
| `bwa_mem` | `bwa_mem` | bwa 0.7.19, samtools 1.24 | identical command incl. read group `ID:{sample}.u1 SM:{sample} LB:{sample} PL:ILLUMINA`; raw BAM is temp like upstream |
| `merge_library_bams` | `merge_library_bams` | samtools 1.24 | per-library merge, single input unit in the default path |
| `merge_library_level_bams` | `merge_library_level_bams` | samtools 1.24 | no-markdup path (`results/bams/merged/{sample}.bam`); used because markdup is excluded |
| `markdup_library` / `merge_dedup_libraries` | not ported | sambamba 1.0.1 | committee exclusion `markdup`; port default `mark_duplicates = false` (upstream default true) |
| `index_bam_csi` | `index_bam_csi` | samtools 1.24 | identical (`samtools index -c`) |
| `gatk_haplotypecaller` (standard mode) | `gatk_haplotypecaller` | gatk4 4.6.2.0 | identical flags incl. `-ploidy 2 --emit-ref-confidence GVCF --min-pruning 1 --min-dangling-branch-length 1` (low-coverage defaults); `-Xmx7000m` = upstream default profile `mem_mb_reduced`; threads 1 as upstream |
| `collect_fastp_stats` | `collect_fastp_stats` | python (script) | identical logic, ported as `scripts/collect_fastp_stats.py` |
| `bam_stats` | `bam_stats` | samtools 1.24 | identical (coverage + flagstat -O tsv); outputs temp like upstream |
| `parse_bam_stats` | `parse_bam_stats` | python (script) | identical logic, ported as `scripts/parse_bam_stats.py` |
| `combine_qc_metrics` | `combine_qc_metrics` | python (script) | identical report format; gather via `expand_inputs` |
| `download_sra` | not ported | sra-tools | SRA (`srr`) inputs out of scope; port default path uses local FASTQ inputs |
| `stage_external_bam` | not ported | — | BAM input type out of scope |
| interval machinery (`picard_intervals`, `create_gvcf_intervals`, `create_db_intervals`, `gatk_haplotypecaller_interval`, `concat_interval_gvcfs*`, `concat_interval_vcfs*`, `compress_interval_raw_vcf`, `normalize_external_gvcf_for_gatk`, `archive_gatk_gvcf`) | not ported | — | upstream default `intervals.enabled: true`; excluded per committee scope (interval scatter serves joint genotyping). Port default `intervals_enabled = false` |
| joint genotyping (`joint_genomics_db_import`, `joint_genotype_gvcfs`, `create_db_mapfile`, `gatk_genomics_db_import`, `gatk_genotype_gvcfs`) | not ported | — | committee exclusion `joint_genotyping`; per-sample gVCF is the port's final call-set output |
| `variant_filtration` (hard filters) | not ported | gatk4, bcftools | downstream of the excluded joint-genotyping raw VCF; cannot run faithfully without it |
| callable sites (`mosdepth`, `clam_collect`, `callable_coverage_thresholds`, `clam_loci`, `coverage_bed`, `genmap_index`, `genmap_mappability`, `mappability_bed`, `callable_sites_bed`) | not ported | mosdepth, clam, genmap, bedtools | coverage/mappability BED branch out of scope (not in the ~9-rule committee scope) |
| `bcftools_call` / `deepvariant_call` / `glnexus_joint` / parabricks / sentieon rules | not ported | — | non-GATK callers, selected by config only |
| postprocess module rules (`basic_filter`, `strict_filter`, `drop_indel_SNPs`, `subset_snps`, `subset_indels`, `contig_map`, `update_bed`, …) | not ported | — | `modules.postprocess.enabled: false` by default upstream |
| qc module rules (`plink`, `admixture`, `subsample_snps`, `filter_individuals`, `vcftools_individuals`, `prepare_plink_inputs`, `setup_admixture`, `generate_coords_file`, `copy_qc_report`, `qc_dashboard`, `denovo`-style dashboard inputs) | not ported | — | `modules.qc.enabled: false` by default upstream |
| `setup` / `download_reads` / `map_samples` / `call_variants` / `qc_report` / `callable_sites` / `gvcfs` (Snakefile aggregation targets) | n/a | — | Snakemake target rules, no commands of their own |

Version pinning: upstream envs declare only `>=` ranges with no lockfile;
exact pins (fastp 1.3.6, samtools 1.24, bwa 0.7.19, gatk4 4.6.2.0, picard
3.5.0, bcftools 1.24) were resolved from bioconda/conda-forge at port time
(2026-08-15). Upstream default-profile thread overrides (fastp 6, bwa_mem
16) are runtime knobs; the port keeps the rules' own declarations (4 and 8).

## Links

- Repository: [oxo-flow-snparcher](https://github.com/oxo-flow-community/oxo-flow-snparcher)
- Upstream: [harvardinformatics/snparcher](https://github.com/harvardinformatics/snparcher) @ `v2.2`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
