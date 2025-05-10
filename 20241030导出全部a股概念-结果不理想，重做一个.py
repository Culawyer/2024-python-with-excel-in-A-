import tushare as ts
import pandas as pd

# 设置 Tushare Token
ts.set_token('c**********************e************02')
pro = ts.pro_api()

# 获取所有概念列表
concepts = pro.concept()

# 创建一个空的 DataFrame，用于存储股票及其概念
all_stock_concepts = pd.DataFrame(columns=['ts_code', 'name', 'concept'])

# 遍历每个概念，获取概念对应的股票列表
for _, row in concepts.iterrows():
    concept_id = row['code']  # 概念ID
    concept_name = row['name']  # 概念名称

    # 获取当前概念的股票列表
    concept_stocks = pro.concept_detail(id=concept_id)
    concept_stocks['concept'] = concept_name  # 添加概念名称列

    # 将当前概念的股票列表添加到总表中
    all_stock_concepts = pd.concat([all_stock_concepts, concept_stocks[['ts_code', 'name', 'concept']]])

# 将股票代码列转换为字符串格式，以保留 Excel 中的前导零
all_stock_concepts['ts_code'] = all_stock_concepts['ts_code'].astype(str)

# 导出到 Excel
output_path = r'D:\投资\投资数据实验\A股股票概念汇总.xlsx'
all_stock_concepts.to_excel(output_path, index=False)

print("全部 A 股股票概念信息已成功导出。")
