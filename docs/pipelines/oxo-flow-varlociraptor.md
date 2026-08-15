# Small and structural variant calling with Varlociraptor

<div class="ox-page-badges"><span class="ox-badge ox-badge--star">★ Verified</span> <span class="ox-badge ox-badge--origin">⇄ Official port</span> <span class="ox-badge ox-badge--sn"><span class="dot"></span>snakemake port</span></div>

Scenario-driven somatic small and structural variant calling with Varlociraptor: paired-end reads are aligned against the 1000 Genomes human pangenome with vg giraffe, QC'd with FastQC/MultiQC, covered with mosdepth, and used for freebayes and delly candidate calling; Varlociraptor then estimates alignment properties and calls variants under a tumor scenario (events present + somatic_tumor_high + somatic_tumor_medium, FDR 0.05), FDR is controlled per variant type (SNV/INS/DEL/MNV/BND/INV/DUP/REP) with merge and phred decoding, and the calls are annotated with VEP (LoFtool/REVEL plugins) and dbSNFP/dbSNP, filtered, turned into a 34-column variant table with oncoprint label-sorting, and rendered as interactive datavzrd variant and gene-coverage reports. All reference data (GRCh38 FASTA and GTF, VEP cache/plugins, REVEL scores, known-variants VCFs, HPRC pangenome graph) is downloaded automatically into resources/.

