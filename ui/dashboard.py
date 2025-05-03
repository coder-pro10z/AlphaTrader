import sys
import os

# Add the root path (one level up from 'backtester') to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


import streamlit as st
import pandas as pd
import time
from collections import deque

from strategies.scalping import find_scalping_opportunity
from paper_trading.paper_trader import PaperTradingEngine
from config import settings

# --- Configuration ---
SYMBOL = settings.DEFAULT_TRADE_SYMBOL.upper()
INITIAL_BALANCE = 1000.0
QTY = 0.001

# --- Initialize Engine & Data ---
engine = PaperTradingEngine(starting_balance=INITIAL_BALANCE, symbol=SYMBOL.lower())
price_window = deque(maxlen=50)
trade_history = []

# --- Streamlit Layout ---
st.set_page_config(page_title="AlphaTrader Dashboard", layout="wide")
st.title("⚡ AlphaTrader Live Dashboard")

col1, col2 = st.columns(2)

with col1:
    st.subheader("Price Chart")
    price_chart = st.line_chart(pd.DataFrame([], columns=["Price"]))

with col2:
    st.subheader("Portfolio Status")
    balance_text = st.empty()
    position_text = st.empty()
    st.subheader("Last Signal")
    signal_text = st.empty()

st.subheader("Trade History")
history_table = st.empty()

# --- Streaming Loop ---
while True:
    # TODO: replace with real-time fetch (WebSocket or REST)
    latest_price = price_window[-1] if price_window else settings.FALLBACK_PRICE

    # Update price window
    price_window.append(latest_price)
    df = pd.DataFrame({"close": list(price_window)})

    # Calculate SMA and signal if enough data
    if len(price_window) >= 10:
        signal = find_scalping_opportunity(df)
        if signal:
            engine.place_order(signal, price=latest_price, quantity=QTY)
            trade_history.append(
                {
                    "time": pd.Timestamp.now().strftime("%H:%M:%S"),
                    "side": signal,
                    "price": latest_price,
                    "qty": QTY,
                }
            )
            signal_text.markdown(f"👉 **{signal}** @ {latest_price:.2f}")

    # Refresh chart and status
    price_chart.add_rows(pd.DataFrame({"Price": [latest_price]}))
    status = engine.get_status()
    balance_text.markdown(f"**Balance:** {status['balance']:.2f}")
    position_text.markdown(f"**Position:** {status['position']} {SYMBOL}")

    # Update history table
    history_table.table(pd.DataFrame(trade_history).iloc[::-1])

    time.sleep(1)
