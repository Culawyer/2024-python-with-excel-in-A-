import pandas as pd

# 文件路径
file_a = r"D:\投资\投资数据实验\全部A股概念.xlsx"
file_b = r"D:\投资\投资数据实验\【优先】数据整理包\02-2019-2023A股数据(eps Teps 主营业务)-01副本图片删除版本 可以先.xlsx"

# 读取表A和表B，指定证券代码列为字符串类型
df_a = pd.read_excel(file_a)
df_b = pd.read_excel(file_b, dtype={'证券代码': str})  # 将证券代码列指定为字符串类型

# 提取前六位
df_a['ts_code_prefix'] = df_a['ts_code'].astype(str).str[:6]
df_b['证券代码_prefix'] = df_b['证券代码'].astype(str).str[:6]

# 结果存储列表
result_rows = []

# 遍历表B的每一行
for index, row in df_b.iterrows():
    matching_concepts = df_a[df_a['ts_code_prefix'] == row['证券代码_prefix']]['concept_name'].tolist()

    if matching_concepts:
        # 将所有匹配的concept_name添加到结果行中
        for concept in matching_concepts:
            new_row = row.copy()
            new_row['概念'] = concept  # 在新行中填充概念
            result_rows.append(new_row)  # 添加到结果列表中
    else:
        # 如果没有匹配，保留原行（概念列为空）
        new_row = row.copy()
        new_row['概念'] = None
        result_rows.append(new_row)

# 创建新的DataFrame
df_result = pd.DataFrame(result_rows)

# 导出结果
output_path = r"D:\投资\投资数据实验\更新后的数据.xlsx"
df_result.to_excel(output_path, index=False)

print("数据合并完成，已导出至：", output_path)
