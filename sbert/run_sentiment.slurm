#!/bin/bash --login
#SBATCH --job-name=add_sentiment
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=10
#SBATCH --gres=gpu:a100:1
#SBATCH --mem=256G
#SBATCH --time=24:00:00
#SBATCH --output=add_sentiment_%j.log
#SBATCH --error=add_sentiment_%j.err
#SBATCH --mail-type=END,FAIL
#SBATCH --mail-user=bhatta73@msu.edu

module purge
module load Miniforge3
conda activate CMSE495-TwoSix

cd /mnt/research/TwoSix/bhatta73/TwoSix_Spring25

python sbert_and_viz/add_sentiment.py

# Optional speed/stability tweaks
export OPENBLAS_NUM_THREADS=1