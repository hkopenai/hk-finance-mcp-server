import argparse
from fastmcp import FastMCP
from hkopenai.hk_finance_mcp_server import tool_business_reg
from hkopenai.hk_finance_mcp_server import tool_neg_resident_mortgage
from hkopenai.hk_finance_mcp_server import tool_credit_card
from hkopenai.hk_finance_mcp_server import tool_coin_cart
from hkopenai.hk_finance_mcp_server import tool_hkma_tender
from hkopenai.hk_finance_mcp_server import tool_hibor_daily
from hkopenai.hk_finance_mcp_server import tool_atm_locator
from hkopenai.hk_finance_mcp_server import tool_stamp_duty_statistics
from hkopenai.hk_finance_mcp_server import tool_bank_branch_locator
from hkopenai.hk_finance_mcp_server import tool_fraudulent_bank_scams

from typing import Dict, Annotated, Optional, List
from pydantic import Field


def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Finance Server")

    @mcp.tool(
        description="Get monthly statistics on the number of new business registrations in Hong Kong"
    )
    def get_business_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None,
    ) -> List[Dict]:
        return tool_business_reg.get_business_stats(
            start_year, start_month, end_year, end_month
        )

    @mcp.tool(
        description="Get statistics on residential mortgage loans in negative equity in Hong Kong"
    )
    def get_neg_equity_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None,
    ) -> List[Dict]:
        return tool_neg_resident_mortgage.get_neg_equity_stats(
            start_year, start_month, end_year, end_month
        )

    @mcp.tool(description="Get credit card lending survey results in Hong Kong")
    def get_credit_card_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None,
    ) -> List[Dict]:
        return tool_credit_card.get_credit_card_stats(
            start_year, start_month, end_year, end_month
        )

    @mcp.tool(
        description="Get coin collection cart schedule in Hong Kong. The cart can charge your electronic wallet and you no long have to keep coins."
    )
    def get_coin_cart() -> Dict:
        return tool_coin_cart.get_coin_cart_schedule()

    @mcp.tool(
        description="Get list of hotlines for reporting loss of credit card from Hong Kong banks."
    )
    def get_credit_card_hotlines() -> List[Dict]:
        return tool_credit_card.get_credit_card_hotlines()

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
        return tool_hkma_tender.get_tender_invitations(
            lang=lang if lang is not None else "en",
            segment=segment if segment is not None else "tender",
            pagesize=pagesize,
            offset=offset,
            from_date=from_date,
            to_date=to_date,
        )

    @mcp.tool(
        description="Get daily figures of Hong Kong Interbank Interest Rates (HIBOR) from HKMA"
    )
    def get_hibor_daily_stats(
        start_date: Annotated[
            Optional[str], Field(description="Start date (YYYY-MM-DD)")
        ] = None,
        end_date: Annotated[
            Optional[str], Field(description="End date (YYYY-MM-DD)")
        ] = None,
    ) -> List[Dict]:
        return tool_hibor_daily.get_hibor_stats(start_date, end_date)

    @mcp.tool(
        description="Get information on Automated Teller Machines (ATMs) of retail banks in Hong Kong"
    )
    def get_atm_locations(
        district: Annotated[
            Optional[str], Field(description="District name to filter results")
        ] = None,
        bank_name: Annotated[
            Optional[str], Field(description="Bank name to filter results")
        ] = None,
        pagesize: Annotated[
            Optional[int], Field(description="Number of records per page")
        ] = 100,
        offset: Annotated[
            Optional[int], Field(description="Starting record offset")
        ] = 0,
    ) -> List[Dict]:
        return tool_atm_locator.get_atm_locations(district, bank_name, pagesize, offset)

    @mcp.tool(
        description="Get monthly statistics on stamp duty collected from transfer of Hong Kong stock (both listed and unlisted)"
    )
    def get_stamp_duty_statistics(
        start_period: Annotated[
            Optional[str],
            Field(description="Start period in YYYYMM format to filter results"),
        ] = None,
        end_period: Annotated[
            Optional[str],
            Field(description="End period in YYYYMM format to filter results"),
        ] = None,
    ) -> List[Dict]:
        return tool_stamp_duty_statistics.get_stamp_duty_statistics(
            start_period, end_period
        )

    @mcp.tool(
        description="Get information on bank branch locations of retail banks in Hong Kong"
    )
    def get_bank_branch_locations(
        district: Annotated[
            Optional[str], Field(description="District name to filter results")
        ] = None,
        bank_name: Annotated[
            Optional[str], Field(description="Bank name to filter results")
        ] = None,
        lang: Annotated[
            Optional[str],
            Field(
                description="Language for data output (en, tc, sc)",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
        pagesize: Annotated[
            Optional[int], Field(description="Number of records per page")
        ] = 100,
        offset: Annotated[
            Optional[int], Field(description="Starting record offset")
        ] = 0,
    ) -> List[Dict]:
        return tool_bank_branch_locator.get_bank_branch_locations(
            district, bank_name, lang, pagesize, offset
        )

    @mcp.tool(
        description="Get information on fraudulent bank websites and phishing scams reported to HKMA"
    )
    def get_fraudulent_bank_scams(
        lang: Annotated[
            Optional[str],
            Field(
                description="Language (en/tc/sc)",
                json_schema_extra={"enum": ["en", "tc", "sc"]},
            ),
        ] = "en",
    ) -> List[Dict]:
        return tool_fraudulent_bank_scams.get_fraudulent_bank_scams(
            lang if lang is not None else "en"
        )

    return mcp


def main():
    parser = argparse.ArgumentParser(description="HKO MCP Server")
    parser.add_argument(
        "-s", "--sse", action="store_true", help="Run in SSE mode instead of stdio"
    )
    args = parser.parse_args()

    server = create_mcp_server()

    if args.sse:
        server.run(transport="streamable-http")
        print("HKO MCP Server running in SSE mode on port 8000")
    else:
        server.run()
        print("HKO MCP Server running in stdio mode")


if __name__ == "__main__":
    main()
