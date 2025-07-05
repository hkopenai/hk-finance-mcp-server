import json
import urllib.request
from typing import List, Dict


def fetch_coin_cart_schedule() -> Dict:
    """Fetch and parse HKMA Coin Cart Schedule data

    Returns:
        Dictionary containing the full API response with header and result data
    """
    url = "https://api.hkma.gov.hk/public/coin-cart-schedule?lang=en"
    try:
        response = urllib.request.urlopen(url)
        data = json.loads(response.read().decode("utf-8"))
        return data
    except json.JSONDecodeError as e:
        raise Exception(f"JSON decode error: {e}")
    except Exception as e:
        raise Exception(f"Error fetching data: {e}")


def get_coin_cart_schedule() -> Dict:
    """Get coin cart schedule data in standardized format"""
    data = fetch_coin_cart_schedule()
    return {"coin_cart_schedule": data}
