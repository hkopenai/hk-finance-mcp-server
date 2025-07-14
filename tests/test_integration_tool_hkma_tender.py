"""Integration tests for the HKMA Tender Invitations tool."""

import unittest
from hkopenai.hk_finance_mcp_server.tool_hkma_tender import fetch_tender_invitations


class TestHKMATenderIntegration(unittest.TestCase):
    """Integration test class for verifying HKMA Tender Invitations tool functionality."""

    def setUp(self):
        # Temporarily bypass environment variable check for debugging
        self.run_integration_tests = True
        # Original check: self.run_integration_tests = os.getenv('RUN_INTEGRATION_TESTS', 'false').lower() == 'true'
        # if not self.run_integration_tests:
        #     self.skipTest("Integration tests are disabled. Set RUN_INTEGRATION_TESTS=true to enable.")

    def test_fetch_tender_invitations_live(self):
        """Test fetching HKMA tender invitations from live API."""
        if not self.run_integration_tests:
            return

        try:
            # Fetch data with default parameters
            result = fetch_tender_invitations()
            self.assertIsInstance(result, list)
            self.assertGreater(
                len(result), 0, "Expected non-empty result from live API"
            )
            self.assertTrue("title" in result[0], "Expected 'title' key in result")
            self.assertTrue("link" in result[0], "Expected 'link' key in result")
            self.assertTrue("date" in result[0], "Expected 'date' key in result")
        except Exception as e:
            self.fail(f"Live API call failed with exception: {str(e)}")

    def test_fetch_tender_invitations_with_pagination_live(self):
        """Test fetching HKMA tender invitations with pagination from live API."""
        if not self.run_integration_tests:
            return

        try:
            # Fetch data with pagination parameters
            result = fetch_tender_invitations(pagesize=5, offset=0)
            self.assertIsInstance(result, list)
            self.assertGreater(
                len(result),
                0,
                "Expected non-empty result from live API with pagination",
            )
            self.assertLessEqual(
                len(result), 5, "Expected result length to respect pagesize parameter"
            )
        except Exception as e:
            self.fail(f"Live API call with pagination failed with exception: {str(e)}")


if __name__ == "__main__":
    unittest.main()
