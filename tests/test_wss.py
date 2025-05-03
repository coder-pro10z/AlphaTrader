from websocket import WebSocketApp


def on_message(ws, message):
    print("[DATA]", message)


def on_open(ws):
    print("[CONNECTED]")


def on_error(ws, error):
    print("[ERROR]", error)


def on_close(ws, close_status_code, close_msg):
    print("[CLOSED]", close_status_code, close_msg)


url = "wss://stream.binancefuture.com/ws/btcusdt@kline_1m"
ws = WebSocketApp(
    url, on_message=on_message, on_open=on_open, on_error=on_error, on_close=on_close
)
ws.run_forever()
