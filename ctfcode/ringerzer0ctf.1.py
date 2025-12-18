import requests
from bs4 import BeautifulSoup
import re

base_url = "https://challenges.ringzer0team.com:10032"
def solve_ringzer0_challenge():


    # 第一步：获取初始页面
    response = requests.get(base_url)
    soup = BeautifulSoup(response.content, "lxml")

    # 提取数学表达式
    message_text = soup.find('div', class_='message').text.strip()
    print(f"数学表达式: {message_text}")

    # 提取数字
    numbers = re.findall(r'\b(\d+|0x[0-9a-fA-F]+|[01]+)\b', message_text)

    if len(numbers) == 3:
        decimal_num = int(numbers[0])
        hex_num = int(numbers[1], 16)
        binary_num = int(numbers[2], 2)

        result = decimal_num + hex_num - binary_num
        print(f"计算: {decimal_num} + {hex_num} - {binary_num} = {result}")

        # 第二步：提交答案（根据实际网页结构调整）
        # 通常需要找到提交表单的URL和参数
        submit_url = base_url + "?r=" + str(result)
        result_response = requests.get(submit_url)

        # 查看结果
        result_soup = BeautifulSoup(result_response.content, "lxml")
        print("提交结果页面:")
        print(result_soup.prettify())

        return result
    else:
        print("无法提取足够的数字")
        return None


# 执行
result = solve_ringzer0_challenge()
q = requests.get(f"{base_url}/?r=[{result}]")
print(q.text)