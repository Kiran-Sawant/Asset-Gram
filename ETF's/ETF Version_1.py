import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import time


dict1 = {'Emerging Markets': 'EEM.NYSE', 'Hong-Kong': 'EWH.NYSE', 'Mexico Capped': 'EWW.NYSE', 'Brazil Capped': 'EWZ.NYSE',
         'China Large-cap': 'FXI.NYSE', 'Gold-Miners': 'GDX.NYSE', 'Jr. Gold-Miners': 'GDXJ.NYSE', 'Core Emerging Markets': 'IEMG.NYSE',
         'Corp Bond': 'LQD.NYSE', 'Alternative Harvest': 'MJ.NYSE', 'Agribusiness': 'MOO.NYSE', 'Russia ETF': 'RSX.NYSE', 'DB Agriculture': 'DBA.NYSE',
         'Silver Miners': 'SIL.NYSE', 'Oil&Gas Exp': 'XOP.NYSE', 'US Gas': 'UNG.NYSE', 'US Oil': 'USO.NYSE', 'Global Uranium': 'URA.NYSE',
         'High Divident': 'VYM.NYSE', 'SS Energy': 'XLE.NYSE', 'SS Financial': 'XLF.NYSE', 'SS Industrial': 'XLI.NYSE', 'SS Consumer': 'XLP.NYSE',
         'SS Utilities': 'XLU.NYSE', 'Nasdaq-100 ETF': 'QQQ.NAS', '20+ Y T-Bond': 'TLT.NAS'}

timeFramedict = {'M1': mt5.TIMEFRAME_M1, 'M5': mt5.TIMEFRAME_M5, 'M10': mt5.TIMEFRAME_M10,
                 'M12': mt5.TIMEFRAME_M12, 'M15': mt5.TIMEFRAME_M15, 'M20': mt5.TIMEFRAME_M20,
                 'M30': mt5.TIMEFRAME_M30, 'H1': mt5.TIMEFRAME_H1, 'H2': mt5.TIMEFRAME_H2,
                 'H4': mt5.TIMEFRAME_H4, 'H6': mt5.TIMEFRAME_H6, 'H12': mt5.TIMEFRAME_H12,
                 'D1': mt5.TIMEFRAME_D1, 'W1': mt5.TIMEFRAME_W1, 'MN1': mt5.TIMEFRAME_MN1}

mt5.initialize()

def per_change(symbol, tframe, period):
    mt5.symbol_select(symbol)
    for i in range(2):
        rateFrame = pd.DataFrame(mt5.copy_rates_from_pos(symbol, tframe, 0, period)).drop(columns=['spread', 'real_volume', 'tick_volume'])
        time.sleep(1/2)

    # ((current close - previous open)/previous close) * 100
    pcnt_change = ((rateFrame.iloc[(period - 1), 4] - rateFrame.iloc[0, 1]) / rateFrame.iloc[(period - 1), 4]) * 100

    # return pcnt_change
    return pcnt_change.__round__(3)

print(f"List of Time Frames: {[i for i in timeFramedict]}\n")
tFrame = input('Enter a Time Frame: ').upper()
period = int(input('Enter periods: '))
print('\n', '='*50)
new_dict = dict()

for i in dict1:
    k = per_change(dict1[i], timeFramedict[tFrame], period)
    new_dict[i] = k
    print(f"{i}: {k}")

k = pd.Series(new_dict)

k.plot(kind='bar', title=f'ETFs {period} {tFrame} strength')

plt.show()
mt5.shutdown()