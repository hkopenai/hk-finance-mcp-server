"""Integration tests for the Negative Equity Residential Mortgage tool."""

import unittest
from live_tests._live_helpers import call_with_retry_on_empty
from hkopenai.hk_finance_mcp_server.tools import neg_resident_mortgage


class TestNegResidentMortgageIntegration(unittest.TestCase):
    """Integration test class for verifying Negative Equity Residential Mortgage tool functionality."""

    def test_fetch_neg_equity_data_live(self):
        """Test fetching negative equity mortgage data from live API."""
        result = call_with_retry_on_empty(neg_resident_mortgage._get_neg_equity_stats)
        self.assertIsInstance(result, list)
        self.assertIn("quarter", result[0], "Expected 'quarter' key in result")
        self.assertIn(
            "outstanding_loans",
            result[0],
            "Expected 'outstanding_loans' key in result",
        )

    def test_fetch_neg_equity_data_with_filters_live(self):
        """Test fetching negative equity mortgage data with filters from live API."""
        result = call_with_retry_on_empty(
            neg_resident_mortgage._get_neg_equity_stats,
            start_year=2023,
            start_month=1,
            end_year=2023,
            end_month=12,
        )
        self.assertIsInstance(result, list)
        for entry in result:
            year = int(entry["quarter"].split("-")[0])
            self.assertEqual(year, 2023, f"Expected data for year 2023, got {year}")


if __name__ == "__main__":
    unittest.main()
