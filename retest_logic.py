import pandas as pd

# -------------------------
# LOAD DATA
# -------------------------
path = "D:/crypto ai project/data/BTCUSDT_4h.csv"
df = pd.read_csv(path, index_col="open_time", parse_dates=True)

# -------------------------
# PARAMETERS
# -------------------------
RETEST_TOLERANCE_PCT = 0.003  # 0.3% proximity to level

# -------------------------
# PREP: TREND + STRUCTURE
# -------------------------
# EMA trend
df["EMA50"] = df["close"].ewm(span=50).mean()
df["EMA200"] = df["close"].ewm(span=200).mean()

df["trend_state"] = "no_trade"
df.loc[(df["close"] > df["EMA50"]) & (df["EMA50"] > df["EMA200"]), "trend_state"] = "bullish"

# Structure flags (assumes structure_logic already ran conceptually)
df["swing_high"] = False
df["bullish_bos"] = False

last_high = df.iloc[0]["high"]
potential_high = last_high
PULLBACK_PCT = 0.01

# Detect swings + BOS (live-safe, simplified reuse)
for i in range(1, len(df)):
    high = df.iloc[i]["high"]
    low = df.iloc[i]["low"]

    if high > potential_high:
        potential_high = high

    if (potential_high - low) / potential_high >= PULLBACK_PCT:
        df.iloc[i, df.columns.get_loc("swing_high")] = True
        last_high = potential_high
        potential_high = high

    if df.iloc[i]["close"] > last_high:
        df.iloc[i, df.columns.get_loc("bullish_bos")] = True


# -------------------------
# RETEST LOGIC
# -------------------------
df["bullish_retest"] = False

broken_level = None
waiting_for_retest = False

for i in range(len(df)):
    # Only care in bullish trend
    if df.iloc[i]["trend_state"] != "bullish":
        continue

    # When BOS happens, store level
    if df.iloc[i]["bullish_bos"]:
        broken_level = df.iloc[i]["close"]
        waiting_for_retest = True
        continue

    # Look for retest after BOS
    if waiting_for_retest and broken_level is not None:
        low = df.iloc[i]["low"]
        close = df.iloc[i]["close"]

        # Check proximity to broken level
        near_level = abs(low - broken_level) / broken_level <= RETEST_TOLERANCE_PCT

        # Invalidation condition
        if close < broken_level:
            waiting_for_retest = False
            broken_level = None
            continue

        # Valid retest
        if near_level:
            df.iloc[i, df.columns.get_loc("bullish_retest")] = True
            waiting_for_retest = False
            broken_level = None


# -------------------------
# OUTPUT CHECK
# -------------------------
print(
    df[
        ["close", "trend_state", "bullish_bos", "bullish_retest"]
    ].tail(30)
)