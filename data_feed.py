import yfinance as yf
import pandas as pd

def _to_series_safe(s, fallback_index=None):
    import numpy as np
    # If already a Series, coerce to numeric and return
    if isinstance(s, pd.Series):
        s = pd.to_numeric(s, errors='coerce')
        s.index = pd.to_datetime(s.index)
        return s.dropna()
    # If it's a DataFrame with single column, take that column
    if isinstance(s, pd.DataFrame):
        if s.shape[1] == 1:
            col = s.iloc[:,0]
            col = pd.to_numeric(col, errors='coerce')
            col.index = pd.to_datetime(col.index)
            return col.dropna()
        # if multiple columns, try to pick last numeric column
        numeric_cols = s.select_dtypes(include=['number']).columns
        if len(numeric_cols) > 0:
            col = s[numeric_cols[-1]]
            col = pd.to_numeric(col, errors='coerce')
            col.index = pd.to_datetime(col.index)
            return col.dropna()
        raise ValueError("No numeric column found in DataFrame")
    # If it's a numpy scalar or Python scalar, turn into a Series with fallback_index
    if isinstance(s, (np.generic, float, int)) or not hasattr(s, '__len__'):
        if fallback_index is None:
            raise ValueError("Scalar value returned and no fallback index provided")
        ser = pd.Series([float(s)], index=pd.to_datetime([fallback_index]))
        ser.name = 'close'
        return ser
    # Otherwise try to coerce to Series
    ser = pd.Series(s)
    ser = pd.to_numeric(ser, errors='coerce')
    ser.index = pd.to_datetime(ser.index) if hasattr(ser.index, 'dtype') else pd.to_datetime([fallback_index]*len(ser))
    return ser.dropna()

def fetch_historical(ticker='AAPL', start='2023-01-01', end='2024-12-31'):
    # Use auto_adjust to get adjusted close by default
    df = yf.download(ticker, start=start, end=end, progress=False, auto_adjust=True)
    if df is None:
        raise ValueError(f'No data returned for {ticker}')
    try:
        s = None
        # If yfinance returned a DataFrame, prefer 'Close'
        if isinstance(df, pd.DataFrame):
            if 'Close' in df.columns:
                s = df['Close']
            else:
                numeric_cols = df.select_dtypes(include=['number']).columns
                if len(numeric_cols) > 0:
                    s = df[numeric_cols[-1]]
                else:
                    # fallback to the first column
                    s = df.iloc[:, 0]
        else:
            # if yfinance returned a Series or scalar
            s = df
        ser = _to_series_safe(s, fallback_index=start)
    except Exception as e:
        raise ValueError(f"Failed to normalize price series: {e}")
    ser.name = 'close'
    ser = ser.dropna()
    if ser.empty:
        raise ValueError(f'No numeric close data for {ticker} between {start} and {end}')
    # Return single-column DataFrame to keep API consistent
    return pd.DataFrame({'close': ser})
