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
        
    return data

def get_coin_cart_schedule() -> Dict:
    """Get coin cart schedule data in standardized format"""
    data = fetch_coin_cart_schedule()
    return {'coin_cart_schedule': data}
