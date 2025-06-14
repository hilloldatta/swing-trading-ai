# === run_daily.py ===
import subprocess
import datetime

print("[RUN] Starting daily trading signal pipeline...")
print(f"[INFO] Date: {datetime.date.today()}")

# Step 1: Fetch raw OHLCV data
print("\n[STEP 1] Fetching data...")
subprocess.run(["python", "scripts/fetch_data.py"])

# Step 2: Apply technical indicators to raw data
print("\n[STEP 2] Applying indicators...")
subprocess.run(["python", "scripts/apply_indicators.py"])

# Step 3: Detect chart patterns (VCP, Cup, Flag, RHS)
print("\n[STEP 3] Detecting patterns...")
subprocess.run(["python", "scripts/pattern_analysis.py"])

# Step 4: Rank strategies based on weights and pattern signals
print("\n[STEP 4] Ranking strategies...")
subprocess.run(["python", "scripts/strategy_ranker.py"])

# Step 5: Add GPT explanations to top trades
print("\n[STEP 5] Adding GPT commentary...")
subprocess.run(["python", "scripts/enrich_with_gpt.py"])

print("\n✅ Daily run completed. Final output at results/enriched_recommendations.json")
