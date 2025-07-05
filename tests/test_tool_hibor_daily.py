"""
Module for testing the HIBOR Daily tool functionality.

This module contains unit tests to verify the correct fetching of daily HIBOR
(Hong Kong Interbank Offered Rate) data from the HKMA API using the tool_hibor_daily module.
"""

import unittest
from hkopenai.hk_finance_mcp_server import tool_hibor_daily


class TestHiborDailyTool(unittest.TestCase):
    """Test case class for verifying HIBOR Daily tool functionality."""
    def test_fetch_hibor_daily_data(self):
        """Test fetching HIBOR daily data without filters.
        
        Verifies that the fetch_hibor_daily_data function returns a list of data
        with expected keys when no filters are applied.
        """
        data = tool_hibor_daily.fetch_hibor_daily_data()
        self.assertIsInstance(data, list)
        if data:
            self.assertIsInstance(data[0], dict)
            self.assertIn("date", data[0])
            self.assertIn("overnight", data[0])

    def test_fetch_hibor_daily_data_with_date_range(self):
        """Test fetching HIBOR daily data with date range filter.
        
        Verifies that the fetch_hibor_daily_data function returns a list of data
        within the specified date range.
        """
        data = tool_hibor_daily.fetch_hibor_daily_data(
            start_date="2025-05-01", end_date="2025-05-31"
        )
        self.assertIsInstance(data, list)
        if data:
            for record in data:
                self.assertIsInstance(record, dict)
                self.assertIn("date", record)
                date_str = record["date"]
                self.assertTrue(date_str >= "2025-05-01" and date_str <= "2025-05-31")

    def test_get_hibor_stats(self):
        """Test getting HIBOR stats without filters.
        
        Verifies that the get_hibor_stats function returns a list of statistical data
        with expected keys.
        """
        stats = tool_hibor_daily.get_hibor_stats()
        self.assertIsInstance(stats, list)
        if stats:
            self.assertIsInstance(stats[0], dict)
            self.assertIn("date", stats[0])


if __name__ == "__main__":
    unittest.main()
