"""Client server script that interacts with the asynchronous server
to test for concurrent connections"""

import asyncio
import os
import sys
import ssl
from dotenv import load_dotenv
from config.logging_config import get_logger


# Load values from environment files
load_dotenv()

# Logging configuration
logger = get_logger()
host = os.getenv("HOST")
port = os.getenv("PORT")
use_ssl = False
certfile = None

config_file_path = "config/config.cfg"

try:
    with open(config_file_path, "r", encoding="utf8") as config_file:
        for line in config_file:
            if line.startswith("use_ssl="):
                use_ssl = line.strip().split("=")[1].lower() == "true"
            elif line.startswith("certfile="):
                certfile = line.strip().split("=")[1]
except Exception as e:
    logger.error("Error loading SSL configuration: %s", e)
    sys.exit(1)


async def tcp_client(query: str, file_size: int):
    """TCP Client Server Function"""
    writer = None
    try:
        # Function to test the async program for concurrent connections

        ssl_context = None
        if use_ssl:
            ssl_context = ssl.create_default_context(
                ssl.Purpose.SERVER_AUTH, cafile=certfile
            )

        # Establish connection to the server
        reader, writer = await asyncio.open_connection(
            host, port, ssl=ssl_context
        )

        # Send message to the server
        logger.debug("Send: %s", query)

        # Potentially modify query based on file size
        if file_size > 100000:  # Example: Adjust query for larger files
            modified_query = f"{query} with file size {file_size}"
        else:
            modified_query = query

        # Convert message to bytes before sending
        writer.write(modified_query.encode())

        await writer.drain()

        data = await reader.read(1024)  # Maximum payload of 1024 bytes

        encoded_data = data.decode()

        logger.debug("Recieved: %s", encoded_data)

    except Exception as e:
        # Handle any error that occurs during execution
        logger.error("Error occured when running the server: %s", e)

    finally:
        if writer is not None:
            # Close the connection to async server
            writer.close()

            # Ensure connection is closed before proceeding with operations
            await writer.wait_closed()


if __name__ == "__main__":
    try:
        # Starts the server
        query = input("Enter the string to search: ")

        # Get user input for file size
        while True:
            file_size_str = input("Enter the file size (maximum 1000000): ")
            try:
                file_size = int(file_size_str)
                if file_size <= 0 or file_size > 1000000:
                    logger.debug("Please enter a value between 1 and 1000000")
                    continue
                break
            except ValueError:
                logger.error("Invalid input. Please enter a valid integer.")
        asyncio.run(tcp_client(query, file_size))
    except KeyboardInterrupt:
        # Handle graceful shutdown with keyboard interrupt
        logger.info("Server stopped by user")
