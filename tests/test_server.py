"""
Module for testing the HK OpenAI Finance MCP Server creation.

This module contains unit tests to verify the correct initialization and configuration
of the MCP server with various financial data tools.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_finance_mcp_server.server import create_mcp_server


class TestApp(unittest.TestCase):
    """Test case class for verifying MCP server functionality."""
    @patch("hkopenai.hk_finance_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_business_reg")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_neg_resident_mortgage")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_credit_card")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_coin_cart")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_hkma_tender")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_hibor_daily")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_atm_locator")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_stamp_duty_statistics")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_bank_branch_locator")
    @patch("hkopenai.hk_finance_mcp_server.server.tool_fraudulent_bank_scams")
    def test_create_mcp_server(
        self,
        mock_tool_fraudulent_bank_scams,
        mock_tool_bank_branch_locator,
        mock_tool_stamp_duty_statistics,
        mock_tool_atm_locator,
        mock_tool_hibor_daily,
        mock_tool_hkma_tender,
        mock_tool_coin_cart,
        mock_tool_credit_card,
        mock_tool_neg_resident_mortgage,
        mock_tool_business_reg,
        mock_fastmcp,
    ):
        """Test the creation and configuration of the MCP server with mocked tools.
        
        Verifies that the server is created correctly and all tools are properly registered
        and functional when called.
        """
        # Setup mocks
        mock_server = Mock()

        # Configure mock_server.tool to return a mock that acts as the decorator
        # This mock will then be called with the function to be decorated
        mock_server.tool.return_value = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server = create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        self.assertEqual(server, mock_server)

        # Verify that the tool decorator was called for each tool function
        self.assertEqual(mock_server.tool.call_count, 11)

        # Get all decorated functions
        decorated_funcs = {
            call.args[0].__name__: call.args[0]
            for call in mock_server.tool.return_value.call_args_list
        }
        self.assertEqual(len(decorated_funcs), 11)

        # Call each decorated function and verify that the correct underlying function is called

        decorated_funcs["get_business_stats"](
            start_year=2020, start_month=1, end_year=2020, end_month=12
        )
        mock_tool_business_reg.get_business_stats.assert_called_once_with(
            2020, 1, 2020, 12
        )

        decorated_funcs["get_neg_equity_stats"](
            start_year=2020, start_month=1, end_year=2020, end_month=12
        )
        mock_tool_neg_resident_mortgage.get_neg_equity_stats.assert_called_once_with(
            2020, 1, 2020, 12
        )

        decorated_funcs["get_credit_card_stats"](
            start_year=2020, start_month=1, end_year=2020, end_month=12
        )
        mock_tool_credit_card.get_credit_card_stats.assert_called_once_with(
            2020, 1, 2020, 12
        )

        decorated_funcs["get_coin_cart"]()
        mock_tool_coin_cart.get_coin_cart_schedule.assert_called_once_with()

        decorated_funcs["get_credit_card_hotlines"]()
        mock_tool_credit_card.get_credit_card_hotlines.assert_called_once_with()

        decorated_funcs["get_hkma_tender_invitations"](lang="en", segment="tender")
        mock_tool_hkma_tender.get_tender_invitations.assert_called_once_with(
            lang="en",
            segment="tender",
            pagesize=None,
            offset=None,
            from_date=None,
            to_date=None,
        )

        decorated_funcs["get_hibor_daily_stats"](
            start_date="2020-01-01", end_date="2020-01-31"
        )
        mock_tool_hibor_daily.get_hibor_stats.assert_called_once_with(
            "2020-01-01", "2020-01-31"
        )

        decorated_funcs["get_atm_locations"](district="Central")
        mock_tool_atm_locator.get_atm_locations.assert_called_once_with(
            "Central", None, 100, 0
        )

        decorated_funcs["get_stamp_duty_statistics"](
            start_period="202001", end_period="202012"
        )
        mock_tool_stamp_duty_statistics.get_stamp_duty_statistics.assert_called_once_with(
            "202001", "202012"
        )

        decorated_funcs["get_bank_branch_locations"](district="Central", lang="en")
        mock_tool_bank_branch_locator.get_bank_branch_locations.assert_called_once_with(
            "Central", None, "en", 100, 0
        )

        decorated_funcs["get_fraudulent_bank_scams"](lang="en")
        mock_tool_fraudulent_bank_scams.get_fraudulent_bank_scams.assert_called_once_with(
            "en"
        )


if __name__ == "__main__":
    unittest.main()
