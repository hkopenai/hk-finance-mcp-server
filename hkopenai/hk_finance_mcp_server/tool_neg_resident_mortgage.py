"""
Module for fetching and processing negative equity residential mortgage data from the Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve statistics on residential mortgage loans in negative equity from the HKMA API.
"""

import json
import urllib.request
from typing import List, Dict, Optional, Annotated
from pydantic import Field


def register(mcp):
    """Registers the negative equity residential mortgage statistics tool with the FastMCP server."""

    @mcp.tool(
        description="Get statistics on residential mortgage loans in negative equity in Hong Kong"
    )
    def get_neg_equity_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None,
    ) -> List[Dict]:
        """Retrieve negative equity residential mortgage statistics."""
        return _get_neg_equity_stats(start_year, start_month, end_year, end_month)


def fetch_neg_equity_data(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None,
) -> List[Dict]:
    """Fetch and parse negative equity residential mortgage data from HKMA

    Args:
        start_year: Optional start year (YYYY)
        start_month: Optional start month (1-12)
        end_year: Optional end year (YYYY)
        end_month: Optional end month (1-12)

    Returns:
        List of negative equity mortgage data in JSON format
    """
    url = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/banking/residential-mortgage-loans-neg-equity"
    try:
        with urllib.request.urlopen(url) as response:
            data = json.loads(response.read().decode("utf-8"))
    except json.JSONDecodeError as e:
        return [{"error": f"Invalid JSON data received: {e}"}]
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

    if not data.get("header", {}).get("success", False):
        return []

    results = []
    records = data.get("result", {}).get("records", [])
    for record in records:
        quarter = record["end_of_quarter"]
        year = int(quarter.split("-")[0])
        quarter_num = int(quarter.split("-Q")[1])

        # Convert quarter to approximate month (Q1=3, Q2=6, Q3=9, Q4=12)
        month = quarter_num * 3

        include_record = True

        if start_year and year < start_year:
            include_record = False
        if (
            include_record
            and start_year
            and year == start_year
            and start_month is not None
            and 1 <= start_month <= 12
            and month < start_month
        ):
            include_record = False
        if include_record and end_year and year > end_year:
            include_record = False
        if (
            include_record
            and end_year
            and year == end_year
            and end_month is not None
            and 1 <= end_month <= 12
            and month > end_month
        ):
            include_record = False

        if include_record:
            result = {"quarter": quarter}
            if "outstanding_loans" in record:
                result["outstanding_loans"] = record["outstanding_loans"]
            if "outstanding_loans_ratio" in record:
                result["outstanding_loans_ratio"] = record["outstanding_loans_ratio"]
            if "outstanding_loans_amt" in record:
                result["outstanding_loans_amt"] = record["outstanding_loans_amt"]
            if "outstanding_loans_amt_ratio" in record:
                result["outstanding_loans_amt_ratio"] = record[
                    "outstanding_loans_amt_ratio"
                ]
            if "unsecured_portion_amt" in record:
                result["unsecured_portion_amt"] = record["unsecured_portion_amt"]
            if "lv_ratio" in record:
                result["lv_ratio"] = record["lv_ratio"]
            results.append(result)

    return results


def _get_neg_equity_stats(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None,
) -> List[Dict]:
    """Get negative equity residential mortgage statistics"""
    data = fetch_neg_equity_data(start_year, start_month, end_year, end_month)
    return data
