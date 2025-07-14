"""
Module for testing the HIBOR Daily tool functionality.

This module contains unit tests to verify the correct fetching of daily HIBOR
(Hong Kong Interbank Offered Rate) data from the HKMA API using the tool_hibor_daily module.
"""

import unittest
from unittest.mock import patch, MagicMock
from hkopenai.hk_finance_mcp_server.tool_hibor_daily import _get_hibor_stats, register


class TestHiborDailyTool(unittest.TestCase):
    """Test case class for verifying HIBOR Daily tool functionality."""

    @patch("hkopenai.hk_finance_mcp_server.tool_hibor_daily.fetch_hibor_daily_data")
    def test_get_hibor_stats(self, mock_fetch_hibor_daily_data):
        """Test the retrieval and filtering of HIBOR daily stats."""
        mock_fetch_hibor_daily_data.return_value = [
            {"date": "2025-05-01", "overnight": 0.08, "1_week": 0.15},
            {"date": "2025-05-02", "overnight": 0.09, "1_week": 0.16},
        ]

        result = _get_hibor_stats(start_date="2025-05-01", end_date="2025-05-02")
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0]["date"], "2025-05-01")
        self.assertEqual(result[1]["date"], "2025-05-02")
        mock_fetch_hibor_daily_data.assert_called_once_with("2025-05-01", "2025-05-02")

    @patch("hkopenai.hk_finance_mcp_server.tool_hibor_daily.fetch_hibor_daily_data")
    def test_get_hibor_stats_empty_data(self, mock_fetch_hibor_daily_data):
        """Test _get_hibor_stats returns empty list when no data is fetched."""
        mock_fetch_hibor_daily_data.return_value = []
        result = _get_hibor_stats(start_date="2025-01-01", end_date="2025-01-31")
        self.assertEqual(len(result), 0)
        mock_fetch_hibor_daily_data.assert_called_once_with("2025-01-01", "2025-01-31")

    def test_register_tool(self):
        """Test the registration of the get_hibor_daily_stats tool."""
        mock_mcp = MagicMock()

        register(mock_mcp)

        mock_mcp.tool.assert_called_once_with(
            description="Get daily figures of Hong Kong Interbank Interest Rates (HIBOR) from HKMA"
        )

        mock_decorator = mock_mcp.tool.return_value
        mock_decorator.assert_called_once()

        decorated_function = mock_decorator.call_args[0][0]
        self.assertEqual(decorated_function.__name__, "get_hibor_daily_stats")

        with patch(
            "hkopenai.hk_finance_mcp_server.tool_hibor_daily._get_hibor_stats"
        ) as mock_get_hibor_stats:
            decorated_function(start_date="2024-01-01", end_date="2024-01-31")
            mock_get_hibor_stats.assert_called_once_with("2024-01-01", "2024-01-31")


if __name__ == "__main__":
    unittest.main()
