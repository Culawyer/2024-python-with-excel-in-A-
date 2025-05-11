import tushare as ts
import pandas as pd
import time


# 设置 Tushare Token
ts.set_token('**************************************')  # ← 记得替换成你自己的 token

pro = ts.pro_api()

# 获取股票列表（只取A股主板和中小板、创业板）
stocks = pro.stock_basic(exchange='', list_status='L', fields='ts_code,symbol,name,market,industry')

# 年份设定
year = 2023
start_date = f'{year}0101'
end_date = f'{year}1231'

# 存储结果
result = []

# 遍历每只股票
for i, row in stocks.iterrows():
    ts_code = row['ts_code']
    name = row['name']

    try:
        # 获取财务指标
        df = pro.fina_indicator(ts_code=ts_code, start_date=start_date, end_date=end_date)

        if df.empty:
            continue

        item = df.iloc[0]  # 最新一期

        # 巴菲特风格的简化标准（免费接口能支持的）：
        roe = item.get('roe')  # 净资产收益率
        netprofit_margin = item.get('netprofit_margin')  # 净利率
        debt_to_assets = item.get('debt_to_assets')  # 资产负债率

        if roe is not None and roe > 15 and \
           netprofit_margin is not None and netprofit_margin > 10 and \
           debt_to_assets is not None and debt_to_assets < 50:
            result.append({
                'ts_code': ts_code,
                'name': name,
                'ROE': roe,
                '净利率': netprofit_margin,
                '资产负债率': debt_to_assets
            })

        time.sleep(0.3)  # 防止触发频率限制

    except Exception as e:
        print(f"{ts_code} 出错：{e}")
        time.sleep(0.5)
        continue

# 输出结果
df_result = pd.DataFrame(result)
output_path = '巴菲特风格选股结果.xlsx'
df_result.to_excel(output_path, index=False)

print(f"✅ 完成：共找到 {len(df_result)} 家符合条件的公司，结果保存在：{output_path}")
