import unittest
from unittest.mock import patch, mock_open
import tools

class TestBusinessReturns(unittest.TestCase):
    CSV_DATA = """RUN_DATE,ACTIVE_MAIN_BUS,NEW_REG_MAIN_BUS
202505,1604714,17497
202504,1598085,16982
202503,1591678,18435
202502,1588258,13080
202501,1585520,14115
202412,1583802,14429
202411,1578590,16481
202410,1574431,15081
202409,1574259,13384
202408,1575333,15070
202407,1580017,15076
202406,1580230,13984
202405,1579564,15373
202404,1576889,13149
202403,1577907,15495
202402,1578619,8129
202401,1587450,12588
202312,1585721,12020
202311,1585292,13150
"""

    def setUp(self):
        self.mock_urlopen = patch('urllib.request.urlopen').start()
        self.mock_urlopen.return_value = mock_open(read_data=self.CSV_DATA.encode('utf-8'))()
        self.addCleanup(patch.stopall)

    @patch('urllib.request.urlopen')
    def test_fetch_business_returns_data(self, mock_urlopen):
        # Mock the URL response
        mock_urlopen.return_value = mock_open(read_data=self.CSV_DATA.encode('utf-8'))()
        
        # Call the function
        result = tools.fetch_business_returns_data()
        
        # Verify the result
        self.assertEqual(len(result), 19)
        self.assertEqual(result[0], {
            'year_month': '2025-05',
            'active_business': 1604714,
            'new_registered_business': 17497
        })
        self.assertEqual(result[-1], {
            'year_month': '2023-11',
            'active_business': 1585292,
            'new_registered_business': 13150
        })

    def test_start_year_month_filter(self):
        # Test start year/month filter
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.CSV_DATA.encode('utf-8'))()):
            # Test start year/month filter
            result = tools.fetch_business_returns_data(start_year=2025, start_month=3)
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]['year_month'], '2025-05')

    def test_end_year_month_filter(self):
        # Test end year/month filter
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.CSV_DATA.encode('utf-8'))()):
            # Test end year/month filter
            result = tools.fetch_business_returns_data(end_year=2025, end_month=3)
            self.assertEqual(len(result), 19)
            self.assertEqual(result[-1]['year_month'], '2023-11')

    def test_both_year_month_filters(self):
        # Test both filters
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.CSV_DATA.encode('utf-8'))()):
            # Test both filters
            result = tools.fetch_business_returns_data(
                start_year=2025, start_month=2,
                end_year=2025, end_month=4
            )
            self.assertEqual(len(result), 3)
            self.assertEqual(result[0]['year_month'], '2025-04')
            self.assertEqual(result[-1]['year_month'], '2025-02')

    def test_start_year_only_filter(self):
        # Test start year only filter
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.CSV_DATA.encode('utf-8'))()):
            result = tools.fetch_business_returns_data(start_year=2025)
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]['year_month'], '2025-05')
            self.assertEqual(result[-1]['year_month'], '2025-01')

    def test_end_year_only_filter(self):
        # Test end year only filter
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.CSV_DATA.encode('utf-8'))()):
            result = tools.fetch_business_returns_data(end_year=2025)
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]['year_month'], '2025-05')
            self.assertEqual(result[-1]['year_month'], '2025-01')

    def test_both_year_only_filters(self):
        # Test both year only filters
        with patch('urllib.request.urlopen', return_value=mock_open(read_data=self.CSV_DATA.encode('utf-8'))()):
            result = tools.fetch_business_returns_data(
                start_year=2025,
                end_year=2025
            )
            self.assertEqual(len(result), 5)
            self.assertEqual(result[0]['year_month'], '2025-05')
            self.assertEqual(result[-1]['year_month'], '2025-01')

if __name__ == '__main__':
    unittest.main()
