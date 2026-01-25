import pandas as pd

path = "D:/crypto ai project/data/BTCUSDT_4h.csv"
df = pd.read_csv(path,index_col="open_time",parse_dates=True)
print(df.columns)

PULLBACK_PCT = 0.01 
df["swing_high"] = False
df["swing_low"] = False
 
last_high = df.iloc[0]["high"]
last_low = df.iloc[0]["low"] 

potential_high = last_high 
potential_low = last_low 

for i in range(1,len(df)):
    high = df.iloc[i]["high"]
    low = df.iloc[i]["low"]

    if high > potential_high:
        potential_high = high 

    if (potential_high - low) / potential_high >= PULLBACK_PCT:
        df.iloc[i,df.columns.get_loc("swing_high")] = True 
        last_high = potential_high 
        potential_high = high 

    if low < potential_low :
        potential_low = low 

    if (high - potential_low) / potential_low >= PULLBACK_PCT:
        df.iloc[i,df.columns.get_loc("swing_low")] = True 
        last_low = potential_low 
        potential_low = low 


df["bullish_bos"] = False
df["bearish_bos"] = False

last_confirmed_high = None 
last_confirmed_low = None 

for i in range(len(df)): 
    if df.iloc[i]["swing_high"]: 
        last_confirmed_high = df.iloc[i]["high"]

    if df.iloc[i]["swing_low"]:
        last_confirmed_low = df.iloc[i]["low"]

    if last_confirmed_high is not None :
        if df.iloc[i]["close"] < last_confirmed_low:
            df.iloc[i,df.columns.get_loc("bearish_bos")] =True 

print(df[["high","low","close","swing_high","swing_low","bullish_bos"]].tail(20))