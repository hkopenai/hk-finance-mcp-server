"""
Module for testing the ATM Locator tool functionality.

This module contains unit tests to verify the correct fetching and filtering
of ATM location data from the HKMA API using the tool_atm_locator module.
"""

import unittest
import json
from unittest.mock import patch, Mock
from hkopenai.hk_finance_mcp_server import tool_atm_locator


class TestAtmLocatorTool(unittest.TestCase):
    """Test case class for verifying ATM Locator tool functionality."""
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_data = {
            "result": {
                "records": [
                    {
                        "district": "YuenLong",
                        "bank_name": "Industrial and Commercial Bank of China (Asia) Limited",
                        "type_of_machine": "Automatic Teller Machine",
                        "function": "Cash withdrawal, Cardless withdrawal",
                        "currencies_supported": "HKD, RMB",
                        "barrier_free_access": "Voice navigation, Suitable height ATM for wheelchair users",
                        "network": "JETCO, PLUS, CIRRUS, CUP, VISA, MASTER, DISCOVER, DINER",
                        "address": "No.7, 2/F, T Town South, Tin Chung Court, 30 Tin Wah Road, Tin Shui Wai, Yuen Long, N.T.",
                        "service_hours": "24 hours",
                        "latitude": "22.461655",
                        "longitude": "113.997757",
                    }
                ]
            }
        }

    @patch("urllib.request.urlopen")
    def test_fetch_atm_locator_data(self, mock_urlopen):
        """Test fetching ATM location data without filters.
        
        Verifies that the fetch_atm_locator_data function returns the expected data
        when no filters are applied.
        """
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode("utf-8")
        mock_urlopen.return_value = mock_response

        result = tool_atm_locator.fetch_atm_locator_data(pagesize=1, offset=0)

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["district"], "YuenLong")
        self.assertEqual(
            result[0]["bank_name"],
            "Industrial and Commercial Bank of China (Asia) Limited",
        )

    @patch("urllib.request.urlopen")
    def test_fetch_atm_locator_data_with_filters(self, mock_urlopen):
        """Test fetching ATM location data with filters.
        
        Verifies that the fetch_atm_locator_data function correctly applies filters
        for district and bank name, returning matching and non-matching results as expected.
        """
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode("utf-8")
        mock_urlopen.return_value = mock_response

        result = tool_atm_locator.fetch_atm_locator_data(
            district="YuenLong",
            bank_name="Industrial and Commercial Bank of China (Asia) Limited",
            pagesize=1,
            offset=0,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["district"], "YuenLong")

        result = tool_atm_locator.fetch_atm_locator_data(
            district="Central", pagesize=1, offset=0
        )
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
