"""Pytest module for the async_server module"""

import io
import pytest
import asyncio
from ssl import SSLContext
from async_server import search_string_in_file, search_in_cached_file, main


@pytest.fixture
def query():
    """Sample query sent to the server"""
    content = "6;0;1;26;0;7;3;0;"
    return content.strip()


@pytest.fixture
def file_content():
    """Sample file content"""
    content = "6;0;1;26;0;7;3;0;\n25;0;23;16;0;19;3;0;\n"
    return content.strip()


@pytest.fixture
def mock_file_content(mocker, file_content):
    """Mock fixture to act as a cache for file_contents"""
    mocked_content = mocker.patch("test_async_server.file_content",
                                  return_value=file_content)
    return mocked_content


@pytest.mark.asyncio
async def test_config_loading(mocker):
    """Test case to test the server configuration"""

    # Set up mock configuration values
    config_values = """linuxpath=./200k.txt
    use_ssl=True
    certfile=./ssl/algo.crt
    keyfile=./ssl/algo.key
    """

    mock_open = mocker.patch("builtins.open",
                             return_value=io.StringIO(config_values))

    # Mock server object
    mock_main = mocker.patch("async_server.main")
    mock_main.getsockname = mocker.AsyncMock(return_value=("127.0.0.1",
                                                           "8888"))

    # Server address assertion
    try:
        client_address = await mock_main.getsockname()
        assert client_address[0] == "127.0.0.1"  # localhost
        assert client_address[1] == "8888"  # port
    except (AttributeError, IndexError):
        pytest.fail("Error retrieving server address. Check server startup")

    # SSL Assertion
    if "use_ssl=True" in mock_open.return_value.getvalue():
        # Check if SSL context is created
        assert SSLContext is not None
    else:
        assert SSLContext is None


@pytest.mark.asyncio
async def test_search_string_in_file_exists(mocker, query, file_content):
    """Test case to check if the string exists in file"""
    mock_file = mocker.AsyncMock()
    mock_file.__aenter__.return_value = mock_file
    mock_file.__aiter__.return_value = iter(file_content.splitlines())
    mocker.patch("aiofiles.open", return_value=mock_file)

    result = await search_string_in_file(query)
    assert result == "STRING EXISTS\n"


@pytest.mark.asyncio
async def test_search_string_in_file_not_exists(mocker, file_content):
    """Test case to check if the string not exists in file"""
    mock_file = mocker.AsyncMock()
    mock_file.__aenter__.return_value = mock_file
    mock_file.__aiter__.return_value = iter(file_content.splitlines())
    mocker.patch("aiofiles.open", return_value=mock_file)

    result = await search_string_in_file("fake_string")
    assert result == "STRING NOT FOUND\n"


@pytest.mark.asyncio
async def test_search_string_in_file_empty_query(mocker, file_content):
    """Test case to check for an empty query in file"""
    mock_file = mocker.AsyncMock()
    mock_file.__aenter__.return_value = mock_file
    mock_file.__aiter__.return_value = iter(file_content.splitlines())
    mocker.patch("aiofiles.open", return_value=mock_file)

    empty_query = ''
    result = await search_string_in_file(empty_query)
    assert result == "STRING NOT FOUND\n"


def test_search_string_in_cached_file_exists(query, mock_file_content):
    """Test case to check if the string exists in cached file"""
    result = search_in_cached_file(query)
    assert result == "STRING EXISTS\n"


def test_search_string_in_cached_file_not_exists(mock_file_content):
    """Test case to check if the string not exists in cached file"""
    result = search_in_cached_file("non_exist_string")
    assert result == "STRING NOT FOUND\n"


def test_search_in_cached_file_empty_query(mock_file_content):
    """Test case to check for an empty query in file"""
    empty_query = ''
    result = search_in_cached_file(empty_query)
    assert result == "STRING NOT FOUND\n"


@pytest.mark.asyncio
async def test_server_start(mocker):
    """Test case to check if the server has started"""
    mock_server = mocker.AsyncMock()
    mocker.patch("asyncio.start_server", return_value=mock_server)
    await main()
    asyncio.start_server.assert_called_once()


if __name__ == "__main__":
    pytest.main()
