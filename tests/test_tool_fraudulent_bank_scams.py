"""
Module for testing the Fraudulent Bank Scams tool functionality.

This module contains unit tests to verify the correct fetching of fraudulent bank scam
alerts from the HKMA API using the tool_fraudulent_bank_scams module.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
from hkopenai.hk_finance_mcp_server.tools.fraudulent_bank_scams import (
    _get_fraudulent_bank_scams,
    register,
)


class TestFraudulentBankScamsTool(unittest.TestCase):
    """Test case class for verifying Fraudulent Bank Scams tool functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api_url = (
            "https://api.hkma.gov.hk/public/bank-svf-info/fraudulent-bank-scams"
        )

    @patch("hkopenai.hk_finance_mcp_server.tools.fraudulent_bank_scams.fetch_json_data")
    def test_get_fraudulent_bank_scams_success(self, mock_fetch_json_data):
        """Test fetching fraudulent bank scams data with successful API response.

        Verifies that the _get_fraudulent_bank_scams function returns the expected data
        when the API responds successfully.
        """
        # Mock successful API response
        mock_fetch_json_data.return_value = {
            "header": {
                "success": True,
                "err_code": "0000",
                "err_msg": "No error found",
            },
            "result": {
                "datasize": 2,
                "records": [
                    {
                        "issue_date": "2025-06-19",
                        "alleged_name": "Test Bank",
                        "scam_type": "Fraudulent website",
                        "pr_url": "http://test.com/alert.pdf",
                        "fraud_website_address": "hxxps://fake-test.com",
                    },
                    {
                        "issue_date": "2025-06-18",
                        "alleged_name": "Another Bank",
                        "scam_type": "Phishing email",
                        "pr_url": "http://another.com/alert.pdf",
                        "fraud_website_address": "hxxps://fake-another.com",
                    },
                ],
            },
        }

        # Call the function
        result = _get_fraudulent_bank_scams(lang="en")

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["alleged_name"], "Test Bank")
        self.assertEqual(result[1]["scam_type"], "Phishing email")
        mock_fetch_json_data.assert_called_once_with(
            f"{self.api_url}?lang=en", timeout=10
        )

    @patch("hkopenai.hk_finance_mcp_server.tools.fraudulent_bank_scams.fetch_json_data")
    def test_get_fraudulent_bank_scams_api_error(self, mock_fetch_json_data):
        """Test handling of API error response for fraudulent bank scams data.

        Verifies that the _get_fraudulent_bank_scams function raises an exception
        when the API returns an error.
        """
        # Mock API error response
        mock_fetch_json_data.return_value = {
            "header": {"success": False, "err_code": "9999", "err_msg": "API error"}
        }

        # Call the function and expect an exception
        with self.assertRaises(ValueError) as context:
            _get_fraudulent_bank_scams(lang="en")

        self.assertTrue("API Error: API error" in str(context.exception))
        mock_fetch_json_data.assert_called_once_with(
            f"{self.api_url}?lang=en", timeout=10
        )

    def test_register_tool(self):
        """Test the registration of the get_fraudulent_bank_scams tool."""
        mock_mcp = MagicMock()

        register(mock_mcp)

        mock_mcp.tool.assert_called_once_with(
            description="Get information on fraudulent bank websites and phishing scams reported to HKMA"
        )

        mock_decorator = mock_mcp.tool.return_value
        mock_decorator.assert_called_once()

        decorated_function = mock_decorator.call_args[0][0]
        self.assertEqual(decorated_function.__name__, "get_fraudulent_bank_scams")

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.fraudulent_bank_scams._get_fraudulent_bank_scams"
        ) as mock_get_fraudulent_bank_scams:
            decorated_function(lang="en")
            mock_get_fraudulent_bank_scams.assert_called_once_with("en")


if __name__ == "__main__":
    unittest.main()
