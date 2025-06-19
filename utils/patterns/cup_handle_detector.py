# === utils/patterns/cup_handle_detector.py ===
import pandas as pd

def detect_cup_handle(df: pd.DataFrame) -> dict:
    if len(df) < 60:
        return {"signal": False, "type": "cup_handle", "pivot": None, "stop_loss": None, "target": None}

    recent = df[-60:].copy()
    max_close = recent['Close'].max()
    min_close = recent['Close'].min()
    middle = recent.iloc[20:40]
    handle = recent[-10:]
    last_close = recent['Close'].iloc[-1]

    if (
        min_close / max_close <= 0.85 and
        middle['Close'].min() == min_close and
        handle['Close'].max() - handle['Close'].min() <= 0.1 * max_close and
        last_close >= 0.95 * max_close
    ):
        pivot = last_close
        stop_loss = handle['Low'].min() * 0.97
        target = pivot * 1.2
        return {"signal": True, "type": "cup_handle", "pivot": pivot, "stop_loss": stop_loss, "target": target}

    return {"signal": False, "type": "cup_handle", "pivot": None, "stop_loss": None, "target": None}
