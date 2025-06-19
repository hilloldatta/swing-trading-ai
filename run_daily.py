# === run_daily.py ===
import subprocess
import datetime

print("[RUN] Starting daily trading signal pipeline...")
print(f"[INFO] Date: {datetime.date.today()}")

# Step 1: Classify market stage (Weinstein's method)
print("\n[STEP 1] Classifying market stage...")
subprocess.run(["python", "scripts/classify_market.py"])

# Step 2: Fetch raw OHLCV data
print("\n[STEP 2] Fetching data...")
subprocess.run(["python", "scripts/fetch_data.py"])

# Step 3: Apply technical indicators to raw data
print("\n[STEP 3] Applying indicators...")
subprocess.run(["python", "scripts/apply_indicators.py"])

# Step 4: Detect chart patterns (VCP, Cup, Flag, RHS)
print("\n[STEP 4] Detecting patterns...")
subprocess.run(["python", "scripts/pattern_analysis.py"])

# Step 5: Rank strategies based on market stage and pattern signals
print("\n[STEP 5] Ranking strategies...")
subprocess.run(["python", "scripts/strategy_ranker.py"])

# Step 6: Add GPT explanations to top trades
print("\n[STEP 6] Adding GPT commentary...")
subprocess.run(["python", "scripts/enrich_with_gpt.py"])

print("\n✅ Daily run completed!")
print("📊 Market stage: config/market_status.json")
print("📈 Final recommendations: results/recommendations.json")
print("🤖 GPT-enhanced output: results/enriched_recommendations.json")
