# All stocks trading < $100
import MetaTrader5 as mt5
import pandas as pd
mt5.initialize()

all_assets = mt5.symbols_get()

stocks = list()
small = list()

for asset in all_assets:
    if "Stock" in asset.path:
        stocks.append(asset.name)

for stock in stocks:
    if 'ETF' in mt5.symbol_info(stock).path:
        stocks.remove(stock)
# print(stocks)

for stock in stocks:
    mt5.symbol_select(stock)
    if mt5.symbol_info_tick(stock).ask <= 100:
        small.append(stock)

print(small)
print(len(small))
mt5.shutdown()