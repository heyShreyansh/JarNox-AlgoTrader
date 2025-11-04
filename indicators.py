import pandas as pd
from ta.momentum import RSIIndicator

def sma(df, window=20):
    return df['close'].rolling(window=window).mean()

def rsi(df, window=14):
    close_series = df['close'].squeeze()
    if isinstance(close_series, pd.DataFrame):
        close_series = close_series.iloc[:, 0]
    return RSIIndicator(close_series, window=window).rsi()
