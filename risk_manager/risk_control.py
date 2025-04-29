# Risk Management

# def check_risk():
#     pass
# risk_manager/risk_control.py

# Simple risk management: approve or reject trades based on dummy rules
# def check_risk(symbol: str, quantity: float, signal: str) -> bool:
#     """
#     Check whether a trade can be placed based on risk rules.
    
#     Args:
#         symbol (str): Trading pair like 'BTCUSDT'.
#         quantity (float): Amount of crypto to buy/sell.
#         signal (str): 'BUY' or 'SELL'

#     Returns:
#         bool: True if trade is allowed, False otherwise.
#     """

#     # Example simple rules
#     MAX_QUANTITY = 0.5  # max quantity per trade
#     ALLOWED_SYMBOLS = {"BTCUSDT", "ETHUSDT"}  # Only allow these symbols

#     if signal not in {"BUY", "SELL"}:
#         print(f"❌ Signal {signal} is invalid.")
#         return False

#     if quantity > MAX_QUANTITY:
#         print(f"❌ Quantity {quantity} exceeds max limit.")
#         return False

#     if symbol not in ALLOWED_SYMBOLS:
#         print(f"❌ Symbol {symbol} is not allowed.")
#         return False

#     print(f"✅ Risk Check Passed for {signal} {quantity} {symbol}")
#     return True

# risk_manager/risk_control.py

# MAX_TRADES_PER_DAY = 5
# MAX_LOSS_PER_TRADE = 100  # in USD

# trade_count = 0  # simple counter
# daily_loss = 0  # simple tracking

# def check_risk(symbol: str, quantity: float, signal: str, price: float = 50000) -> bool:
#     """
#     Risk manager for approving trades.

#     Args:
#         symbol (str): Trading pair.
#         quantity (float): Amount to trade.
#         signal (str): 'BUY' or 'SELL'.
#         price (float): Current price (for loss calculation).

#     Returns:
#         bool: True if trade is allowed, False otherwise.
#     """
#     global trade_count, daily_loss

#     if trade_count >= MAX_TRADES_PER_DAY:
#         print("🛑 Max trades per day reached.")
#         return False

#     # Estimate hypothetical loss
#     estimated_loss = quantity * price * 0.01  # Assume 1% slippage risk

#     if estimated_loss > MAX_LOSS_PER_TRADE:
#         print(f"🛑 Risk too high! Estimated loss ${estimated_loss:.2f} exceeds limit.")
#         return False

#     print(f"✅ Risk Check Passed for {signal} {quantity} {symbol}")
#     trade_count += 1
#     daily_loss += estimated_loss
#     return True

# def reset_daily_limits():
#     global trade_count, daily_loss
#     trade_count = 0
#     daily_loss = 0

# risk_manager/risk_control.py

# class RiskManager:
#     """
#     A simple Risk Manager class to control maximum trades and losses per day.
#     """

#     MAX_TRADES_PER_DAY = 5
#     MAX_LOSS_PER_TRADE = 100  # in USD

#     def __init__(self):
#         # Initialize counters for daily trade tracking
#         self.trade_count = 0
#         self.daily_loss = 0

#     def check_risk(self, symbol: str, quantity: float, signal: str, price: float = 50000) -> bool:
#         """
#         Risk manager for approving trades.

#         Args:
#             symbol (str): Trading pair.
#             quantity (float): Amount to trade.
#             signal (str): 'BUY' or 'SELL'.
#             price (float): Current price (for loss calculation).

#         Returns:
#             bool: True if trade is allowed, False otherwise.
#         """
#         if self.trade_count >= self.MAX_TRADES_PER_DAY:
#             print("🛑 Max trades per day reached.")
#             return False

#         # Estimate hypothetical loss
#         estimated_loss = quantity * price * 0.01  # Assume 1% slippage risk

#         if estimated_loss > self.MAX_LOSS_PER_TRADE:
#             print(f"🛑 Risk too high! Estimated loss ${estimated_loss:.2f} exceeds limit.")
#             return False

#         print(f"✅ Risk Check Passed for {signal} {quantity} {symbol}")
#         self.trade_count += 1
#         self.daily_loss += estimated_loss
#         return True

#     def reset_daily_limits(self):
#         """
#         Reset daily counters — should be called at the start of a new trading day.
#         """
#         self.trade_count = 0
#         self.daily_loss = 0

# risk_manager/risk_control.py

# class RiskManager:
#     """
#     A Risk Manager class that monitors daily trading limits and losses.
#     """

#     def __init__(self, max_daily_loss=100, max_trades_per_day=5):
#         """
#         Initialize the Risk Manager.

#         Args:
#             max_daily_loss (float): Maximum allowable loss per day in USD.
#             max_trades_per_day (int): Maximum number of trades allowed per day.
#         """
#         self.max_daily_loss = max_daily_loss
#         self.max_trades_per_day = max_trades_per_day
#         self.daily_loss = 0
#         self.trade_count = 0

#     def can_place_trade(self) -> bool:
#         """
#         Check if a new trade can be placed based on daily limits.

#         Returns:
#             bool: True if allowed, False otherwise.
#         """
#         if self.trade_count >= self.max_trades_per_day:
#             print("🛑 Max trades per day reached.")
#             return False
#         if self.daily_loss <= -self.max_daily_loss:
#             print("🛑 Max daily loss limit reached.")
#             return False
#         return True

#     def update_after_trade(self, pnl: float):
#         """
#         Update counters after a trade is completed.

#         Args:
#             pnl (float): Profit or Loss from the trade (positive or negative).
#         """
#         self.trade_count += 1
#         self.daily_loss += pnl
#         print(f"📊 Updated Risk Manager: Trades={self.trade_count}, Daily PnL=${self.daily_loss:.2f}")

#     def reset_daily_limits(self):
#         """
#         Reset daily counters — should be called at the start of a new trading day.
#         """
#         self.trade_count = 0
#         self.daily_loss = 0
#         print("🔄 Daily risk limits reset.")

import json
import os

class RiskManager:
    def __init__(self, max_daily_loss=100, max_trades_per_day=5, state_file="risk_state.json"):
        self.max_daily_loss = max_daily_loss
        self.max_trades_per_day = max_trades_per_day
        self.state_file = state_file
        self.trade_count = 0
        self.daily_loss = 0
        self._load_state()

    def _load_state(self):
        if os.path.exists(self.state_file):
            with open(self.state_file, "r") as f:
                state = json.load(f)
                self.trade_count = state.get("trade_count", 0)
                self.daily_loss = state.get("daily_loss", 0)

    def _save_state(self):
        with open(self.state_file, "w") as f:
            json.dump({
                "trade_count": self.trade_count,
                "daily_loss": self.daily_loss
            }, f)

    def can_place_trade(self):
        if self.trade_count >= self.max_trades_per_day:
            print("🛑 Max trades per day reached.")
            return False
        if self.daily_loss <= -self.max_daily_loss:
            print("🛑 Max daily loss limit reached.")
            return False
        return True

    def update_after_trade(self, pnl: float):
        self.trade_count += 1
        self.daily_loss += pnl
        self._save_state()
        print(f"📊 Updated Risk Manager: Trades={self.trade_count}, Daily PnL=${self.daily_loss:.2f}")

    def reset_daily_limits(self):
        self.trade_count = 0
        self.daily_loss = 0
        self._save_state()
        print("🔄 Daily risk limits reset.")
