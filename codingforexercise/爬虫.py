import requests
url = input("请输入你要爬取的地址")
headers = input("请输入你的UA")
parameter = {}
def zhanghaomima ():
   print("若需要输入账号密码，请输入账号密码的参数，用逗号分隔,例如：username,password，,输入y下一步,输入q退出")
   userinput = input()
   if (userinput.lower() == 'q' ):
       return None
   elif (userinput.lower() == 'y' ) :
        n = input("这里输入你的输入次数")
        for _ in range(n):
            user = input("这里输入账号")
            passwd = input("这里输入密码")
            parameter[user] = passwd
            print(parameter[user])
   else :
        print("输入错误，请重新输入")
        return zhanghaomima()

def spider(wangzhi,qingqiutou,canshu):
    url = wangzhi
    headers = qingqiutou
    parameter = canshu
    r = requests.get(url,headers,parameter)
    if (r.status_code) == 200 :
        print(r.content.decode('utf-8'))
    else :
        print(r.status_code)

url = input("请输入你要爬取的地址")
headers = {"User-Agent":input("请输入你的UA")}
parameter = zhanghaomima()
