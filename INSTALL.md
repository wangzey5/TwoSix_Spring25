# Installation Instructions

This project was primarily developed using [Michigan State University’s High-Performance Computing Center (HPCC)](https://icer.msu.edu/) . The following instructions outline how to reproduce the full workflow on the HPCC, including database setup, data collection, machine learning modeling, and visualization of results through model embeddings.

The project is located within the /mnt/research/TwoSix directory on the HPCC. Please ensure you are working within a space that provides sufficient storage capacity to accommodate the scraped data, MongoDB database, and trained models.

To begin, connect to the HPCC via [SSH](https://docs.icer.msu.edu/Connect_to_HPCC_System/), and follow the steps below for a complete setup and execution pipeline.

## MongoDB (Ethan writeup)

This project uses MongoDB version 3.6.8 installed manually on the HPCC. The instructions below guide you through installing the same version, starting the MongoDB server, and connecting to it for data operations. 

### Download and Install MongoDB v3.6.8
```
cd /mnt/research/TwoSix #Navigate to your working project directory
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.6.8.tgz
tar -xvzf mongodb-linux-x86_64-3.6.8.tgz
mv mongodb-linux-x86_64-3.6.8 mongodb
export PATH=/mnt/research/your_directory/mongodb/bin:$PATH
```
### Create Data and Log Directories
```
mkdir -p /mnt/research/your_directory/db
mkdir -p /mnt/research/your_directory/logs
```

### Starting and Connecting to the MongoDB Server
```
mongod --dbpath /mnt/research/your_directory/db --logpath /mnt/research/your_directory/logs/mongod.log --fork
mongo
```


## Mirrulations (Archisha or Emma writeup)

## Data Preprocessing and Cleaning (Archisha if needed)

## Model and Embedding Storage (Archan writeup)

## Visualizaiton (Archan or Archisha or Frank)

