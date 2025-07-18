"""
Module for testing the HK OpenAI Finance MCP Server creation.

This module contains unit tests to verify the correct initialization and configuration
of the MCP server with various financial data tools.
"""

import unittest
from unittest.mock import patch, Mock
from hkopenai.hk_finance_mcp_server.server import server


class TestApp(unittest.TestCase):
    """Test case class for verifying MCP server functionality."""

    @patch("hkopenai.hk_finance_mcp_server.server.FastMCP")
    @patch("hkopenai.hk_finance_mcp_server.tools.business_reg.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.neg_resident_mortgage.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.credit_card.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.coin_cart.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.hkma_tender.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.hibor_daily.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.atm_locator.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.stamp_duty_statistics.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.bank_branch_locator.register")
    @patch("hkopenai.hk_finance_mcp_server.tools.fraudulent_bank_scams.register")
    def test_create_mcp_server(
        self,
        mock_fraudulent_bank_scams_register,
        mock_bank_branch_locator_register,
        mock_stamp_duty_statistics_register,
        mock_atm_locator_register,
        mock_hibor_daily_register,
        mock_hkma_tender_register,
        mock_coin_cart_register,
        mock_credit_card_register,
        mock_neg_resident_mortgage_register,
        mock_business_reg_register,
        mock_fastmcp,
    ):
        """Test the creation and configuration of the MCP server with mocked tools.

        Verifies that the server is created correctly and all tools are properly registered
        and functional when called."""
        # Setup mocks
        mock_server = Mock()
        mock_fastmcp.return_value = mock_server

        # Test server creation
        server()

        # Verify server creation
        mock_fastmcp.assert_called_once()

        mock_business_reg_register.assert_called_once_with(mock_server)
        mock_credit_card_register.assert_called_once_with(mock_server)
        mock_coin_cart_register.assert_called_once_with(mock_server)
        mock_hkma_tender_register.assert_called_once_with(mock_server)
        mock_hibor_daily_register.assert_called_once_with(mock_server)
        mock_atm_locator_register.assert_called_once_with(mock_server)
        mock_stamp_duty_statistics_register.assert_called_once_with(mock_server)
        mock_bank_branch_locator_register.assert_called_once_with(mock_server)
        mock_fraudulent_bank_scams_register.assert_called_once_with(mock_server)
        mock_neg_resident_mortgage_register.assert_called_once_with(mock_server)


if __name__ == "__main__":
    unittest.main()
