import ghabl_az_14_farvardin.analysis_candles_ft_amir as ga
import xlsxwriter as xl
import pandas as pd
import os


def renko_into_xlsx(address_in: str, address_out: str, last_candles: int, part_size=16000, part_num=1):
    address_steps = f'steps_strings_{last_candles}_step_size_{STEPS_SIZE}_general.csv'
    steps = pd.read_csv(address_steps, index_col=0)['price_node']
    steps = steps[-part_size * part_num:(-part_size * (part_num - 1)) if part_num > 1 else None]
    print(steps)
    vols = pd.read_csv(address_steps, index_col=0)['volume']
    vols = vols[-part_size * part_num:(-part_size * (part_num - 1)) if part_num > 1 else None]
    candles_count = pd.read_csv(address_steps, index_col=0)['candle_count']
    candles_count = candles_count[-part_size * part_num:(-part_size * (part_num - 1)) if part_num > 1 else None]
    print(vols)
    print('got the files')
    steps.index = steps.reset_index(drop=True).index + 1
    vols.index = vols.reset_index(drop=True).index + 1
    candles_count.index = candles_count.reset_index(drop=True).index + 1
    # candles_count = candles_count.astype(str).apply(lambda x: x.zfill(1))
    # candles_count = candles_count.astype(int)
    out_workbook = xl.Workbook(address_out)
    out_sheet = out_workbook.add_worksheet()
    out_sheet.write(0, 0, 'PRICE')
    format1 = out_workbook.add_format({'bg_color': '#6AA121', 'border': 1})  # green
    format2 = out_workbook.add_format({'bg_color': '#FBB917', 'border': 1})  # orange
    format3 = out_workbook.add_format({'bg_color': '#FF0000', 'border': 1})  # red
    for i in range(1, 2 + (69000 // STEPS_SIZE)):
        out_sheet.write(i, 0, 69000 - (i - 1) * STEPS_SIZE)
    num = 1
    prev_step = 0
    candles_day_num = 0
    candles_week_num = 0
    candles_month_num = 0
    print(steps)
    print(vols)
    print(candles_count)

    for items in steps:
        out_sheet.write(1 + ((69000 - items) / STEPS_SIZE), num, 'X', format1 if items - prev_step > 0 else format3)
        out_sheet.write(2 + ((69000 - items) / STEPS_SIZE), num, vols[num])
        out_sheet.write(3 + ((69000 - items) / STEPS_SIZE), num, candles_count[num])
        out_sheet.write(4 + ((69000 - items) / STEPS_SIZE), num,
                        vols[num] / candles_count[num] if candles_count[num] != 0 else 1)

        if candles_day_num >= 288:
            out_sheet.write(5 + ((69000 - items) / STEPS_SIZE), num, 'D', format2)
            candles_day_num = candles_day_num - 288
        if candles_week_num >= 2016:
            out_sheet.write(6 + ((69000 - items) / STEPS_SIZE), num, 'W', format2)
            candles_week_num = candles_week_num - 2016
        if candles_month_num >= 14112:
            out_sheet.write(7 + ((69000 - items) / STEPS_SIZE), num, 'M', format2)
            candles_month_num = candles_month_num - 14112

        candles_week_num = candles_week_num + candles_count[num]
        candles_day_num = candles_day_num + candles_count[num]
        candles_month_num = candles_month_num + candles_count[num]

        num += 1
        prev_step = items

    out_workbook.close()

    return 'done'


print('getting parameters...')
STEPS_SIZE = 250
last_candles = 447402
address_in = "historical_5m_data_2015_new.csv"
address_steps = f'steps_strings_{last_candles}_step_size_{STEPS_SIZE}_general.csv'
part_size = 16000
print('parameters are set')
print('lets start')


def steps_string_maker(address_one: str, address_second: str, last_candles: int):
    if not os.path.exists(address_second):
        print('does not exist')
        default_candles = pd.read_csv(address_one, index_col=0)
        step_string = ga.renko_df_maker(default_candles, last_candles)
        step_string.to_csv(address_second)
        return step_string
    else:
        print('already exists')
        return pd.read_csv(address_second, index_col=0)


def main_project():
    steps_df_main = steps_string_maker(address_in, address_steps, last_candles)
    type(steps_df_main)
    print(steps_df_main)
    for i in range(1, len(steps_df_main) // part_size + 1):
        renko_into_xlsx(address_in, f'renko_chart_last_{last_candles}_step_size_{STEPS_SIZE}_part_{i}.xlsx',
                        last_candles)
        print(f'part {i} is done')


main_project()

# def gather_sheets_together(common_address: str, address_out: str):
#     out_workbook = xl.Workbook(address_out)
#     for i in range(1, 10):
#         temp_address = common_address + str(i) + '.xlsx'
#         temp_df = pd.read_excel(io=temp_address, engine='openpyxl')
#         exec(f'out_sheet_{i} = out_workbook.add_worksheet(sheet_{i})')
#     out_workbook.close()
#
#
# print('working')
# common_address = 'renko_chart_last_447402_step_size_50_part_'
# address_out = 'renko_chart_last_447402_step_size_50_general.xlsx'
# gather_sheets_together(common_address, address_out)
# print('done the whole project')
