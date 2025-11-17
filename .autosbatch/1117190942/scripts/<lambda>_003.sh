#!/bin/bash
#SBATCH --job-name=<lambda>_003
#SBATCH --partition=gpu2
#SBATCH --nodes=1
#SBATCH -w gpu38
#SBATCH --cpus-per-task=4
#SBATCH --error=.autosbatch/1117190942/log/<lambda>_003.err.log
#SBATCH --output=.autosbatch/1117190942/log/<lambda>_003.out.log

echo "Process will start at : "
date
echo "----------------------------------------"

##############################
conda run -n autoDropRunner snakemake --snakefile /mnt/hpc/home/weiyongjian/tool_installations/autoDropseqRunner/autodroprunner/Snakefile_drop.smk --cores 4 -d /mnt/hpc/home/weiyongjian/tool_installations/autoDropseqRunner/test_output_autosbatch/test3and4 --rerun-incomplete
wait
##############################

echo "========================================"
echo "Process end at : "
date