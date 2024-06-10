import unittest
import asyncio
import os
from unittest.mock import patch, mock_open, MagicMock
from client import tcp_client


class TestClientServer(unittest.TestCase):
    """Test cases for the client server"""

    def setUp(self):
        """Setup method for the test cases"""
        self.query = "6;0;1;26;0;7;3;0;"  # sample query to be sent to the server
        self.config_data = "use_ssl=False\ncertfile=./ssl/algo.crt\n"
        self.env_vars = {"HOST": "127.0.0.1", "PORT": "8888"}

    @patch("builtins.open", new_callable=mock_open)
    def test_ssl_config_loading(self, mock_file):
        with patch.dict(os.environ, self.env_vars):
            from client import use_ssl, certfile

            self.assertTrue(use_ssl)
            self.assertEqual(certfile, "./ssl/algo.crt")

    @patch("asyncio.open_connection")
    async def test_tcp_client(self, mock_open_connection):
        mock_reader = asyncio.StreamReader()
        mock_writer = MagicMock()
        mock_writer.write = MagicMock()
        mock_writer.drain = MagicMock()
        mock_writer.close = MagicMock()
        mock_writer.wait_closed = MagicMock()
        mock_open_connection.return_value = (mock_reader, mock_writer)

        # Simulate server response
        mock_reader.feed_data(b"STRING EXISTS\n")
        mock_reader.feed_eof()

        await tcp_client(self.query)
        mock_writer.write.assert_called_with(self.query.encode())


if __name__ == "__main__":
    unittest.main()
