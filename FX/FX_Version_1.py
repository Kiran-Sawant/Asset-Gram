import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import time

dict1 = {'EUR': 'EURUSD', 'GBP': 'GBPUSD', 'JPY': 'USDJPY', 'CHF': 'USDCHF', 'AUD': 'AUDUSD', 'CAD': 'USDCAD',
         'NZD': 'NZDUSD', 'NOK': 'USDNOK', 'SEK': 'USDSEK',
         'SGD': 'USDSGD', 'HKD': 'USDHKD', 'THB': 'USDTHB', 'CNH': 'USDCNH',
         'ZAR': 'USDZAR', 'MXN': 'USDMXN',
         'TRY': 'USDTRY', 'RUB': 'USDRUB', 'PLN': 'USDPLN', 'CZK': 'USDCZK', 'HUF': 'USDHUF', 'DKK': 'USDDKK',
         'Gold': 'XAUUSD', 'Silver': 'XAGUSD'}

timeFramedict = {'M1': mt5.TIMEFRAME_M1, 'M5': mt5.TIMEFRAME_M5, 'M10': mt5.TIMEFRAME_M10,
                 'M12': mt5.TIMEFRAME_M12, 'M15': mt5.TIMEFRAME_M15, 'M20': mt5.TIMEFRAME_M20,
                 'M30': mt5.TIMEFRAME_M30, 'H1': mt5.TIMEFRAME_H1, 'H2': mt5.TIMEFRAME_H2,
                 'H4': mt5.TIMEFRAME_H4, 'H6': mt5.TIMEFRAME_H6, 'H12': mt5.TIMEFRAME_H12,
                 'D1': mt5.TIMEFRAME_D1, 'W1': mt5.TIMEFRAME_W1, 'MN1': mt5.TIMEFRAME_MN1}

mt5.initialize()

def per_change(symbol, tframe, period):
    mt5.symbol_select(symbol)
    for i in range(2):
        rateFrame = pd.DataFrame(mt5.copy_rates_from_pos(symbol, tframe, 1, period))
        time.sleep(1/2)

    # pcnt_change = (float(rateFrame.tail(1)['close']) - float(rateFrame.head(1)['close'])) / float(rateFrame.tail(1)['close']) * 100
    pcnt_change = ((rateFrame.iloc[(period - 1), 4] - rateFrame.iloc[0, 1]) / rateFrame.iloc[(period - 1), 4]) * 100
    if symbol[3:6] == 'USD':      # Dollar Quoted pairs. 
        return pcnt_change
    else:                         # Dollar Based pairs.
        return - (pcnt_change)

print(f"List of Time Frames: {[i for i in timeFramedict]}\n")
tFrame = input('Enter a Time Frame: ').upper()
period = int(input('Enter periods: '))
new_dict = dict()

for i in dict1:
    k = per_change(dict1[i], timeFramedict[tFrame], period)
    new_dict[i] = k
    print(f'{i}: {k}')

k = pd.Series(new_dict)

k.plot(kind='bar', title=f'FX {period} {tFrame} strength')

plt.show()

mt5.shutdown()