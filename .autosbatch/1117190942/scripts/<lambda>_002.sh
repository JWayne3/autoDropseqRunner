#!/bin/bash
#SBATCH --job-name=<lambda>_002
#SBATCH --partition=gpu
#SBATCH --nodes=1
#SBATCH -w gpu19
#SBATCH --cpus-per-task=4
#SBATCH --error=.autosbatch/1117190942/log/<lambda>_002.err.log
#SBATCH --output=.autosbatch/1117190942/log/<lambda>_002.out.log

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