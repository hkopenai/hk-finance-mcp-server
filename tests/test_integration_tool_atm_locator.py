"""Integration tests for the ATM Locator tool."""

import unittest
from hkopenai.hk_finance_mcp_server import tool_atm_locator


class TestAtmLocatorIntegration(unittest.TestCase):
    """Integration test class for verifying ATM Locator tool functionality."""

    def test_fetch_atm_locator_data_integration(self):
        """Test fetching ATM location data from the live API."""
        result = tool_atm_locator.fetch_atm_locator_data(pagesize=5, offset=0)

        self.assertTrue(len(result) > 0, "Expected to fetch at least one ATM record")
        self.assertIn("district", result[0], "Expected 'district' field in result")
        self.assertIn("bank_name", result[0], "Expected 'bank_name' field in result")
        self.assertIn("address", result[0], "Expected 'address' field in result")

    def test_fetch_atm_locator_data_with_district_filter(self):
        """Test fetching ATM location data with district filter from the live API."""
        result = tool_atm_locator.fetch_atm_locator_data(
            district="YuenLong", pagesize=5, offset=0
        )

        self.assertTrue(
            len(result) > 0, "Expected to fetch at least one ATM record in YuenLong"
        )
        for record in result:
            self.assertEqual(
                record["district"].lower(),
                "yuenlong",
                "Expected all results to be from YuenLong district",
            )


if __name__ == "__main__":
    unittest.main()
