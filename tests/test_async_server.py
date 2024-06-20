import io
from ssl import SSLContext
import unittest
from unittest.mock import patch, AsyncMock, mock_open, MagicMock
from async_server import search_string_in_file, search_string_in_cached_file
from async_server import main


class TestAsyncServer(unittest.TestCase):
    """Test cases for the async server"""

    def setUp(self):
        """Setup method for the test cases"""
        self.query = "6;0;1;26;0;7;3;0;"  # sample query sent to the server
        self.file_content = (
            "6;0;1;26;0;7;3;0;\n25;0;23;16;0;19;3;0;\n"  # sample file content
        )

    @patch("async_server.main")
    async def test_config_loading(self, mock_main, mock_open):
        """Test cases for the configurations"""
        # Set up mock configuration values
        mock_open.return_value = io.StringIO(
            """
                                             linuxpath=./200k.txt
                                             use_ssl=False
                                             certfile=./ssl/algo.crt
                                             keyfile=./ssl/algo.key
                                             """
        )
        # Assertions

        # File read assertion
        await mock_open.assert_called_once_with(
            "config/config.cfg", "r", encoding="utf8"
        )

        # Mock server object (optional, for more control)
        mock_server = await mock_main.return_value

        # Server address assertion
        try:
            client_address = mock_server.getsockname()
            self.assertEqual(client_address[0], "127.0.0.1")  # localhost
            self.assertEqual(client_address[1], "8.8.8.8")  # port
        except (AttributeError, IndexError):
            self.fail("Error retrieving server address. Check server startup")

        # SSL Assertion
        if "use_ssl=True" in mock_open.return_value.getvalue():
            self.assertIsNotNone(SSLContext)  # Check if SSL context is created
        else:
            self.assertIsNone(SSLContext)

    @patch("aiofiles.open", new_callable=AsyncMock)
    async def test_search_string_in_file_exists(self, mock_aiofile):
        """Test case to test for a string in the file"""
        mock_file = AsyncMock()
        mock_file.__aenter__.return_value = mock_file
        mock_file.__aiter__.return_value = iter(self.file_content.splitlines())
        mock_aiofile.return_value = mock_file

        result = await search_string_in_file(self.query)
        self.assertEqual(result, "STRING EXISTS\n")

    @patch("aiofiles.open", new_callable=AsyncMock)
    async def test_search_string_in_file_not_exists(self, mock_aiofile):
        """Test case to test for a string not in the file"""
        mock_file = AsyncMock()
        mock_file.__aenter__.return_value = mock_file
        mock_file.__aiter__.return_value = iter(self.file_content.splitlines())
        mock_aiofile.return_value = mock_file

        result = await search_string_in_file(self.query)
        self.assertEqual(result, "STRING NOT FOUND\n")

    @patch("builtins.open", new_callable=mock_open)
    async def test_search_string_in_cached_file_exists(self, mock_file):
        """Test case to test for a string in the cached file"""
        global file_contents
        file_contents = self.file_content.splitlines()
        result = await search_string_in_cached_file(
            self.query, self.file_content
        )
        self.assertEqual(result, "STRING EXISTS\n")

    @patch("builtins.open", new_callable=mock_open)
    async def test_search_string_in_cached_file_not_exists(self, mock_file):
        """Test case to test for a string not in the cached file"""
        global file_contents
        file_contents = self.file_content.splitlines()
        result = await search_string_in_cached_file(
            "non_exist_string", self.file_content
        )
        self.assertEqual(result, "STRING NOT FOUND\n")

    @patch("asyncio.start_server")
    async def test_server_start(self, mock_start_server):
        mock_server = MagicMock()
        mock_start_server.return_value = mock_server
        await main()
        await mock_start_server.assert_called_once()


if __name__ == "__main__":
    unittest.main()
