# 🚀 JarNox Algo Trading Dashboard

**JarNox** is an end-to-end algorithmic trading dashboard that demonstrates data-driven strategy design, quantitative analysis, and full-stack deployment. It integrates a **Flask + Python backend** for data collection and backtesting with a **React + Plotly frontend** for real-time visualization.

<img width="1384" height="878" alt="Screenshot 2025-11-04 at 9 12 10 PM" src="https://github.com/user-attachments/assets/f697277e-1d99-44a9-9d03-0445d4424d68" />
<img width="1373" height="525" alt="Screenshot 2025-11-04 at 9 12 21 PM" src="https://github.com/user-attachments/assets/3d048ec2-2449-4506-9ec8-75f4dad83fed" />
<img width="1373" height="310" alt="Screenshot 2025-11-04 at 9 12 29 PM" src="https://github.com/user-attachments/assets/68b159e5-724a-4556-9a20-2f0aeed1ded6" />





---

## 📈 Project Overview

JarNox allows users to:
- **Run backtests** for any stock ticker and date range using live market data via **Yahoo Finance** (`yfinance`)
- **Visualize** price movements, SMA crossovers, RSI signals, and buy/sell triggers
- **View** equity curve evolution and key performance metrics (PnL, trade count, ROI)
- **Experience** seamless communication between backend APIs and a responsive React dashboard

---

## 🧠 Approach & Architecture

### Backend (Flask)
- **Data ingestion** using `yfinance` for real-time market data
- **Signal generation** with `ta` and `pandas` for technical analysis
- **Portfolio simulation** with SMA + RSI hybrid trading strategy
- **REST API endpoints** that feed structured JSON responses to the dashboard

### Frontend (React + Plotly)
- **Real-time charting** with responsive graphs and animated transitions
- **Clean UI** built with TailwindCSS, emphasizing readability and performance metrics
- **Interactive visualizations** using Plotly.js for time-series data

---

## ⚙️ Tech Stack

**Backend:**
- Python 3.10+
- Flask (REST API)
- Pandas (Data manipulation)
- TA-Lib / ta (Technical indicators)
- YFinance (Market data)

**Frontend:**
- React 18+
- Plotly.js (Interactive charts)
- TailwindCSS (Styling)
- Axios (HTTP client)

**Tools:**
- Conda (Environment management)
- Node.js & npm
- Git version control

**Deployment:**
- Local development via `run-all.sh`
- Cloud-ready architecture

---

## 📁 Project Structure

```
jarnox_algo_trader/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── backtest.py           # Backtesting engine
│   ├── data_feed.py          # Data ingestion module
│   ├── indicators.py         # Technical indicators
│   ├── strategies.py         # Trading strategies
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── public/               # Static assets
│   ├── src/
│   │   ├── App.js           # Main React component
│   │   ├── App.css          # Styling
│   │   └── index.js         # Entry point
│   ├── package.json         # Node dependencies
│   └── .gitignore
├── run-all.sh               # Auto-launch script
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Node.js 16+ and npm
- Conda (recommended)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/heyShreyansh/JarNox-AlgoTrader.git
cd JarNox-AlgoTrader
```

2. **Set up Python environment**
```bash
# Create conda environment
conda create -n jarnox python=3.10
conda activate jarnox

# Install Python dependencies
pip install -r requirements.txt
```

3. **Set up React frontend**
```bash
cd frontend
npm install
cd ..
```

### Running the Application

#### Option 1: Using the launch script (Recommended)
```bash
chmod +x run-all.sh
./run-all.sh
```

#### Option 2: Manual launch

**Terminal 1 - Backend:**
```bash
conda activate jarnox
python app.py
```

**Terminal 2 - Frontend:**
```bash
cd frontend
npm start
```

The application will be available at:
- **Frontend:** http://localhost:3000
- **Backend API:** http://localhost:5000

---

## 🎯 Features

### Backtesting Engine
- Fetch historical market data for any ticker symbol
- Implement SMA (Simple Moving Average) and RSI (Relative Strength Index) indicators
- Generate buy/sell signals based on technical analysis
- Track portfolio performance with detailed metrics

### Visualization Dashboard
- Interactive candlestick/line charts with Plotly
- Real-time indicator overlays (SMA, RSI)
- Buy/sell signal markers on price charts
- Equity curve and drawdown analysis
- Performance metrics display (Total PnL, ROI, Win Rate)

### REST API Endpoints
```
GET  /api/backtest?ticker=AAPL&start_date=2023-01-01&end_date=2024-01-01
POST /api/strategy
GET  /api/indicators
```

---

## 🧩 Challenges & Learnings

Building JarNox highlighted the gap between algorithm design and production-ready architecture.

**Data Normalization:** The biggest challenge was ensuring downloaded stock data remained consistent across pandas versions. Ambiguous Series issues surfaced during signal generation, forcing deep debugging into pandas' internal logic. This refined understanding of data integrity and shape enforcement, crucial in any ML/quant pipeline.

**Communication Layer:** Designing the communication between Flask and React without blocking or race conditions required careful attention. Asynchronous `fetch()` handling, CORS management, and data serialization became practical lessons in clean API design.

**UI Performance:** On the UI side, crafting a dashboard that balanced performance with interactivity involved learning how Plotly.js handles large time-series efficiently. Optimizing re-renders and chart updates was essential for a smooth user experience.

**Key Takeaways:**
- Stronger command over Python's data-handling ecosystem
- Flask deployment pipelines and REST API design
- Frontend reactivity and state management patterns
- Real-world debugging and iteration strategies

The result — JarNox — isn't just a trading demo, but a showcase of **quantitative reasoning, full-stack integration, and code clarity** under pressure. Every error log became a debugging case study — proof that engineering progress thrives on iteration, not perfection.

---

## 📊 Example Usage

1. **Select a stock ticker** (e.g., AAPL, GOOGL, TSLA)
2. **Choose date range** for backtesting
3. **View results:**
   - Price chart with SMA lines
   - RSI indicator subplot
   - Buy/sell signals marked on chart
   - Performance metrics and equity curve

---

## 🛠️ Configuration

Edit `app.py` to modify:
- Default port settings
- CORS configurations
- Strategy parameters

Edit `strategies.py` to:
- Adjust SMA periods (default: 20, 50)
- Modify RSI thresholds (default: 30, 70)
- Implement custom trading strategies

---

## 📝 API Documentation

### Backtest Endpoint
```http
GET /api/backtest
```

**Query Parameters:**
- `ticker` (string, required): Stock symbol
- `start_date` (string, required): Format YYYY-MM-DD
- `end_date` (string, required): Format YYYY-MM-DD

**Response:**
```json
{
  "ticker": "AAPL",
  "data": [...],
  "signals": [...],
  "performance": {
    "total_return": 15.23,
    "trades": 45,
    "win_rate": 0.67
  }
}
```

---

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

## 👤 Author

**Shreyansh**
- GitHub: [@heyShreyansh](https://github.com/heyShreyansh)

---

## 🙏 Acknowledgments

- Yahoo Finance API for market data
- Plotly.js for interactive visualizations
- React and Flask communities for excellent documentation

---

## 📧 Contact

For questions or feedback, please open an issue on GitHub or reach out via email.

---

**⭐ If you found this project helpful, please consider giving it a star!**
