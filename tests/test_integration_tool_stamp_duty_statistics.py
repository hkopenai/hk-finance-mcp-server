import unittest
from hkopenai.hk_finance_mcp_server import tool_stamp_duty_statistics


class TestStampDutyStatisticsIntegration(unittest.TestCase):
    def test_fetch_stamp_duty_data_integration(self):
        result = tool_stamp_duty_statistics.fetch_stamp_duty_data()

        self.assertTrue(
            len(result) > 0, "Expected to fetch at least one stamp duty record"
        )
        self.assertIn("period", result[0], "Expected 'period' field in result")
        self.assertIn("sd_listed", result[0], "Expected 'sd_listed' field in result")
        self.assertIn(
            "sd_unlisted", result[0], "Expected 'sd_unlisted' field in result"
        )

    def test_get_stamp_duty_statistics_with_period_filter(self):
        result = tool_stamp_duty_statistics.get_stamp_duty_statistics(
            start_period="202501", end_period="202502"
        )

        self.assertTrue(
            len(result) > 0,
            "Expected to fetch at least one stamp duty record within the period range",
        )
        for record in result:
            self.assertTrue(
                "202501" <= record["period"] <= "202502",
                "Expected all results to be within the specified period range",
            )


if __name__ == "__main__":
    unittest.main()
