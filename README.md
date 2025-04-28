# AlphaTrader
Automated Crypto Trading Bot.

# AlphaTrader 🚀
A Python-based crypto trading execution engine using Binance Spot and Futures API.

---

## 📚 Project Structure

AlphaTrader/ 
├── execution_engine/ 
│ 
├── binance_connector.py # Handles signed requests, order management 
│ 
├── init.py 
│ 
├── settings/ 
│ 
├── settings.py # Environment settings (dotenv based) 
│ 
├── main.py # Entry point to test order placement 
│ 
├── .env # Environment variables (private, not uploaded to GitHub) 
├── README.md # Documentation (you are here) 
├── requirements.txt # Project dependencies 
├── venv/ # Virtual environment (excluded in .gitignore)

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