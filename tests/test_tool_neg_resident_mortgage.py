"""
Module for testing the negative equity residential mortgage tool functionality.

This module contains unit tests for fetching and processing negative equity residential mortgage data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_finance_mcp_server.tools.neg_resident_mortgage import (
    _get_neg_equity_stats,
    register,
)


class TestNegEquityResidentialMortgage(unittest.TestCase):
    """
    Test class for verifying negative equity residential mortgage functionality.

    This class contains test cases to ensure the data fetching and processing
    for negative equity residential mortgage data work as expected.
    """

    def test_get_neg_equity_stats(self):
        """
        Test the retrieval and filtering of negative equity residential mortgage statistics.

        This test verifies that the function correctly fetches and filters data by year and month range,
        and handles error cases.
        """
        # Mock the JSON data
        mock_json_data = {
            "header": {"success": True},
            "result": {
                "records": [
                    {
                        "end_of_quarter": "2023-Q1",
                        "outstanding_loans": 100,
                        "outstanding_loans_ratio": 0.1,
                    },
                    {
                        "end_of_quarter": "2023-Q2",
                        "outstanding_loans": 110,
                        "outstanding_loans_ratio": 0.11,
                    },
                    {
                        "end_of_quarter": "2024-Q1",
                        "outstanding_loans": 120,
                        "outstanding_loans_ratio": 0.12,
                    },
                ]
            },
        }

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.neg_resident_mortgage.fetch_json_data"
        ) as mock_fetch_json_data:
            # Setup mock response for successful data fetching
            mock_fetch_json_data.return_value = mock_json_data

            # Test filtering by year range
            result = _get_neg_equity_stats(start_year=2023, end_year=2023)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["quarter"], "2023-Q1")
            self.assertEqual(result[0]["outstanding_loans"], 100)

            # Test filtering by year and month range (Q1 = Jan-Mar, Q2 = Apr-Jun)
            result = _get_neg_equity_stats(
                start_year=2023, start_month=4, end_year=2023, end_month=6
            )
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["quarter"], "2023-Q2")

            # Test empty result for non-matching years
            result = _get_neg_equity_stats(start_year=2025, end_year=2025)
            self.assertEqual(len(result), 0)

            # Test error handling when fetch_json_data returns an error
            mock_fetch_json_data.return_value = {"error": "JSON fetch failed"}
            result = _get_neg_equity_stats(start_year=2023, end_year=2023)
            self.assertEqual(result, {"type": "Error", "error": "JSON fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_neg_equity_stats tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_neg_equity_stats function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get statistics on residential mortgage loans in negative equity in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_neg_equity_stats")

        # Call the decorated function and verify it calls _get_neg_equity_stats
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.neg_resident_mortgage._get_neg_equity_stats"
        ) as mock_get_neg_equity_stats:
            decorated_function(start_year=2023, end_year=2023)
            mock_get_neg_equity_stats.assert_called_once_with(2023, None, 2023, None)
