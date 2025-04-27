
# Installation Instructions

This project was primarily developed using [Michigan State University’s High-Performance Computing Center (HPCC)](https://icer.msu.edu/) . The following instructions outline how to reproduce the full workflow on the HPCC, including database setup, data collection, machine learning modeling, and visualization of results through model embeddings.

The project is located within the /mnt/research/TwoSix directory on the HPCC. Please ensure you are working within a space that provides sufficient storage capacity to accommodate the scraped data, MongoDB database, and trained models, as well as enough memory to run BERTopic modeling and high-dimensional visualizations.

To begin, connect to the HPCC via [SSH](https://docs.icer.msu.edu/Connect_to_HPCC_System/), and follow the steps below for a complete setup and execution pipeline.

## MongoDB 

This project uses MongoDB version 3.6.8 installed manually on the HPCC. The file [setup_mongodb.sh](https://github.com/wangzey5/TwoSix_Spring25/blob/main/setup_mongodb.sh) automates the following steps:

- Downloads and extracts MongoDB
- Adds MongoDB to the local enviroment path
- Creates the necessary data and log directories
- Starts the MongoDB server
- Opens the MongoDB shell to verify it is working

To exit, simply type ```exit```. 

### Make sure the setupt script is executable
```
chmod +x setup_mongodb.sh
```
### Run the script 
```
./setup_mongodb.sh
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
conda env create --prefix ./envs --file environment.yml
```

Before running *any* python code please activate the environment with...
```bash
conda activate CMSE495-TwoSix
```

## Mirrulations

Once a server has been started on the current node and you have set up the conda environment (see above), the scraper job can be started with the following

```bash
conda activate CMSE495-TwoSix
sbatch data_collection/scrape.sb
```

It is a long-running checkpointing job, and will likely need to be ran multiple times to collect the full dataset, though further steps should be completeable with only a small subset

## Data Extraction and Preprocessing

You may extract the data through your own instance of mongodb, but if you have access to '/mnt/research/TwoSix/mongodb' on the HPCC, the MongoDB server will aleady contain the Mirrulations-scraped data under the 'mirrulations' database. To extract the scraped data into a json file 'comments.json' for pre-processing, follow these steps:

1. Connect to a development node, or an interactive node with sufficient memory.

2. Ensure the MongoDB instance and server is up and running. (ensure you have followed instructions above)

3. Export the data
The MongoDB database tools including mongoexport are located at: ```bash
/mnt/ufs18/rs-036/TwoSix/mongodb/mongodb-database-tools-ubuntu2004-x86_64-100.2.1/bin/mongoexport
```

To export the raw_comments collection from the mirrulations database into a json file, run the following bash command (note that it is not a Mongo shell command and should be run through your normal bash terminal)

```bash
/mnt/ufs18/rs-036/TwoSix/mongodb/mongodb-database-tools-ubuntu2004-x86_64-100.2.1/bin/mongoexport \
  --db=mirrulations \
  --collection=raw_comments \
  --out=/mnt/research/TwoSix/data/comments.json
```

As the comments.json you have just extracted is very messy and unclean, we first extract a .csv out of the .json file by running extract_csv.py: 
[Make sure you are in the TwoSix_Spring25 repository. 'cd /your_path/TwoSix_Spring25']

```bash
python data/extract_csv.py
```
Then, to clean the csv, run the cleaning slurm job which calls on cleaning.py:

```bash
sbatch data/run_cleaning.slurm
```

You may also access our extracted and cleaned data files which we have used for this project through the [data/README.md](data/README.md).

## Modeling and Embedding

To add the BERTopic embeddings, and sentiment:

```bash
sbatch sbert/run_sbert.slurm
```
This output df_final, which will be used for visualization and analyses, and can be found in [data/README.md](data/README.md) as well

## Visualization

We have utilized Jupyter notebooks to run our visualization results.

For preliminary BERTopic and sentiment analyses visualizations, we have the files [sbert/bertopic_analysis.ipynb](bertopic_analysis.ipynb), and [sentiment.ipynb](sbert/sentiment.ipynb). 
We have [phate.ipynb](visualizations/phate.ipynb) and [comparison.ipynb](visualizations/comparison.ipynb) to show dimensionality reducing methods and their clustering.

The output visualizations can be accessed through the directory 'outputs'.

---