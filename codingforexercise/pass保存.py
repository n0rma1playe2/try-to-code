import json
import os
import hashlib
import base64
FILE = "data.json"
if os.path.exists(FILE):
    with open(FILE,'r',encoding='utf-8')as f:
        try:
            old_data = json.load(f)
        except json.JSONDecodeError:
            old_data = {}
else:
    old_data = {}

print("-"*20)
service = input("请输入你需要保存的服务名:\n")
password = input("请输入你需要保存的密码:\n")

old_data[service] = password #关键把新数据存入旧字典(更新字典)

with open(FILE,'w',encoding='utf-8')as f:
    json.dump(old_data,f,indent=4,ensure_ascii=False)
    
print(f"成功保存！当前有{len(old_data)}条密码")

    
    
