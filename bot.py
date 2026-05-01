import argparse
import logging
import os
import sys
from binance.client import Client
from dotenv import load_dotenv

# Local mock client (used when testing without network/API keys)
try:
    from mock_client import MockClient
except Exception:
    MockClient = None

# Load environment variables from .env
load_dotenv()

API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

# Logging setup
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename=os.path.join("logs", "bot.log"),
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_client():
    """Create and return a Binance Client configured for the futures testnet.

    Note: you must set API_KEY and API_SECRET in the .env file for private endpoints.
    """
    if not API_KEY or not API_SECRET:
        print("\n⚠️  API_KEY or API_SECRET not found. Put your keys into the .env file.")

    client = Client(API_KEY, API_SECRET)

    # Point futures endpoints to the Binance Futures Testnet
    # This sets the FUTURES_URL used by futures endpoints in python-binance
    client.FUTURES_URL = "https://testnet.binancefuture.com/fapi"
    return client


def validate(symbol, side, order_type, quantity, price):
    side = side.upper() if isinstance(side, str) else side
    order_type = order_type.upper() if isinstance(order_type, str) else order_type

    if side not in ["BUY", "SELL"]:
        raise ValueError("Side must be BUY or SELL")
    if order_type not in ["MARKET", "LIMIT"]:
        raise ValueError("Type must be MARKET or LIMIT")
    if quantity <= 0:
        raise ValueError("Quantity must be > 0")
    if order_type == "LIMIT" and (price is None or price <= 0):
        raise ValueError("Price required for LIMIT and must be > 0")


def place_order(client, symbol, side, order_type, quantity, price=None):
    """Place a futures order and return the response from Binance.

    Logs both the request and the response to logs/bot.log.
    """
    logging.info(f"Request: {symbol} {side} {order_type} {quantity} {price}")

    try:
        if order_type == "MARKET":
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity
            )
        else:
            # LIMIT order requires price and timeInForce
            order = client.futures_create_order(
                symbol=symbol,
                side=side,
                type=order_type,
                quantity=quantity,
                price=price,
                timeInForce="GTC"
            )

        logging.info(f"Response: {order}")
        return order

    except Exception as e:
        logging.exception("Order failed")
        raise


def main():
    parser = argparse.ArgumentParser(description="Simple Binance Futures Testnet trading bot")

    parser.add_argument("--symbol", required=True, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("--side", required=True, help="BUY or SELL")
    parser.add_argument("--type", required=True, dest="order_type", help="MARKET or LIMIT")
    parser.add_argument("--quantity", type=float, required=True, help="Order quantity (contracts or asset amount)")
    parser.add_argument("--price", type=float, help="Price for LIMIT orders")
    parser.add_argument("--mock", action="store_true", help="Use mock client (no network calls)")

    args = parser.parse_args()

    # Normalize
    side = args.side.upper()
    order_type = args.order_type.upper()

    try:
        validate(args.symbol, side, order_type, args.quantity, args.price)

        print("\n📌 Order Summary")
        print(args.symbol, side, order_type, args.quantity, args.price)

        if args.mock:
            if MockClient is None:
                raise RuntimeError("Mock client not available")
            client = MockClient()
        else:
            client = get_client()

        print("\n🚀 Placing order...")
        order = place_order(
            client,
            args.symbol,
            side,
            order_type,
            args.quantity,
            args.price
        )

        print("\n✅ SUCCESS")
        # futures endpoints return different keys; print helpful ones
        print("Order ID:", order.get("orderId") or order.get("clientOrderId") or "N/A")
        print("Status:", order.get("status", "N/A"))
        print("Executed Qty:", order.get("executedQty", "N/A"))
        print("Avg Price:", order.get("avgPrice", "N/A"))

    except Exception as e:
        print("\n❌ FAILED")
        print("Error:", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
