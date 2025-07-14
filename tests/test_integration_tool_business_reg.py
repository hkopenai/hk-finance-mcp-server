"""Integration tests for the Business Registration tool."""

import unittest
from hkopenai.hk_finance_mcp_server.tool_business_reg import fetch_business_returns_data


class TestBusinessReturnsIntegration(unittest.TestCase):
    """Integration test class for verifying Business Registration tool functionality."""

    def setUp(self):
        # Temporarily bypass environment variable check for debugging
        self.run_integration_tests = True
        # Original check: self.run_integration_tests = os.getenv('RUN_INTEGRATION_TESTS', 'false').lower() == 'true'
        # if not self.run_integration_tests:
        #     self.skipTest("Integration tests are disabled. Set RUN_INTEGRATION_TESTS=true to enable.")

    def test_fetch_business_returns_data_live(self):
        """Test fetching business registration data from live API."""
        if not self.run_integration_tests:
            return

        try:
            # Fetch data with default parameters
            result = fetch_business_returns_data()
            self.assertIsInstance(result, list)
            self.assertGreater(
                len(result), 0, "Expected non-empty result from live API"
            )
            self.assertIn(
                "year_month", result[0], "Expected 'year_month' key in result"
            )
            self.assertIn(
                "active_business", result[0], "Expected 'active_business' key in result"
            )
            self.assertIn(
                "new_registered_business",
                result[0],
                "Expected 'new_registered_business' key in result",
            )
        except Exception as e:
            self.fail(f"Live API call failed with exception: {str(e)}")

    def test_fetch_business_returns_data_with_filters_live(self):
        """Test fetching business registration data with filters from live API."""
        if not self.run_integration_tests:
            return

        try:
            # Fetch data with a specific time range
            result = fetch_business_returns_data(
                start_year=2023, start_month=1, end_year=2023, end_month=12
            )
            self.assertIsInstance(result, list)
            self.assertGreater(
                len(result), 0, "Expected non-empty result from live API with filters"
            )
            for entry in result:
                year = int(entry["year_month"].split("-")[0])
                self.assertEqual(year, 2023, f"Expected data for year 2023, got {year}")
        except Exception as e:
            self.fail(f"Live API call with filters failed with exception: {str(e)}")


if __name__ == "__main__":
    unittest.main()
