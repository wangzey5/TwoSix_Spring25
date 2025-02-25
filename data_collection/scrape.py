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
    help="specify the MongoDB collection name to target, if empty use the defaults ('comments' for metadata, 'commentDetails' for details)"
)
parser.add_argument(
    "--sourceCollection",
    default="comments",
    help="specify the MongoDB collection name to gather comments from if in 'details' mode"
)
parser.add_argument(
    "--apikey",
    default=None,
    help="specify the regulations.gov API Key to be used, if empty, use the default (Emma's')"
)

args = parser.parse_args()

client = pymongo.MongoClient()
db = client[args.db]
if args.targetCollection is None:
    if args.mode == "meta":
        collection = db.comments
    elif args.mode == "details":
        collection = db.commentDetails
    else:
        raise RuntimeError(f"Mode {args.mode} must be one of ['meta', 'details']")
else:
    collection = db[args.col]

if args.apikey is None:
    api = RegAPI(page_size=250)
else:
    api = RegAPI(page_size=250, apikey=args.apikey)

if args.mode == "meta":
    getAllComments(api.endpoint("/comments"), collection)
elif args.mode == "details":
    scraper = APICommentDetailScraper(api)
    comments = [comment for comment in db[args.sourceCollection].find()]
    getCommentDetails(scraper, comments, collection)
