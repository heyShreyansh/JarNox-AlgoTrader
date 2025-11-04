from data_feed import fetch_historical
from strategies import generate_signals
import pandas as pd

def run_backtest(ticker='AAPL', start='2023-01-01', end='2024-12-31', capital=10000):
    df = fetch_historical(ticker, start, end)
    df = generate_signals(df)
    cash = float(capital)
    position = 0
    trades = []
    equity = []

    for idx in df.index:
        # use df.at to guarantee scalar access
        try:
            buy_signal = bool(df.at[idx, 'buy']) if 'buy' in df.columns else False
            sell_signal = bool(df.at[idx, 'sell']) if 'sell' in df.columns else False
        except Exception:
            # fallback: coerce row values explicitly
            row = df.loc[idx]
            buy_signal = bool(row['buy']) if 'buy' in row.index else False
            sell_signal = bool(row['sell']) if 'sell' in row.index else False

        price = float(df.at[idx, 'close']) if pd.notna(df.at[idx, 'close']) else 0.0

        if buy_signal and position == 0 and price > 0:
            qty = int(cash // price)
            if qty > 0:
                position = qty
                cost = qty * price
                cash -= cost
                trades.append({'date': idx.strftime('%Y-%m-%d'), 'type':'BUY', 'price': price, 'size': qty})
        if sell_signal and position > 0 and price > 0:
            proceeds = position * price
            cash += proceeds
            trades.append({'date': idx.strftime('%Y-%m-%d'), 'type':'SELL', 'price': price, 'size': position})
            position = 0

        total = cash + position * price
        equity.append({'date': idx.strftime('%Y-%m-%d'), 'equity': total})

    eq_df = pd.DataFrame(equity).set_index('date') if equity else pd.DataFrame([{'date':'0','equity':capital}]).set_index('date')
    ending = float(eq_df['equity'].iloc[-1]) if not eq_df.empty else capital
    summary = {
        'starting_capital': capital,
        'ending_capital': ending,
        'trades': len(trades),
        'pnl': ending - capital
    }
    payload = {
        'dates': df.index.strftime('%Y-%m-%d').tolist(),
        'close': df['close'].round(4).tolist(),
        'sma_short': df['sma_short'].fillna(0).round(4).tolist(),
        'sma_long': df['sma_long'].fillna(0).round(4).tolist(),
        'buy_dates': [t['date'] for t in trades if t['type']=='BUY'],
        'buy_prices': [t['price'] for t in trades if t['type']=='BUY'],
        'sell_dates': [t['date'] for t in trades if t['type']=='SELL'],
        'sell_prices': [t['price'] for t in trades if t['type']=='SELL'],
        'eq_dates': eq_df.index.tolist(),
        'equity': eq_df['equity'].tolist(),
        'summary': summary
    }
    return payload
