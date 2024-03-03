from binance import ThreadedWebsocketManager
import pandas as pd
import time
from datetime import datetime

bids = []  #
asks = []  #
twm = ThreadedWebsocketManager()
bid_price_list_all = []
ask_price_list_all = []
bid_qty_list_all = []
ask_qty_list_all = []
df = pd.DataFrame()
list_price_level = []
DN = 25  # DEVIDE NUMBER
for i in range(1, 40):
    list_price_level.append(45500 - DN * i)
df['in'] = list_price_level
df.index = df['in']
del df['in']
# for t in range(10):
#     df[f'bid{t}'] = 0
#     df[f'ask{t}'] = 0
# df['sum_bid'] = 0.0
# df['sum_ask'] = 0.0


# prev_price = 0
prev_time = 0
df_score_board = pd.DataFrame(columns=['time', 'price', 'qty', 'count_maker', 'count_taker',
                                       'sum_qty_maker', 'sum_qty_taker', 'count_maker_per_taker',
                                       'qty_maker_per_taker', 'time_diff', 'price_diff',
                                       'diff_first_and_current'])

df_temp = pd.DataFrame(columns=['time', 'price', 'qty', 'count_maker', 'count_taker',
                                'sum_qty_maker', 'sum_qty_taker', 'count_maker_per_taker',
                                'qty_maker_per_taker', 'time_diff', 'price_diff',
                                'diff_first_and_current'])


def on_message(message):
    global df_temp
    global df_score_board
    global first_price
    global prev_price
    global prev_time
    global sum_qty_maker
    global sum_qty_taker
    global count_maker
    global count_taker
    global n
    global df
    global bid_price_list_all
    global ask_price_list_all
    global bid_qty_list_all
    global ask_qty_list_all
    # if message["stream"] == "btcusdt@depth":
    #     try:
    #         n += 1
    #         if n % 2 == 0:
    #             print(pd.concat([df[df['sum_bid'] != 0], df[df['sum_ask'] != 0]]))
    #     except NameError:
    #         n = 1
    #
    #     try:
    #         message = message['data']
    #         bids_list = message['b']
    #         # print(bids_list)
    #         asks_list = message['a']
    #         bid_prices = [x[0] for x in bids_list]
    #         bid_qtys = [x[1] for x in bids_list]
    #         # print(bid_prices)
    #         # print(bid_qtys)
    #
    #         ask_prices = [x[0] for x in asks_list]
    #         ask_qtys = [x[1] for x in asks_list]
    #         print(n)
    #         print("\n")
    #         for t in range(len(bid_prices)):
    #             df.at[int(float(bid_prices[t])) // DN * DN, 'sum_bid'] += float(bid_qtys[t])
    #             df.at[int(float(ask_prices[t])) // DN * DN, 'sum_ask'] -= float(ask_qtys[t])
    #
    #         # for t in range(len(bid_prices)):
    #         #     df.at[int(float(bid_prices[t])) // DN * DN, f"bid{n}"] += float(bid_qtys[t])
    #         # for t in range(len(ask_prices)):
    #         #     df.at[int(float(ask_prices[t])) // DN * DN, f"ask{n}"] -= float(ask_qtys[t])
    #     except:
    #         pass
    try:
        if message["stream"] == "btcusdt@aggTrade":
            try:
                message = message['data']
                price = float(message['p'])
                qty = float(message['q'])
                is_maker = message['m']
                current_time = str(datetime.fromtimestamp(message['E'] / 1000))

                if is_maker:
                    try:
                        count_maker += 1
                        sum_qty_maker += qty

                    except:
                        sum_qty_maker = 0.0
                        count_maker = 1

                else:
                    try:
                        count_taker += 1
                        sum_qty_taker += qty
                    except:
                        count_taker = 1
                        sum_qty_taker = 0.0

                print(f"\n{current_time=}\n{price=}\n{qty=}\n{count_maker=}\n{count_taker=}\n"
                      f"{sum_qty_maker=}\n{sum_qty_taker=}\n"
                      f"count_maker/taker={count_maker / count_taker}\n"
                      f"qty_maker/taker={sum_qty_maker / sum_qty_taker}"
                      )

                df_temp.at[0, 'time'] = current_time
                df_temp.at[0, 'price'] = price
                df_temp.at[0, 'qty'] = qty
                df_temp.at[0, 'count_maker'] = count_maker
                df_temp.at[0, 'count_taker'] = count_taker
                df_temp.at[0, 'sum_qty_maker'] = sum_qty_maker
                df_temp.at[0, 'sum_qty_taker'] = sum_qty_taker
                df_temp.at[0, 'count_maker_per_taker'] = count_maker / count_taker
                df_temp.at[0, 'qty_maker_per_taker'] = sum_qty_maker / sum_qty_taker

                try:
                    time_diff = message['E'] - prev_time
                    print(f'{time_diff=} ms')
                    prev_time = message['E']
                    df_temp.at[0, 'time_diff'] = time_diff
                except:
                    prev_time = 0

                try:
                    price_diff = price - prev_price
                    print(f'{price_diff=} $')
                    prev_price = price
                    df_temp.at[0, 'price_diff'] = price_diff
                except:
                    prev_price = 0
                try:
                    diff_first_and_current = price - first_price
                    print(f'{diff_first_and_current=} $')
                    df_temp.at[0, 'diff_first_and_current'] = diff_first_and_current
                    print("_____________________________________________")

                except:
                    first_price = price

                df_score_board = df_score_board.append(df_temp, ignore_index=True)
                # print('df score board = ')
                print(df_score_board)
                # print("_____________________________________________")
            except:
                df_score_board.to_csv(f'test_websocket_{time_out_s}_temp.csv')
    except:
        df_score_board.to_csv(f'test_websocket_{time_out_s}_temp4.csv')


time_out_s = 1800
streams = ["btcusdt@aggTrade"]  # 'btcusdt@depth'
twm.start()
try:
    twm.start_multiplex_socket(on_message, streams)
except:
    df_score_board.to_csv(f'test_websocket_{time_out_s}_temp2.csv')

twm.join(timeout=time_out_s)
twm.stop()
print('\n\nhey this is me\n')
print(f"{df_score_board=}")
df_score_board.to_csv(f'test_websocket_{time_out_s}.csv')
