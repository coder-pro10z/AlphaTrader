from execution_engine.binance_connector import BinanceConnector
# from execution_engine.executor import BinanceExecutor

# executor = BinanceExecutor(account_type="spot")

# # Place a test market buy order
# response = executor.place_order(
#     symbol="BTCUSDT",
#     side="BUY",
#     order_type="MARKET",
#     quantity=0.001
# )

# print(response)


executor = BinanceConnector(account_type="spot")

# Place a Market Order
response = executor.place_order(
    symbol="BTCUSDT",
    side="BUY",
    order_type="MARKET",
    quantity=0.001
)

print(response)
