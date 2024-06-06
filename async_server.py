"""Asynchronous server file that sends requests to the server for concurrent tasks
Efficient method of sending concurrent tasks to server dut to its async nature
Traditionally, it is single-threaded but will be combined with threading to support
multithreading.
"""
import os
import asyncio
import aiofiles
from asyncio import StreamReader, StreamWriter
from dotenv import load_dotenv
from config.logging_config import get_logger


"""Load values from environment files"""
load_dotenv()

host = os.getenv("HOST")
port = os.getenv("PORT")

"""Logging configuration"""
logger = get_logger()

"""Load the path to the 200k.txt from the configuration file"""
config_file_path = 'config/config.cfg'
search_file_path = None

try:
    """Read the configuration file to get the path"""
    with open(config_file_path, 'r') as config_file:
        for line in config_file:
            if line.startswith('linuxpath='):
                search_file_path = line.strip().split('=')[1]
                break

    logger.debug(f"Extracted path from config: {search_file_path}")

    """Log an error if file or file path doesnt exist"""
    if not search_file_path or not os.path.exists(search_file_path):
        logger.error(f"Path to 200k.txt not found in {config_file_path} or file does not exist.")
        exit(1)
except FileNotFoundError:
    logger.error(f"Configuration file {config_file_path} not found.")
    exit(1)
except Exception as e:
    logger.error(f"An unexpected error occurred: {e}")
    exit(1)


async def search_string_in_file(query: str) -> str:
    """Function to search string in 200k.txt file"""
    try:
        async with aiofiles.open(search_file_path, 'r') as file:
            async for line in file:
                if line.strip() == query:
                    return "STRING EXISTS\n"
        return "STRING NOT FOUND\n"
    except Exception as e:
        logger.error(f"Error searching in file: {str(e)}")
        return "ERROR\n"


async def handle_client(reader: StreamReader, writer: StreamWriter) -> None:
    """Async function that will handle concurrent tasks to the client server"""
    try:
        while True:
            data = await reader.read(1024) # Maximum payload of 1024 bytes
            if not data:
                """Discontinue program if maximum payload is exceeded"""
                break

            """Strip \x00 characters from the end of the payload"""
            stripped_data = data.rstrip(b'\x00')

            """Convert the raw bytes  from server to human readable format"""
            query: str = stripped_data.decode().strip()

            """Response from search of the text file"""
            response = await search_string_in_file(query)

            logger.debug(f"Query: {query!r}, Response: {response}")

            encoded_response = response.encode() # Encode the response

            """Write data to the stream"""
            writer.write(encoded_response)

            """Ensures subsequent operations occur only after data is transmitted"""
            await writer.drain()
    
    except asyncio.CancelledError:
        """Return an error if an error occured while connecting to client server"""
        logger.error("Error occured while connecting to client server")

    except Exception as e:
        logger.error(f"An unexpected error happened: {e}")
    
    finally:
        """Close the connection to client server"""
        writer.close()

        """Ensure connection is closed before proceeding with other operations"""
        await writer.wait_closed()


async def main() -> None:
    """Start asyncio server amd handle client connections"""
    client_server = await asyncio.start_server(handle_client, host, port)

    """Retrieves the address on which the server is listening
    for incoming connections"""
    client_address = client_server.sockets[0].getsockname() # first socket object

    """Indicate server is listening for incoming connections"""
    logger.debug(f"Serving on {client_address}")

    async with client_server:
        """Server is ready and active and should start serving forever"""
        await client_server.serve_forever()


if __name__ == "__main__":
    try:
        """Starts the server and the main coroutine until it completes"""
        asyncio.run(main())
    except KeyboardInterrupt:
        """Handle graceful shutdown with keyboard interrupt"""
        logger.info('Server stopped by user')