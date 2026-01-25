# Crypto Trading Decision Engine (Python)

This project is a **rule-based crypto trading decision engine** built for learning and experimentation.

## What this project does
- Uses **4H timeframe** for trend and market structure
- Detects **Break of Structure (BOS)** and **valid retests**
- Uses **15m timeframe** for entry timing
- Confirms momentum using **bullish engulfing candles**
- Avoids **look-ahead bias**
- Outputs a final decision: `SETUP VALID` or `NO TRADE`

## What this project is NOT
- Not a fully automated trading bot
- Not guaranteed to be profitable
- No live trading or real money execution

## Core Logic Flow
1. Identify bullish trend using EMA50 & EMA200 (4H)
2. Detect swing highs and bullish BOS
3. Validate structure with a retest
4. Confirm entry using 15m bullish engulfing
5. Combine all conditions into a final decision

## Current Status
- Logic implemented and working
- No backtesting yet
- Risk management not added

## Next Steps
- Backtesting the strategy
- Adding risk management
- Paper trading

This project focuses on **clean logic, structure, and disciplined decision-making**.
