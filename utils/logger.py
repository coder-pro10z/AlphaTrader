# import logging

# # Configure the logger once
# logging.basicConfig(
#     level=logging.INFO,
#     format="%(asctime)s [%(levelname)s] %(message)s",
#     handlers=[logging.StreamHandler()],
# )


# def log_event(message: str):
#     logging.info(message)

# utils/trade_logger.py
# import logging
# import os

# os.makedirs("logs", exist_ok=True)

# trade_logger = logging.getLogger("TRADE_LOGGER")
# trade_logger.setLevel(logging.INFO)

# fh = logging.FileHandler("logs/trade_log.txt")
# formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
# fh.setFormatter(formatter)

# trade_logger.addHandler(fh)


# def log_trade(action, symbol, price, quantity):
#     trade_logger.info(f"{action} {quantity} {symbol} @ {price}")

import logging
import os

# Ensure logs directory exists
os.makedirs("logs", exist_ok=True)

# --- Trade Logger ---
trade_logger = logging.getLogger("TRADE_LOGGER")
trade_logger.setLevel(logging.INFO)

trade_file_handler = logging.FileHandler("logs/trade_log.txt")
trade_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
trade_file_handler.setFormatter(trade_formatter)

if not trade_logger.handlers:
    trade_logger.addHandler(trade_file_handler)


def log_trade(action, symbol, price, quantity):
    trade_logger.info(f"{action} {quantity} {symbol} @ {price}")


# --- General Event Logger ---
event_logger = logging.getLogger("EVENT_LOGGER")
event_logger.setLevel(logging.INFO)

event_file_handler = logging.FileHandler("logs/event_log.txt")
event_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
event_file_handler.setFormatter(event_formatter)

if not event_logger.handlers:
    event_logger.addHandler(event_file_handler)


def log_event(message, level="info"):
    if level == "info":
        event_logger.info(message)
    elif level == "warning":
        event_logger.warning(message)
    elif level == "error":
        event_logger.error(message)
    elif level == "debug":
        event_logger.debug(message)
