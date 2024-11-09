
import pandas as pd
import matplotlib.pyplot as plt
import os
import warnings
warnings.simplefilter("ignore", UserWarning)

import pandas as pd
import matplotlib.pyplot as plt
import os

import re  # 正则表达式库
import pandas as pd
import matplotlib.pyplot as plt
import os

# 读取Excel文件
file_path = r"D:\投资\投资数据实验\智能查询_沪深京股票(年频)182031014\智能查询_沪深京股票(年频).xlsx"
df = pd.read_excel(file_path)

# 创建一个文件夹来保存生成的图像
output_folder = r"C:\日常\计算机学习\Python零散文件\折线图结果"
os.makedirs(output_folder, exist_ok=True)

# 按B列“证券简称”分组
grouped = df.groupby('证券简称')

# 遍历每个组（证券简称）生成折线图
for name, group in grouped:
    # 清除文件名中的非法字符
    safe_name = re.sub(r'[\\/*?:"<>|]', "", name)  # 替换非法字符为空字符串
    output_path = os.path.join(output_folder, f"{safe_name}_折线图.png")

    # 设置横坐标和纵坐标的数据
    x = group['年份']
    y = group['数值']

    plt.figure()
    plt.plot(x, y, marker='o')
    plt.title(f"{name} 年份-数值折线图")
    plt.xlabel("年份")
    plt.ylabel("数值")

    # 保存图像
    plt.savefig(output_path, format='png')
    plt.close()

print("所有图像已生成并保存到", output_folder)