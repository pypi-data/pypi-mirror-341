from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from quantplay_mcp.client import QuantPlayClient

# Create an MCP server
load_dotenv()
api_key = os.getenv("QUANTPLAY_API_KEY")

if not api_key:
    raise ValueError("QUANTPLAY_API_KEY environment variable is required")

quantplay_client = QuantPlayClient(api_key=api_key)
mcp = FastMCP("Quantplay")


# Add a tool to get positions by nickname
@mcp.tool()
def get_accounts() -> list[dict]:
    """Get all broker Accounts for the user

    Returns:
        A list of account dictionaries
    """
    return quantplay_client.get_accounts()

# Add a tool to get positions by nickname
@mcp.tool()
def get_positions(nickname: str) -> list[dict]:
    """Get positions for a given nickname

    Args:
        nickname: The nickname to search positions for

    Returns:
        A list of position dictionaries
    """
    # Implementation needed here
    # For example:

    return quantplay_client.get_positions()

# Add a tool to get holdings by nickname
@mcp.tool()
def get_holdings(nickname: str) -> list[dict]:
    """Get holdings for a given nickname

    Args:
        nickname: The nickname to search holdings for

    Returns:
        A list of holdings dictionaries
    """
    # Implementation needed here
    # For example:

    return quantplay_client.get_holdings(nickname)

def main():
    print("Starting MCP server")
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()