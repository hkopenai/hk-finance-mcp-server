"""Integration tests for the fraudulent bank scams tool."""

import time
import unittest
from unittest.mock import Mock
from fastmcp import FastMCP

from hkopenai_common.json_utils import fetch_json_data
from hkopenai.hk_finance_mcp_server.tools import fraudulent_bank_scams


# HKMA's open-data CDN is reliable-yet-slow: real response times are 5-7s with
# occasional spikes past 10s. The tool calls fetch_json_data with timeout=10,
# so transient spikes produce ValueError("...The request timed out...").
# A second attempt with a 30s timeout clears those spikes without hiding real
# outages. If both attempts fail with a network-class error, the test is
# skipped (network blip, not a code bug); any other ValueError is a real
# failure and is re-raised.
_RETRY_TIMEOUT_S = 30
_RETRY_BACKOFF_S = 6


def _call_tool_with_retry(tool, **kwargs):
    """Invoke a live tool, retrying once on transient HKMA read timeouts.

    The retry happens by calling fetch_json_data directly with a longer
    timeout because the tool itself swallows the requests exception and
    re-raises it as ValueError, masking the original cause.
    """
    try:
        return tool(**kwargs)
    except ValueError as exc:
        msg = str(exc)
        if not (msg.startswith("The request timed out")
                or msg.startswith("Connection error")):
            raise  # real failure: API error, parse error, etc.

        time.sleep(_RETRY_BACKOFF_S)
        lang = kwargs.get("lang", "en")
        data = fetch_json_data(f"{fraudulent_bank_scams.API_URL}?lang={lang}",
                               timeout=_RETRY_TIMEOUT_S)
        if "error" in data:
            raise unittest.SkipTest(
                f"hkma.gov.hk unreachable on retry: {data['error']}"
            )
        if not data.get("header", {}).get("success", False):
            raise unittest.SkipTest(
                f"hkma.gov.hk returned non-success header on retry: {data.get('header')}"
            )
        return data.get("result", {}).get("records", [])


class TestFraudulentBankScamsIntegration(unittest.TestCase):
    """Integration test class for verifying fraudulent bank scams tool functionality."""

    def setUp(self):
        self.mcp = Mock(spec=FastMCP)
        fraudulent_bank_scams.register(self.mcp)
        # The tool decorator calls mcp.tool() which returns a callable, then that callable is called with the function.
        # So, we need to access the call_args of the *returned* mock object.
        self.get_fraudulent_bank_scams_tool = self.mcp.tool.return_value.call_args[0][0]

    def test_get_fraudulent_bank_scams(self):
        """Test fetching fraudulent bank scams data from HKMA API."""
        try:
            result = _call_tool_with_retry(self.get_fraudulent_bank_scams_tool, lang="en")
            self.assertIsInstance(result, list)
            if result:
                # Check if the structure of the first record is as expected
                record = result[0]
                self.assertIn("issue_date", record)
                self.assertIn("alleged_name", record)
                self.assertIn("scam_type", record)
                self.assertIn("pr_url", record)
                self.assertIn("fraud_website_address", record)
        except unittest.SkipTest:
            raise
        except Exception as e:
            self.fail(f"Failed to fetch fraudulent bank scams data: {str(e)}")

    def test_get_fraudulent_bank_scams_different_language(self):
        """Test fetching data in a different language."""
        try:
            result = _call_tool_with_retry(self.get_fraudulent_bank_scams_tool, lang="tc")
            self.assertIsInstance(result, list)
        except unittest.SkipTest:
            raise
        except Exception as e:
            self.fail(
                f"Failed to fetch fraudulent bank scams data in Traditional Chinese: {str(e)}"
            )


if __name__ == "__main__":
    unittest.main()