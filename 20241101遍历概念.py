# 结合tushare爬取全部a股所属概念
# 需注意在Excel中导入以000开头的股票代码时，Excel会将其视为数字格式并自动去掉前导零的问题。
# 解决方式添加代码 today_data['ts_code'] = today_data['ts_code'].astype(str)  # 确保股票代码为字符串格式
today_data.to_excel(output_path, index=False)
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

# 进行合并，并处理多个概念
df_b = df_b.merge(df_a[['ts_code_prefix', 'concept_name']],
                  how='left',
                  left_on='证券代码_prefix',
                  right_on='ts_code_prefix')

# 将同一证券代码对应的多个概念合并，使用@分隔
df_b['概念'] = df_b.groupby('证券代码_prefix')['concept_name'].transform(lambda x: '@'.join(x.dropna().unique()))

# 移除临时列
df_b.drop(columns=['ts_code_prefix', 'concept_name'], inplace=True)

# 导出结果
output_path = r"D:\投资\投资数据实验\更新后的数据.xlsx"
df_b.to_excel(output_path, index=False)

print("数据合并完成，已导出至：", output_path)
