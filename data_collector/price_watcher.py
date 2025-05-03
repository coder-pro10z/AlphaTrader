import sys
import os

# Add the root path (one level up from 'backtester') to Python path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
)  # data_collector/price_watcher.py

# import json
# import threading
# from websocket import WebSocketApp
# from utils.logger import log_event
# from strategies.scalping import evaluate_trade_signal
# from execution_engine.executor import Executor  # Switch between MockExecutor and live
# from config import settings

# SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()  # e.g., 'btcusdt'
# STREAM_URL = (
#     f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"
#     if settings.USE_TESTNET
#     else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"
# )

# executor = Executor("futures")  # Choose 'spot' or 'futures' accordingly


# def on_message(ws, message):
#     try:
#         data = json.loads(message)
#         candle = data["k"]  # Kline data

#         if candle["x"]:
#             # Candle closed
#             close_price = float(candle["c"])
#             log_event(f"[DATA] 1m Close: {close_price}")

#             # Evaluate strategy
#             signal = evaluate_trade_signal(close_price)
#             if signal in ["BUY", "SELL"]:
#                 log_event(f"[SIGNAL] {signal} at {close_price}")
#                 executor.execute_trade(signal, SYMBOL, close_price)

#     except Exception as e:
#         log_event(f"[ERROR] Failed to process message: {e}")


# def on_error(ws, error):
#     log_event(f"[WS ERROR] {error}")


# def on_close(ws, close_status_code, close_msg):
#     log_event(f"[WS CLOSED] Code: {close_status_code}, Msg: {close_msg}")


# def on_open(ws):
#     log_event("[WS CONNECTED] Listening for new candles...")


# def start_price_stream():
#     ws = WebSocketApp(
#         STREAM_URL,
#         on_message=on_message,
#         on_error=on_error,
#         on_close=on_close,
#         on_open=on_open,
#     )
#     thread = threading.Thread(target=ws.run_forever)
#     thread.daemon = True
#     thread.start()
#     log_event("[STREAM] Price watcher started.")


# if __name__ == "__main__":
#     start_price_stream()
#     while True:
#         pass  # Keeps main thread alive
import json
import threading
from collections import deque
import pandas as pd
from websocket import WebSocketApp

from utils.logger import log_event
from strategies.scalping import find_scalping_opportunity
from utils.logger import log_trade

# from execution_engine.executor import Executor
# from execution_engine.binance_connector import BinanceConnector
from paper_trading.paper_trader import PaperTradingEngine


from config import settings

SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()  # e.g., 'btcusdt'
STREAM_URL = (
    f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"
    if settings.USE_TESTNET
    else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"
)

# executor = BinanceConnector("futures")  # Choose 'spot' or 'futures' accordingly
executor = PaperTradingEngine(starting_balance=1000.0, symbol="btcusdt")
price_window = deque(maxlen=20)  # Stores last 20 closing prices


def on_message(ws, message):
    try:
        data = json.loads(message)
        candle = data["k"]  # Kline data

        if candle["x"]:  # If candle is closed
            close_price = float(candle["c"])
            log_event(f"[DATA] 1m Close: {close_price}")
            price_window.append(close_price)

            if len(price_window) >= 10:
                df = pd.DataFrame({"close": list(price_window)})
                signal = find_scalping_opportunity(df)

                if signal in ["BUY", "SELL"]:
                    # log_trade(signal, symbol, price, quantity)
                    log_event(f"[SIGNAL] {signal} at {close_price}")
                    quantity = 0.001  # Example quantity; adjust as needed
                    order_type = "MARKET"
                    side = "BUY" if signal == "BUY" else "SELL"
                    log_trade(signal, SYMBOL, close_price, quantity)
                    executor.place_order(SYMBOL, side, order_type, quantity)

                    # executor.execute_trade(signal, SYMBOL, close_price)

    except Exception as e:
        log_event(f"[ERROR] Failed to process message: {e}")


def on_error(ws, error):
    log_event(f"[WS ERROR] {error}")


def on_close(ws, close_status_code, close_msg):
    log_event(f"[WS CLOSED] Code: {close_status_code}, Msg: {close_msg}")


def on_open(ws):
    log_event("[WS CONNECTED] Listening for new candles...")


def start_price_stream():
    ws = WebSocketApp(
        STREAM_URL,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close,
        on_open=on_open,
    )
    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
    log_event("[STREAM] Price watcher started.")


if __name__ == "__main__":
    start_price_stream()
    while True:
        pass  # Keeps main thread alive
