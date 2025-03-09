# Installation Instructions

## Git Repo

Install this repo using
```bash
git clone https://github.com/wangzey5/TwoSix_Spring25.git
```

## Environment Setup

We used [Anaconda](https://www.anaconda.com/) for environment management, please download and install it if it is not already installed.

Our repo includes an `environment.yaml` file. To create a new environment using this file navigate to the base directory of our repo and run
```bash
conda env create --file environment.yaml
```

In order to replicate the data collection phase, first install MongoDB. This process is different on different machines, so please follow the [MongoDB Install Instructions](https://www.mongodb.com/docs/manual/installation/)

> **MongoDB Version**: We are using the [MSU HPCC](https://docs.icer.msu.edu/). Due to dependency conflicts and system limitations, MongoDB 3.6.8 is the most viable version for deployment on HPCC.

##### Pre-runtime setup

Before running *any* of the following code, ensure that the conda environment is activated and you have a MongoDB server running locally.

To activate the environment run
```bash
conda activate CMSE495-TwoSix
```

You can start the MongoDB server by locating the `mongod` executable and running it. Do not change the port from the default port. 

> **MongoDB Auto-start**: Many distributions of MongoDB autostart the MongoDB server on startup, if the `mongod` command fails, please check to see if it already running with task manager or `ps aux | grep mongod` before proceeding with trouble-shooting

## Data Collection

> **API Keys**: By default our code uses an API key owned by a team member. To use your own API key please create one at [regulations.gov API](https://open.gsa.gov/api/regulationsgov/), then either supply this to the `RegAPI` constructor in the `data_collection/API-Scraping.ipynb` file or to the `--apikey` argument when running `data_collection/scrape.py`

Our data is collected using the [regulations.gov API](https://open.gsa.gov/api/regulationsgov/) and stored in a MongoDB database using pymongo. 

The full data collection process takes several days to weeks. To collect only a small amount of sample data, you can use the Jupyter Notebook `data_collection/API-Scraping.ipynb` by running `jupyter lab` and navigating to the notebook using Jupyter Lab's file explorer.

To perform the full data collection, you can call the python script at `data_collection/scrape.py`. For details on arguments run `python data_collection/scrape.py --help`. 

## Modeling and Visualization

Our modeling and visualization code can be found in `DemoCode.ipynb`. Once you have collected some sample data in the local MongoDB database, you can run the code by running `jupyter lab` and navigating to `DemoCode.ipynb` using the file explorer.
