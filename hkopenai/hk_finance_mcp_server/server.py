"""
Module for creating and running the HK OpenAI Finance MCP Server.

This module configures and initializes a FastMCP server with various financial data tools provided by the Hong Kong Monetary Authority (HKMA) and other sources. It includes functionality to run the server in different modes (stdio or SSE).
"""

from fastmcp import FastMCP
from hkopenai.hk_finance_mcp_server import tool_business_reg
from hkopenai.hk_finance_mcp_server import tool_neg_resident_mortgage
from hkopenai.hk_finance_mcp_server import tool_credit_card
from hkopenai.hk_finance_mcp_server import tool_coin_cart
from hkopenai.hk_finance_mcp_server import tool_hkma_tender
from hkopenai.hk_finance_mcp_server import tool_hibor_daily
from hkopenai.hk_finance_mcp_server import tool_atm_locator
from hkopenai.hk_finance_mcp_server import tool_stamp_duty_statistics
from hkopenai.hk_finance_mcp_server import tool_bank_branch_locator
from hkopenai.hk_finance_mcp_server import tool_fraudulent_bank_scams


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Finance Server")

    tool_business_reg.register(mcp)
    tool_neg_resident_mortgage.register(mcp)
    tool_credit_card.register(mcp)
    tool_coin_cart.register(mcp)
    tool_hkma_tender.register(mcp)
    tool_hibor_daily.register(mcp)
    tool_atm_locator.register(mcp)
    tool_stamp_duty_statistics.register(mcp)
    tool_bank_branch_locator.register(mcp)
    tool_fraudulent_bank_scams.register(mcp)

    return mcp
