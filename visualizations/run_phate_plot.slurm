#!/bin/bash --login
#SBATCH --job-name=phate
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8
#SBATCH --mem=200G
#SBATCH --time=6:00:00
#SBATCH --output=phate_%j.log
#SBATCH --error=phate_%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=bhatta73@msu.edu

module purge
module load Miniforge3
conda activate CMSE495-TwoSix

cd /mnt/research/TwoSix/bhatta73/TwoSix_Spring25

python visualizations/phate_plot.py
