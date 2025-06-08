import csv
import urllib.request
from typing import List, Dict, Optional
from datetime import datetime

def fetch_business_returns_data(start_date: Optional[str] = None, end_date: Optional[str] = None) -> List[Dict]:
    """Fetch and parse business returns data from IRD Hong Kong
    
    Args:
        start_date: Optional start date in YYYYMM format
        end_date: Optional end date in YYYYMM format
        
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
        if start_date and int(year_month) < int(start_date):
            continue
        if end_date and int(year_month) > int(end_date):
            continue
            
        results.append({
            'year_month': f"{year_month[:4]}-{year_month[4:]}",
            'active_business': int(row['ACTIVE_MAIN_BUS']),
            'new_registered_business': int(row['NEW_REG_MAIN_BUS'])
        })
    
    return results

def get_business_return_stats(start_date: Optional[str] = None, end_date: Optional[str] = None) -> Dict:
    """Calculate statistics from business returns data"""
    data = fetch_business_returns_data(start_date, end_date)
    # Add statistical calculations here
    return {}
