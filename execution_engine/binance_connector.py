# Standard libraries
import time
import hmac
import hashlib
import random
import urllib.parse

# Third-party libraries
import requests
from urllib.parse import urlencode
from requests.exceptions import ConnectionError, Timeout, HTTPError, RequestException

# Internal imports
from config import settings  # Assuming you have settings.py ready

# BinanceConnector class handles interaction with Binance API (Spot and Futures)
class BinanceConnector:
    def __init__(self, account_type="spot"):
        # Initialize the connector with the specified account type (default: spot)
        self.account_type = account_type.lower()  # Account type could be 'spot' or 'futures'
        self.session = requests.Session()  # Create a session for making HTTP requests

        # Set max retries and delay settings (✅ NEW!)
        self.max_retries = 3         # Number of retries before giving up
        self.retry_delay = 1          # Delay between retries in seconds
        self.timeout = 10            # Timeout for API requests (in seconds)

        
        # Set API keys and base URLs based on account type
        if self.account_type == "spot":
            self.api_key = settings.SPOT_API_KEY
            self.api_secret = settings.SPOT_API_SECRET
            self.base_url = settings.SPOT_BASE_URL
        elif self.account_type == "futures":
            self.api_key = settings.FUTURES_API_KEY
            self.api_secret = settings.FUTURES_API_SECRET
            self.base_url = settings.FUTURES_BASE_URL
        else:
            # If account type is invalid, raise an error
            raise ValueError("Account type must be either 'spot' or 'futures'.")

    def _sign_params(self, params):
        # This method generates a signature for the API request
        query_string = "&".join([f"{key}={params[key]}" for key in sorted(params)])  # Sort and join params
        signature = hmac.new(
            self.api_secret.encode("utf-8"),  # Create HMAC using the API secret
            query_string.encode("utf-8"),  # Create HMAC with the query string
            hashlib.sha256  # Use SHA256 as the hash function
        ).hexdigest()  # Return the hex-encoded HMAC
        params["signature"] = signature  # Add the signature to the parameters
        return params  # Return the signed parameters

    # def _send_signed_request(self, http_method, url_path, payload=None):
    #     # This method sends a signed request to the Binance API
    #     url = self.base_url + url_path  # Construct the full URL for the API endpoint
    #     headers = {
    #         'X-MBX-APIKEY': self.api_key,  # Add the API key to headers for authentication
    #         'Content-Type': 'application/x-www-form-urlencoded'  # Set content type for POST requests
    #     }

    #     if payload is None:
    #         payload = {}

    #     # 🛠 Add timestamp before signing the request to avoid timing issues
    #     payload["timestamp"] = int(time.time() * 1000)  # Current timestamp in milliseconds

    #     # 🛠 Encode the payload parameters to match Binance's expected format
    #     query_string = urllib.parse.urlencode(sorted(payload.items()), doseq=True)

    #     # 🛠 Sign the encoded query string with HMAC SHA256
    #     signature = hmac.new(
    #         self.api_secret.encode('utf-8'),
    #         query_string.encode('utf-8'),
    #         hashlib.sha256
    #     ).hexdigest()  # Hex-encoded signature

    #     # 🛠 Append the signature to the query string
    #     full_query_string = query_string + "&signature=" + signature

    #     # Send the HTTP request (GET, POST, DELETE) with the correct method
    #     if http_method == "GET" or http_method == "DELETE":
    #         final_url = url + "?" + full_query_string  # For GET/DELETE, append query string to URL
    #         response = self.session.request(http_method, final_url, headers=headers)  # Send request
    #     elif http_method == "POST":
    #         response = self.session.request(http_method, url, headers=headers, data=full_query_string)  # For POST, send the data
    #     else:
    #         raise ValueError("Invalid HTTP method")  # Raise an error if an invalid method is provided

    #     try:
    #         response.raise_for_status()  # Check if the request was successful
    #         if response.text.strip() == "":  # If the response is empty, return None
    #             return None
    #         return response.json()  # Return the JSON response if available
    #     except requests.exceptions.HTTPError as e:
    #         # If an HTTP error occurs, print the error and return None
    #         print(f"HTTP error occurred: {e} - {response.text}")
    #         return None
    #     except ValueError as e:
    #         # If JSON decoding fails, print the error and return None
    #         print(f"JSON decode failed: {e} - Raw response: {response.text}")
    #         return None

    def _send_signed_request(self, http_method, url_path, payload=None):
        # Combine base URL with the specific endpoint path
        url = self.base_url + url_path

        # Prepare the request headers required by Binance API
        headers = {
            'X-MBX-APIKEY': self.api_key,  # Your API key for authentication
            'Content-Type': 'application/x-www-form-urlencoded'  # Specify the content type
        }

        # If no payload is given, initialize an empty one
        if payload is None:
            payload = {}

        # 🛠 Step 1: Add timestamp to the payload (required by Binance)
        payload["timestamp"] = int(time.time() * 1000)  # Current time in milliseconds

        # 🛠 Step 2: Properly encode all parameters (sorted order)
        query_string = urlencode(sorted(payload.items()), doseq=True)

        # 🛠 Step 3: Sign the encoded query string using HMAC SHA256
        signature = hmac.new(
            self.api_secret.encode('utf-8'),   # API Secret as key
            query_string.encode('utf-8'),       # Message to hash
            hashlib.sha256                     # Hashing algorithm
        ).hexdigest()  # Return a hex-encoded signature

        # 🛠 Step 4: Attach signature to the final query string
        full_query_string = query_string + "&signature=" + signature

        # Now ready to send the request...
        
        # 🛡 Implement Retry Logic (for network issues)
        for attempt in range(1, self.max_retries + 1):
            try:
                # 🛠 Step 5: Send request according to the HTTP method
                if http_method in ["GET", "DELETE"]:
                    final_url = url + "?" + full_query_string  # Attach parameters to URL
                    response = self.session.request(
                        method=http_method,
                        url=final_url,
                        headers=headers,
                        timeout=self.timeout  # Max seconds to wait for a response
                    )
                elif http_method == "POST":
                    response = self.session.request(
                        method=http_method,
                        url=url,
                        headers=headers,
                        data=full_query_string,  # Attach parameters in POST body
                        timeout=self.timeout
                    )
                else:
                    # 🚫 If invalid HTTP method, stop immediately
                    raise ValueError("Invalid HTTP method")

                # 🛠 Step 6: Check if server responded with HTTP error (4xx, 5xx)
                response.raise_for_status()  # Will raise HTTPError if status != 2xx

                # 🛠 Step 7: If response body is empty, return None
                if response.text.strip() == "":
                    return None

                # 🛠 Step 8: If everything is fine, return parsed JSON
                return response.json()

            except (ConnectionError, Timeout) as e:
                # 🛡 Handle network errors (e.g., server down, no internet)
                print(f"[Attempt {attempt}] Network error: {e}. Retrying...")
                time.sleep(2 ** attempt + random.uniform(0, 1))  
                # Wait longer after each retry (Exponential backoff + slight randomness)

            except HTTPError as e:
                # 🛡 Handle HTTP error responses (e.g., 400 Bad Request, 401 Unauthorized)
                print(f"[Attempt {attempt}] HTTP error: {e} - {response.text}")
                return None  # After HTTP error, do not retry blindly

            except RequestException as e:
                # 🛡 Catch any other Request-related exceptions
                print(f"[Attempt {attempt}] Unexpected error: {e}")
                return None

            except ValueError as e:
                # 🛡 Handle JSON decoding errors if Binance returns non-JSON
                print(f"[Attempt {attempt}] JSON decode failed: {e} - Raw response: {response.text}")
                return None

        # After all retries failed
        print("All retry attempts failed.")
        return None


    def place_order(self, symbol, side, order_type, quantity, price=None):
        # Place an order on Binance (either Spot or Futures)
        endpoint = "/api/v3/order" if self.account_type == "spot" else "/fapi/v1/order"  # Choose endpoint based on account type

        params = {
            "symbol": symbol.upper(),  # Convert symbol (e.g., BTCUSDT) to uppercase
            "side": side.upper(),  # Convert side to uppercase (BUY or SELL)
            "type": order_type.upper(),  # Convert order type to uppercase (LIMIT, MARKET, etc.)
            "quantity": quantity  # Quantity to buy or sell
        }
        if order_type.upper() == "LIMIT":  # If order type is LIMIT, include price and timeInForce
            params["price"] = price
            params["timeInForce"] = "GTC"  # Good till canceled

        # Send signed request to place the order and return the response
        return self._send_signed_request("POST", endpoint, params)

    def cancel_order(self, symbol, order_id):
        # Cancel an existing order on Binance
        endpoint = "/api/v3/order" if self.account_type == "spot" else "/fapi/v1/order"  # Choose endpoint based on account type

        params = {
            "symbol": symbol.upper(),  # Convert symbol to uppercase
            "orderId": order_id  # Order ID to cancel
        }

        # Send signed request to cancel the order and return the response
        return self._send_signed_request("DELETE", endpoint, params)

    def get_open_orders(self, symbol):
        # Get all open orders for a specific symbol
        endpoint = "/api/v3/openOrders" if self.account_type == "spot" else "/fapi/v1/openOrders"  # Choose endpoint based on account type

        params = {
            "symbol": symbol.upper()  # Convert symbol to uppercase
        }

        # Send signed request to get open orders and return the response
        return self._send_signed_request("GET", endpoint, params)
