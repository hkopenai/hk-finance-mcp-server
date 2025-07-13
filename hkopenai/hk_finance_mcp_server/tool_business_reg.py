"""
Module for fetching and processing business registration statistics from the Inland Revenue Department (IRD) of Hong Kong.

This module provides functions to retrieve data on active and newly registered businesses from the IRD API with date range filtering options.
"""

import csv
import urllib.request
from typing import List, Dict, Optional
from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the business registration tool with the FastMCP server."""

    @mcp.tool(
        description="Get monthly statistics on the number of new business registrations in Hong Kong"
    )
    def get_business_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None,
    ) -> List[Dict]:
        """Get monthly statistics on the number of new business registrations in Hong Kong"""
        return _get_business_stats(start_year, start_month, end_year, end_month)


def fetch_business_returns_data(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None,
) -> List[Dict]:
    """Fetch and parse business returns data from IRD Hong Kong

    Args:
        start_year: Optional start year (YYYY)
        start_month: Optional start month (1-12)
        end_year: Optional end year (YYYY)
        end_month: Optional end month (1-12)

    Returns:
        List of business data in JSON format with year_month, active_business, new_registered_business
    """
    url = "https://www.ird.gov.hk/datagovhk/BRFMBUSC.csv"
    with urllib.request.urlopen(url) as response:
        lines = [l.decode("utf-8") for l in response.readlines()]
        reader = csv.DictReader(lines)

    results = []
    for row in reader:
        year_month = row.get("RUN_DATE", "")
        if len(year_month) < 6:
            continue
        current_year = int(year_month[:4])
        current_month = int(year_month[4:])
        if start_year is not None and current_year < start_year:
            continue
        if (
            start_year is not None
            and current_year == start_year
            and start_month is not None
            and start_month <= 12
            and current_month < start_month
        ):
            continue
        if end_year is not None and current_year > end_year:
            continue
        if (
            end_year is not None
            and current_year == end_year
            and end_month is not None
            and current_month > end_month
        ):
            continue

        active_business_str = row.get("ACTIVE_MAIN_BUS", "0")
        new_registered_business_str = row.get("NEW_REG_MAIN_BUS", "0")

        try:
            active_business = int(active_business_str)
        except ValueError:
            active_business = f"Invalid data for ACTIVE_MAIN_BUS: {active_business_str}"

        try:
            new_registered_business = int(new_registered_business_str)
        except ValueError:
            new_registered_business = (
                f"Invalid data for NEW_REG_MAIN_BUS: {new_registered_business_str}"
            )

        results.append(
            {
                "year_month": f"{year_month[:4]}-{year_month[4:]}",
                "active_business": active_business,
                "new_registered_business": new_registered_business,
            }
        )

    return results


def _get_business_stats(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None,
) -> List[Dict]:
    """Calculate statistics from business returns data"""
    data = fetch_business_returns_data(start_year, start_month, end_year, end_month)

    if not data:
        return []
    return data
