#a = int(input("请输入一个数"))
#if a % 2 == 0 :
#    print(f'a为偶数')
#else :
#    print(f'a为奇数')

# result_list = []
# for i in range(2000,3200):
#     if(i%7==0) and (i%5!=0):
#         result_list.append(i)
# print(result_list)

# f-string 示例
"""name = "世界"
print(f"1. f-string: 你好, {name}!")
print(f"   计算: 1 + 2 = {1 + 2}\n")

# r-string 示例
normal_path = "C:\new\test.txt"  # 这里 \n 和 \t 会被转义
raw_path = r"C:\new\test.txt"    # 这里则会原样输出
print("2. 普通字符串:", normal_path)
print("   raw字符串:", raw_path, "\n")

# b-string 示例
byte_data = b'Python'
print("3. b-string 类型:", type(byte_data))
print("   内容:", byte_data, "\n")

# u-string 示例 (在Python3中与不加u无区别)
unicode_str = u"这是Unicode字符串"
print("4. u-string:", unicode_str)"""
import requests

"""强转类型直接在通过其他变量名把旧变量名写入
a = 123
b = "hello"
c = 1.23
d = True
print(type(a))
print(type(b))
print(type(c))
print(type(d))
<class 'int'>
<class 'str'>
<class 'float'>
<class 'bool'>
<class 'float'>
print(type(float(a)))
"""
#f = float(input("请输入华氏度"))
#c = (f - 32) / 1.8
#print(f'{f:.2f}华氏度 = {c:.2f}设氏度')

"""match...case 是 Python 3.10 版本中引入的一种强大的结构模式匹配语法，它远比其他语言中的 switch 语句强大。
它不仅可以匹配简单的值，还能匹配数据的结构、类型，并能从复杂的数据类型中提取变量。"""

"""a = float(input("请输入a的值"))
b = float(input("请输入b的值"))
c = float(input("请输入c的值"))
if (a + b > c) and (a + c > b) and (b + c > a):
    zhouchang =  a + b + c
    print(f'周长: {zhouchang}')
    s = (a + b + c) / 2
    area = (s * (s - a) * (s - b) * (s - c)) ** 0.5
    print(f'面积: {area}')
else :
    print("这些无法组成三角形")"""
"""for i in range(1, 10):
    for j in range(1, 10):
        print(f"{i} * {j} = {i * j}",end = '\t')
    print(  ) """

'''import base64
a = "SXpVRlF4TTFVelJtdFNSazB3VTJ4U1UwNXFSWGRVVlZrOWNWYzU="
jiema = base64.b64decode(a)
print(jiema)
 
 IzUFQxM1UzRmtSRk0wU2xSU05qRXdUVVk9cVc5 '''
# import requests
# import hashlib
# from bs4 import BeautifulSoup
# import re
# url="http://challenges.ringzer0team.com:10013"
# response = requests.get(url)
# soup = BeautifulSoup(response.text, "lxml")
# a=soup.find_all("<br/>",class_="message")
#
# pattern = r'----- BEGIN MESSAGE -----(.*?)----- END MESSAGE -----'
# match = re.search(pattern, text, re.DOTALL)

# import requests
# from bs4 import BeautifulSoup
# import re
# url="http://challenges.ringzer0team.com:10032"
# soup = BeautifulSoup(requests.get(url).text, "lxml")
# a = soup.find_all('div')
# print(a)
#
# for i,t in enumerate(a):
#     print(f"{i}. {t.text.strip()}")
# X =re.findall(r'\b(\d+|0x[0-9a-fA-F]+|[01]+)\b')

# import requests
# from bs4 import BeautifulSoup
# import re
#
# base_url = "http://challenges.ringzer0team.com:10032"
# def solve_ringzer0_challenge():
#
#
#     # 第一步：获取初始页面
#     response = requests.get(base_url)
#     soup = BeautifulSoup(response.content, "lxml")
#
#     # 提取数学表达式
#     message_text = soup.find('div', class_='message').text.strip()
#     print(f"数学表达式: {message_text}")
#
#     # 提取数字
#     numbers = re.findall(r'\b(\d+|0x[0-9a-fA-F]+|[01]+)\b', message_text)
#
#     if len(numbers) == 3:
#         decimal_num = int(numbers[0])
#         hex_num = int(numbers[1], 16)
#         binary_num = int(numbers[2], 2)
#
#         result = decimal_num + hex_num - binary_num
#         print(f"计算: {decimal_num} + {hex_num} - {binary_num} = {result}")
#
#         # 第二步：提交答案（根据实际网页结构调整）
#         # 通常需要找到提交表单的URL和参数
#         submit_url = base_url + "?r=" + str(result)
#         result_response = requests.get(submit_url)
#
#         # 查看结果
#         result_soup = BeautifulSoup(result_response.content, "lxml")
#         print("提交结果页面:")
#         print(result_soup.prettify())
#
#         return result
#     else:
#         print("无法提取足够的数字")
#         return None
#
#
# # 执行
# result = solve_ringzer0_challenge()
# q = requests.get(f"{base_url}/?r=[{result}]")
# print(q.text)

# d = 0
# for a in range(0,256):
#     for b in range(0,256):
#         for c in range(0,256):
#             if (c > a and c > b and c != a and c !=b) :
#                 d = d + 1
#             else:
#                 continue
# print(d)


