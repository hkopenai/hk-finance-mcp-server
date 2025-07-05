"""
Integration tests for the fraudulent bank scams tool.
These tests interact with the actual HKMA API.
"""

import unittest
from hkopenai.hk_finance_mcp_server import tool_fraudulent_bank_scams


class TestFraudulentBankScamsIntegration(unittest.TestCase):
    def test_get_fraudulent_bank_scams(self):
        """Test fetching fraudulent bank scams data from HKMA API"""
        try:
            result = tool_fraudulent_bank_scams.get_fraudulent_bank_scams(lang="en")
            self.assertIsInstance(result, list)
            if result:
                # Check if the structure of the first record is as expected
                record = result[0]
                self.assertIn("issue_date", record)
                self.assertIn("alleged_name", record)
                self.assertIn("scam_type", record)
                self.assertIn("pr_url", record)
                self.assertIn("fraud_website_address", record)
        except Exception as e:
            self.fail(f"Failed to fetch fraudulent bank scams data: {str(e)}")

    def test_get_fraudulent_bank_scams_different_language(self):
        """Test fetching data in a different language"""
        try:
            result = tool_fraudulent_bank_scams.get_fraudulent_bank_scams(lang="tc")
            self.assertIsInstance(result, list)
        except Exception as e:
            self.fail(
                f"Failed to fetch fraudulent bank scams data in Traditional Chinese: {str(e)}"
            )


if __name__ == "__main__":
    unittest.main()
