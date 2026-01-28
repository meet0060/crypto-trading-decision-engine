# crypto-trading-decision-engine
# Data – Market Data Handling

This folder is responsible for **data collection and storage** for the project.

All strategy logic and backtesting depend on the data prepared here, so the goal of this folder is to keep things **clean, consistent, and reproducible**.

---

## What’s inside this folder

### CSV files (market data)

These files contain historical OHLCV data fetched from Binance:

- `BTCUSDT_4h.csv` – Bitcoin 4-hour candles  
- `BTCUSDT_15m.csv` – Bitcoin 15-minute candles  
- `ETHUSDT_4h.csv` – Ethereum 4-hour candles  
- `ETHUSDT_15m.csv` – Ethereum 15-minute candles  

Each CSV uses the same structure so they can be easily swapped into the backtest engine.

**Columns include:**
- open_time (timestamp)
- open
- high
- low
- close
- volume

---

### Python scripts (data fetching)

#### `fetch_data.py`
Fetches historical **BTCUSDT** data from Binance.

- Supports pagination to collect large historical ranges
- Saves data in CSV format
- Designed to be run **once**, not repeatedly

#### `fetch_data_eth.py`
Fetches historical **ETHUSDT** data from Binance.

- Same logic as `fetch_data.py`
- Separated for clarity and simplicity
- Produces ETH-specific CSV files

---

## How this data is used

- CSV files are read directly by the backtest engine
- No preprocessing is done inside strategy code
- Keeping data separate ensures:
  - no look-ahead bias
  - reproducible backtests
  - easier debugging

---

## Important notes

- Data should not be modified manually
- Strategy logic assumes consistent column names
- Backtest results will only change if:
  - strategy rules change
  - data range significantly changes

---

## Design philosophy

This folder follows a simple rule:

> **Data first, logic later.**

By isolating data collection here, the rest of the project stays focused on analysis and decision-making rather than infrastructure.
