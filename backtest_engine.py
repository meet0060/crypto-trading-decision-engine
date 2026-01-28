import pandas as pd

# =========================
# LOAD DATA
# =========================
path_4h = "D:/crypto ai project/data/BTCUSDT_4h.csv"
path_15m = "D:/crypto ai project/data/BTCUSDT_15m.csv"

df_4h = pd.read_csv(path_4h, index_col="open_time", parse_dates=True)
df_15m = pd.read_csv(path_15m, index_col="open_time", parse_dates=True)

# =========================
# PARAMETERS
# =========================
RR = 2
PULLBACK_PCT = 0.01
RETEST_TOLERANCE = 0.003
MINOR_HIGH_LOOKBACK = 5   # candles

# =========================
# 1️⃣ TREND (4H)
# =========================
df_4h["EMA50"] = df_4h["close"].ewm(span=50).mean()
df_4h["EMA200"] = df_4h["close"].ewm(span=200).mean()

df_4h["trend_state"] = "no_trade"
df_4h.loc[
    (df_4h["close"] > df_4h["EMA50"]) &
    (df_4h["EMA50"] > df_4h["EMA200"]),
    "trend_state"
] = "bullish"

# =========================
# 2️⃣ STRUCTURE + RETEST (4H)
# =========================
df_4h["bullish_retest"] = False
df_4h["retest_low"] = None

potential_high = df_4h.iloc[0]["high"]
last_high = None
waiting_for_retest = False
broken_level = None

for i in range(1, len(df_4h)):
    high = df_4h.iloc[i]["high"]
    low = df_4h.iloc[i]["low"]
    close = df_4h.iloc[i]["close"]

    if df_4h.iloc[i]["trend_state"] != "bullish":
        continue

    if high > potential_high:
        potential_high = high

    if (potential_high - low) / potential_high >= PULLBACK_PCT:
        last_high = potential_high
        potential_high = high

    if last_high and close > last_high and not waiting_for_retest:
        broken_level = last_high
        waiting_for_retest = True

    if waiting_for_retest and broken_level:
        near = abs(low - broken_level) / broken_level <= RETEST_TOLERANCE
        invalid = close < broken_level

        if invalid:
            waiting_for_retest = False
            broken_level = None

        elif near:
            df_4h.iloc[i, df_4h.columns.get_loc("bullish_retest")] = True
            df_4h.iloc[i, df_4h.columns.get_loc("retest_low")] = low
            waiting_for_retest = False
            broken_level = None

# =========================
# 3️⃣ ENTRY LOGIC (15M)
# =========================
df_15m["bullish_engulfing"] = False
df_15m["break_minor_high"] = False

# Bullish engulfing
for i in range(1, len(df_15m)):
    prev = df_15m.iloc[i - 1]
    curr = df_15m.iloc[i]

    if prev["close"] < prev["open"] and curr["close"] > curr["open"]:
        if curr["open"] <= prev["close"] and curr["close"] >= prev["open"]:
            df_15m.iloc[i, df_15m.columns.get_loc("bullish_engulfing")] = True

# Break of minor high
for i in range(MINOR_HIGH_LOOKBACK, len(df_15m)):
    recent_high = df_15m.iloc[i - MINOR_HIGH_LOOKBACK:i]["high"].max()
    if df_15m.iloc[i]["close"] > recent_high:
        df_15m.iloc[i, df_15m.columns.get_loc("break_minor_high")] = True

# =========================
# 4️⃣ BACKTEST
# =========================
trades = []

for i in range(len(df_4h)):
    row = df_4h.iloc[i]

    if not row["bullish_retest"]:
        continue

    retest_time = df_4h.index[i]
    stop_price = row["retest_low"]

    df_15m_after = df_15m[df_15m.index > retest_time]

    for j in range(len(df_15m_after)):
        candle = df_15m_after.iloc[j]

        entry_signal = (
            candle["bullish_engulfing"] or
            candle["break_minor_high"]
        )

        if not entry_signal:
            continue

        entry = candle["close"]
        risk = entry - stop_price

        if risk <= 0:
            break

        target = entry + RR * risk

        for k in range(j + 1, len(df_15m_after)):
            high = df_15m_after.iloc[k]["high"]
            low = df_15m_after.iloc[k]["low"]

            if low <= stop_price:
                trades.append(-1)
                break

            if high >= target:
                trades.append(RR)
                break

        break

# =========================
# 5️⃣ RESULTS
# =========================
total = len(trades)
wins = trades.count(RR)
losses = trades.count(-1)
winrate = (wins / total * 100) if total > 0 else 0
net_r = sum(trades)

print("\n========== BACKTEST v3 RESULTS ==========")
print(f"Total trades : {total}")
print(f"Wins         : {wins}")
print(f"Losses       : {losses}")
print(f"Win rate     : {winrate:.2f}%")
print(f"Net R        : {net_r}")
print("========================================")