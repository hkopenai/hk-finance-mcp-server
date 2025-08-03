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
    # AOF API endpoint for the licensed banks historical dataset
    url = "https://www.aof.org.hk/api/v1/hkimr/lic-bank-branches-and-offices"
    
    # Add query parameters
    params = {"lang": lang}
    if start_year:
        params["start_year"] = start_year
    if end_year:
        params["end_year"] = end_year
    if data_type and data_type != "all":
        params["data_type"] = data_type

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
            year = record.get("year")
            if year:
                year_int = int(year) if isinstance(year, str) else year
                
                # Apply year filtering if specified
                if start_year and year_int < start_year:
                    continue
                if end_year and year_int > end_year:
                    continue
                
                processed_record = {
                    "year": year,
                    "licensed_banks": record.get("licensed_banks"),
                    "bank_branches": record.get("bank_branches"),
                    "bank_offices": record.get("bank_offices"),
                    "total_branches_and_offices": record.get("total_branches_and_offices"),
                    "notes": record.get("notes", ""),
                }
                
                # Filter by data type if specified
                if data_type == "licensed_banks":
                    processed_record = {"year": year, "licensed_banks": record.get("licensed_banks")}
                elif data_type == "bank_branches":
                    processed_record = {"year": year, "bank_branches": record.get("bank_branches")}
                elif data_type == "bank_offices":
                    processed_record = {"year": year, "bank_offices": record.get("bank_offices")}
                
                processed_records.append(processed_record)
        
        return processed_records
        
    except Exception as e:
        return {"error": f"Failed to fetch data: {str(e)}"} 