"""
Module for fetching and processing Hong Kong Interbank Interest Rates (HIBOR) daily data from the Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve HIBOR daily figures from the HKMA API and format them for further use.
"""

import json
import urllib.request
from typing import List, Dict, Optional
from datetime import datetime


def fetch_hibor_daily_data(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> List[Dict]:
    """Fetch and parse Hong Kong Interbank Interest Rates (HIBOR) daily figures from HKMA API

    Args:
        start_date: Optional start date in YYYY-MM-DD format
        end_date: Optional end date in YYYY-MM-DD format

    Returns:
        List of HIBOR daily data in JSON format with date and interest rates for various tenors
    """
    url = "https://api.hkma.gov.hk/public/market-data-and-statistics/monthly-statistical-bulletin/er-ir/hk-interbank-ir-daily?segment=hibor.fixing"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))

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


def get_hibor_stats(
    start_date: Optional[str] = None, end_date: Optional[str] = None
) -> List[Dict]:
    """Retrieve HIBOR daily figures data"""
    data = fetch_hibor_daily_data(start_date, end_date)

    if not data:
        return []
    return data
