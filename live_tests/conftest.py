"""Shared fixtures for live integration tests.

These tests hit real upstream APIs (HKMA, HKO, AOF, IRD, etc.). Running them
back-to-back without any throttle will trip the upstream rate-limiter and
produce spurious 502/429 errors. The `throttle` fixture below sleeps for a
short, configurable interval before each test so that a full ``pytest
live_tests`` run stays well below typical per-second request budgets.
"""

import os
import time
import pytest

# Default pause between live tests. Override with the LIVE_TEST_THROTTLE_S
# environment variable when running against APIs that need a longer cool-down
# (e.g. when investigating 502s). 1.5s is a safe default for the HKMA / HKO /
# AOF / IRD endpoints used by this server.
DEFAULT_THROTTLE_SECONDS = float(os.environ.get("LIVE_TEST_THROTTLE_S", "1.5"))


@pytest.fixture(autouse=True)
def throttle():
    """Sleep DEFAULT_THROTTLE_SECONDS before every live test."""
    time.sleep(DEFAULT_THROTTLE_SECONDS)


def pytest_collection_modifyitems(config, items):
    """Auto-mark every test collected under live_tests/ with `live`.

    The `live` marker is declared in pyproject.toml's [tool.pytest.ini_options].
    Without this hook, every test file would need a `@pytest.mark.live`
    decorator on each class or method. The hook is local to this conftest
    (auto-applied only to items collected in this directory tree), so unit
    tests under tests/ remain unmarked.

    Combined with `pytest -m "not live"` in CI, this skips the live suite
    entirely on PR runs (where real upstream access is flaky from CI IPs).
    Developers can opt in with `pytest -m live` or `pytest live_tests/`.
    """
    live_marker = pytest.mark.live
    for item in items:
        # `item.nodeid` starts with "live_tests/" for anything collected in
        # this directory. The skip on items already marked avoids re-marking.
        if item.nodeid.startswith("live_tests/") and "live" not in item.keywords:
            item.add_marker(live_marker)