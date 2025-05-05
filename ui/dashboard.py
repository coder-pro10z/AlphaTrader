import sys
import os

# Add the root path (one level up from 'backtester') to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


# import streamlit as st
# import pandas as pd
# import time
# from collections import deque

# from strategies.scalping import find_scalping_opportunity
# from paper_trading.paper_trader import PaperTradingEngine
# from config import settings

# # --- Configuration ---
# SYMBOL = settings.DEFAULT_TRADE_SYMBOL.upper()
# INITIAL_BALANCE = 1000.0
# QTY = 0.001

# # --- Initialize Engine & Data ---
# engine = PaperTradingEngine(starting_balance=INITIAL_BALANCE, symbol=SYMBOL.lower())
# price_window = deque(maxlen=50)
# trade_history = []

# # --- Streamlit Layout ---
# st.set_page_config(page_title="AlphaTrader Dashboard", layout="wide")
# st.title("⚡ AlphaTrader Live Dashboard")

# col1, col2 = st.columns(2)

# with col1:
#     st.subheader("Price Chart")
#     price_chart = st.line_chart(pd.DataFrame([], columns=["Price"]))

# with col2:
#     st.subheader("Portfolio Status")
#     balance_text = st.empty()
#     position_text = st.empty()
#     st.subheader("Last Signal")
#     signal_text = st.empty()

# st.subheader("Trade History")
# history_table = st.empty()

# # --- Streaming Loop ---
# while True:
#     # TODO: replace with real-time fetch (WebSocket or REST)
#     latest_price = price_window[-1] if price_window else settings.FALLBACK_PRICE

#     # Update price window
#     price_window.append(latest_price)
#     df = pd.DataFrame({"close": list(price_window)})

#     # Calculate SMA and signal if enough data
#     if len(price_window) >= 10:
#         signal = find_scalping_opportunity(df)
#         if signal:
#             engine.place_order(signal, price=latest_price, quantity=QTY)
#             trade_history.append(
#                 {
#                     "time": pd.Timestamp.now().strftime("%H:%M:%S"),
#                     "side": signal,
#                     "price": latest_price,
#                     "qty": QTY,
#                 }
#             )
#             signal_text.markdown(f"👉 **{signal}** @ {latest_price:.2f}")

#     # Refresh chart and status
#     price_chart.add_rows(pd.DataFrame({"Price": [latest_price]}))
#     status = engine.get_status()
#     balance_text.markdown(f"**Balance:** {status['balance']:.2f}")
#     position_text.markdown(f"**Position:** {status['position']} {SYMBOL}")

#     # Update history table
#     history_table.table(pd.DataFrame(trade_history).iloc[::-1])

#     time.sleep(1)


# 2 works
# import streamlit as st
# from data_collector.stream import price_window, start_price_stream
# from config import settings
# import time

# st.set_page_config(page_title="AlphaTrader Dashboard", layout="wide")

# # Start the price stream in the background (only once)
# if "stream_started" not in st.session_state:
#     start_price_stream()
#     st.session_state.stream_started = True

# st.title("📈 AlphaTrader Live Dashboard")

# # Auto-refresh every 5 seconds
# st_autorefresh = (
#     st.experimental_rerun if hasattr(st, "experimental_rerun") else lambda: None
# )
# st.experimental_rerun_interval = 5000  # 5000 ms = 5 sec

# # Get latest price
# latest_price = price_window[-1] if price_window else settings.FALLBACK_PRICE

# st.metric(label="💰 Latest BTC/USDT Price", value=f"${latest_price:,.2f}")

# st.write("---")

# # Future: Add strategy signals & trade log
# st.subheader("🔍 Strategy Signal (Coming Soon)")
# st.info("Live trade signals will appear here...")

# st.subheader("📜 Trade Log (Coming Soon)")
# st.warning("Trade history will be shown here once integrated.")


# # 3
# import streamlit as st
# from streamlit_autorefresh import st_autorefresh
# from data_collector.stream import price_window, latest_signal
# import pandas as pd
# from config import settings

# st.set_page_config(page_title="AlphaTrader Dashboard", layout="wide")
# st.title("📈 AlphaTrader Live Dashboard")

