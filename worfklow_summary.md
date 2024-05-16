# Summary of Steps in each workflow

## Workflows

Three main Snakemake workflows were developed: short-reads workflow, long-reads workflow, and post- classification workflow. The **short-reads workflow classifies Illumina NGS sequences**. The **long-reads workflow analyzes Oxford Nanopore Technologies (ONT) long-reads**. Meanwhile, the post-classification workflow does further sample analysis of either the short or long-reads workflows with the aim of a metadata file. Additionally, the short and long-reads workflows allow for an additional secondary workflow, called QC-only. These variants only perform the quality control step and are designed as a first step to evaluate the quality of the samples before classification.

### Configuration files
A YAML configuration file is required before running any analysis. There is a specific configuration file for every workflow with the needed parameters to run the analysis. You can find a template of the config files in the **config_templates folder**. Specify the parameters of your analysis before running the workflow

## Steps in each workflow

### QC-only workflows: 
1.	Quality Control with **FastQC** (short-reads) or **NanoPlot** (long-reads)

### Classification workflows:
1.	Quality Control of raw reads with **FastQC** (short-reads) or **NanoPlot** (long-reads)
2.	Sequence Trimming with **Trimmomatic (short-reads)** or NanoFilt (long-reads)
3.	Quality Control of trimmed reads with **FastQC** (short-reads) or **NanoPlot** (long-reads)
4.	Sample classification with **Kraken2** (short-reads) or **Centrifuge** (long-reads)
5.	Individual results for each sample: **Krona Graph, Alpha diversity, Relative abundance plot**
6.	Collective sample results for all samples: **OTU table, Rarefaction curve**
7.	Other files: **Citation file, copy of the configuration file** 

### Post-Classification workflow
A **metadata file** is required for the post-classification workflow. This is a csv file, with simple requirements: An identifier column (SampleID) with unique values (one row per sample), and any additional columns with other information about the samples. You can find an example of the metadata file in the **data/metadata folder** 

1.	**Beta diversity** using Bray-Curtis Distance \
2.	**Number of Sequences per Sample** plot \
3.	**Principal Coordinate Analysis Plot (PCoA)** colored by metadata variable \
4.	**Dendrogram** colored by metadata variable
