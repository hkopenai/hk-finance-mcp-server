"""
Module for testing the Business Registration Returns tool functionality.

This module contains unit tests to verify the correct fetching and filtering
of business registration data from the IRD API using the tool_business_reg module.
"""

import unittest
from unittest.mock import patch, mock_open
from hkopenai.hk_finance_mcp_server.tool_business_reg import fetch_business_returns_data


class TestBusinessReturns(unittest.TestCase):
    """Test case class for verifying Business Registration Returns tool functionality."""

    CSV_DATA = """RUN_DATE,ACTIVE_MAIN_BUS,NEW_REG_MAIN_BUS
202505,1604714,17497
202504,1598085,16982
202503,1591678,18435
202502,1588258,13080
202501,1585520,14115
202412,1583802,14429
202411,1578590,16481
202410,1574431,15081
202409,1574259,13384
202408,1575333,15070
202407,1580017,15076
202406,1580230,13984
202405,1579564,15373
202404,1576889,13149
202403,1577907,15495
202402,1578619,8129
202401,1587450,12588
202312,1585721,12020
202311,1585292,13150
"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_urlopen = patch("urllib.request.urlopen").start()
        self.mock_urlopen.return_value = mock_open(
            read_data=self.CSV_DATA.encode("utf-8")
        )()
        self.addCleanup(patch.stopall)

    @patch("urllib.request.urlopen")
    def test_fetch_business_returns_data(self, mock_urlopen):
        """Test fetching business returns data without filters.

        Verifies that the fetch_business_returns_data function returns the expected data
        when no filters are applied.
        """
        # Mock the URL response
        mock_urlopen.return_value = mock_open(read_data=self.CSV_DATA.encode("utf-8"))()

        # Call the function
        result = fetch_business_returns_data()

        # Verify the result
        self.assertEqual(len(result), 19)
        self.assertEqual(
            result[0],
            {
                "year_month": "2025-05",
                "active_business": 1604714,
                "new_registered_business": 17497,
            },
        )
        self.assertEqual(
            result[-1],
            {
                "year_month": "2023-11",
                "active_business": 1585292,
                "new_registered_business": 13150,
            },
        )

    def test_start_year_month_filter(self):
        """Test fetching business returns data with start year and month filter.

        Verifies that the fetch_business_returns_data function correctly filters results
        based on the specified start year and month.
        """
        # Test start year/month filter
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test start year/month filter
            result = fetch_business_returns_data(start_year=2025, start_month=3)
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["year_month"], "2025-05")

    def test_end_year_month_filter(self):
        """Test fetching business returns data with end year and month filter.

        Verifies that the fetch_business_returns_data function correctly filters results
        based on the specified end year and month.
        """
        # Test end year/month filter
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test end year/month filter
            result = fetch_business_returns_data(end_year=2025, end_month=3)
            self.assertEqual(len(result), 17)
            self.assertEqual(result[-1]["year_month"], "2023-11")

    def test_both_year_month_filters(self):
        """Test fetching business returns data with both start and end year/month filters.

        Verifies that the fetch_business_returns_data function correctly filters results
        within the specified date range.
        """
        # Test both filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test both filters
            result = fetch_business_returns_data(
                start_year=2025, start_month=2, end_year=2025, end_month=4
            )
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["year_month"], "2025-04")
            self.assertEqual(result[-1]["year_month"], "2025-02")

    def test_start_year_only_filter(self):
        """Test fetching business returns data with start year only filter.

        Verifies that the fetch_business_returns_data function correctly filters results
        based on the specified start year.
        """
        # Test start year only filter
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            result = fetch_business_returns_data(start_year=2025)
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]["year_month"], "2025-05")
            self.assertEqual(result[-1]["year_month"], "2025-01")

    def test_end_year_only_filter(self):
        """Test fetching business returns data with end year only filter.

        Verifies that the fetch_business_returns_data function correctly filters results
        based on the specified end year.
        """
        # Test end year only filter
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            result = fetch_business_returns_data(end_year=2025)
            self.assertEqual(len(result), 19)
            self.assertEqual(result[0]["year_month"], "2025-05")
            self.assertEqual(result[-1]["year_month"], "2023-11")

    def test_end_year_only_filter_2024(self):
        """Test fetching business returns data with end year only filter for 2024.

        Verifies that the fetch_business_returns_data function correctly filters results
        based on the specified end year of 2024.
        """
        # Test end year only filter
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            result = fetch_business_returns_data(end_year=2024)
            self.assertEqual(len(result), 14)
            self.assertEqual(result[0]["year_month"], "2024-12")
            self.assertEqual(result[-1]["year_month"], "2023-11")

    def test_both_year_only_filters(self):
        """Test fetching business returns data with both start and end year only filters.

        Verifies that the fetch_business_returns_data function correctly filters results
        within the specified year range.
        """
        # Test both year only filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            result = fetch_business_returns_data(start_year=2025, end_year=2025)
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]["year_month"], "2025-05")
            self.assertEqual(result[-1]["year_month"], "2025-01")

    @patch("urllib.request.urlopen")
    def test_invalid_csv_data(self, mock_urlopen):
        """Test handling of invalid CSV data.

        Verifies that the fetch_business_returns_data function handles invalid CSV data
        by returning a result with an error message for the invalid field.
        """
        # Test handling of invalid CSV data
        invalid_csv = """RUN_DATE,ACTIVE_MAIN_BUS,NEW_REG_MAIN_BUS
