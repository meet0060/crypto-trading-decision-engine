import pandas as pd

# Load 4H data
path = "D:/crypto ai project/data/BTCUSDT_4h.csv"
df = pd.read_csv(path, index_col="open_time", parse_dates=True)

# Calculate EMAs
df["EMA50"] = df["close"].ewm(span=50).mean()
df["EMA200"] = df["close"].ewm(span=200).mean()


def get_trend_state(row):
    """
    Determines market regime using EMA structure.
    """
    if row["close"] > row["EMA50"] > row["EMA200"]:
        return "bullish"

    elif row["close"] < row["EMA50"] < row["EMA200"]:
        return "bearish"

    else:
        return "no_trade"


# Apply logic to every candle
df["trend_state"] = df.apply(get_trend_state, axis=1)

# Inspect last few candles
print(df[["close", "EMA50", "EMA200", "trend_state"]].tail(12))