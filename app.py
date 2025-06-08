import argparse
from fastmcp import FastMCP
import tools
from typing import Dict

def create_mcp_server():
    """Create and configure the MCP server"""
    mcp = FastMCP(name="HK OpenAI Finance aServer")

    @mcp.tool(
        description="Get monthly statistics on the number of new business registrations in Hong Kong"
    )
    def get_weather_warning() -> Dict:
        return tools.get_new_business_reg()

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
