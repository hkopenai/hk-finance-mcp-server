import json
import urllib.request
from typing import List, Dict, Optional


def fetch_bank_branch_data(
    district: Optional[str] = None,
    bank_name: Optional[str] = None,
    lang: Optional[str] = "en",
    pagesize: Optional[int] = 100,
    offset: Optional[int] = 0,
) -> List[Dict]:
    """Fetch and parse bank branch data from HKMA API

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
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode("utf-8"))

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


def get_bank_branch_locations(
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
