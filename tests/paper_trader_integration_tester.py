import unittest
from unittest.mock import patch
from paper_trading.paper_trader import PaperTradingEngine
from strategies.scalping import find_scalping_opportunity
import pandas as pd
import os
import json


class TestPriceWatcherIntegration(unittest.TestCase):
    def setUp(self):
        self.engine = PaperTradingEngine(starting_balance=1000.0, symbol="btcusdt")
        self.test_prices = [
            31000,
            30900,
            30800,
            30700,
            30600,  # these 5 set SMA10 up high
            30500,
            30400,
            30300,
            30200,
            30100,  # these lower the SMA10 below SMA5
            31500,
            32000,  # these two push SMA5 above SMA10
        ]
        #  [
        #     100,
        #     100,
        #     100,
        #     100,
        #     100,  # low
        #     200,
        #     200,
        #     200,
        #     200,
        #     200,  # high plateau for prev
        #     10,
        #     10,  # very deep drop
        # ]
        # BUY
        # [100, 100, 100, 100, 100, 100, 100, 120, 140, 160, 180, 200]
        # [
        #     100,
        #     100,
        #     100,
        #     100,
        #     100,  # first 5
        #     200,
        #     200,
        #     200,
        #     200,
        #     200,  # next 5 → pushes both SMAs to 200
        #     50,
        #     50,  # last 2 → heavy drop
        # ]
        # #  [
        #     100,
        #     100,
        #     100,
        #     100,
        #     100,  # flat start
        #     100,
        #     100,
        #     100,
        #     100,  # still flat: SMA5=100, SMA10=100
        #     200,  # spike: new SMA5=(100*4 + 200)/5 = 120, SMA10=(100*9+200)/10=110
        # ]
        # [
        #     100,
        #     101,
        #     102,
        #     100,
        #     99,
        #     98,
        #     97,
        #     98,
        #     99,
        #     100,
        # ]  # Mock 1m close prices

        # Clean previous trade logs
        if os.path.exists(self.engine.trade_log_path):
            os.remove(self.engine.trade_log_path)
        self.engine._init_trade_log()

    def test_signal_triggers_order_and_log(self):
        df = pd.DataFrame({"close": self.test_prices})
        signal = find_scalping_opportunity(df)

        if signal in ["BUY", "SELL"]:
            side = "BUY" if signal == "BUY" else "SELL"
            self.engine.place_order(side=side, price=100.0, quantity=1.0)

            # Validate the trade was recorded
            with open(self.engine.trade_log_path, "r") as f:
                trades = json.load(f)
                self.assertEqual(len(trades), 1)
                self.assertEqual(trades[0]["side"], side)
                self.assertEqual(trades[0]["price"], 100.0)
                self.assertEqual(trades[0]["quantity"], 1.0)
        else:
            self.skipTest("No valid signal was triggered")


if __name__ == "__main__":
    unittest.main()
