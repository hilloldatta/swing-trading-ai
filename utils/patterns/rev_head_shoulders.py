# === utils/patterns/rev_head_shoulders.py ===
import pandas as pd

def detect_reverse_head_and_shoulders(df: pd.DataFrame) -> dict:
    """
    Detect Reverse Head & Shoulders pattern (simplified version).

    :param df: DataFrame with OHLCV data
    :return: dict with {'signal': bool, 'pivot': float, 'stop_loss': float, 'target': float, 'type': str}
    """
    signal = False
    pivot = None
    stop_loss = None
    target = None

    try:
        closes = df['Close'].values
        if len(closes) < 20:
            return {"signal": False, "pivot": None, "stop_loss": None, "target": None, "type": "rhs"}

        right = closes[-1]
        middle = min(closes[-10:-5])
        left = closes[-15:-10].min()

        # Approximate: middle should be lowest, LHS and RHS shoulders slightly higher
        if middle < left and middle < right and abs(left - right) / middle < 0.15:
            signal = True
            pivot = closes[-1]
            stop_loss = middle * 0.95
            target = pivot * 1.15

    except Exception as e:
        print(f"RHS detection error: {e}")

    return {
        "signal": signal,
        "pivot": pivot,
        "stop_loss": stop_loss,
        "target": target,
        "type": "rhs"
    }
