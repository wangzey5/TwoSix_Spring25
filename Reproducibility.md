# Installation Instructions - Demo

## Git Repo

Install this repo using
```bash
git clone https://github.com/wangzey5/TwoSix_Spring25.git
```

## Environment Setup

We used [Anaconda](https://www.anaconda.com/) for environment management, please download and install it if it is not already installed.

Our repo includes an `environment.yml` file. To create a new environment using this file navigate to the base directory of our repo and run
```bash
conda env create --file environment.yml
```

##### Pre-runtime setup

Before running *any* of the following code, ensure that the conda environment is activated and you have a MongoDB server running locally.

To activate the environment run
```bash
conda activate CMSE495-TwoSix
```

## Data Collection


Our data is collected using [Mirrulations](https://github.com/MoravianUniversity/mirrulations). However, for simplicity purposes, the [demo.ipynb](https://github.com/wangzey5/TwoSix_Spring25/blob/main/demo.ipynb) utilizes sample data collected. For more comprehensive instructions on replicating the full end to end project, see [INSTALL.md](https://github.com/wangzey5/TwoSix_Spring25/blob/main/INSTALL.md). 



