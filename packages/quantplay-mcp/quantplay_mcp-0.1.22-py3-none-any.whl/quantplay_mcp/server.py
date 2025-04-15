from typing import Literal

from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
import os
from quantplay_mcp.client import QuantPlayClient
from quantplay_mcp.models import Account
import requests

# Create an MCP server
load_dotenv()
api_key = os.getenv("QUANTPLAY_API_KEY")

if not api_key:
    raise ValueError("QUANTPLAY_API_KEY environment variable is required")

quantplay_client = QuantPlayClient(api_key=api_key)
mcp = FastMCP("Quantplay")


# Add a tool to get positions by nickname
@mcp.tool()
def get_accounts() -> list[Account]:
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

    return quantplay_client.get_positions(nickname)

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

@mcp.tool()
def place_order(
    nickname: str,
    tradingsymbol: str,
    quantity: int,
    transaction_type: Literal["BUY", "SELL"],
    product: str = "CNC",
    price: float = 0,
    order_type: str = "MARKET",
    exchange: str = "NSE",
    tag: str = "MCP"
) -> dict:
    """Place an order using individual parameters.

    Args:
        nickname: Broker nickname.
        token: Token ID for the security.
        tradingsymbol: Trading symbol of the instrument.
        product: Product type (e.g., CNC, MIS).
        price: Price at which to place the order.
        order_type: Type of the order (e.g., LIMIT, MARKET).
        exchange: Exchange name (e.g., NSE, BSE).
        transaction_type: BUY or SELL.
        quantity: Number of units to order.
        tag: Custom tag for tracking.

    Returns:
        The API response as a dictionary.
    """
    order = {
        "nickname": nickname,
        "tradingsymbol": tradingsymbol,
        "product": product,
        "price": price,
        "order_type": order_type,
        "exchange": exchange,
        "transaction_type": transaction_type,
        "quantity": quantity,
        "tag": tag
    }

    quantplay_client.place_order(order)

def main():
    print("Starting MCP server")
    """Run the MCP server"""
    mcp.run()

if __name__ == "__main__":
    main()