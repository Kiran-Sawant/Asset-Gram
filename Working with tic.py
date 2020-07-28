import MetaTrader5 as mt5
import datetime as dt
import pandas as pd

mt5.initialize()

now_tic = mt5.symbol_info_tick('EURUSD')

delta = dt.timedelta(hours=5).seconds     # 5 hr Delta in seconds.

past_time = int(now_tic.time - delta)

past_tic = mt5.copy_ticks_from('EURUSD', dt.datetime.fromtimestamp(past_time), 1, mt5.COPY_TICKS_INFO)
past_ask = past_tic[0][2]
# past_tic['time'] = pd.to_datetime(past_tic['time'], unit='s')
# # print(past_tic)

per_change = ((now_tic.ask - past_ask)/past_ask) * 100
print(per_change)