import yfinance as yf
import pandas as pd
from datetime import date
import os

INPUT_PATH = "data/nifty100_list.csv"
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
        data = yf.download(symbol, period="1y", interval="1d")
        if not data.empty:
            data.to_csv(f"{RAW_OUTPUT_DIR}/{symbol}.csv")

            # Basic normalization: drop NA, reset index, round floats
            data = data.dropna().reset_index()
            data = data[['Date', 'Open', 'High', 'Low', 'Close', 'Volume']]
            data[['Open', 'High', 'Low', 'Close']] = data[['Open', 'High', 'Low', 'Close']].round(2)
            data['Volume'] = data['Volume'].astype(int)
            data.to_csv(f"{PROCESSED_OUTPUT_DIR}/{symbol}.csv", index=False)
            print(f"✅ Saved: {symbol}.csv (processed)")
        else:
            print(f"⚠️ No data for {symbol}")
    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")
