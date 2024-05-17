# Snakemake Metagenomics Workflow

## Summary:

This Snakemake-based program allows to classify metagenomic samples from NGS and ONT samples.

## Brief Description

The program allows to clasify and analyze NGS sequences and long-read ONT samples.
The program consists of 3 workflows: short-reads classification, long-reads classification and post-classification workflow.  The short-reads workflow and the long-reads workflow have a QC-only mode, which runs FastQC and NanoPlot respectively. This method is useful to evaluate sequence quality before classification.
The post-classification workflow works on the results of the classification workflows and provides additional information using a metadata file and an additional target variable.

## Prerequisites

This installation requires git and conda/miniconda. If they are already installed, skip these steps, otherwise install them they with the following steps:

Git Installation: \
```sudo apt install git```

Miniconda Installation:
```
mkdir -p ~/miniconda3
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda3/miniconda.sh
bash ~/miniconda3/miniconda.sh -b -u -p ~/miniconda3
After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:zrm -rf ~/miniconda3/miniconda.sh
```

After installing, initialize your newly-installed Miniconda. The following commands initialize for bash and zsh shells:
```
~/miniconda3/bin/conda init bash
~/miniconda3/bin/conda init zsh
```

## Snakemake Installation

```
git clone https://github.com/pablorr24/metagenomics_snakemake/
cd metagenomics/Snakemake
conda env create -f environment.yml -n snakemake_meta
conda activate snakemake_meta
```
## Database Installation

If you already have a database such as Silva, Greengenes, RefSeq, Kraken2, or a similar classification database, you can skip this step. Otherwise, make sure you install a database. The following instructions will download and install the Silva database. 

```
cd databases/
kraken2-build --special silva --db SilvaDB
kraken2-build --special greengenes --db greengenes
```

### Running a workflow 

For details on the steps of each workflow, see the **workflow_summary** file

To run a workflow, first modify the configuration file and adjust to your parameters. Afterwards, run Snakemake.
Note: Make sure you are in the working directory (specified in the config file)

### Short-reads
```snakemake -s Snakefile_fastqc --cores all``` \
```snakemake -s Snakefile_full_workflow --cores all``` 

### Long-reads
```snakemake -s Snakefile_nanoplot --cores all``` \
```snakemake -s Snakefile_long_read --cores all``` 

### Post Classification Workflow
```snakemake -s Snakefile_post_analysis --cores all``` 

**Metadata File** \
The post-classification workflow requires a metadata file, with one row per sample, and different columns specifying specific sample variables (sample location, species, etc). 

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
