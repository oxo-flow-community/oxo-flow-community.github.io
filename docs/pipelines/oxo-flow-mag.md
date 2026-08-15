# Metagenome assembly, binning and taxonomic classification

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Turn paired-end metagenomic reads into quality-checked, taxonomically classified draft genomes: FastQC and fastp QC with phiX removal, SPAdes and MEGAHIT assembly, QUAST and Prodigal assessment, bowtie2 mapping, binning with six binners (MetaBAT2, MaxBin2, CONCOCT, COMEBin, MetaBinner, SemiBin2), BUSCO bin QC, GTDB-Tk classification with a combined summary, PROKKA annotation, ALE evaluation and a final MultiQC report. The default short-read path of nf-core/mag, faithfully ported with the same tool versions and commands.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | metagenomics |
| **Rules** | 134 |
| **Tools** | fastqc · fastp · bowtie2 · samtools · spades · megahit · quast · prodigal · bioawk · seqkit · metabat2 · maxbin2 · concoct · comebin · metabinner · semibin · busco · qsv · ale · gtdbtk · prokka · multiqc · python · pandas · biopython |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/mag](https://github.com/nf-core/mag) |
| **Pinned version** | `5.5.0` |

## Run it

```bash
oxo-flow run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.11.0

**Toolchain.** conda envs — pinned

**Requirements.**
- input: paired-end reads as {sample}_R1.fastq.gz / {sample}_R2.fastq.gz in config.input_dir (default test/fixtures/raw); single-end not ported
- reference: GTDB-Tk database — download gtdbtk_data.tar.gz (~100 GB) or unpacked directory and set config.gtdb_db (oxo-flow cannot download it mid-run)
- reference: phiX genome FASTA bundled in the repo (assets/data/GCA_002596845.1_ASM259684v1_genomic.fna.gz) — no download needed
- compute: up to 12 CPUs / 140 GB RAM per rule (SPAdes 10 CPUs/72 GB/24 h; GTDB-Tk classifywf 2 CPUs/140 GB/12 h; defaults 1 thread/6 GB)
- software: conda or mamba with the pinned envs/*.yaml environments (one per tool, no container layer)
- optional: disk — hundreds of GB for real datasets (GTDB-Tk database plus per-sample assemblies and bins)

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/download/v0.11.0/oxo-flow-v0.11.0-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-mag
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- fastqc_raw
- fastp
- bowtie2_phix_removal
- fastqc_trimmed
- spades
- megahit
- gunzip
- quast
- prodigal
- bowtie2_assembly_build
- bowtie2_assembly_align
- depths
- convert_depths
- metabat2
- maxbin2
- concoct
- comebin
- metabinner
- semibin
- seqkit_stats
- split_fasta
- busco
- concat_busco
- mag_depths
- mag_depths_summary
- quast_bins
- concat_quast
- ale
- gtdbtk_db_preparation
- gtdbtk_classifywf
- gtdbtk_summary
- bin_summary
- prokka
- multiqc

**Excluded**

- longreads — long-read assemblies (Flye/MetaMDBG) and long-read binning, off by default
- refinement — DAS Tool binning refinement, off by default
- kaiju — taxonomic profiling with kaiju, off by default
- diamond — taxonomic profiling with diamond, off by default
- run_checkm / run_checkm2 / run_gunc — additional bin QC tools, off by default (the GTDB-Tk filter therefore uses BUSCO metrics only, which is the default configuration)
- bin_domain_classification (tiara) — off by default; all bins keep domain='unclassified' exactly like the upstream default
- hostremoval — off by default
- assembly_input / bbnorm / adapters trimming variants (adapterremoval, trimmomatic) — non-default preprocessing branches
- ancient_dna / catpack / virus_identification — dedicated subworkflows, off by default
- pydamage, checkm2 and gunc report pages — off by default
- BUSCO `*-busco.batch_summary.failed.txt` artifact — only produced by upstream when a BUSCO run fails
- nf-core boilerplate files (pipeline_summary/methods_description, versions.yml) — not part of the analysis

## Fidelity

| Upstream | Port | Notes |
|----------|------|-------|
| Process-per-(assembler, binner) with `meta` tuples | One rule per (assembler, binner, ...) combination, names hard-coded | oxo-flow has no assembler/binner wildcard; `04_binning` has 48 rules, `05_binqc` 41, `06_taxonomy` 28 |
| Nextflow task workdir per process | Shared workflow dir + per-rule `.tmp/` scratch dirs | Tools that write generic-named files (spades, megahit, busco, quast, prokka, gtdbtk) run inside a scratch subdir and move outputs out |
| bash task scripts | `sh -c` executor | Process substitution (`2> >(tee ...)` in fastp) replaced with a plain redirect; brace expansion (`short_summary.*.{txt,json}`) split into two `mv` commands |
| Two BUSCO/GTDB-Tk/QUAST_BINS/MAG_DEPTHS runs per group (bins + chunks) | One rule per group that runs the tool twice in separate scratch subdirs | The two upstream runs share output names (`S1-auto-busco.*`); they are kept apart by the publish dirs `...-unclassified-unrefined-{sample}/` and `...-unclassified-unrefined_unbinned-{sample}/` |
| GTDB-Tk QC filter (Groovy) | `scripts/filter_bins_by_qc.py` | Same semantics: negative readings dropped, bins without metrics dropped, pass iff any reading clears both thresholds; BUSCO `Duplicated` is the contamination column |
| `gtdbtk_single_job` option | Not ported | Off by default upstream |
| `gtdbtk_use_full_tree` / `gtdbtk_place_species` | Config keys not exposed | Off by default upstream |
| Empty bin groups crash upstream (BUSCO on no input) | Empty groups produce empty/touched outputs and skip downstream classification | The pipeline never fails on empty groups |
| Versions.yml / pipeline boilerplate (summary, methods_description) | Not ported | Not analysis output |
| `*-busco.batch_summary.failed.txt` | Not produced | Only exists upstream when a BUSCO run failed |
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

### Not ported (off by default upstream)

Long-read assembly and binning, DAS Tool refinement, kaiju and diamond taxonomic profiling, CheckM/CheckM2/GUNC QC, tiara domain classification, host removal, ancient DNA, CAT/BAT, pydamage, hybrid assembly, and the benchmarking modes.

## Links

- Repository: [oxo-flow-mag](https://github.com/oxo-flow-community/oxo-flow-mag)
- Upstream: [nf-core/mag](https://github.com/nf-core/mag) @ `5.5.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
