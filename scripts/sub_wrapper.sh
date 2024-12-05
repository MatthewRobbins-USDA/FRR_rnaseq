#! /bin/bash
#SBATCH -A arsturf
#SBATCH --job-name="sub_wrapper"
#SBATCH -q frr
#SBATCH -p priority
#SBATCH -n 1
#SBATCH -t 24:00:00
#SBATCH -o "run/logs/subwrapper/stdout.%x.%j.%N"
#SBATCH -e "run/logs/subwrapper/stderr.%x.%j.%N"

sample=$1
seqdir=$2
r1=$3
r2=$4
basedir=$5
basename=$6
gfffile=$7

date
#id1=`sbatch -W -J ${sample}_trimmomatic  run/run_trimmomatic.sh $seqdir $sample $r1 $r2 | cut -d ' ' -f4`
date
#id2=`sbatch --dependency=afterok:${id1}  -W -J ${sample}_hisat2 run/run_hisat2.sh $basedir $basename $sample | cut -d ' ' -f4`
date
#sbatch --dependency=afterok:${id2} -W -J ${sample}_htseq run/run_htseq.sh $sample $gfffile
sbatch -W -J ${sample}_htseq run/run_htseq.sh $sample $gfffile
date
