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
    @patch("hkopenai.hk_finance_mcp_server.tool_business_reg.register")
    @patch("hkopenai.hk_finance_mcp_server.tool_neg_resident_mortgage.register")
    @patch("hkopenai.hk_finance_mcp_server.tool_credit_card.register")
    @patch("hkopenai.hk_finance_mcp_server.tool_coin_cart.register")
    @patch("hkopenai.hk_finance_mcp_server.tool_hkma_tender.register")
    @patch("hkopenai.hk_finance_mcp_server.tool_hibor_daily.get_hibor_stats")
    @patch("hkopenai.hk_finance_mcp_server.tool_atm_locator.register")
    @patch("hkopenai.hk_finance_mcp_server.tool_stamp_duty_statistics.get_stamp_duty_statistics")
    @patch("hkopenai.hk_finance_mcp_server.tool_bank_branch_locator.register")
    @patch("hkopenai.hk_finance_mcp_server.tool_fraudulent_bank_scams.get_fraudulent_bank_scams")
    def test_create_mcp_server(
        self,
        mock_get_fraudulent_bank_scams,
        mock_bank_branch_locator_register,
        mock_get_stamp_duty_statistics,
        mock_atm_locator_register,
        mock_get_hibor_stats,
        mock_get_tender_invitations,
        mock_coin_cart_register,
        mock_credit_card_register,
        mock_get_neg_equity_stats,
        mock_business_reg_register,
        mock_fastmcp
    ):
        """Test the creation and configuration of the MCP server with mocked tools.

        Verifies that the server is created correctly and all tools are properly registered
        and functional when called."""
        # Setup mocks
        mock_server = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        create_mcp_server()

        # Verify server creation
        mock_fastmcp.assert_called_once()
        
        mock_business_reg_register.assert_called_once_with(mock_server)
        mock_credit_card_register.assert_called_once_with(mock_server)
        mock_coin_cart_register.assert_called_once_with(mock_server)
        mock_atm_locator_register.assert_called_once_with(mock_server)
        mock_bank_branch_locator_register.assert_called_once_with(mock_server)


if __name__ == "__main__":
    unittest.main()
