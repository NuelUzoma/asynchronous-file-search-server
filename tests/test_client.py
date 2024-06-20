import unittest
import asyncio
from unittest.mock import patch, MagicMock
from client import tcp_client


class TestClientServer(unittest.TestCase):
    """Test cases for the client server"""

    def setUp(self):
        """Setup method for the test cases"""
        self.query = "6;0;1;26;0;7;3;0;"  # sample query sent to the server
        self.config_data = "use_ssl=False\ncertfile=./ssl/algo.crt\n"
        self.env_vars = {"HOST": "127.0.0.1", "PORT": "8888"}

    @patch("client.use_ssl")
    @patch("client.certfile")
    def test_ssl_config_loading(self, mock_use_ssl, mock_certfile):
        """Test cases for SSL configuration (independent)"""
        # Parse configuration data
        config_dict = dict(
            line.strip().split("=") for line in self.config_data.splitlines())

        # Set mock behavior based on parsed data
        mock_use_ssl.return_value = config_dict.get(
            "use_ssl", False).lower() in ("true", "on", "1")

        mock_certfile.return_value = config_dict.get("certfile",
                                                     "./default.crt")

        self.assertFalse(mock_use_ssl.called)
        self.assertEqual(mock_certfile.return_value,
                         config_dict.get("certfile"))

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
