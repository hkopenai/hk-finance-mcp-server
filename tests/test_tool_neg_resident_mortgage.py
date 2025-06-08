import unittest
from unittest.mock import patch, mock_open
import json
from hk_finance_mcp_server import tool_neg_resident_mortgage

class TestNegativeEquityMortgage(unittest.TestCase):
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
        self.mock_urlopen = patch('urllib.request.urlopen').start()
        self.mock_urlopen.return_value = mock_open(read_data=self.JSON_DATA.encode('utf-8'))()
        self.addCleanup(patch.stopall)

    @patch('urllib.request.urlopen')
    def test_fetch_neg_equity_data(self, mock_urlopen):
        mock_urlopen.return_value = mock_open(read_data=self.JSON_DATA.encode('utf-8'))()
        
        result = tool_neg_resident_mortgage.fetch_neg_equity_data()
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], {
            'quarter': '2025-Q1',
            'outstanding_loans': 40741,
            'outstanding_loans_ratio': '6.88',
            'outstanding_loans_amt': 205881,
            'outstanding_loans_amt_ratio': '10.95',
            'unsecured_portion_amt': 16402,
            'lv_ratio': 1.09
        })
        self.assertEqual(result[-1], {
            'quarter': '2024-Q1',
            'outstanding_loans': 32073,
            'outstanding_loans_ratio': '5.47',
            'outstanding_loans_amt': 165349,
            'outstanding_loans_amt_ratio': '8.91',
            'unsecured_portion_amt': 11223,
            'lv_ratio': 1.07
        })

    def test_start_year_month_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(start_year=2025, start_month=3)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['quarter'], '2025-Q1')

    def test_end_year_month_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(end_year=2024, end_month=6)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['quarter'], '2024-Q2')
            self.assertEqual(result[-1]['quarter'], '2024-Q1')

    def test_both_year_month_filters(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(
                start_year=2024, start_month=6,
                end_year=2024, end_month=12
            )
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]['quarter'], '2024-Q4')
            self.assertEqual(result[-1]['quarter'], '2024-Q2')

    def test_start_year_only_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(start_year=2025)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['quarter'], '2025-Q1')

    def test_end_year_only_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_neg_resident_mortgage.fetch_neg_equity_data(end_year=2024)
            self.assertEqual(len(result), 4)
            self.assertEqual(result[0]['quarter'], '2024-Q4')
            self.assertEqual(result[-1]['quarter'], '2024-Q1')

    def test_get_neg_equity_stats(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_neg_resident_mortgage.get_neg_equity_stats()
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]['quarter'], '2025-Q1')

if __name__ == '__main__':
    unittest.main()
