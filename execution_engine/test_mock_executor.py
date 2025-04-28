# execution_engine/test_mock_executor.py

import unittest
from execution_engine.mock_executor import place_order

class TestMockExecutor(unittest.TestCase):

    def test_place_order_success(self):
        symbol = "BTCUSDT"
        quantity = 0.5
        side = "BUY"
        
        response = place_order(symbol, quantity, side)
        
        # Check that response contains expected fields
        self.assertEqual(response["symbol"], symbol)
        self.assertEqual(response["side"], side)
        self.assertEqual(response["quantity"], quantity)
        self.assertEqual(response["status"], "FILLED")
        self.assertIn("order_id", response)
        self.assertIn("price", response)
        self.assertIn("timestamp", response)

    def test_place_order_sell(self):
        symbol = "ETHUSDT"
        quantity = 1.0
        side = "SELL"
        
        response = place_order(symbol, quantity, side)
        
        self.assertEqual(response["side"], "SELL")
        self.assertEqual(response["symbol"], "ETHUSDT")

if __name__ == "__main__":
    unittest.main()
