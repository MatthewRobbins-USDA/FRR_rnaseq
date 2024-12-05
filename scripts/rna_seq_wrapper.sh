#! /bin/bash

tablefile=$1

while read -r LINE
do
	sample=`echo "${LINE}" | awk '{print $1}'`
	if [[ "$sample" == "Sample" ]]; then
		continue
	fi
	if [[ "$sample" == \#* ]]; then
		continue
	fi
	seqdir=`echo "${LINE}" | awk '{print $2}'`
	r1=`echo "${LINE}" | awk '{print $3}'`
	r2=`echo "${LINE}" | awk '{print $4}'`
	basedir=`echo "${LINE}" | awk '{print $5}'`
	basename=`echo "${LINE}" | awk '{print $6}'`
	gfffile=`echo "${LINE}" | awk '{print $7}'`
	sbatch -J ${sample}_fastqc run/run_QC.sh $seqdir
	sbatch -J ${sample}_sub_wrapper run/sub_wrapper.sh $sample $seqdir $r1 $r2 $basedir $basename $gfffile
done < "$tablefile"
