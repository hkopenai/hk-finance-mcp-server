"""Integration tests for the HKMA Tender Invitations tool."""

import unittest
from live_tests._live_helpers import call_with_retry_on_empty
from hkopenai.hk_finance_mcp_server.tools import hkma_tender


class TestHKMATenderIntegration(unittest.TestCase):
    """Integration test class for verifying HKMA Tender Invitations tool functionality."""

    def test_fetch_tender_invitations_live(self):
        """Test fetching HKMA tender invitations from live API."""
        result = call_with_retry_on_empty(hkma_tender._get_tender_invitations)
        self.assertIsInstance(result, list)
        self.assertIn("title", result[0], "Expected 'title' key in result")
        self.assertIn("link", result[0], "Expected 'link' key in result")
        self.assertIn("date", result[0], "Expected 'date' key in result")

    def test_fetch_tender_invitations_with_pagination_live(self):
        """Test fetching HKMA tender invitations with pagination from live API."""
        result = call_with_retry_on_empty(
            hkma_tender._get_tender_invitations, pagesize=5, offset=0
        )
        self.assertIsInstance(result, list)
        self.assertLessEqual(
            len(result), 5, "Expected result length to respect pagesize parameter"
        )


if __name__ == "__main__":
    unittest.main()
