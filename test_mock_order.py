"""Simple script to test `place_order` using the mock client.

Run with: python test_mock_order.py
"""
from mock_client import MockClient
from bot import place_order

def run():
    client = MockClient()
    # Market order test
    resp = place_order(client, "BTCUSDT", "BUY", "MARKET", 0.001)
    print("Market order response:", resp)

    # Limit order test
    resp2 = place_order(client, "BTCUSDT", "SELL", "LIMIT", 0.001, price=60000)
    print("Limit order response:", resp2)

if __name__ == "__main__":
    run()
