import tushare as ts
import pandas as pd
import datetime

# 初始化 tushare
ts.set_token('c**************************************************')  # 替换为你的token
pro = ts.pro_api()

# 设置年份范围（近3年）
end_year = datetime.datetime.now().year - 1
years = [str(end_year - i) for i in range(3)][::-1]  # 比如 ['2021', '2022', '2023']

# 读取所有A股列表
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,area,industry,list_date')

# 建立空列表用于存放结果
results = []

# 遍历每只股票
for i, row in stocks.iterrows():
    ts_code = row['ts_code']
    name = row['name']
    try:
        # 获取近三年财务指标
        df_fin = pro.fina_indicator(ts_code=ts_code)
        df_fin = df_fin[df_fin['end_date'].str[:4].isin(years)]

        # 获取估值
        df_val = pro.daily_basic(ts_code=ts_code, trade_date=f'{end_year}1231')

        # 获取资产负债表数据（资产负债率）
        df_bs = pro.balancesheet(ts_code=ts_code, start_date=f'{end_year - 2}0101', end_date=f'{end_year}1231')
        df_bs['debt_ratio'] = df_bs['total_liab'] / df_bs['total_assets']
        avg_debt_ratio = df_bs['debt_ratio'].mean()

        # 判断是否满足格雷厄姆筛选条件
        if (
                len(df_fin) >= 3 and
                all(df_fin['eps'].fillna(0) > 0) and
                all(df_fin['netprofit'].fillna(0) > 0) and
                df_val is not None and
                df_val.iloc[0]['pe'] < 15 and
                df_val.iloc[0]['pb'] < 1.5 and
                df_val.iloc[0]['pe'] * df_val.iloc[0]['pb'] < 22.5 and
                avg_debt_ratio < 0.5
        ):
            results.append({
                'ts_code': ts_code,
                'name': name,
                'PE': df_val.iloc[0]['pe'],
                'PB': df_val.iloc[0]['pb'],
                'avg_debt_ratio': round(avg_debt_ratio, 2)
            })

    except Exception as e:
        continue  # 忽略异常，比如有的公司停牌或数据缺失

# 输出结果
df_result = pd.DataFrame(results)
output_path = '格雷厄姆初选公司名单.xlsx'
df_result.to_excel(output_path, index=False)
print(f"✅ 完成：共找到 {len(df_result)} 家符合格雷厄姆标准的公司，结果已保存至：{output_path}")
