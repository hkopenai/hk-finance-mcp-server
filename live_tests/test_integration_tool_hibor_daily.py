"""Integration tests for the HIBOR Daily tool."""

import unittest
from unittest.mock import Mock
from fastmcp import FastMCP
from live_tests._live_helpers import call_with_retry_on_empty
from hkopenai.hk_finance_mcp_server.tools import hibor_daily


class TestHiborDailyIntegration(unittest.TestCase):
    """Integration test class for verifying HIBOR Daily tool functionality."""

    def setUp(self):
        self.mcp = Mock(spec=FastMCP)
        hibor_daily.register(self.mcp)
        self.get_hibor_daily_stats_tool = self.mcp.tool.return_value.call_args[0][0]

    def test_get_hibor_daily_stats(self):
        """Test fetching HIBOR daily stats from HKMA API."""
        stats = call_with_retry_on_empty(self.get_hibor_daily_stats_tool)
        self.assertIsInstance(stats, list)
        self.assertIsInstance(stats[0], dict)
        self.assertIn("date", stats[0])
        self.assertIn("overnight", stats[0])

    def test_get_hibor_daily_stats_with_date_range(self):
        """Test fetching HIBOR daily stats with date range from HKMA API."""
        stats = call_with_retry_on_empty(
            self.get_hibor_daily_stats_tool,
            start_date="2025-01-01",
            end_date="2025-01-31",
        )
        self.assertIsInstance(stats, list)
        for record in stats:
            self.assertIsInstance(record, dict)
            self.assertIn("date", record)
            date_str = record["date"]
            self.assertTrue("2025-01-01" <= date_str <= "2025-01-31")


if __name__ == "__main__":
    unittest.main()
