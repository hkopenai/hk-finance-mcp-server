import json
import urllib.request
from typing import List, Dict, Optional


def fetch_atm_locator_data(
    district: Optional[str] = None,
    bank_name: Optional[str] = None,
    pagesize: Optional[int] = 100,
    offset: Optional[int] = 0,
) -> List[Dict]:
    """Fetch and parse ATM locator data from HKMA API

    Args:
        district: Optional district name to filter results
        bank_name: Optional bank name to filter results
        pagesize: Number of records per page (default: 100)
        offset: Offset for pagination (default: 0)

    Returns:
        List of ATM location data in JSON format
    """
    url = f"https://api.hkma.gov.hk/public/bank-svf-info/banks-atm-locator?lang=en&pagesize={pagesize}&offset={offset}"
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
                "type_of_machine": record.get("type_of_machine", ""),
                "function": record.get("function", ""),
                "currencies_supported": record.get("currencies_supported", ""),
                "barrier_free_access": record.get("barrier_free_access", ""),
                "network": record.get("network", ""),
                "address": record.get("address", ""),
                "service_hours": record.get("service_hours", ""),
                "latitude": float(record.get("latitude", 0.0)),
                "longitude": float(record.get("longitude", 0.0)),
            }
        )

    return filtered_records


def get_atm_locations(
    district: Optional[str] = None,
    bank_name: Optional[str] = None,
    pagesize: Optional[int] = 100,
    offset: Optional[int] = 0,
) -> List[Dict]:
    """Retrieve ATM locations with optional filtering"""
    data = fetch_atm_locator_data(district, bank_name, pagesize, offset)

    if not data:
        return []
    return data
