import pandas as pd

# 读取Excel文件
file_path = r'D:\投资\投资数据实验\【优先】数据整理包\02-2019-2023A股数据(eps Teps 主营业务)遍历概念2目的是单个股票看概念 - 副本.xlsx'
df = pd.read_excel(file_path)

# 输出初始数据以检查
print("初始数据：")
print(df.head())

# 获取E列（持股排名(第一大股东)）和C列（上市日期）的数据
shareholder_rankings = df['持股排名(第一大股东)']
listing_dates = df['上市日期']

# 将持股排名逐行放入上市日期的尾部
for index, ranking in enumerate(shareholder_rankings):
    if pd.notna(ranking):  # 只添加非NaN值
        # 使用分隔符' '确保不影响原有数据格式
        listing_dates.at[index] = str(listing_dates.at[index]) + ' ' + str(ranking)

# 更新C列（上市日期）的数据
df['上市日期'] = listing_dates

# 保存更改到Excel文件
df.to_excel(file_path, index=False)

print("\n更新后的数据已保存。")