| | |
|---:|---|
| **Rating** | ★ Verified |
| **Origin** | port |
| **Domain** | genomics |
| **Rules** | 88 |
| **Tools** | altair · bcftools · bedtools · biopython · curl · datavzrd · delly · ensembl-vep · fastqc · freebayes · gatk4 · gawk · htslib · mosdepth · multiqc · openpyxl · pandas · parallel · picard · pysam · python · rust-bio-tools · samtools · scikit-learn · sed · snpsift · statsmodels · unzip · varlociraptor · vcflib · vega-lite-cli · vembrane · vg |
| **Ported** | 2026-08-15 |
| **License** | Apache-2.0 |
| **Source** | [snakemake-workflows/dna-seq-varlociraptor](https://github.com/snakemake-workflows/dna-seq-varlociraptor) |
| **Pinned version** | `v6.10.0` |

## Run it

```bash
oxo-flow run workflow/varlociraptor.toml
```

## Installation

**Engine.** oxo-flow >= 0.12.0

**Toolchain.** conda envs — pinned versions (no containers)

**Requirements.**
- paired-end FASTQ reads at reads_dir/<sample>_1.fastq.gz / _2.fastq.gz; sample cohort declared in [[sample_groups]] (one group = one tumor sample); fixtures bundled for dry-run
- reference data: downloaded automatically into resources/ — GRCh38 primary assembly FASTA (Ensembl release 111) + .fai/.dict, Ensembl release 111 GTF, VEP cache and plugins (release 111), REVEL scores, Ensembl known-variants VCFs, HPRC v1.1 human pangenome graph
- compute: up to 96 CPUs / 32 GB per rule (freebayes candidates 96 threads; vg giraffe 64 threads; samtools sort 16 threads/32G; Varlociraptor call 8G)
- tools: conda envs with pinned versions (envs/*.yaml, one env per tool pin set); conda/mamba required at runtime
- disk: multi-GB reference downloads under resources/ (pangenome graph, VEP cache, known-variants VCFs) plus results/ for BAMs, BCFs, tables and reports

```bash
# 1. install oxo-flow (release binary, recommended)
curl -fL -o oxo-flow.tar.gz https://github.com/Traitome/oxo-flow/releases/latest/download/oxo-flow-latest-x86_64-unknown-linux-gnu.tar.gz
tar xzf oxo-flow.tar.gz && sudo mv oxo-flow /usr/local/bin/
#    or, via conda (may lag behind releases):
#    conda install -c bioconda oxo-flow-cli

# 2. get this workflow
git clone https://github.com/oxo-flow-community/oxo-flow-varlociraptor
```

## Scope

The default-parameters main path of the source pipeline was ported rule-for-rule; alternate paths are documented as excluded.

**In scope**

- pangenome_index
- vg_giraffe_map
- samtools_sort_index
- markduplicates
- baserecalibrator
- applybqsr
- fastqc
- multiqc
- mosdepth_coverage
- covered_regions
- expanded_regions
- delly_excluded_regions
- freebayes_candidates
- delly_candidates
- varlociraptor_estimate
- varlociraptor_call
- fdr_control
- merge_calls
- decode_phred
- vep_annotation
- dbnsfp_annotation
- annotation_filtering
- vembrane_table
- oncoprint_prepare
- datavzrd_report
- coverage_table

**Excluded**

- bwa mapping — non-default aligner branch, not ported
- fastp/trimming — non-default trimming branch, not ported
- fusions (arriba) — fusion calling is off in the default config (calling mode variants)
- MAF conversion — not reachable with the default config
- mutational burden and mutational signature analyses — non-default branches
- population database (germline AF annotation) — population db is off in the default config
- dgidb druggability annotation — off by default
- CADD annotation — off by default
- primer design — off by default
- benchmarking — upstream benchmarking rules are not ported
- consensus reads — non-default branch
- target regions — not part of the default path
- template oncoprint views (gene_oncoprint / variant_oncoprints datasets) — empty with the default single group; prepare_oncoprint itself runs
- gather_annotated_calls / filter_odds — not reachable in the default path (benchmarking off, filter present only)
- upstream scatter.calling(16) chunks beyond scatteritem=0 — collapsed to a single chunk

## Fidelity

The port aims for byte-identical commands on the default path. Known,
deliberate deviations:

| upstream | port | reason |
|---|---|---|
| `scatter.calling(16)` (rules run 16x, once per scatter item) | single chunk, `scatteritem=0` | oxo-flow has no scatter construct; with one small sample the 16 chunks are identical work |
| rule outputs that are directories (VEP cache/plugins, oncoprint `label_sortings/`/`variant-oncoprints/` dirs) | directory + `.completed` marker file output | oxo-flow targets files, not directories |
| scenario rendered at run time from `config/scenario.yaml` (yte template) | pre-rendered `resources/scenarios/SRR702070_group.yaml` for the default sample group; the template is kept verbatim at `config/scenario.yaml` | one scenario (purity 1.0) in the default path |
| `download_vep_plugins.py` with a hard-coded Ensembl variation FTP list and fallback | the `--release`/`--output`/`--log` argv variant of the same wrapper port | one release (111), one output dir; the FTP fallback list was dropped as dead code in the default path |
| wrapper-utils based rules (calls, tables, report) | plain `python scripts/*.py` argv ports of the same wrappers | wrapper-utils is a Snakemake runtime; the ported scripts keep the wrapper logic verbatim |
| `gather_annotated_calls` / `filter_odds` | not ported | not reachable in the default path (benchmarking off + `filter: present` only) |
| template oncoprint views (`gene_oncoprint` / `variant_oncoprints` datasets) | empty (upstream defaults with a single group) | `prepare_oncoprint` itself runs and feeds the label-sorting table, exactly like upstream |
| vembrane filter/table expressions evaluated from Python at run time | precomputed literal expression/header (34 columns) | same semantics, evaluated once |
| upstream `config/units.tsv` absolute `/projects/...` read paths | `config.reads_dir` + sample group fixture paths | portability |
| Snakemake `temp()` outputs | `temporary = true` | engine equivalent |
| per-rule conda environments | one env per tool pin set (`envs/`) | same packages, same pins, consolidated |

## Links

- Repository: [oxo-flow-varlociraptor](https://github.com/oxo-flow-community/oxo-flow-varlociraptor)
- Upstream: [snakemake-workflows/dna-seq-varlociraptor](https://github.com/snakemake-workflows/dna-seq-varlociraptor) @ `v6.10.0`
- License: Apache-2.0 (this workflow) · MIT (upstream)

Created on 2026-08-15 — this port may lag behind upstream releases. See the repository's NOTICE for full attribution.
