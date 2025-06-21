import unittest
from unittest.mock import patch, mock_open
import json
from hkopenai.hk_finance_mcp_server import tool_hkma_tender

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

    @patch('urllib.request.urlopen')
    def test_invalid_json_data(self, mock_urlopen):
        # Test handling of invalid JSON data
        invalid_json = "{invalid json}"
        mock_urlopen.return_value = mock_open(read_data=invalid_json.encode('utf-8'))()
        
        with self.assertRaises(Exception) as context:
            tool_hkma_tender.fetch_tender_invitations()
        self.assertTrue("JSON" in str(context.exception) or "decode" in str(context.exception), "Expected JSON decode error")

    @patch('urllib.request.urlopen')
    def test_empty_json_data(self, mock_urlopen):
        # Test handling of empty JSON data
        empty_json = "{}"
        mock_urlopen.return_value = mock_open(read_data=empty_json.encode('utf-8'))()
        
        result = tool_hkma_tender.fetch_tender_invitations()
        self.assertEqual(len(result), 0, "Expected empty result for empty JSON data")

    @patch('urllib.request.urlopen')
    def test_missing_records_in_json(self, mock_urlopen):
        # Test handling of JSON data with missing records
        missing_records_json = {
            "header": {"success": True},
            "result": {
                "datasize": 0,
                "records": []
            }
        }
        mock_urlopen.return_value = mock_open(read_data=json.dumps(missing_records_json).encode('utf-8'))()
        
        result = tool_hkma_tender.fetch_tender_invitations()
        self.assertEqual(len(result), 0, "Expected empty result for JSON with no records")

    @patch('urllib.request.urlopen')
    def test_incomplete_record_data(self, mock_urlopen):
        # Test handling of JSON data with incomplete records
        incomplete_record_json = {
            "header": {"success": True},
            "result": {
                "datasize": 1,
                "records": [
                    {
                        "title": "Incomplete Tender"
                        # Missing other fields
                    }
                ]
            }
        }
        mock_urlopen.return_value = mock_open(read_data=json.dumps(incomplete_record_json).encode('utf-8'))()
        
        result = tool_hkma_tender.fetch_tender_invitations()
        self.assertEqual(len(result), 1, "Expected result with partial data to be processed")
        self.assertIn("title", result[0], "Expected 'title' to be present in result")
        self.assertNotIn("link", result[0], "Expected missing fields to not be in result")

    def test_invalid_parameters(self):
        # Test handling of invalid parameters
        def create_mock_response():
            return mock_open(read_data=json.dumps(self.MOCK_JSON).encode('utf-8'))()
        
        with patch('urllib.request.urlopen', side_effect=lambda *args, **kwargs: create_mock_response()):
            # Test invalid language (using empty string as a placeholder for invalid input)
            result = tool_hkma_tender.fetch_tender_invitations(lang='')
            self.assertEqual(len(result), 2, "Expected full data set when language is empty")

            # Test invalid segment (using empty string as a placeholder for invalid input)
            result = tool_hkma_tender.fetch_tender_invitations(segment='')
            self.assertEqual(len(result), 2, "Expected full data set when segment is empty")
            
            # Test invalid pagesize (using None as a placeholder for invalid input)
            result = tool_hkma_tender.fetch_tender_invitations(pagesize=None)
            self.assertEqual(len(result), 2, "Expected full data set when pagesize is None")
            
            # Test invalid offset (using None as a placeholder for invalid input)
            result = tool_hkma_tender.fetch_tender_invitations(offset=None)
            self.assertEqual(len(result), 2, "Expected full data set when offset is None")
            
            # Test invalid from_date format (using None as a placeholder for invalid input)
            result = tool_hkma_tender.fetch_tender_invitations(from_date=None)
            self.assertEqual(len(result), 2, "Expected full data set when from_date is None")

    def test_boundary_parameters(self):
        # Test boundary conditions for parameters.
        def create_mock_response():
            return mock_open(read_data=json.dumps(self.MOCK_JSON).encode('utf-8'))()
                
        with patch('urllib.request.urlopen', side_effect=lambda *args, **kwargs: create_mock_response()):
            # Test very large pagesize
            result = tool_hkma_tender.fetch_tender_invitations(pagesize=1000)
            self.assertEqual(len(result), 2, "Expected data even with very large pagesize")
            
            # Test zero offset
            result = tool_hkma_tender.fetch_tender_invitations(offset=0)
            self.assertEqual(len(result), 2, "Expected data with zero offset")
            
if __name__ == '__main__':
    unittest.main()
