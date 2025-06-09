import argparse
from fastmcp import FastMCP
from . import tool_business_reg
from . import tool_neg_resident_mortgage
from . import tool_credit_card
from . import tool_coin_cart
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
        return tool_coin_cart() 

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
