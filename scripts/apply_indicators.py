import os
import pandas as pd
from datetime import date
import sys


from utils.tech_indicators import calculate_sma, calculate_ema, calculate_rsi, calculate_macd

RAW_FOLDER = f"data/processed/{date.today()}"
PROCESSED_FOLDER = RAW_FOLDER  # Save over the same processed data
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

for file in os.listdir(RAW_FOLDER):
    if file.endswith(".csv"):
        symbol = file.replace(".csv", "")
        path = os.path.join(RAW_FOLDER, file)
        try:
            df = pd.read_csv(path)

            # Calculate indicators
            df['SMA_50'] = calculate_sma(df, 50)
            df['SMA_200'] = calculate_sma(df, 200)
            df['EMA_20'] = calculate_ema(df, 20)
            df['RSI_14'] = calculate_rsi(df)
            df['MACD_Line'], df['MACD_Signal'] = calculate_macd(df)

            # Save processed data
            df.to_csv(os.path.join(PROCESSED_FOLDER, file), index=False)
            print(f"Processed: {symbol}")
        except Exception as e:
            print(f"Failed for {symbol}: {e}")
