# import requests

# url = "https://www.baidu.com"
# response=requests.get(url)
# print(response.text)
# class person:
#     pass
# p = person()
# print(p)
# class newperson:
#     def sayhi(self):
#         print("hello")
# p1 = newperson()
# p1.sayhi()


# count = 2
# total = 0
# while (count < 100):
#     if count % 2 == 0:
#         total -= count
#     else:
#         total += count
#     count += 1
#     print(total)

# import random
# secret = random.randint(1,100)
# print("guess the number")
# truenum = int(input("enter you number"))
# while True:
#     truenum = int(input("enter you number"))
#     if (truenum > secret):
#         print("bigger guess")
#     elif (truenum < secret):
#         print("smaller guess")
#     else:
#         print("you guess right")
#         break

# """ 练习列表
# todo = []
# while True:
#     print("\n请选择操作")
#     print("1.注意事项")
#     print("2.查看所有事项")
#     print("3.删除事项")
#     print("4.删除程序")
#
#     choice = input("请输入你的选择")
#     if choice == "1": #添加事项
#         item= input("请输入要添加的事项")
#         todo.append(item)
#         print(f"{item}已成功添加")
#     elif choice == "2": #查看事项
#         if not todo:
#             print("当前没有待办事项")
#         else :
#             for index,item in enumerate(todo):
#                 print(f"{index+1}. {item}")
#         print("-------------------------------")
#     elif choice == "3":
#         if not todo:
#             print("没有事项删除")
#             continue
#         try:
#             for index,item in enumerate(todo):
#                 print(f"{index+1}. {item}")
#
#             item_num=int(input("请输入要删除的事项编号"))
#
#             if 1 <= item_num <= len(todo):
#                 remove_item = todo.pop(item_num - 1)
#                 print(f"{remove_item}已被删除")
#             else :
#                 print("无效编号")
#         except ValueError:
#             print("请输入正确编号")
#     elif choice == "4":
#         print("感谢使用")
#         break
#     else :
#         print("无效选择") """
# from http.client import responses

# from prometheus_client.decorator import append

# word_counts= {}
# print("单词计数器")
# try:
#     with open("encode.txt",'r') as file:
#         for line in file:
#             words = line.strip().lower().split()
#             for word in words:
#                 if word in word_counts:
#                     word_counts[word] += 1
#                 else:
#                     word_counts[word] = 1
#
#
#     print("result below")
#     for word,count in word_counts.items():
#         print(f"{word}: {count}次")
#
# except FileNotFoundError:
#     print("请确保脚本文件在同一文件夹下")

#练习
# chengji ={}
# while True:
#     print("开始运行学生成绩管理系统，请选择你所需要的功能")
#     print("1.录入成绩")
#     print("2.查询成绩")
#     print("3.显示成绩单")
#     print("4.计算平均分")
#     print("5.删除学生")
#     print("6.退出系统")
#     num = int(input("此处输入功能代码"))#这里需要使用try except来防止valueerror
#     if num == 1:
#         stdname=input("请输入你录入学生的姓名")
#         grade =int(input("请输入你所需要写入的成绩"))
#         if stdname in chengji:
#             print(f"{stdname}已存在，成绩将从{chengji[stdname]}更新为{grade}")
#         else :
#             print(f"为{stdname}新生录入")
#         try:
#             chengji[stdname]=grade
#             print(f"已成功录入{stdname}为{grade}")
#         except ValueError:
#             print("错误，数字不有效")
#             continue
#     elif num == 2:
#         print("请输入你所要查询的学生名字")
#         stdname1 = input("这里输入学生名字")
#         if stdname1 in chengji:
#             grade1 = chengji[stdname1]
#             print(f"{chengji}的成绩是{grade1}")
#         else:
#             print("此学生不存在，请重新输入")
#             continue
#     elif num == 3:
#         print(f"以下为成绩单{chengji}")
#         continue
#     elif num == 4:
#         if not chengji:
#             print("当前没有成绩，无法计算")
#         else:
#             all_score = chengji.values()
#             total = sum(all_score)
#             count = len(chengji)
#             avg = total/count
#             print(f"{count},{avg}")
#             continue
#     elif num == 5:
#         print("请输入你要删除的学生")
#         stdname2 = input("这里输入你要删除的学生名字")
#         if stdname2 in chengji:
#             re =  chengji.pop(stdname2)
#             print(f"{stdname2}的{re}已被删除")
#         else :
#             print(f"字典里没有{stdname2}的成绩")
#             continue
#     elif num == 6:
#         print("感谢使用")
#         break
#     else:
#         if num not in [1,2,3,4,5,6]:
#             print("无效应用代码，请重新输入")
#             continue

