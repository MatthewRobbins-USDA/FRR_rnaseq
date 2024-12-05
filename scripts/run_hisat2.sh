#! /bin/bash
#SBATCH -A forage_turf
#SBATCH --job-name="run_hisat2"
#SBATCH -q frr
#SBATCH -p priority
#SBATCH -n 24
#SBATCH -t 04:00:00
#SBATCH -o "run/logs/hisat2/stdout.%x.%j.%N"
#SBATCH -e "run/logs/hisat2/stderr.%x.%j.%N"
date

trimdir="$(pwd)/trimmomatic_output"
basedir=$1
basename=$2
sample=$3

mkdir hisat2_output
cd hisat2_output

curdir=`pwd`

module purge
module load apptainer

singularity exec --cleanenv \
	-B ${trimdir}:/trim \
	-B ${curdir}:/cur \
	-B ${basedir}:/base \
	/project/forage_turf/shared/singularity/rnaseq.sif hisat2 \
	-x /base/${basename} \
        -p 24 \
        -1 /trim/${sample}_R1.fq.gz \
        -2 /trim/${sample}_R2.fq.gz \
        -S /cur/${sample}_prg_nagy.sam \
	&> ${sample}_hisat2_nagy_log.txt

singularity exec --cleanenv \
	-B ${curdir}:/cur \
	/project/forage_turf/shared/singularity/rnaseq.sif samtools sort \
	-n \
	-@ 24 \
	-O bam \
	-o /cur/${sample}_prg_nagy_sorted.bam \
	/cur/${sample}_prg_nagy.sam

rm ${sample}_prg_nagy.sam
date
