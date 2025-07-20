"""
Module for testing the coin cart tool functionality.

This module contains unit tests for fetching and processing coin cart schedule data.
"""

import unittest
from unittest.mock import patch, MagicMock

from hkopenai.hk_finance_mcp_server.tools.coin_cart import (
    _get_coin_cart_schedule,
    register,
)


class TestCoinCart(unittest.TestCase):
    """
    Test class for verifying coin cart functionality.

    This class contains test cases to ensure the data fetching and processing
    for coin cart schedule data work as expected.
    """

    def test_get_coin_cart_schedule(self):
        """
        Test the retrieval of coin cart schedule data.

        This test verifies that the function correctly fetches and returns data,
        and handles error cases.
        """
        # Mock the JSON data
        mock_json_data = {
            "header": {"success": True},
            "result": {
                "records": [
                    {"location": "Central", "date": "2023-07-17"},
                    {"location": "Mong Kok", "date": "2023-07-18"},
                ]
            },
        }

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.coin_cart.fetch_json_data"
        ) as mock_fetch_json_data:
            # Setup mock response for successful data fetching
            mock_fetch_json_data.return_value = mock_json_data

            # Test successful data retrieval
            result = _get_coin_cart_schedule()
            self.assertIn("coin_cart_schedule", result)
            self.assertEqual(len(result["coin_cart_schedule"]["result"]["records"]), 2)
            self.assertEqual(
                result["coin_cart_schedule"]["result"]["records"][0]["location"],
                "Central",
            )

            # Test error handling when fetch_json_data returns an error
            mock_fetch_json_data.return_value = {"error": "JSON fetch failed"}
            result = _get_coin_cart_schedule()
            self.assertEqual(result, {"type": "Error", "error": "JSON fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_coin_cart tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_coin_cart_schedule function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get coin collection cart schedule in Hong Kong. The cart can charge your electronic wallet and you no long have to keep coins."
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_coin_cart")

        # Call the decorated function and verify it calls _get_coin_cart_schedule
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.coin_cart._get_coin_cart_schedule"
        ) as mock_get_coin_cart_schedule:
            decorated_function()
            mock_get_coin_cart_schedule.assert_called_once()
