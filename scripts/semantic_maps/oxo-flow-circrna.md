**circRNA detection pipeline**: given paired-end FASTQ reads and a reference genome, it trims and QC-checks the reads, detects circular RNAs with four complementary callers running in parallel, merges their calls, and delivers an across-sample circRNA table plus an HTML report.

**1. Read QC and trimming** — `fastp` is the entry point: it trims adapters and low-quality tails from raw paired-end reads and emits trimmed FASTQ plus per-sample fastp JSON/HTML reports. `multiqc` consumes those JSONs and aggregates them into one MultiQC HTML report.

**2. Parallel detection (four complementary callers)** — trimmed reads fan out to four independently running methods: `ciriquant` (CIRIquant, BWA/HISAT2 alignment-based), `circexplorer2` (CIRCexplorer2, BWA unmapped-junction based), `find_circ` (bowtie2 anchor based), and `circrna_finder` (circRNA_finder, STAR chimeric-read based). Each writes a per-sample BED of candidate circRNAs.

**3. Aggregation and reporting** — `aggregate` merges the four BEDs per sample, tolerating a missing caller (at least 2 of the 4 methods are required) and writing results/{sample}.aggr.txt. From the same aggregate two steps diverge in parallel: `aggregate_dataset` pools all per-sample aggregates into one dataset table, while `report` renders the circRNA HTML report.

*Verified: every rule name above is a real rule of main.oxoflow (oxo-flow validate); the described order follows the actual rule dependencies.*
