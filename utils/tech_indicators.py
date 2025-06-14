import pandas as pd

def calculate_sma(df: pd.DataFrame, period: int, column: str = 'Close') -> pd.Series:
    """
    Calculate Simple Moving Average (SMA)
    :param df: DataFrame with OHLCV data
    :param period: lookback window
    :param column: price column (default: Close)
    :return: SMA series
    """
    return df[column].rolling(window=period).mean()

def calculate_ema(df: pd.DataFrame, period: int, column: str = 'Close') -> pd.Series:
    """
    Calculate Exponential Moving Average (EMA)
    :param df: DataFrame with OHLCV data
    :param period: lookback window
    :param column: price column (default: Close)
    :return: EMA series
    """
    return df[column].ewm(span=period, adjust=False).mean()

def calculate_rsi(df: pd.DataFrame, period: int = 14, column: str = 'Close') -> pd.Series:
    """
    Calculate Relative Strength Index (RSI)
    :param df: DataFrame with OHLCV data
    :param period: lookback window (default 14)
    :param column: price column
    :return: RSI series
    """
    delta = df[column].diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)
    avg_gain = gain.rolling(window=period).mean()
    avg_loss = loss.rolling(window=period).mean()
    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))
    return rsi

def calculate_macd(df: pd.DataFrame, fast_period: int = 12, slow_period: int = 26, signal_period: int = 9, column: str = 'Close'):
    """
    Calculate MACD line and Signal line
    :param df: DataFrame with OHLCV data
    :param fast_period: short EMA period
    :param slow_period: long EMA period
    :param signal_period: signal line EMA period
    :param column: price column
    :return: MACD line, Signal line as pd.Series
    """
    ema_fast = df[column].ewm(span=fast_period, adjust=False).mean()
    ema_slow = df[column].ewm(span=slow_period, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    return macd_line, signal_line
