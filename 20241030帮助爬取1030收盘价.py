# 结合tushare 我想导出全部a股当日收盘价
# 确保你已经安装了 tushare 和 pandas 库。
# 获取当日的收盘价数据。
# 将数据导出到Excel

import tushare as ts
import pandas as pd

# 设置Tushare的token
ts.set_token('c2c9a9f0b04de25d869b9bcbcb45764b1d7264f981a6ae4df14b0302')
pro = ts.pro_api()

# 获取当天的A股收盘价数据
today_data = pro.daily(trade_date='20231030')  # 替换为你想要查询的日期

# 将数据导出到Excel
output_path = r'D:\投资\投资数据实验\A股当日收盘价.xlsx'
today_data.to_excel(output_path, index=False)

print("A股当日收盘价已成功导出。")
