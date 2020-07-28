import MetaTrader5 as mt5
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
import time

dict1 = {'EUR': 'EURUSD', 'GBP': 'GBPUSD', 'JPY': 'USDJPY', 'CHF': 'USDCHF', 'AUD': 'AUDUSD', 'CAD': 'USDCAD',
         'NZD': 'NZDUSD', 'NOK': 'USDNOK', 'SEK': 'USDSEK',
         'SGD': 'USDSGD', 'HKD': 'USDHKD', 'THB': 'USDTHB', 'CNH': 'USDCNH',
         'ZAR': 'USDZAR', 'MXN': 'USDMXN',
         'TRY': 'USDTRY', 'RUB': 'USDRUB', 'PLN': 'USDPLN', 'CZK': 'USDCZK', 'HUF': 'USDHUF', 'DKK': 'USDDKK',
         'Gold': 'XAUUSD', 'Silver': 'XAGUSD'}

deltas = {'M1': dt.timedelta(minutes=1).seconds,
          'M10': dt.timedelta(minutes=10).seconds,
          'M12': dt.timedelta(minutes=12).seconds,
          'M15': dt.timedelta(minutes=15).seconds,
          'M20': dt.timedelta(minutes=20).seconds,
          'M30': dt.timedelta(minutes=30).seconds,
          'H1': dt.timedelta(hours=1).seconds,
          'H2': dt.timedelta(hours=2).seconds,
          'H4': dt.timedelta(hours=4).seconds,
          'H6': dt.timedelta(hours=6).seconds,
          'H12': dt.timedelta(hours=12).seconds,
          'D1': dt.timedelta(days=1).seconds,
          'W1': dt.timedelta(weeks=1).seconds,
          'MN1': dt.timedelta(days=30).seconds}

mt5.initialize()

# print(mt5.account_info())

def per_change(symbol, delta):
    """Returns the percentage change in the price of asset in the given 
    time-delta from the latest price in the terminal."""

    mt5.symbol_select(symbol)

    # latest tick data.
    now_tick = mt5.symbol_info_tick(symbol)
    now_ask = now_tick.ask                  # latest ask price.
    now_time = now_tick.time                # latest time of tick

    # setting past-time adjusting with delta.
    past_time = dt.datetime.fromtimestamp(now_time - delta)

    # Getting past tick
    past_tick = mt5.copy_ticks_from(symbol, past_time, 1, mt5.COPY_TICKS_INFO)
    past_ask = past_tick[0][2]              # getting past ask.

    # calculating percentage change.
    per_chng = ((now_ask - past_ask)/past_ask) * 100

    if symbol[3:6] == 'USD':
        return per_chng
    else:
        return -(per_chng)

print(f"List of Time Frames: {[i for i in deltas]}\n")
tFrame = input('Enter Timeframe: ').upper()
period = int(input('Enter periods: '))
delta = deltas[tFrame] * period

percent_dict = dict()

for i in dict1:
    # print(f'{i}: {per_change(dict1[i], delta)}')
    percent_dict[i] = per_change(dict1[i], delta)

percent_Series = pd.Series(percent_dict)

percent_Series.plot(kind='bar', title=f'FX {period} {tFrame} strength')
plt.show()

mt5.shutdown()