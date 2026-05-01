# Trading Bot

Simple Binance Futures Testnet trading bot with a mock client for local testing.

Setup

1. Create a `.env` file with your testnet keys:

```
API_KEY=your_testnet_api_key
API_SECRET=your_testnet_secret_key
```

2. Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run (mock):

```powershell
python bot.py --symbol BTCUSDT --side BUY --type MARKET --quantity 0.001 --mock
```

Run tests:

```powershell
python test_mock_order.py
```

Run the web UI:

```powershell
python web.py
# then open http://localhost:5000 in your browser
```
