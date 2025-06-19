import pandas as pd
import numpy as np

def compute_sma(series: pd.Series, window: int) -> pd.Series:
    return series.rolling(window=window).mean()

def compute_slope(series: pd.Series, window: int = 3) -> float:
    if len(series) < window:
        return 0.0
    y = series[-window:].values
    x = np.arange(window)
    m, _ = np.polyfit(x, y, 1)
    return m

def detect_market_stage(df: pd.DataFrame) -> str:
    """
    Detect market stage (Stage 1 to 4) using Weinstein's method.
    Assumes df is weekly OHLCV with columns: Date, Open, High, Low, Close, Volume
    """
    if df.empty or 'Close' not in df.columns:
        return "Insufficient Data"

    df = df.copy()
    df['SMA_30'] = compute_sma(df['Close'], 30)

    # Drop rows with NaN SMA values
    df = df.dropna(subset=['SMA_30'])

    if len(df) < 10:
        return "Insufficient Data"

    # Get scalar values instead of Series
    latest_close = float(df['Close'].iloc[-1])
    latest_sma = float(df['SMA_30'].iloc[-1])

    # Check SMA slope (ensure we have valid SMA data)
    slope = compute_slope(df['SMA_30'].dropna(), 3)

    # Stage detection logic
    if slope > 0 and latest_close > latest_sma:
        return "Stage 2"
    elif slope < 0 and latest_close < latest_sma:
        return "Stage 4"
    elif abs(slope) < 0.05:
        # Flat slope = Stage 1 or 3
        recent_high = float(df['Close'][-10:].max())
        recent_low = float(df['Close'][-10:].min())
        if latest_close > (recent_high * 0.95):
            return "Stage 3"
        elif latest_close < (recent_low * 1.05):
            return "Stage 1"

    return "Unclear"
