#! /bin/bash
#SBATCH -A forage_turf
#SBATCH --job-name="QC"
#SBATCH -q frr
#SBATCH -p priority
#SBATCH -N 1
#SBATCH -n 12
#SBATCH -t 0-04:00:00
#SBATCH -o "run/logs/step1_qc/stdout.%x.%j.%N"
#SBATCH -e "run/logs/step1_qc/stderr.%x.%j.%N"

# This wrapper scripts runs FastQC and MultiQC on input fastq.gz files

date

in_dir=$1

out_dir=$(pwd)/QC

mkdir $out_dir

module load apptainer

for file in ${in_dir}/*.gz
do
	singularity exec --cleanenv \
		/project/forage_turf/shared/singularity/seqtools.sif \
		fastqc -o ${out_dir} $file | tee -a ${out_dir}/step1.log
done

mkdir ${out_dir}/multiqc
singularity exec --cleanenv \
	/project/forage_turf/shared/singularity/seqtools.sif \
	multiqc -o ${out_dir}/multiqc ${out_dir} | tee -a ${out_dir}/step1.log

date
