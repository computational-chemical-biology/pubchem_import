#!/bin/bash -f
#SBATCH --partition=SP2
#SBATCH --ntasks=1              # numero de CPUs - neste exemplo, 1 CPU
#SBATCH --cpus-per-task=1       # Number OpenMP Threads per process
#SBATCH -J pftp 
#SBATCH --time=192:00:00         # Se voce nao especificar, o default é 8 horas. O limite é 480 horas

#OpenMP settings:
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OMP_PLACES=threads
export OMP_PROC_BIND=spread

echo $SLURM_JOB_ID              #ID of job allocation
echo $SLURM_SUBMIT_DIR          #Directory job where was submitted
echo $SLURM_JOB_NODELIST        #File containing allocated hostnames
echo $SLURM_NTASKS              #Total number of cores for job

source ~/.bashrc
cd /scratch/6293113/pubchem
#python pubchem_ftp.py 
wget ftp.ncbi.nlm.nih.gov/pubchem/Compound/CURRENT-Full/SDF/Compound_000000001_000500000.sdf.gz
