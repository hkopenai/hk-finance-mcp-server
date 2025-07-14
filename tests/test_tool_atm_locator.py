"""
Module for testing the ATM Locator tool functionality.

This module contains unit tests to verify the correct fetching and filtering
of ATM location data from the HKMA API using the tool_atm_locator module.
"""

import unittest
import json
from unittest.mock import patch, Mock, MagicMock
from hkopenai.hk_finance_mcp_server.tool_atm_locator import (
    fetch_atm_locator_data,
    _get_atm_locations,
    register,
)


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
        
        """Test fetching ATM location data without filters."""


        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        result = fetch_atm_locator_data(pagesize=1, offset=0)

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
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        result = fetch_atm_locator_data(
            district="YuenLong",
            bank_name="Industrial and Commercial Bank of China (Asia) Limited",
            pagesize=1,
            offset=0,
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["district"], "YuenLong")

        result = fetch_atm_locator_data(district="Central", pagesize=1, offset=0)
        self.assertEqual(len(result), 0)

    def test_get_atm_locations(self):
        """Test retrieving ATM locations with optional filtering."""
        with patch(
            "hkopenai.hk_finance_mcp_server.tool_atm_locator.fetch_atm_locator_data"
        ) as mock_fetch:
            mock_fetch.return_value = [
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
                    "latitude": 22.461655,
                    "longitude": 113.997757,
                }
            ]
            result = _get_atm_locations(district="YuenLong")
            mock_fetch.assert_called_once_with("YuenLong", None, 100, 0)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["district"], "YuenLong")

    def test_register_tool(self):
        """Test the registration of the get_atm_locations tool."""
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get information on Automated Teller Machines (ATMs) of retail banks in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_atm_locations")

        # Call the decorated function and verify it calls _get_atm_locations
        with patch(
            "hkopenai.hk_finance_mcp_server.tool_atm_locator._get_atm_locations"
        ) as mock_get_atm_locations:
            decorated_function(
                district="YuenLong",
                bank_name="Industrial and Commercial Bank of China (Asia) Limited",
                pagesize=1,
                offset=0,
            )
            mock_get_atm_locations.assert_called_once_with(
                "YuenLong",
                "Industrial and Commercial Bank of China (Asia) Limited",
                1,
                0,
            )


if __name__ == "__main__":
    unittest.main()
