import argparse
from fastmcp import FastMCP
from openaihk.hk_finance_mcp_server import tool_business_reg
from openaihk.hk_finance_mcp_server import tool_neg_resident_mortgage
from openaihk.hk_finance_mcp_server import tool_credit_card
from openaihk.hk_finance_mcp_server import tool_coin_cart
from openaihk.hk_finance_mcp_server import tool_hkma_tender
from typing import Dict, Annotated, Optional
from pydantic import Field

def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Finance Server")

    @mcp.tool(
        description="Get monthly statistics on the number of new business registrations in Hong Kong"
    )
    def get_business_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")]  = None,
        end_year: Annotated[Optional[int], Field(description="End Year")]  = None,
        end_month: Annotated[Optional[int], Field(description="End Month")]  = None
        ) -> Dict:
        return tool_business_reg.get_business_stats(start_year, start_month, end_year, end_month)

    @mcp.tool(
        description="Get statistics on residential mortgage loans in negative equity in Hong Kong"
    )
    def get_neg_equity_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None
    ) -> Dict:
        return tool_neg_resident_mortgage.get_neg_equity_stats(start_year, start_month, end_year, end_month)

    @mcp.tool(
        description="Get credit card lending survey results in Hong Kong"
    )
    def get_credit_card_stats(
        start_year: Annotated[Optional[int], Field(description="Start Year")] = None,
        start_month: Annotated[Optional[int], Field(description="Start Month")] = None,
        end_year: Annotated[Optional[int], Field(description="End Year")] = None,
        end_month: Annotated[Optional[int], Field(description="End Month")] = None
    ) -> Dict:
        return tool_credit_card.get_credit_card_stats(start_year, start_month, end_year, end_month)
    
    @mcp.tool(
        description="Get coin collection cart schedule in Hong Kong. The cart can charge your electronic wallet and you no long have to keep coins."
    )
    def get_coin_cart(
    ) -> Dict:
        return tool_coin_cart.get_coin_cart_schedule()

    @mcp.tool(
        description="Get list of hotlines for reporting loss of credit card from Hong Kong banks."
    )
    def get_credit_card_hotlines() -> Dict:
        return tool_credit_card.get_credit_card_hotlines()

    @mcp.tool(
        description="Get information of Tender Invitation and Notice of Award of Contracts from Hong Kong Monetary Authority"
    )
    def get_hkma_tender_invitations(
        lang: Annotated[Optional[str], Field(description="Language (en/tc/sc)", enum=["en", "tc", "sc"])] = 'en',
        segment: Annotated[Optional[str], Field(description="Type of records (tender/notice)", enum=["tender", "notice"])] = 'tender',
        pagesize: Annotated[Optional[int], Field(description="Number of records per page")] = None,
        offset: Annotated[Optional[int], Field(description="Starting record offset")] = None,
        from_date: Annotated[Optional[str], Field(description="Filter records from date (YYYY-MM-DD)")] = None,
        to_date: Annotated[Optional[str], Field(description="Filter records to date (YYYY-MM-DD)")] = None
    ) -> Dict:
        return tool_hkma_tender.get_tender_invitations(
            lang=lang,
            segment=segment,
            pagesize=pagesize,
            offset=offset,
            from_date=from_date,
            to_date=to_date
        )

    return mcp

def main():
    parser = argparse.ArgumentParser(description='HKO MCP Server')
    parser.add_argument('-s', '--sse', action='store_true',
                       help='Run in SSE mode instead of stdio')
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
