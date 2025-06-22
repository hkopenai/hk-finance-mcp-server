import unittest
import json
from unittest.mock import patch, Mock
from hkopenai.hk_finance_mcp_server import tool_atm_locator

class TestAtmLocatorTool(unittest.TestCase):
    def setUp(self):
        self.sample_data = {
            "result": {
                "records": [
                    {
                        "district": "YuenLong",
                        "bank_name": "Industrial and Commercial Bank of China (Asia) Limited",
                        "type_of_machine": "Automatic Teller Machine",
                        "function": "Cash withdrawal, Cardless withdrawal",
                        "currencies_supported": "HKD, RMB",
                        "barrier_free_access": "Voice navigation, Suitable height ATM for wheelchair users",
                        "network": "JETCO, PLUS, CIRRUS, CUP, VISA, MASTER, DISCOVER, DINER",
                        "address": "No.7, 2/F, T Town South, Tin Chung Court, 30 Tin Wah Road, Tin Shui Wai, Yuen Long, N.T.",
                        "service_hours": "24 hours",
                        "latitude": "22.461655",
                        "longitude": "113.997757"
                    }
                ]
            }
        }

    @patch('urllib.request.urlopen')
    def test_fetch_atm_locator_data(self, mock_urlopen):
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode('utf-8')
        mock_urlopen.return_value = mock_response

        result = tool_atm_locator.fetch_atm_locator_data(pagesize=1, offset=0)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['district'], "YuenLong")
        self.assertEqual(result[0]['bank_name'], "Industrial and Commercial Bank of China (Asia) Limited")

    @patch('urllib.request.urlopen')
    def test_fetch_atm_locator_data_with_filters(self, mock_urlopen):
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(self.sample_data).encode('utf-8')
        mock_urlopen.return_value = mock_response

        result = tool_atm_locator.fetch_atm_locator_data(district="YuenLong", bank_name="Industrial and Commercial Bank of China (Asia) Limited", pagesize=1, offset=0)
        
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['district'], "YuenLong")

        result = tool_atm_locator.fetch_atm_locator_data(district="Central", pagesize=1, offset=0)
        self.assertEqual(len(result), 0)

if __name__ == '__main__':
    unittest.main()
