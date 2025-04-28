# Scalping Strategy Logic
import pandas as pd

def find_scalping_opportunity(df: pd.DataFrame):
    """
    df: expects a DataFrame with columns ['timestamp', 'open', 'high', 'low', 'close', 'volume']
    """
    # Calculate 5-period Simple Moving Average (SMA)
    df['sma_5'] = df['close'].rolling(window=5).mean()

    # Get the latest candle
    latest_close = df['close'].iloc[-1]
    latest_sma_5 = df['sma_5'].iloc[-1]

    # Basic signal logic
    if latest_close > latest_sma_5:
        return "BUY"
    elif latest_close < latest_sma_5:
        return "SELL"
    else:
        return "HOLD"
