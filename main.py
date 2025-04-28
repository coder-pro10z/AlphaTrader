from execution_engine.binance_connector import BinanceConnector
# from execution_engine.executor import BinanceExecutor

# executor = BinanceExecutor(account_type="spot")

# # Place a test market buy order
# response = executor.place_order(
#     symbol="BTCUSDT",
#     side="BUY",
#     order_type="MARKET",
#     quantity=0.001
# )

# print(response)


# executor = BinanceConnector(account_type="spot")

# # Place a Market Order
# response = executor.place_order(
#     symbol="BTCUSDT",
#     side="BUY",
#     order_type="MARKET",
#     quantity=0.001
# )

# print(response)

# main.py

from strategies.scalping import find_scalping_opportunity
from risk_manager.risk_control import check_risk
from execution_engine.mock_executor import place_order

import pandas as pd

# Mock: Assume we fetched real-time candles
data = {
    "timestamp": range(5),
    "open": [100, 102, 104, 106, 108],
    "high": [101, 103, 105, 107, 109],
    "low": [99, 101, 103, 105, 107],
    "close": [100, 102, 104, 106, 110],  # Last close is high
    "volume": [10, 10, 10, 10, 10]
}
df = pd.DataFrame(data)

# Step 1: Strategy gives a signal
signal = find_scalping_opportunity(df)
symbol = "BTCUSDT"
quantity = 0.3

# Step 2: Risk Manager approves/rejects
if check_risk(symbol, quantity, signal):
    # Step 3: If approved, place order
#     print(f"🚀 Placing {signal} order for {quantity} {symbol}")
# else:
#     print("🛑 Trade Blocked by Risk Manager.")
        # Step 3: Mock execution engine places order
    response = place_order(symbol, quantity, side=signal)
else:
    print("🛑 Trade Blocked by Risk Manager.")

