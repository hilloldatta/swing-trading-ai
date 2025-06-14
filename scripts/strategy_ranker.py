# === scripts/strategy_ranker.py ===
import json
import pandas as pd
from datetime import date

SIGNALS_PATH = "results/vcp_signals.json"
RANKED_OUTPUT_PATH = "results/recommendations.json"

# Strategy weights for different pattern types
strategy_weights = {
    "vcp": 1.5,
    "cup": 1.2,
    "flag": 1.0,
    "rhs": 1.3  # Reverse Head & Shoulders
}

# Load signals from JSON
with open(SIGNALS_PATH, 'r') as f:
    signals = json.load(f)

# Convert to DataFrame
df = pd.DataFrame(signals)

# Assign weight-based score
df['score'] = df['type'].map(strategy_weights).fillna(0)

# Sort by score and optionally pivot value
df = df.sort_values(by=['score', 'pivot'], ascending=[False, False])

# Add rank
df['rank'] = range(1, len(df) + 1)

# Save to recommendations output
df.to_json(RANKED_OUTPUT_PATH, orient='records', indent=2)
print(f"Ranked {len(df)} signals and saved to {RANKED_OUTPUT_PATH}")
