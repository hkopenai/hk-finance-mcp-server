import unittest
from unittest.mock import patch, mock_open
import json
from hk_finance_mcp_server import tool_coin_cart

class TestCoinCartSchedule(unittest.TestCase):
    MOCK_JSON = {
        "result": {
            "records": [
                {
                    "date": "2025-06-10",
                    "district": "Central and Western",
                    "location": "Central (near Star Ferry Pier)",
                    "start_time": "10:00",
                    "end_time": "17:00",
                    "service_hours": "10:00 - 17:00"
                },
                {
                    "date": "2025-06-11",
                    "district": "Wan Chai",
                    "location": "Wan Chai (near MTR Station)",
                    "start_time": "09:30",
                    "end_time": "16:30",
                    "service_hours": "09:30 - 16:30"
                },
                {
                    "date": "2025-06-12",
                    "district": "Eastern",
                    "location": "Quarry Bay (near MTR Station)",
                    "start_time": "11:00",
                    "end_time": "18:00",
                    "service_hours": "11:00 - 18:00"
                }
            ]
        }
    }

    def setUp(self):
        self.mock_urlopen = patch('urllib.request.urlopen').start()
        mock_response = mock_open(read_data=json.dumps(self.MOCK_JSON).encode('utf-8'))
        self.mock_urlopen.return_value = mock_response()
        self.addCleanup(patch.stopall)

    def test_fetch_coin_cart_schedule(self):
        result = tool_coin_cart.fetch_coin_cart_schedule()
        
        self.assertEqual(len(result), 1)

    def test_get_coin_cart_schedule(self):
        result = tool_coin_cart.get_coin_cart_schedule()
        
        self.assertIn('coin_cart_schedule', result)

    @patch('urllib.request.urlopen')
    def test_api_error_handling(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            tool_coin_cart.fetch_coin_cart_schedule()

if __name__ == '__main__':
    unittest.main()
