# AlphaTrader
Automated Crypto Trading Bot.

# AlphaTrader 🚀
A Python-based crypto trading execution engine using Binance Spot and Futures API.

---

## 📚 Project Structure

AlphaTrader/ 
 │ 
 ├── config/ # Configurations (API keys, environment) 
 ├── data_collector/ # Real-time market data fetcher
 ├── indicators/ # Technical indicator calculations 
 ├── strategies/ # Trading strategies (scalping, trend-following, etc.) 
 ├── regime_detector/ # Market regime detection (trend or range) 
 ├── execution_engine/ # Order execution engine 
 ├── risk_manager/ # Risk controls 
 ├── ui/ # Streamlit dashboard 
 ├── utils/ # Utility functions like logger 
 ├── backtester/ # Historical strategy backtesting (future) 
 ├── venv/ # Virtual environment (excluded from Git) 
 │ 
 ├── main.py # Project entry point 
 ├── requirements.txt # Project dependencies 
 ├── README.md # Project documentation
---

## ⚙️ Architecture Overview

- **Environment Loader**: `settings.py` loads `.env` variables (keys, secrets, URLs).
- **Connector Class**: `BinanceConnector` in `binance_connector.py` manages:
  - Signing requests (HMAC SHA256)
  - Sending retries with timeout
  - Spot and Futures API separation
  - Placing, cancelling, querying orders
- **Execution Entry**: `main.py` calls `BinanceConnector.place_order()` etc.

---

## 🧩 Workflow

1. Load environment variables (API keys) using `dotenv`.
2. Initialize `BinanceConnector` with `account_type` (either `"spot"` or `"futures"`).
3. Use `place_order()`, `cancel_order()`, `get_open_orders()` methods to interact with Binance API securely.
4. Retry failed requests automatically (max 3 retries with 1s delay).
5. Handle network issues like timeout, HTTP errors safely.

---
---

## 🏗️ Core Components

- **Configuration Management**: Safely load API keys and settings
- **Data Collection**: Fetch OHLCV data in real-time
- **Indicators**: Compute TA indicators using pandas-ta / TA-Lib
- **Strategies**: Modular strategies (easy to add new ones)
- **Execution Engine**: Robust, retriable order placement/cancellation
- **Risk Manager**: Position sizing and risk control logic
- **UI Dashboard**: Web interface using Streamlit
- **Logger**: Centralized logging and error handling
- **Backtester** *(coming soon)*: Historical simulation

---

## 📚 Libraries Used

- `ccxt`
- `pandas`
- `pandas-ta`
- `TA-Lib`
- `apscheduler`
- `fastapi`
- `streamlit`
- `requests`
- `dotenv`
- `logging`
- `hmac`, `hashlib`, `time`, `os`, `urllib`

---

## 🚀 Installation

```bash
git clone https://github.com/your-username/AlphaTrader.git
cd AlphaTrader

# Setup virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS
# or
venv\Scripts\activate     # Windows

# Install requirements
pip install -r requirements.txt

## 🚀 Current Progress

| Task                             | Status  |
|---------------------------------- |---------|
| Basic project setup              | ✅ Done |
| .env loading via `dotenv`         | ✅ Done |
| Spot and Futures separation       | ✅ Done |
| Signing and sending secured API requests | ✅ Done |
| Retry mechanism for failed requests | ✅ Done |
| Order placement / cancellation    | ✅ Done |
| Proper error handling (HTTPError, RequestException) | ✅ Done |
| Extensive code comments           | ✅ Done |
| Project structure documentation   | 🚧 In Progress |
| Testing different API endpoints   | 🚧 In Progress |
| Logging system for API calls       | ❌ Not Started |
| Add unit tests (pytest)           | ❌ Not Started |

---

## 🔥 Setup Instructions

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/AlphaTrader.git
   cd AlphaTrader

How BinnanceConnector flow works?

BinanceConnector
  |
  |--> place_order() 
  |--> cancel_order()
  |--> get_open_orders()
         |
         --> _send_request() 
                 |
                 --> _sign_payload() (if needed)

Project Updated Structure

AlphaTrader/
  backtester/
    test_scalping.py
  config/
    settings.py
  data_collector/
    fetch_data.py
  execution_engine/
    executor.py
    mock_executor.py
    test_mock_executor.py
  indicators/
    technicals.py
  risk_manager/
    risk_control.py
  strategies/
    scalping.py
  ui/
    dashboard.py
  utils/
    logger.py
  main.py
  README.md
  requirements.txt
