
# Installation Instructions

*Note: These instructions are a work in progress and will continue to evolve as we update our methods and findings.*

This project was primarily developed using [Michigan State University’s High-Performance Computing Center (HPCC)](https://icer.msu.edu/) . The following instructions outline how to reproduce the full workflow on the HPCC, including database setup, data collection, machine learning modeling, and visualization of results through model embeddings.

The project is located within the /mnt/research/TwoSix directory on the HPCC. Please ensure you are working within a space that provides sufficient storage capacity to accommodate the scraped data, MongoDB database, and trained models.

To begin, connect to the HPCC via [SSH](https://docs.icer.msu.edu/Connect_to_HPCC_System/), and follow the steps below for a complete setup and execution pipeline.

## MongoDB (Ethan writeup)

This project uses MongoDB version 3.6.8 installed manually on the HPCC. The instructions below guide you through installing the same version, starting the MongoDB server, and connecting to it for data operations. 

### Download and Install MongoDB v3.6.8
```bash
#Navigate to your working project directory
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.6.8.tgz
tar -xvzf mongodb-linux-x86_64-3.6.8.tgz
mv mongodb-linux-x86_64-3.6.8 mongodb
export PATH=$PWD/mongodb/bin:$PATH
```
### Create Data and Log Directories
```bash
mkdir data
mkdir log
```

### Starting and Connecting to the MongoDB Server
```bash
mongod --dbpath /mnt/research/your_directory/data --logpath /mnt/research/your_directory/log/mongod.log --fork
mongo
```

## Conda Setup

We use a shared `environment.yaml` file located at the base of our repo.

To install on HPCC, first run the following commands to load the Miniforge module

```bash
module purge
module load Miniforge3
```

To install the environment from the file
```bash
conda create --file environment.yaml
```

Before running *any* python code please activate the environment with...
```bash
conda activate CMSE495-TwoSix
```

## Mirrulations (Archisha or Emma writeup)

Once a server has been started on the current node and you have set up the conda environment (see above), the scraper job can be started with the following

```bash
conda activate CMSE495-TwoSix
sbatch data_collection/scrape.sb
```

It is a long-running checkpointing job, and will likely need to be ran multiple times to collect the full dataset, though further steps should be completeable with only a small subset

## Data Preprocessing and Cleaning (Archisha if needed)

## Model and Embedding Storage (Archan writeup)

## Visualizaiton (Archan or Archisha or Frank)

