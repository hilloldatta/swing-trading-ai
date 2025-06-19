import pandas as pd

def detect_cup_handle(df: pd.DataFrame) -> bool:
    """
    Basic Cup and Handle pattern detection:
    - U-shaped base in last N bars
    - Followed by small pullback (handle)
    - Close near top of cup
    """
    if len(df) < 60:
        return False

    recent = df[-60:].copy()
    max_close = recent['Close'].max()
    min_close = recent['Close'].min()

    # Check for deep enough base
    if min_close / max_close > 0.85:
        return False

    # Cup: low is somewhere in the middle third
    middle = recent.iloc[20:40]
    if middle['Close'].min() != min_close:
        return False

    # Handle: last 10 bars are slightly down and tight
    handle = recent[-10:]
    if handle['Close'].max() - handle['Close'].min() > 0.1 * max_close:
        return False

    # Price near breakout zone
    if recent['Close'].iloc[-1] < 0.95 * max_close:
        return False

    return True