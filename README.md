# Snakemake Metagenomics Workflow

### Summary:

This Snakemake-based program allows to classify metagenomic samples from NGS and ONT samples.

### Brief Description

The program allows to analyze NGS sequences and long-read ONT samples.

For short-read sequences, it allows 3 different workflows:  

1. Quality control workflow (fastqc)  
2. Kraken-2 Classification workflow (full workflow)  
3. Post-classification Analysis (post analysis)


For long-read sequences, it allows 3 different workflows:

1. Quality control workflow (nanofilt)
2. Centrifuge Classification workflow (full workflow)
3. Post-classification Analysis (post analysis)

### Prerequisites

To run this workflow, you need:

- Anaconda Environment
- Python 3.6+
- Snakemake 5.10+
- Minimum disk space of -- gb.
- Other dependencies listed in a `requirements.txt` or `environment.yml` file

### Installation

```git clone...```
(other steps)


### Preparation steps

After installing the program, you need to add your data in the /data folder. The program accepts zipped (.gz) and unzipped (.fq or .fastq) raw files.

Simply add the data files in the corresponding folder
For short-read sequences: `".../snake_folder/data/short-reads/"`
For long-read sequences: `".../snake_folder/data/long-reads/"`

For short read sequences, the program expects two files per sample (forward and reverse), with the following format: `"sample1_1.fq"`, `"sample1_2.fq"`. Make sure your samples have the "_1.fq" and "_2.fq" format.

For long-read sequences, the program expects regular fastq files (sample1.fastq).

Trimmomatic also may require to include adapters. Some adapters are included in `".../snake_folder/data/short-reads/adapters/"` but some 

The post-classification analysis works for both short and long-read sequences. A metadata file with the sample information must be provided. Make sure the you have unique values in the SampleID column.

### Config file

There is a YAML config file for each of the workflows. This file must be edited with the right parameters and configuration before performing the analysis.

### Running the workflows

Running the workflow requires to be in the correct anaconda environment 

```conda activate snakemake```

Then, simply run the desired workflow:

**Short-reads quality control**

```snakemake -s Snakefile_fastqc --cores all```

**Short-reads classification**

``` snakemake -s Snakefile_full_workflow --cores all ```

**Long-reads quality control**

```snakemake -s Snakefile_nanofilt --cores all```

**Long-reads classification**

```snakemake -s Snakefile_long_read --cores all```

**Post-classification analysis**

```snakemake -s Snakefile_post_analysis --cores all```

### Output 

After running the workflow, a timestamp folder is created in the `output` folder. Specific folders are created with the different results of the workflow. A copy of the config file is also created, which can be used to track the parameters used in the analysis.

### References

