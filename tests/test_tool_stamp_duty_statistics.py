"""
Module for testing the Stamp Duty Statistics tool functionality.

This module contains unit tests to verify the correct fetching and filtering
of stamp duty statistics data using the tool_stamp_duty_statistics module.
"""

import unittest
from unittest.mock import patch, Mock, MagicMock
from hkopenai.hk_finance_mcp_server.tool_stamp_duty_statistics import (
    _get_stamp_duty_statistics,
    register,
    fetch_stamp_duty_data,
)


class TestStampDutyStatisticsTool(unittest.TestCase):
    """Test case class for verifying Stamp Duty Statistics tool functionality."""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.sample_data = [
            {
                "Period": "202501",
                "SD_Listed": "3554.692596",
                "SD_Unlisted": "27.088813",
            },
            {"Period": "202502", "SD_Listed": "6206.47798", "SD_Unlisted": "32.083893"},
        ]
        self.csv_content = "Period,SD_Listed,SD_Unlisted\n202501,3554.692596,27.088813\n202502,6206.47798,32.083893\n"

    @patch("urllib.request.urlopen")
    def test_fetch_stamp_duty_data(self, mock_urlopen):
        """Test fetching stamp duty statistics data.

        Verifies that the fetch_stamp_duty_data function returns the expected data
        from the provided CSV content.
        """
        mock_response = Mock()
        mock_response.read.return_value = self.csv_content.encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        result = fetch_stamp_duty_data()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["period"], "202501")
        self.assertEqual(result[0]["sd_listed"], 3554.692596)
        self.assertEqual(result[0]["sd_unlisted"], 27.088813)

    @patch(
        "hkopenai.hk_finance_mcp_server.tool_stamp_duty_statistics.fetch_stamp_duty_data"
    )
    def test_get_stamp_duty_statistics_with_filters(self, mock_fetch_stamp_duty_data):
        """Test getting stamp duty statistics with period filters.

        Verifies that the _get_stamp_duty_statistics function correctly filters results
        based on the specified start and end periods.
        """
        mock_fetch_stamp_duty_data.return_value = [
            {"period": "202501", "sd_listed": 100.0, "sd_unlisted": 10.0},
            {"period": "202502", "sd_listed": 200.0, "sd_unlisted": 20.0},
            {"period": "202503", "sd_listed": 300.0, "sd_unlisted": 30.0},
        ]

        result = _get_stamp_duty_statistics(start_period="202501", end_period="202501")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["period"], "202501")

        result = _get_stamp_duty_statistics(start_period="202503")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["period"], "202503")

        result = _get_stamp_duty_statistics(end_period="202502")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["period"], "202501")
        self.assertEqual(result[1]["period"], "202502")

        result = _get_stamp_duty_statistics(start_period="202601")
        self.assertEqual(len(result), 0)

    def test_register_tool(self):
        """Test the registration of the get_stamp_duty_statistics tool."""
        mock_mcp = MagicMock()

        register(mock_mcp)

        mock_mcp.tool.assert_called_once_with(
            description="Get monthly statistics on stamp duty collected from transfer of Hong Kong stock (both listed and unlisted)"
        )

        mock_decorator = mock_mcp.tool.return_value
        mock_decorator.assert_called_once()

        decorated_function = mock_decorator.call_args[0][0]
        self.assertEqual(decorated_function.__name__, "get_stamp_duty_statistics")

        with patch(
            "hkopenai.hk_finance_mcp_server.tool_stamp_duty_statistics._get_stamp_duty_statistics"
        ) as mock_get_stamp_duty_statistics:
            decorated_function(start_period="202401", end_period="202403")
            mock_get_stamp_duty_statistics.assert_called_once_with("202401", "202403")


if __name__ == "__main__":
    unittest.main()
