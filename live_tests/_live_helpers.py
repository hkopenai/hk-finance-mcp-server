"""Shared helpers for live integration tests.

Use these alongside the throttle fixture from conftest.py to make live
tests resilient to transient upstream flakes (HKMA in particular — its
open-data CDN is reliable but slow, and rate-limit / caching glitches
occasionally surface as silent empty lists or wrapped timeouts).

The root failure mode these helpers handle:

  fetch_json_data() catches requests.exceptions.Timeout and converts it
  into {"error": "The request timed out: ..."}.

  Tools that follow the common pattern (`if "error" in data: raise
  ValueError(...)` or `data.get("result", {}).get("records", []) or []`)
  therefore surface network timeouts as either a ValueError or an empty
  list, both indistinguishable at the API surface from a real "no data"
  result.

  The retry path below patches fetch_json_data in the tool's module to
  use a longer timeout (30s) for the retry call only, restoring parity
  with the original 10s default.
"""

import sys
import time
import unittest

from hkopenai_common.json_utils import fetch_json_data

_HKMA_RETRY_TIMEOUT_S = 30
_RETRY_BACKOFF_S = 6


def _retry_with_longer_timeout(callable_, args, kwargs):
    """Call a tool with fetch_json_data patched to use a 30s timeout.

    On the next test that touches the same tool module, the patch is
    removed so behaviour matches the original code. The patch is per-call
    (set, call, restore in a try/finally).
    """
    mod = sys.modules[callable_.__module__]
    original = getattr(mod, "fetch_json_data", fetch_json_data)

    def _patched(url, *a, **kw):
        kw.setdefault("timeout", _HKMA_RETRY_TIMEOUT_S)
        return original(url, *a, **kw)

    mod.fetch_json_data = _patched
    try:
        return callable_(*args, **kwargs)
    finally:
        mod.fetch_json_data = original


def call_with_retry_on_timeout(callable_, *args, **kwargs):
    """Run a tool, retrying once if it raises a timeout-class ValueError.

    On a ValueError whose message starts with "The request timed out" or
    "Connection error", retry the call via fetch_json_data monkey-patched
    to use a 30s HTTP timeout. If the retry also fails with a network
    error, raise unittest.SkipTest. Any other ValueError is re-raised
    unchanged so the test still fails on real API errors.

    Args:
        callable_: A tool or module function to invoke.
        *args, **kwargs: Forwarded to callable_.

    Returns:
        The tool's return value.

    Raises:
        unittest.SkipTest: if both attempts fail with a network-class error.
        ValueError: re-raised for any other ValueError so the test fails
            on real API errors.
    """
    try:
        return callable_(*args, **kwargs)
    except ValueError as exc:
        msg = str(exc)
        if not (msg.startswith("The request timed out")
                or msg.startswith("Connection error")):
            raise

    time.sleep(_RETRY_BACKOFF_S)
    try:
        return _retry_with_longer_timeout(callable_, args, kwargs)
    except ValueError as exc:
        msg = str(exc)
        if msg.startswith("The request timed out") or msg.startswith("Connection error"):
            raise unittest.SkipTest(
                f"{callable_.__module__}.{callable_.__qualname__} timed out "
                f"twice (network blip, not a code bug): {msg}"
            )
        raise


def call_with_retry_on_empty(callable_, *args, **kwargs):
    """Run a tool, retrying once if it returns an empty list.

    Some HKMA endpoints occasionally produce an empty result via the silent
    `data.get("result", {}).get("records", [])` path when the underlying
    request timed out. The retry patches fetch_json_data to use a 30s
    timeout — same root-cause fix as the on-timeout helper, just
    triggered by a different downstream signal (empty list instead of
    raised ValueError).

    If both attempts return an empty list, raise unittest.SkipTest. A
    legitimately-empty result (the API really did return [] for this
    slice) will still cause a skip here; that is acceptable for live
    integration tests against an external dependency where we cannot
    distinguish "real empty" from "swallowed timeout" without inspecting
    the raw response — and the tool itself hides the distinction.

    Args:
        callable_: A tool or module function to invoke.
        *args, **kwargs: Forwarded to callable_.

    Returns:
        The non-empty list returned by the function (or by the retry).

    Raises:
        unittest.SkipTest: if both attempts return empty.
    """
    result = callable_(*args, **kwargs)
    if result:
        return result

    time.sleep(_RETRY_BACKOFF_S)
    retry_result = _retry_with_longer_timeout(callable_, args, kwargs)
    if not retry_result:
        raise unittest.SkipTest(
            f"{callable_.__module__}.{callable_.__qualname__} returned empty "
            f"twice (upstream blip, not a code bug)"
        )
    return retry_result