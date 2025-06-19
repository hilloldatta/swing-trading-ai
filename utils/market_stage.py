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
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) >= 2 else latest

    # Check SMA slope
    slope = compute_slope(df['SMA_30'], 3)

    # Stage detection logic
    if slope > 0 and latest['Close'] > latest['SMA_30']:
        return "Stage 2"
    elif slope < 0 and latest['Close'] < latest['SMA_30']:
        return "Stage 4"
    elif abs(slope) < 0.05:
        # Flat slope = Stage 1 or 3
        recent_high = df['Close'][-10:].max()
        recent_low = df['Close'][-10:].min()
        if latest['Close'] > (recent_high * 0.95):
            return "Stage 3"
        elif latest['Close'] < (recent_low * 1.05):
            return "Stage 1"

    return "Unclear"
