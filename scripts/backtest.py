# === scripts/backtest.py ===
import os
import json
import pandas as pd
from datetime import date

RECOMMENDATIONS_PATH = "results/recommendations.json"
DATA_PATH = f"data/processed/{date.today()}"

results = []

with open(RECOMMENDATIONS_PATH, 'r') as f:
    signals = json.load(f)

for signal in signals:
    symbol = signal['symbol']
    pivot = signal['pivot']
    stop_loss = signal['stop_loss']
    target = signal['target']
    pattern_type = signal.get('type', 'unknown')

    file_path = os.path.join(DATA_PATH, f"{symbol}.csv")
    if not os.path.exists(file_path):
        print(f"❌ Missing data for {symbol}, skipping")
        continue

    df = pd.read_csv(file_path)
    if 'Date' in df.columns:
        df['Date'] = pd.to_datetime(df['Date'])
    
    entry_index = df[df['Close'].round(2) == round(pivot, 2)].index
    if len(entry_index) == 0:
        print(f"⚠️ Pivot price {pivot} not found for {symbol}, skipping")
        continue

    entry_idx = entry_index[-1] + 1  # Start checking from next day
    trade_data = df.iloc[entry_idx:].copy()

    outcome = 'open'
    exit_price = None
    exit_date = None
    for i, row in trade_data.iterrows():
        if row['Low'] <= stop_loss:
            outcome = 'loss'
            exit_price = stop_loss
            exit_date = row['Date']
            break
        elif row['High'] >= target:
            outcome = 'win'
            exit_price = target
            exit_date = row['Date']
            break

    if outcome == 'open':
        continue  # Skip unresolved trades

    ret_pct = round((exit_price - pivot) / pivot * 100, 2)
    days_held = (exit_date - df.loc[entry_idx - 1, 'Date']).days

    results.append({
        'symbol': symbol,
        'pattern': pattern_type,
        'entry': pivot,
        'exit': exit_price,
        'return_pct': ret_pct,
        'days_held': days_held,
        'outcome': outcome,
        'exit_date': str(exit_date.date())
    })

# Output results
output_path = "results/backtest_results.json"
with open(output_path, 'w') as f:
    json.dump(results, f, indent=2)

print(f"✅ Backtest complete. Results saved to {output_path}")
