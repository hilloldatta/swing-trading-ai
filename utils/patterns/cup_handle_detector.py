import pandas as pd

def detect_cup_handle(df: pd.DataFrame) -> dict:
    """
    Basic Cup and Handle pattern detection:
    - U-shaped base in last N bars
    - Followed by small pullback (handle)
    - Close near top of cup
    """
    if len(df) < 60:
        return {"signal": False, "pivot": None, "reason": "Insufficient data"}

    recent = df[-60:].copy()
    max_close = recent['Close'].max()
    min_close = recent['Close'].min()
    last_close = recent['Close'].iloc[-1]

    # Check for deep enough base
    if min_close / max_close > 0.85:
        return {"signal": False, "pivot": None, "reason": "Base not deep enough"}

    # Cup: low is somewhere in the middle third
    middle = recent.iloc[20:40]
    if middle['Close'].min() != min_close:
        return {"signal": False, "pivot": None, "reason": "Low not in middle third"}

    # Handle: last 10 bars are slightly down and tight
    handle = recent[-10:]
    if handle['Close'].max() - handle['Close'].min() > 0.1 * max_close:
        return {"signal": False, "pivot": None, "reason": "Handle too wide"}

    # Price near breakout zone
    if last_close < 0.95 * max_close:
        return {"signal": False, "pivot": None, "reason": "Price not near breakout"}

    return {
        "signal": True,
        "pivot": float(last_close),
        "reason": "Cup and Handle pattern detected",
        "depth": float((max_close - min_close) / max_close),
        "breakout_level": float(max_close)
    }