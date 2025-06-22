"""
Tool for fetching information about fraudulent bank websites and phishing scams from HKMA.
"""

import json
from typing import Any, Dict, List, Optional
import requests

API_URL = "https://api.hkma.gov.hk/public/bank-svf-info/fraudulent-bank-scams"

def get_fraudulent_bank_scams(lang: str = "en") -> List[Dict[str, Any]]:
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

def input_schema() -> Dict[str, Any]:
    """
    Define the input schema for the tool.
    
    Returns:
        Dictionary representing the JSON schema for input parameters.
    """
    return {
        "type": "object",
        "properties": {
            "lang": {
                "anyOf": [
                    {"type": "string"},
                    {"type": "null"}
                ],
                "default": "en",
                "description": "Language (en/tc/sc)",
                "enum": ["en", "tc", "sc"],
                "title": "Lang"
            }
        }
    }

def output_schema() -> Dict[str, Any]:
    """
    Define the output schema for the tool.
    
    Returns:
        Dictionary representing the JSON schema for output data.
    """
    return {
        "type": "array",
        "items": {
            "type": "object",
            "properties": {
                "issue_date": {"type": "string", "description": "Date the scam was reported"},
                "alleged_name": {"type": "string", "description": "Name of the bank being impersonated"},
                "scam_type": {"type": "string", "description": "Type of scam (e.g., fraudulent website)"},
                "pr_url": {"type": "string", "description": "URL to the press release or alert"},
                "fraud_website_address": {"type": "string", "description": "Fraudulent website URL (obfuscated)"}
            },
            "required": ["issue_date", "alleged_name", "scam_type", "pr_url", "fraud_website_address"]
        }
    }
