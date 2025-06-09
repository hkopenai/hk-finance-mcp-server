import json
import urllib.request
from typing import List, Dict

def fetch_coin_cart_schedule() -> List[Dict]:
    """Fetch and parse HKMA Coin Cart Schedule data
    
    Returns:
        List of coin cart schedule entries with date, district, location, 
        start_time, end_time, and service_hours
    """
    url = "https://api.hkma.gov.hk/public/coin-cart-schedule?lang=en"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    results = []
    for entry in data['result']['records']:
        results.append({
            'date': entry['date'],
            'district': entry['district'],
            'location': entry['location'],
            'start_time': entry['start_time'],
            'end_time': entry['end_time'],
            'service_hours': entry['service_hours']
        })
    
    return results

def get_coin_cart_schedule() -> Dict:
    """Get coin cart schedule data in standardized format"""
    data = fetch_coin_cart_schedule()
    return {'coin_cart_schedule': data}
