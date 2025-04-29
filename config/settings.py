from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# General settings
USE_TESTNET = os.getenv("USE_TESTNET", "False").lower() == "true"
DEFAULT_TRADE_SYMBOL = os.getenv("DEFAULT_TRADE_SYMBOL")

# Spot account keys
SPOT_API_KEY = os.getenv("BINANCE_SPOT_API_KEY")
SPOT_API_SECRET = os.getenv("BINANCE_SPOT_API_SECRET")

# Futures account keys
FUTURES_API_KEY = os.getenv("FUTURES_API_KEY")
FUTURES_API_SECRET = os.getenv("FUTURES_API_SECRET")

# Base URLs depending on environment
if USE_TESTNET:
    SPOT_BASE_URL = "https://testnet.binance.vision"
    FUTURES_BASE_URL = "https://testnet.binancefuture.com"
else:
    SPOT_BASE_URL = "https://api.binance.com"
    FUTURES_BASE_URL = "https://fapi.binance.com"
