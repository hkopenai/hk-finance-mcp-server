import csv
import urllib.request
from typing import List, Dict, Optional

def fetch_business_returns_data(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None
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
    response = urllib.request.urlopen(url)
    lines = [l.decode('utf-8') for l in response.readlines()]
    reader = csv.DictReader(lines)
    
    results = []
    for row in reader:
        year_month = row['RUN_DATE']
        current_year = int(year_month[:4])
        current_month = int(year_month[4:])
        
        if start_year and current_year < start_year:
            continue
        if start_year and current_year == start_year and start_month and current_month < start_month:
            continue
        if end_year and current_year > end_year:
            continue
        if end_year and current_year == end_year and end_month and current_month > end_month:
            continue
        
        results.append({
            'year_month': f"{year_month[:4]}-{year_month[4:]}",
            'active_business': int(row['ACTIVE_MAIN_BUS']),
            'new_registered_business': int(row['NEW_REG_MAIN_BUS'])
        })

    return results

def get_business_stats(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None
) -> Dict:
    """Calculate statistics from business returns data"""
    data = fetch_business_returns_data(start_year, start_month, end_year, end_month)
    
    if not data:
        return {}
    print(data)
    return data
