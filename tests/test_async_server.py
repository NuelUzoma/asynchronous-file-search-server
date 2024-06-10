import unittest
import os
import asyncio
from unittest.mock import patch, AsyncMock, mock_open, MagicMock
from async_server import search_string_in_cached_file, search_string_in_file, main


class TestAsyncServer(unittest.TestCase):
    """Test cases for the async server"""

    def setUp(self):
        """Setup method for the test cases"""
        self.query = "6;0;1;26;0;7;3;0;"  # sample query to be sent to the server
        self.file_content = (
            "6;0;1;26;0;7;3;0;\n25;0;23;16;0;19;3;0;\n"  # sample file content
        )
        self.config_data = "linuxpath=./200k.txt\nuse_ssl=False\ncertfile=./ssl/algo.crt\nkeyfile=./ssl/algo.key\n"
        self.env_vars = {"HOST": "127.0.0.1", "PORT": "8888", "REREAD_ON_QUERY": "True"}

    @patch("builtins.open", new_callable=mock_open)
    def test_config_loading(self, mock_file):
        """Test cases for the configurations"""
        with patch.dict(os.environ, self.env_vars):
            from async_server import search_file_path, use_ssl, certfile, keyfile

            self.assertEqual(search_file_path, "./200k.txt")
            self.assertTrue(use_ssl)
            self.assertEqual(certfile, "./ssl/algo.crt")
            self.assertEqual(keyfile, "./ssl/algo.key")

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
    def test_search_string_in_cached_file_exists(self, mock_file):
        """Test case to test for a string in the cached file"""
        global file_contents
        file_contents = self.file_content.splitlines()
        result = search_string_in_cached_file(self.query)
        self.assertEqual(result, "STRING EXISTS\n")

    @patch("builtins.open", new_callable=mock_open)
    def test_search_string_in_cached_file_not_exists(self, mock_file):
        """Test case to test for a string not in the cached file"""
        global file_contents
        file_contents = self.file_content.splitlines()
        result = search_string_in_cached_file("non_existent_string")
        self.assertEqual(result, "STRING NOT FOUND\n")

    @patch("asyncio.start_server")
    async def test_server_start(self, mock_start_server):
        mock_server = MagicMock()
        mock_start_server.return_value = mock_server
        await main()
        await mock_start_server.assert_called_once()


if __name__ == "__main__":
    unittest.main()
