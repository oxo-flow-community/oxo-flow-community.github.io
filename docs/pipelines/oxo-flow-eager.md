# Ancient DNA (aDNA): QC, mapping, damage estimation and genotyping

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--nf"><span class="dot"></span>nf-core port</span></div>

Ancient DNA (aDNA) analysis in one run: FastQC raw QC, optional fastp poly-G filtering (2-colour chemistry), AdapterRemoval adapter clipping and paired-end read merging, BWA aln mapping with ancient-DNA parameters, picard MarkDuplicates (or DeDup) deduplication, preseq library-complexity curves, DamageProfiler damage estimation, Qualimap BAM QC, optional pileupCaller genotyping with eigenstrat SNP coverage, and a final MultiQC report — every rule pinned to the nf-core/eager 2.5.3 tool versions in the upstream container.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 17 |
| **Tools** | fastqc · adapterremoval · adapterremovalfixprefix · bwa · samtools · picard · dedup · preseq · damageprofiler · qualimap · sequencetools · eigenstratdatabasetools · fastp · pigz · multiqc · rename · python |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [nf-core/eager](https://github.com/nf-core/eager) |
| **Pinned version** | `2.5.3` |

## Run it

```bash
oxo-flow dry-run main.oxoflow
```

## Installation

**Engine.** oxo-flow >= 0.11.0

**Toolchain.** containers (Docker/Singularity) — pinned image nfcore/eager:2.5.3 for all rules (bundles the pinned conda env from envs/eager.yaml)

**Requirements.**
- reference genome FASTA, plain and uncompressed (.gz references are not supported — upstream's unzip_reference step is not ported); the workflow builds the .fai / .dict / BWA indices itself
- paired-end FASTQ pairs named <sample>_R1.fastq.gz / <sample>_R2.fastq.gz in a directory (directory input mode; sample = text before the _R1/_R2 suffix); single-end is not supported
- optional — pileupCaller genotyping (run_genotyping=true genotyping_tool='pileupcaller') requires pileupcaller_snpfile and pileupcaller_bedfile; the rule fails fast without them
- compute: up to 4 CPUs / 8 GB RAM per rule (bwa_aln: 4 threads / 8G; reference-index and MultiQC rules up to 8 GB; base default 1 CPU / 7 GB / 24 h)
- Docker or Singularity to run the pinned container nfcore/eager:2.5.3 (not needed for validate / lint / dry-run)
- disk: results/ holds reference indices, mapped BAMs and reports — size grows with the reference genome and number of samples

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/download/v0.11.0/oxo-flow-v0.11.0-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-eager
```

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

**Excluded**

- unzip_reference: conditional .gz-fasta decompression process (main.nf line 187) — the port requires a plain FASTA (a .gz reference is silently unsupported)
- bwamem / bowtie2: non-default mappers (params.mapper) — default path uses bwa aln
- makeBT2Index: bowtie2 mapper's conditional index process (main.nf line 523) — unreachable with the default bwaaln mapper
- circulargenerator / circularmapper: circular mapping branch (params.circularfilter, off by default)
- convertBam / indexinputbam: BAM-input mode preprocessing (params.bam, off by default)
- hostremoval_input_fastq: host removal branch (params.hostremoval_input_fastq, off by default)
- samtools_filter / samtools_flagstat_after_filter: BAM filtering branch (params.run_bam_filtering, off by default)
- picard_addorreplacereadgroups: read-group replacement branch (off by default)
- bedtools: coverage branch (params.run_bedtools_coverage, off by default)
- mapdamage_calculation / mapdamage_rescaling / mask_reference_for_pmdtools / pmdtools: mapDamage and pmdtools branches (damage_calculation_tool='damageprofiler' default; run_mapdamage_rescaling / run_pmdtools off by default)
- bam_trim: trimbam branch (params.run_trim_bam, off by default)
- post_ar_fastq_trimming: post-AdapterRemoval trimming branch (params.run_post_ar_trimming, off by default)
- lanemerge / lanemerge_hostremoval_fastq: multi-lane merging — unreachable in the single-lane default path
- library_merge / additional_library_merge: multi-library merging — unreachable in the single-library default path
- seqtype_merge: PE/SE mixed-input merge (main.nf line 1597) — unreachable in the pure-PE port
- genotyping_ug / genotyping_hc / genotyping_freebayes: non-pileupcaller genotyping tools (genotyping_tool default null; genotyping off by default)
- genotyping_angsd: ANGSD genotyping branch (genotyping_tool='angsd')
- bcftools_stats: only consumes UG/HC/FB outputs, which are not ported
- malt / maltextract / metagenomic_complexity_filter / kraken / kraken_parse / kraken_merge / decomp_kraken: metagenomic screening branch (params.run_metagenomic_screening, off by default; decomp_kraken is the conditional .tar.gz DB unpacker)
- sexdeterrmine / sexdeterrmine_prep: sex determination branch (params.run_sexdeterrmine, off by default)
- mtnucratio: mitochondrial-to-nuclear ratio branch (params.run_mtnucratio, off by default)
- endorSpy: endogenous-content branch (params.run_endorSpy, off by default)
- nuclear_contamination / print_nuclear_contamination: nuclear contamination branch (params.run_nuclear_contamination, off by default; nuclear_contamination is the angsd estimation process, print_nuclear_contamination the report-only consumer)
- multivcfanalyzer: branch gated by params.run_multivcfanalyzer (off by default)
- vcf2genome: consensus-sequence branch (params.run_vcf2genome, off by default)
- output_documentation / get_software_versions: nf-core boilerplate processes

## Fidelity

Every upstream process of nf-core/eager 2.5.3 (63 total: 56 top-level
processes plus 7 conditional/indented ones — `makeBWAIndex`,
`makeBT2Index`, `unzip_reference`, `seqtype_merge`, `mtnucratio`,
`nuclear_contamination`, `decomp_kraken`) is listed below.
The 17 processes on the default-parameters main path (directory input,
paired-end, `mapper=bwaaln`, `dedupper=markduplicates`) are ported
byte-faithfully; everything else is `not ported` with a reason.

| Upstream process | oxo-flow rule | Tool (version) | Notes |
|---|---|---|---|
| unzip_reference | — | pigz 2.6 | not ported — upstream's conditional process (main.nf line 187) decompresses a `.gz` reference FASTA with `pigz -d` before indexing. **A `.gz`-compressed FASTA is therefore NOT supported: pass a plain FASTA** (the port's index rules would run samtools/bwa on the gzipped file and fail) |
| makeFastaIndex | `make_fasta_index` | samtools 1.12 | `samtools faidx` verbatim. Port copies the input to `results/reference_genome/fasta_index/reference.fa` (canonical name; upstream publishes `<fasta-base>.fai` only when `--save_reference`) |
| makeSeqDict | `make_seq_dict` | picard 2.26.0 | `picard -Xmx8192M CreateSequenceDictionary` verbatim; output named `reference.dict` (upstream `<fasta-base>.dict`) |
| makeBWAIndex | `make_bwa_index` | bwa 0.7.17 | `cp` into `BWAIndex/` + `bwa index` verbatim; canonical file name `reference.fa` |
| fastqc | `fastqc` | fastqc 0.11.9 | `fastqc -t N -q r1 r2` + rename `*_fastqc.zip` → `*_raw_fastqc.zip` verbatim (per-instance scoped rename; zips moved to `zips/` like the upstream publishDir saveAs) |
| fastp | `fastp` | fastp 0.20.1 | Off by default, same as upstream (`complexity_filter_poly_g=false`). PE branch flags verbatim. **Upstream feeds fastp only the 2-colour-chemistry branch** (`ch_input_for_fastp.twocol`, main.nf lines 723-746): with the default `colour_chemistry=4` fastp runs on zero samples even when the flag is on. The port mirrors this gate (`when = complexity_filter_poly_g && colour_chemistry == 2`); use `colour_chemistry=2` to actually filter poly-G |
| adapter_removal | `adapter_removal` | adapterremoval 2.3.2, adapterremovalfixprefix 0.0.5, pigz 2.6 | Default PE collapse branch verbatim: `--collapse --trimns --trimqualities`, cat of the 5 gz parts (`<base>.pe.collapsed.gz` etc. — the `.pe` basename AR writes, as upstream), `AdapterRemovalFixPrefix \| pigz -p <cpus-1>`. The `cat` operands are explicit per-sample names (shared results dir; upstream globs the workdir). When fastp is enabled the input switches to the fastp outputs (upstream channel mix); the AR basename stays the default-path one (`{r1.baseName}_L0` with the `_R1` suffix as upstream derives it) |
| fastqc_after_clipping | `fastqc_after_clipping` | fastqc 0.11.9 | Verbatim; zips to `zips/` |
| bwa | `bwa_aln` | bwa 0.7.17, samtools 1.12 | Verbatim PE branch: `bwa aln -n/-l/-k/-o` (Oliva 2021 defaults), `bwa samse` with the eager `@RG` string, `samtools sort -@ <cpus-1>`, `samtools index`. `.sai` written into the mapping dir (upstream workdir-local) |
| bwamem | — | bwa 0.7.17 | not ported — non-default mapper (`--mapper bwamem`) |
| bowtie2 | — | bowtie2 2.4.4 | not ported — non-default mapper (`--mapper bowtie2`) |
| makeBT2Index | — | bowtie2 2.4.4 | not ported — bowtie2 mapper's conditional index process (main.nf line 523), only reachable with `--mapper bowtie2` |
| circulargenerator | — | circularmapper 1.93.5 | not ported — circular-mapping branch (gated by `params.circularfilter`) |
| circularmapper | — | circularmapper 1.93.5 | not ported — circular-mapping branch (gated by `params.circularfilter`) |
| convertBam | — | samtools 1.12 | not ported — BAM-input mode (`--bam`) preprocessing |
| indexinputbam | — | samtools 1.12 | not ported — BAM-input mode |
| hostremoval_input_fastq | — | — | not ported — host-removal branch (gated by `params.hostremoval_input_fastq`) |
| samtools_flagstat | `samtools_flagstat` | samtools 1.12 | Verbatim: `samtools flagstat > {libraryid}_flagstat.stats` |
| samtools_filter | — | samtools 1.12 | not ported — BAM filtering branch (gated by `params.run_bam_filtering`) |
| samtools_flagstat_after_filter | — | samtools 1.12 | not ported — downstream of samtools_filter |
| picard_addorreplacereadgroups | — | picard 2.26.0 | not ported — read-group replacement branch (off by default) |
| markduplicates | `markduplicates` | picard 2.26.0, samtools 1.12 | Default dedupper. picard MarkDuplicates verbatim (`-Xmx4096M`, `REMOVE_DUPLICATES=TRUE AS=TRUE`, `VALIDATION_STRINGENCY=SILENT`) + `samtools index`. INPUT points at the mapped BAM directly instead of upstream's workdir-local `mv {bam} {libraryid}.bam` rename (the shared results dir must keep the mapped BAM for preseq/flagstat) |
| dedup | `dedup` | dedup 0.12.8, samtools 1.12 | Alternative dedupper (off by default, `dedupper='dedup'`). Verbatim: `dedup -Xmx4g -i ... -o . -u`, `mv *.log dedup.log`, in-place `samtools sort`, index. Upstream's `mv {bam} {libraryid}.bam` becomes a `cp` (shared-results-dir equivalent, same effect) |
| preseq | `preseq` | preseq 3.1.2 | Verbatim default branch: `preseq c_curve -s 1000 -o <base>.preseq -B <mapped bam>`. The `-H` (dedup mode) and `lc_extrap` branches are the alternate `preseq_mode`/`dedupper` combinations |
| bedtools | — | bedtools 2.30.0 | not ported — coverage branch (gated by `params.run_bedtools_coverage`) |
| damageprofiler | `damageprofiler` | damageprofiler 0.4.9 | Verbatim: `-Xmx4g -i <rmdup bam> -r <fasta> -l 100 -t 15 -o . -yaxis_damageplot 0.30`; output lands in `results/damageprofiler/<bam-basename>/` as upstream |
| mapdamage_calculation | — | mapdamage2 2.2.1 | not ported — `damage_calculation_tool='mapdamage'` alternative |
| mapdamage_rescaling | — | mapdamage2 2.2.1 | not ported — rescaling branch (gated by `params.run_mapdamage_rescaling`) |
| mask_reference_for_pmdtools | — | bedtools 2.30.0 | not ported — pmdtools branch (gated by `params.run_pmdtools`) |
| pmdtools | — | pmdtools 0.60 | not ported — pmdtools branch (gated by `params.run_pmdtools`) |
| bam_trim | — | bamutil 1.0.15 | not ported — trimbam branch (gated by `params.run_trim_bam`) |
| post_ar_fastq_trimming | — | fastp 0.20.1 | not ported — post-AR trimming branch (gated by `params.run_post_ar_trimming`) |
| lanemerge | — | — | not ported — multi-lane merging; unreachable in the single-lane default path |
| lanemerge_hostremoval_fastq | — | — | not ported — multi-lane + host removal combination |
| library_merge | — | — | not ported — multi-library merging; unreachable in the single-library default path |
| additional_library_merge | — | — | not ported — multi-library merging |
| seqtype_merge | — | samtools 1.12 | not ported — PE/SE mixed-input merge (main.nf line 1597); unreachable in the pure-PE port |
| qualimap | `qualimap` | qualimap 2.2.2d | Default path, ported: `qualimap bamqc -bam <rmdup bam> -nt 2 -outdir . -outformat "HTML" --java-mem-size=4G` verbatim; output lands in `results/qualimap/<bam-base>_bamqc/` as upstream |
| genotyping_pileupcaller | `genotyping_pileupcaller` | samtools 1.12, sequencetools 1.5.2 | Off by default, same as upstream (`run_genotyping=false`). Verbatim: `samtools mpileup -B --ignore-RG -q 30 -Q 30 [-l <bed>] -f <fasta> <bams> \| pileupCaller --randomHaploid --sampleNames <csv> [-f <snp>] -e pileupcaller.double` (single-instance fan-in; `-e` prefix `pileupcaller.double` = PE strandedness). `-l`/`-f` render only when `pileupcaller_bedfile`/`pileupcaller_snpfile` are set, exactly as upstream's dummy-file check (main.nf lines 2608-2609); without them the rule fails fast with upstream's error message — upstream exits 1 at workflow start (main.nf lines 74-78), the port's guard lives in the rule shell because oxo-flow has no params-validation stage |
| genotyping_ug | — | gatk 3.5 | not ported — UnifiedGenotyper branch (`genotyping_tool='unifiedgenotyper'`) |
| genotyping_hc | — | gatk4 4.2.0.0 | not ported — HaplotypeCaller branch (`genotyping_tool='haplotypecaller'`) |
| genotyping_freebayes | — | freebayes 1.3.5 | not ported — FreeBayes branch (`genotyping_tool='freebayes'`) |
| genotyping_angsd | — | angsd 0.935 | not ported — ANGSD branch (`genotyping_tool='angsd'`) |
| bcftools_stats | — | bcftools 1.12 | not ported — only consumes UG/HC/FB outputs, which are not ported |
| eigenstrat_snp_coverage | `eigenstrat_snp_coverage` | eigenstratdatabasetools 1.0.2, python 3.9.4 | Off by default, same as upstream. Verbatim: `eigenstrat_snp_coverage -i pileupcaller.double >double_eigenstrat_coverage.txt` + `parse_snp_cov.py` (bundled upstream script, called via `python3 scripts/parse_snp_cov.py` — oxo-flow does not auto-add `bin/` to PATH) |
| malt | — | malt 0.61 | not ported — metagenomic screening branch (gated by `params.run_metagenomic_screening`) |
| maltextract | — | malt 0.61 | not ported — metagenomic screening branch |
| metagenomic_complexity_filter | — | fastp 0.20.1 | not ported — metagenomic screening branch |
| kraken | — | kraken2 2.1.2 | not ported — metagenomic screening branch |
| kraken_parse | — | kraken2 2.1.2 | not ported — metagenomic screening branch |
| kraken_merge | — | kraken2 2.1.2 | not ported — metagenomic screening branch |
| decomp_kraken | — | kraken2 2.1.2 | not ported — conditional process (main.nf line 3080) that unpacks a `.tar.gz` kraken DB; only reachable with `--run_metagenomic_screening --metagenomic_tool kraken` on a `.tar.gz` database |
| sexdeterrmine | — | sexdeterrmine 1.1.2 | not ported — sex determination branch (gated by `params.run_sexdeterrmine`) |
| sexdeterrmine_prep | — | — | not ported — sex determination branch |
| mtnucratio | — | samtools 1.12, sequencetools 1.5.2 | not ported — mitochondrial-to-nuclear ratio branch (gated by `params.run_mtnucratio`, main.nf line 2812) |
| nuclear_contamination | — | angsd 0.935 | not ported — nuclear contamination estimation branch (gated by `params.run_nuclear_contamination`, main.nf line 2881; consumes a BAM, unlike the report-only `print_nuclear_contamination` below) |
| endorSpy | — | endorSpy | not ported — endogenous-content branch (gated by `params.run_endorSpy`) |
| print_nuclear_contamination | — | python 3.9.4 | not ported — nuclear contamination report branch (gated by `params.run_nuclear_contamination`) |
| multivcfanalyzer | — | multivcfanalyzer 0.85.2 | not ported — branch (gated by `params.run_multivcfanalyzer`) |
| vcf2genome | — | vcf2genome 0.91 | not ported — consensus-sequence branch (gated by `params.run_vcf2genome`) |
| multiqc | `multiqc` | multiqc 1.16 | `multiqc -f --config assets/multiqc_config.yaml .` (the upstream `--title/--filename` run-name flags are nf-core boilerplate and are dropped). Module files are staged into per-module subdirs mirroring the upstream multiqc process inputs; staging is guarded so skipped modules are simply absent. Report at `results/multiqc/multiqc_report.html` |
| output_documentation | — | — | not ported — nf-core boilerplate docs process |
| get_software_versions | — | — | not ported — nf-core boilerplate versions process |

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
- `run_pmdtools`, `run_bam_filtering`, `run_trim_bam`,
  `run_post_ar_trimming`, `run_mapdamage_rescaling`, `run_bedtools_coverage`,
  `run_vcf2genome`, `run_multivcfanalyzer`, `run_sexdeterrmine`,
  `run_mtnucratio`, `run_nuclear_contamination`, `run_endorSpy`,
  `run_metagenomic_screening`, `run_convertinputbam`, `run_hostremoval` and
  the non-default mapper/dedupper/damage-tool/genotyping-tool choices are
  all listed above as `not ported` branches; default values are kept in
  `[config]` where a config key exists.

## Links

- Repository: [oxo-flow-eager](https://github.com/oxo-flow-community/oxo-flow-eager)
- Upstream: [nf-core/eager](https://github.com/nf-core/eager) @ `2.5.3`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
