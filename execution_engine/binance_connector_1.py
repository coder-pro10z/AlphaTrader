# execution_engine/binance_connector.py

import requests
import time
import hmac
import hashlib
from config import settings
import urllib.parse

class BinanceConnector:
    """
    Handles connection and authenticated requests to Binance Spot and Futures APIs.
    """

    def __init__(self, account_type="spot"):
        # Initialize session and select account type (spot or futures)
        self.session = requests.Session()

        account_type = account_type.lower()
        if account_type == "spot":
            self.api_key = settings.SPOT_API_KEY
            self.api_secret = settings.SPOT_API_SECRET
            self.base_url = settings.SPOT_BASE_URL
        elif account_type == "futures":
            self.api_key = settings.FUTURES_API_KEY
            self.api_secret = settings.FUTURES_API_SECRET
            self.base_url = settings.FUTURES_BASE_URL
        else:
            raise ValueError("Account type must be either 'spot' or 'futures'.")

    def _sign_payload(self, params):
        """
        Sign parameters using HMAC-SHA256 and your secret key.
        """
        # query_string = "&".join([f"{key}={params[key]}" for key in sorted(params)])
        # signature = hmac.new(
        #     self.api_secret.encode('utf-8'),
        #     query_string.encode('utf-8'),
        #     hashlib.sha256
        # ).hexdigest()
           # 🛠 2. Encode payload exactly as Binance expects
        query_string = urllib.parse.urlencode(sorted(params.items()), doseq=True)

        # 🛠 3. Sign the query_string, NOT dict directly
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()
        params['signature'] = signature
        return params

    def _send_request(self, http_method, endpoint, params=None, signed=False):
        """
        Send HTTP request to Binance API.
        signed=True means the request requires authentication (signature).
        """
        url = self.base_url + endpoint
        headers = {
            'X-MBX-APIKEY': self.api_key
        }
        if params is None:
            params = {}

        # Add timestamp and signature if needed
        if signed:
            params['timestamp'] = int(time.time() * 1000)
            params = self._sign_payload(params)

        try:
            response = self.session.request(
                method=http_method,
                url=url,
                headers=headers,
                params=params
            )
            response.raise_for_status()  # Throws error for 4xx/5xx responses
            if response.text.strip() == "":
                return None
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error: {e} - {response.text}")
            return None
        except ValueError as e:
            print(f"JSON decode error: {e} - Raw response: {response.text}")
            return None

    # Public Methods

    def place_order(self, symbol, side, order_type, quantity, price=None):
        """
        Place a buy or sell order.
        """
        endpoint = "/api/v3/order" if "spot" in self.base_url else "/fapi/v1/order"
        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),        # BUY or SELL
            "type": order_type.upper(),  # LIMIT, MARKET, etc.
            "quantity": quantity
        }
        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good Till Cancelled

        return self._send_request("POST", endpoint, params, signed=True)

    def cancel_order(self, symbol, order_id):
        """
        Cancel an active order.
        """
        endpoint = "/api/v3/order" if "spot" in self.base_url else "/fapi/v1/order"
        params = {
            "symbol": symbol.upper(),
            "orderId": order_id
        }
        return self._send_request("DELETE", endpoint, params, signed=True)

    def get_open_orders(self, symbol):
        """
        Fetch all open orders for a symbol.
        """
        endpoint = "/api/v3/openOrders" if "spot" in self.base_url else "/fapi/v1/openOrders"
        params = {
            "symbol": symbol.upper()
        }
        return self._send_request("GET", endpoint, params, signed=True)
