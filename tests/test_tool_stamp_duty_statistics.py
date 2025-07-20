"""
Module for testing the stamp duty statistics tool functionality.

This module contains unit tests for fetching and processing stamp duty statistics data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_finance_mcp_server.tools.stamp_duty_statistics import (
    _get_stamp_duty_statistics,
    register,
)


class TestStampDutyStatistics(unittest.TestCase):
    """
    Test class for verifying stamp duty statistics functionality.

    This class contains test cases to ensure the data fetching and processing
    for stamp duty statistics data work as expected.
    """

    def test_get_stamp_duty_statistics(self):
        """
        Test the retrieval and filtering of stamp duty statistics.

        This test verifies that the function correctly fetches and filters data by period range,
        and handles error cases.
        """
        # Mock the CSV data
        mock_csv_data = [
            {"Period": "202301", "SD_Listed": "100.0", "SD_Unlisted": "50.0"},
            {"Period": "202302", "SD_Listed": "110.0", "SD_Unlisted": "55.0"},
            {"Period": "202303", "SD_Listed": "120.0", "SD_Unlisted": "60.0"},
            {"Period": "202401", "SD_Listed": "130.0", "SD_Unlisted": "65.0"},
        ]

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.stamp_duty_statistics.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            # Setup mock response for successful data fetching
            mock_fetch_csv_from_url.return_value = mock_csv_data

            # Test filtering by period range
            result = _get_stamp_duty_statistics(
                start_period="202301", end_period="202302"
            )
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["period"], "202301")
            self.assertEqual(result[0]["sd_listed"], 100.0)

            # Test empty result for non-matching periods
            result = _get_stamp_duty_statistics(
                start_period="202501", end_period="202512"
            )
            self.assertEqual(len(result), 0)

            # Test error handling when fetch_csv_from_url returns an error
            mock_fetch_csv_from_url.return_value = {"error": "CSV fetch failed"}
            result = _get_stamp_duty_statistics(start_period="202301")
            self.assertEqual(result, {"error": "CSV fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_stamp_duty_statistics tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_stamp_duty_statistics function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="""Get monthly statistics on stamp duty collected from transfer of Hong Kong stock (both listed and unlisted)"""
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_stamp_duty_statistics")

        # Call the decorated function and verify it calls _get_stamp_duty_statistics
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.stamp_duty_statistics._get_stamp_duty_statistics"
        ) as mock_get_stamp_duty_statistics:
            decorated_function(start_period="202301", end_period="202312")
            mock_get_stamp_duty_statistics.assert_called_once_with("202301", "202312")
