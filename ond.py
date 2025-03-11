import os
import platform

import requests
import time
from tabulate import tabulate

def get_secid(stock_code):
    """将股票代码转换为东方财富接口所需的secid格式"""
    if stock_code.startswith(('sh', 'sz')):
        market = 1 if stock_code.startswith('sh') else 0
        code = stock_code[2:]
    else:
        if stock_code.startswith('6'):
            market = 1
        elif stock_code.startswith(('0', '3')):
            market = 0
        else:
            raise ValueError(f"无效的股票代码：{stock_code}")
        code = stock_code
    return f"{market}.{code}"


def fetch_stock_data(stock_code):
    """获取单只股票的行情数据"""
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Referer": "https://quote.eastmoney.com/"
    }
    params = {
        "secid": get_secid(stock_code),
        "fields": "f43,f44,f45,f46,f47,f48,f57,f58,f60,f84,f116,f169",
        "ut": "fa5fd1943c7b386f172d6893dbfba10b",
        "invt": 2,
        "fltt": 2
    }

    try:
        response = requests.get(
            "https://push2.eastmoney.com/api/qt/stock/get",
            params=params,
            headers=headers,
            timeout=10
        )
        response.raise_for_status()
        json_data = response.json()

        if not json_data.get('data'):
            return None

        data = json_data['data']
        processed = {
            "name": data.get("f58", "N/A"),
            "code": data.get("f57", stock_code),
            "latest": data.get("f43", 0) if data.get("f43") is not None else 0.0,
            "change_percent": data.get("f169", 0) / data.get("f60", 0) * 100,
            "high": data.get("f44", 0) if data.get("f44") is not None else 0,
            "low": data.get("f45", 0) if data.get("f45") is not None else 0,
            "open": data.get("f46", 0) if data.get("f46") is not None else 0,
            "prev_close": data.get("f60", 0) if data.get("f60") is not None else 0,
            "volume": data.get("f47", 0) / 10000,  # 转换为万手
            "turnover": data.get("f48", 0) / 1e8,  # 转换为亿元
            "turnover_rate": data.get("f84", 0),
            "market_cap": data.get("f116", 0) / 1e8  # 转换为亿元
        }
        return processed
    except Exception as e:
        print(f"股票 {stock_code} 查询失败: {str(e)}")
        return None


def display_stocks(stock_codes):
    """展示股票行情信息"""
    headers = ["名称",
               # "代码",
               "最新价",
               "涨跌幅%",
               # "最高",
               # "最低",
               # "今开",
               # "昨收",
               # "成交量(万手)",
               # "成交额(亿元)",
               # "换手率%",
               # "市值(亿元)"
               ]
    rows = []

    for code in stock_codes:
        stock_data = fetch_stock_data(code)
        if stock_data:
            rows.append([
                stock_data["name"],
                # stock_data["name"][:2],
                # stock_data["code"],
                f"{stock_data['latest']:.2f}",
                f"{stock_data['change_percent']:.2f}%",
                # f"{stock_data['high']:.2f}",
                # f"{stock_data['low']:.2f}",
                # f"{stock_data['open']:.2f}",
                # f"{stock_data['prev_close']:.2f}",
                # f"{stock_data['volume']:.2f}",
                # f"{stock_data['turnover']:.2f}",
                # f"{stock_data['turnover_rate']:.2f}%",
                # f"{stock_data['market_cap']:.2f}"
            ])

    print(tabulate(rows, tablefmt="grid"))
    # for item in rows:
    #     print(item)


def clear_screen():
    # 检查操作系统类型
    if platform.system() == "Windows":
        os.system('cls')  # Windows 系统使用 'cls'
    else:
        os.system('clear')  # Unix/Linux 系统使用 'clear'


if __name__ == "__main__":
    # 在此处添加需要查询的股票代码（支持格式：600000、sh600000、sz000001）"000795", "601127"
    stock_list = ["601127"]
    # 设置循环执行的时间间隔（以秒为单位）
    interval = 5  # 例如，每10秒执行一次

    while True:
        print(f"{time.strftime('%Y-%m-%d %H:%M:%S')}")
        display_stocks(stock_list)
        time.sleep(interval)
        clear_screen()
