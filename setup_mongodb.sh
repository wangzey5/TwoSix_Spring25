#!/bin/bash

# Navigate to working directory
echo "Downloading and setting up MongoDB 3.6.8..."
wget https://fastdl.mongodb.org/linux/mongodb-linux-x86_64-3.6.8.tgz
tar -xvzf mongodb-linux-x86_64-3.6.8.tgz
mv mongodb-linux-x86_64-3.6.8 mongodb

# Update PATH
export PATH=$PWD/mongodb/bin:$PATH

# Create data and log directories
mkdir -p data
mkdir -p log

# Start MongoDB
echo "Starting MongoDB server..."
mongod --dbpath ./data --logpath ./log/mongod.log --fork

# Connect to MongoDB shell
mongo