# # Latest Price
# # latest_price = price_window[-1] if price_window else settings.FALLBACK_PRICE
# if not price_window:
#     st.info("Waiting for first candle… (may take up to 1 minute)")
# else:
#     latest_price = price_window[-1]
#     st.metric("💰 Latest BTC/USDT Price", f"${latest_price:,.2f}")

# # st.metric("💰 Latest BTC/USDT Price", f"${latest_price:,.2f}")

# # Live Trade Signal
# st.subheader("🔍 Strategy Signal")
# st.write(f"**Current Signal:** `{latest_signal}`")

# # Price Chart
# if price_window:
#     df = pd.DataFrame({"Price": list(price_window)})
#     st.line_chart(df)

# # Trade Log - Placeholder
# st.subheader("📜 Trade Log (Coming Soon)")
# st.write("Trade history will be shown here once integrated.")

# # # Auto-refresh every 5 seconds
# # st.experimental_rerun()
# # Auto-refresh every 5 seconds using Streamlit's native feature
# # st_autorefresh = st.experimental_singleton(lambda: None)

# # Add this at the top of your dashboard.py
# # st_autorefresh(interval=5000, limit=None, key="live_dashboard_refresh")

# 4
# import streamlit as st
# from data_collector.stream import price_window, start_price_stream
# from config import settings
# import time
# from datetime import datetime
# import requests
# from streamlit_autorefresh import st_autorefresh

# # --- UI Setup ---
# st.set_page_config(page_title="AlphaTrader Dashboard", layout="wide")
# # # Add this at the top of your dashboard.py
# st_autorefresh(interval=5000000, limit=None, key="live_dashboard_refresh")

# SYMBOL = settings.DEFAULT_TRADE_SYMBOL


# # --- Helper to fetch spot price as fallback ---
# def fetch_rest_price(symbol):
#     url = f"{settings.SPOT_BASE_URL}/api/v3/ticker/price?symbol={symbol.upper()}"
#     data = requests.get(url).json()
#     return float(data["price"])


# # Start the price stream once
# if "stream_started" not in st.session_state:
#     start_price_stream()
#     st.session_state.stream_started = True

# # --- Price Logic ---
# if not price_window:
#     try:
#         rest_price = fetch_rest_price(SYMBOL)
#         price_window.append(rest_price)
#         latest_price = rest_price
#         st.info("Waiting for first candle from WebSocket... (using REST snapshot)")
#     except Exception:
#         latest_price = settings.FALLBACK_PRICE
#         st.error("Unable to fetch initial price")
# else:
#     latest_price = price_window[-1]

# st.metric(label="\U0001f4b0 Latest BTC/USDT Price", value=f"${latest_price:,.2f}")

# # Timestamp if available
# last_update = getattr(price_window, "last_update", None)
# if last_update:
#     st.caption(f"Last WebSocket update: {last_update.strftime('%H:%M:%S')} UTC")

# st.write("---")

# # --- Strategy Signal ---
# st.subheader("\U0001f50d Strategy Signal")
# st.info("Current Signal: HOLD")

# # --- Trade Log ---
# st.subheader("\U0001f4dc Trade Log (Coming Soon)")
# st.warning("Trade history will be shown here once integrated.")

# # Refresh trick
# # st.experimental_singleton(lambda: time.sleep(st_autorefresh_interval))
# # st.experimental_rerun()

# 5
import streamlit as st
from streamlit_autorefresh import st_autorefresh
from data_collector.stream import (
    price_window,
    latest_signal,
    start_price_stream,
    seed_price_window,
)
from config import settings
from datetime import datetime
import pandas as pd
import requests
import altair as alt

# import pandas as pd

# ─── Page Config & Auto‑Refresh ─────────────────────────────
st.set_page_config(page_title="AlphaTrader Dashboard", layout="wide")
# Refresh the app every 5 seconds
st_autorefresh(interval=1_500, limit=None, key="live_dashboard_refresh")

SYMBOL = settings.DEFAULT_TRADE_SYMBOL.upper()
# ─── Start WebSocket Stream ──────────────────────────────────
# if "stream_started" not in st.session_state:
#     start_price_stream()
#     st.session_state.stream_started = True

