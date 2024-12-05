#! /bin/bash
#SBATCH -A forage_turf
#SBATCH --job-name="run_htseq"
#SBATCH -q frr
#SBATCH -p priority
#SBATCH -n 2
#SBATCH -t 06:00:00
#SBATCH -o "run/logs/htseq/stdout.%x.%j.%N"
#SBATCH -e "run/logs/htseq/stderr.%x.%j.%N"
date

sample=$1
gfffile=$2
bamdir="$(pwd)/hisat2_output"
gffdir=`dirname $gfffile`
gffname=`basename $gfffile`

mkdir htseq_output
cd htseq_output

curdir=`pwd`

module purge
module load apptainer

singularity exec --cleanenv \
	-B ${bamdir}:/bams \
	-B ${gffdir}:/gff \
	-B ${curdir}:/cur \
	/project/forage_turf/shared/singularity/rnaseq.sif htseq-count \
	-m union \
	-f bam \
	-r name \
	-a 10 \
	-i Parent \
	-s no \
	/bams/${sample}_prg_nagy_sorted.bam \
	/gff/${gffname} \
	1> ${sample}_htseq_counts.tsv \
	2> ${sample}_htseq_log.txt

#-c /cur/${sample}_htseq_counts \
#-i in above command indicates gene_id on the exon line of the gff file. This may need to be adjusted based on inputted gff file.
date
