# Small and structural variant calling with Varlociraptor

oxo-flow port of snakemake-workflows/dna-seq-varlociraptor v6.10.0 (default-parameter path, one tumor sample group): vg giraffe mapping against the 1000 Genomes human pangenome, FastQC/MultiQC QC, mosdepth coverage with region filtering, freebayes + delly candidate calling, Varlociraptor calling under scenario some_id (present + somatic_tumor_high + somatic_tumor_medium, FDR 0.05, local-smart), per-variant-type FDR control (SNV/INS/DEL/MNV/BND/INV/DUP/REP) with merge and phred decoding, VEP annotation with LoFtool + REVEL plugins and dbSNFP annotation, annotation filtering, the 34-column vembrane variant table, oncoprint label-sorting preparation, and datavzrd reports for variant calls and gene coverage. 88 rules, commands byte-identical to upstream wrappers.

| | |
|---:|---|
| **Engine** | snakemake |
| **Source** | [snakemake-workflows/dna-seq-varlociraptor](https://github.com/snakemake-workflows/dna-seq-varlociraptor) |
| **Pinned version** | `v6.10.0` |
| **Ported** | 2026-08-15 |
| **Rules** | 88 |
| **Tools** | altair · bcftools · bedtools · biopython · curl · datavzrd · delly · ensembl-vep · fastqc · freebayes · gatk4 · gawk · htslib · mosdepth · multiqc · openpyxl · pandas · parallel · picard · pysam · python · rust-bio-tools · samtools · scikit-learn · sed · snpsift · statsmodels · unzip · varlociraptor · vcflib · vega-lite-cli · vembrane · vg |
| **Domain** | genomics |

## Run it

```bash
oxo-flow run workflow/varlociraptor.toml
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

- bwa mapping — non-default aligner branch
- fastp/trimming — non-default branch
- fusions (arriba) — off in default config (calling mode variants)
- MAF conversion — not reachable with default config
- mutational burden and mutational signature analyses
- population database (germline AF annotation) — off by default
- dgidb druggability — off by default
- CADD annotation — off by default
- primer design — off by default
- benchmarking rules
- consensus reads — non-default branch
- target regions — not in default path
- template oncoprint views (gene_oncoprint / variant_oncoprints datasets) — empty with single group; prepare_oncoprint itself runs
- gather_annotated_calls / filter_odds — not reachable in default path (benchmarking off, filter present only)
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
- License: Apache-2.0 (port) · MIT (upstream)

This port was created on 2026-08-15 and may lag behind upstream releases. See the repository's NOTICE for full attribution.
