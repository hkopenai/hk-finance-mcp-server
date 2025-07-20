"""
Module for testing the credit card tools functionality.

This module contains unit tests for fetching and processing credit card related data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_finance_mcp_server.tools.credit_card import (
    _get_credit_card_stats,
    _get_credit_card_hotlines,
    register,
)


class TestCreditCardTools(unittest.TestCase):
    """
    Test class for verifying credit card tools functionality.

    This class contains test cases to ensure the data fetching and processing
    for credit card related data work as expected.
    """

    def test_get_credit_card_stats(self):
        """
        Test the retrieval and filtering of credit card lending survey statistics.

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
                        "endperiod_noofaccts": 100,
                        "endperiod_delinquent_amt": 10,
                        "during_chargeoff_amt": 5,
                        "during_rollover_amt": 20,
                        "during_avg_total_receivables": 500,
                    },
                    {
                        "end_of_quarter": "2023-Q2",
                        "endperiod_noofaccts": 110,
                        "endperiod_delinquent_amt": 12,
                        "during_chargeoff_amt": 6,
                        "during_rollover_amt": 22,
                        "during_avg_total_receivables": 550,
                    },
                    {
                        "end_of_quarter": "2024-Q1",
                        "endperiod_noofaccts": 120,
                        "endperiod_delinquent_amt": 15,
                        "during_chargeoff_amt": 7,
                        "during_rollover_amt": 25,
                        "during_avg_total_receivables": 600,
                    },
                ]
            },
        }

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.credit_card.fetch_json_data"
        ) as mock_fetch_json_data:
            # Setup mock response for successful data fetching
            mock_fetch_json_data.return_value = mock_json_data

            # Test filtering by year range
            result = _get_credit_card_stats(start_year=2023, end_year=2023)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["quarter"], "2023-Q1")
            self.assertEqual(result[0]["accounts_count"], 100)

            # Test filtering by year and month range (Q1 = Jan-Mar, Q2 = Apr-Jun)
            result = _get_credit_card_stats(
                start_year=2023, start_month=4, end_year=2023, end_month=6
            )
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["quarter"], "2023-Q2")

            # Test empty result for non-matching years
            result = _get_credit_card_stats(start_year=2025, end_year=2025)
            self.assertEqual(len(result), 0)

            # Test error handling when fetch_json_data returns an error
            mock_fetch_json_data.return_value = {"error": "JSON fetch failed"}
            result = _get_credit_card_stats(start_year=2023, end_year=2023)
            self.assertEqual(result, {"type": "Error", "error": "JSON fetch failed"})

    def test_get_credit_card_hotlines(self):
        """
        Test the retrieval of credit card hotlines.

        This test verifies that the function correctly fetches and returns hotline data.
        """
        # Mock the JSON data
        mock_json_data = {
            "header": {"success": True},
            "result": {
                "records": [
                    {"bank": "Bank A", "hotline": "11112222"},
                    {"bank": "Bank B", "hotline": "33334444"},
                ]
            },
        }

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.credit_card.fetch_json_data"
        ) as mock_fetch_json_data:
            # Setup mock response for successful data fetching
            mock_fetch_json_data.return_value = mock_json_data

            # Test successful data retrieval
            result = _get_credit_card_hotlines()
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["bank"], "Bank A")

            # Test error handling when fetch_json_data returns an error
            mock_fetch_json_data.return_value = {"error": "JSON fetch failed"}
            result = _get_credit_card_hotlines()
            self.assertEqual(result, {"type": "Error", "error": "JSON fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the credit card tools.

        This test verifies that the register function correctly registers the tools
        with the FastMCP server and that the registered tools call the underlying
        functions.
        """
        mock_mcp = MagicMock()

        # Mock the decorator behavior
        mock_decorator_stats = MagicMock(return_value=lambda f: f)
        mock_decorator_hotlines = MagicMock(return_value=lambda f: f)
        mock_mcp.tool.side_effect = [mock_decorator_stats, mock_decorator_hotlines]

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called for get_credit_card_stats
        mock_mcp.tool.assert_any_call(
            description="Get credit card lending survey results in Hong Kong"
        )

        # Verify that mcp.tool was called for get_credit_card_hotlines
        mock_mcp.tool.assert_any_call(
            description="Get list of hotlines for reporting loss of credit card from Hong Kong banks."
        )

        # Get the decorated functions from the calls to the decorator mocks
        decorated_function_stats = mock_decorator_stats.call_args[0][0]
        self.assertEqual(decorated_function_stats.__name__, "get_credit_card_stats")

        decorated_function_hotlines = mock_decorator_hotlines.call_args[0][0]
        self.assertEqual(
            decorated_function_hotlines.__name__, "get_credit_card_hotlines"
        )

        # Call the decorated functions and verify they call the underlying functions
        with (
            patch(
                "hkopenai.hk_finance_mcp_server.tools.credit_card._get_credit_card_stats"
            ) as mock_get_credit_card_stats,
            patch(
                "hkopenai.hk_finance_mcp_server.tools.credit_card._get_credit_card_hotlines"
            ) as mock_get_credit_card_hotlines,
        ):
            decorated_function_stats(start_year=2023, end_year=2023)
            mock_get_credit_card_stats.assert_called_once_with(2023, None, 2023, None)

            decorated_function_hotlines()
            mock_get_credit_card_hotlines.assert_called_once()
