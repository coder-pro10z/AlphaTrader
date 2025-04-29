# # Scalping Strategy Logic

# import pandas as pd

# def find_scalping_opportunity(df: pd.DataFrame):
#     """
#     df: expects a DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
#     """
#     # Calculate 5-period Simple Moving Average (SMA)
#     df['sma_5'] = df['close'].rolling(window=5).mean()

#     # Get the latest candle
#     latest_close = df['close'].iloc[-1]
#     latest_sma_5 = df['sma_5'].iloc[-1]

#     # Basic signal logic
#     if latest_close > latest_sma_5:
#         return "BUY"
#     elif latest_close < latest_sma_5:
#         return "SELL"
#     else:
#         return "HOLD"

# strategies/scalping.py

# import pandas as pd

# def find_scalping_opportunity(df: pd.DataFrame) -> str | None:
#     """
#     Determine if there's a scalping opportunity using SMA crossover.

#     Args:
#         df (pd.DataFrame): Historical price data with a 'close' column.

#     Returns:
#         str | None: 'BUY', 'SELL', or None
#     """
#     if 'close' not in df.columns or len(df) < 10:
#         print("⛔ Not enough data or missing 'close' column.")
#         return None

#     # Calculate short and long moving averages
#     df['sma_5'] = df['close'].rolling(window=5).mean()
#     df['sma_10'] = df['close'].rolling(window=10).mean()

#         # print the last 2 values manually for debugging:
#     print("Prev SMA5:", df['sma_5'].iloc[-2], "Prev SMA10:", df['sma_10'].iloc[-2])
#     print("Curr SMA5:", df['sma_5'].iloc[-1], "Curr SMA10:", df['sma_10'].iloc[-1])


#     # print(market_data[['close', 'sma_5', 'sma_10']].tail())

#     # Get the last 2 values to check for crossover
#     if df['sma_5'].iloc[-2] < df['sma_10'].iloc[-2] and df['sma_5'].iloc[-1] > df['sma_10'].iloc[-1]:
#         return "BUY"
#     elif df['sma_5'].iloc[-2] > df['sma_10'].iloc[-2] and df['sma_5'].iloc[-1] < df['sma_10'].iloc[-1]:
#         return "SELL"
    
#     return None

import pandas as pd

def find_scalping_opportunity(df: pd.DataFrame) -> str | None:
    if 'close' not in df.columns or len(df) < 10:
        print("⛔ Not enough data or missing 'close' column.")
        return None

    df['sma_5'] = df['close'].rolling(window=5).mean()
    df['sma_10'] = df['close'].rolling(window=10).mean()

    prev_sma5 = df['sma_5'].iloc[-2]
    prev_sma10 = df['sma_10'].iloc[-2]
    curr_sma5 = df['sma_5'].iloc[-1]
    curr_sma10 = df['sma_10'].iloc[-1]

    print("Prev SMA5:", prev_sma5, "Prev SMA10:", prev_sma10)
    print("Curr SMA5:", curr_sma5, "Curr SMA10:", curr_sma10)

    # ✅ Skip comparison if either is NaN
    if pd.notna(prev_sma10) and pd.notna(curr_sma10):
        if prev_sma5 < prev_sma10 and curr_sma5 > curr_sma10:
            return "BUY"
        elif prev_sma5 > prev_sma10 and curr_sma5 <= curr_sma10:
            return "SELL"

    return None
