import pandas as pd

# 加载表A和表B，指定证券代码列为字符串类型
file_a = r"D:\投资\投资数据实验\20241030沪深京股票(年频)2023主要是行业，主营业务无形资产\智能查询_沪深京股票(年频).xlsx"
file_b = r"D:\投资\投资数据实验\【优先】数据整理包\02-2019-2023A股数据(eps Teps 主营业务)-01副本图片删除版本 可以先.xlsx"

# 读取数据
df_a = pd.read_excel(file_a)
df_b = pd.read_excel(file_b, dtype={'证券代码': str})  # 将证券代码列指定为字符串类型

# 提取前六位
df_a['code_prefix'] = df_a['code'].astype(str).str[:6]
df_b['证券代码_prefix'] = df_b['证券代码'].astype(str).str[:6]

# 进行合并
df_b = df_b.merge(df_a[['code_prefix', 'FI_T9-F090101B']],
                  how='left',
                  left_on='证券代码_prefix',
                  right_on='code_prefix')

# 将合并结果的 'FI_T9-F090101B' 列数据插入到 'kk' 列
df_b['kk'] = df_b['FI_T9-F090101B']

# 移除临时列
df_b.drop(columns=['code_prefix', '证券代码_prefix', 'FI_T9-F090101B'], inplace=True)

# 导出结果
output_path = r"D:\投资\投资数据实验\更新后的数据.xlsx"
df_b.to_excel(output_path, index=False)

print("数据合并完成，已导出至：", output_path)