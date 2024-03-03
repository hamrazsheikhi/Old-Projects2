from binance import Client, ThreadedWebsocketManager, ThreadedDepthCacheManager
import pandas as pd
import os
from datetime import datetime


def get_clean_candles(symbol: str, start_time: int):
    klines = client.get_historical_klines(symbol, Client.KLINE_INTERVAL_5MINUTE, start_time)
    print("done new candles")
    columns = ['open_time', 'open', 'high', 'low', 'close', 'volume', "close_time", "quote_asset_volume",
               'number_of_trades', "taker_buy_base_asset_volume", "taker_buy_quote_asset_volume",
               "Ignore"]
    klines_df = pd.DataFrame(klines, columns=columns)
    klines_df = klines_df[
        ['open_time', 'open', 'high', 'low', 'close', 'volume', "close_time", "number_of_trades"]]
    klines_df['open'] = klines_df['open'].astype(float)
    klines_df['high'] = klines_df['high'].astype(float)
    klines_df['low'] = klines_df['low'].astype(float)
    klines_df['close'] = klines_df['close'].astype(float)
    klines_df['volume'] = klines_df['volume'].astype(float)
    klines_df["ohlc4"] = (klines_df.open + klines_df.high +
                          klines_df.low + klines_df.close) / 4
    return klines_df


def update_historical_candles(start_date: int, address_name: str):
    if not os.path.exists(address_name):
        print("does not exist")
        print("working")
        klines_df = get_clean_candles("BTCUSDT", start_date)
        klines_df.to_csv(address_name)
        print(klines_df)
    else:
        print('exists')
        df_previous = pd.read_csv(address_name)
        df_previous = df_previous[
            ['open_time', 'open', 'high', 'low', 'close', 'volume', "close_time", "number_of_trades", "ohlc4"]]
        last_candle_open_time = df_previous['open_time'].iloc[-1]
        print(last_candle_open_time)
        klines_df = get_clean_candles("BTCUSDT", int(last_candle_open_time))
        df_previous = pd.concat([df_previous, klines_df.iloc[1:]])
        df_previous.index = range(len(df_previous))
        df_previous.to_csv(address_name)
        print(df_previous)


start_date = 1514764800000  # 2018
# start_date = 1609446600000  # 2021
# start_date = 1640986261000  # 2022
# start_date = 1648758900000  # test
start_date_list = [1514764800000 ,1609446600000 ,1640986261000]
api_key_noa = 'CA5ou8keMV8vUrEiu48ussACzcADCKzVH0X1O9Eo7V75Un3N4kfyVOXKbFxEbZgk'
client = Client(api_key_noa)
for start_date in start_date_list:
    normal_time = datetime.fromtimestamp(start_date / 1000)
    ADDRESS_NAME = f'historical_5m_candles_updatable_from_{normal_time.strftime("%Y_%m_%d")}.csv'
    update_historical_candles(start_date, ADDRESS_NAME)
    print(f'{normal_time}')
print('done all candles')
