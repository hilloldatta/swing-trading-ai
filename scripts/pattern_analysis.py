# === scripts/pattern_analysis.py ===
import os
import json
import pandas as pd
from datetime import date
from utils.patterns.vcp_detector import detect_vcp
from utils.patterns.cup_handle_detector import detect_cup_handle
from utils.patterns.flag_breakout import detect_flag_breakout
from utils.patterns.rev_head_shoulders import detect_reverse_head_and_shoulders

RAW_PROCESSED_PATH = f"data/processed/{date.today()}"
SIGNALS_PATH = "results/pattern_signals.json"

signals = []

for file in os.listdir(RAW_PROCESSED_PATH):
    if file.endswith(".csv"):
        symbol = file.replace(".csv", "")
        try:
            df = pd.read_csv(os.path.join(RAW_PROCESSED_PATH, file))

            vcp = detect_vcp(df)
            cup = detect_cup_handle(df)
            flag = detect_flag_breakout(df)
            rhs = detect_reverse_head_and_shoulders(df)

            # Collect detected patterns for this symbol
            detected_patterns = []
            pattern_details = {}

            if vcp["signal"]:
                detected_patterns.append("VCP")
                pattern_details["VCP"] = vcp
                print(f"VCP Signal: {symbol} → Pivot: {vcp['pivot']}")

            if cup["signal"]:
                detected_patterns.append("CupHandle")
                pattern_details["CupHandle"] = cup
                print(f"Cup Signal: {symbol} → Pivot: {cup['pivot']}")

            if flag["signal"]:
                detected_patterns.append("Flag")
                pattern_details["Flag"] = flag
                print(f"Flag Signal: {symbol} → Pivot: {flag['pivot']}")

            if rhs["signal"]:
                detected_patterns.append("RHS")
                pattern_details["RHS"] = rhs
                print(f"RHS Signal: {symbol} → Pivot: {rhs['pivot']}")

            # If any patterns detected, create a signal entry
            if detected_patterns:
                signal = {
                    "symbol": symbol,
                    "patterns": detected_patterns,
                    "details": pattern_details,
                    "pivot": pattern_details[detected_patterns[0]]["pivot"]  # Use first pattern's pivot
                }
                signals.append(signal)

        except Exception as e:
            print(f"Error processing {symbol}: {e}")

# Save detected signals
if signals:
    with open(SIGNALS_PATH, 'w') as f:
        json.dump(signals, f, indent=2)
    print(f"Saved {len(signals)} signals to {SIGNALS_PATH}")
else:
    print("No pattern signals detected today.")
