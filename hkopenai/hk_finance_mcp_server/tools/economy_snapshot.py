"""
Economy Snapshot Tool - Returns the latest observation from each
of Hong Kong's main HKMA/IRD time-series endpoints in a single
MCP call.

The Hong Kong Monetary Authority exposes ~8 distinct time-series
endpoints (HIBOR daily, residential mortgage negative equity
quarterly, credit card lending quarterly, business registration
monthly, etc.) plus a fraud-alert list and two locators. Each
existing tool in this package wraps exactly one endpoint.

An agent that needs "the current state of HK's economy" today
has to call five different `tools/call` round-trips, know that
"latest" means "last record in the API's natural order", and
sequentially stitch five responses together. This module adds a
single `get_economy_snapshot` tool that fetches the latest
observation from each of those five time series concurrently
via `asyncio.gather`, plus a count of currently-listed fraudulent
bank websites as an operational alert signal.

The aggregator reuses the existing per-section private helpers
rather than re-implementing the HTTP calls, so URL paths, date
filtering logic, validation stay where they are.

Capabilities deliberately NOT included and why:
- `coin_cart`: not time-keyed (static schedule). Doesn't fit "latest.
- `hkma_tender`: list of contracts, not a time series.
- `credit_card_hotlines`: static hotline list, not time series.
- `bank_branch_locator` / `atm_locator`: locators, not observations.
- `fraudulent_bank_scams`: used as a count signal, not as a time
  series. The full list is one tool call away if needed.
- `licensed_banks_historical`: static list, not time series.
"""

import asyncio
from datetime import date
from typing import Any, Awaitable, Callable, Dict, List, Optional, Tuple

from fastmcp import FastMCP

from . import business_reg, credit_card, fraudulent_bank_scams, hibor_daily, neg_resident_mortgage, stamp_duty_statistics


# Type aliases for clarity
SyncFactory = Callable[[], Any]


def _build_factories() -> List[Tuple[str, SyncFactory]]:
    """
    Return the ordered list of (section_key, callable-returning-latest-observation).

    Each callable returns either:
      - a single dict (the latest observation), or
      - None (if the underlying series is empty), or
      - {"error": "..."} if the underlying fetch already produced an error.

    "Latest" is selected by lexicographic maximum of each series' time key
    (e.g. ``"date": "2026-10-01"`` or ``"quarter": "2026-Q2"``). This is safe
    for all currently supported sections because their period keys are
    zero-padded and lex-sort equals time-sort.
    """
    def latest_or_none(fn, time_key: str, *args, **kw) -> Optional[Dict[str, Any]]:
        result = fn(*args, **kw)
        if isinstance(result, dict) and "error" in result:
            return result
        if isinstance(result, list):
            if not result:
                return None
            return max(result, key=lambda r: r.get(time_key, ""))
        return result

    return [
        ("hibor",        lambda: latest_or_none(hibor_daily._get_hibor_stats, time_key="date")),
        ("neg_equity",   lambda: latest_or_none(neg_resident_mortgage._get_neg_equity_stats, time_key="quarter")),
        ("credit_card",  lambda: latest_or_none(credit_card._get_credit_card_stats, time_key="quarter")),
        ("stamp_duty",   lambda: latest_or_none(stamp_duty_statistics._get_stamp_duty_statistics, time_key="period")),
        ("business_reg", lambda: latest_or_none(business_reg._get_business_stats, time_key="year_month")),
        ("active_fraud_alerts", lambda: _count_fraud_records()),
    ]


def _count_fraud_records() -> int:
    """Count currently-listed fraudulent bank websites / phishing scams."""
    result = fraudulent_bank_scams._get_fraudulent_bank_scams(lang="en")
    if isinstance(result, dict) and "error" in result:
        raise RuntimeError(result["error"])
    if isinstance(result, list):
        return len(result)
    return 0


async def _run_section(
    name: str, factory: SyncFactory
) -> Tuple[str, Any]:
    """Run one sync section helper in the default executor, catching all errors."""
    loop = asyncio.get_running_loop()
    try:
        result = await loop.run_in_executor(None, factory)
        return name, result
    except Exception as exc:  # noqa: BLE001 - deliberately swallow per-section failures
        return name, {"error": f"{type(exc).__name__}: {exc}"}


async def _aggregate() -> Dict[str, Any]:
    """Fan out to all section factories concurrently and assemble the dashboard."""
    sections = _build_factories()
    tasks: List[Awaitable[Tuple[str, Any]]] = [
        _run_section(name, factory) for name, factory in sections
    ]
    results = await asyncio.gather(*tasks)
    payload: Dict[str, Any] = dict(results)
    payload["_meta"] = {
        "generated_at": date.today().isoformat(),
        "sections": [name for name, _ in sections],
        "sources": "HKMA + IRD open data",
    }
    return payload


def register(mcp: FastMCP) -> None:
    """Register the economy snapshot tool with the FastMCP server."""

    @mcp.tool(
        description=(
            "Get a one-shot snapshot of Hong Kong's macro-finance state: the latest "
            "observation from each of the five main HKMA/IRD time series (HIBOR "
            "daily, residential mortgage negative equity quarterly, credit card "
            "lending quarterly, stamp duty monthly, business registration monthly) "
            "plus a count of currently-listed fraudulent bank websites. Internally "
            "fans out to all endpoints concurrently; per-section failures are "
            "reported as {\"error\": \"...\"} rather than failing the whole call. "
            "Use this for an at-a-glance current-state view. For historical "
            "ranges or time-series analysis, call the underlying per-series tools."
        ),
    )
    async def get_economy_snapshot(lang: str = "en") -> Dict[str, Any]:
        """
        Aggregated Hong Kong economy snapshot (latest observation per series).

        Args:
            lang: Reserved for future use. HKMA/IRD open-data endpoints are
                bilingual by source; current sections do not filter on lang.
                Kept for API symmetry with other aggregator tools.

        Returns:
            Dict with one key per section plus a `_meta` key listing the
            sections fetched and the response generation date. Each section
            value is either the latest observation dict, None (if the series
            was empty), or {"error": "..."} if that section's upstream call
            failed. `active_fraud_alerts` is an int count.
        """
        return await _aggregate()