# ─── Start WebSocket Stream (once) ──────────────────────────
if "stream_started" not in st.session_state:
    start_price_stream()
    st.session_state.stream_started = True

# ─── Seed Historical Data (once) ────────────────────────────
if "seeded" not in st.session_state:
    seed_price_window(SYMBOL, limit=45)
    st.session_state.seeded = True

# ─── Header ──────────────────────────────────────────────────
st.title("📈 AlphaTrader Live Dashboard")

# ─── Fetch or Display Latest Price ──────────────────────────
if not price_window:
    # Fallback to REST snapshot
    try:
        resp = requests.get(
            f"{settings.SPOT_BASE_URL}/api/v3/ticker/price?symbol={SYMBOL}"
        )
        rest_price = float(resp.json()["price"])
    except Exception:
        rest_price = settings.FALLBACK_PRICE
    latest_price = rest_price
    st.info("Waiting for WebSocket data… (showing REST snapshot)")
else:
    latest_price = price_window[-1]

st.metric(label="💰 Latest BTC/USDT Price", value=f"${latest_price:,.2f}")

# ─── Timestamp ────────────────────────────────────────────────
last_update = getattr(price_window, "last_update", None)
if last_update:
    st.caption(f"Last WS update: {last_update.strftime('%H:%M:%S')} UTC")

st.write("---")

# ─── Strategy Signal ─────────────────────────────────────────
st.subheader("🔍 Strategy Signal")
st.info(f"Current Signal: **{latest_signal}**")

st.write("---")

# # ─── Price Chart ─────────────────────────────────────────────
# if price_window:
#     df = pd.DataFrame({"Price": list(price_window)})
#     st.line_chart(df, use_container_width=True)
# else:
#     st.write("Price chart will appear here once data arrives.")

# st.write("---")


# # ─── Price Chart ─────────────────────────────────────────────
# st.subheader("📊 Price Chart")

# if price_window:
#     # Build DataFrame and filter out any zero (or invalid) values
#     df = pd.DataFrame({"Price": list(price_window)})
#     df = df[df["Price"] > 0]

#     # Compute dynamic axis bounds (±0.5% around min/max)
#     min_price = df["Price"].min()
#     max_price = df["Price"].max()
#     y_min = min_price * 0.995
#     y_max = max_price * 1.005

#     # Create Altair line chart with labeled y-axis
#     chart = (
#         alt.Chart(df.reset_index().rename(columns={"index": "Minute"}))
#         .mark_line()
#         .encode(
#             x=alt.X("Minute:Q", title="Minutes Ago"),
#             y=alt.Y(
#                 "Price:Q", title="Price (USDT)", scale=alt.Scale(domain=(y_min, y_max))
#             ),
#             tooltip=["Minute", alt.Tooltip("Price:Q", format="$.2f")],
#         )
#         .properties(
#             height=300, width=800, title=f"BTC/USDT Price (last {len(df)} minutes)"
#         )
#     )

#     st.altair_chart(chart, use_container_width=True)
# else:
#     st.write("Price chart will appear here once data arrives.")

# ─── Chart ───────────────────────────────────────────────────
st.subheader("📊 Price Chart")

if price_window:
    df = pd.DataFrame({"Price": list(price_window)})
    df = df[df["Price"] > 0]

    min_p, max_p = df["Price"].min(), df["Price"].max()
    y_min, y_max = min_p * 0.995, max_p * 1.005

    chart = (
        alt.Chart(df.reset_index().rename(columns={"index": "Minute"}))
        .mark_line(point=True)  # point=True shows dots you can hover
        .encode(
            x=alt.X("Minute:Q", title="Minutes Ago"),
            y=alt.Y(
                "Price:Q", title="Price (USDT)", scale=alt.Scale(domain=(y_min, y_max))
            ),
            tooltip=[alt.Tooltip("Minute:Q"), alt.Tooltip("Price:Q", format="$.2f")],
        )
        .properties(height=300, title=f"BTC/USDT Price (last {len(df)}m)")
    )

    st.altair_chart(chart, use_container_width=True)
else:
    st.write("Price chart will appear here once data arrives.")
# ─── Trade Log ───────────────────────────────────────────────
st.subheader("📜 Trade Log")
st.warning("Trade history will appear here once integrated.")
