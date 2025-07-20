"""
Module for testing the HKMA tender invitations tool functionality.

This module contains unit tests for fetching and processing HKMA tender invitations data.
"""

import unittest
from unittest.mock import patch, MagicMock
from datetime import datetime


from hkopenai.hk_finance_mcp_server.tools.hkma_tender import (
    _get_tender_invitations,
    register,
)


class TestHKMATenderInvitations(unittest.TestCase):
    """
    Test class for verifying HKMA tender invitations functionality.

    This class contains test cases to ensure the data fetching and processing
    for HKMA tender invitations data work as expected.
    """

    def test_get_tender_invitations(self):
        """
        Test the retrieval and filtering of HKMA tender invitations.

        This test verifies that the function correctly fetches and filters data by date range,
        and handles error cases.
        """
        # Mock the JSON data
        mock_json_data = {
            "header": {"success": True},
            "result": {
                "records": [
                    {"issue_date": "2023-01-15", "title": "Tender 1"},
                    {"issue_date": "2023-02-20", "title": "Tender 2"},
                    {"issue_date": "2023-03-10", "title": "Tender 3"},
                    {"issue_date": "2024-01-05", "title": "Tender 4"},
                ]
            },
        }

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.hkma_tender.fetch_json_data"
        ) as mock_fetch_json_data:
            # Setup mock response for successful data fetching
            mock_fetch_json_data.return_value = mock_json_data

            # Test filtering by date range
            result = _get_tender_invitations(
                from_date="2023-02-01", to_date="2023-03-31"
            )
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["title"], "Tender 2")
            self.assertEqual(result[1]["title"], "Tender 3")

            # Test empty result for non-matching dates
            result = _get_tender_invitations(
                from_date="2025-01-01", to_date="2025-12-31"
            )
            self.assertEqual(len(result), 0)

            # Test error handling when fetch_json_data returns an error
            mock_fetch_json_data.return_value = {"error": "JSON fetch failed"}
            result = _get_tender_invitations(from_date="2023-01-01")
            self.assertEqual(result, {"type": "Error", "error": "JSON fetch failed"})

    def test_register_tool(self):
        """
        Test the registration of the get_hkma_tender_invitations tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_tender_invitations function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get information of Tender Invitation and Notice of Award of Contracts from Hong Kong Monetary Authority"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_hkma_tender_invitations")

        # Call the decorated function and verify it calls _get_tender_invitations
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.hkma_tender._get_tender_invitations"
        ) as mock_get_tender_invitations:
            decorated_function(
                lang="en",
                segment="tender",
                from_date="2023-01-01",
                to_date="2023-12-31",
            )
            mock_get_tender_invitations.assert_called_once_with(
                lang="en",
                segment="tender",
                pagesize=None,
                offset=None,
                from_date="2023-01-01",
                to_date="2023-12-31",
            )
