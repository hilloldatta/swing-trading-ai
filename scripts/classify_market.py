# === scripts/classify_market.py ===
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import yfinance as yf
import pandas as pd
import json
from utils.market_stage import detect_market_stage

# Download 3 years of Nifty 50 weekly data
symbol = "^NSEI"  # Yahoo Finance ticker for Nifty 50 index
print(f"📊 Fetching historical weekly data for {symbol}...")

df = yf.download(symbol, period="3y", interval="1wk", auto_adjust=True, progress=False)

# Handle multi-level columns from yfinance
if isinstance(df.columns, pd.MultiIndex):
    # Flatten multi-level columns by taking the first level (the actual column names)
    df.columns = [col[0] if isinstance(col, tuple) else col for col in df.columns]

# Reset index to get Date as a column and clean data
df = df.dropna().reset_index()

# Ensure we have the expected columns
expected_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
if not all(col in df.columns for col in expected_cols):
    print(f"⚠️ Missing expected columns. Available: {df.columns.tolist()}")
    print(f"📋 Sample data:\n{df.head(3)}")
    exit(1)

# Select and clean the data
df = df[expected_cols]

print(f"✅ Data processed: {len(df)} weeks of data")
print(f"📋 Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"📋 Latest close: {df['Close'].iloc[-1]:.2f}")

# Detect market stage
stage = detect_market_stage(df)
print(f"\n🧠 Market Stage: {stage}")

# Save result to config
os.makedirs("config", exist_ok=True)
out_path = "config/market_status.json"
with open(out_path, "w") as f:
    json.dump({"market_stage": stage}, f, indent=2)

print(f"📁 Saved to {out_path}")
