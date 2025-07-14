"""Integration tests for the Coin Cart tool."""

import unittest
from hkopenai.hk_finance_mcp_server.tool_coin_cart import fetch_coin_cart_schedule


class TestCoinCartIntegration(unittest.TestCase):
    """Integration test class for verifying Coin Cart tool functionality."""

    def setUp(self):
        # Temporarily bypass environment variable check for debugging
        self.run_integration_tests = True
        # Original check: self.run_integration_tests = os.getenv('RUN_INTEGRATION_TESTS', 'false').lower() == 'true'
        # if not self.run_integration_tests:
        #     self.skipTest("Integration tests are disabled. Set RUN_INTEGRATION_TESTS=true to enable.")

    def test_fetch_coin_cart_schedule_live(self):
        """Test fetching coin cart schedule data from live API."""
        if not self.run_integration_tests:
            return

        try:
            # Fetch data with default parameters
            result = fetch_coin_cart_schedule()
            self.assertIsInstance(result, dict)
            self.assertTrue("header" in result, "Expected 'header' key in result")
            self.assertTrue("result" in result, "Expected 'result' key in result")

            try:
                header = result["header"]
                self.assertTrue("success" in header, "Expected 'success' key in header")
            except KeyError as ke:
                self.fail(f"Missing expected key in header: {str(ke)}")

            try:
                result_data = result["result"]
                self.assertTrue(
                    "records" in result_data, "Expected 'records' key in result"
                )
                records = result_data["records"]
                self.assertGreater(
                    len(records), 0, "Expected non-empty records from live API"
                )
            except KeyError as ke:
                self.fail(f"Missing expected key in result: {str(ke)}")
        except Exception as e:
            self.fail(f"Live API call failed with exception: {str(e)}")


if __name__ == "__main__":
    unittest.main()
