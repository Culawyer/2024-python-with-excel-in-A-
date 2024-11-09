import pandas as pd

# 文件路径
file_a = r"D:\投资\投资数据实验\2023资产负债率\智能查询_沪深京股票(年频).xlsx"
file_b = r"D:\投资\投资数据实验\【优先】数据整理包\06最终打印版本 - 副本.xlsx"

# 读取表A和表B，确保'证券代码'列读取为字符串类型
df_a = pd.read_excel(file_a, dtype={'code': str})
df_b = pd.read_excel(file_b, dtype={'证券代码': str})

# 打印列名确认
print("表A列名:", df_a.columns)
print("表B列名:", df_b.columns)

# 重命名表A中的列，以便与代码中的列名一致
df_a = df_a.rename(columns={'code': '证券代码', 'FI_T1-F011201A': '资产负债率'})

# 合并数据
df_merged = pd.merge(df_b, df_a[['证券代码', '资产负债率']], on='证券代码', how='left')

# 导出结果
output_path = r"D:\投资\投资数据实验\06最终打印版本_更新后.xlsx"
df_merged.to_excel(output_path, index=False)

print("数据合并完成，已导出至：", output_path)
