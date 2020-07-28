"""NYSE small shares <~ $100"""

import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import time

dict1 = {'Abbott': 'ABT.NYSE', 'Abbvie': 'ABBV.NYSE', 'Aurora Cannabis': 'ACB.NYSE', 'American Express': 'AXP.NYSE',
         'Bank of America': 'BAC.NYSE', 'Bristol Myers': 'BMY.NYSE',
         'Citi Grp': 'C.NYSE', 'Canopy': 'CGC.NYSE', 'CVS Health': 'CVS.NYSE', 'Chevron': 'CVX.NYSE',
         'DuPont Denumorus': 'DD.NYSE', 'DowDuPont': 'DWDP.NYSE',
         'General Electric': 'GE.NYSE',
         'JP Morgan': 'JPM.NYSE',
         'Coca Cola': 'KO.NYSE',
         'Altria': 'MO.NYSE', 'Morgan Stanly': 'MS.NYSE',
         'Nike': 'NKE.NYSE',
         'Oracle': 'ORCL.NYSE',
         'Pinterest': 'PINS.NYSE', 'Pfizer': 'PFE.NYSE', 'Phillip Morris': 'PM.NYSE',
         'Schlumberger': 'SLB.NYSE',
         'AT&T': 'T.NYSE', 'Time Werner': 'TWX.NYSE',
         'US Bancorp': 'USB.NYSE', 'United Tech': 'UTX.NYSE', 'Uber': 'UBER.NYSE',
         'Verizon': 'VZ.NYSE',
         'Wells Fargo': 'WFC.NYSE',
         'Exxon Mobil': 'XOM.NYSE'}

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

k.plot(kind='bar', title=f'NYSE small {period} {tFrame} strength')

plt.show()

mt5.shutdown()