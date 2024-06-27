"""Performance Test script with REREAD_ON_QUERY boolean switch"""

import asyncio
import time
import random
import sys
from search_algorithm import linear_search, jump_search
from search_algorithm import binary_search, kmp_search
from search_algorithm import exponential_search


config_file_path = "config/config.cfg"
file_path = None

# Confirmation for file path to 200k.txt file
try:
    with open(config_file_path, "r", encoding="utf8") as file:
        for line in file:
            if line.startswith("linuxpath="):
                file_path = line.strip().split("=")[1]
except FileNotFoundError:
    print("Configuration file %s not found.", config_file_path)
    sys.exit(1)

if file_path is None:
    print("File path not found in the configuration file.")
    sys.exit(1)


async def measure_execution_time(search_fn, file_path, pattern, num_queries,
                                 reread_on_query, preloaded_text=None):
    """Function to measure the execution time"""
    NUM_RUNS = 5
    total_time = 0

    for _ in range(NUM_RUNS):
        start_time = time.perf_counter()
        for _ in range(num_queries):
            if reread_on_query:
                if file_path is None:
                    raise ValueError("File path unavailable for rereading")
                
                with open(file_path, 'r', encoding="utf8") as file:
                    lines = file.readlines()

                # Remove newline characters and any trailing whitespace
                lines = [line.strip() for line in lines]

                # Join lines to create a text block for searching
                text = "\n".join(lines)
            else:
                text = preloaded_text
            search_fn(text, pattern)
        end_time = time.perf_counter()
        total_time += end_time - start_time

    return total_time / NUM_RUNS  # Average execution time


async def main():
    """Main function of the program"""
    file_sizes = [10000, 50000, 100000, 500000, 1000000]
    num_queries_list = [1, 5, 10, 50, 100]
    reread_on_query = True  # Set this to True or False

    with open(file_path, 'r', encoding="utf8") as file:
        lines = file.readlines()

    # Remove newline characters and trailing whitespace
    lines = [line.strip() for line in lines]

    # Implemented search algorithms
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

        # Join lines to create a text block for searching
        preloaded_text = "\n".join(lines[:file_size])
        print(f"Testing with file size: {file_size}")

        for num_queries in num_queries_list:
            for name, search_fn in search_functions.items():
                # Select a random line as the pattern to search for
                pattern = random.choice(lines)

                avg_exec_time = await measure_execution_time(search_fn,
                                                             file_path,
                                                             pattern,
                                                             num_queries,
                                                             reread_on_query,
                                                             preloaded_text)

                print(f"Search: {name}, "
                      + f"File Size: {file_size}, "
                      + f"Number of Queries: {num_queries}, "
                      + f"Reread: {reread_on_query}, "
                      + f"Avg Execution Time: {avg_exec_time * 1000:.2f} ms")


if __name__ == "__main__":
    try:
        # Starts the server and the main coroutine until it completes
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle graceful shutdown with keyboard interrupt
        print("Server stopped by user")