# name = "\tsteam \neric"
# print(name.lstrip()) #（）内部放参数 l为左 r为右 默认清除空格
# print(name.rstrip())
# print(name.strip())

# 将任意两个数相除时，结果总是浮点数，即便这两个数都是整数且能整除：
# >> > 4 / 2
# 2.0
#
# 在其他任何运算中，如果一个操作数是整数，另一个操作数是浮点数，结果也总是浮点
# 数：
# >> > 1 + 2.0
# 3.0
# >> > 2 * 3.0
# 6.0
# >> > 3.0 ** 2
# 9.0
#
# 无论是哪种运算，只要有操作数是浮点数，Python默认得到的总是浮点数，即便结果原
# 本为整数也是如此。
# universal_number =14_000_000_000
# print(universal_number) #当你打印这种使用下划线定义的数时，Python不会打印其中的下划线
# import this #python之禅
# print(this.d)
# MAXNUM = 1000 #在代码中，要指出应将特定的变量视为常量，可将其字母全部大写。
# x,y,z =0,0,0#可以这样进行赋值

# m = ['1','2',"3"]
# print(m[0])
# m[0]= 5 #可任意修改列表任意序列的值
# print(m[0])
# m.append("4")#在末尾插入元素
# m.insert(1,"5")#可以选择任意位置插入元素
#
# del m[0] #可以选择索引来删除元素
# m.pop()#删除末尾的元素  可以选择索引()
#  #如果你不确定该使用del 语句还是pop() 方法，下面是一个简单的判断标准：如果
# # 你要从列表中删除一个元素，且不再以任何方式使用它，就使用del 语句；如果你要在删除元素后还能继续使用它，就使用方法pop()
# m.remove("4")#根据值来进行删除 但是只能删除第一个指定的值,多个需要循环
# pl = ["re","12","dfda","231"]
# print(f"{pl}是我邀请的人")
# print(f"{pl[0]}无法收到邀请")
# del pl[0]
# print(f"{pl}是最新名单")

# s = ['scss',"da",'12',"a"]
# print(sorted(s)) #sort和sorted进行排序,sort永久进行排序,sorted进行临时排序
# sorted(s).reverse() #reverse=True：我要降序排列 reverse()：把这个列表倒过来
# s.sort(reverse=True)
#title()方法是首字母大写,其余小写

# pizzas = ['fruit','bake','pepperoni']
# for pizza in pizzas:
#     print(f"i like {pizza} pizza")

# nums = []
# for num in range(1,1000001):
#     nums.append(num)
# print(nums)
# print(max(nums))
# print(min(nums))
# print(sum(nums))

#切片
# qiepian = ['1','sdhj','123sd','fsdaas','safdhjd']
# print(qiepian[1:4])
# print(qiepian[-3:])#从开头开始往倒数第一个数，不及第一个
# print(qiepian[:-3])#

# #🎯 易错点2：负索引就像"倒数座位"
# 座位 = ['小明', '小红', '小刚', '小丽', '小王']
# # 正索引: 0      1      2      3      4
# # 负索引: -5     -4     -3     -2     -1
# #         ↑      ↑      ↑      ↑      ↑
# #      "第一排" "第二排" "第三排" "倒数第二" "倒数第一"
# #易错：[-3:-1] 不包含最后一个！
# print(座位[-3:-1])  # ['小刚', '小丽'] 没有小王！
# # 从倒数第三个小刚开始，到倒数第一个小王前结束
#
# nu = ['charles','marina','michael','florence','eli']
# print("Here are the first three players on my team:")
# for player in nu[:3]:
#     print(player.title())
#
# old = nu[:] #适用于一维数组，需要使用独立的副本时




# people ={"city":"beijing","age":5,"first_name":"ni","last_name":"ge"}
# # print(people["city"])
# # print(people["age"])
# # print(people["first_name"])
# # print(people["last_name"])
# for k,v in people.items():
#     print(f"{k},{v}分别是key和value")#遍历所有键值对
# # .items() 方法：
# # 返回字典中所有键值对的视图
# # 每个键值对是一个元组 (key, value)
# #如果指定的键有可能不存在，应考虑使用方法get() ，而不要使用方括号表示法。
#
# for k in people.keys(): #遍历字典时会默认遍历所有的键
#     print(k.title())
# for v in people.values():
#     print(v.title())
#
# print(sorted(people.items()))#列出键之前把键进行的顺序进行排序

