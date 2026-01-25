import pandas as pd

path_15m = "D:/crypto ai project/data/BTCUSDT_4h.csv"
df = pd.read_csv(path_15m , index_col = "open_time", parse_dates = True)

df["bullish_engulfing"] = False 

for i in range(1 , len(df)):
    prev = df.iloc[i - 1] 
    curr = df.iloc[i] 

    prev_bearish = prev["close"] < prev["open"]

    curr_bullish = curr["close"] > curr["open"]

    body_engulf = (curr["open"] <= prev["close"] and curr["close"] >= prev["open"])

    if prev_bearish and curr_bullish and body_engulf:
        df.iloc[i , df.columns.get_loc("bullish_engulfing")] = True 

print(df[["open","close","bullish_engulfing"]].tail(30))
