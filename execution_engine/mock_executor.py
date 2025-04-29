# # execution_engine/mock_executor.py

# def place_order(symbol: str, quantity: float, side: str) -> dict:
#     """
#     Simulates placing an order on an exchange.

#     Args:
#         symbol (str): The trading pair like 'BTCUSDT'.
#         quantity (float): The quantity to buy/sell.
#         side (str): 'BUY' or 'SELL'.

#     Returns:
#         dict: Simulated response of order placement.
#     """
#     print(f"🛒 Simulating {side} order for {quantity} {symbol}...")

#     # Mock response
#     response = {
#         "symbol": symbol,
#         "side": side,
#         "quantity": quantity,
#         "status": "FILLED",  # Assume the order always fills
#         "order_id": 123456,
#         "price": 50000.0,  # Mock price
#         "timestamp": "2025-04-29 10:30:00"
#     }
#     print(f"✅ Mock Order Filled: {response}")
#     return response

# execution_engine/mock_executor.py

class MockExecutor:
    def place_order(self, symbol: str, quantity: float, side: str) -> dict:
        """
        Simulates placing an order on an exchange.
        """
        print(f"🛒 Simulating {side} order for {quantity} {symbol}...")

        response = {
            "symbol": symbol,
            "side": side,
            "quantity": quantity,
            "status": "FILLED",
            "order_id": 123456,
            "price": 50000.0,
            "timestamp": "2025-04-29 10:30:00"
        }

        print(f"✅ Mock Order Filled: {response}")
        return response
