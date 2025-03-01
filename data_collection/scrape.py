"""
Entry script for scraping. To view help run `python scrape.py --help`
"""

import argparse
from concurrent.futures import ProcessPoolExecutor, wait

import pymongo
import numpy as np

from CommentScraper import getAllComments, getCommentDetails, APICommentDetailScraper, PWCommentDetailScraper
from RegAPI import RegAPI

parser = argparse.ArgumentParser()
parser.add_argument(
    "mode",
    choices=["meta", "details"],
    help="choose whether to scrape the meta-data of comments or their details"
)
parser.add_argument(
    "--db",
    default="regulationsgov",
    help="specify the MongoDB database name"
)
parser.add_argument(
    "--targetCollection",
    default=None,
    help="specify the MongoDB collection name to target, if empty use the defaults ('comments' for metadata, 'details' for details)"
)
parser.add_argument(
    "--sourceCollection",
    default="comments",
    help="specify the MongoDB collection name to gather comments from if in 'details' mode"
)
parser.add_argument(
    "--checkpointCollection",
    default="checkpoints",
    help="specify the MongoDB collection name to gather comments from if in 'details' mode"
)
parser.add_argument(
    "--apikey",
    default=None, action="append",
    help="specify the regulations.gov API Key to be used. Can be called multiple times to append new keys. If empty, use the default (Emma's key)"
)
parser.add_argument(
    "--apikeyFile",
    default=None,
    help="specify the path to a file containing the regulations.gov API Keys to be used."
)

class Setup:
    def __init__(self, args):
        self.args = args

    def db(self, client):
        return client[self.args.db]

    def targetCollection(self, client):
        db = client[self.args.db]
        if self.args.targetCollection is None:
            if self.args.mode == "meta":
                target_collection = db.comments
            elif self.args.mode == "details":
                target_collection = db.commentDetails
            else:
                raise RuntimeError(f"Mode {self.args.mode} must be one of ['meta', 'details']")
        else:
            target_collection = db[self.args.targetCollection]
        return target_collection

    def APIKeys(self):
        apikeys = []
        if self.args.apikeyFile is not None:
            with open(self.args.apikeyFile, "r") as keyfile:
                apikeys = [key.strip() for key in keyfile]
        if self.args.apikey is not None:
            for key in self.args.apikey:
                apikeys.append(key)
        return apikeys

    def API(self, apikeys):
        if self.args.apikey is None and self.args.apikeyFile is None:
            api = RegAPI(page_size=250)
        else:
            api = RegAPI(page_size=250, apikeys=apikeys)
        return api

args = parser.parse_args()
setup = Setup(args)
global_client = pymongo.MongoClient() 
db = setup.db(global_client)

def getCommentDetailsProcess(comment_list, api_key):
    api = setup.API([api_key])
    scraper = APICommentDetailScraper(api, parseAttachments=False)
    target_collection = setup.targetCollection(pymongo.MongoClient())
    getCommentDetails(
        scraper,
        comment_list,
        target_collection
    )

# Start scrapers
if args.mode == "meta":
    api = setup.API(setup.APIKeys())
    checkpoint_collection = db[args.checkpointCollection]
    getAllComments(
        api.endpoint("/comments"),
        setup.targetCollection(global_client),
        checkpoint_collection
    )
elif args.mode == "details":
    source = db[args.sourceCollection]

    highest = source.find().sort({ "_idx": -1 }).limit(1).next()["_idx"]
    try:
        lowest = setup.targetCollection(global_client).find().sort({ "_idx": -1 }).limit(1).next()["_idx"]
    except StopIteration:
        lowest = 0

    apikeys = setup.APIKeys()

    all_comments = [comment for comment in db[args.sourceCollection].find({"_idx": {"$gte": lowest, "$lte": highest }})]
    comment_lists = np.array_split(np.array(all_comments), len(apikeys))

    with ProcessPoolExecutor() as exec:
        fs = exec.map(getCommentDetailsProcess, comment_lists, apikeys)
        exec.shutdown(wait=True)
