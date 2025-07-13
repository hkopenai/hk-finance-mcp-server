"""
Module for fetching and processing information about fraudulent bank websites and phishing scams from the Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve data on reported fraudulent bank scams from the HKMA API, including details on scam types, alleged bank names, and related press releases.
"""

from typing import Any, Dict, List, Optional
import requests
from pydantic import Field
from typing_extensions import Annotated
from fastmcp import FastMCP

API_URL = "https://api.hkma.gov.hk/public/bank-svf-info/fraudulent-bank-scams"

def register(mcp: FastMCP):
    @mcp.tool(
        description="Get information on fraudulent bank websites and phishing scams reported to HKMA"
    )
    def get_fraudulent_bank_scams(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc)",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
    ) -> List[Dict]:
        return _get_fraudulent_bank_scams(lang if lang is not None else "en")

def _get_fraudulent_bank_scams(lang: str = "en") -> List[Dict[str, Any]]:
    """
    Get information on fraudulent bank websites and phishing scams reported to HKMA.

    Args:
        lang: Language of the data. Options are 'en' (English, default), 'tc' (Traditional Chinese), 'sc' (Simplified Chinese).

    Returns:
        List of dictionaries containing details of fraudulent bank scams.
    """
    url = f"{API_URL}?lang={lang}"
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    data = response.json()
    if data.get("header", {}).get("success", False):
        return data.get("result", {}).get("records", [])
    else:
        error_msg = data.get("header", {}).get("err_msg", "Unknown error")
        raise ValueError(f"API Error: {error_msg}")
