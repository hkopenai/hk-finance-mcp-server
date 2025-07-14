"""Integration tests for the fraudulent bank scams tool."""

import unittest
from unittest.mock import Mock
from fastmcp import FastMCP
from hkopenai.hk_finance_mcp_server import tool_fraudulent_bank_scams


class TestFraudulentBankScamsIntegration(unittest.TestCase):
    """Integration test class for verifying fraudulent bank scams tool functionality."""

    def setUp(self):
        self.mcp = Mock(spec=FastMCP)
        tool_fraudulent_bank_scams.register(self.mcp)
        # The tool decorator calls mcp.tool() which returns a callable, then that callable is called with the function.
        # So, we need to access the call_args of the *returned* mock object.
        self.get_fraudulent_bank_scams_tool = self.mcp.tool.return_value.call_args[0][0]

    def test_get_fraudulent_bank_scams(self):
        """Test fetching fraudulent bank scams data from HKMA API."""
        try:
            result = self.get_fraudulent_bank_scams_tool(lang="en")
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
        """Test fetching data in a different language."""
        try:
            result = self.get_fraudulent_bank_scams_tool(lang="tc")
            self.assertIsInstance(result, list)
        except Exception as e:
            self.fail(
                f"Failed to fetch fraudulent bank scams data in Traditional Chinese: {str(e)}"
            )


if __name__ == "__main__":
    unittest.main()
