from flask import Flask, render_template_string, jsonify, request
from flask_cors import CORS
from data_feed import fetch_historical
from backtest import run_backtest

app = Flask(__name__)
CORS(app)

INDEX_HTML = """
<!doctype html>
<html>
<head>
<title>JarNox - Algo Trading Dashboard</title>
<style>
body { font-family: Arial, sans-serif; max-width: 1200px; margin: 40px auto; padding: 20px; background: #f5f5f5; }
h2 { color: #333; }
.status { padding: 20px; background: white; border-radius: 8px; margin: 20px 0; }
</style>
</head>
<body>
<h2>🚀 JarNox Backend API</h2>
<div class="status">
  <p>✅ Backend is running!</p>
  <p><strong>Endpoints:</strong></p>
  <ul>
    <li>GET <code>/</code> - This page</li>
    <li>GET <code>/backtest?ticker=AAPL&start=2023-01-01&end=2024-12-31</code> - Run backtest</li>
  </ul>
  <p><strong>React Dashboard:</strong> <a href="http://localhost:3000" target="_blank">http://localhost:3000</a></p>
</div>
</body>
</html>
"""

@app.route('/')
def index():
    return render_template_string(INDEX_HTML)

@app.route('/backtest')
def backtest_route():
    try:
        ticker = request.args.get('ticker', 'AAPL')
        start = request.args.get('start', '2023-01-01')
        end = request.args.get('end', '2024-12-31')
        result = run_backtest(ticker, start, end)
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='127.0.0.1', port=5000)
