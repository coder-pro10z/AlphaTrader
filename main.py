from execution_engine.binance_connector import BinanceConnector
import sys
import os

# Add the root path (one level up from 'backtester') to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
# from execution_engine.executor import BinanceExecutor

# # executor = BinanceExecutor(account_type="spot")

# # # Place a test market buy order
# # response = executor.place_order(
# #     symbol="BTCUSDT",
# #     side="BUY",
# #     order_type="MARKET",
# #     quantity=0.001
# # )

# # print(response)


# # executor = BinanceConnector(account_type="spot")

# # # Place a Market Order
# # response = executor.place_order(
# #     symbol="BTCUSDT",
# #     side="BUY",
# #     order_type="MARKET",
# #     quantity=0.001
# # )

# # print(response)

# # main.py

# # from strategies.scalping import find_scalping_opportunity
# # from risk_manager.risk_control import check_risk
# # from execution_engine.mock_executor import place_order

# # import pandas as pd

# # # Mock: Assume we fetched real-time candles
# # data = {
# #     "timestamp": range(5),
# #     "open": [100, 102, 104, 106, 108],
# #     "high": [101, 103, 105, 107, 109],
# #     "low": [99, 101, 103, 105, 107],
# #     "close": [100, 102, 104, 106, 110],  # Last close is high
# #     "volume": [10, 10, 10, 10, 10]
# # }
# # df = pd.DataFrame(data)

# # # Step 1: Strategy gives a signal
# # signal = find_scalping_opportunity(df)
# # symbol = "BTCUSDT"
# # quantity = 0.3

# # # Step 2: Risk Manager approves/rejects
# # if check_risk(symbol, quantity, signal):
# #     # Step 3: If approved, place order
# # #     print(f"🚀 Placing {signal} order for {quantity} {symbol}")
# # # else:
# # #     print("🛑 Trade Blocked by Risk Manager.")
# #         # Step 3: Mock execution engine places order
# #     response = place_order(symbol, quantity, side=signal)
# # else:
# #     print("🛑 Trade Blocked by Risk Manager.")

# # main.py

# # from strategies.scalping import find_scalping_opportunity
# # from risk_manager.risk_control import RiskManager
# # from execution_engine.mock_executor import MockExecutor

# # def main():
# #     print("🚀 Starting AlphaTrader...")

# #     # Initialize components
# #     risk_manager = RiskManager(max_daily_loss=50, max_trades_per_day=10)
# #     executor = MockExecutor()

# #     # Example market data (normally you'd get this from real-time API)
# #     market_data = {
# #         'price': 30000,
# #         'moving_average': 29950
# #     }

# #     # Step 1: Find a trading opportunity
# #     signal = find_scalping_opportunity(market_data)

# #     if signal:
# #         print(f"📈 Signal detected: {signal}")

# #         # Step 2: Risk Management Check
# #         if risk_manager.can_place_trade():
# #             # Step 3: Execute the trade
# #             order = executor.place_order(symbol="BTCUSDT", side=signal, quantity=0.001)
# #             print(f"✅ Order placed: {order}")

# #             # Step 4: Update Risk Manager with trade result (Example: Simulate small profit)
# #             risk_manager.update_after_trade(pnl=5)  
# #         else:
# #             print("⚠️ Risk limits reached. Cannot place trade.")
# #     else:
# #         print("🔍 No trading signal found.")

# # if __name__ == "__main__":
# #     main()

# # from risk_manager.risk_control import RiskManager

# # risk_manager = RiskManager()

# # # Example trade
# # if risk_manager.check_risk("BTCUSDT", quantity=0.01, signal="BUY", price=30000):
# #     print("Trade allowed, sending order...")

# # # Reset at day end
# # risk_manager.reset_daily_limits()

# # # working
# # from risk_manager.risk_control import RiskManager

# # risk_manager = RiskManager(max_daily_loss=50, max_trades_per_day=10)
# # if risk_manager.can_place_trade():
# #     risk_manager.update_after_trade(pnl=5)

# # main.py

# IS_BACKTEST = True  # 🔄 Toggle this to False for live trading

# from strategies.scalping import find_scalping_opportunity
# from execution_engine.mock_executor import MockExecutor
# # from execution_engine.executor import RealExecutor  # Assume this is implemented
# from risk_manager.risk_control import RiskManager
# import pandas as pd

# # Create mock historical candle data with a 'close' column
# market_data = pd.DataFrame({
#     'close': [29800, 29900, 30000, 29950, 30050, 30100]
# })

# def main():
#     print("🚀 Starting AlphaTrader...")

#     # Choose Executor based on mode
#     executor = MockExecutor() if IS_BACKTEST else print("Execute RealExecutor")
#     # RealExecutor()
#     risk_manager = RiskManager(max_daily_loss=50, max_trades_per_day=10)

#     # Simulated market data (live or test)
#     # market_data = {
#     #     'price': 30000,
#     #     'moving_average': 29950
#     # }

#     signal = find_scalping_opportunity(market_data)

#     if signal:
#         print(f"📈 Signal: {signal}")
#         if risk_manager.can_place_trade():
#             order = executor.place_order(symbol="BTCUSDT", side=signal, quantity=0.001)
#             print(f"✅ Order placed: {order}")
#             risk_manager.update_after_trade(pnl=5 if IS_BACKTEST else order.get("pnl", 0))
#         else:
#             print("⚠️ Risk check failed.")
#     else:
#         print("🔍 No signal found.")

