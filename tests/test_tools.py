import unittest
from unittest.mock import patch, mock_open
import tools

class TestBusinessReturns(unittest.TestCase):
    @patch('urllib.request.urlopen')
    def test_fetch_business_returns_data(self, mock_urlopen):
        # Mock CSV data
        csv_data = """RUN_DATE,ACTIVE_MAIN_BUS,NEW_REG_MAIN_BUS
202505,1604714,17497
202504,1598085,16982
202503,1591678,18435
202502,1588258,13080
202501,1585520,14115"""
        
        # Mock the URL response
        mock_urlopen.return_value = mock_open(read_data=csv_data.encode('utf-8'))()
        
        # Call the function
        result = tools.fetch_business_returns_data()
        
        # Verify the result
        self.assertEqual(len(result), 5)
        self.assertEqual(result[0], {
            'year_month': '2025-05',
            'active_business': 1604714,
            'new_registered_business': 17497
        })
        self.assertEqual(result[-1], {
            'year_month': '2025-01',
            'active_business': 1585520,
            'new_registered_business': 14115
        })

    def test_date_filtering(self):
        # Mock CSV data
        csv_data = """RUN_DATE,ACTIVE_MAIN_BUS,NEW_REG_MAIN_BUS
202505,1604714,17497
202504,1598085,16982
202503,1591678,18435
202502,1588258,13080
202501,1585520,14115"""
        
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=csv_data.encode('utf-8'))()):
            # Test start date filter
            result = tools.fetch_business_returns_data(start_date='202503')
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]['year_month'], '2025-05')
            
            # Test end date filter
            result = tools.fetch_business_returns_data(end_date='202503')
            self.assertEqual(len(result), 3)
            self.assertEqual(result[-1]['year_month'], '2025-01')
            
            # Test both filters
            result = tools.fetch_business_returns_data(start_date='202502', end_date='202504')
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]['year_month'], '2025-04')
            self.assertEqual(result[-1]['year_month'], '2025-02')

    def test_get_business_return_stats(self):
        # TODO: Add tests for statistics calculation
        pass

if __name__ == '__main__':
    unittest.main()
