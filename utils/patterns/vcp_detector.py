import pandas as pd

def detect_vcp(df: pd.DataFrame) -> dict:
    if len(df) < 30:
        return {"signal": False, "type": "vcp", "pivot": None, "stop_loss": None, "target": None}

    recent = df[-20:].copy()
    recent['Range'] = recent['High'] - recent['Low']

    r1 = recent['Range'][-5:].mean()
    r2 = recent['Range'][-10:-5].mean()
    v1 = recent['Volume'][-5:].mean()
    v2 = recent['Volume'][-10:-5].mean()
    last_close = recent['Close'].iloc[-1]
    highest = recent['Close'].max()

    if r1 < r2 and v1 < v2 and last_close > 0.9 * highest:
        pivot = last_close
        stop_loss = recent['Low'].min() * 0.97
        target = pivot * 1.15
        return {"signal": True, "type": "vcp", "pivot": pivot, "stop_loss": stop_loss, "target": target}

    return {"signal": False, "type": "vcp", "pivot": None, "stop_loss": None, "target": None}