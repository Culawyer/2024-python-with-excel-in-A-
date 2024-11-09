import pandas as pd

# 文件路径
file_path = r"D:\投资\投资数据实验\【优先】数据整理包\07-2019-2023A股数据(eps Teps 增加资产负债率 - 副本.xlsx"

# 读取 Excel 数据
df = pd.read_excel(file_path, dtype={'证券代码': str})

# 按 D 列“行业名称D”分组，在分组内按 I 列“2023调整每股收益EPS*（检验期(校验期6个月);）”从大到小排序
df_sorted = df.sort_values(by=['行业名称D', '2023调整每股收益EPS*（检验期(校验期6个月);）'], ascending=[True, False])

# 导出排序后的数据
output_path = r"D:\投资\投资数据实验\07-2019-2023A股数据_排序后.xlsx"
df_sorted.to_excel(output_path, index=False)

print("数据已按要求排序并导出至：", output_path)
