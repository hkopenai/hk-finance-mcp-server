"""Integration tests for the Credit Card tool."""

import unittest
from hkopenai.hk_finance_mcp_server.tool_credit_card import fetch_credit_card_data


class TestCreditCardIntegration(unittest.TestCase):
    """Integration test class for verifying Credit Card tool functionality."""

    def setUp(self):
        # Temporarily bypass environment variable check for debugging
        self.run_integration_tests = True
        # Original check: self.run_integration_tests = os.getenv('RUN_INTEGRATION_TESTS', 'false').lower() == 'true'
        # if not self.run_integration_tests:
        #     self.skipTest("Integration tests are disabled. Set RUN_INTEGRATION_TESTS=true to enable.")

    def test_fetch_credit_card_data_live(self):
        """Test fetching credit card data from live API."""
        if not self.run_integration_tests:
            return

        try:
            # Fetch data with default parameters
            result = fetch_credit_card_data()
            self.assertIsInstance(result, list)
            self.assertGreater(
                len(result), 0, "Expected non-empty result from live API"
            )
            self.assertTrue("quarter" in result[0], "Expected 'quarter' key in result")
            self.assertTrue(
                "accounts_count" in result[0], "Expected 'accounts_count' key in result"
            )
        except Exception as e:
            self.fail(f"Live API call failed with exception: {str(e)}")

    def test_fetch_credit_card_data_with_filters_live(self):
        """Test fetching credit card data with filters from live API."""
        if not self.run_integration_tests:
            return

        try:
            # Fetch data with a specific time range
            result = fetch_credit_card_data(
                start_year=2023, start_month=1, end_year=2023, end_month=12
            )
            self.assertIsInstance(result, list)
            self.assertGreater(
                len(result), 0, "Expected non-empty result from live API with filters"
            )
            for entry in result:
                year = int(entry["quarter"].split("-")[0])
                self.assertEqual(year, 2023, f"Expected data for year 2023, got {year}")
        except Exception as e:
            self.fail(f"Live API call with filters failed with exception: {str(e)}")


if __name__ == "__main__":
    unittest.main()
