import multiprocessing as mp
import argparse

from mirrulations import getDockets, storeDocketInfo

parser = argparse.ArgumentParser()
parser.add_argument(
    "--nthreads",
    default=4,
    type=int,
    help="The number of threads to spawn for parallelization"
)

with mp.Pool(4) as pool:
    pool.map(storeDocketInfo, getDockets())
