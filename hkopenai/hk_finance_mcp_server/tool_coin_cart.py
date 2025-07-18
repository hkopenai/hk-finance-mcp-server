"""
Module for fetching and processing Hong Kong Monetary Authority (HKMA) Coin Cart Schedule data.

This module provides functions to retrieve coin cart schedule information from the HKMA API
and format it for further use.
"""

from typing import Dict
from hkopenai_common.json_utils import fetch_json_data


def register(mcp):
    """Registers the coin cart tool with the FastMCP server."""

    @mcp.tool(
        description="Get coin collection cart schedule in Hong Kong. The cart can charge your electronic wallet and you no long have to keep coins."
    )
    def get_coin_cart() -> Dict:
        """Get coin cart schedule data in standardized format"""
        return _get_coin_cart_schedule()


def fetch_coin_cart_schedule() -> Dict:
    """
    Fetch and parse HKMA Coin Cart Schedule data

    Returns:
        Dictionary containing the full API response with header and result data
    """
    url = "https://api.hkma.gov.hk/public/coin-cart-schedule?lang=en"
    return fetch_json_data(url)


def _get_coin_cart_schedule() -> Dict:
    """Get coin cart schedule data in standardized format"""
    data = fetch_coin_cart_schedule()
    if "error" in data:
        return {"type": "Error", "error": data["error"]}
    return {"coin_cart_schedule": data}
