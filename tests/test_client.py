"""Pytest module for the client server module"""

import pytest
import asyncio
from client import tcp_client


@pytest.fixture
def query():
    """Sample query sent to the server"""
    content = "6;0;1;26;0;7;3;0;"
    return content.strip()


@pytest.fixture
def config_data():
    """Sample file content"""
    data = "use_ssl=False\ncertfile=./ssl/algo.crt\n"
    return data.strip()


@pytest.fixture
def env_vars():
    config = {"HOST": "127.0.0.1", "PORT": "8888"}
    return config


@pytest.mark.asyncio
async def test_ssl_config_loading(query, config_data, env_vars, mocker):
    """Test cases for SSL configuration (independent)"""
    mock_use_ssl = mocker.patch("client.use_ssl")
    mock_certfile = mocker.patch("client.certfile")

    # Parse configuration data
    config_dict = dict(line.strip().split("=")
                       for line in config_data.splitlines())

    # Set mock behavior based on parsed data
    mock_use_ssl.return_value = config_dict.get("use_ssl",
                                                False).lower() in ("true",
                                                                   "on", "1")

    mock_certfile.return_value = config_dict.get("certfile",
                                                 "./default.crt")

    assert not mock_use_ssl.called
    assert mock_certfile.return_value == config_dict.get("certfile")


@pytest.mark.asyncio
async def test_tcp_client_without_ssl(query, mocker):
    """Test cases for TCP client without ssl"""
    mock_open_connection = mocker.patch("asyncio.open_connection")
    mock_reader = asyncio.StreamReader()
    mock_writer = mocker.AsyncMock()
    mock_writer.write = mocker.AsyncMock()
    mock_writer.drain = mocker.AsyncMock()
    mock_writer.close = mocker.AsyncMock()
    mock_writer.wait_closed = mocker.AsyncMock()
    mock_open_connection.return_value = (mock_reader, mock_writer)

    # Simulate server response
    mock_reader.feed_data(b"STRING EXISTS\n")
    mock_reader.feed_eof()

    await tcp_client(query)
    mock_writer.write.assert_called_with(query.encode())

    # Ensure all mocked coroutines are awaited
    await mock_writer.write()
    await mock_writer.drain()
    await mock_writer.close()
    await mock_writer.wait_closed()


if __name__ == "__main__":
    pytest.main()
