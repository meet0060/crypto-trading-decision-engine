# crypto-trading-decision-engine
# Features – Trading Logic Breakdown

This folder contains the **core logic** of the trading system.  
Each file represents **one decision layer**, written separately so the logic stays clear, testable, and debuggable.

The idea was simple:  
👉 *Don’t build a black box. Build understandable blocks.*

---

## Why this folder exists

Instead of writing one huge script, the logic was broken down into steps that mirror how a discretionary trader thinks:

1. First understand the **market context**
2. Then check **structure**
3. Then wait for **confirmation**
4. Only then make a decision

Each file here focuses on **one question only**.

---

## File overview

### `trend_state.py`
**Question it answers:**  
> “Is the market even in a condition where long trades make sense?”

- Uses higher timeframe (4H)
- Determines bullish vs no-trade state
- Prevents trading against the broader trend

This acts as a **permission filter**.

---

### `structure_logic.py`
**Question it answers:**  
> “Has the market shown real intent (break of structure)?”

- Identifies swing highs
- Detects bullish break of structure (BOS)
- Avoids reacting to random price moves

This is where **market intent** is defined.

---

### `retest_logic.py`
**Question it answers:**  
> “Did price accept the new structure, or was it a fake move?”

- Checks if price retests the broken level
- Invalidates setups that fail to hold
- Filters out weak breakouts

This step removes many bad trades before they happen.

---

### `entry_logic.py`
**Question it answers:**  
> “When should I actually enter?”

- Lower timeframe logic (15m)
- Uses price-action confirmation (engulfing / momentum)
- Focuses on timing, not prediction

This improves execution without changing the core idea.

---

### `backtest_engine.py`
**Purpose:**  
> “Does this logic survive contact with real data?”

- Combines all layers into one pipeline
- Runs an honest, no-lookahead backtest
- Measures outcomes in R-multiples, not money
- Tested across BTC and ETH

This file turns **ideas into evidence**.

---

## Design philosophy

- No guaranteed profits
- No curve fitting
- No future candle access
- Focus on clarity over complexity

Every rule exists because it answers a **specific trading question**, not because it looks fancy.

---

## Current status

- Logic validated on BTC & ETH
- Conservative, low-frequency system
- Further work focuses on:
  - deeper analysis
  - risk refinement
  - execution improvement

---

## Final note

This folder represents **thinking in systems**, not just trading code.  
The goal was to understand *why* trades happen — not just whether they win.
