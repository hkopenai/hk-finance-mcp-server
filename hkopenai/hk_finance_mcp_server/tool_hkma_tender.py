"""
Module for fetching and processing tender invitations data from the Hong Kong Monetary Authority (HKMA).

This module provides functions to retrieve tender invitations and notices from the HKMA API with various filtering options.
"""

import json
import urllib.request
from datetime import datetime
from typing import Dict, List, Optional, Annotated
from pydantic import Field


def register(mcp):
    """Registers the HKMA tender invitations tool with the FastMCP server."""

    @mcp.tool(
        description="Get information of Tender Invitation and Notice of Award of Contracts from Hong Kong Monetary Authority"
    )
    def get_hkma_tender_invitations(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc)",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
        segment: Annotated[
            Optional[str],
            Field(
                description="Type of records (tender/notice)",
                json_schema_extra={"enum": ["tender", "notice"]},
            ),
        ] = "tender",
        pagesize: Annotated[
            Optional[int], Field(description="Number of records per page")
        ] = None,
        offset: Annotated[
            Optional[int], Field(description="Starting record offset")
        ] = None,
        from_date: Annotated[
            Optional[str], Field(description="Filter records from date (YYYY-MM-DD)")
        ] = None,
        to_date: Annotated[
            Optional[str], Field(description="Filter records to date (YYYY-MM-DD)")
        ] = None,
    ) -> Dict:
        """Retrieve tender invitations and notices from HKMA."""
        return _get_tender_invitations(
            lang=lang if lang is not None else "en",
            segment=segment if segment is not None else "tender",
            pagesize=pagesize,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )


def fetch_tender_invitations(
    lang: str = "en",
    segment: str = "tender",
    pagesize: Optional[int] = None,
    offset: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> List[Dict]:
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
    # Use default values if parameters are empty or invalid
    effective_lang = lang if lang in ["en", "tc", "sc"] else "en"
    effective_segment = (
        segment if segment and segment in ["tender", "notice"] else "tender"
    )
    params = [f"lang={effective_lang}", f"segment={effective_segment}"]

    if pagesize:
        params.append(f"pagesize={pagesize}")
    if offset:
        params.append(f"offset={offset}")
    if from_date:
        params.append(f"from={from_date}")
    if to_date:
        params.append(f"to={to_date}")

    url = f"{base_url}?{'&'.join(params)}"
    try:
        with urllib.request.urlopen(url) as response:
            raw_data = response.read().decode("utf-8")

        if not raw_data:
            return []
        data = json.loads(raw_data)
        return data.get("result", {}).get("records", [])
    except json.JSONDecodeError as e:
        raise Exception(f"JSON decode error: {e}")
    except Exception as e:
        raise Exception(f"Error fetching data: {e}")


def _get_tender_invitations(
    lang: str = "en",
    segment: str = "tender",
    pagesize: Optional[int] = None,
    offset: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    fetch_func=fetch_tender_invitations,  # Add fetch_func as an argument
) -> List[Dict]:
    """Fetch tender invitations from HKMA API

    Args:
        lang: Language (en/tc/sc)
        segment: Type of records (tender/notice)
        pagesize: Number of records per page
        offset: Starting record offset
        from_date: Filter records from date (YYYY-MM-DD)
        to_date: Filter records to date (YYYY-MM-DD)
        fetch_func: Function to fetch raw data (for mocking in tests)

    Returns:
        List of tender records with title, link and date
    """
    base_url = "https://api.hkma.gov.hk/public/tender-invitations"
    # Use default values if parameters are empty or invalid
    effective_lang = lang if lang in ["en", "tc", "sc"] else "en"
    effective_segment = (
        segment if segment and segment in ["tender", "notice"] else "tender"
    )
    params = [f"lang={effective_lang}", f"segment={effective_segment}"]

    if pagesize:
        params.append(f"pagesize={pagesize}")
    if offset:
        params.append(f"offset={offset}")
    if from_date:
        params.append(f"from={from_date}")
    if to_date:
        params.append(f"to={to_date}")

    url = f"{base_url}?{'&'.join(params)}"
    try:
        # Use fetch_func instead of direct urllib.request.urlopen
        records = fetch_func(lang, segment, pagesize, offset, from_date, to_date)

        filtered_records = []
        for record in records:
            include_record = True

            record_date_str = record.get("issue_date")
            if record_date_str:
                record_date = datetime.strptime(record_date_str, "%Y-%m-%d")

                if from_date:
                    from_dt = datetime.strptime(from_date, "%Y-%m-%d")
                    if record_date < from_dt:
                        include_record = False
                if include_record and to_date:
                    to_dt = datetime.strptime(to_date, "%Y-%m-%d")
                    if record_date > to_dt:
                        include_record = False

            if include_record:
                filtered_records.append(record)

        return filtered_records
    except Exception as e:
        raise Exception(f"Error fetching data: {e}")


def get_tender_invitations(
    lang: str = "en",
    segment: str = "tender",
    pagesize: Optional[int] = None,
    offset: Optional[int] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
) -> Dict:
    """Get tender invitations in standardized format

    Returns:
        Dictionary with 'tender_invitations' key containing list of records
    """
    records = _get_tender_invitations(
        lang, segment, pagesize, offset, from_date, to_date, fetch_tender_invitations
    )
    return {"tender_invitations": records}
