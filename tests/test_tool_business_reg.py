"""
Module for testing the business registration tool functionality.

This module contains unit tests for fetching and processing business registration data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_finance_mcp_server.tools.business_reg import (
    _get_business_stats,
    register,
)


class TestBusinessRegistration(unittest.TestCase):
    """
    Test class for verifying business registration functionality.

    This class contains test cases to ensure the data fetching and processing
    for business registration data work as expected.
    """

    def test_get_business_stats(self):
        """
        Test the retrieval and filtering of business registration statistics.

        This test verifies that the function correctly fetches and filters data by year and month range,
        and handles error cases.
        """
        # Mock the CSV data
        mock_csv_data = [
            {
                "RUN_DATE": "202301",
                "ACTIVE_MAIN_BUS": "1000",
                "NEW_REG_MAIN_BUS": "100",
            },
            {
                "RUN_DATE": "202302",
                "ACTIVE_MAIN_BUS": "1050",
                "NEW_REG_MAIN_BUS": "110",
            },
            {
                "RUN_DATE": "202303",
                "ACTIVE_MAIN_BUS": "1100",
                "NEW_REG_MAIN_BUS": "120",
            },
            {
                "RUN_DATE": "202401",
                "ACTIVE_MAIN_BUS": "1200",
                "NEW_REG_MAIN_BUS": "130",
            },
        ]

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.business_reg.fetch_csv_from_url"
        ) as mock_fetch_csv_from_url:
            # Setup mock response for successful data fetching
            mock_fetch_csv_from_url.return_value = mock_csv_data

            # Test filtering by year range
            result = _get_business_stats(start_year=2023, end_year=2023)
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["year_month"], "2023-01")
            self.assertEqual(result[0]["active_business"], 1000)

            # Test filtering by year and month range
            result = _get_business_stats(
                start_year=2023, start_month=2, end_year=2023, end_month=2
            )
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["year_month"], "2023-02")

            # Test empty result for non-matching years
            result = _get_business_stats(start_year=2025, end_year=2025)
            self.assertEqual(len(result), 0)

            # Test error handling when fetch_csv_from_url returns an error
            mock_fetch_csv_from_url.return_value = {"error": "CSV fetch failed"}
            result = _get_business_stats(start_year=2023, end_year=2023)
            self.assertEqual(result, {"type": "Error", "error": "CSV fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_business_stats tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_business_stats function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get monthly statistics on the number of new business registrations in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_business_stats")

        # Call the decorated function and verify it calls _get_business_stats
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.business_reg._get_business_stats"
        ) as mock_get_business_stats:
            decorated_function(start_year=2023, end_year=2023)
            mock_get_business_stats.assert_called_once_with(2023, None, 2023, None)
