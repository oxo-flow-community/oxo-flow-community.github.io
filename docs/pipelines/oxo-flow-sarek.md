# WGS/WES germline and somatic variant calling

oxo-flow port of nf-core/sarek 3.10.0 default main path: FastQC, fastp trim/split, BWA-MEM alignment, MarkDuplicates, BQSR, HaplotypeCaller, VEP annotation, VCF QC and MultiQC aggregation for WGS/WES germline and somatic variant calling.

| | |
|---:|---|
| **Engine** | nf-core |
| **Source** | [nf-core/sarek](https://github.com/nf-core/sarek) |
| **Pinned version** | `3.10.0` |
| **Ported** | 2026-08-15 |
| **Rules** | 18 |
| **Tools** | fastqc@0.12.1 · fastp@1.1.0 · bwa@0.7.18 · samtools@1.24 · gatk@4.7.1.0 · mosdepth@0.3.8 · bcftools@1.23.1 · vcftools@0.1.17 · ensembl-vep@116.0 · multiqc@1.35 |
| **Domain** | genomics |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastqc
- fastp
- bwa_mem
- gatk_markduplicates
- mosdepth_md
- samtools_stats_md
- gatk_baserecalibrator
- gatk_applybqsr
- samtools_index_recal
- mosdepth_recal
- samtools_stats_recal
- gatk_haplotypecaller
- bcftools_stats
- vcftools_tstv_count
- vcftools_tstv_qual
- vcftools_filter_summary
- ensemblvep_vep
- multiqc

**Excluded**

- deepvariant (--tools alternative, not on default path)
- strelka (--tools alternative, not on default path)
- manta (--tools alternative, not on default path)
- cnvkit (--tools alternative, not on default path)
- ascat (--tools alternative, not on default path)
- mutect2/msisensor/somalier/freebayes/snpeff/vep-somatic etc. (optional --tools callers)
- NGSCheckMate (BAM_NGSCHECKMATE + BCFTOOLS_MPILEUP) — sample-identity QC on default path but outside port scope
- TrimGalore trimming (--trim_fastq_trimgalore alternative; fastp is upstream default)
- bwa-mem2 aligner (upstream default aligner is bwa-mem)
- save_output_as_bam=true BAM branch of MarkDuplicates (CRAM-only port)
- prepare_genome/bed-prep/interval-prep — reference prep, not default execution path
- joint_germline GVCF joint-genotyping subworkflow (default joint_germline=false)
- UMI workflows (SAREK_UMI_*) — not on default path
- fastp split parts beyond 0001. — only first split part wired fastp->BWA (upstream-compatible naming, documented)

## Fidelity

Rows cover every upstream process/rule on the default main execution path.
"not ported" rows carry a reason.

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command |
| FASTP | `fastp` | fastp 1.1.0 | upstream default trimming/fastp module; TrimGalore is the `--trim_fastq_trimgalore` alternative and is not ported |
| BWA_MEM | `bwa_mem` | bwa 0.7.19 | upstream default aligner is `bwa-mem`, not `bwa-mem2`; read-group flags from sarek.nf; prefix `{meta.id}.{reads[0] token}` = `test.0001` under split_fastq; the same image also carries samtools 1.22.1 (used for `samtools sort`) |
| GATK4_MARKDUPLICATES | `gatk_markduplicates` | gatk4 4.6.2.0 | CRAM-only port (`save_output_as_bam=false`); upstream's `if [[ ${prefix} == *.cram ]]` BAM branch not ported — conversion is unconditional |
| MOSDEPTH (post-MD) | `mosdepth_md` | mosdepth 0.3.14 | ext.prefix `{meta.id}.md`; WGS `--by 500` mode |
| SAMTOOLS_STATS (post-MD) | `samtools_stats_md` | samtools 1.24 | ext.prefix `{meta.id}.md.cram`; 1.24 is the version in the `htslib_samtools` stats/index images (the BWA image carries 1.22.1) |
| GATK4_BASERECALIBRATOR | `gatk_baserecalibrator` | gatk4 4.6.2.0 | known-sites = dbsnp + Mills gold standard + known indels (GRCh38); single whole-genome job, no per-interval scatter (see deviations) |
| GATK4_APPLYBQSR | `gatk_applybqsr` | gatk4 4.6.2.0 | output CRAM (not BAM) per default; single whole-genome job, no per-interval scatter (see deviations) |
| SAMTOOLS_INDEX (recal) | `samtools_index_recal` | samtools 1.24 | indexes the recalibrated CRAM |
| MOSDEPTH (recal) | `mosdepth_recal` | mosdepth 0.3.14 | ext.prefix `{meta.id}.recal` |
| SAMTOOLS_STATS (recal) | `samtools_stats_recal` | samtools 1.24 | ext.prefix `{meta.id}.recal.cram` |
| GATK4_HAPLOTYPECALLER | `gatk_haplotypecaller` | gatk4 4.6.2.0 | default `tools=haplotypecaller,vep` → `call_haplotypecaller=true`; single-sample mode (no `-ERC GVCF`), `--pcr-indel-model CONSERVATIVE`; single whole-genome job, no per-interval scatter (see deviations) |
| GATK4_CNNSCOREVARIANTS | `gatk_cnnscorevariants` | gatk4 4.6.2.0 | VCF_VARIANT_FILTERING_GATK part 1; CNN 1D scoring (module default `--tensor-type 1D`); upstream keeps the `{sample}.cnn.vcf.gz` intermediate unpublished — the port stores it under `results/variant_calling/cnnscorevariants/` for DAG handoff |
| GATK4_FILTERVARIANTTRANCHES | `gatk_filtervarianttranches` | gatk4 4.6.2.0 | VCF_VARIANT_FILTERING_GATK part 2; ext.args `--info-key CNN_1D`, ext.prefix `{meta.id}.haplotypecaller`, known sites (dbsnp + 2 GRCh38 indel sets) passed as `--resource`; produces `{sample}.haplotypecaller.filtered.vcf.gz` |
| BCFTOOLS_STATS | `bcftools_stats` | bcftools 1.23.1 | VCF_QC_BCFTOOLS_VCFTOOLS part 1; runs on the filtered VCF (prefix `{meta.id}.haplotypecaller.filtered`) |
| VCFTOOLS_TSTV_COUNT | `vcftools_tstv_count` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 2; runs on the filtered VCF |
| VCFTOOLS_TSTV_QUAL | `vcftools_tstv_qual` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 3; runs on the filtered VCF |
| VCFTOOLS_SUMMARY | `vcftools_filter_summary` | vcftools 0.1.17 | VCF_QC_BCFTOOLS_VCFTOOLS part 4; runs on the filtered VCF |
| ENSEMBLVEP_VEP | `ensemblvep_vep` | ensembl-vep 116.0 | annotates the filtered VCF (`{sample}.haplotypecaller.filtered_VEP.ann.vcf.gz`); requires a VEP cache mounted at `/.vep` in the container (upstream bundles it via `--vep_cache`); `--cache_version 116`, GRCh38 |
| MULTIQC | `multiqc` | multiqc 1.35 | fan-in over all report producers; scans the results dir with the upstream `assets/multiqc_config.yml` |
| NGSCheckMate (BAM_NGSCHECKMATE + BCFTOOLS_MPILEUP) | — not ported | — | sample-identity QC on the CRAM; outside this port's scope (QC fan-in, needs a cohort reference) |
| PREPARE_GENOME (BWA_INDEX, GATK4_CREATESEQUENCEDICTIONARY, SAMTOOLS_FAIDX) | — not ported | — | reference preparation; the port requires a pre-built reference bundle (upstream also accepts pre-built index/dict/fai via `params.bwa`/`dict`/`fasta_fai`, so this is an upstream-compatible shortcut, not a behavior change) |
| BED_PREPARE_INTERVALS (BUILD_INTERVALS, CREATE_INTERVALS_BED, TABIX bgzip/tabix interval split) + per-interval scatter/gather (GATK4_GATHERBQSRREPORTS, CRAM_MERGE_INDEX_SAMTOOLS, GATK4_MERGEVCFS) | — not ported | — | interval preparation and the per-interval scatter/gather of BQSR/ApplyBQSR/HaplotypeCaller; the port runs single whole-genome GATK jobs without `--intervals` (gathers are exact, so results are equivalent, but the per-contig parallelism of the upstream default path is absent) |
| SAREK_UMI_* / Strelka2 / Mutect2 / Manta / DeepVariant / CNVkit / ASCAT / MSIsensor / ... | — not ported | — | UMI workflows, `--tools` alternatives and optional callers; out of scope (default `haplotypecaller,vep` only) |

Deviations (all documented, nothing silently dropped):

- **fastp split parts — supported input cap**: upstream `--split_by_lines`
  produces `0001.`-prefixed outputs; only the first split part (`0001.`) is
  wired to BWA-MEM (the nf-core bwa/mem prefix logic `tokenize('.')[0]` gives
  `{sample}.0001.bam`). The supported input size is therefore capped at one
  split part — ~50M read pairs / 200M lines per sample (the upstream default
  `split_fastq=50,000,000` threshold). Datasets above the threshold are a
  **known unsupported upstream behavior**: upstream aligns every part and
  merges the part BAMs before MarkDuplicates (`BAM_MERGE_INDEX_SAMTOOLS`),
  which this port does not reproduce — **do not run WGS data above ~50M read
  pairs per sample** with this port until the multi-part path is wired.
- **no per-interval scatter/gather**: BQSR, ApplyBQSR and HaplotypeCaller run
  as single whole-genome jobs (no `--intervals`, no
  GATK4_GATHERBQSRREPORTS / CRAM_MERGE_INDEX_SAMTOOLS / GATK4_MERGEVCFS).
  Gathers are exact, so the results are mathematically equivalent to
  upstream's, but wall-time and per-contig parallelism differ substantially.
- **CNN-scored intermediate location**: upstream disables the
  CNNSCOREVARIANTS publishDir (the `{sample}.cnn.vcf.gz` stays in the task
  workdir); oxo-flow hands files between rules through `results/`, so the
  port keeps it under `results/variant_calling/cnnscorevariants/`.
- **markduplicates CRAM branch**: unconditional `samtools view -Ch` +
  `samtools index` replaces upstream's bash conditional; BAM output mode
  (`save_output_as_bam=true`) is not ported.
- **Docker staging**: only the rule workdir is mounted, so reference files are
  copied into the workdir under fixed local names (`reference.fasta`,
  `reference.fasta.fai`, `reference.dict`) — same effect as Nextflow's
  staging of the reference into the task directory.
- **`known_indels`** is a TOML array (2 GRCh38 files); both it and
  `known_indels_tbi` must be updated together when changing references.

## Links

- Repository: [oxo-flow-sarek](https://github.com/oxo-flow-community/oxo-flow-sarek)
- Upstream: [nf-core/sarek](https://github.com/nf-core/sarek) @ `3.10.0`
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
