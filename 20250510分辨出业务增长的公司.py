import pandas as pd
import matplotlib.pyplot as plt
import os

# 设置中文字体支持（避免图中中文乱码）
plt.rcParams['font.sans-serif'] = ['SimHei']  # 中文字体（黑体）
plt.rcParams['axes.unicode_minus'] = False  # 正常显示负号

# 1. 读取 Excel 文件
file_path = r'C:\Users\Cunning\Desktop\2024上市公司财务信息\2020-2024会计信息.xlsx'
df = pd.read_excel(file_path)

# 2. 保留关注的列并去除缺失值
columns_to_use = ['Symbol', 'EndDate', 'ShortName', 'OperatingRevenue', 'NetProfit', 'EPS']
df = df[columns_to_use].copy()
df.dropna(subset=['OperatingRevenue', 'NetProfit', 'EPS'], inplace=True)

# 3. 转换日期格式并提取年份
df['EndDate'] = pd.to_datetime(df['EndDate'], format='%Y-%m-%d', errors='coerce')
df['Year'] = df['EndDate'].dt.year


# 4. 定义判断是否是增长公司的函数
def is_growth_company(group):
    group = group.sort_values('Year')

    # 至少三年才判断
    if group['Year'].nunique() < 3:
        return False

    # 取出序列，判断是否严格递增
    rev = group['OperatingRevenue'].values
    profit = group['NetProfit'].values
    eps = group['EPS'].values

    def strictly_increasing(arr):
        return all(x < y for x, y in zip(arr, arr[1:]))

    return strictly_increasing(rev) and strictly_increasing(profit) and strictly_increasing(eps)


# 5. 准备输出目录
output_folder = r'C:\Users\Cunning\Desktop\2024上市公司财务信息\增长公司EPS图表'
os.makedirs(output_folder, exist_ok=True)

growth_companies = []

# 6. 分组筛选 + 绘图
for symbol, group in df.groupby('Symbol'):
    try:
        group_clean = group.sort_values('Year')
        if is_growth_company(group_clean):
            name = group_clean['ShortName'].iloc[0]
            growth_companies.append({'Symbol': symbol, 'ShortName': name})

            # 画图
            plt.figure(figsize=(6, 4))
            plt.plot(group_clean['Year'], group_clean['EPS'], marker='o', linestyle='-', color='blue')
            plt.title(f"{name}（{symbol}）EPS变化图")
            plt.xlabel('年份')
            plt.ylabel('每股收益（EPS）')
            plt.grid(True)
            plt.xticks(group_clean['Year'])
            plt.tight_layout()

            # 保存图像（避免特殊字符引起保存失败）
            safe_name = ''.join(c for c in name if c.isalnum())
            filename = f"{symbol}_{safe_name}_EPS.png"
            image_path = os.path.join(output_folder, filename)
            plt.savefig(image_path)
            plt.close()
    except Exception as e:
        print(f"⚠️ 跳过公司 {symbol}，因出错：{e}")

# 7. 输出名单为 Excel
output_excel = r'C:\Users\Cunning\Desktop\2024上市公司财务信息\持续增长公司名单.xlsx'
pd.DataFrame(growth_companies).to_excel(output_excel, index=False)

print("✅ 完成：已筛选出持续增长的公司，并生成图表与名单。")
