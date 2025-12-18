import requests

# 1. API 的基础 URL
base_url = "https://api.openweathermap.org/data/2.5/weather"

# 2. 获取用户输入
city = input('请输入你的城市名 (例如 beijing): ')

# 3. 你的 API Key (请确保它是有效的)
api_key = 'baa7aa7aa3ba72c78e81a29a2a32972e' 

# 4. 创建正确的参数字典
# 格式是 '键': 值
params = {
    'q': city,
    'appid': api_key,
    'units': 'metric', # API 文档要求是 'units' 而不是 'unit'
    'lang': 'zh_cn'  # (可选) 添加这个参数可以让描述变成中文
}

print(f"正在查询城市: {city} ...")

try:
    # 5. 发送 GET 请求，同时传入 URL 和参数
    response = requests.get(base_url, params=params)
    
    # 检查 HTTP 状态码，如果不是 2xx，则会引发异常
    response.raise_for_status() 

    # 6. 解析 JSON 数据
    data = response.json()

    # 7. 提取并打印所需信息
    weather_description = data['weather'][0]['description']
    current_temperature = data['main']['temp']

    print("\n查询成功！")
    print(f"天气状况: {weather_description}")
    print(f"当前温度: {current_temperature}°C")

# 8. 捕获可能发生的错误
except requests.exceptions.HTTPError as err:
    if response.status_code == 404:
        print(f"错误：找不到城市 '{city}'。请检查拼写是否正确。")
    elif response.status_code == 401:
        print("错误：API Key 无效或未激活。请检查你的 Key。")
    else:
        print(f"请求失败，HTTP 错误: {err}")
except requests.exceptions.RequestException as err:
    print(f"请求发生网络错误: {err}")
except KeyError:
    print("错误：返回的数据格式不符合预期，无法解析天气信息。")