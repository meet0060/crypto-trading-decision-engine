import pandas as pd 
import matplotlib.pyplot as plt 

path = "D:/crypto ai project/data/BTCUSDT_4h.csv"
df = pd.read_csv(path,index_col="open_time",parse_dates=True)

df["EMA50"] = df["close"].ewm(span=50).mean()
df["EMA200"] = df["close"].ewm(span=200).mean()


plt.figure(figsize=(12,6))
plt.plot(df.index ,df["close"],label="Price")
plt.plot(df.index ,df["EMA50"],label="EMA50")
plt.plot(df.index,df["EMA200"],label="EMA200")

plt.legend()
plt.title("BTCUSDT 4H Trend")
plt.show()
