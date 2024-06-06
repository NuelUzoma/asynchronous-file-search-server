"""Client server script that interacts with the asynchronous server
to test for concurrent connections"""
import asyncio
import os
from dotenv import load_dotenv
from config.logging_config import get_logger


"""Load values from environment files"""
load_dotenv()

"""Logging configuration"""
logger = get_logger()
host = os.getenv("HOST")
port = os.getenv("PORT")


async def tcp_client(query: str):
    try:
        """Function to test the async program for concurrent connections"""
    
        """Establish connection to the server"""
        reader, writer = await asyncio.open_connection(host, port)

        """Send message to the server"""
        logger.debug(f"Send: {query!r}")

        writer.write(query.encode()) # converts message to bytes before sending

        await writer.drain()

        data = await reader.read(1024) # Maximum payload of 1024 bytes

        encoded_data = data.decode()

        logger.debug(f'Recieved: {encoded_data}')
    
    except Exception as e:
        """Handle any error that occurs during execution"""
        logger.error(f'Error occured when running the server: {str(e)}')
    
    finally:
        """Close the connection to async server"""
        writer.close()

        """Ensure connection is closed before proceeding with other operations"""
        await writer.wait_closed()


if __name__ == "__main__":
    try:
        """Starts the server"""
        query = input("Enter the string to search: ")
        asyncio.run(tcp_client(query))
    except KeyboardInterrupt:
        """Handle graceful shutdown with keyboard interrupt"""
        logger.info('Server stopped by user')