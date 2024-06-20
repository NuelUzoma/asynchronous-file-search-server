import unittest
from unittest.mock import patch, AsyncMock
from performance_test import measure_execution_time, main


class TestPerformance(unittest.TestCase):
    """Test cases for the performance speed"""

    @patch('asyncio.run')
    async def test_measure_execution_time(self, mock_run):
        """Test case for measuring the execution time"""
        mock_tcp_client = AsyncMock()

        # Simulate successful execution
        mock_run.return_value = mock_tcp_client

        # Call measure_execution_time with mocked function
        avg_time = await measure_execution_time(100, "test_query", 2)

        # Assertions

        # Verify tcp_client called twice
        self.assertEqual(mock_tcp_client.call_count, 2)

        # Ensure positive average time
        self.assertGreater(avg_time, 0)

        # Test with empty data or query
        with self.assertRaises(ValueError):
            await measure_execution_time(0, "", 2)

    @patch('asyncio.run')
    async def test_main(self, mock_run):
        """Test case to test the main function"""
        mock_tcp_client = AsyncMock()

        # Simulate successful execution
        mock_run.return_value = mock_tcp_client

        await main()

        # Assertions

        # Verify main function called
        mock_run.call_args[0][0].__name__

        # Ensure main is called at least once
        self.assertGreaterEqual(mock_run.call_count, 1)

        # Sample file sizes and list of queries
        file_sizes = [10000, 50000, 100000, 500000, 1000000]
        num_queries_list = [10, 50, 100, 500, 1000]

        # Ensures main uses set filesize and queries list
        first_call_args = mock_run.call_args_list[0][0]
        self.assertEqual(first_call_args[0], file_sizes)
        self.assertEqual(first_call_args[1], num_queries_list)


if __name__ == "__main__":
    unittest.main()