202505,invalid_data,17497
"""
        mock_urlopen.return_value = mock_open(read_data=invalid_csv.encode("utf-8"))()

        result = fetch_business_returns_data()
        self.assertEqual(
            result,
            [
                {
                    "year_month": "2025-05",
                    "active_business": "Invalid data for ACTIVE_MAIN_BUS: invalid_data",
                    "new_registered_business": 17497,
                }
            ],
        )

    @patch("urllib.request.urlopen")
    def test_empty_csv_data(self, mock_urlopen):
        """Test handling of empty CSV data.

        Verifies that the fetch_business_returns_data function returns an empty list
        when the CSV data is empty.
        """
        # Test handling of empty CSV data
        empty_csv = """RUN_DATE,ACTIVE_MAIN_BUS,NEW_REG_MAIN_BUS
"""
        mock_urlopen.return_value = mock_open(read_data=empty_csv.encode("utf-8"))()

        result = fetch_business_returns_data()
        self.assertEqual(len(result), 0, "Expected empty result for empty CSV data")

    @patch("urllib.request.urlopen")
    def test_network_failure(self, mock_urlopen):
        """Test handling of network failure.

        Verifies that the fetch_business_returns_data function raises an exception
        when a network error occurs.
        """
        # Test handling of network failure
        mock_urlopen.side_effect = Exception("Network Error")

        with self.assertRaises(Exception) as context:
            fetch_business_returns_data()
        self.assertTrue(
            "Network Error" in str(context.exception), "Expected network error message"
        )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters(self, mock_urlopen):
        """Test handling of invalid year/month filters (start year None).

        Verifies that the fetch_business_returns_data function returns full data set
        when start year is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Since the function likely converts inputs to int or handles invalid types internally,
            # we test with None or out-of-range values instead of invalid types to avoid type checker errors.
            # Test invalid start year (using None as a placeholder for invalid input)
            result = fetch_business_returns_data(start_year=None)
            self.assertEqual(
                len(result), 19, "Expected full data set when start year is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters2(self, mock_urlopen):
        """Test handling of invalid year/month filters (start month None).

        Verifies that the fetch_business_returns_data function returns full data set
        when start month is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test invalid start month (using None as a placeholder for invalid input)
            result = fetch_business_returns_data(start_month=None)
            self.assertEqual(
                len(result), 19, "Expected full data set when start month is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters3(self, mock_urlopen):
        """Test handling of invalid year/month filters (end year None).

        Verifies that the fetch_business_returns_data function returns full data set
        when end year is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test invalid end year (using None as a placeholder for invalid input)
            result = fetch_business_returns_data(end_year=None)
            self.assertEqual(
                len(result), 19, "Expected full data set when end year is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters4(self, mock_urlopen):
        """Test handling of invalid year/month filters (end month None).

        Verifies that the fetch_business_returns_data function returns full data set
        when end month is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test invalid end month (using None as a placeholder for invalid input)
            result = fetch_business_returns_data(end_month=None)
            self.assertEqual(
                len(result), 19, "Expected full data set when end month is None"
            )

    def test_boundary_year_month_filters(self):
        """Test boundary conditions for year/month filters (future date).

        Verifies that the fetch_business_returns_data function returns an empty result
        for a future start year.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test future date filter
            result = fetch_business_returns_data(start_year=2030)
            self.assertEqual(
                len(result), 0, "Expected empty result for future start year"
            )

    def test_boundary_year_month_filters2(self):
        """Test boundary conditions for year/month filters (very old date).

        Verifies that the fetch_business_returns_data function returns an empty result
        for a very old end year.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test very old date filter
            result = fetch_business_returns_data(end_year=2000)
            self.assertEqual(
                len(result), 0, "Expected empty result for very old end year"
            )

    def test_boundary_year_month_filters3(self):
        """Test boundary conditions for year/month filters (invalid month value).

        Verifies that the fetch_business_returns_data function uses only the year
        when the month value is out of range.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.CSV_DATA.encode("utf-8"))(),
        ):
            # Test invalid month value (out of range)
            result = fetch_business_returns_data(start_year=2025, start_month=13)
            self.assertEqual(
                len(result), 5, "Expected data for year only when month is out of range"
            )


if __name__ == "__main__":
    unittest.main()
