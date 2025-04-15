import pymongo
### to import copy and past the following into your file
# import sys
# sys.path.append("/mnt/research/TwoSix/CMSE-495/TwoSix_Spring25/mongo")
# from mongoUtils import mongoConnect
def mongoConnect(IPpath="/mnt/research/TwoSix/mongodb/IP.txt"):
    """Connect to the MongoDB server at the IP specified in the file at `path`
    """
    try:
        with open(IPpath, "r") as ipFile:
            ip = ipFile.read().strip()
            return pymongo.MongoClient(host=[ip])
    except:
        return pymongo.MongoClient()
