import sys
import os

# Add the root path (one level up from 'backtester') to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

# from data_collector.price_watcher import stream_candles

# # from execution_engine.strategy import SimpleSMAStrategy
# from strategies.scalping import ScalpingStrategy

# # or your actual strategy
# from execution_engine.executor import TradeExecutor
# from config import settings

# # Setup strategy
# strategy = ScalpingStrategy(short_window=5, long_window=15)
# executor = TradeExecutor()


# def on_new_candle(candle_data):
#     """
#     This function is triggered on every new candle from price_watcher.
#     """
#     print("📊 New candle received:", candle_data)

#     # Step 1: Send candle to strategy
#     signal = strategy.evaluate(candle_data)
#     print("🧠 Signal:", signal)

#     # Step 2: Execute trade if signal is generated
#     if signal in ["buy", "sell"] and settings.ENABLE_ORDER_EXECUTION:
#         response = executor.place_order(
#             symbol="BTCUSDT", side=signal, order_type="MARKET", quantity=0.001
#         )
#         print("📦 Order response:", response)
#     elif signal:
#         print(f"🧪 DRY RUN: Would have placed a {signal.upper()} order.")


# # Kick off the stream
# if __name__ == "__main__":
#     print("🚀 Starting integration test...")
#     stream_candles(symbol="btcusdt", interval="1m", on_message=on_new_candle)

# from data_collector.price_watcher import start_price_stream
# import time

# if __name__ == "__main__":
#     start_price_stream()

#     # Keep the main thread alive to allow WebSocket to keep running
#     try:
#         while True:
#             time.sleep(1)
#     except KeyboardInterrupt:
#         print("Stopped manually.")
import time
from data_collector.price_watcher import start_price_stream


def run_integration_test():
    print("🔍 Starting integration test: price stream...")
    start_price_stream()
    print("✅ Stream started. Waiting for candle events...")

    try:
        # Run for a limited duration to observe logs
        time.sleep(120)  # 2 minutes
    except KeyboardInterrupt:
        print("🛑 Test interrupted by user.")


if __name__ == "__main__":
    run_integration_test()
