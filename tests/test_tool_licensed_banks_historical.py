"""Module for testing the Licensed Banks Historical Data tool functionality."""

import unittest
import json
from unittest.mock import patch, Mock, MagicMock
from hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical import (
    _get_licensed_banks_historical_data,
    register,
)


class TestLicensedBanksHistoricalTool(unittest.TestCase):
    """Test case class for verifying Licensed Banks Historical Data tool functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_data = """
{
    "result": {
        "datasize": 3,
        "records": [
            {
                "year": "1980",
                "licensed_banks": 115,
                "bank_branches": 1234,
                "bank_offices": 567,
                "total_branches_and_offices": 1801,
                "notes": "Data for 1980"
            },
            {
                "year": "1990",
                "licensed_banks": 165,
                "bank_branches": 1456,
                "bank_offices": 789,
                "total_branches_and_offices": 2245,
                "notes": "Data for 1990"
            },
            {
                "year": "2000",
                "licensed_banks": 154,
                "bank_branches": 1312,
                "bank_offices": 456,
                "total_branches_and_offices": 1768,
                "notes": "Data for 2000"
            }
        ]
    }
}"""

        self.sample_data_direct = """
{
    "records": [
        {
            "year": "1985",
            "licensed_banks": 125,
            "bank_branches": 1350,
            "bank_offices": 600,
            "total_branches_and_offices": 1950,
            "notes": "Data for 1985"
        },
        {
            "year": "1995",
            "licensed_banks": 159,
            "bank_branches": 1389,
            "bank_offices": 623,
            "total_branches_and_offices": 2012,
            "notes": "Data for 1995"
        }
    ]
}"""

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_no_filter(self, mock_fetch_json_data):
        """Test fetching historical data without filters."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_licensed_banks_historical_data()

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["year"], "1980")
        self.assertEqual(result[0]["licensed_banks"], 115)
        self.assertEqual(result[1]["bank_branches"], 1456)

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_with_year_filter(self, mock_fetch_json_data):
        """Test fetching historical data with year filter."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_licensed_banks_historical_data(start_year=1990, end_year=2000)

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["year"], "1990")
        self.assertEqual(result[1]["year"], "2000")

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_licensed_banks_only(self, mock_fetch_json_data):
        """Test fetching only licensed banks data."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_licensed_banks_historical_data(data_type="licensed_banks")

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0]["year"], "1980")
        self.assertEqual(result[0]["licensed_banks"], 115)
        # Should not have other fields
        self.assertNotIn("bank_branches", result[0])
        self.assertNotIn("bank_offices", result[0])

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_bank_branches_only(self, mock_fetch_json_data):
        """Test fetching only bank branches data."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_licensed_banks_historical_data(data_type="bank_branches")

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[1]["year"], "1990")
        self.assertEqual(result[1]["bank_branches"], 1456)
        # Should not have other fields
        self.assertNotIn("licensed_banks", result[1])
        self.assertNotIn("bank_offices", result[1])

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_bank_offices_only(self, mock_fetch_json_data):
        """Test fetching only bank offices data."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_licensed_banks_historical_data(data_type="bank_offices")

        # Assert
        self.assertEqual(len(result), 3)
        self.assertEqual(result[2]["year"], "2000")
        self.assertEqual(result[2]["bank_offices"], 456)
        # Should not have other fields
        self.assertNotIn("licensed_banks", result[2])
        self.assertNotIn("bank_branches", result[2])

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_direct_format(self, mock_fetch_json_data):
        """Test fetching data with direct records format."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data_direct)

        # Act
        result = _get_licensed_banks_historical_data()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["year"], "1985")
        self.assertEqual(result[1]["year"], "1995")

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_empty_result(self, mock_fetch_json_data):
        """Test fetching historical data with empty result."""
        # Arrange
        empty_data = {"result": {"datasize": 0, "records": []}}
        mock_fetch_json_data.return_value = empty_data

        # Act
        result = _get_licensed_banks_historical_data()

        # Assert
        self.assertEqual(result, {"message": "No data found for the specified criteria"})

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_error_response(self, mock_fetch_json_data):
        """Test handling error response from API."""
        # Arrange
        error_data = {"error": "API rate limit exceeded"}
        mock_fetch_json_data.return_value = error_data

        # Act
        result = _get_licensed_banks_historical_data()

        # Assert
        self.assertEqual(result, {"error": "API rate limit exceeded"})

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_invalid_format(self, mock_fetch_json_data):
        """Test handling invalid data format."""
        # Arrange
        mock_fetch_json_data.return_value = "invalid json string"

        # Act
        result = _get_licensed_banks_historical_data()

        # Assert
        self.assertEqual(result, {"error": "Invalid data format received from API"})

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_exception_handling(self, mock_fetch_json_data):
        """Test handling exceptions during data fetching."""
        # Arrange
        mock_fetch_json_data.side_effect = Exception("Network error")

        # Act
        result = _get_licensed_banks_historical_data()

        # Assert
        self.assertEqual(result, {"error": "Failed to fetch data: Network error"})

    @patch("hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical.fetch_json_data")
    def test_fetch_historical_data_with_language_parameter(self, mock_fetch_json_data):
        """Test fetching data with language parameter."""
        # Arrange
        mock_fetch_json_data.return_value = json.loads(self.sample_data)

        # Act
        result = _get_licensed_banks_historical_data(lang="tc")

        # Assert
        mock_fetch_json_data.assert_called_once()
        call_args = mock_fetch_json_data.call_args
        self.assertIn("params", call_args.kwargs)
        self.assertEqual(call_args.kwargs["params"]["lang"], "tc")

    def test_register_tool(self):
        """Test the registration of the get_licensed_banks_historical_data tool."""
        mock_mcp = MagicMock()

        # Call the register function
        register(mock_mcp)

        # Verify that mcp.tool was called with the correct description
        mock_mcp.tool.assert_called_once_with(
            description="Get historical data on licensed banks, bank branches, and bank offices in Hong Kong from 1954-2002"
        )

        # Get the mock that represents the decorator returned by mcp.tool
        mock_decorator = mock_mcp.tool.return_value

        # Verify that the mock decorator was called once (i.e., the function was decorated)
        mock_decorator.assert_called_once()

        # The decorated function is the first argument of the first call to the mock_decorator
        decorated_function = mock_decorator.call_args[0][0]

        # Verify the name of the decorated function
        self.assertEqual(decorated_function.__name__, "get_licensed_banks_historical_data")

        # Call the decorated function and verify it calls _get_licensed_banks_historical_data
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.licensed_banks_historical._get_licensed_banks_historical_data"
        ) as mock_get_historical_data:
            decorated_function(
                start_year=1980,
                end_year=2000,
                data_type="licensed_banks",
                lang="en",
            )
            mock_get_historical_data.assert_called_once_with(1980, 2000, "licensed_banks", "en")


if __name__ == "__main__":
    unittest.main() 