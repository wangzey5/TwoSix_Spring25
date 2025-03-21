import pymongo

def mongoConnect(IPpath="/mnt/research/TwoSix/mongodb/IP.txt"):
    try:
        with open(IPpath, "r") as ipFile:
            ip = ipFile.read()
            return pymongo.MongoClient(host=[ip])
    except:
        return pymongo.MongoClient()
