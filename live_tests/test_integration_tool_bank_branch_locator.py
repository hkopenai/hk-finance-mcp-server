"""Integration tests for the Bank Branch Locator tool."""

import unittest
from live_tests._live_helpers import call_with_retry_on_empty
from hkopenai.hk_finance_mcp_server.tools.bank_branch_locator import (
    _get_bank_branch_locations,
)


class TestBankBranchLocatorIntegration(unittest.TestCase):
    """Integration test class for verifying Bank Branch Locator tool functionality."""

    def test_get_bank_branch_locations_no_filter(self):
        """Test fetching bank branch locations without filters from the live API."""
        result = call_with_retry_on_empty(_get_bank_branch_locations, pagesize=10)
        self.assertIn("district", result[0])
        self.assertIn("bank_name", result[0])
        self.assertIn("branch_name", result[0])
        self.assertIn("address", result[0])

    @unittest.skip(
        "Test skipped due to unknown district naming in API; need to determine correct district name"
    )
    def test_get_bank_branch_locations_with_district_filter(self):
        """Test fetching bank branch locations with district filter from the live API."""
        result = _get_bank_branch_locations(district="Central", pagesize=10)
        self.assertTrue(len(result) > 0, "No bank branches found in Central district")

    def test_get_bank_branch_locations_with_bank_name_filter(self):
        """Test fetching bank branch locations with bank name filter from the live API."""
        result = call_with_retry_on_empty(
            _get_bank_branch_locations,
            bank_name="Hang Seng Bank Limited",
            pagesize=10,
        )
        self.assertEqual(result[0]["bank_name"], "Hang Seng Bank Limited")

    def test_get_bank_branch_locations_language_support(self):
        """Test fetching bank branch locations with language support from the live API."""
        for lang in ["en", "tc", "sc"]:
            with self.subTest(lang=lang):
                result = call_with_retry_on_empty(
                    _get_bank_branch_locations, lang=lang, pagesize=5
                )


if __name__ == "__main__":
    unittest.main()