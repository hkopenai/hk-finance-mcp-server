"""
Module for fetching and processing credit card related data from Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve credit card lending survey statistics and hotline information
for reporting lost credit cards from the HKMA API.
"""

import json
import urllib.request
from typing import List, Dict, Optional
from pydantic import Field
from typing_extensions import Annotated


def register(mcp):
    """Registers the credit card tools with the FastMCP server."""

    @mcp.tool(description="Get credit card lending survey results in Hong Kong")
    def get_credit_card_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None,
    ) -> List[Dict]:
        """Get credit card lending survey results in Hong Kong"""
        return _get_credit_card_stats(start_year, start_month, end_year, end_month)

    @mcp.tool(
        description="Get list of hotlines for reporting loss of credit card from Hong Kong banks."
    )
    def get_credit_card_hotlines() -> List[Dict]:
        """Get list of hotlines for reporting loss of credit card"""
        return _get_credit_card_hotlines()


def fetch_credit_card_data(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None,
) -> List[Dict]:
    """Fetch and parse credit card lending survey data from HKMA

    Args:
        start_year: Optional start year (YYYY)
        start_month: Optional start month (1-12)
        end_year: Optional end year (YYYY)
        end_month: Optional end month (1-12)

    Returns:
        List of credit card lending data in JSON format
    """
    url = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/banking/credit-card-lending-survey"
    try:
        with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
    except json.JSONDecodeError as e:
        raise Exception(f"JSON decode error: {str(e)}")
    except Exception as e:
        raise Exception(f"Error fetching data: {str(e)}")

    if not data.get("header", {}).get("success", False):
        return []

    results = []
    for record in data["result"]["records"]:
        quarter = record["end_of_quarter"]
        year = int(quarter.split("-")[0])
        quarter_num = int(quarter.split("-Q")[1])

        # Convert quarter to approximate month (Q1=3, Q2=6, Q3=9, Q4=12)
        month = quarter_num * 3

        if start_year and year < start_year:
            continue
        if start_year and year == start_year and start_month:
            if start_month < 1 or start_month > 12:
                start_month = 1  # Ignore invalid month, treat as start of year
            if month < start_month:
                continue
        if end_year:
            if year > end_year:
                continue
            if end_month is not None:
                if end_month < 1 and year <= end_year:
                    continue  # Treat as before any data, exclude all records up to end_year
                elif year == end_year and end_month > 12:
                    end_month = 12  # Treat as end of year
                    if month > end_month:
                        continue
                elif year == end_year and month > end_month:
                    continue

        results.append(
            {
                "quarter": quarter,
                "accounts_count": record.get("endperiod_noofaccts", "invalid data"),
                "delinquent_amount": record.get(
                    "endperiod_delinquent_amt", "invalid data"
                ),
                "chargeoff_amount": record.get("during_chargeoff_amt", "invalid data"),
                "rollover_amount": record.get("during_rollover_amt", "invalid data"),
                "avg_receivables": record.get(
                    "during_avg_total_receivables", "invalid data"
                ),
            }
        )

    return results


def _get_credit_card_stats(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None,
) -> List[Dict]:
    """Get credit card lending survey statistics"""
    data = fetch_credit_card_data(start_year, start_month, end_year, end_month)
    return data


def fetch_credit_card_hotlines() -> List[Dict]:
    """Fetch and parse credit card hotline data from HKMA

    Returns:
        List of credit card hotline information in JSON format
    """
    url = "https://api.hkma.gov.hk/public/bank-svf-info/hotlines-report-loss-credit-card?lang=en"
    try:
        with urllib.request.urlopen(url) as response:
        data = json.loads(response.read().decode("utf-8"))
    except json.JSONDecodeError as e:
        raise Exception(f"JSON decode error: {e}")
    except Exception as e:
        raise Exception(f"Error fetching data: {e}")

    if not data.get("header", {}).get("success", False):
        return []

    return data["result"]["records"]


def _get_credit_card_hotlines() -> List[Dict]:
    """Get list of hotlines for reporting loss of credit card"""
    data = fetch_credit_card_hotlines()
    return data
