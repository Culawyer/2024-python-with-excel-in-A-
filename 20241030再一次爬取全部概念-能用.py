import tushare as ts
import pandas as pd

pro = ts.pro_api('c2c9a9f0b04de25d869b9bcbcb45764b1d7264f981a6ae4df14b0302')

# 获取所有概念
all_concepts = pro.concept()

# 创建一个空的 DataFrame 存放所有股票和对应概念
all_stock_concepts = pd.DataFrame()

# 遍历每个概念ID，将结果合并到一个DataFrame中
for concept_id in all_concepts['code']:
    try:
        concept_stocks = pro.concept_detail(id=concept_id)
        all_stock_concepts = pd.concat([all_stock_concepts, concept_stocks])
    except Exception as e:
        print(f"获取概念ID {concept_id} 失败:", e)

# 确保股票代码格式正确，并保存到文件中
all_stock_concepts['ts_code'] = all_stock_concepts['ts_code'].astype(str).str.zfill(6)
all_stock_concepts.to_excel("D:\\投资\\投资数据实验\\全部A股概念.xlsx", index=False)