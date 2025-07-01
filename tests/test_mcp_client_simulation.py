# IMPORTANT: This test file must run sequentially and not in parallel to avoid conflicts with the MCP server subprocess.
import unittest
import subprocess
import json
import sys
import os
import time
import asyncio
import socket
import logging
from datetime import datetime, timedelta

# Configure logging
log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
logging.basicConfig(level=getattr(logging, log_level),
                    format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
from mcp.client.streamable_http import streamablehttp_client # Added for MCP SDK communication
from mcp import ClientSession


class TestMCPClientSimulation(unittest.TestCase):
    server_process = None
    SERVER_URL = "http://127.0.0.1:8000/mcp/" # Updated server URL for MCP API

    # Need a fresh mcp server to avoid lock up
    def setUp(self):
        logger.debug("Starting MCP server subprocess for HTTP communication...")
        # Start the MCP server as a subprocess. It should expose an HTTP endpoint.
        self.server_process = subprocess.Popen(
            [sys.executable, "-m", "hkopenai.hk_finance_mcp_server", "--sse"],
            # No stdin/stdout/stderr pipes needed for HTTP communication, but keep for server logs
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        logger.debug("MCP server subprocess started. Giving it a moment to start up and listen on HTTP...")
        # Give the server a moment to start up and listen on the port
        time.sleep(5) # Increased sleep time for server to fully initialize HTTP server

        # Check if the server is actually listening on the port
        for _ in range(10):
            try:
                with socket.create_connection(("127.0.0.1", 8000), timeout=1):
                    logger.debug("Server is listening on port 8000.")
                    break
            except OSError as e:
                logger.debug(f"Waiting for server to start: {e}")
                time.sleep(1)
        else:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                self.server_process.kill()
            raise Exception("Server did not start listening on port 8000 in time.")

        logger.debug(f"Server setup complete.")

    def tearDown(self):
        # Terminate the server process
        if self.server_process:
            self.server_process.terminate()
            self.server_process.wait(timeout=5)
            if self.server_process.poll() is None:
                logger.debug("Tear down complete.")
                self.server_process.kill()
            
            # Print any remaining stderr output from the server process
            if self.server_process.stdout:
                self.server_process.stdout.close()
            if self.server_process.stderr:
                stderr_output = self.server_process.stderr.read()
                if stderr_output:
                    logger.debug(f"Server stderr (remaining):\n{stderr_output}")
                else:
                    logger.debug("Server stderr (remaining): (empty)")
                self.server_process.stderr.close()
            logger.info("Tear down complete.")

    async def _call_tool_and_assert(self, tool_name, params):
        async with streamablehttp_client(self.SERVER_URL) as (read_stream, write_stream, _):
            async with ClientSession(read_stream, write_stream) as session:
                await session.initialize()
                response = await session.call_tool(tool_name, params)
                logger.info(f"'{tool_name}' tool response: {str(response)[:500]}...")

                json_text = response.content[0].text if response.content else "{}"
                data = json.loads(json_text)
                self.assertIsInstance(data, (dict, list), f"Result for {tool_name} should be a dictionary or list")
                if isinstance(data, dict):
                    self.assertNotIn("error", data, f"Result for {tool_name} should not contain an error: {data.get('error')}")
                elif isinstance(data, list) and data and isinstance(data[0], dict):
                    self.assertNotIn("error", data[0], f"Result for {tool_name} should not contain an error: {data[0].get('error')}")
                return data

    def test_get_business_stats_tool(self):
        logger.debug("Testing 'get_business_stats' tool...")
        asyncio.run(self._call_tool_and_assert("get_business_stats", {"start_year": 2023, "end_year": 2023}))

    def test_get_neg_equity_stats_tool(self):
        logger.debug("Testing 'get_neg_equity_stats' tool...")
        asyncio.run(self._call_tool_and_assert("get_neg_equity_stats", {"start_year": 2023, "end_year": 2023}))

    def test_get_credit_card_stats_tool(self):
        logger.debug("Testing 'get_credit_card_stats' tool...")
        asyncio.run(self._call_tool_and_assert("get_credit_card_stats", {"start_year": 2023, "end_year": 2023}))

    def test_get_coin_cart_tool(self):
        logger.debug("Testing 'get_coin_cart' tool...")
        asyncio.run(self._call_tool_and_assert("get_coin_cart", {}))

    def test_get_credit_card_hotlines_tool(self):
        logger.debug("Testing 'get_credit_card_hotlines' tool...")
        asyncio.run(self._call_tool_and_assert("get_credit_card_hotlines", {}))

    def test_get_hkma_tender_invitations_tool(self):
        logger.debug("Testing 'get_hkma_tender_invitations' tool...")
        asyncio.run(self._call_tool_and_assert("get_hkma_tender_invitations", {"lang": "en", "segment": "tender", "pagesize": 1}))

    def test_get_hibor_daily_stats_tool(self):
        logger.debug("Testing 'get_hibor_daily_stats' tool...")
        today = datetime.now()
        start_date = (today - timedelta(days=30)).strftime('%Y-%m-%d')
        end_date = today.strftime('%Y-%m-%d')
        asyncio.run(self._call_tool_and_assert("get_hibor_daily_stats", {"start_date": start_date, "end_date": end_date}))

    def test_get_atm_locations_tool(self):
        logger.debug("Testing 'get_atm_locations' tool...")
        asyncio.run(self._call_tool_and_assert("get_atm_locations", {"pagesize": 1}))

    def test_get_stamp_duty_statistics_tool(self):
        logger.debug("Testing 'get_stamp_duty_statistics' tool...")
        current_year_month = datetime.now().strftime('%Y%m')
        asyncio.run(self._call_tool_and_assert("get_stamp_duty_statistics", {"start_period": "202301", "end_period": current_year_month}))

    def test_get_bank_branch_locations_tool(self):
        logger.debug("Testing 'get_bank_branch_locations' tool...")
        asyncio.run(self._call_tool_and_assert("get_bank_branch_locations", {"pagesize": 1}))

    def test_get_fraudulent_bank_scams_tool(self):
        logger.debug("Testing 'get_fraudulent_bank_scams' tool...")
        asyncio.run(self._call_tool_and_assert("get_fraudulent_bank_scams", {"lang": "en"}))
