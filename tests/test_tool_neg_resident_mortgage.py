"""
Module for testing the negative equity residential mortgage tool.

This module contains unit tests for fetching and filtering negative equity residential mortgage data.
"""

import unittest
from unittest.mock import patch, MagicMock
import json

from hkopenai.hk_finance_mcp_server.tool_neg_resident_mortgage import (
    register,
    fetch_neg_equity_data,
)


class TestNegResidentMortgage(unittest.TestCase):
    """
    Test class for verifying negative equity residential mortgage functionality.
    """

    def setUp(self):
        self.sample_data = {
            "header": {"success": True},
            "result": {
                "records": [
                    {
                        "end_of_quarter": "2023-Q4",
                        "outstanding_loans": 1000,
                        "outstanding_loans_ratio": 0.5,
                        "outstanding_loans_amt": 500,
                        "outstanding_loans_amt_ratio": 0.25,
                        "unsecured_portion_amt": 100,
                        "lv_ratio": 0.1,
                    },
                    {
                        "end_of_quarter": "2023-Q3",
                        "outstanding_loans": 900,
                        "outstanding_loans_ratio": 0.4,
                        "outstanding_loans_amt": 450,
                        "outstanding_loans_amt_ratio": 0.20,
                        "unsecured_portion_amt": 90,
                        "lv_ratio": 0.09,
                    },
                    {
                        "end_of_quarter": "2022-Q4",
                        "outstanding_loans": 800,
                        "outstanding_loans_ratio": 0.3,
                        "outstanding_loans_amt": 400,
                        "outstanding_loans_amt_ratio": 0.15,
                        "unsecured_portion_amt": 80,
                        "lv_ratio": 0.08,
                    },
                    {
                        "end_of_quarter": "2021-Q1",
                        "outstanding_loans": 700,
                        "outstanding_loans_ratio": 0.2,
                        "outstanding_loans_amt": 350,
                        "outstanding_loans_amt_ratio": 0.10,
                        "unsecured_portion_amt": 70,
                        "lv_ratio": 0.07,
                    },
                ]
            },
        }

    @patch("urllib.request.urlopen")
    def test_fetch_neg_equity_data_success(self, mock_urlopen):
        """
        Test successful fetching and parsing of negative equity data.
        """
        mock_response = MagicMock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode("utf-8")
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        data = fetch_neg_equity_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 4)
        self.assertEqual(data[0]["quarter"], "2023-Q4")

    @patch("urllib.request.urlopen")
    def test_fetch_neg_equity_data_api_error(self, mock_urlopen):
        """
        Test handling of API errors during data fetching.
        """
        mock_urlopen.side_effect = Exception("Connection failed")
        with self.assertRaisesRegex(
            Exception, "Error fetching data: Connection failed"
        ):
            fetch_neg_equity_data()

    @patch("urllib.request.urlopen")
    def test_fetch_neg_equity_data_invalid_json(self, mock_urlopen):
        """
        Test handling of invalid JSON response.
        """
        mock_response = MagicMock()
        mock_response.read.return_value.decode.return_value = "invalid json"
        mock_urlopen.return_value.__enter__.return_value = mock_response
        mock_urlopen.return_value.__exit__.return_value = None

        data = fetch_neg_equity_data()
        self.assertIsInstance(data, list)
        self.assertEqual(len(data), 1)
        self.assertIn("error", data[0])
        self.assertIn("Invalid JSON data received", data[0]["error"])

    def test_register_tool(self):
        """
        Test the registration of the get_neg_equity_stats tool.
        """
        mock_mcp = MagicMock()
        register(mock_mcp)

        mock_mcp.tool.assert_called_once_with(
            description="Get statistics on residential mortgage loans in negative equity in Hong Kong"
        )
        mock_decorator = mock_mcp.tool.return_value
        mock_decorator.assert_called_once()
        decorated_function = mock_decorator.call_args[0][0]
        self.assertEqual(decorated_function.__name__, "get_neg_equity_stats")

        with patch(
            "hkopenai.hk_finance_mcp_server.tool_neg_resident_mortgage._get_neg_equity_stats"
        ) as mock_get_neg_equity_stats:
            decorated_function(start_year=2023, end_year=2023)
            mock_get_neg_equity_stats.assert_called_once_with(2023, None, 2023, None)


if __name__ == "__main__":
    unittest.main()