# if __name__ == "__main__":
#     main()

# main.py

import pandas as pd
from strategies.scalping import find_scalping_opportunity
# from execution_engine.mock_executor import place_order
from execution_engine.mock_executor import MockExecutor
from risk_manager.risk_control import RiskManager

IS_BACKTEST = True

def main():
    print("🚀 Starting AlphaTrader...")

    # Choose Executor based on mode
    executor = MockExecutor() if IS_BACKTEST else print("Execute RealExecutor")
    # RealExecutor()
    risk_manager = RiskManager(max_daily_loss=50, max_trades_per_day=10)

    # ✅ Mock historical 'close' data
    # market_data = pd.DataFrame({
    #     'close': [29800, 29900, 30000, 29950, 30050, 30100, 30000, 29900, 29850, 30050]
    # })
    # market_data = pd.DataFrame({
    # 'close': [29800, 29850, 29900, 29950, 30000, 30050, 30100, 30200, 30300, 30400]
    # })
    # print(market_data[['close', 'sma_5', 'sma_10']].tail())
# ✅ Mock historical 'close' data
    # market_data = pd.DataFrame({
    #     'close': [29800, 29850, 29900, 29950, 30000, 30050, 30100, 30200, 30300, 30400]
    # })
    # market_data = pd.DataFrame({
    # 'close': [30500, 30400, 30300, 30200, 30100, 30000, 30100, 30200, 30300, 30400]
    # })
    # market_data = pd.DataFrame({
    # 'close': [30000, 30050, 30100, 30150, 30200, 30300, 30400, 30500, 30600, 30700]
    # })
    # market_data = pd.DataFrame({
    # 'close': [30000, 29900, 29800, 29700, 29600, 29700, 29800, 29900, 30000, 30100, 30200]
    # })

    # market_data = pd.DataFrame({
    # 'close': [30200, 30100, 30000, 29900, 29800, 29900, 30000, 30100, 30200, 30300, 30400]
    # })
    # market_data = pd.DataFrame({
    # 'close': [30500, 30400, 30300, 30200, 30100, 30000, 29900, 29800, 29700, 29600, 29800]
    # })
    # market_data = pd.DataFrame({
    # 'close': [
    #     30700, 30600, 30500, 30400, 30300,  # ↓ SMA5 > SMA10 here
    #     30200, 30100, 30000, 29900, 29800,  # ↓ SMA5 crosses BELOW SMA10
    #     30100, 30400                        # ↑ Now SMA5 crosses ABOVE SMA10 ✅
    # ]
    # })
    
    #Gauranteed Buy Order
    # 12 data points so that SMA10 exists at index 10 and 11
    # market_data = pd.DataFrame({
    # 'close': [
    #     31000, 30900, 30800, 30700, 30600,  # these 5 set SMA10 up high
    #     30500, 30400, 30300, 30200, 30100,  # these lower the SMA10 below SMA5
    #     31500, 32000                        # these two push SMA5 above SMA10
    # ]
    # })

#     market_data = pd.DataFrame({
#     'close': [
#         280, 275, 270, 265, 260,  # Start high
#         250, 240, 230, 220, 210,  # Falling
#         200, 190                  # Sharply down → SMA_5 dives
#     ]
# })
    #Gauranteed Sell Order
#     market_data = pd.DataFrame({
#     'close': [
#         280, 275, 270, 265, 260,  # Start high
#         250, 240, 230, 220, 210,  # Falling
#         200, 190                  # Sharply down → SMA_5 dives
#     ]
# })
    # market_data = pd.DataFrame({
    #     'close': [290, 290, 290, 290, 290, 300, 300, 300, 300, 300, 200, 100]
    # })
    # “Dropped prices too late—SMA window still too ‘stale’ on the previous row.”
#     market_data = pd.DataFrame({
#     'close': [
#         290, 290, 290, 290, 290,  # plateau
#         300, 300, 300, 300, 300,  # peak to push SMA₅ above SMA₁₀
#         200,                      # first drop for “prev” cross
#         100                       # second drop for “current” cross
#     ]
# })

#     market_data = pd.DataFrame({
#     'close': [100,100,100,100,100, 200,200,200,200,200, 50,50]
# })

# Gauranteed Scalping sell Signal RMA
    market_data = pd.DataFrame({
    'close': [100,100,100,100,100,200,200,200,200,200,50,50]
})



    # Calculate SMAs for debug print
    market_data['sma_5'] = market_data['close'].rolling(window=5).mean()
    market_data['sma_10'] = market_data['close'].rolling(window=10).mean()

    print(market_data[['close', 'sma_5', 'sma_10']].tail())

    signal = find_scalping_opportunity(market_data)

    if signal:
        print(f"📈 Signal: {signal}")
        if risk_manager.can_place_trade():
            order = executor.place_order(symbol="BTCUSDT", side=signal, quantity=0.001)
            print(f"✅ Order placed: {order}")
            risk_manager.update_after_trade(pnl=5 if IS_BACKTEST else order.get("pnl", 0))
        else:
            print("⚠️ Risk check failed.")
    else:
        print("🔍 No signal found.")

if __name__ == "__main__":
    main()

