import yfinance as yf
import pandas as pd
from datetime import date
import os

INPUT_PATH = "data/test_symbols.csv"
RAW_OUTPUT_DIR = f"data/raw/{date.today()}"
PROCESSED_OUTPUT_DIR = f"data/processed/{date.today()}"

# Ensure output directories exist
os.makedirs(RAW_OUTPUT_DIR, exist_ok=True)
os.makedirs(PROCESSED_OUTPUT_DIR, exist_ok=True)

# Load ticker list
tickers_df = pd.read_csv(INPUT_PATH)
tickers = tickers_df['symbol'].tolist()

for symbol in tickers:
    try:
        print(f"📥 Fetching {symbol}...")
        data = yf.download(symbol, period="1y", interval="1d", progress=False)
        if not data.empty:
            # Save raw data
            data.to_csv(f"{RAW_OUTPUT_DIR}/{symbol}.csv")

            # Clean and normalize data
            # Reset index to get Date as a column
            data = data.reset_index()

            # Handle multi-level columns if they exist
            if isinstance(data.columns, pd.MultiIndex):
                # Flatten multi-level columns by taking the first level
                data.columns = [col[0] if isinstance(col, tuple) else col for col in data.columns]

            # Ensure we have the expected columns
            expected_cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
            if not all(col in data.columns for col in expected_cols):
                print(f"⚠️ Missing expected columns for {symbol}. Available: {data.columns.tolist()}")
                continue

            # Select and clean data
            data = data[expected_cols].dropna()

            # Convert to proper data types
            data[['Open', 'High', 'Low', 'Close']] = data[['Open', 'High', 'Low', 'Close']].round(2)
            data['Volume'] = data['Volume'].astype(int)

            # Save processed data
            data.to_csv(f"{PROCESSED_OUTPUT_DIR}/{symbol}.csv", index=False)
            print(f"✅ Saved: {symbol}.csv ({len(data)} rows)")
        else:
            print(f"⚠️ No data for {symbol}")
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
