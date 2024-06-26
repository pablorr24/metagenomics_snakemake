# Snakemake Metagenomics Workflow

## Summary:

This Snakemake-based program allows an automated classification of metagenomic samples from Illumina and Oxford Nanopore Technologies, as well as an automatic generation of different visualizations, tables and statistics useful in the metagenomics field.

## Brief Description

The metagenomics workflows were developed using Snakemake Version 7.32.4 on an Ubuntu 22.04.2 LTS environment. The program was developed on an UNIX system and is compatible with Linux and iOS devices. For Windows users, using a Linux virtual environment such as Oracle Virtual Box is required. \
This program consists of 3 workflows: short-reads classification, long-reads classification and post-classification workflow. The short-reads workflow and the long-reads workflow have a QC-only mode, which runs FastQC and NanoPlot respectively. This method is useful to evaluate sequence quality before classification. The post-classification workflow works on the results of the classification workflows and provides additional information using a metadata file and an additional target variable.

The figure below shows the general steps of each workflow. For a detailed view of the steps in each workflow, check the **workflow_summary.md** file. 

![image](https://github.com/pablorr24/metagenomics_snakemake/assets/92135285/c98ff5f7-e1ba-4799-934f-faf9400cb25d)



## Prerequisites

This installation requires git and conda/miniconda. If they are already installed, skip these steps. To check if you have git and miniconda/conda installed, type
```git --version```
```conda --version```

If you need to install them, follow these steps:

Git Installation: \
```sudo apt install git```

Miniconda Installation:
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
```

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:
```
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

## Snakemake Installation

```
git clone https://github.com/pablorr24/metagenomics_snakemake/
cd metagenomics_snakemake
conda env create -f environment.yml -n snakemake_meta
conda activate snakemake_meta
```
Every new time you want to run Snakemake metagenomics, make sure to activate the conda environment with ```conda activate snakemake_meta```

## Update Krona Taxonomy

Before runnung the analysis, you must update the Krona Taxonomy. Navigate to ```home/miniconda3/envs/snakemake_meta/opt/krona``` and run 
```
 ./updateTaxonomy.sh
```

This process may take a couple of minutes.

## Short-reads database installation
If you already have access to a classification database such as Silva, Greengenes, or Kraken2, you can skip the installation step. Otherwise, make sure you install a database. The following instructions will download and install the Silva and Greengenes databases. Navigate to the your main folder and run:

```
cd databases/
kraken2-build --special silva --db silvaDB
kraken2-build --special greengenes --db greengenesDB
```

## Long-reads database installation 
For long-read sequences, Centrifuge requires a different database configuration. The following steps download the Centrifuge (compressed) database.

```
centrifuge-download -o taxonomy taxonomy
wget https://genome-idx.s3.amazonaws.com/centrifuge/p_compressed_2018_4_15.tar.gz
tar -xzvf genome-idx.s3.amazonaws.com/centrifuge/p_compressed_2018_4_15.tar.gz -C /database/centrifuge_db/
```

After this, you will see several files with the format db_centrifuge#.cf, where db_centrifuge is the prefix. This prefix will be important later, as it must match the parameter ‘prefix’ in your configuration file. Navigate to the folder where the Silva database is located and type the following command:

You can also adapt a previously installed database to work with Centrifuge. The following example shows how to build the previously installed Silva database for use by Centrifuge.

```
centrifuge-build --conversion-table seqid2taxid.map --taxonomy-tree taxonomy/nodes.dmp --name-table taxonomy/names.dmp library/combined_sequences.fna silva_centrifuge
```
This command will generate the .cf files that will become the prefix on the configuration file. Note that the file names may change, but they generally follow the previous format.

### Running a workflow 

For details on the steps of each workflow, see the **workflow_summary.md** file. You can also follow the example in the /example folder.

To run a workflow, first modify the configuration file and adjust to your parameters. Afterwards, run Snakemake.
Note: Make sure you are in the working directory (specified in the config file)

### Short-reads
QC-only: ```snakemake -s Snakefile_fastqc --cores all``` \
Classification Workflow: ```snakemake -s Snakefile_short_reads_full_workflow --cores all``` 

### Long-reads
QC-only:```snakemake -s Snakefile_nanoplot --cores all``` \
Classification Workflow:```snakemake -s Snakefile_long_reads_full_workflow --cores all``` 

### Post Classification Workflow
**Metadata File** (only for post-classification workflow) \
The post-classification workflow requires a metadata file, with one row per sample, and different columns specifying specific sample variables (sample location, species, etc). Please update this file before running the analysis

```snakemake -s Snakefile_post_classification --cores all``` 

### Output 

After running the workflow, a timestamped folder is created in the `output` folder. All your results will be inside this folder.

### References

**Rules**

The rule ‘create_otu_table’ uses a modified version of the ‘kraken2OTU.py’ script created by GitHub user sipost1, available in https://github.com/sipost1/kraken2OTUtable/blob/main/kraken2otu.py

The rules ‘calculate_alpha_diversity’ and 'calculate_beta_diversity' use a modified version of the ‘alpha_diversity.py’and 'beta_diversity_py' script created by GitHub user jenniferlu717 in the DiversityTools repository, available in https://github.com/jenniferlu717/KrakenTools/blob/master/DiversityTools/alpha_diversity.py

The rules ‘create_dendogram’ and ‘create_pcoa_plot’ use a modified_version of the ‘dendro.R’ and ‘pca.R’ created by GitHub user GATB in the simka repository, both available in https://github.com/GATB/simka/tree/master/scripts/visualization

**External Software**

Andrews, S. (2010). FastQC:  A Quality Control Tool for High Throughput Sequence Data [Online]. Available online at: http://www.bioinformatics.babraham.ac.uk/projects/fastqc/

Bolger, A. M., Lohse, M., & Usadel, B. (2014). Trimmomatic: A flexible trimmer for Illumina Sequence Data. Bioinformatics, btu170.

Wood, D.E., Lu, J. & Langmead, B. Improved metagenomic analysis with Kraken 2. Genome Biol 20, 257 (2019). https://doi.org/10.1186/s13059-019-1891-0

Ondov, B.D., Bergman, N.H. & Phillippy, A.M. Interactive metagenomic visualization in a Web browser. BMC Bioinformatics 12, 385 (2011). https://doi.org/10.1186/1471-2105-12-385

Wouter De Coster, Svenn D’Hert, Darrin T Schultz, Marc Cruts, Christine Van Broeckhoven, NanoPack: visualizing and processing long-read sequencing data, Bioinformatics, Volume 34, Issue 15, August 2018, Pages 2666–2669, https://doi.org/10.1093/bioinformatics/bty149

Kim D, Song L, Breitwieser FP, Salzberg SL. Centrifuge: rapid and sensitive classification of metagenomic sequences. Genome Res. 2016 Dec;26(12):1721-1729. doi: 10.1101/gr.210641.116. Epub 2016 Oct 17. PMID: 27852649; PMCID: PMC5131823.