#
# p = {"f":1,"s":2,"t":3,"f":1}
# for l in set(p.values()):#为剔除重复项，可使用集合set()
#     print(l)

#列表储存在字典中，或者字典储存在列表中，甚至在字典里嵌套字典，这个被称作嵌套
# aliens = []
# for i in range(30):
#     new = {'color':"red","speed":100,"points":6}
#     aliens.append(new)
#
# print(aliens)

# pizza = { #字典里插入列表
#     'crust':'thick',
#     'toppings':['mushrooms','extra cheese'],
# }
# print(f"You ordered a {pizza['crust']}-crust pizza "
#       "with the following toppings:")
#
# for topping in pizza['toppings']:#遍历字典里的列表
#     print(""+topping)
#
# users = { #字典嵌套字典
#     'aeinstein': {
#         'first': 'albert',
#         'last': 'einstein',
#         'location': 'princeton',
#     },
#
#     'mcurie': {
#         'first': 'marie',
#         'last': 'curie',
#         'location': 'paris',
#     },
#
# }
#
# for username, user_info in users.items():
#     print(f"\nUsername: {username}")
#     full_name = f"{user_info['first']} {user_info['last']}"
#     location = user_info['location']
#     print(f"\tFull name: {full_name.title()}")
#     print(f"\tLocation: {location.title()}")

# unconfirmed_users = ['alice','brain','candace']
# confirmed_users = []
#
# while unconfirmed_users:
#     current_user = unconfirmed_users.pop()
#     print(f"Verifying user :{current_user.title()}")
#     confirmed_users.append(current_user)
#
# print("\nThe following users are confirmed:")
# for confirmed in confirmed_users:
#     print(f"there are confirmed users:{confirmed.title()}")

# pets = ['dog', 'cat', 'dog', 'goldfish', 'cat', 'rabbit', 'cat']
# print(pets)
# while 'cat' in pets:
#     pets.remove('cat')
# print(pets)

# re = {}
# con = True
# while con:
#     name = input("\nplease input your name")
#     r = input("please input your favorite hobby")
#
#     re[name] = r
#
#     repeat = input("\ncontinue?(yes or no) ")
#     if repeat == "no":
#         con = False
# print("\n done survey")
# for i in re:
#     print(re)

# def display_message(p):
#     print(p)
# q = "function"
# display_message(q)
#
# def favorite_book(title):
#     print(f"one of my favorite books is {title}")
#
# b = "green tale"
# favorite_book(b)

#传递实参的方法分别为 位置实参，关键字实参和默认参数
# def describe_pet(animal_type,pet_name): #此处位置实参有问题导致输出相反
#     print(f"\n I have a {animal_type}.")
#     print(f"my {animal_type}'s name is {pet_name.title()}")
#
# describe_pet('harry','hamaster')

# def describe_pet(animal_type,pet_name):
#     print(f"\n I have a {animal_type}.")
#     print(f"my {animal_type}'s name is {pet_name.title()}")
# describe_pet(animal_type='hamaster',pet_name='harry')#此处关键字的顺序无须专门进行调整

# def describe_pet(pet_name,animal_type='dog',):#个函数调用的输出与前一个示例相同。只提供了一个实参'willie' ，这个实参将关联到函数定义中的第一个形参pet_name 。由于没有给animal_type 提供实参，Python将使用默认值'dog' 。
#     print(f"\n I have a {animal_type}.")
#     print(f"my {animal_type}'s name is {pet_name.title()}")
# describe_pet("willie")

# import  random
# import string
#
# all = string.digits + string.ascii_letters
# def genercodes(*,code_len=6):
#     return ''.join(random.choices(all,k=code_len))
# for _ in range(10):
#     print(genercodes())

# def make_shirt(size,string="I love Python"):
#     print(f"这件衣服的尺码是{size}，上面写的是{string}")
#
# make_shirt(size='big')
# make_shirt(size='medium')
# make_shirt('small','wtfwhoami')

# def describe_city(city,country):
#     print(f"{city} is in {country}.")
#
# describe_city('beijng','china')
# def city_counter(city,country):
#     print(f"{city.title()},{country.title()}")
# city_counter("santiago","chile")

# class dog :
#     def __init__(self,name,age):
#         self.name=name
#         self.age=age
#     def sit(self):
#         print(f"{self.name} is now sitting")
#     def roll_over(self):
#         print(f"{self.name} is now rolling over")
#
# new_dog = dog('willie',6)
# new_dog.sit()
# new_dog.roll_over()
# class Restaurant:
#     def __init__(self,name,cuisine):
#         self.name=name
#         self.cuisine=cuisine
#     def describe_restaurant(self):
#         print(f"这是一家{self.name}餐厅，拥有{self.cuisine}菜品")
#     def open_restaurant(self):
#         print(f"这家{self.name}已经开业")
#
# res = Restaurant("zhongye","chaoliji")
# de = res.describe_restaurant()
# op = res.open_restaurant()

