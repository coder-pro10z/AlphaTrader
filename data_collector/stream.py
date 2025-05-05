# # data_collector/stream.py

# import json
# import threading
# from collections import deque
# from websocket import WebSocketApp

# # from config import settings

# # SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()
# # STREAM_URL = (
# #     f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"
# #     if settings.USE_TESTNET
# #     else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"
# # )
# from config import settings

# SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()  # e.g., 'btcusdt'

# if settings.EXCHANGE_TYPE == "futures":
#     STREAM_URL = (
#         f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"  # ✅ Futures Testnet
#         if settings.USE_TESTNET
#         else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"  # ✅ Futures Mainnet
#     )
# else:  # spot
#     STREAM_URL = (
#         f"wss://testnet.binance.vision/ws/{SYMBOL}@kline_1m"
#         if settings.USE_TESTNET
#         else f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_1m"
#     )


# # Shared price window
# price_window = deque(maxlen=50)
# # price_window = deque(maxlen=20)
# latest_signal = "HOLD"  # default value


# def _on_message(ws, message):
#     data = json.loads(message)
#     candle = data["k"]
#     if candle["x"]:
#         price_window.append(float(candle["c"]))


# def start_stream():
#     ws = WebSocketApp(
#         STREAM_URL,
#         on_message=_on_message,
#         on_error=lambda ws, e: None,
#         on_close=lambda ws, c, m: None,
#         on_open=lambda ws: None,
#     )
#     t = threading.Thread(target=ws.run_forever, daemon=True)
#     t.start()


# # data_collector/stream.py

# import json
# import threading
# from collections import deque
# from websocket import WebSocketApp
# from config import settings

# SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()
# STREAM_URL = (
#     f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"
#     if settings.USE_TESTNET
#     else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"
# )

# # Shared price window accessible from other modules
# price_window = deque(maxlen=50)
# latest_signal = "HOLD"  # default value


# def _on_message(ws, message):
#     try:
#         data = json.loads(message)
#         candle = data["k"]
#         if candle["x"]:  # Candle closed
#             close_price = float(candle["c"])
#             price_window.append(close_price)
#     except Exception:
#         pass  # You can add logging if needed


# def start_price_stream():
#     ws = WebSocketApp(
#         STREAM_URL,
#         on_message=_on_message,
#         on_error=lambda ws, err: print(f"[WS ERROR] {err}"),
#         on_close=lambda ws, code, msg: print(f"[WS CLOSED] {code}, {msg}"),
#         on_open=lambda ws: print("[WS OPENED] Stream started."),
#     )
#     thread = threading.Thread(target=ws.run_forever)
#     thread.daemon = True
#     thread.start()

# data_collector/stream.py

import json
import threading
import requests
from collections import deque
from websocket import WebSocketApp
from config import settings

# ---- Configuration ----
SYMBOL = settings.DEFAULT_TRADE_SYMBOL.lower()

if settings.EXCHANGE_TYPE == "futures":
    STREAM_URL = (
        f"wss://stream.binancefuture.com/ws/{SYMBOL}@kline_1m"
        if settings.USE_TESTNET
        else f"wss://fstream.binance.com/ws/{SYMBOL}@kline_1m"
    )
else:  # Spot
    STREAM_URL = (
        f"wss://testnet.binance.vision/ws/{SYMBOL}@kline_1m"
        if settings.USE_TESTNET
        else f"wss://stream.binance.com:9443/ws/{SYMBOL}@kline_1m"
    )

# ---- Shared State ----
# price_window = deque(maxlen=50)
# to—for 30 minutes:
price_window = deque(maxlen=45)
latest_signal = "HOLD"
last_update = None


# ---- WebSocket Handlers ----
def _on_message(ws, message):
    global last_update
    try:
        data = json.loads(message)
        candle = data.get("k")
        if candle and candle.get("x"):  # Only closed candles
            close_price = float(candle["c"])
            price_window.append(close_price)
            last_update = candle.get("T")  # Event time
    except Exception as e:
        print(f"[WS MESSAGE ERROR] {e}")


def start_price_stream():
    ws = WebSocketApp(
        STREAM_URL,
        on_message=_on_message,
        on_error=lambda ws, err: print(f"[WS ERROR] {err}"),
        on_close=lambda ws, code, msg: print(f"[WS CLOSED] {code} | {msg}"),
        on_open=lambda ws: print("[WS OPENED] Stream started."),
    )
    thread = threading.Thread(target=ws.run_forever, daemon=True)
    thread.start()


# ---- REST Seeding (1m Klines) ----
# def seed_price_window(symbol: str, limit: int = 20):
# def seed_price_window(symbol: str, limit: int = 45):
#     """
#     Fetch recent 1m closes via REST and fill the price_window.
#     limit=number of minutes to seed
#     """
#     try:
#         base_url = (
#             settings.FUTURES_BASE_URL
#             if settings.EXCHANGE_TYPE == "futures"
#             else settings.SPOT_BASE_URL
#         )
#         url = f"{base_url}/api/v3/klines?symbol={symbol.upper()}&interval=1m&limit={limit}"
#         response = requests.get(url)
#         response.raise_for_status()
#         klines = response.json()
#         closes = [float(k[4]) for k in klines]  # 4th index is 'close' price
#         price_window.clear()
#         price_window.extend(closes)
#         print(f"[SEED] Preloaded {len(closes)} candles into price_window.")
#     except Exception as e:
#         print(f"[SEED ERROR] Failed to preload candles: {e}")


def seed_price_window(symbol: str, limit: int = 45):
    """
    Fetch recent 1m closes via REST and fill the price_window.
    Supports both Spot and Futures.
    """
    try:
        if settings.EXCHANGE_TYPE == "futures":
            base = settings.FUTURES_BASE_URL  # e.g. https://testnet.binancefuture.com
            path = "/fapi/v1/klines"
        else:
            base = settings.SPOT_BASE_URL  # e.g. https://testnet.binance.vision
            path = "/api/v3/klines"

        url = f"{base}{path}" f"?symbol={symbol.upper()}&interval=1m&limit={limit}"

        response = requests.get(url)
        response.raise_for_status()
        klines = response.json()

        closes = [float(k[4]) for k in klines]
        price_window.clear()
        price_window.extend(closes)
        print(f"[SEED] Preloaded {len(closes)} candles into price_window.")

    except Exception as e:
        print(f"[SEED ERROR] Failed to preload candles: {e}")
