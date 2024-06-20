"""Performance test for the TCP client."""

import asyncio
import time
from client import tcp_client


NUM_RUNS = 5  # Number of times to run each test for averaging


async def measure_execution_time(file_size: int, query: str, num_queries: int):
    """Function to measure the execution time (averaged over multiple runs)"""
    total_time = 0
    for _ in range(NUM_RUNS):
        start_time = time.perf_counter()
        tasks = []

        for _ in range(num_queries):
            # Pass file size to client
            tasks.append(tcp_client(query, file_size))

        await asyncio.gather(*tasks)
        end_time = time.perf_counter()
        total_time += end_time - start_time
    return total_time / NUM_RUNS  # Average execution time


async def main():
    """Main function of the program"""
    file_sizes = [10000, 50000, 100000, 500000, 1000000]
    num_queries_list = [1, 5, 10, 50, 100]
    query = "Starting Speed Test..."

    for file_size in file_sizes:
        print(f"Testing with file size: {file_size}")
        for num_queries in num_queries_list:
            avg_exec_time = await measure_execution_time(
                file_size, query, num_queries
            )
            print(
                f"File Size: {file_size},"
                + f"Number of Queries: {num_queries},"
                + f"Average Execution Time: {avg_exec_time:.2f} seconds"
            )


if __name__ == "__main__":
    asyncio.run(main())
