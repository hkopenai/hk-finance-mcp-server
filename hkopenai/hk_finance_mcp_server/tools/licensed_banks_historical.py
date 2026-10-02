"""
Module for fetching and processing historical licensed banks, branches, and offices data from Hong Kong Academy of Finance (AOF).

This module provides functions to retrieve historical data about licensed banks, bank branches, and bank offices in Hong Kong from 1954-2002 from the AOF API.
"""

from typing import List, Dict, Optional
from hkopenai_common.json_utils import fetch_json_data
from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the licensed banks historical data tool with the FastMCP server."""

    @mcp.tool(
        description="Get historical data on licensed banks, bank branches, and bank offices in Hong Kong from 1954-2002"
    )
    def get_licensed_banks_historical_data(
        start_year: Annotated[
            Optional[int], Field(description="Start year for filtering data (1954-2002)")
        ] = None,
        end_year: Annotated[
            Optional[int], Field(description="End year for filtering data (1954-2002)")
        ] = None,
        data_type: Annotated[
            Optional[str],
            Field(
                description="Type of data to retrieve",
                json_schema_extra={"enum": ["licensed_banks", "bank_branches", "bank_offices", "all"]},
            ),
        ] = "all",
        lang: Annotated[
            Optional[str],
            Field(
                description="Language for data output (en, tc, sc)",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
    ) -> List[Dict]:
        """Retrieve historical licensed banks, branches, and offices data with optional filtering"""
        return _get_licensed_banks_historical_data(start_year, end_year, data_type, lang)


def _get_licensed_banks_historical_data(
    start_year: Optional[int] = None,
    end_year: Optional[int] = None,
    data_type: Optional[str] = "all",
    lang: Optional[str] = "en",
) -> List[Dict]:
    """
    Retrieve historical data on licensed banks, branches, and offices in Hong Kong from 1954-2002

    Args:
        start_year: Optional start year to filter data (1954-2002)
        end_year: Optional end year to filter data (1954-2002)
        data_type: Type of data to retrieve (licensed_banks, bank_branches, bank_offices, all)
        lang: Language for data output (en, tc, sc) - default: en

    Returns:
        List of historical bank data
    """
    # HKMA hkimr endpoint (the AOF v1 endpoint was retired). The dataset is small
    # (49 rows covering 1954-2002), so we fetch the full page and apply
    # year-range / data-type filters in Python -- the HKMA filter query parameter
    # on this endpoint only supports exact-match equality, not ranges, and
    # `sortby` is rejected with err 1002.
    url = "https://api.hkma.gov.hk/public/hkimr/lic-bank-branches-and-offices"

    # HKMA only needs `lang`; we filter year-range and data_type client-side.
    params = {"lang": lang, "pagesize": 100}

    try:
        data = fetch_json_data(url, params=params, timeout=30)

        if not isinstance(data, dict):
            return {"error": "Invalid data format received from API"}

        # Handle different response formats
        if "error" in data:
            return {"error": data["error"]}

        if "result" in data:
            records = data.get("result", {}).get("records", [])
        else:
            records = data.get("records", [])

        if not records:
            return {"message": "No data found for the specified criteria"}

        # Process and filter the records
        processed_records = []
        for record in records:
            year_raw = record.get("Lb_yr")
            if year_raw is None:
                continue
            try:
                year_int = int(str(year_raw))
            except (TypeError, ValueError):
                continue

            # Apply year filtering if specified
            if start_year and year_int < start_year:
                continue
            if end_year and year_int > end_year:
                continue

            licensed_banks = record.get("Lb_brnum_a")
            bank_branches = record.get("Lb_bran_a")
            bank_offices = record.get("Lb_broff_a")
            if bank_branches is not None and bank_offices is not None:
                total = bank_branches + bank_offices
            else:
                total = None

            base = {
                "year": str(year_raw),
                "licensed_banks": licensed_banks,
                "bank_branches": bank_branches,
                "bank_offices": bank_offices,
                "total_branches_and_offices": total,
            }

            # Filter by data type if specified
            if data_type == "licensed_banks":
                processed_record = {"year": base["year"], "licensed_banks": base["licensed_banks"]}
            elif data_type == "bank_branches":
                processed_record = {"year": base["year"], "bank_branches": base["bank_branches"]}
            elif data_type == "bank_offices":
                processed_record = {"year": base["year"], "bank_offices": base["bank_offices"]}
            else:
                processed_record = base

            processed_records.append(processed_record)

        return processed_records

    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"} 