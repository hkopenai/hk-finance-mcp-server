import unittest
from unittest.mock import patch, mock_open
import json
from openaihk.hk_finance_mcp_server import tool_hkma_tender

class TestHKMAtender(unittest.TestCase):
    MOCK_JSON = {
        "header": {
            "success": True,
            "err_code": "0000",
            "err_msg": "No error found"
        },
        "result": {
            "datasize": 2,
            "records": [
                {
                    "title": "Provision of BI Application Support",
                    "link": "https://example.com/tender1",
                    "date": "2025-06-01"
                },
                {
                    "title": "Renewal of software for VDI",
                    "link": "https://example.com/tender2", 
                    "date": "2025-05-30"
                }
            ]
        }
    }

    def setUp(self):
        self.mock_urlopen = patch('urllib.request.urlopen').start()
        mock_response = mock_open(read_data=json.dumps(self.MOCK_JSON).encode('utf-8'))
        self.mock_urlopen.return_value = mock_response()
        self.addCleanup(patch.stopall)

    def test_fetch_tender_invitations(self):
        result = tool_hkma_tender.fetch_tender_invitations()
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]['title'], "Provision of BI Application Support")

    def test_fetch_tender_invitations_with_params(self):
        result = tool_hkma_tender.fetch_tender_invitations(
            lang='tc',
            segment='notice',
            pagesize=10,
            from_date='2025-01-01'
        )
        self.assertEqual(len(result), 2)

    def test_get_tender_invitations(self):
        result = tool_hkma_tender.get_tender_invitations()
        self.assertIn('tender_invitations', result)
        self.assertEqual(len(result['tender_invitations']), 2)

    @patch('urllib.request.urlopen')
    def test_api_error_handling(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("API Error")
        
        with self.assertRaises(Exception):
            tool_hkma_tender.fetch_tender_invitations()

if __name__ == '__main__':
    unittest.main()
