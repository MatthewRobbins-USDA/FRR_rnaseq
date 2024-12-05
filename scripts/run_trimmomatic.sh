#! /bin/bash
#SBATCH -A forage_turf
#SBATCH --job-name="run_trimmomatic"
#SBATCH -q frr
#SBATCH -p priority
#SBATCH -n 24
#SBATCH -t 01:30:00
#SBATCH -o "run/logs/trimmomatic2/stdout.%x.%j.%N"
#SBATCH -e "run/logs/trimmomatic2/stderr.%x.%j.%N"
date

seqdir=$1
sample=$2
r1file=$3
r2file=$4
adaptpath=/usr/local/Trimmomatic-0.39/adapters/TruSeq3-PE.fa

#file1=`echo $file | cut -f4 -d'/'`
#fileR=`echo $file1 | sed 's/_R1/_R2/'`
#file1trim=`echo $file1 | sed 's/.fq.gz/_trim/'`
#fileRtrim=`echo $fileR | sed 's/.fq.gz/_trim/'`
#echo $file1
#echo $fileR
#echo $file1trim
#echo $fileRtrim

echo $seqdir/$r1file

mkdir trimmomatic_output
cd trimmomatic_output

curdir=`pwd`

module purge
module load apptainer

singularity exec --cleanenv \
	-B ${seqdir}:/seqs \
	-B ${curdir}:/cur \
	/project/forage_turf/shared/singularity/rnaseq.sif java -jar /usr/local/Trimmomatic-0.39/trimmomatic-0.39.jar PE -threads 24 -phred33 \
	/seqs/${r1file} \
	/seqs/${r2file} \
	/cur/${sample}_R1.fq.gz \
	/cur/${sample}_R1_unpair.fq.gz \
	/cur/${sample}_R2.fq.gz \
	/cur/${sample}_R2_unpair.fq.gz \
	ILLUMINACLIP:${adaptpath}:2:30:10 LEADING:5 TRAILING:5 SLIDINGWINDOW:4:20 MINLEN:51 \
	&> ${sample}_trimmomatic.log
date
