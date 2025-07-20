"""Module for testing the Bank Branch Locator tool functionality."""

import unittest
import json
from unittest.mock import patch, Mock, MagicMock
from hkopenai.hk_finance_mcp_server.tools.bank_branch_locator import (
    _get_bank_branch_locations,
    register,
)


class TestBankBranchLocatorTool(unittest.TestCase):
    """Test case class for verifying Bank Branch Locator tool functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_data = """
{
    "result": {
        "datasize": 3,
        "records": [
            {
                "district": "YuenLong",
                "bank_name": "Industrial and Commercial Bank of China (Asia) Limited",
                "branch_name": "Yuen Long Branch",
                "address": "No.7, 2/F, T Town South, Tin Chung Court, 30 Tin Wah Road, Tin Shui Wai, Yuen Long, N.T.",
                "service_hours": "24 hours",
                "latitude": "22.461655",
                "longitude": "113.997757",
                "barrier_free_access": "Wheelchair accessible"
            },
            {
                "district": "Central",
                "bank_name": "Bank of China (Hong Kong) Limited",
                "branch_name": "Bank of China Tower Branch",
                "address": "Bank of China Tower, 1 Garden Road, Central, Hong Kong",
                "service_hours": "24 hours",
                "latitude": "22.2793",
                "longitude": "114.1616",
                "barrier_free_access": "None"
            },
            {
                "district": "Central",
                "bank_name": "Test Bank 3",
                "branch_name": "Another Branch",
                "address": "789 Another Street, Central",
                "service_hours": "Mon-Fri, 09:00 - 17:00",
                "latitude": "22.2800",
                "longitude": "114.1590",
                "barrier_free_access": "None"
            }
        ]
    }
}
"""

    @patch("hkopenai.hk_finance_mcp_server.tools.bank_branch_locator.fetch_json_data")
    def test_fetch_bank_branch_data_no_filter(self, mock_fetch_json_data):
        """Test fetching bank branch data without filters."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_bank_branch_locations(pagesize=2, offset=0)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["district"], "YuenLong")
        self.assertEqual(result[1]["bank_name"], "Bank of China (Hong Kong) Limited")

    @patch("hkopenai.hk_finance_mcp_server.tools.bank_branch_locator.fetch_json_data")
    def test_fetch_bank_branch_data_with_district_filter(self, mock_fetch_json_data):
        """Test fetching bank branch data with district filter."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_bank_branch_locations(district="Central", pagesize=100, offset=0)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["district"], "Central")

    @patch("hkopenai.hk_finance_mcp_server.tools.bank_branch_locator.fetch_json_data")
    def test_fetch_bank_branch_data_with_bank_name_filter(self, mock_fetch_json_data):
        """Test fetching bank branch data with bank name filter."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_bank_branch_locations(
            bank_name="Test Bank 3", pagesize=1, offset=0
        )

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["bank_name"], "Test Bank 3")

    @patch("hkopenai.hk_finance_mcp_server.tools.bank_branch_locator.fetch_json_data")
    def test_get_bank_branch_locations_empty_result(self, mock_fetch_json_data):
        """
        Test fetching bank branch locations with empty result.

        Verifies that the _get_bank_branch_locations function returns an empty list
        when no data is available from the API.
        """
        # Arrange
        empty_data = {"result": {"datasize": 0, "records": []}}
        mock_fetch_json_data.return_value = empty_data

        # Act
        result = _get_bank_branch_locations(
            district=None, bank_name=None, lang="en", pagesize=100, offset=0
        )

        # Assert
        self.assertEqual(result, [])

    def test_register_tool(self):
        """
        Test the registration of the get_bank_branch_locations tool.

        This test verifies that the register function correctly registers the tool
        with the FastMCP server and that the registered tool calls the underlying
        _get_bank_branch_locations function.
        """
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get information on bank branch locations of retail banks in Hong Kong"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_bank_branch_locations")

        # Call the decorated function and verify it calls _get_bank_branch_locations
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.bank_branch_locator._get_bank_branch_locations"
        ) as mock_get_bank_branch_locations:
            decorated_function(
                district="Central",
                bank_name="Test Bank 1",
                lang="en",
                pagesize=1,
                offset=0,
            )
            mock_get_bank_branch_locations.assert_called_once_with(
                "Central", "Test Bank 1", "en", 1, 0
            )


if __name__ == "__main__":
    unittest.main()
