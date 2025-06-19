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

df = yf.download(symbol, period="3y", interval="1wk")
df = df.dropna().reset_index()
df = df[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]

# Detect market stage
stage = detect_market_stage(df)
print(f"\n🧠 Market Stage: {stage}")

# Save result to config
os.makedirs("config", exist_ok=True)
out_path = "config/market_status.json"
with open(out_path, "w") as f:
    json.dump({"market_stage": stage}, f, indent=2)

print(f"📁 Saved to {out_path}")
