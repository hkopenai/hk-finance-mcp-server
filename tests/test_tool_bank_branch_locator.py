"""Module for testing the Bank Branch Locator tool functionality."""

import unittest
import json
from unittest.mock import patch, Mock, MagicMock
import hkopenai.hk_finance_mcp_server.tool_bank_branch_locator as tool_bank_branch_locator


class TestBankBranchLocatorTool(unittest.TestCase):
    """Test case class for verifying Bank Branch Locator tool functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_data = """
{
    "result": {
        "datasize": 2,
        "records": [
            {
                "district": "Central",
                "bank_name": "Test Bank 1",
                "branch_name": "Main Branch",
                "address": "123 Test Street, Central",
                "service_hours": "Mon-Fri, 09:00 - 17:00",
                "latitude": "22.2799",
                "longitude": "114.1588",
                "barrier_free_access": "Wheelchair accessible"
            },
            {
                "district": "Kowloon",
                "bank_name": "Test Bank 2",
                "branch_name": "Kowloon Branch",
                "address": "456 Test Road, Kowloon",
                "service_hours": "Mon-Fri, 09:00 - 17:00",
                "latitude": "22.3169",
                "longitude": "114.1694",
                "barrier_free_access": "Guide dogs welcome"
            }
        ]
    }
}
"""

    @patch("urllib.request.urlopen")
    def test_fetch_bank_branch_data_no_filter(self, mock_urlopen):
        """Test fetching bank branch data without filters.

        Verifies that the fetch_bank_branch_data function returns all available data
        when no filters are applied.
        """
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = self.sample_data.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        # Act
        result = tool_bank_branch_locator.fetch_bank_branch_data()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["district"], "Central")
        self.assertEqual(result[1]["bank_name"], "Test Bank 2")

    @patch("urllib.request.urlopen")
    def test_fetch_bank_branch_data_with_district_filter(self, mock_urlopen):
        """Test fetching bank branch data with district filter.

        Verifies that the fetch_bank_branch_data function correctly filters results
        based on the specified district.
        """
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = self.sample_data.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        # Act
        result = tool_bank_branch_locator.fetch_bank_branch_data(district="Central")

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["district"], "Central")

    @patch("urllib.request.urlopen")
    def test_fetch_bank_branch_data_with_bank_name_filter(self, mock_urlopen):
        """Test fetching bank branch data with bank name filter.

        Verifies that the fetch_bank_branch_data function correctly filters results
        based on the specified bank name.
        """
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = self.sample_data.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        # Act
        result = tool_bank_branch_locator.fetch_bank_branch_data(
            bank_name="Test Bank 2"
        )

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["bank_name"], "Test Bank 2")

    @patch("urllib.request.urlopen")
    def test_get_bank_branch_locations_empty_result(self, mock_urlopen):
        """
        Test fetching bank branch locations with empty result.

        Verifies that the get_bank_branch_locations function returns an empty list
        when no data is available from the API.
        """
        # Arrange
        empty_data = {"result": {"datasize": 0, "records": []}}
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(empty_data).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        # Act
        result = tool_bank_branch_locator._get_bank_branch_locations(
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
        tool_bank_branch_locator.register(mock_mcp)

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
            "hkopenai.hk_finance_mcp_server.tool_bank_branch_locator._get_bank_branch_locations"
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
