import re  # 正则表达式库
import pandas as pd
import matplotlib.pyplot as plt
import os
from matplotlib import font_manager
import numpy as np  # 引入NumPy用于检测有限值

# 设置中文字体（这里可以替换为你系统中的其他中文字体）
font_path = "C:/Windows/Fonts/simsun.ttc"
font_prop = font_manager.FontProperties(fname=font_path)

# 读取Excel文件
file_path = r"D:\投资\投资数据实验\智能查询_沪深京股票(年频)182031014\智能查询_沪深京股票(年频).xlsx"
df = pd.read_excel(file_path)

# 创建一个新的文件夹来保存生成的图像
output_folder = r"D:\您的新文件夹路径\折线图结果"  # 修改为您想要的输出路径
os.makedirs(output_folder, exist_ok=True)

# 按B列“证券简称”分组，同时获取证券代码
grouped = df.groupby(['证券代码', '证券简称'])

# 遍历每个组（证券代码和证券简称）生成折线图
for (code, name), group in grouped:
    # 清除文件名中的非法字符
    safe_name = re.sub(r'[\\/*?:"<>|]', "", f"{code}_{name}")  # 替换非法字符为空字符串
    output_path = os.path.join(output_folder, f"{safe_name}_折线图.png")

    # 设置横坐标和纵坐标的数据
    x = group['年份']
    y = group['数值']

    plt.figure()
    plt.plot(x, y, marker='o', label=f"{code} {name}")  # 使用证券代码和名称作为图例
    plt.title(f"{name} ({code}) 年份-数值折线图", fontproperties=font_prop)
    plt.xlabel("年份", fontproperties=font_prop)
    plt.ylabel("数值", fontproperties=font_prop)
    plt.legend(prop=font_prop)  # 显示图例

    # 添加数据点标注
    for i, v in enumerate(y):
        if np.isfinite(v):  # 检查v是否是有限值
            plt.text(x.iloc[i], v, str(v), ha='center', va='bottom', fontproperties=font_prop)  # 标注具体数值

    # 保存图像
    plt.savefig(output_path, format='png')
    plt.close()

print("所有图像已生成并保存到", output_folder)
