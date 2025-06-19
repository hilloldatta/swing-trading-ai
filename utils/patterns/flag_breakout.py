import pandas as pd

def detect_flag_breakout(df: pd.DataFrame) -> bool:
    """
    Basic flag breakout detection:
    - Strong up move (flagpole)
    - Short-term consolidation (flag)
    - Breakout above flag resistance
    """
    if len(df) < 30:
        return False

    recent = df[-30:].copy()
    breakout_zone = recent['High'][-10:].max()
    last_close = recent['Close'].iloc[-1]

    # Check for recent breakout
    if last_close < breakout_zone:
        return False

    # Check previous trend (flagpole)
    pole = recent.iloc[-20:-10]
    if pole['Close'].iloc[-1] < pole['Close'].iloc[0] * 1.05:
        return False

    # Check flag tightness
    flag = recent.iloc[-10:]
    if flag['High'].max() - flag['Low'].min() > 0.1 * pole['Close'].iloc[-1]:
        return False

    return True
