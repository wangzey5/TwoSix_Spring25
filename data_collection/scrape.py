"""
Script that uses the functions defined in `mirrulations.py` to scrape
"""

import multiprocessing as mp
import argparse
from time import perf_counter

from mirrulations import getDockets, storeDocketInfo

parser = argparse.ArgumentParser()
parser.add_argument(
    "--nthreads",
    default=4,
    type=int,
    help="The number of threads to spawn for parallelization"
)
parser.add_argument(
    "--time",
    action="store_true",
    help="Time how long it takes to get the list of dockets"
)
parser.add_argument(
    "--agency",
    default=None,
    action="append",
    help="The ID of an agency to get documents for. Can be used multiple times"
)

args=parser.parse_args()

# Get a list of missing dockets
start = perf_counter()
dockets = getDockets(args.agency)
stop = perf_counter()

if args.time:
    print(f"Got Documents in {stop - start} seconds")

# Download all missing dockets in parallel
with mp.Pool(args.nthreads) as pool:
    pool.map(storeDocketInfo, dockets)
