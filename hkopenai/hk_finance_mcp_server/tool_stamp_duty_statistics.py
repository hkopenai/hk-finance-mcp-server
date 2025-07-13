"""
Module for fetching and processing monthly stamp duty statistics from the Inland Revenue Department (IRD) of Hong Kong.

This module provides functions to retrieve stamp duty data related to listed and unlisted securities from the IRD API.
"""

import csv
import urllib.request
from typing import List, Dict, Optional
from io import StringIO


def fetch_stamp_duty_data() -> List[Dict]:
    """Fetch and parse monthly stamp duty statistics from IRD API

    Returns:
        List of stamp duty statistics data in JSON format
    """
    url = "https://www.ird.gov.hk/datagovhk/Stamp_Col_ST.csv"
    with urllib.request.urlopen(url) as response:
    data = response.read().decode("utf-8")

    # Parse CSV data
    csv_file = StringIO(data)
    csv_reader = csv.DictReader(csv_file)
    records = []

    for row in csv_reader:
        records.append(
            {
                "period": row.get("Period", ""),
                "sd_listed": float(row.get("SD_Listed", 0.0)),
                "sd_unlisted": float(row.get("SD_Unlisted", 0.0)),
            }
        )

    return records


def get_stamp_duty_statistics(
    start_period: Optional[str] = None, end_period: Optional[str] = None
) -> List[Dict]:
    """Retrieve monthly stamp duty statistics with optional period filtering

    Args:
        start_period: Optional start period in YYYYMM format to filter results
        end_period: Optional end period in YYYYMM format to filter results

    Returns:
        List of stamp duty statistics data in JSON format
    """
    data = fetch_stamp_duty_data()

    if not data:
        return []

    if start_period or end_period:
        filtered_data = []
        for record in data:
            period = record.get("period", "")
            if start_period and period < start_period:
                continue
            if end_period and period > end_period:
                continue
            filtered_data.append(record)
        return filtered_data

    return data
