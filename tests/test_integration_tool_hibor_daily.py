"""Integration tests for the HIBOR Daily tool."""

import unittest
from unittest.mock import Mock
from fastmcp import FastMCP
from hkopenai.hk_finance_mcp_server import tool_hibor_daily


class TestHiborDailyIntegration(unittest.TestCase):
    """Integration test class for verifying HIBOR Daily tool functionality."""

    def setUp(self):
        self.mcp = Mock(spec=FastMCP)
        tool_hibor_daily.register(self.mcp)
        self.get_hibor_daily_stats_tool = self.mcp.tool.return_value.call_args[0][0]

    def test_get_hibor_daily_stats(self):
        """Test fetching HIBOR daily stats from HKMA API."""
        try:
            stats = self.get_hibor_daily_stats_tool()
            self.assertIsInstance(stats, list)
            if stats:
                self.assertIsInstance(stats[0], dict)
                self.assertIn("date", stats[0])
                self.assertIn("overnight", stats[0])
        except Exception as e:
            self.fail(f"Failed to fetch HIBOR daily stats: {str(e)}")

    def test_get_hibor_daily_stats_with_date_range(self):
        """Test fetching HIBOR daily stats with date range from HKMA API."""
        try:
            stats = self.get_hibor_daily_stats_tool(
                start_date="2025-01-01", end_date="2025-01-31"
            )
            self.assertIsInstance(stats, list)
            if stats:
                for record in stats:
                    self.assertIsInstance(record, dict)
                    self.assertIn("date", record)
                    date_str = record["date"]
                    self.assertTrue(
                        date_str >= "2025-01-01" and date_str <= "2025-01-31"
                    )
        except Exception as e:
            self.fail(f"Failed to fetch HIBOR daily stats with date range: {str(e)}")


if __name__ == "__main__":
    unittest.main()
