import unittest
import json
from unittest.mock import patch, Mock
from hkopenai.hk_finance_mcp_server import tool_bank_branch_locator

class TestBankBranchLocatorTool(unittest.TestCase):
    def setUp(self):
        self.sample_data = '''
{
    "result": {
        "datasize": 2,
        "records": [
            {
                "district": "Central",
                "bank_name": "Test Bank 1",
                "branch_name": "Main Branch",
                "address": "123 Test Street, Central",
                "service_hours": "Mon-Fri, 09:00 - 17:00",
                "latitude": "22.2799",
                "longitude": "114.1588",
                "barrier_free_access": "Wheelchair accessible"
            },
            {
                "district": "Kowloon",
                "bank_name": "Test Bank 2",
                "branch_name": "Kowloon Branch",
                "address": "456 Test Road, Kowloon",
                "service_hours": "Mon-Fri, 09:00 - 17:00",
                "latitude": "22.3169",
                "longitude": "114.1694",
                "barrier_free_access": "Guide dogs welcome"
            }
        ]
    }
}
'''

    @patch('urllib.request.urlopen')
    def test_fetch_bank_branch_data_no_filter(self, mock_urlopen):
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = self.sample_data.encode('utf-8')
        mock_urlopen.return_value = mock_response

        # Act
        result = tool_bank_branch_locator.fetch_bank_branch_data()

        # Assert
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['district'], "Central")
        self.assertEqual(result[1]['bank_name'], "Test Bank 2")

    @patch('urllib.request.urlopen')
    def test_fetch_bank_branch_data_with_district_filter(self, mock_urlopen):
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = self.sample_data.encode('utf-8')
        mock_urlopen.return_value = mock_response

        # Act
        result = tool_bank_branch_locator.fetch_bank_branch_data(district="Central")

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['district'], "Central")

    @patch('urllib.request.urlopen')
    def test_fetch_bank_branch_data_with_bank_name_filter(self, mock_urlopen):
        # Arrange
        mock_response = Mock()
        mock_response.read.return_value = self.sample_data.encode('utf-8')
        mock_urlopen.return_value = mock_response

        # Act
        result = tool_bank_branch_locator.fetch_bank_branch_data(bank_name="Test Bank 2")

        # Assert
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]['bank_name'], "Test Bank 2")

    @patch('urllib.request.urlopen')
    def test_get_bank_branch_locations_empty_result(self, mock_urlopen):
        # Arrange
        empty_data = {"result": {"datasize": 0, "records": []}}
        mock_response = Mock()
        mock_response.read.return_value = json.dumps(empty_data).encode('utf-8')
        mock_urlopen.return_value = mock_response

        # Act
        result = tool_bank_branch_locator.get_bank_branch_locations()

        # Assert
        self.assertEqual(result, [])

if __name__ == '__main__':
    unittest.main()
