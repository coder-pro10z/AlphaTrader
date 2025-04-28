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

MAX_TRADES_PER_DAY = 5
MAX_LOSS_PER_TRADE = 100  # in USD

trade_count = 0  # simple counter
daily_loss = 0  # simple tracking

def check_risk(symbol: str, quantity: float, signal: str, price: float = 50000) -> bool:
    """
    Risk manager for approving trades.

    Args:
        symbol (str): Trading pair.
        quantity (float): Amount to trade.
        signal (str): 'BUY' or 'SELL'.
        price (float): Current price (for loss calculation).

    Returns:
        bool: True if trade is allowed, False otherwise.
    """
    global trade_count, daily_loss

    if trade_count >= MAX_TRADES_PER_DAY:
        print("🛑 Max trades per day reached.")
        return False

    # Estimate hypothetical loss
    estimated_loss = quantity * price * 0.01  # Assume 1% slippage risk

    if estimated_loss > MAX_LOSS_PER_TRADE:
        print(f"🛑 Risk too high! Estimated loss ${estimated_loss:.2f} exceeds limit.")
        return False

    print(f"✅ Risk Check Passed for {signal} {quantity} {symbol}")
    trade_count += 1
    daily_loss += estimated_loss
    return True

def reset_daily_limits():
    global trade_count, daily_loss
    trade_count = 0
    daily_loss = 0
