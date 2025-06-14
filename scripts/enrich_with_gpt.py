# === scripts/enrich_with_gpt.py ===
import json
from utils.gpt_client import explain_pattern

INPUT_PATH = "results/recommendations.json"
OUTPUT_PATH = "results/enriched_recommendations.json"
MAX_SIGNALS = 5  # Limit to top N signals for cost-saving

def enrich_signals_with_explanations():
    with open(INPUT_PATH, 'r') as f:
        signals = json.load(f)

    enriched = []
    for i, signal in enumerate(signals):
        if i >= MAX_SIGNALS:
            break

        print(f"[GPT] Explaining {signal['symbol']} ({signal['type']})...")
        explanation = explain_pattern(
            symbol=signal['symbol'],
            pattern_type=signal['type'],
            pivot=signal['pivot'],
            stop_loss=signal['stop_loss'],
            target=signal['target']
        )
        signal['explanation'] = explanation
        enriched.append(signal)

    with open(OUTPUT_PATH, 'w') as f:
        json.dump(enriched, f, indent=2)

    print(f"✅ Saved enriched signals to {OUTPUT_PATH}")

if __name__ == "__main__":
    enrich_signals_with_explanations()
