import unittest
from hkopenai.hk_finance_mcp_server import tool_hibor_daily

class TestHiborDailyIntegration(unittest.TestCase):
    def test_integration_fetch_hibor_daily_data(self):
        """Test integration of fetching HIBOR daily data"""
        data = tool_hibor_daily.fetch_hibor_daily_data()
        self.assertIsInstance(data, list)
        if data:
            self.assertIsInstance(data[0], dict)
            self.assertIn('date', data[0])
            self.assertIn('overnight', data[0])

    def test_integration_fetch_hibor_daily_data_with_date_range(self):
        """Test integration of fetching HIBOR daily data with date range"""
        data = tool_hibor_daily.fetch_hibor_daily_data(start_date="2025-05-01", end_date="2025-05-31")
        self.assertIsInstance(data, list)
        if data:
            for record in data:
                self.assertIsInstance(record, dict)
                self.assertIn('date', record)
                date_str = record['date']
                self.assertTrue(date_str >= "2025-05-01" and date_str <= "2025-05-31")

    def test_integration_get_hibor_stats(self):
        """Test integration of getting HIBOR stats"""
        stats = tool_hibor_daily.get_hibor_stats()
        self.assertIsInstance(stats, list)
        if stats:
            self.assertIsInstance(stats[0], dict)
            self.assertIn('date', stats[0])

if __name__ == '__main__':
    unittest.main()
