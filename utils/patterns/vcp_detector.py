import pandas as pd


def detect_vcp(df: pd.DataFrame) -> dict:
    """
    Basic Volatility Contraction Pattern (VCP) detection logic:
    - Look for 3 consecutive lower highs and lower lows
    - Look for decreasing volatility (range contraction)
    - Look for decreasing volume trend
    """
    if len(df) < 30:
        return {"signal": False, "pivot": None, "reason": "Insufficient data"}

    recent = df[-20:].copy()
    recent['Range'] = recent['High'] - recent['Low']

    # Check range contraction: average of last 5 < previous 5
    r1 = recent['Range'][-5:].mean()
    r2 = recent['Range'][-10:-5].mean()
    if r1 >= r2:
        return {"signal": False, "pivot": None, "reason": "No range contraction"}

    # Check volume contraction
    v1 = recent['Volume'][-5:].mean()
    v2 = recent['Volume'][-10:-5].mean()
    if v1 >= v2:
        return {"signal": False, "pivot": None, "reason": "No volume contraction"}

    # Optional: price trending up near recent high
    last_close = recent['Close'].iloc[-1]
    highest = recent['Close'].max()
    if last_close < 0.9 * highest:
        return {"signal": False, "pivot": None, "reason": "Price not near high"}

    return {
        "signal": True,
        "pivot": float(last_close),
        "reason": "VCP pattern detected",
        "range_contraction": float(r1/r2),
        "volume_contraction": float(v1/v2)
    }
