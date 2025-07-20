"""
Module for fetching and processing Hong Kong Interbank Interest Rates (HIBOR) daily data from the Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve HIBOR daily figures from the HKMA API and format them for further use.
"""

from datetime import datetime
from typing import List, Dict, Optional
from pydantic import Field
from typing_extensions import Annotated
from fastmcp import FastMCP
from hkopenai_common.json_utils import fetch_json_data


def register(mcp: FastMCP):
    """Registers the HIBOR daily stats tool with the FastMCP server."""

    @mcp.tool(
        description="Get daily figures of Hong Kong Interbank Interest Rates (HIBOR) from HKMA"
    )
    def get_hibor_daily_stats(
        start_date: Annotated[
            Optional[str], Field(description="Start date (YYYY-MM-DD)")
        ] = None,
        end_date: Annotated[
            Optional[str], Field(description="End date (YYYY-MM-DD)")
        ] = None,
    ) -> List[Dict]:
        """Get daily figures of Hong Kong Interbank Interest Rates (HIBOR) from HKMA."""
        return _get_hibor_stats(start_date, end_date)


def _get_hibor_stats(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> List[Dict]:
    """Retrieve HIBOR daily figures data"""
    url = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-daily?segment=hibor.fixing"
    data = fetch_json_data(url)

    if "error" in data:
        return data

    # Ensure data is a dictionary before attempting to get 'result'
    if not isinstance(data, dict):
        return {"type": "Error", "error": "Invalid data format from API"}

    records = data.get("result", {}).get("records", [])

    results = []
    for record in records:
        record_date = record.get("end_of_day", "")
        if not record_date:
            continue

        try:
            current_date = datetime.strptime(record_date, "%Y-%m-%d")
        except ValueError:
            continue

        if start_date:
            start_dt = datetime.strptime(start_date, "%Y-%m-%d")
            if current_date < start_dt:
                continue

        if end_date:
            end_dt = datetime.strptime(end_date, "%Y-%m-%d")
            if current_date > end_dt:
                continue

        results.append(
            {
                "date": record_date,
                "overnight": record.get("ir_overnight", None),
                "1_week": record.get("ir_1w", None),
                "1_month": record.get("ir_1m", None),
                "3_months": record.get("ir_3m", None),
                "6_months": record.get("ir_6m", None),
                "9_months": record.get("ir_9m", None),
                "12_months": record.get("ir_12m", None),
            }
        )

    return results
