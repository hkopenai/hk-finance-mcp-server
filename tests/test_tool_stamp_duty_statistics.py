"""
Module for testing the Stamp Duty Statistics tool functionality.

This module contains unit tests to verify the correct fetching and filtering
of stamp duty statistics data using the tool_stamp_duty_statistics module.
"""

import unittest
import csv
from unittest.mock import patch, Mock
from io import StringIO
from hkopenai.hk_finance_mcp_server import tool_stamp_duty_statistics


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
        mock_urlopen.return_value = mock_response

        result = tool_stamp_duty_statistics.fetch_stamp_duty_data()

        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["period"], "202501")
        self.assertEqual(result[0]["sd_listed"], 3554.692596)
        self.assertEqual(result[0]["sd_unlisted"], 27.088813)

    @patch("urllib.request.urlopen")
    def test_get_stamp_duty_statistics_with_filters(self, mock_urlopen):
        """Test getting stamp duty statistics with period filters.
        
        Verifies that the get_stamp_duty_statistics function correctly filters results
        based on the specified start and end periods.
        """
        mock_response = Mock()
        mock_response.read.return_value = self.csv_content.encode("utf-8")
        mock_urlopen.return_value = mock_response

        result = tool_stamp_duty_statistics.get_stamp_duty_statistics(
            start_period="202501", end_period="202501"
        )

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["period"], "202501")

        result = tool_stamp_duty_statistics.get_stamp_duty_statistics(
            start_period="202503"
        )
        self.assertEqual(len(result), 0)


if __name__ == "__main__":
    unittest.main()
