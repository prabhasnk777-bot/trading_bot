import time
import random

class MockClient:
    """A minimal mock client that simulates Binance futures order responses.

    Use this for local testing without network calls or API keys.
    """
    def __init__(self):
        # simulate client state if needed
        self._next_id = random.randint(100000, 999999)

    def _make_order_response(self, symbol, side, type, quantity, price=None):
        self._next_id += 1
        executed = 0
        avg_price = "0"

        if type == "MARKET":
            # market orders are executed immediately in mock
            executed = quantity
            avg_price = round(random.uniform(1000.0, 70000.0), 2)
            status = "FILLED"
        else:
            # limit orders are created but not executed in this simple mock
            executed = 0
            avg_price = "0"
            status = "NEW"

        return {
            "orderId": self._next_id,
            "symbol": symbol,
            "side": side,
            "type": type,
            "status": status,
            "executedQty": str(executed),
            "origQty": str(quantity),
            "avgPrice": str(avg_price),
            "transactTime": int(time.time() * 1000)
        }

    # futures_create_order mirrors python-binance method signature used in bot.py
    def futures_create_order(self, symbol, side, type, quantity, price=None, timeInForce=None):
        return self._make_order_response(symbol, side, type, quantity, price)
