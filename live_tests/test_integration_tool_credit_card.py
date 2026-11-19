"""Integration tests for the Credit Card tool."""

import unittest
from live_tests._live_helpers import call_with_retry_on_empty
from hkopenai.hk_finance_mcp_server.tools import credit_card


class TestCreditCardIntegration(unittest.TestCase):
    """Integration test class for verifying Credit Card tool functionality."""

    def test_fetch_credit_card_data_live(self):
        """Test fetching credit card data from live API."""
        result = call_with_retry_on_empty(credit_card._get_credit_card_stats)
        self.assertIsInstance(result, list)
        self.assertIn("quarter", result[0], "Expected 'quarter' key in result")
        self.assertIn(
            "accounts_count", result[0], "Expected 'accounts_count' key in result"
        )

    def test_fetch_credit_card_data_with_filters_live(self):
        """Test fetching credit card data with filters from live API."""
        result = call_with_retry_on_empty(
            credit_card._get_credit_card_stats,
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
