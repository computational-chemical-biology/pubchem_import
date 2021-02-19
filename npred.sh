#!/bin/bash  
#SBATCH --partition=GPUSP4
#SBATCH --ntasks=20 		# number of tasks / mpi processes
#SBATCH --cpus-per-task=20 	# Number OpenMP Threads per process
#SBATCH -J npred 
#SBATCH --time=80:00:00 	# Se voce nao especificar, o default é 8 horas. O limite é 80 horas.
#SBATCH --gres=gpu:tesla:1       # para solicitar uma GPU


#OpenMP settings:
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

echo $SLURM_JOB_ID		#ID of job allocation
echo $SLURM_SUBMIT_DIR		#Directory job where was submitted
echo $SLURM_JOB_NODELIST	#File containing allocated hostnames
echo $SLURM_NTASKS		#Total number of cores for job

export PATH=/scratch/6293113/miniconda3/bin/:$PATH
source ~/.bashrc
conda activate pubchem 

cd /scratch/6293113/pubchem/pubchem_import
snakemake --cores all 
