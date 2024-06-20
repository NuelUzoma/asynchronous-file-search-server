"""Asynchronous server file that sends requests to the server
for concurrent tasks.
Efficient method of sending concurrent tasks to server
due to its async nature.
Traditionally, it is single-threaded but will be combined
with threading to support multithreading.
"""

import os
import sys
import asyncio
import ssl
from concurrent.futures import ThreadPoolExecutor
from asyncio import StreamReader, StreamWriter
import aiofiles
from dotenv import load_dotenv
from config.logging_config import get_logger


# Load values from environment files
load_dotenv()

host = os.getenv("HOST")  # host
port = os.getenv("PORT")  # host
reread_on_query = os.getenv("REREAD_ON_QUERY", "False").lower() == "true"

"""Logging configuration"""
logger = get_logger()

"""Load the path to the 200k.txt from the configuration file"""
config_file_path = "config/config.cfg"
search_file_path = None
use_ssl = False
certfile = None
keyfile = None

try:
    # Read the configuration file to get the path
    with open(config_file_path, "r", encoding="utf8") as config_file:
        for line in config_file:
            if line.startswith("linuxpath="):
                search_file_path = line.strip().split("=")[1]
            elif line.startswith("use_ssl="):
                use_ssl = line.strip().split("=")[1].lower() == "true"
            elif line.startswith("certfile="):
                certfile = line.strip().split("=")[1]
            elif line.startswith("keyfile="):
                keyfile = line.strip().split("=")[1]

    logger.debug("Extracted path from config: %s", search_file_path)

    # Log an error if file or file path doesnt exist
    if not search_file_path or not os.path.exists(search_file_path):
        logger.error(
            "Path to 200k.txt not found in %s or file does not exist.",
            config_file_path
        )
        sys.exit(1)
except FileNotFoundError:
    logger.error("Configuration file %s not found.", config_file_path)
    sys.exit(1)
except Exception as e:
    logger.error("An unexpected error occurred: %s", e)
    sys.exit(1)

# Cache the file contents if REREAD_ON_QUERY is False
file_contents = None

if not reread_on_query:
    try:
        with open(search_file_path, "r", encoding="utf8") as file:
            file_contents = file.readlines()
    except Exception as e:
        logger.error("Error reading the file: %s", e)
        exit(1)

# Thread pool executor for multithreading
executor = ThreadPoolExecutor(max_workers=10)


def search_string_in_cached_file(query: str, file_contents: str) -> str:
    """Search for the string in cached file contents"""
    try:
        for line in file_contents.splitlines():
            if line.strip() == query:
                return "STRING EXISTS\n"
        return "STRING NOT FOUND\n"
    except Exception as e:
        logger.error("Error searching cached file: %s", e)
        return "ERROR\n"


async def search_string_in_file(query: str) -> str:
    """Function to search string in 200k.txt file"""
    try:
        async with aiofiles.open(str(search_file_path), "r") as file:
            async for line in file:
                if line.strip() == query:
                    return "STRING EXISTS\n"
        return "STRING NOT FOUND\n"
    except Exception as e:
        logger.error("Error searching in file: %s", e)
        return "ERROR\n"


async def handle_client(reader: StreamReader, writer: StreamWriter) -> None:
    """Async function that will handle
    concurrent tasks to the client server"""
    try:
        while True:
            data = await reader.read(1024)  # Maximum payload of 1024 bytes
            if not data:
                # Discontinue program if maximum payload is exceeded
                break

            # Strip \x00 characters from the end of the payload
            stripped_data = data.rstrip(b"\x00")

            # Convert the raw bytes  from server to human readable format
            query: str = stripped_data.decode().strip()

            # Response from search of the text file
            if reread_on_query:
                response = await search_string_in_file(query)
            else:
                # Run the search in a seperate thread
                loop = asyncio.get_running_loop()  # Get current event loop
                response = await loop.run_in_executor(
                    executor, search_string_in_cached_file, query
                )

            logger.debug("Query: %s, Response: %s", query, response)

            encoded_response = response.encode()  # Encode the response

            # Write data to the stream
            writer.write(encoded_response)

            # Ensure subsequent operations occurs after data is transmitted
            await writer.drain()

    except asyncio.CancelledError:
        # Return error if an error occured while connecting to client server
        logger.error("Error occured while connecting to client server")

    except Exception as e:
        logger.error("An unexpected error happened: %s", e)

    finally:
        # Close the connection to client server
        writer.close()

        # Ensure connection is closed before proceeding with other operations
        await writer.wait_closed()


async def main() -> None:
    """Main function of the program"""
    try:
        ssl_context = None
        if use_ssl:
            ssl_context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            ssl_context.load_cert_chain(
                certfile=str(certfile), keyfile=str(keyfile)
            )

        # Start asyncio server amd handle client connections
        client_server = await asyncio.start_server(
            handle_client, host, port, ssl=ssl_context
        )

        # Retrieves the address the server listens for incoming connections
        client_address = client_server.sockets[0].getsockname()

        # Indicate server is listening for incoming connections
        logger.debug("Serving on %s", client_address)

        async with client_server:
            # Server is ready and active and should start serving forever
            await client_server.serve_forever()
    except FileNotFoundError:
        logger.error(
            "Kindly double-check the SSL files: %s, %s for errors",
            certfile, keyfile
        )
        sys.exit(1)
    except Exception as e:
        logger.error("An unexpected error occurred: %s", e)
        sys.exit(1)


if __name__ == "__main__":
    try:
        # Starts the server and the main coroutine until it completes
        asyncio.run(main())
    except KeyboardInterrupt:
        # Handle graceful shutdown with keyboard interrupt
        logger.info("Server stopped by user")
