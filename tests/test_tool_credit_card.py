import unittest
from unittest.mock import patch, mock_open
import json
from hk_finance_mcp_server import tool_credit_card

class TestCreditCardLending(unittest.TestCase):
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
        self.mock_urlopen = patch('urllib.request.urlopen').start()
        self.mock_urlopen.return_value = mock_open(read_data=self.JSON_DATA.encode('utf-8'))()
        self.addCleanup(patch.stopall)

    @patch('urllib.request.urlopen')
    def test_fetch_credit_card_data(self, mock_urlopen):
        mock_urlopen.return_value = mock_open(read_data=self.JSON_DATA.encode('utf-8'))()
        
        result = tool_credit_card.fetch_credit_card_data()
        
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], {
            'quarter': '2025-Q1',
            'accounts_count': 18500000,
            'delinquent_amount': 1250000000,
            'chargeoff_amount': 350000000,
            'rollover_amount': 4200000000,
            'avg_receivables': 18500000000
        })
        self.assertEqual(result[-1], {
            'quarter': '2024-Q1',
            'accounts_count': 17800000,
            'delinquent_amount': 1100000000,
            'chargeoff_amount': 310000000,
            'rollover_amount': 3800000000,
            'avg_receivables': 17800000000
        })

    def test_start_year_month_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_credit_card.fetch_credit_card_data(start_year=2025, start_month=3)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['quarter'], '2025-Q1')

    def test_end_year_month_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_credit_card.fetch_credit_card_data(end_year=2024, end_month=6)
            self.assertEqual(len(result), 2)
            self.assertEqual(result[0]['quarter'], '2024-Q2')
            self.assertEqual(result[-1]['quarter'], '2024-Q1')

    def test_both_year_month_filters(self):
        with patch('urllib.request.urlopen', 
                  return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_credit_card.fetch_credit_card_data(
                start_year=2024, start_month=6,
                end_year=2024, end_month=12
            )
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]['quarter'], '2024-Q4')
            self.assertEqual(result[-1]['quarter'], '2024-Q2')

    def test_start_year_only_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_credit_card.fetch_credit_card_data(start_year=2025)
            self.assertEqual(len(result), 1)
            self.assertEqual(result[0]['quarter'], '2025-Q1')

    def test_end_year_only_filter(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_credit_card.fetch_credit_card_data(end_year=2024)
            self.assertEqual(len(result), 4)
            self.assertEqual(result[0]['quarter'], '2024-Q4')
            self.assertEqual(result[-1]['quarter'], '2024-Q1')

    def test_get_credit_card_stats(self):
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.JSON_DATA.encode('utf-8'))()):
            result = tool_credit_card.get_credit_card_stats()
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]['quarter'], '2025-Q1')

if __name__ == '__main__':
    unittest.main()
