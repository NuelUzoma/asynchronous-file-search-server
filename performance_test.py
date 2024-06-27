"""Performance test for 5 different search algorithms.

Linear Search, Jump Search, Binary Search
KMP Search and Exponential Search
Defaults to REREAD_ON_QUERY = FALSE for this algorithm test
"""

import asyncio
import sys
import time
import random
from search_algorithm import linear_search, jump_search, binary_search
from search_algorithm import kmp_search, exponential_search


config_file_path = "config/config.cfg"
file_path = None
NUM_RUNS = 5  # Number of times to run each test for averaging


async def measure_execution_time(search_fn, arr, num_queries: int):
    """Function to measure the execution time"""
    total_time = 0

    for _ in range(NUM_RUNS):
        start_time = time.perf_counter()

        for _ in range(num_queries):
            target = random.choice(arr)
            search_fn(arr, target)

        end_time = time.perf_counter()
        total_time += end_time - start_time

    return total_time / NUM_RUNS  # Average execution time


async def main():
    """Main function of the program"""

    # Confirmation for file path to 200k.txt file
    try:
        with open(config_file_path, "r", encoding="utf8") as file:
            for line in file:
                if line.startswith("linuxpath="):
                    file_path = line.strip().split("=")[1]
    except FileNotFoundError:
        print("Configuration file %s not found.", config_file_path)
        sys.exit(1)

    file_sizes = [10000, 50000, 100000, 500000, 1000000]
    num_queries_list = [1, 5, 10, 50, 100]

    with open(file_path, "r", encoding="utf8") as file:
        lines = file.readlines()

    # Remove newline characters and any leading/trailing whitespace
    lines = [line.strip() for line in lines]

    search_functions = {
        "Linear Search": linear_search,
        "Jump Search": jump_search,
        "Binary Search": binary_search,
        "KMP Search": kmp_search,
        "Exponential Search": exponential_search,
    }

    for file_size in file_sizes:
        # Check if the file size exceeds the 200k.txt file lines
        if file_size > len(lines):
            print(f"File size {file_size} is larger than the number of lines")
            continue

        # Get portion of the file corresponding to the required size
        arr = lines[:file_size]
        print(f"Testing with file size: {file_size}")

        for num_queries in num_queries_list:
            for name, search_fn in search_functions.items():
                avg_exec_time = await measure_execution_time(search_fn,
                                                             arr, num_queries)
                print(f"Search: {name}, "
                      + f"File size: {file_size}, "
                      + f"Number of Queries: {num_queries}, "
                      + f"Avg Execution Time: {avg_exec_time * 1000:.2f} ms")


if __name__ == "__main__":
    try:
        # Starts the server and the main coroutine until it completes
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle graceful shutdown with keyboard interrupt
        print("Server stopped by user")
