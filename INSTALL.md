# Installation Instructions

### Git Repo

Install this repo using
```bash
git clone git@github.com:wangzey5/TwoSix_Spring25.git
```

### Environment Setup

We used [Anaconda](https://www.anaconda.com/) for environment management, please download and install it if it is not already installed.

Our repo includes an `environment.yaml` file. To create a new environment using this file navigate to the base directory of our repo and run
```bash
conda env create --file environment.yaml
```

To use this environment you must activate it before running any code. To do so run
```bash
conda activate CMSE495-TwoSix
```

### Data Collection

> **Note**: We are using the [MSU HPCC](https://docs.icer.msu.edu/). Due to dependency conflicts and system limitations, MongoDB 3.6.8 is the most viable version for deployment on HPCC.

Our data is collected using the [regulations.gov API](https://open.gsa.gov/api/regulationsgov/) and stored in a MongoDB database using pymongo. In order to replicate the data collection phase, first install MongoDB. This process is different on different machines, so please follow the [MongoDB Install Instructions](https://www.mongodb.com/docs/manual/installation/)

Our data collection process takes several days. To collect only a small amount of data, you can use the Jupyter Notebook `/data_collection/API/API-Scraping.ipynb`. To do so, please activate the conda environment, then run `jupyter lab` and navigate to the notebook using Jupyter Lab's file explorer.

To perform the full data collection, we used an SBATCH job. To run it, please navigate to `/data_collection/API` and run
```bash
sbatch APIScraper.sb
```
This will populate the MongoDB database with the collected data.

### Visualizations


