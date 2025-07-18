"""
Module for fetching and processing bank branch location data from the Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve bank branch location information from the HKMA API with filtering options for district and bank name.
"""

from typing import List, Dict, Optional
from hkopenai_common.json_utils import fetch_json_data
from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the bank branch locator tool with the FastMCP server."""

    @mcp.tool(
        description="Get information on bank branch locations of retail banks in Hong Kong"
    )
    def get_bank_branch_locations(
        district: Annotated[
            Optional[str], Field(description="District name to filter results")
        ] = None,
        bank_name: Annotated[
            Optional[str], Field(description="Bank name to filter results")
        ] = None,
        lang: Annotated[
            Optional[str],
            Field(
                description="Language for data output (en, tc, sc)",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
        pagesize: Annotated[
            Optional[int], Field(description="Number of records per page")
        ] = 100,
        offset: Annotated[
            Optional[int], Field(description="Starting record offset")
        ] = 0,
    ) -> List[Dict]:
        """Retrieve bank branch locations with optional filtering"""
        return _get_bank_branch_locations(district, bank_name, lang, pagesize, offset)


def fetch_bank_branch_data(
    district: Optional[str] = None,
    bank_name: Optional[str] = None,
    lang: Optional[str] = "en",
    pagesize: Optional[int] = 100,
    offset: Optional[int] = 0,
) -> List[Dict]:
    """
    Fetch and parse bank branch data from HKMA API

    Args:
        district: Optional district name to filter results
        bank_name: Optional bank name to filter results
        lang: Language for data output (en, tc, sc) - default: en
        pagesize: Number of records per page (default: 100)
        offset: Offset for pagination (default: 0)

    Returns:
        List of bank branch location data in JSON format
    """
    url = f"https://api.hkma.gov.hk/public/bank-svf-info/banks-branch-locator?lang={lang}&pagesize={pagesize}&offset={offset}"
    data = fetch_json_data(url)

    records = data.get("result", {}).get("records", [])
    filtered_records = []

    for record in records:
        if district and record.get("district", "").lower() != district.lower():
            continue
        if bank_name and record.get("bank_name", "").lower() != bank_name.lower():
            continue
        filtered_records.append(
            {
                "district": record.get("district", ""),
                "bank_name": record.get("bank_name", ""),
                "branch_name": record.get("branch_name", ""),
                "address": record.get("address", ""),
                "service_hours": record.get("service_hours", ""),
                "latitude": float(record.get("latitude", 0.0)),
                "longitude": float(record.get("longitude", 0.0)),
                "barrier_free_access": record.get("barrier_free_access", ""),
            }
        )

    return filtered_records


def _get_bank_branch_locations(
    district: Optional[str] = None,
    bank_name: Optional[str] = None,
    lang: Optional[str] = "en",
    pagesize: Optional[int] = 100,
    offset: Optional[int] = 0,
) -> List[Dict]:
    """Retrieve bank branch locations with optional filtering

    Args:
        district: Optional district name to filter results
        bank_name: Optional bank name to filter results
        lang: Language for data output (en, tc, sc) - default: en
        pagesize: Number of records per page (default: 100)
        offset: Offset for pagination (default: 0)

    Returns:
        List of bank branch location data
    """
    data = fetch_bank_branch_data(district, bank_name, lang, pagesize, offset)

    if not data:
        return []
    return data
