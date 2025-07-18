"""
Module for creating and running the HK OpenAI Finance MCP Server.

This module configures and initializes a FastMCP server with various financial data tools provided by the Hong Kong Monetary Authority (HKMA) and other sources. It includes functionality to run the server in different modes (stdio or SSE).
"""

from fastmcp import FastMCP
from .tools import business_reg
from .tools import neg_resident_mortgage
from .tools import credit_card
from .tools import coin_cart
from .tools import hkma_tender
from .tools import hibor_daily
from .tools import atm_locator
from .tools import stamp_duty_statistics
from .tools import bank_branch_locator
from .tools import fraudulent_bank_scams


def server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Finance Server")

    business_reg.register(mcp)
    neg_resident_mortgage.register(mcp)
    credit_card.register(mcp)
    coin_cart.register(mcp)
    hkma_tender.register(mcp)
    hibor_daily.register(mcp)
    atm_locator.register(mcp)
    stamp_duty_statistics.register(mcp)
    bank_branch_locator.register(mcp)
    fraudulent_bank_scams.register(mcp)

    return mcp
