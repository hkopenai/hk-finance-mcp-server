import json
import urllib.request
from typing import Dict, List, Optional

def fetch_tender_invitations(lang: str = 'en', segment: str = 'tender', 
                           pagesize: Optional[int] = None, offset: Optional[int] = None,
                           from_date: Optional[str] = None, to_date: Optional[str] = None) -> List[Dict]:
    """Fetch tender invitations from HKMA API
    
    Args:
        lang: Language (en/tc/sc)
        segment: Type of records (tender/notice)
        pagesize: Number of records per page
        offset: Starting record offset
        from_date: Filter records from date (YYYY-MM-DD)
        to_date: Filter records to date (YYYY-MM-DD)
        
    Returns:
        List of tender records with title, link and date
    """
    base_url = "https://api.hkma.gov.hk/public/tender-invitations"
    params = [f"lang={lang}", f"segment={segment}"]
    
    if pagesize:
        params.append(f"pagesize={pagesize}")
    if offset:
        params.append(f"offset={offset}")
    if from_date:
        params.append(f"from={from_date}")
    if to_date:
        params.append(f"to={to_date}")
        
    url = f"{base_url}?{'&'.join(params)}"
    response = urllib.request.urlopen(url)
    data = json.loads(response.read().decode('utf-8'))
    
    return data.get('result', {}).get('records', [])

def get_tender_invitations(lang: str = 'en', segment: str = 'tender',
                          pagesize: Optional[int] = None, offset: Optional[int] = None,
                          from_date: Optional[str] = None, to_date: Optional[str] = None) -> Dict:
    """Get tender invitations in standardized format
    
    Returns:
        Dictionary with 'tender_invitations' key containing list of records
    """
    records = fetch_tender_invitations(lang, segment, pagesize, offset, from_date, to_date)
    return {'tender_invitations': records}
