import pandas as pd
import requests
import time

# =========================
# CONFIG
# =========================
SYMBOL = "BTCUSDT"
INTERVAL = "15m"
LIMIT = 1000
TOTAL_CANDLES = 35000

# IMPORTANT: Windows-safe path
OUTPUT_PATH = "D:/crypto ai project/data/"

BINANCE_URL = "https://api.binance.com/api/v3/klines"


# =========================
# FETCH DATA FROM BINANCE
# =========================
def fetch_klines(symbol, interval, total_candles):
    all_data = []
    end_time = None

    while len(all_data) < total_candles:
        params = {
            "symbol": symbol,
            "interval": interval,
            "limit": LIMIT
        }

        if end_time is not None:
            params["endTime"] = end_time

        response = requests.get(BINANCE_URL, params=params)
        data = response.json()

        if not data:
            break

        all_data = data + all_data
        end_time = data[0][0] - 1

        time.sleep(0.2)

    return all_data[-total_candles:]


# =========================
# CLEAN RAW DATA
# =========================
def process_data(raw_data):
    df = pd.DataFrame(raw_data, columns=[
        "open_time", "open", "high", "low", "close", "volume",
        "close_time", "qav", "num_trades",
        "taker_base_vol", "taker_quote_vol", "ignore"
    ])

    df = df[["open_time", "open", "high", "low", "close", "volume"]]

    df["open_time"] = pd.to_datetime(df["open_time"], unit="ms")
    df.set_index("open_time", inplace=True)

    df = df.astype(float)
    return df


# =========================
# MAIN EXECUTION
# =========================
if __name__ == "__main__":
    print("Fetching BTCUSDT data from Binance...")

    raw_data = fetch_klines(SYMBOL, INTERVAL, TOTAL_CANDLES)
    df_15m = process_data(raw_data)

    # Save 15-minute data
    df_15m.to_csv(OUTPUT_PATH + "BTCUSDT_15m.csv")

    # Create 4-hour candles from 15m
    df_4h = df_15m.resample("4H").agg({
        "open": "first",
        "high": "max",
        "low": "min",
        "close": "last",
        "volume": "sum"
    }).dropna()

    # Save 4-hour data
    df_4h.to_csv(OUTPUT_PATH + "BTCUSDT_4h.csv")

    print("DONE ✅")
    print("Files saved to:", OUTPUT_PATH)