from mcp.server.fastmcp import FastMCP
from quantplay_mcp.client import QuantPlayClient

# Create an MCP server
mcp = FastMCP("Quantplay")
quantplay_client = QuantPlayClient(api_key="i8Nj5w7ix3Hsk8Na")


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
    positions = [
        {
            "tradingsymbol": "SENSEX2541575300CE",
            "sell_value": 10725.71,
            "average_price": 536.29,
            "quantity": -20,
            "buy_value": 0.0,
            "product": "NRML",
            "ltp": 615.95,
            "pnl": -1593.2,
            "token": 874786,
            "exchange": "BFO",
            "sell_quantity": 20,
            "option_type": "CE",
            "buy_quantity": 0,
            "instrument_token": 223945221
        }
    ] # Replace with actual implementation
    return positions


# Add a dynamic greeting resource
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    """Get a personalized greeting"""
    return f"Hello, {name}!"