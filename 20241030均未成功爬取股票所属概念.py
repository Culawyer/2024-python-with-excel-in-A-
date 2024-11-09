import requests
from bs4 import BeautifulSoup


def get_stock_concepts(stock_code):
    url = f"https://xueqiu.com/S/{stock_code}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/94.0.4606.61 Safari/537.36"
    }

    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print("无法访问页面")
        return None

    soup = BeautifulSoup(response.text, 'html.parser')
    concepts = []
    for concept in soup.find_all("a", class_="tag"):  # 根据实际结构调整
        concepts.append(concept.get_text())

    return concepts


# 测试获取某个股票的概念
stock_code = "600519"  # 替换为您想要查询的股票代码
concepts = get_stock_concepts(stock_code)
print(f"股票 {stock_code} 所属概念：", concepts)
