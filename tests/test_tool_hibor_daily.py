"""
Module for testing the HIBOR daily data tool functionality.

This module contains unit tests for fetching and processing HIBOR daily data.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime

from hkopenai.hk_finance_mcp_server.tools.hibor_daily import (
    _get_hibor_stats,
    register,
)


class TestHIBORDaily(unittest.TestCase):
    """
    Test class for verifying HIBOR daily data functionality.

    This class contains test cases to ensure the data fetching and processing
    for HIBOR daily data work as expected.
    """

    def test_get_hibor_stats(self):
        """
        Test the retrieval and filtering of HIBOR daily statistics.

        This test verifies that the function correctly fetches and filters data by date range,
        and handles error cases.
        """
        # Mock the JSON data
        mock_json_data = {
            "header": {"success": True},
            "result": {
                "records": [
                    {"end_of_day": "2023-01-01", "ir_overnight": 0.1, "ir_1m": 1.0},
                    {"end_of_day": "2023-01-02", "ir_overnight": 0.11, "ir_1m": 1.1},
                    {"end_of_day": "2023-02-01", "ir_overnight": 0.12, "ir_1m": 1.2},
                    {"end_of_day": "2024-01-01", "ir_overnight": 0.13, "ir_1m": 1.3},
                ]
            },
        }

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.hibor_daily.fetch_json_data"
        ) as mock_fetch_json_data:
            # Setup mock response for successful data fetching
            mock_fetch_json_data.return_value = mock_json_data

            # Test filtering by date range
            result = _get_hibor_stats(start_date="2023-01-01", end_date="2023-01-31")
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["date"], "2023-01-01")
            self.assertEqual(result[0]["overnight"], 0.1)

            # Test empty result for non-matching dates
            result = _get_hibor_stats(start_date="2025-01-01", end_date="2025-12-31")
            self.assertEqual(len(result), 0)

            # Test error handling when fetch_hibor_daily_data returns an error
            mock_fetch_json_data.return_value = {"error": "JSON fetch failed"}
            result = _get_hibor_stats(start_date="2023-01-01")
            self.assertEqual(result, {"error": "JSON fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_hibor_daily_stats tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_hibor_stats function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get daily figures of Hong Kong Interbank Interest Rates (HIBOR) from HKMA"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_hibor_daily_stats")

        # Call the decorated function and verify it calls _get_hibor_stats
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.hibor_daily._get_hibor_stats"
        ) as mock_get_hibor_stats:
            decorated_function(start_date="2023-01-01", end_date="2023-12-31")
            mock_get_hibor_stats.assert_called_once_with("2023-01-01", "2023-12-31")
