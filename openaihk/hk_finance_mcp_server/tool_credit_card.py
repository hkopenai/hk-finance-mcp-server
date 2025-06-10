import json
import urllib.request
from typing import List, Dict, Optional

def fetch_credit_card_data(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None
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
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    if not data['header']['success']:
        return []
    
    results = []
    for record in data['result']['records']:
        quarter = record['end_of_quarter']
        year = int(quarter.split('-')[0])
        quarter_num = int(quarter.split('-Q')[1])
        
        # Convert quarter to approximate month (Q1=3, Q2=6, Q3=9, Q4=12)
        month = quarter_num * 3
        
        if start_year and year < start_year:
            continue
        if start_year and year == start_year and start_month and month < start_month:
            continue
        if end_year and year > end_year:
            continue
        if end_year and year == end_year and end_month and month > end_month:
            continue
            
        results.append({
            'quarter': quarter,
            'accounts_count': record['endperiod_noofaccts'],
            'delinquent_amount': record['endperiod_delinquent_amt'],
            'chargeoff_amount': record['during_chargeoff_amt'],
            'rollover_amount': record['during_rollover_amt'],
            'avg_receivables': record['during_avg_total_receivables']
        })

    return results

def get_credit_card_stats(
    start_year: Optional[int] = None,
    start_month: Optional[int] = None,
    end_year: Optional[int] = None,
    end_month: Optional[int] = None
) -> Dict:
    """Get credit card lending survey statistics"""
    data = fetch_credit_card_data(start_year, start_month, end_year, end_month)
    return data

def fetch_credit_card_hotlines() -> List[Dict]:
    """Fetch and parse credit card hotline data from HKMA
    
    Returns:
        List of credit card hotline information in JSON format
    """
    url = "https://api.hkma.gov.hk/public/bank-svf-info/hotlines-report-loss-credit-card?lang=en"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    if not data['header']['success']:
        return []

    return data['result']['records']

def get_credit_card_hotlines() -> Dict:
    """Get list of hotlines for reporting loss of credit card"""
    data = fetch_credit_card_hotlines()
    return data
