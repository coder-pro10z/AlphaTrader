# Unit test for paper_trading too
import os
import json
from datetime import datetime
from utils.logger import log_trade
from datetime import datetime, timezone


class PaperTradingEngine:
    def __init__(self, starting_balance=1000.0, symbol="btcusdt"):
        self.balance = starting_balance
        self.symbol = symbol.lower()
        self.position = 0.0
        self.entry_price = 0.0
        self.trade_log_path = "logs/paper_trades.json"
        os.makedirs("logs", exist_ok=True)
        self._init_trade_log()

    def _init_trade_log(self):
        if not os.path.exists(self.trade_log_path):
            with open(self.trade_log_path, "w") as f:
                json.dump([], f)

    def _record_trade(self, trade):
        with open(self.trade_log_path, "r+") as f:
            data = json.load(f)
            data.append(trade)
            f.seek(0)
            json.dump(data, f, indent=4)

    def place_order(self, side, price, quantity):
        """
        Simulate a BUY or SELL order.
        """
        timestamp = datetime.now(timezone.utc).isoformat()

        # timestamp = datetime.utcnow().isoformat()
        price = float(price)
        quantity = float(quantity)

        if side.upper() == "BUY":
            cost = price * quantity
            if cost > self.balance:
                print(f"⚠️ Insufficient balance to buy {quantity} {self.symbol}")
                return
            self.balance -= cost
            self.position += quantity
            self.entry_price = price
        elif side.upper() == "SELL":
            if quantity > self.position:
                print(f"⚠️ Not enough position to sell {quantity} {self.symbol}")
                return
            revenue = price * quantity
            self.balance += revenue
            self.position -= quantity
        else:
            print(f"❌ Invalid trade side: {side}")
            return

        # Log to file + console
        trade = {
            "time": timestamp,
            "side": side,
            "symbol": self.symbol,
            "price": price,
            "quantity": quantity,
            "balance": round(self.balance, 2),
            "position": round(self.position, 4),
        }
        log_trade(side, self.symbol, price, quantity)
        self._record_trade(trade)
        print(
            f"[PAPER TRADE] {side} {quantity} {self.symbol} @ {price:.2f} | Balance: {self.balance:.2f}"
        )

    def get_status(self):
        return {
            "balance": round(self.balance, 2),
            "position": round(self.position, 4),
            "entry_price": round(self.entry_price, 2),
        }
