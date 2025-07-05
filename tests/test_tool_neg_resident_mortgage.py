"""
Module for testing the Negative Equity Mortgage tool functionality.

This module contains unit tests to verify the correct fetching and filtering
of negative equity mortgage data from the HKMA API using the tool_neg_resident_mortgage module.
"""

import unittest
from unittest.mock import patch, mock_open
import json
from hkopenai.hk_finance_mcp_server import tool_neg_resident_mortgage


class TestNegativeEquityMortgage(unittest.TestCase):
    """Test case class for verifying Negative Equity Mortgage tool functionality."""
    JSON_DATA = """{
        "header": {"success": true},
        "result": {
            "datasize": 5,
            "records": [
                {
                    "end_of_quarter": "2025-Q1",
                    "outstanding_loans": 40741,
                    "outstanding_loans_ratio": "6.88",
                    "outstanding_loans_amt": 205881,
                    "outstanding_loans_amt_ratio": "10.95",
                    "unsecured_portion_amt": 16402,
                    "lv_ratio": 1.09
                },
                {
                    "end_of_quarter": "2024-Q4",
                    "outstanding_loans": 38389,
                    "outstanding_loans_ratio": "6.5",
                    "outstanding_loans_amt": 195072,
                    "outstanding_loans_amt_ratio": "10.41",
                    "unsecured_portion_amt": 14517,
                    "lv_ratio": 1.08
                },
                {
                    "end_of_quarter": "2024-Q3",
                    "outstanding_loans": 40713,
                    "outstanding_loans_ratio": "6.89",
                    "outstanding_loans_amt": 207510,
                    "outstanding_loans_amt_ratio": "11.06",
                    "unsecured_portion_amt": 15778,
                    "lv_ratio": 1.08
                },
                {
                    "end_of_quarter": "2024-Q2",
                    "outstanding_loans": 30288,
                    "outstanding_loans_ratio": "5.13",
                    "outstanding_loans_amt": 154992,
                    "outstanding_loans_amt_ratio": "8.29",
                    "unsecured_portion_amt": 10003,
                    "lv_ratio": 1.07
                },
                {
                    "end_of_quarter": "2024-Q1",
                    "outstanding_loans": 32073,
                    "outstanding_loans_ratio": "5.47",
                    "outstanding_loans_amt": 165349,
                    "outstanding_loans_amt_ratio": "8.91",
                    "unsecured_portion_amt": 11223,
                    "lv_ratio": 1.07
                }
            ]
        }
    }"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_urlopen = patch("urllib.request.urlopen").start()
        self.mock_urlopen.return_value = mock_open(
            read_data=self.JSON_DATA.encode("utf-8")
        )()
        self.addCleanup(patch.stopall)

    @patch("urllib.request.urlopen")
    def test_fetch_neg_equity_data(self, mock_urlopen):
        """Test fetching negative equity mortgage data without filters.
        
        Verifies that the fetch_neg_equity_data function returns the expected data
        when no filters are applied.
        """
        mock_urlopen.return_value = mock_open(
            read_data=self.JSON_DATA.encode("utf-8")
        )()

        result = tool_neg_resident_mortgage.fetch_neg_equity_data()

        self.assertEqual(len(result), 5)
        self.assertEqual(
            result[0],
            {
                "quarter": "2025-Q1",
                "outstanding_loans": 40741,
                "outstanding_loans_ratio": "6.88",
                "outstanding_loans_amt": 205881,
                "outstanding_loans_amt_ratio": "10.95",
                "unsecured_portion_amt": 16402,
                "lv_ratio": 1.09,
            },
        )
        self.assertEqual(
            result[-1],
            {
                "quarter": "2024-Q1",
                "outstanding_loans": 32073,
                "outstanding_loans_ratio": "5.47",
                "outstanding_loans_amt": 165349,
                "outstanding_loans_amt_ratio": "8.91",
                "unsecured_portion_amt": 11223,
                "lv_ratio": 1.07,
            },
        )

    def test_start_year_month_filter(self):
        """Test fetching negative equity mortgage data with start year and month filter.
        
        Verifies that the fetch_neg_equity_data function correctly filters results
        based on the specified start year and month.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(
                start_year=2025, start_month=3
            )
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["quarter"], "2025-Q1")

    def test_end_year_month_filter(self):
        """Test fetching negative equity mortgage data with end year and month filter.
        
        Verifies that the fetch_neg_equity_data function correctly filters results
        based on the specified end year and month.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(
                end_year=2024, end_month=6
            )
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["quarter"], "2024-Q2")
            self.assertEqual(result[-1]["quarter"], "2024-Q1")

    def test_both_year_month_filters(self):
        """Test fetching negative equity mortgage data with both start and end year/month filters.
        
        Verifies that the fetch_neg_equity_data function correctly filters results
        within the specified date range.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(
                start_year=2024, start_month=6, end_year=2024, end_month=12
            )
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["quarter"], "2024-Q4")
            self.assertEqual(result[-1]["quarter"], "2024-Q2")

    def test_start_year_only_filter(self):
        """Test fetching negative equity mortgage data with start year only filter.
        
        Verifies that the fetch_neg_equity_data function correctly filters results
        based on the specified start year.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(start_year=2025)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["quarter"], "2025-Q1")

    def test_end_year_only_filter(self):
        """Test fetching negative equity mortgage data with end year only filter.
        
        Verifies that the fetch_neg_equity_data function correctly filters results
        based on the specified end year.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(end_year=2024)
            self.assertEqual(len(result), 4)
            self.assertEqual(result[0]["quarter"], "2024-Q4")
            self.assertEqual(result[-1]["quarter"], "2024-Q1")

    def test_get_neg_equity_stats(self):
        """Test getting negative equity mortgage statistics.
        
        Verifies that the get_neg_equity_stats function returns the expected data.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.get_neg_equity_stats()
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]["quarter"], "2025-Q1")

    @patch("urllib.request.urlopen")
    def test_invalid_json_data(self, mock_urlopen):
        """Test handling of invalid JSON data.
        
        Verifies that the fetch_neg_equity_data function returns an error entry
        when invalid JSON data is received.
        """
        # Test handling of invalid JSON data
        invalid_json = "{invalid json}"
        mock_urlopen.return_value = mock_open(read_data=invalid_json.encode("utf-8"))()

        result = tool_neg_resident_mortgage.fetch_neg_equity_data()
        self.assertEqual(
            len(result), 1, "Expected a single error entry for invalid JSON data"
        )
        self.assertIn("error", result[0], "Expected an error message in the result")
        self.assertIn(
            "JSON",
            result[0]["error"] or "",
            "Expected JSON decode error message in the result",
        )

    @patch("urllib.request.urlopen")
    def test_empty_json_data(self, mock_urlopen):
        """Test handling of empty JSON data.
        
        Verifies that the fetch_neg_equity_data function returns an empty list
        when empty JSON data is received.
        """
        # Test handling of empty JSON data
        empty_json = "{}"
        mock_urlopen.return_value = mock_open(read_data=empty_json.encode("utf-8"))()

        result = tool_neg_resident_mortgage.fetch_neg_equity_data()
        self.assertEqual(len(result), 0, "Expected empty result for empty JSON data")

    @patch("urllib.request.urlopen")
    def test_missing_records_in_json(self, mock_urlopen):
        """Test handling of JSON data with missing records.
        
        Verifies that the fetch_neg_equity_data function returns an empty list
        when no records are present in the JSON data.
        """
        # Test handling of JSON data with missing records
        missing_records_json = {
            "header": {"success": True},
            "result": {"datasize": 0, "records": []},
        }
        mock_urlopen.return_value = mock_open(
            read_data=json.dumps(missing_records_json).encode("utf-8")
        )()

        result = tool_neg_resident_mortgage.fetch_neg_equity_data()
        self.assertEqual(
            len(result), 0, "Expected empty result for JSON with no records"
        )

    @patch("urllib.request.urlopen")
    def test_incomplete_record_data(self, mock_urlopen):
        """Test handling of JSON data with incomplete records.
        
        Verifies that the fetch_neg_equity_data function processes partial data
        and includes only the available fields in the result.
        """
        # Test handling of JSON data with incomplete records
        incomplete_record_json = {
            "header": {"success": True},
            "result": {
                "datasize": 1,
                "records": [
                    {
                        "end_of_quarter": "2025-Q1"
                        # Missing other fields
                    }
                ],
            },
        }
        mock_urlopen.return_value = mock_open(
            read_data=json.dumps(incomplete_record_json).encode("utf-8")
        )()

        result = tool_neg_resident_mortgage.fetch_neg_equity_data()
        self.assertEqual(
            len(result), 1, "Expected result with partial data to be processed"
        )
        self.assertIn(
            "quarter", result[0], "Expected 'quarter' to be present in result"
        )
        self.assertNotIn(
            "outstanding_loans",
            result[0],
            "Expected missing fields to not be in result",
        )

    @patch("urllib.request.urlopen")
    def test_network_failure(self, mock_urlopen):
        """Test handling of network failure.
        
        Verifies that the fetch_neg_equity_data function raises an exception
        when a network error occurs.
        """
        # Test handling of network failure
        mock_urlopen.side_effect = Exception("Network Error")

        with self.assertRaises(Exception) as context:
            tool_neg_resident_mortgage.fetch_neg_equity_data()
        self.assertTrue(
            "Network Error" in str(context.exception), "Expected network error message"
        )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters(self, mock_urlopen):
        """Test handling of invalid year/month filters (start year None).
        
        Verifies that the fetch_neg_equity_data function returns full data set
        when start year is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Since the function likely converts inputs to int or handles invalid types internally,
            # we test with None instead of invalid types to avoid type checker errors.
            # Test invalid start year (using None as a placeholder for invalid input)
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(start_year=None)
            self.assertEqual(
                len(result), 5, "Expected full data set when start year is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters2(self, mock_urlopen):
        """Test handling of invalid year/month filters (start month None).
        
        Verifies that the fetch_neg_equity_data function returns full data set
        when start month is None.
        """
        # Test invalid start month (using None as a placeholder for invalid input)
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(
                start_year=None, start_month=None
            )
            self.assertEqual(
                len(result), 5, "Expected full data set when start month is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters3(self, mock_urlopen):
        """Test handling of invalid year/month filters (end year None).
        
        Verifies that the fetch_neg_equity_data function returns full data set
        when end year is None.
        """
        # Test invalid end year (using None as a placeholder for invalid input)
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(end_year=None)
            self.assertEqual(
                len(result), 5, "Expected full data set when end year is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters4(self, mock_urlopen):
        """Test handling of invalid year/month filters (end month None).
        
        Verifies that the fetch_neg_equity_data function returns full data set
        when end month is None.
        """
        # Test invalid end month (using None as a placeholder for invalid input)
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(end_month=None)
            self.assertEqual(
                len(result), 5, "Expected full data set when end month is None"
            )

    @patch("urllib.request.urlopen")
    def test_boundary_year_month_filters(self, mock_urlopen):
        """Test boundary conditions for year/month filters (future date).
        
        Verifies that the fetch_neg_equity_data function returns an empty result
        for a future start year.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test future date filter
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(start_year=2030)
            self.assertEqual(
                len(result), 0, "Expected empty result for future start year"
            )

    @patch("urllib.request.urlopen")
    def test_boundary_year_month_filters2(self, mock_urlopen):
        """Test boundary conditions for year/month filters (very old date).
        
        Verifies that the fetch_neg_equity_data function returns an empty result
        for a very old end year.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test very old date filter
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(end_year=2000)
            self.assertEqual(
                len(result), 0, "Expected empty result for very old end year"
            )

    @patch("urllib.request.urlopen")
    def test_boundary_year_month_filters3(self, mock_urlopen):
        """Test boundary conditions for year/month filters (invalid month value).
        
        Verifies that the fetch_neg_equity_data function returns data for the year only
        when the month value is out of range.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test invalid month value (out of range)
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(
                start_year=2025, start_month=13
            )
            self.assertEqual(
                len(result), 1, "Expected data for year only when month is out of range"
            )


if __name__ == "__main__":
    unittest.main()
