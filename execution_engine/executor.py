# Execution Engine
import requests
import time
import hmac
import hashlib
from config import settings
import urllib.parse

class BinanceExecutor:
    def __init__(self, account_type="spot"):
        self.account_type = account_type.lower()
        self.session = requests.Session()  # <-- ADD THIS LINE
        if self.account_type == "spot":
            self.api_key = settings.SPOT_API_KEY
            self.api_secret = settings.SPOT_API_SECRET
            self.base_url = settings.SPOT_BASE_URL
        elif self.account_type == "futures":
            self.api_key = settings.FUTURES_API_KEY
            self.api_secret = settings.FUTURES_API_SECRET
            self.base_url = settings.FUTURES_BASE_URL
        else:
            raise ValueError("Account type must be either 'spot' or 'futures'.")

    def _sign_params(self, params):
        query_string = "&".join([f"{key}={params[key]}" for key in sorted(params)])
        signature = hmac.new(
            self.api_secret.encode("utf-8"),
            query_string.encode("utf-8"),
            hashlib.sha256
        ).hexdigest()
        params["signature"] = signature
        return params

    # def _send_signed_request(self, method, endpoint, params):
        # headers = {
        #     "X-MBX-APIKEY": self.api_key
        # }
        # params["timestamp"] = int(time.time() * 1000)
        # params = self._sign_params(params)
        # url = self.base_url + endpoint

        # if method == "POST":
        #     response = requests.post(url, headers=headers, params=params)
        # elif method == "GET":
        #     response = requests.get(url, headers=headers, params=params)
        # elif method == "DELETE":
        #     response = requests.delete(url, headers=headers, params=params)
        # else:
        #     raise ValueError("HTTP method not supported.")

        # return response.json()
    
    # def _send_signed_request(self, http_method, url_path, payload=None):
    #     url = self.base_url + url_path
    #     headers = {
    #         'X-MBX-APIKEY': self.api_key
    #     }
    #     response = self.session.request(http_method, url, headers=headers, params=payload)
    #     # response.raise_for_status()  # will throw exception if status != 200

    #     try:
    #         response.raise_for_status()  # raise HTTPError if 4xx/5xx
    #         if response.text.strip() == "":  # if empty response
    #             return None
    #         return response.json()
    #     except requests.exceptions.HTTPError as e:
    #         print(f"HTTP error occurred: {e} - {response.text}")
    #         return None
    #     except ValueError as e:
    #         print(f"JSON decode failed: {e} - Raw response: {response.text}")
    #         return None

    # def _send_signed_request(self, http_method, url_path, payload=None):
    #     url = self.base_url + url_path
    #     headers = {
    #         'X-MBX-APIKEY': self.api_key
    #     }
        
    #     if payload is None:
    #         payload = {}

    #     # 🛠 FIX: Add timestamp
    #     payload["timestamp"] = int(time.time() * 1000)
        
    #     # 🛠 FIX: Sign payload
    #     payload = self._sign_params(payload)

    #     # Now send the signed request
    #     response = self.session.request(http_method, url, headers=headers, params=payload)

    #     try:
    #         response.raise_for_status()
    #         if response.text.strip() == "":
    #             return None
    #         return response.json()
    #     except requests.exceptions.HTTPError as e:
    #         print(f"HTTP error occurred: {e} - {response.text}")
    #         return None
    #     except ValueError as e:
    #         print(f"JSON decode failed: {e} - Raw response: {response.text}")
    #         return None

    # import urllib.parse

    # def _send_signed_request(self, http_method, url_path, payload=None):
    #     url = self.base_url + url_path
    #     headers = {
    #         'X-MBX-APIKEY': self.api_key
    #     }
        
    #     if payload is None:
    #         payload = {}

    #     payload["timestamp"] = int(time.time() * 1000)
    #     payload = self._sign_params(payload)

    #     query_string = urllib.parse.urlencode(payload, doseq=True)

    #     if http_method == "GET" or http_method == "DELETE":
    #         final_url = url + "?" + query_string
    #         response = self.session.request(http_method, final_url, headers=headers)
    #     else:  # POST
    #         response = self.session.request(http_method, url, headers=headers, params=payload)

    #     try:
    #         response.raise_for_status()
    #         if response.text.strip() == "":
    #             return None
    #         return response.json()
    #     except requests.exceptions.HTTPError as e:
    #         print(f"HTTP error occurred: {e} - {response.text}")
    #         return None
    #     except ValueError as e:
    #         print(f"JSON decode failed: {e} - Raw response: {response.text}")
    #         return None

    # import urllib.parse

    # def _send_signed_request(self, http_method, url_path, payload=None):
    #     url = self.base_url + url_path
    #     headers = {
    #         'X-MBX-APIKEY': self.api_key,
    #         'Content-Type': 'application/x-www-form-urlencoded'
    #     }
        
    #     if payload is None:
    #         payload = {}

    #     payload["timestamp"] = int(time.time() * 1000)
    #     payload = self._sign_params(payload)

    #     query_string = urllib.parse.urlencode(payload, doseq=True)

    #     if http_method == "GET" or http_method == "DELETE":
    #         final_url = url + "?" + query_string
    #         response = self.session.request(http_method, final_url, headers=headers)
    #     elif http_method == "POST":
    #         response = self.session.request(http_method, url, headers=headers, data=query_string)  # POST -> data=query_string
    #     else:
    #         raise ValueError("Invalid HTTP method")

    #     try:
    #         response.raise_for_status()
    #         if response.text.strip() == "":
    #             return None
    #         return response.json()
    #     except requests.exceptions.HTTPError as e:
    #         print(f"HTTP error occurred: {e} - {response.text}")
    #         return None
    #     except ValueError as e:
    #         print(f"JSON decode failed: {e} - Raw response: {response.text}")
    #         return None

    def _send_signed_request(self, http_method, url_path, payload=None):
        url = self.base_url + url_path
        headers = {
            'X-MBX-APIKEY': self.api_key,
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        if payload is None:
            payload = {}

        # 🛠 1. Always add timestamp BEFORE signing
        payload["timestamp"] = int(time.time() * 1000)

        # 🛠 2. Encode payload exactly as Binance expects
        query_string = urllib.parse.urlencode(sorted(payload.items()), doseq=True)

        # 🛠 3. Sign the query_string, NOT dict directly
        signature = hmac.new(
            self.api_secret.encode('utf-8'),
            query_string.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # 🛠 4. Attach signature
        full_query_string = query_string + "&signature=" + signature

        if http_method == "GET" or http_method == "DELETE":
            final_url = url + "?" + full_query_string
            response = self.session.request(http_method, final_url, headers=headers)
        elif http_method == "POST":
            response = self.session.request(http_method, url, headers=headers, data=full_query_string)
        else:
            raise ValueError("Invalid HTTP method")

        try:
            response.raise_for_status()
            if response.text.strip() == "":
                return None
            return response.json()
        except requests.exceptions.HTTPError as e:
            print(f"HTTP error occurred: {e} - {response.text}")
            return None
        except ValueError as e:
            print(f"JSON decode failed: {e} - Raw response: {response.text}")
            return None

    def place_order(self, symbol, side, order_type, quantity, price=None):
        endpoint = "/api/v3/order" if self.account_type == "spot" else "/fapi/v1/order"

        params = {
            "symbol": symbol.upper(),
            "side": side.upper(),  # BUY or SELL
            "type": order_type.upper(),  # LIMIT, MARKET, etc.
            "quantity": quantity
        }
        if order_type.upper() == "LIMIT":
            params["price"] = price
            params["timeInForce"] = "GTC"

        return self._send_signed_request("POST", endpoint, params)

    def cancel_order(self, symbol, order_id):
        endpoint = "/api/v3/order" if self.account_type == "spot" else "/fapi/v1/order"

        params = {
            "symbol": symbol.upper(),
            "orderId": order_id
        }

        return self._send_signed_request("DELETE", endpoint, params)

    def get_open_orders(self, symbol):
        endpoint = "/api/v3/openOrders" if self.account_type == "spot" else "/fapi/v1/openOrders"

        params = {
            "symbol": symbol.upper()
        }

        return self._send_signed_request("GET", endpoint, params)

