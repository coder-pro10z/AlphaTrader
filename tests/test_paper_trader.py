import unittest
import os
import json

# from execution_engine.paper_trading_engine import PaperTradingEngine
from paper_trading.paper_trader import PaperTradingEngine


class TestPaperTradingEngine(unittest.TestCase):
    def setUp(self):
        self.engine = PaperTradingEngine(starting_balance=1000.0, symbol="btcusdt")
        self.test_log_path = self.engine.trade_log_path
        # Reset trade log before each test
        with open(self.test_log_path, "w") as f:
            json.dump([], f)

    def test_initial_status(self):
        status = self.engine.get_status()
        self.assertEqual(status["balance"], 1000.0)
        self.assertEqual(status["position"], 0.0)
        self.assertEqual(status["entry_price"], 0.0)

    def test_buy_order(self):
        self.engine.place_order("BUY", price=500.0, quantity=1)
        status = self.engine.get_status()
        self.assertEqual(status["position"], 1.0)
        self.assertEqual(status["balance"], 500.0)
        self.assertEqual(status["entry_price"], 500.0)

    # def test_sell_order(self):
    #     self.engine.place_order("BUY", price=200.0, quantity=2)
    #     self.engine.place_order("SELL", price=300.0, quantity=1)
    #     status = self.engine.get_status()
    #     self.assertEqual(status["position"], 1.0)
    #     self.assertEqual(status["balance"], 1000.0)  # 600 spent, 300 earned → net 1000
    #     self.assertEqual(status["entry_price"], 200.0)

    def test_sell_order(self):
        self.engine.place_order("BUY", 200, 2.0)
        self.engine.place_order("SELL", 300, 1.0)
        status = self.engine.get_status()
        self.assertEqual(status["balance"], 900.0)  # Corrected balance
        self.assertEqual(status["position"], 1.0)  # One BTC left

    def test_insufficient_balance(self):
        self.engine.place_order("BUY", price=2000.0, quantity=1)
        status = self.engine.get_status()
        self.assertEqual(status["position"], 0.0)
        self.assertEqual(status["balance"], 1000.0)

    def test_oversell(self):
        self.engine.place_order("BUY", price=100.0, quantity=1)
        self.engine.place_order("SELL", price=100.0, quantity=2)  # Should fail
        status = self.engine.get_status()
        self.assertEqual(status["position"], 1.0)
        self.assertEqual(status["balance"], 900.0)

    def test_trade_logging(self):
        self.engine.place_order("BUY", price=100.0, quantity=1)
        with open(self.test_log_path, "r") as f:
            data = json.load(f)
        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["side"], "BUY")
        self.assertEqual(data[0]["price"], 100.0)


if __name__ == "__main__":
    unittest.main()
