"""
Module for testing the Coin Cart Schedule tool functionality.

This module contains unit tests to verify the correct fetching and processing
of coin cart schedule data from the HKMA API using the tool_coin_cart module.
"""

import unittest
from unittest.mock import patch, mock_open
import json
import hkopenai.hk_finance_mcp_server.tool_coin_cart as tool_coin_cart


class TestCoinCartSchedule(unittest.TestCase):
    """Test case class for verifying Coin Cart Schedule tool functionality."""

    MOCK_JSON = {
        "header": {"success": "true", "err_code": "0000", "err_msg": "No error found"},
        "result": {
            "datasize": 2,
            "records": [
                {
                    "start_date": "2025-08-11",
                    "end_date": "2025-08-17",
                    "cart_no": 1,
                    "district": "Tuen Mun District",
                    "address": "Open area outside Yuet Tin House, Yan Tin Estate, Tuen Mun",
                    "latitude": 22.414693,
                    "longitude": 113.977181,
                    "remarks": "Service suspended on Wednesday 13 August",
                },
                {
                    "start_date": "2025-08-12",
                    "end_date": "2025-08-17",
                    "cart_no": 2,
                    "district": "Kwun Tong District",
                    "address": "Chi Tai House, On Tai Estate, Kwun Tong",
                    "latitude": 22.328886,
                    "longitude": 114.228783,
                    "remarks": "Service suspended on Monday 11 August",
                },
            ],
        },
    }

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.mock_urlopen = patch("urllib.request.urlopen").start()
        mock_response = mock_open(read_data=json.dumps(self.MOCK_JSON).encode("utf-8"))
        self.mock_urlopen.return_value = mock_response()
        self.addCleanup(patch.stopall)

    def test_fetch_coin_cart_schedule(self):
        """Test fetching coin cart schedule data.

        Verifies that the fetch_coin_cart_schedule function returns the expected data structure
        with header and result information.
        """
        result = tool_coin_cart.fetch_coin_cart_schedule()

        self.assertIsInstance(result, dict)
        self.assertIn("header", result)
        self.assertIn("result", result)
        self.assertEqual(result["result"]["datasize"], 2)

    def test_get_coin_cart_schedule(self):
        """Test getting coin cart schedule data in standardized format.

        Verifies that the get_coin_cart_schedule function returns data with the expected key.
        """
        result = tool_coin_cart._get_coin_cart_schedule()

        self.assertIn("coin_cart_schedule", result)

    @patch("urllib.request.urlopen")
    def test_api_error_handling(self, mock_urlopen):
        """Test handling of API errors.

        Verifies that the fetch_coin_cart_schedule function raises an exception
        when an API error occurs.
        """
        mock_urlopen.side_effect = Exception("API Error")

        with self.assertRaises(Exception):
            tool_coin_cart.fetch_coin_cart_schedule()

    @patch("urllib.request.urlopen")
    def test_invalid_json_data(self, mock_urlopen):
        """Test handling of invalid JSON data.

        Verifies that the fetch_coin_cart_schedule function raises an exception
        when invalid JSON data is received.
        """
        # Test handling of invalid JSON data
        invalid_json = "{invalid json}"
        mock_urlopen.return_value = mock_open(read_data=invalid_json.encode("utf-8"))()

        with self.assertRaises(Exception) as context:
            tool_coin_cart.fetch_coin_cart_schedule()
        self.assertTrue(
            "JSON" in str(context.exception) or "decode" in str(context.exception),
            "Expected JSON decode error",
        )

    @patch("urllib.request.urlopen")
    def test_empty_json_data(self, mock_urlopen):
        """Test handling of empty JSON data.

        Verifies that the fetch_coin_cart_schedule function returns an empty dict
        when empty JSON data is received.
        """
        # Test handling of empty JSON data
        empty_json = "{}"
        mock_urlopen.return_value = mock_open(read_data=empty_json.encode("utf-8"))()

        result = tool_coin_cart.fetch_coin_cart_schedule()
        self.assertEqual(result, {}, "Expected empty dict for empty JSON data")

    @patch("urllib.request.urlopen")
    def test_missing_records_in_json(self, mock_urlopen):
        """Test handling of JSON data with missing records.

        Verifies that the fetch_coin_cart_schedule function returns a result
        with an empty records list when no records are present in the JSON data.
        """
        # Test handling of JSON data with missing records
        missing_records_json = {"result": {"records": []}}
        mock_urlopen.return_value = mock_open(
            read_data=json.dumps(missing_records_json).encode("utf-8")
        )()

        result = tool_coin_cart.fetch_coin_cart_schedule()
        self.assertIn("result", result)
        self.assertEqual(
            result["result"]["records"],
            [],
            "Expected empty records list for JSON with no records",
        )

    @patch("urllib.request.urlopen")
    def test_incomplete_record_data(self, mock_urlopen):
        """Test handling of JSON data with incomplete records.

        Verifies that the fetch_coin_cart_schedule function processes partial data
        and includes only the available fields in the result.
        """
        # Test handling of JSON data with incomplete records
        incomplete_record_json = {
            "result": {
                "records": [
                    {
                        "date": "2025-06-10",
                        # Missing other fields
                    }
                ]
            }
        }
        mock_urlopen.return_value = mock_open(
            read_data=json.dumps(incomplete_record_json).encode("utf-8")
        )()

        result = tool_coin_cart.fetch_coin_cart_schedule()
        self.assertIn("result", result)
        self.assertEqual(
            len(result["result"]["records"]),
            1,
            "Expected result with partial data to be processed",
        )
        self.assertIn(
            "date",
            result["result"]["records"][0],
            "Expected 'date' to be present in result",
        )
        self.assertNotIn(
            "district",
            result["result"]["records"][0],
            "Expected missing fields to not be in result",
        )


if __name__ == "__main__":
    unittest.main()
