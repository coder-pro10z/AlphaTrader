# data_collector/stream.py

import json
import threading
from collections import deque
from websocket import WebSocketApp

# from config import settings

# SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()
# STREAM_URL = (
#     f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"
#     if settings.USE_TESTNET
#     else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"
# )
from config import settings

SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()  # e.g., 'btcusdt'

if settings.EXCHANGE_TYPE == "futures":
    STREAM_URL = (
        f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"  # ✅ Futures Testnet
        if settings.USE_TESTNET
        else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"  # ✅ Futures Mainnet
    )
else:  # spot
    STREAM_URL = (
        f"wss://testnet.binance.vision/ws/{SYMBOL}@kline_1m"
        if settings.USE_TESTNET
        else f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_1m"
    )


# Shared price window
price_window = deque(maxlen=50)


def _on_message(ws, message):
    data = json.loads(message)
    candle = data["k"]
    if candle["x"]:
        price_window.append(float(candle["c"]))


def start_stream():
    ws = WebSocketApp(
        STREAM_URL,
        on_message=_on_message,
        on_error=lambda ws, e: None,
        on_close=lambda ws, c, m: None,
        on_open=lambda ws: None,
    )
    t = threading.Thread(target=ws.run_forever, daemon=True)
    t.start()


# data_collector/stream.py

import json
import threading
from collections import deque
from websocket import WebSocketApp
from config import settings

SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()
STREAM_URL = (
    f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"
    if settings.USE_TESTNET
    else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"
)

# Shared price window accessible from other modules
price_window = deque(maxlen=50)


def _on_message(ws, message):
    try:
        data = json.loads(message)
        candle = data["k"]
        if candle["x"]:  # Candle closed
            close_price = float(candle["c"])
            price_window.append(close_price)
    except Exception:
        pass  # You can add logging if needed


def start_price_stream():
    ws = WebSocketApp(
        STREAM_URL,
        on_message=_on_message,
        on_error=lambda ws, err: print(f"[WS ERROR] {err}"),
        on_close=lambda ws, code, msg: print(f"[WS CLOSED] {code}, {msg}"),
        on_open=lambda ws: print("[WS OPENED] Stream started."),
    )
    thread = threading.Thread(target=ws.run_forever)
    thread.daemon = True
    thread.start()
