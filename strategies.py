import pandas as pd
from ta.momentum import RSIIndicator

def sma(df, window):
    return df['close'].rolling(window).mean()

def rsi(df, window=14):
    s = df['close']
    # If single-column DataFrame sneaks in, convert to Series
    if getattr(s, 'ndim', 1) > 1:
        s = pd.Series(s.values.flatten(), index=df.index)
    s = pd.to_numeric(s, errors='coerce')
    return RSIIndicator(s, window=window).rsi()

def generate_signals(df, short=20, long=50):
    df = df.copy()
    df['sma_short'] = sma(df, short)
    df['sma_long'] = sma(df, long)
    df['rsi'] = rsi(df)
    df['signal_sma'] = 0
    df.loc[df['sma_short'] > df['sma_long'], 'signal_sma'] = 1
    df.loc[df['sma_short'] < df['sma_long'], 'signal_sma'] = -1
    df['sma_cross'] = df['signal_sma'].diff()

    raw_buy = ((df['sma_cross'] == 2) | (df['sma_cross'] == 1)) & (df['rsi'] < 60)
    raw_sell = ((df['sma_cross'] == -2) | (df['sma_cross'] == -1)) & (df['rsi'] > 40)

    # Coerce to plain Python booleans per row to remove any ambiguity
    df['buy'] = raw_buy.fillna(False).apply(lambda x: bool(x))
    df['sell'] = raw_sell.fillna(False).apply(lambda x: bool(x))
    return df
