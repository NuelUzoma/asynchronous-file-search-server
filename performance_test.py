"""Performance test for the TCP client."""

import asyncio
import time
from client import tcp_client


async def measure_execution_time(file_size: int,
                                 query: str,
                                 num_queries: int):
    """Function to measure the execution time"""
    start_time = time.time()
    tasks = []
    for _ in range(num_queries):
        tasks.append(tcp_client(query))
    await asyncio.gather(*tasks)
    end_time = time.time()
    execution_time = end_time - start_time
    return execution_time


async def main():
    """Main function of the program"""
    file_sizes = [10000, 50000, 100000, 500000, 1000000]
    num_queries_list = [10, 50, 100, 500, 1000]
    query = "test_string"

    for file_size in file_sizes:
        print(f"Testing with file size: {file_size}")
        for num_queries in num_queries_list:
            exec_time = await measure_execution_time(file_size, query, num_queries)
            print(
                f"File Size: {file_size}, Number of Queries: {num_queries}, Execution Time: {exec_time:.2f} seconds"
            )


if __name__ == "__main__":
    asyncio.run(main())
