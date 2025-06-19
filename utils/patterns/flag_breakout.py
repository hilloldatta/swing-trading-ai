# === utils/patterns/flag_breakout.py ===
import pandas as pd

def detect_flag_breakout(df: pd.DataFrame) -> dict:
    if len(df) < 30:
        return {"signal": False, "type": "flag", "pivot": None, "stop_loss": None, "target": None}

    recent = df[-30:].copy()
    breakout_zone = recent['High'][-10:].max()
    last_close = recent['Close'].iloc[-1]
    pole = recent.iloc[-20:-10]
    flag = recent.iloc[-10:]

    if (
        last_close >= breakout_zone and
        pole['Close'].iloc[-1] > pole['Close'].iloc[0] * 1.05 and
        flag['High'].max() - flag['Low'].min() <= 0.1 * pole['Close'].iloc[-1]
    ):
        pivot = last_close
        stop_loss = flag['Low'].min() * 0.97
        target = pivot * 1.1
        return {"signal": True, "type": "flag", "pivot": pivot, "stop_loss": stop_loss, "target": target}

    return {"signal": False, "type": "flag", "pivot": None, "stop_loss": None, "target": None}
