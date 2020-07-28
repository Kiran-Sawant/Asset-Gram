"""NASDAQ small shares <~ $100"""

import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import time

dict1 = {'Applied Materials': 'AMAT.NAS', 'Activision Blizzard': 'ATVI.NAS',
         'Comcast': 'CMCSA.NAS', 'Cronos': 'CRON.NAS', 'Cisco': 'CSCO.NAS', 'CSX': 'CSX.NAS', 'Cognizant': 'CTSH.NAS',
         'Dish Network': 'DISH.NAS',
         'Ebay': 'EBAY.NAS',
         'FOX-B': 'FOX.NAS', 'FOX-A': 'FOXA.NAS',
         'Gilead': 'GILD.NAS',
         'Intel': 'INTC.NAS',
         'Kraft Heinz': 'KHC.NAS',
         'Lyft': 'LYFT.NAS',
         'Marriot': 'MAR.NAS', 'Mondelez': 'MDLZ.NAS',
         'Qualcomm': 'QCOM.NAS',
         'Starbucks': 'SBUX.NAS',
         'Tilray': 'TLRY.NAS',
         'Wallrgeen boots': 'WBA.NAS'}

timeFramedict = {'M1': mt5.TIMEFRAME_M1, 'M5': mt5.TIMEFRAME_M5, 'M10': mt5.TIMEFRAME_M10,
                 'M12': mt5.TIMEFRAME_M12, 'M15': mt5.TIMEFRAME_M15, 'M20': mt5.TIMEFRAME_M20,
                 'M30': mt5.TIMEFRAME_M30, 'H1': mt5.TIMEFRAME_H1, 'H2': mt5.TIMEFRAME_H2,
                 'H4': mt5.TIMEFRAME_H4, 'H6': mt5.TIMEFRAME_H6, 'H12': mt5.TIMEFRAME_H12,
                 'D1': mt5.TIMEFRAME_D1, 'W1': mt5.TIMEFRAME_W1, 'MN1': mt5.TIMEFRAME_MN1}

mt5.initialize()

def per_change(symbol, tframe, period):
    mt5.symbol_select(symbol)
    for i in range(2):
        rateFrame = pd.DataFrame(mt5.copy_rates_from_pos(symbol, tframe, 0, period))
        time.sleep(1/2)

    # pcnt_change = (float(rateFrame.tail(1)['close']) - float(rateFrame.head(1)['close'])) / float(rateFrame.tail(1)['close']) * 100
    pcnt_change = ((rateFrame.iloc[(period - 1), 4] - rateFrame.iloc[0, 1]) / rateFrame.iloc[(period - 1), 4]) * 100
    return pcnt_change

print(f"List of Time Frames: {[i for i in timeFramedict]}\n")
tFrame = input('Enter a Time Frame: ').upper()
period = int(input('Enter periods: '))
new_dict = dict()

for i in dict1:
    k = per_change(dict1[i], timeFramedict[tFrame], period)
    new_dict[i] = k
    print(f'{i}: {k}')

k = pd.Series(new_dict)

k.plot(kind='bar', title=f'NASDAQ small {period} {tFrame} strength')

plt.show()

mt5.shutdown()