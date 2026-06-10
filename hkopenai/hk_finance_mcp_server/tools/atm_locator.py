"""
Module for fetching and processing ATM location data from the Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve ATM location information from the HKMA API with filtering options for district and bank name.
"""

from typing import List, Dict, Optional
from hkopenai_common.json_utils import fetch_json_data
from pydantic import Field
from typing_extensions import Annotated


HKMA_PAGE_SIZE = 100


def register(mcp):
    """Registers the ATM locator tool with the FastMCP server."""

    @mcp.tool(
        description="Get information on Automated Teller Machines (ATMs) of retail banks in Hong Kong"
    )
    def get_atm_locations(
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
        """Retrieve ATM locations with optional filtering"""
        return _get_atm_locations(district, bank_name, lang, pagesize, offset)


def _get_atm_locations(
    district: Optional[str] = None,
    bank_name: Optional[str] = None,
    lang: Optional[str] = "en",
    pagesize: Optional[int] = 100,
    offset: Optional[int] = 0,
) -> List[Dict]:
    """
    Retrieve ATM locations with optional filtering.

    Args:
        district: Optional district name to filter results
        bank_name: Optional bank name to filter results
        lang: Language for data output (en, tc, sc) - default: en
        pagesize: Number of records per page (default: 100)
        offset: Offset for pagination (default: 0)

    Returns:
        List of ATM location data in JSON format
    """
    lang = lang or "en"
    records = []
    fetch_offset = 0
    while True:
        url = (
            "https://api.hkma.gov.hk/public/bank-svf-info/banks-atm-locator"
            f"?lang={lang}&pagesize={HKMA_PAGE_SIZE}&offset={fetch_offset}"
        )
        data = fetch_json_data(url)
        page_records = data.get("result", {}).get("records", []) or []
        records.extend(page_records)

        if len(page_records) < HKMA_PAGE_SIZE:
            break
        fetch_offset += HKMA_PAGE_SIZE

    filtered_records = []

    normalized_district_param = district.lower().strip() if district else None
    normalized_bank_name_param = bank_name.lower().strip() if bank_name else None

    for record in records:
        record_district = record.get("district", "").lower().strip()
        record_bank_name = record.get("bank_name", "").lower().strip()

        if normalized_district_param and normalized_district_param != record_district:
            continue
        if (
            normalized_bank_name_param
            and normalized_bank_name_param != record_bank_name
        ):
            continue
        filtered_records.append(
            {
                "district": str(record.get("district", "")).strip(),
                "bank_name": str(record.get("bank_name", "")).strip(),
                "type_of_machine": str(record.get("type_of_machine", "")).strip(),
                "function": str(record.get("function", "")).strip(),
                "currencies_supported": str(
                    record.get("currencies_supported", "")
                ).strip(),
                "barrier_free_access": str(
                    record.get("barrier_free_access", "")
                ).strip(),
                "network": str(record.get("network", "")).strip(),
                "address": str(record.get("address", "")).strip(),
                "service_hours": str(record.get("service_hours", "")).strip(),
                "latitude": float(record.get("latitude", 0.0)),
                "longitude": float(record.get("longitude", 0.0)),
            }
        )

    # Apply pagesize and offset after filtering
    start_index = offset
    end_index = offset + pagesize
    return filtered_records[start_index:end_index]
