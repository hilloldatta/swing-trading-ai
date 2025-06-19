# === scripts/strategy_ranker.py ===
import json
import os
from collections import defaultdict

# Load strategy weights based on market condition
DEFAULT_WEIGHTS = {
    "Stage 1": {"VCP": 0.2, "CupHandle": 0.2, "Flag": 0.1, "RHS": 0.1},
    "Stage 2": {"VCP": 1.0, "CupHandle": 0.9, "Flag": 0.8, "RHS": 0.7},
    "Stage 3": {"VCP": 0.3, "CupHandle": 0.2, "Flag": 0.1, "RHS": 0.1},
    "Stage 4": {"VCP": 0.1, "CupHandle": 0.1, "Flag": 0.1, "RHS": 0.1},
    "Unknown": {"VCP": 0.5, "CupHandle": 0.5, "Flag": 0.5, "RHS": 0.5}
}

INPUT_PATH = "results/pattern_signals.json"
OUTPUT_PATH = "results/recommendations.json"


def rank_strategies(market_stage=None):
    if not os.path.exists(INPUT_PATH):
        print("⚠️ No pattern_signals.json found.")
        return

    # Load market stage from config if not provided
    if market_stage is None:
        market_config_path = "config/market_status.json"
        if os.path.exists(market_config_path):
            with open(market_config_path, 'r') as f:
                market_data = json.load(f)
                market_stage = market_data.get("market_stage", "Unknown")
                print(f"📈 Using market stage: {market_stage}")
        else:
            market_stage = "Unknown"
            print("⚠️ No market stage data found, using 'Unknown'")

    with open(INPUT_PATH, 'r') as f:
        signals = json.load(f)

    weights = DEFAULT_WEIGHTS.get(market_stage, DEFAULT_WEIGHTS["Unknown"])
    print(f"🎯 Pattern weights for {market_stage}: {weights}")
    ranked = []

    for signal in signals:
        score = 0
        patterns = signal.get("patterns", [])
        for pattern in patterns:
            score += weights.get(pattern, 0.0)
        signal['score'] = round(score, 2)
        ranked.append(signal)

    ranked.sort(key=lambda x: x['score'], reverse=True)

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(ranked, f, indent=2)

    print(f"📊 Strategy ranking complete. Top {len(ranked)} signals saved to {OUTPUT_PATH}")


if __name__ == "__main__":
    rank_strategies()
