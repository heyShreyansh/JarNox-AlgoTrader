import React, { useState } from 'react';
import Plot from 'react-plotly.js';

function App() {
  const [ticker, setTicker] = useState('AAPL');
  const [start, setStart] = useState('2023-01-01');
  const [end, setEnd] = useState('2024-12-31');
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const runBacktest = async () => {
    setLoading(true);
    setError(null);
    try {
      const url = `http://localhost:5000/backtest?ticker=${ticker}&start=${start}&end=${end}`;
      const response = await fetch(url);
      if (!response.ok) throw new Error('Backend error');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: '100vh', background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)' }}>
      <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '40px 20px' }}>
        <h1 style={{ fontSize: '2rem', fontWeight: 'bold', color: 'white', marginBottom: '30px' }}>
          🚀 JarNox Algo Trading Dashboard
        </h1>

        <section style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '16px', marginBottom: '24px' }}>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: 'white', marginBottom: '4px' }}>Ticker</label>
            <input value={ticker} onChange={e => setTicker(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '8px', border: 'none' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: 'white', marginBottom: '4px' }}>Start Date</label>
            <input type="date" value={start} onChange={e => setStart(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '8px', border: 'none' }} />
          </div>
          <div>
            <label style={{ display: 'block', fontSize: '0.875rem', fontWeight: '500', color: 'white', marginBottom: '4px' }}>End Date</label>
            <input type="date" value={end} onChange={e => setEnd(e.target.value)} style={{ width: '100%', padding: '8px', borderRadius: '8px', border: 'none' }} />
          </div>
        </section>

        <div style={{ display: 'flex', gap: '12px', marginBottom: '24px', flexWrap: 'wrap' }}>
          <button onClick={runBacktest} disabled={loading} style={{ padding: '10px 20px', background: loading ? '#9333ea' : '#7c3aed', color: 'white', borderRadius: '8px', border: 'none', cursor: loading ? 'not-allowed' : 'pointer', fontWeight: '600' }}>
            {loading ? '⏳ Running...' : '▶️ Run Backtest'}
          </button>
          <button onClick={() => { setTicker('AAPL'); setStart('2023-01-01'); setEnd('2024-12-31'); setData(null); setError(null); }} style={{ padding: '10px 20px', background: 'white', color: '#333', borderRadius: '8px', border: 'none', cursor: 'pointer', fontWeight: '600' }}>
            🔄 Reset
          </button>
        </div>

        {error && <div style={{ padding: '16px', background: '#fee2e2', color: '#991b1b', borderRadius: '8px', marginBottom: '16px' }}>⚠️ Error: {error}</div>}

        {!data && !loading && <div style={{ padding: '60px 20px', textAlign: 'center', color: 'white', fontSize: '1.1rem' }}>📊 No data yet. Run a backtest!</div>}

        {data && (
          <div style={{ display: 'flex', flexDirection: 'column', gap: '24px' }}>
            <div style={{ background: 'white', padding: '20px', borderRadius: '12px' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '16px' }}>📈 Price Chart — {ticker.toUpperCase()}</h2>
              <Plot data={[
                { x: data.dates, y: data.close, type: 'scatter', mode: 'lines', name: 'Close', line: { color: '#3b82f6', width: 2 } },
                { x: data.dates, y: data.sma_short, type: 'scatter', mode: 'lines', name: 'SMA Short', line: { color: '#f59e0b', dash: 'dash' } },
                { x: data.dates, y: data.sma_long, type: 'scatter', mode: 'lines', name: 'SMA Long', line: { color: '#ef4444', dash: 'dash' } },
                { x: data.buy_dates, y: data.buy_prices, mode: 'markers', name: 'Buy', marker: { symbol: 'triangle-up', size: 12, color: '#10b981' } },
                { x: data.sell_dates, y: data.sell_prices, mode: 'markers', name: 'Sell', marker: { symbol: 'triangle-down', size: 12, color: '#ef4444' } }
              ]} layout={{ height: 450, autosize: true, margin: { l: 50, r: 40, t: 40, b: 50 } }} style={{ width: '100%' }} useResizeHandler />
            </div>

            <div style={{ background: 'white', padding: '20px', borderRadius: '12px' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '16px' }}>💰 Equity Curve</h2>
              <Plot data={[{ x: data.eq_dates, y: data.equity, type: 'scatter', mode: 'lines+markers', name: 'Equity', line: { color: '#8b5cf6', width: 3 } }]} layout={{ height: 350, autosize: true, margin: { l: 50, r: 40, t: 30, b: 50 } }} style={{ width: '100%' }} useResizeHandler />
            </div>

            <div style={{ background: 'white', padding: '20px', borderRadius: '12px' }}>
              <h2 style={{ fontSize: '1.25rem', fontWeight: '600', marginBottom: '16px' }}>📊 Summary</h2>
              <pre style={{ fontSize: '0.9rem', background: '#f3f4f6', padding: '16px', borderRadius: '8px', fontFamily: 'monospace' }}>{JSON.stringify(data.summary, null, 2)}</pre>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default App;
