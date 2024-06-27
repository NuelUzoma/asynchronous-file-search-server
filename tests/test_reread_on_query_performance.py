"""Pytest module for the performance test and the search algorithms"""

import pytest
import asyncio
import search_algorithm
from reread_on_query_test import measure_execution_time


@pytest.mark.asyncio
async def test_linear_search_no_reread(mocker):
    """Test cases for linear search without rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "linear_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = False
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_linear_search_reread(mocker):
    """Test cases for linear search rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "linear_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = True
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_jump_search_no_reread(mocker):
    """Test cases for jump search without rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "jump_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = False
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_jump_search_reread(mocker):
    """Test cases for jump search rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "jump_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = True
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_binary_search_no_reread(mocker):
    """Test cases for binary search without rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "binary_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = False
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_binary_search_reread(mocker):
    """Test cases for binary search rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "binary_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = True
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_kmp_search_no_reread(mocker):
    """Test cases for kmp search without rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "kmp_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = False
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_kmp_search_reread(mocker):
    """Test cases for kmp search without rereading the file."""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "kmp_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = True
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_exponential_search_no_reread(mocker):
    """Test cases for exponential search without rereading the file"""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "exponential_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = False
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


@pytest.mark.asyncio
async def test_exponential_search_reread(mocker):
    """Test cases for exponential search without rereading the file"""

    # Mock search function
    mock_search_fn = mocker.patch.object(search_algorithm,
                                         "exponential_search",
                                         return_value=None)

    # Test Inputs
    text = "This is a test text"
    pattern = "test"
    num_queries = 5
    reread_on_query = True
    file_path = "./200k.txt"

    # Patch asyncio.sleep to avoid actual sleep during test execution
    mock_sleep = mocker.patch.object(asyncio, "sleep", return_value=None)

    average_time = await measure_execution_time(mock_search_fn, file_path,
                                                pattern, num_queries,
                                                reread_on_query, text)

    # Assertions
    assert mock_search_fn.call_count == num_queries * 5  # Due to num_of_runs
    assert mock_search_fn.called_with(text.split(), pattern)
    assert average_time > 0
    assert mock_sleep.call_count == 0


def test_search_functions(mocker):
    """Tests if all search functions are defined."""

    # Patch the actual execution of search functions (not called here)
    for search_name in [
        "linear_search",
        "jump_search",
        "binary_search",
        "kmp_search",
        "exponential_search",
    ]:
        mocker.patch.object(search_algorithm,
                            search_name,
                            mocker.AsyncMock())

    # Assert all search functions are defined in the module
    assert all(hasattr(search_algorithm, name)
               for name in [
                   "linear_search",
                   "jump_search",
                   "binary_search",
                   "kmp_search",
                   "exponential_search",
                ])


if __name__ == "__main__":
    pytest.main()
