import pandas as pd

# =========================
# LOAD DATA
# =========================
path_4h = "D:/crypto ai project/data/BTCUSDT_4h.csv"
path_15m = "D:/crypto ai project/data/BTCUSDT_15m.csv"

df_4h = pd.read_csv(path_4h, index_col="open_time", parse_dates=True)
df_15m = pd.read_csv(path_15m, index_col="open_time", parse_dates=True)

# =========================
# 1️⃣ TREND STATE (4H)
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
# 2️⃣ STRUCTURE + BOS + RETEST (4H)
# =========================
PULLBACK_PCT = 0.01
RETEST_TOLERANCE = 0.003

df_4h["swing_high"] = False
df_4h["bullish_bos"] = False
df_4h["bullish_retest"] = False

potential_high = df_4h.iloc[0]["high"]
last_confirmed_high = None
waiting_for_retest = False
broken_level = None

for i in range(1, len(df_4h)):
    high = df_4h.iloc[i]["high"]
    low = df_4h.iloc[i]["low"]
    close = df_4h.iloc[i]["close"]

    # Only operate in bullish trend
    if df_4h.iloc[i]["trend_state"] != "bullish":
        continue

    # Track potential swing high
    if high > potential_high:
        potential_high = high

    # Confirm swing high after pullback
    if (potential_high - low) / potential_high >= PULLBACK_PCT:
        df_4h.iloc[i, df_4h.columns.get_loc("swing_high")] = True
        last_confirmed_high = potential_high
        potential_high = high

    # Break of Structure (once)
    if (
        last_confirmed_high is not None
        and close > last_confirmed_high
        and not waiting_for_retest
    ):
        df_4h.iloc[i, df_4h.columns.get_loc("bullish_bos")] = True
        broken_level = last_confirmed_high
        waiting_for_retest = True

    # Retest logic
    if waiting_for_retest and broken_level is not None:
        near = abs(low - broken_level) / broken_level <= RETEST_TOLERANCE
        invalid = close < broken_level

        if invalid:
            waiting_for_retest = False
            broken_level = None

        elif near:
            df_4h.iloc[i, df_4h.columns.get_loc("bullish_retest")] = True
            waiting_for_retest = False
            broken_level = None

# =========================
# 3️⃣ ENTRY CONFIRMATION (15M)
# =========================
df_15m["bullish_engulfing"] = False

for i in range(1, len(df_15m)):
    prev = df_15m.iloc[i - 1]
    curr = df_15m.iloc[i]

    prev_bearish = prev["close"] < prev["open"]
    curr_bullish = curr["close"] > curr["open"]

    engulf = (
        curr["open"] <= prev["close"] and
        curr["close"] >= prev["open"]
    )

    if prev_bearish and curr_bullish and engulf:
        df_15m.iloc[i, df_15m.columns.get_loc("bullish_engulfing")] = True

# =========================
# 4️⃣ FINAL DECISION
# =========================
latest_4h = df_4h.iloc[-1]
recent_15m = df_15m.tail(10)

setup_valid = (
    latest_4h["trend_state"] == "bullish" and
    latest_4h["bullish_retest"] and
    recent_15m["bullish_engulfing"].any()
)

print("\n========== FINAL DECISION ==========")
print(f"Trend bullish     : {latest_4h['trend_state'] == 'bullish'}")
print(f"4H Retest valid   : {latest_4h['bullish_retest']}")
print(f"15m Engulfing     : {recent_15m['bullish_engulfing'].any()}")
print("-----------------------------------")
print("SETUP VALID → MANUAL REVIEW" if setup_valid else "NO TRADE")