"""
Module for testing the Fraudulent Bank Scams tool functionality.

This module contains unit tests to verify the correct fetching of fraudulent bank scam
alerts from the HKMA API using the tool_fraudulent_bank_scams module.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_finance_mcp_server import tool_fraudulent_bank_scams


class TestFraudulentBankScamsTool(unittest.TestCase):
    """Test case class for verifying Fraudulent Bank Scams tool functionality."""
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.api_url = tool_fraudulent_bank_scams.API_URL

    @patch("requests.get")
    def test_get_fraudulent_bank_scams_success(self, mock_get):
        """Test fetching fraudulent bank scams data with successful API response.
        
        Verifies that the get_fraudulent_bank_scams function returns the expected data
        when the API responds successfully.
        """
        # Mock successful API response
        mock_response = Mock()
        mock_response.json.return_value = {
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
        mock_get.return_value = mock_response

        # Call the function
        result = tool_fraudulent_bank_scams.get_fraudulent_bank_scams(lang="en")

        # Assertions
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["alleged_name"], "Test Bank")
        self.assertEqual(result[1]["scam_type"], "Phishing email")
        mock_get.assert_called_once_with(f"{self.api_url}?lang=en", timeout=10)

    @patch("requests.get")
    def test_get_fraudulent_bank_scams_api_error(self, mock_get):
        """Test handling of API error response for fraudulent bank scams data.
        
        Verifies that the get_fraudulent_bank_scams function raises an exception
        when the API returns an error.
        """
        # Mock API error response
        mock_response = Mock()
        mock_response.json.return_value = {
            "header": {"success": False, "err_code": "9999", "err_msg": "API error"}
        }
        mock_get.return_value = mock_response

        # Call the function and expect an exception
        with self.assertRaises(ValueError) as context:
            tool_fraudulent_bank_scams.get_fraudulent_bank_scams(lang="en")

        self.assertTrue("API Error: API error" in str(context.exception))
        mock_get.assert_called_once_with(f"{self.api_url}?lang=en", timeout=10)


if __name__ == "__main__":
    unittest.main()
