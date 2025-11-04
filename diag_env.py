import sys, traceback, pprint
print("Running diagnostic with interpreter:", sys.executable)
print("Python version:", sys.version)
print("\nFirst entries of sys.path:")
pprint.pprint(sys.path[:6])

try:
    import yfinance as yf
    print("\nyfinance import: OK (version unknown display suppressed)")
    # quick quick test: fetch a tiny dataframe
    df = yf.download("AAPL", start="2023-01-01", end="2023-01-10", progress=False)
    print("yfinance fetch shape:", getattr(df, 'shape', None))
except Exception as e:
    print("\nFAILED importing or running yfinance:")
    traceback.print_exc()

# Now try to import your modules and run the signal generator
try:
    from data_feed import fetch_historical
    from strategies import generate_signals
    df = fetch_historical('AAPL', '2023-01-01', '2023-03-31')
    df2 = generate_signals(df)
    print("\ngenerate_signals succeeded. columns:", df2.columns.tolist())
    print("Sample buy/sell types (first 5):")
    for idx in df2.index[:5]:
        print(idx.strftime('%Y-%m-%d'), type(df2.at[idx,'buy']), repr(df2.at[idx,'buy']), type(df2.at[idx,'sell']), repr(df2.at[idx,'sell']))
except Exception as e:
    print("\nFAILED running generate_signals:")
    traceback.print_exc()
