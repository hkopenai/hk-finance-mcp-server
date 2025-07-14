"""
Module for testing the HKMA Tender Invitations tool.

This module contains unit tests for fetching and filtering HKMA Tender Invitations data.
"""

import unittest
from unittest.mock import patch, MagicMock
import json

from hkopenai.hk_finance_mcp_server.tool_hkma_tender import (
    _get_tender_invitations,
    register,
    fetch_tender_invitations,
)


class TestHkmaTender(unittest.TestCase):
    """
    Test class for verifying HKMA Tender Invitations functionality.
    """

    def setUp(self):
        self.sample_data = {
            "header": {"success": True},
            "result": {
                "records": [
                    {
                        "title": "Tender for Cleaning Services",
                        "link": "http://example.com/tender1",
                        "issue_date": "2023-01-15",
                    },
                    {
                        "title": "Notice of Award for IT Services",
                        "link": "http://example.com/award1",
                        "issue_date": "2023-02-20",
                    },
                    {
                        "title": "Tender for Security System",
                        "link": "http://example.com/tender2",
                        "issue_date": "2022-11-01",
                    },
                ]
            },
        }

    @patch("urllib.request.urlopen")
    def test_fetch_tender_invitations_success(self, mock_urlopen):
        """
        Test successful fetching and parsing of tender invitations data.
        """
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        data = fetch_tender_invitations()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 3)
        self.assertEqual(data[0]["title"], "Tender for Cleaning Services")

    @patch("urllib.request.urlopen")
    def test_fetch_tender_invitations_api_error(self, mock_urlopen):
        """
        Test handling of API errors during data fetching.
        """
        mock_urlopen.side_effect = Exception("Connection failed")
        with self.assertRaisesRegex(
            Exception, "Error fetching data: Connection failed"
        ):
            fetch_tender_invitations()

    @patch("urllib.request.urlopen")
    def test_fetch_tender_invitations_invalid_json(self, mock_urlopen):
        """
        Test handling of invalid JSON response.
        """
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = "invalid json"
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        with self.assertRaisesRegex(Exception, "JSON decode error"):
            fetch_tender_invitations()

    @patch("hkopenai.hk_finance_mcp_server.tool_hkma_tender.fetch_tender_invitations")
    def test_get_tender_invitations_filtering(self, mock_fetch_data):
        """
        Test filtering logic in _get_tender_invitations.
        """
        mock_fetch_data.return_value = self.sample_data["result"]["records"]

        # Test without filters
        result = _get_tender_invitations(fetch_func=mock_fetch_data)
        self.assertEqual(len(result), 3)

        # Test with lang filter (should not affect count with current mock data)
        result = _get_tender_invitations(lang="tc", fetch_func=mock_fetch_data)
        self.assertEqual(len(result), 3)

        # Test with segment filter
        mock_fetch_data.return_value = [
            {
                "title": "Tender for Cleaning Services",
                "link": "http://example.com/tender1",
                "issue_date": "2023-01-15",
                "segment": "tender",
            },
            {
                "title": "Notice of Award for IT Services",
                "link": "http://example.com/award1",
                "issue_date": "2023-02-20",
                "segment": "notice",
            },
            {
                "title": "Tender for Security System",
                "link": "http://example.com/tender2",
                "issue_date": "2022-11-01",
                "segment": "tender",
            },
        ]
        result = _get_tender_invitations(segment="tender", fetch_func=mock_fetch_data)
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["title"], "Tender for Cleaning Services")

        # Test with from_date filter
        result = _get_tender_invitations(
            from_date="2023-01-01", fetch_func=mock_fetch_data
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Tender for Cleaning Services")

        # Test with to_date filter
        result = _get_tender_invitations(
            to_date="2023-01-31", fetch_func=mock_fetch_data
        )
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["title"], "Tender for Cleaning Services")

        # Test with from_date and to_date filter
        result = _get_tender_invitations(
            from_date="2022-01-01", to_date="2022-12-31", fetch_func=mock_fetch_data
        )
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["title"], "Tender for Security System")

    def test_register_tool(self):
        """
        Test the registration of the get_hkma_tender_invitations tool.
        """
        mock_mcp = MagicMock()
        register(mock_mcp)

        mock_mcp.tool.assert_called_once_with(
            description="Get information of Tender Invitation and Notice of Award of Contracts from Hong Kong Monetary Authority"
        )
        mock_decorator = mock_mcp.tool.return_value
        mock_decorator.assert_called_once()
        decorated_function = mock_decorator.call_args[0][0]
        self.assertEqual(decorated_function.__name__, "get_hkma_tender_invitations")

        with patch(
            "hkopenai.hk_finance_mcp_server.tool_hkma_tender._get_tender_invitations"
        ) as mock_get_tender_invitations:
            decorated_function(
                lang="en",
                segment="tender",
                pagesize=1,
                offset=0,
                from_date="2023-01-01",
                to_date="2023-12-31",
            )
            mock_get_tender_invitations.assert_called_once_with(
                lang="en",
                segment="tender",
                pagesize=1,
                offset=0,
                from_date="2023-01-01",
                to_date="2023-12-31",
            )


if __name__ == "__main__":
    unittest.main()
