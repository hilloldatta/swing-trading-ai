# === scripts/pattern_analysis.py ===
import os
import json
import pandas as pd
from datetime import date
from utils.patterns.vcp_detector import detect_vcp
from utils.patterns.cup_handle_detector import detect_cup_with_handle
from utils.patterns.flag_breakout import detect_flag_breakout
from utils.patterns.rev_head_shoulders import detect_reverse_head_and_shoulders

RAW_PROCESSED_PATH = f"data/processed/{date.today()}"
SIGNALS_PATH = "results/vcp_signals.json"

signals = []

for file in os.listdir(RAW_PROCESSED_PATH):
    if file.endswith(".csv"):
        symbol = file.replace(".csv", "")
        try:
            df = pd.read_csv(os.path.join(RAW_PROCESSED_PATH, file))

            vcp = detect_vcp(df)
            cup = detect_cup_with_handle(df)
            flag = detect_flag_breakout(df)
            rhs = detect_reverse_head_and_shoulders(df)

            if vcp["signal"]:
                vcp.update({"symbol": symbol, "type": "vcp"})
                signals.append(vcp)
                print(f"VCP Signal: {symbol} → Pivot: {vcp['pivot']}")

            if cup["signal"]:
                cup.update({"symbol": symbol, "type": "cup"})
                signals.append(cup)
                print(f"Cup Signal: {symbol} → Pivot: {cup['pivot']}")

            if flag["signal"]:
                flag.update({"symbol": symbol, "type": "flag"})
                signals.append(flag)
                print(f"Flag Signal: {symbol} → Pivot: {flag['pivot']}")

            if rhs["signal"]:
                rhs.update({"symbol": symbol, "type": "rhs"})
                signals.append(rhs)
                print(f"RHS Signal: {symbol} → Pivot: {rhs['pivot']}")

        except Exception as e:
            print(f"Error processing {symbol}: {e}")

# Save detected signals
if signals:
    with open(SIGNALS_PATH, 'w') as f:
        json.dump(signals, f, indent=2)
    print(f"Saved {len(signals)} signals to {SIGNALS_PATH}")
else:
    print("No pattern signals detected today.")
