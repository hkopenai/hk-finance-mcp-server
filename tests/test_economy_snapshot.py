"""
Unit tests for the economy snapshot tool.

Same conventions as test_weather_summary.py:
unittest.TestCase, @patch the underlying per-section helpers
(not the HTTP layer), and assert on the consolidated structure
returned by get_economy_snapshot.
"""

import asyncio
import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from hkopenai.hk_finance_mcp_server.tools.economy_snapshot import (
    _aggregate,
    register,
)


class TestEconomySnapshotTool(unittest.TestCase):
    """Test case class for the economy snapshot tool."""

    def test_register_tool(self):
        """Tests that the aggregator tool is correctly registered on a FastMCP mock."""
        mock_mcp = MagicMock()
        register(mock_mcp)
        self.assertEqual(mock_mcp.tool.call_count, 1)
        decorated_func = mock_mcp.tool.return_value.call_args[0][0]
        self.assertEqual(decorated_func.__name__, "get_economy_snapshot")

    def test_aggregate_returns_latest_from_each_series(self):
        """Each section returns the latest record (last item in list)."""
        # Arrange: every per-section helper returns a 3-element list,
        # one returns an empty list (-> None), one raises (-> error dict).
        def ok_hibor(start_date=None, end_date=None):
            return [
                {"date": "2026-09-29", "overnight": 3.10, "1_week": 3.30},
                {"date": "2026-09-30", "overnight": 3.15, "1_week": 3.35},
                {"date": "2026-10-01", "overnight": 3.21, "1_week": 3.42},
            ]

        def ok_neg_equity(start_year=None, start_month=None, end_year=None, end_month=None):
            return [
                {"quarter": "2025-Q4", "outstanding_loans": 100},
                {"quarter": "2026-Q1", "outstanding_loans": 150},
                {"quarter": "2026-Q2", "outstanding_loans": 175, "lv_ratio": 0.02},
            ]

        def ok_credit_card(start_year=None, start_month=None, end_year=None, end_month=None):
            return [
                {"quarter": "2025-Q4", "accounts_count": 1_900_000},
                {"quarter": "2026-Q1", "accounts_count": 1_920_000},
                {"quarter": "2026-Q2", "accounts_count": 1_945_000},
            ]

        def ok_stamp_duty(start_period=None, end_period=None):
            return [
                {"period": "202607", "scs_stamp_duty": 1_000},
                {"period": "202608", "scs_stamp_duty": 1_500},
                {"period": "202609", "scs_stamp_duty": 2_000},
            ]

        def empty_business(start_year=None, start_month=None, end_year=None, end_month=None):
            return []

        def boom_fraud(lang="en"):
            raise RuntimeError("HKMA API timeout")

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.hibor_daily._get_hibor_stats",
            side_effect=ok_hibor,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.neg_resident_mortgage._get_neg_equity_stats",
            side_effect=ok_neg_equity,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.credit_card._get_credit_card_stats",
            side_effect=ok_credit_card,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.stamp_duty_statistics._get_stamp_duty_statistics",
            side_effect=ok_stamp_duty,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.business_reg._get_business_stats",
            side_effect=empty_business,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.fraudulent_bank_scams._get_fraudulent_bank_scams",
            side_effect=boom_fraud,
        ):
            # Act
            payload = asyncio.run(_aggregate())

        # Assert: all sections present
        for key in (
            "hibor",
            "neg_equity",
            "credit_card",
            "stamp_duty",
            "business_reg",
            "active_fraud_alerts",
            "_meta",
        ):
            self.assertIn(key, payload, f"missing section {key!r}")

        # The healthy time-series sections are the LAST record from each helper
        self.assertEqual(payload["hibor"]["date"], "2026-10-01")
        self.assertEqual(payload["hibor"]["overnight"], 3.21)
        self.assertEqual(payload["neg_equity"]["quarter"], "2026-Q2")
        self.assertEqual(payload["neg_equity"]["lv_ratio"], 0.02)
        self.assertEqual(payload["credit_card"]["accounts_count"], 1_945_000)
        self.assertEqual(payload["stamp_duty"]["period"], "202609")

        # The empty series section is None (not missing, not error)
        self.assertIsNone(payload["business_reg"])

        # The failing section surfaces an error key
        # Note: active_fraud_alerts wraps fraud helper in _count_fraud_records,
        # which raises -> _run_section catches and converts to {"error": ...}
        self.assertIn("error", payload["active_fraud_alerts"])
        self.assertIn("RuntimeError", payload["active_fraud_alerts"]["error"])

        # Meta is well-formed
        meta = payload["_meta"]
        self.assertEqual(meta["generated_at"], date.today().isoformat())
        self.assertEqual(
            meta["sections"],
            [
                "hibor",
                "neg_equity",
                "credit_card",
                "stamp_duty",
                "business_reg",
                "active_fraud_alerts",
            ],
        )
        self.assertEqual(meta["sources"], "HKMA + IRD open data")

    def test_aggregate_fraud_count_is_int(self):
        """active_fraud_alerts is an int when the fraud endpoint returns a list."""
        def ok_fraud(lang="en"):
            return [{"role": "fake-bank", "reported_date": "2026-09-15"}] * 7

        def ok_hibor(start_date=None, end_date=None):
            return [{"date": "2026-10-01"}]

        def ok_neg(start_year=None, start_month=None, end_year=None, end_month=None):
            return [{"quarter": "2026-Q2"}]

        def ok_cc(start_year=None, start_month=None, end_year=None, end_month=None):
            return [{"quarter": "2026-Q2"}]

        def ok_sd(start_period=None, end_period=None):
            return [{"period": "202609"}]

        def ok_br(start_year=None, start_month=None, end_year=None, end_month=None):
            return [{"month": "2026-09"}]

        with patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.hibor_daily._get_hibor_stats",
            side_effect=ok_hibor,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.neg_resident_mortgage._get_neg_equity_stats",
            side_effect=ok_neg,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.credit_card._get_credit_card_stats",
            side_effect=ok_cc,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.stamp_duty_statistics._get_stamp_duty_statistics",
            side_effect=ok_sd,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.business_reg._get_business_stats",
            side_effect=ok_br,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.fraudulent_bank_scams._get_fraudulent_bank_scams",
            side_effect=ok_fraud,
        ):
            payload = asyncio.run(_aggregate())

        self.assertIsInstance(payload["active_fraud_alerts"], int)
        self.assertEqual(payload["active_fraud_alerts"], 7)

    def test_aggregate_picks_max_by_time_key_not_last_element(self):
        """The latest observation is selected by max(time_key), not by index.
        HKMA returns series in arbitrary order, so result[-1] is not safe.
        This test feeds records in scrambled order to lock the fix in.
        """
        scrambled_hibor = [
            {"date": "2026-09-30", "overnight": 3.10},
            {"date": "2026-10-15", "overnight": 3.99},  # this is the latest
            {"date": "2026-10-01", "overnight": 3.21},
            {"date": "2026-10-05", "overnight": 3.50},
        ]
        scrambled_neg = [
            {"quarter": "2026-Q1", "outstanding_loans": 100},
            {"quarter": "2025-Q4", "outstanding_loans": 90},
            {"quarter": "2026-Q2", "outstanding_loans": 175},
            {"quarter": "2026-Q3", "outstanding_loans": 200},  # actually latest
        ]
        with patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.hibor_daily._get_hibor_stats",
            return_value=scrambled_hibor,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.neg_resident_mortgage._get_neg_equity_stats",
            return_value=scrambled_neg,
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.credit_card._get_credit_card_stats",
            return_value=[],
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.stamp_duty_statistics._get_stamp_duty_statistics",
            return_value=[],
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.business_reg._get_business_stats",
            return_value=[],
        ), patch(
            "hkopenai.hk_finance_mcp_server.tools.economy_snapshot.fraudulent_bank_scams._get_fraudulent_bank_scams",
            return_value=[],
        ):
            payload = asyncio.run(_aggregate())
        self.assertEqual(payload["hibor"]["date"], "2026-10-15")
        self.assertEqual(payload["hibor"]["overnight"], 3.99)
        self.assertEqual(payload["neg_equity"]["quarter"], "2026-Q3")
        self.assertEqual(payload["neg_equity"]["outstanding_loans"], 200)


if __name__ == "__main__":
    unittest.main()