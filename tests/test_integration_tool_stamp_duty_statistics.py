"""Integration tests for the Stamp Duty Statistics tool."""

import unittest
from unittest.mock import Mock
from fastmcp import FastMCP
from hkopenai.hk_finance_mcp_server import tool_stamp_duty_statistics


class TestStampDutyStatisticsIntegration(unittest.TestCase):
    """Integration test class for verifying Stamp Duty Statistics tool functionality."""

    def setUp(self):
        self.mcp = Mock(spec=FastMCP)
        tool_stamp_duty_statistics.register(self.mcp)
        self.get_stamp_duty_statistics_tool = self.mcp.tool.return_value.call_args[0][0]

    def test_get_stamp_duty_statistics(self):
        """Test fetching stamp duty statistics from HKMA API."""
        try:
            result = self.get_stamp_duty_statistics_tool()
            self.assertIsInstance(result, list)
            self.assertTrue(
                len(result) > 0, "Expected to fetch at least one stamp duty record"
            )
            self.assertIn("period", result[0], "Expected 'period' field in result")
            self.assertIn(
                "sd_listed", result[0], "Expected 'sd_listed' field in result"
            )
            self.assertIn(
                "sd_unlisted", result[0], "Expected 'sd_unlisted' field in result"
            )
        except Exception as e:
            self.fail(f"Failed to fetch stamp duty statistics: {str(e)}")

    def test_get_stamp_duty_statistics_with_period_filter(self):
        """Test fetching stamp duty statistics with period filter from the live API."""
        try:
            result = self.get_stamp_duty_statistics_tool(
                start_period="202501", end_period="202502"
            )
            self.assertIsInstance(result, list)
            self.assertTrue(
                len(result) > 0,
                "Expected to fetch at least one stamp duty record within the period range",
            )
            for record in result:
                self.assertTrue(
                    "202501" <= record["period"] <= "202502",
                    "Expected all results to be within the specified period range",
                )
        except Exception as e:
            self.fail(
                f"Failed to fetch stamp duty statistics with period filter: {str(e)}"
            )


if __name__ == "__main__":
    unittest.main()
