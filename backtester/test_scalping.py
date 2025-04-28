import pandas as pd
from strategies.scalping import find_scalping_opportunity

def test_find_scalping_opportunity():
    # Mock DataFrame with closing prices slightly above and below SMA
    data = {
        "timestamp": range(5),
        "open": [100, 102, 104, 106, 108],
        "high": [101, 103, 105, 107, 109],
        "low": [99, 101, 103, 105, 107],
        "close": [100, 102, 104, 106, 110],  # Last close = 110
        "volume": [10, 10, 10, 10, 10]
    }
    df = pd.DataFrame(data)

    signal = find_scalping_opportunity(df)

    print(f"Test Signal: {signal}")
    assert signal == "BUY", "Expected signal to be BUY but got {signal}"

if __name__ == "__main__":
    test_find_scalping_opportunity()
    print("✅ test_find_scalping_opportunity passed!")
