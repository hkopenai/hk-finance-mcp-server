"""Integration tests for the Licensed Banks Historical Data tool."""

import unittest
from unittest.mock import Mock
from fastmcp import FastMCP
from hkopenai.hk_finance_mcp_server.tools import licensed_banks_historical


class TestLicensedBanksHistoricalIntegration(unittest.TestCase):
    """Integration test class for verifying Licensed Banks Historical Data tool functionality."""

    def setUp(self):
        self.mcp = Mock(spec=FastMCP)
        licensed_banks_historical.register(self.mcp)
        self.get_licensed_banks_historical_data_tool = self.mcp.tool.return_value.call_args[0][0]

    def test_get_licensed_banks_historical_data(self):
        """Test fetching licensed banks historical data from AOF API."""
        try:
            data = self.get_licensed_banks_historical_data_tool()
            self.assertIsInstance(data, list)
            if data:
                self.assertIsInstance(data[0], dict)
                self.assertIn("year", data[0])
                # Check if it's an error response
                if "error" not in data[0]:
                    self.assertIn("licensed_banks", data[0])
                    self.assertIn("bank_branches", data[0])
                    self.assertIn("bank_offices", data[0])
        except Exception as e:
            self.fail(f"Failed to fetch licensed banks historical data: {str(e)}")

    def test_get_licensed_banks_historical_data_with_year_range(self):
        """Test fetching licensed banks historical data with year range from AOF API."""
        try:
            data = self.get_licensed_banks_historical_data_tool(
                start_year=1980, end_year=2000
            )
            self.assertIsInstance(data, list)
            if data:
                for record in data:
                    self.assertIsInstance(record, dict)
                    self.assertIn("year", record)
                    year = int(record["year"])
                    self.assertTrue(year >= 1980 and year <= 2000)
        except Exception as e:
            self.fail(f"Failed to fetch licensed banks historical data with year range: {str(e)}")

    def test_get_licensed_banks_historical_data_licensed_banks_only(self):
        """Test fetching only licensed banks data from AOF API."""
        try:
            data = self.get_licensed_banks_historical_data_tool(data_type="licensed_banks")
            self.assertIsInstance(data, list)
            if data:
                for record in data:
                    self.assertIsInstance(record, dict)
                    self.assertIn("year", record)
                    self.assertIn("licensed_banks", record)
                    # Should only have year and licensed_banks fields
                    self.assertEqual(len(record.keys()), 2)
        except Exception as e:
            self.fail(f"Failed to fetch licensed banks only data: {str(e)}")

    def test_get_licensed_banks_historical_data_bank_branches_only(self):
        """Test fetching only bank branches data from AOF API."""
        try:
            data = self.get_licensed_banks_historical_data_tool(data_type="bank_branches")
            self.assertIsInstance(data, list)
            if data:
                for record in data:
                    self.assertIsInstance(record, dict)
                    self.assertIn("year", record)
                    self.assertIn("bank_branches", record)
                    # Should only have year and bank_branches fields
                    self.assertEqual(len(record.keys()), 2)
        except Exception as e:
            self.fail(f"Failed to fetch bank branches only data: {str(e)}")

    def test_get_licensed_banks_historical_data_bank_offices_only(self):
        """Test fetching only bank offices data from AOF API."""
        try:
            data = self.get_licensed_banks_historical_data_tool(data_type="bank_offices")
            self.assertIsInstance(data, list)
            if data:
                for record in data:
                    self.assertIsInstance(record, dict)
                    self.assertIn("year", record)
                    self.assertIn("bank_offices", record)
                    # Should only have year and bank_offices fields
                    self.assertEqual(len(record.keys()), 2)
        except Exception as e:
            self.fail(f"Failed to fetch bank offices only data: {str(e)}")

    def test_get_licensed_banks_historical_data_with_language(self):
        """Test fetching licensed banks historical data with language parameter from AOF API."""
        try:
            data = self.get_licensed_banks_historical_data_tool(lang="tc")
            self.assertIsInstance(data, list)
            if data:
                self.assertIsInstance(data[0], dict)
                self.assertIn("year", data[0])
        except Exception as e:
            self.fail(f"Failed to fetch licensed banks historical data with language: {str(e)}")


if __name__ == "__main__":
    unittest.main() 