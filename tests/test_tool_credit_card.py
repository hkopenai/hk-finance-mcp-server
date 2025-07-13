"""
Module for testing the Credit Card Lending tool functionality.

This module contains unit tests to verify the correct fetching and filtering
of credit card lending survey data from the HKMA API using the tool_credit_card module.
"""

import unittest
import json
from unittest.mock import patch, mock_open
import hkopenai.hk_finance_mcp_server.tool_credit_card as tool_credit_card


class TestCreditCardLending(unittest.TestCase):
    """Test case class for verifying Credit Card Lending tool functionality."""

    JSON_DATA = """{
        "header": {"success": true},
        "result": {
            "datasize": 5,
            "records": [
                {
                    "end_of_quarter": "2025-Q1",
                    "endperiod_noofaccts": 18500000,
                    "endperiod_delinquent_amt": 1250000000,
                    "during_chargeoff_amt": 350000000,
                    "during_rollover_amt": 4200000000,
                    "during_avg_total_receivables": 18500000000
                },
                {
                    "end_of_quarter": "2024-Q4",
                    "endperiod_noofaccts": 18300000,
                    "endperiod_delinquent_amt": 1200000000,
                    "during_chargeoff_amt": 340000000,
                    "during_rollover_amt": 4100000000,
                    "during_avg_total_receivables": 18300000000
                },
                {
                    "end_of_quarter": "2024-Q3",
                    "endperiod_noofaccts": 18200000,
                    "endperiod_delinquent_amt": 1180000000,
                    "during_chargeoff_amt": 330000000,
                    "during_rollover_amt": 4000000000,
                    "during_avg_total_receivables": 18200000000
                },
                {
                    "end_of_quarter": "2024-Q2",
                    "endperiod_noofaccts": 18000000,
                    "endperiod_delinquent_amt": 1150000000,
                    "during_chargeoff_amt": 320000000,
                    "during_rollover_amt": 3900000000,
                    "during_avg_total_receivables": 18000000000
                },
                {
                    "end_of_quarter": "2024-Q1",
                    "endperiod_noofaccts": 17800000,
                    "endperiod_delinquent_amt": 1100000000,
                    "during_chargeoff_amt": 310000000,
                    "during_rollover_amt": 3800000000,
                    "during_avg_total_receivables": 17800000000
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
    def test_fetch_credit_card_data(self, mock_urlopen):
        """Test fetching credit card lending data without filters.

        Verifies that the fetch_credit_card_data function returns the expected data
        when no filters are applied.
        """
        mock_urlopen.return_value = mock_open(
            read_data=self.JSON_DATA.encode("utf-8")
        )()

        result = tool_credit_card.fetch_credit_card_data()

        self.assertEqual(len(result), 5)
        self.assertEqual(
            result[0],
            {
                "quarter": "2025-Q1",
                "accounts_count": 18500000,
                "delinquent_amount": 1250000000,
                "chargeoff_amount": 350000000,
                "rollover_amount": 4200000000,
                "avg_receivables": 18500000000,
            },
        )
        self.assertEqual(
            result[-1],
            {
                "quarter": "2024-Q1",
                "accounts_count": 17800000,
                "delinquent_amount": 1100000000,
                "chargeoff_amount": 310000000,
                "rollover_amount": 3800000000,
                "avg_receivables": 17800000000,
            },
        )

    def test_start_year_month_filter(self):
        """Test fetching credit card lending data with start year and month filter.

        Verifies that the fetch_credit_card_data function correctly filters results
        based on the specified start year and month.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_credit_card.fetch_credit_card_data(
                start_year=2025, start_month=3
            )
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["quarter"], "2025-Q1")

    def test_end_year_month_filter(self):
        """Test fetching credit card lending data with end year and month filter.

        Verifies that the fetch_credit_card_data function correctly filters results
        based on the specified end year and month.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_credit_card.fetch_credit_card_data(end_year=2024, end_month=6)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]["quarter"], "2024-Q2")
            self.assertEqual(result[-1]["quarter"], "2024-Q1")

    def test_both_year_month_filters(self):
        """Test fetching credit card lending data with both start and end year/month filters.

        Verifies that the fetch_credit_card_data function correctly filters results
        within the specified date range.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_credit_card.fetch_credit_card_data(
                start_year=2024, start_month=6, end_year=2024, end_month=12
            )
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]["quarter"], "2024-Q4")
            self.assertEqual(result[-1]["quarter"], "2024-Q2")

    def test_start_year_only_filter(self):
        """Test fetching credit card lending data with start year only filter.

        Verifies that the fetch_credit_card_data function correctly filters results
        based on the specified start year.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_credit_card.fetch_credit_card_data(start_year=2025)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]["quarter"], "2025-Q1")

    def test_end_year_only_filter(self):
        """Test fetching credit card lending data with end year only filter.

        Verifies that the fetch_credit_card_data function correctly filters results
        based on the specified end year.
        """
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_credit_card.fetch_credit_card_data(end_year=2024)
            self.assertEqual(len(result), 4)
            self.assertEqual(result[0]["quarter"], "2024-Q4")
            self.assertEqual(result[-1]["quarter"], "2024-Q1")

    def test_get_credit_card_stats(self):
        """Test getting credit card lending statistics."""
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_credit_card._get_credit_card_stats()
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]["quarter"], "2025-Q1")

    @patch("urllib.request.urlopen")
    def test_invalid_json_data(self, mock_urlopen):
        """Test handling of invalid JSON data.

        Verifies that the fetch_credit_card_data function raises an exception
        when invalid JSON data is received.
        """
        # Test handling of invalid JSON data
        invalid_json = "{invalid json}"
        mock_urlopen.return_value = mock_open(read_data=invalid_json.encode("utf-8"))()

        with self.assertRaises(Exception) as context:
            tool_credit_card.fetch_credit_card_data()
        self.assertTrue(
            "JSON decode error" in str(context.exception),
            "Expected JSON decode error message",
        )

    @patch("urllib.request.urlopen")
    def test_empty_json_data(self, mock_urlopen):
        """Test handling of empty JSON data.

        Verifies that the fetch_credit_card_data function returns an empty list
        when empty JSON data is received.
        """
        # Test handling of empty JSON data
        empty_json = "{}"
        mock_urlopen.return_value = mock_open(read_data=empty_json.encode("utf-8"))()

        result = tool_credit_card.fetch_credit_card_data()
        self.assertEqual(len(result), 0, "Expected empty result for empty JSON data")

    @patch("urllib.request.urlopen")
    def test_missing_records_in_json(self, mock_urlopen):
        """Test handling of JSON data with missing records.

        Verifies that the fetch_credit_card_data function returns an empty list
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

        result = tool_credit_card.fetch_credit_card_data()
        self.assertEqual(
            len(result), 0, "Expected empty result for JSON with no records"
        )

    @patch("urllib.request.urlopen")
    def test_incomplete_record_data(self, mock_urlopen):
        """Test handling of JSON data with incomplete records.

        Verifies that the fetch_credit_card_data function processes partial data
        and sets 'invalid data' for missing fields.
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

        result = tool_credit_card.fetch_credit_card_data()
        self.assertEqual(
            len(result), 1, "Expected result with partial data to be processed"
        )
        self.assertIn(
            "quarter", result[0], "Expected 'quarter' to be present in result"
        )
        self.assertEqual(
            result[0].get("accounts_count"),
            "invalid data",
            "Expected 'accounts_count' to be 'invalid data' for missing field",
        )
        self.assertEqual(
            result[0].get("delinquent_amount"),
            "invalid data",
            "Expected 'delinquent_amount' to be 'invalid data' for missing field",
        )
        self.assertEqual(
            result[0].get("chargeoff_amount"),
            "invalid data",
            "Expected 'chargeoff_amount' to be 'invalid data' for missing field",
        )
        self.assertEqual(
            result[0].get("rollover_amount"),
            "invalid data",
            "Expected 'rollover_amount' to be 'invalid data' for missing field",
        )
        self.assertEqual(
            result[0].get("avg_receivables"),
            "invalid data",
            "Expected 'avg_receivables' to be 'invalid data' for missing field",
        )

    @patch("urllib.request.urlopen")
    def test_network_failure(self, mock_urlopen):
        """Test handling of network failure.

        Verifies that the fetch_credit_card_data function raises an exception
        when a network error occurs.
        """
        # Test handling of network failure
        mock_urlopen.side_effect = Exception("Network Error")

        with self.assertRaises(Exception) as context:
            tool_credit_card.fetch_credit_card_data()
        self.assertTrue(
            "Network Error" in str(context.exception), "Expected network error message"
        )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters(self, mock_urlopen):
        """Test handling of invalid year/month filters (start year None).

        Verifies that the fetch_credit_card_data function returns full data set
        when start year is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Since the function likely converts inputs to int or handles invalid types internally,
            # we test with None or out-of-range values instead of invalid types to avoid type checker errors.
            # Test invalid start year (using None as a placeholder for invalid input)
            result = tool_credit_card.fetch_credit_card_data(start_year=None)
            self.assertEqual(
                len(result), 5, "Expected full data set when start year is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters2(self, mock_urlopen):
        """Test handling of invalid year/month filters (start month None).

        Verifies that the fetch_credit_card_data function returns full data set
        when start month is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test invalid start month (using None as a placeholder for invalid input)
            result = tool_credit_card.fetch_credit_card_data(start_month=None)
            self.assertEqual(
                len(result), 5, "Expected full data set when start month is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters3(self, mock_urlopen):
        """Test handling of invalid year/month filters (end year None).

        Verifies that the fetch_credit_card_data function returns full data set
        when end year is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test invalid end year (using None as a placeholder for invalid input)
            result = tool_credit_card.fetch_credit_card_data(end_year=None)
            self.assertEqual(
                len(result), 5, "Expected full data set when end year is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters4(self, mock_urlopen):
        """Test handling of invalid year/month filters (end month None).

        Verifies that the fetch_credit_card_data function returns full data set
        when end month is None.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test invalid end month (using None as a placeholder for invalid input)
            result = tool_credit_card.fetch_credit_card_data(end_month=None)
            self.assertEqual(
                len(result), 5, "Expected full data set when end month is None"
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters5(self, mock_urlopen):
        """Test handling of invalid year/month filters (start month out of range).

        Verifies that the fetch_credit_card_data function uses only the year
        when start month is out of range.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test out-of-range month values
            result = tool_credit_card.fetch_credit_card_data(
                start_year=2025, start_month=13
            )
            self.assertEqual(
                len(result),
                1,
                "Expected data for year only when start month is out of range",
            )

    @patch("urllib.request.urlopen")
    def test_invalid_year_month_filters6(self, mock_urlopen):
        """Test handling of invalid year/month filters (end month out of range).

        Verifies that the fetch_credit_card_data function returns no data
        when end month is out of range and before any data.
        """
        # Test handling of invalid year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            result = tool_credit_card.fetch_credit_card_data(end_year=2024, end_month=0)
            self.assertEqual(
                len(result),
                0,
                "Expected no data when end month is out of range and before any data",
            )

    @patch("urllib.request.urlopen")
    def test_boundary_year_month_filters(self, mock_urlopen):
        """Test boundary conditions for year/month filters (future date).

        Verifies that the fetch_credit_card_data function returns an empty result
        for a future start year.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test future date filter
            result = tool_credit_card.fetch_credit_card_data(start_year=2030)
            self.assertEqual(
                len(result), 0, "Expected empty result for future start year"
            )

    @patch("urllib.request.urlopen")
    def test_boundary_year_month_filters2(self, mock_urlopen):
        """Test boundary conditions for year/month filters (very old date).

        Verifies that the fetch_credit_card_data function returns an empty result
        for a very old end year.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test very old date filter
            result = tool_credit_card.fetch_credit_card_data(end_year=2000)
            self.assertEqual(
                len(result), 0, "Expected empty result for very old end year"
            )

    @patch("urllib.request.urlopen")
    def test_boundary_year_month_filters3(self, mock_urlopen):
        """Test boundary conditions for year/month filters (invalid month value).

        Verifies that the fetch_credit_card_data function uses only the year
        when the month value is out of range.
        """
        # Test boundary conditions for year/month filters
        with patch(
            "urllib.request.urlopen",
            return_value=mock_open(read_data=self.JSON_DATA.encode("utf-8"))(),
        ):
            # Test invalid month value (out of range)
            result = tool_credit_card.fetch_credit_card_data(
                start_year=2025, start_month=13
            )
            self.assertEqual(
                len(result), 1, "Expected data for year only when month is out of range"
            )


if __name__ == "__main__":
    unittest.main()