# import pizza#通过在一个文件夹下导入写的py文件，就可以在这个文件使用导入文件中所有的函数
# from pizza import make_pizza as pz#导入指定函数 as 可以给模块指定别名 *号导入所有函数
# pizza.make_pizza(16,'pepperoni')
# pizza.make_pizza(12,'mushroom','green pepper','extra cheese')


# import string
# import random
#
# def generete(length:int = 10):#length后面的int=10是参数注解
#     alphabet = string.ascii_letters + string.digits + string.punctuation
#     password =''.join(random.choice(alphabet)for i in range(length))
#     return password


# def is_iris(number:int)->bool:  #水仙花数解一
#     if number > 999 or number < 100 :
#         return False
#     number = str(number)
#     gewei = int(number[2])
#     shiwei = int(number[1])
#     baiwei = int(number[0])
#     if gewei**3 + shiwei**3 + baiwei**3 ==int(number):
#         return True
#     return False
# print(is_iris(153))
# print(is_iris(154))

# def is_iris(number:int)->bool: 
#     if number > 999 or number < 100 :
#         return False
#     number = number
#     gewei = number%10
#     shiwei = number//10%10
#     baiwei = number//10//10%10
#     if gewei**3 + shiwei**3 + baiwei**3 ==number:
#         return True
#     return False
# print(is_iris(153))
# print(is_iris(154))

# a = 11 
# b = 21
# def testfunc():
#     global a # 使用全局a
#     a = 10 
#     b = 20
#     return a,b
# c,d = testfunc()
# print(a,b,c,d)#10 21 10 20

# with open('pi_digits.txt') as file_object:
#     contents = file_object.read()
# print(contents)

# class Car:
#     def __init__(self,make,model,year):
#         self.make = make
#         self.model = model
#         self.year = year
#         self.odometer_reading = 0
    
#     def get_descriptive_name(self):
#         long_name = f'{self.year} {self.make} {self.model}'
#         return long_name.title()
    
#     def read_odometer(self):
#         print(f"This car has {self.odometer_reading} miles on it.")
    
#     def update_odometer(self,mileage):
#         if mileage >= self.odometer_reading:
#             self.odometer_reading = mileage
#         else :
#             print("you can't roll back an odometer!")
    
#     def increment_odometer(self,miles):
#         self.odometer_reading += miles

# class ElectricCar(Car):
#     def __init__(self,make,model,year):#初始化父类的属性
#         super().__init__(make,model,year) #super()是一个特殊的函数，能够调用父类的方法
#         self.battery_size =75
#     def describe_battery(self):
#         print(f"This car has a {self.battery_size}-Kwh battery ")
# my_tesla = ElectricCar('tesla','model s',2019)
# print(my_tesla.get_descriptive_name())
# my_tesla.describe_battery()

# class Restaurant:
#     def __init(self,name,dish,level)
#         self.name = name
#         self.dish = dish
#         self.level = level
#     def pt(self,name,dish,level):
#         print()

# import os 
# print(os.getcwd())

# file = open(r'D:/PythonProject1/网安/text.txt','r')
# print(file.read())
# file.close()

# import socket #套接字
# import sys

# class Client:
#     def __init__(self,host):
#         self.host = host
#     def connet(self):
#         try :
#             s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#         except socket.error as e :
#             print("Failed to create socket.Error: %s"%e)
        
#         sys.exit

# if __name__ == '__main__':
#     cl = Client('www.baidu,com')
#     cl.connet

# import nmap
# nm = nmap.PortScanner()
# nm.scan('127.0.0.1','22-443')

# for host in nm.all_hosts():
#     print('Host : %s (%s)' %(host, nm[host].hostname()) )
#     print('State : %s' % nm[host].state())
#     for proto in nm[host].all_protocols():
#         print('Protocol : %s' % proto)
#         lport = nm[host][proto].keys()
#         for port in lport:
#             print('port : %s\tstate :  %s' % (port,nm[host][porto][port]['state']))


def find_min_max(numbers):
    min = numbers[0]
    max = numbers[0]
    if not numbers:
        return None
    else :
        for i in numbers[1:]:
            if i < min:
                min = i
            if i > max:
                max = i
        return (max,min)
    pass

print(find_min_max([4,2,9,5,7,1]))



