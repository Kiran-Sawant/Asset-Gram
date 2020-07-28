import MetaTrader5 as mt5
import pandas as pd
import matplotlib.pyplot as plt
import time


dict1 = {'Dow Jones': 'US30', 'SnP 500': 'US500', 'NASDAQ': 'USTEC', 'Russel 2000': 'US2000',
         'DAX': 'DE30', 'M-DAX': 'MidDE60', 'Tec-DAX': 'TecDE30', 'Eu-Stoxx 50': 'STOXX50',
         'F40': 'F40', 'IBEX': 'ES35', 'MIB': 'IT40', 'NETH25': 'NETH25', 'SE30': 'SE30',
         'Footsie': 'UK100', 'Swiss Market Index': 'SWI20', 'NOR25': 'NOR25', 
         'AUS200': 'AUS200', 'Nikki': 'JP225', 'CHINA50': 'CHINA50', 'Hang Seng': 'HK50',
         'CHINAH': 'CHINAH', 'SA40': 'SA40'}

timeFramedict = {'M1': mt5.TIMEFRAME_M1, 'M5': mt5.TIMEFRAME_M5, 'M10': mt5.TIMEFRAME_M10,
                 'M12': mt5.TIMEFRAME_M12, 'M15': mt5.TIMEFRAME_M15, 'M20': mt5.TIMEFRAME_M20,
                 'M30': mt5.TIMEFRAME_M30, 'H1': mt5.TIMEFRAME_H1, 'H2': mt5.TIMEFRAME_H2,
                 'H4': mt5.TIMEFRAME_H4, 'H6': mt5.TIMEFRAME_H6, 'H12': mt5.TIMEFRAME_H12,
                 'D1': mt5.TIMEFRAME_D1, 'W1': mt5.TIMEFRAME_W1, 'MN1': mt5.TIMEFRAME_MN1}


def dollarPair(currency: str):
    if currency in ['EUR', 'GBP', 'AUD', 'NZD']:
        return currency + 'USD'
    else:
        return 'USD' + currency


def dollarizer(asset, dollarpair, tframe, period):

    mt5.symbol_select(dollarpair)
    time.sleep(2)
    
    asset_rates = pd.DataFrame(mt5.copy_rates_from_pos(asset, tframe, 0, period)).drop(columns=['spread', 'real_volume', 'tick_volume'])
    dollar_rates = pd.DataFrame(mt5.copy_rates_from_pos(dollarpair, tframe, 0, period)).drop(columns=['spread', 'real_volume', 'tick_volume'])
        
    asset_rates['time'] = pd.to_datetime(asset_rates['time'], unit='s')
    dollar_rates['time'] = pd.to_datetime(dollar_rates['time'], unit='s')

    asset_rates.set_index(keys=['time'], inplace=True)
    dollar_rates.set_index(keys=['time'], inplace=True)
    
    if dollarpair[3:6] == 'USD':     # quoted in dollar
        dollarised_asset = asset_rates[['open', 'high', 'low', 'close']] * dollar_rates[['open', 'high', 'low', 'close']]
    
    else:                             # based in dollar
        dollarised_asset = asset_rates[['open', 'high', 'low', 'close']] / dollar_rates[['open', 'high', 'low', 'close']]
        dollarised_asset.rename(columns={'high': 'low', 'low': 'high'})
    
    # dollarised_asset['vol'] = (asset_rates['tick_volume'] + dollar_rates['tick_volume']) / 2
    dollarised_asset.dropa()
    return dollarised_asset


mt5.initialize()

def per_change(symbol, tframe, period):
    mt5.symbol_select(symbol)

    denomination = mt5.symbol_info(symbol).currency_profit
    if denomination != 'USD':
        rateFrame = dollarizer(symbol, dollarPair(denomination), tframe, period)
    for i in range(2):
        rateFrame = pd.DataFrame(mt5.copy_rates_from_pos(symbol, tframe, 0, period)).drop(columns=['spread', 'real_volume', 'tick_volume'])
        time.sleep(1/2)

    # ((current close - previous open)/previous close) * 100
    pcnt_change = ((rateFrame.iloc[(period - 1), 4] - rateFrame.iloc[0, 1]) / rateFrame.iloc[(period - 1), 4]) * 100

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

k.plot(kind='bar', title=f"Index's {period} {tFrame} strength")

plt.show()
mt5.shutdown()