# Bisulfite methylation analysis with Bismark

oxo-flow port of nf-core/methylseq 4.2.0 (default paired-end bismark path): FastQC, TrimGalore with library presets, Bismark (bowtie2) alignment, deduplication, samtools sort/index, per-context methylation extraction with bedGraph and coverage output, bismark2report/bismark2summary HTML reports, and a final MultiQC report. 13 rules, all tool versions pinned to the upstream module environments, upstream process labels baked into rule resources.

| | |
|---:|---|
| **Engine** | nf-core |
| **Source** | [nf-core/methylseq](https://github.com/nf-core/methylseq) |
| **Pinned version** | `4.2.0` |
| **Ported** | 2026-08-15 |
| **Rules** | 13 |
| **Tools** | fastqc · trim-galore · cutadapt · pigz · bismark · samtools · htslib · multiqc |
| **Domain** | genomics |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- bismark_genomepreparation
- fastqc
- trimgalore
- bismark_align
- bismark_deduplicate
- samtools_sort
- samtools_index
- bismark_methylationextractor
- bismark_coverage2cytosine
- bismark_report
- bismark_summary
- multiqc_versions
- multiqc

**Excluded**

- single_end — paired-end only; upstream samplesheet 'single_end' column not ported
- bwameth (bwa-meth) / bwamem / bismark_hisat aligners — non-default branches; aligner config accepts only 'bismark'
- BAM_TAPS_CONVERSION (rastair) — taps/bwamem branch, off by default
- BAM_METHYLDACKEL — bwameth branch, off by default
- QUALIMAP_BAMQC — --run_qualimap branch, off by default
- PRESEQ_LCEXTRAP — --run_preseq branch, off by default
- TARGETED_SEQUENCING (+ PICARD_MARKDUPLICATES / ADDORREPLACEREADGROUPS) — --run_targeted_sequencing branch, off by default
- CAT_FASTQ — only for samples with >1 fastq pair
- GUNZIP / UNTAR — only when a prebuilt --bismark_index is supplied; port always builds the index (upstream default)

## Fidelity

| Upstream process/rule | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| FASTQC | `fastqc` | fastqc 0.12.1 | identical command; `--memory` derived from task resources |
| TRIMGALORE | `trimgalore` | trim-galore 0.6.10, cutadapt 4.9, pigz 2.8 | identical command incl. library-preset clipping and `--cores` clamp |
| BISMARK_GENOMEPREPARATION | `bismark_genomepreparation` | bismark 0.25.1 | `--bowtie2`; runs when no prebuilt index is supplied (upstream default) |
| BISMARK_ALIGN | `bismark_align` | bismark 0.25.1 | identical flag order (pbat/non_directional/unmapped/score_min/local/minins/maxins/multicore) |
| BISMARK_DEDUPLICATE | `bismark_deduplicate` | bismark 0.25.1 | identical command; skipped with `skip_deduplication`/`rrbs` like upstream |
| SAMTOOLS_SORT | `samtools_sort` | samtools 1.22.1, htslib 1.22.1 | upstream prefix `${sample}.deduplicated.sorted` |
| SAMTOOLS_INDEX | `samtools_index` | samtools 1.22.1 | identical command |
| BISMARK_METHYLATIONEXTRACTOR | `bismark_methylationextractor` | bismark 0.25.1 | identical flag order on the **deduplicated** BAM; `--multicore`/`--buffer_size` derived from resources |
| BISMARK_COVERAGE2CYTOSINE | `bismark_coverage2cytosine` | bismark 0.25.1 | off by default; runs with `cytosine_report`/`nomeseq` |
| BISMARK_REPORT | `bismark_report` | bismark 0.25.1 | bismark2report run with the four reports co-located, as in the upstream workdir |
| BISMARK_SUMMARY | `bismark_summary` | bismark 0.25.1 | bismark2summary with upstream BAM-name arguments |
| MULTIQC | `multiqc` | multiqc 1.32 | same search space + `assets/multiqc_config.yml`; versions pinned statically |
| softwareVersionsToYAML + collectFile | `multiqc_versions` | — | upstream extracts versions at runtime; port pins the module versions statically |
| CAT_FASTQ | not ported | — | only active when a sample has >1 fastq pair; single-pair samplesheets cover the default path |
| GUNZIP / UNTAR | not ported | — | only active when a prebuilt `--bismark_index` is supplied; the port always builds the index |
| QUALIMAP_BAMQC | not ported | — | `--run_qualimap` branch, off by default |
| PRESEQ_LCEXTRAP | not ported | — | `--run_preseq` branch, off by default |
| TARGETED_SEQUENCING (+ PICARD_MARKDUPLICATES / ADDORREPLACEREADGROUPS) | not ported | — | `--run_targeted_sequencing` branch, off by default |
| BAM_TAPS_CONVERSION (rastair) | not ported | — | `--taps` / bwamem branch, off by default |
| BAM_METHYLDACKEL | not ported | — | bwameth branch, off by default |
| aligners bismark_hisat / bwameth / bwamem | not ported | — | `aligner` config accepts only `bismark` (the default) |

Additional notes: paired-end only (`single_end` samplesheet column is not
ported); `--save_*` / `publish_dir_mode` params are N/A (oxo-flow publishes
every declared output); per-process `withName:` resource overrides are baked
into `[rules.resources]` (upstream labels process_single/low/medium/high +
BISMARK_ALIGN 8d / DEDUPLICATE 2d / METHYLATIONEXTRACTOR 1d time limits).

## Links

- Repository: [oxo-flow-methylseq](https://github.com/oxo-flow-community/oxo-flow-methylseq)
- Upstream: [nf-core/methylseq](https://github.com/nf-core/methylseq) @ `4.2.0`
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
