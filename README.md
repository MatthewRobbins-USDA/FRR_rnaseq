# FRR_rnaseq
Code and notes on the pipeline the FRR on the ARS computing clusters to run and RNAseq analysis

This repository contains scripts used to run RNAseq analysis on an HPC with a SLURM controller.

## Setup
### Docker/Singularity
This pipeline is run using a Singularity container. We built this container by first creating a Docker container, exporting it, and then converting it to Singularity using `singularity build`. To build the docker container, download the files in this repository's docker folder, and run
```
docker build -t rnaseq .
```
From the directory containing the files from the docker folder. Once you have build the container, it can be exported to a tar file with
```
docker save -o rnaseq.tar rnaseq
```
You can then convert it to a singualrity container with
```
singularity build rnaseq.sif docker-archive:///path/to/rnaseq.tar
```

### Scripts setup
In order to run the scripts, you will need to create a run folder within your working directory for the scripts to reside in, i.e
```
mkdir run
```

Copy the scripts from this repository's scripts folder into the newly created run folder.

### Table setup
This pipeline operates by using a table of samples and their corresponding files and metadata. The table is tab delimited (essentially a .tsv). Its columns and data are as follows
|Sample|Location|R1|R2|base_ref_dir|basename|GFF_file|
|:---|:---|:---|:---|:---|:---|:---|
|Name of the sample|Full file path to folder containing the R1 and R2 files| R1 filename | R2 filename | Full file path to the base reference folder | Basename of the ht2 files in the base reference folder | Full path to the GFF file |

For example, the table could look something like this:
```
Sample  Location        R1      R2      base_ref_dir    basename        GFF_file
lat1    /path/to/lat1/data    lat1_1.fq.gz    lat1_2.fq.gz    /path/to/ht2/files    haplo_a    /path/to/gff.gff3
lat2    /path/to/lat2/data    lat2_1.fq.gz    lat2_2.fq.gz    /path/to/ht2/files    haplo_a    /path/to/gff.gff3
lat3    /path/to/lat3/data    lat3_1.fq.gz    lat3_2.fq.gz    /path/to/ht2/files    haplo_a    /path/to/gff.gff3
```

## Running the pipeline
Once you have everything setup, you can run the pipeline with
```
./run/rna_seq_wrapper.sh ./table
```
This will run the pipeline in your current directory from your table file. The pipeline will end up creating 4 output folder: QC, trimmomatic_output, hisat2_output, and htseq_output. These folder will contain the results for each step of the pipeline, and will have logs as well. Additional logs will be created in run/logs.
