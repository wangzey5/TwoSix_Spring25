import argparse

import pymongo

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

args = parser.parse_args()

# DB setup
client = pymongo.MongoClient()
db = client[args.db]
if args.targetCollection is None:
    if args.mode == "meta":
        target_collection = db.comments
    elif args.mode == "details":
        target_collection = db.details
    else:
        raise RuntimeError(f"Mode {args.mode} must be one of ['meta', 'details']")
else:
    target_collection = db[args.targetCollection]

# API setup
apikeys = []
if args.apikeyFile is not None:
    with open(args.apikeyFile, "r") as keyfile:
        apikeys = [key for key in keyfile]
if args.apikey is not None:
    for key in args.apikey:
        apikeys.append(key)


if args.apikey is None and args.apikeyFile is None:
    api = RegAPI(page_size=250)
else:
    api = RegAPI(page_size=250, apikeys=apikeys)

# Start scrapers
if args.mode == "meta":
    checkpoint_collection = db[args.checkpointCollection]
    getAllComments(api.endpoint("/comments"), target_collection, checkpoint_collection)
elif args.mode == "details":
    scraper = APICommentDetailScraper(api)
    comments = [comment for comment in db[args.sourceCollection].find()]
    getCommentDetails(scraper, comments, target_collection)
