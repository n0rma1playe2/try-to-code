# Python 基础语法学习笔记

## 1. 列表 (List)

列表是序列，支持切片和索引，可以储存任何对象，使用 `[]` 定义。

### 基本操作

```python
list = [1, 3, 2, 4, 5, 6, 7, 8, 9]
print(list)

# 添加元素
list.append(22)  # 对列表数据进行追加，且只能追加在末尾
list.insert(9, 123)  # 根据索引确定插入位置，如果超出范围，就放在最后
list.extend([10, 11])  # 可以添加多个数据（可迭代对象），只能追加在末尾

# 删除元素
list.pop(3)  # 根据索引删除数据，返回值是索引所对应删除的数据
list.remove(3.14)  # 根据值去删除

# 排序和反转
list.reverse()  # 反转列表
list.sort()  # 排序

# 统计和查找
list.count(1)  # 统计元素出现次数
list[2:]  # 支持切片
```

### 列表常用操作

```python
my_list1 = [1, 2, 3]
my_list2 = ["A", "B", "C"]

# 求列表长度
ln = len(my_list1)  # 3

# 合并两个列表
my_list3 = my_list1 + my_list2  # [1, 2, 3, 'A', 'B', 'C']

# 重复列表元素
my_list4 = my_list1 * 3  # [1, 2, 3, 1, 2, 3, 1, 2, 3]

# 判断元素是否在列表内
ex1 = 3 in my_list1  # True
ex2 = 3 in my_list2  # False

# 对列表进行遍历
for x in my_list1:
    print("遍历元素:", x)
```

### 列表推导式

列表推导式运算时间更少，代码更简洁：

```python
# 普通方式
a = []
for i in range(10):
    a.append(i)

# 列表推导式
a = [i for i in range(10)]
```

---

## 2. 元组 (Tuple)

元组是稳固版的列表（里面的数据不能被修改），支持切片和索引，使用 `()` 定义。

```python
# 定义元组
tup = (1, 2, 3, 4, 5)

# 如果元组只有一个数据，需要在后面加上逗号
tup = (1,)

# 元组方法
tup.count()  # 统计元素出现次数
tup.index()  # 输出元素所在的索引值
```

**特点**：
- 元素不可变（不能添加、删除或修改）
- 支持切片和索引
- 访问和遍历操作与列表相似

---

## 3. 字典 (Dictionary)

字典使用 `{}` 定义，必须有键值对，键不能重复且不能修改，值可以修改。当键重复时，以最后的元素为准。

```python
dict = {"k1": "v1", "k2": "v2", "k3": "v3"}

# 删除操作
dict.pop("k2")  # 根据键移除数据，有返回值
del dict["k2"]  # 与 pop() 等效
dict.popitem()  # 从后往前删除数据，一次只能移除一个

# 添加/更新
dict.update({"k3": "v3", "k4": "v4"})  # 可以控制插入变量的数量，把数据添加到末尾

# 遍历
dict.items()  # 把字典里所有的数据依次遍历，键值以元组的形式返回
dict.keys()  # 遍历键
dict.values()  # 遍历值
```

**注意**：字典不是序列，不支持切片和索引

---

## 4. 集合 (Set)

集合可以理解为没有值的字典，不是序列，不支持切片和索引，可以删除增加元素，使用 `{}` 定义。

```python
# 定义集合（不包含数据会被认为是字典，需要至少一个数据）
set = {1}

# 集合特点：不重复、无序
set = {1, 2, 3, 2, 1}  # 自动去重 -> {1, 2, 3}

# 集合操作
set.discard("q1")  # 删除指定元素
set.add("add")  # 没有插入顺序，随机出现在某个位置
```

**特点**：
- 元素不重复（自动去重）
- 无序
- 可以进行集合运算（并集、交集、差集等）

---

## 5. 字符串 (String)

字符串可以使用单引号、双引号、三引号定义。

### 字符串索引和切片

语法：`[start:end:step]`，step 为步长，默认是 1

```python
name = 'zhangsan'

# 索引
print(name[2])  # 'a' - 正向索引
print(name[-3])  # 's' - 反向索引

# 切片
print(name[2:4])  # 'an' - 切片不包含 end 位置的字符
print(name[2:4:2])  # 'a' - 步长为 2
print(name[2:])  # 'angsan' - 输出下标为 2 后面的所有数据
print(name[:5])  # 'zhang' - 输出下标为 5 前面的所有数据
print(name[-3:-1])  # 'sa' - 反向切片，不包含 -1
print(name[::-1])  # 'nasgnazh' - 逆序输出
```

### 字符串常用方法

```python
# 1. capitalize() - 首字母变大写
# 2. endswith/startswith() - 是否以 x 结束/开始
# 3. find(x) - 检测 x 是否在字符串中
# 4. isalnum() - 判断是否是字母和数字
# 5. isalpha() - 判断是否是字母
# 6. isdigit() - 判断是否是数字
# 7. islower() - 判断是否是小写
# 8. join() - 循环取出所有值用 xx 去连接
# 9. lower/upper - 大小写转换
# 10. swapcase - 大写变小写，小写变大写
# 11. lstrip/rstrip/strip - 移除左右两侧空格
# 12. split() - 切割字符串
# 13. title() - 把每个单词的首字母变成大写
# 14. replace(old, new, [max]) - 字符串替换
# 15. count() - 统计出现的次数
```

### 字符串格式化

```python
name = 'zhangsan'

# % 格式化
print('name: %s' % (name * 3))  # s: 字符串, d: 整型, f: 浮点型

# format() 方法
print('{}, 23456{}'.format(a, b))  # a=1, b=7
```

---

## 6. 排序 (sorted)

`sorted()` 函数按照大小、英文字母的顺序给列表中的元素进行排序，不会改变对象本身。

```python
list = [3, 1, 4, 1, 5, 9, 2, 6]

print(sorted(list))  # 正向排序
print(sorted(list, reverse=True))  # 反向排序
print(sorted(list, key=lambda x: -x))  # 使用 lambda 表达式自定义排序
```

---

## 7. Lambda 表达式

Lambda 表达式相当于没有名字的函数，优点是让代码更简洁。

```python
# Lambda 表达式
key = lambda x: -x

# 等价的函数
def test(x):
    return -x

for item in list:
    print(test(item))
```

---

## 8. 循环 (for/while)

### for 循环

```python
# range() 生成数据集合
# 语法：range(起始, 结束, 步长)
# 步长不能为零，只能整数集合，默认起始值为 0，区间为左闭右开

# 正序输出
for i in range(1, 10, 1):
    print(i)

# 反序输出
for i in range(9, 0, -1):
    print(i)
```

### while 循环

容易死循环，建议在不确定循环次数时使用。

```python
# while 循环三要素：
# 1. 有初始值
# 2. 有条件表达式（一般为布尔表达式）
# 3. 循环体内变量自增/自减

i = 0
while i <= 100:
    if i % 2 == 0:
        print(i)
    i += 1
```

---

## 9. 条件判断

### 比较运算符

```python
# >= 和 <= 注意
# 1 >= 2 等价于 1 > 2 or 1 == 2
```

### 布尔运算符优先级

```
() > not > and > or
```

---

## 10. 异常处理

使用 `try/except` 语句处理异常。

```python
try:
    a = int(input("请输入一个整数："))
except ValueError as msg:
    print("请输入整数")
except Exception as e:
    # Exception 能够捕获比较常见的异常
    print(f"发生错误: {e}")
finally:
    # finally 后面的代码一定会执行
    print("程序结束")
```

---

## 11. 文件操作

### 方法1：传统方式

```python
file = open('文件路径', 'w/r/a')  # 地址右斜杠改成左斜杠
file.write("内容")
file.close()

# w: 覆盖原来的数据
# r: 读取
# a: 追加
```

### 方法2：with...as... (推荐)

```python
path = r"文件路径"  # 或者把反斜杠写成正斜杠

with open(path, "r") as file:
    content = file.read()
    print(content)
```

---

## 12. 导入模块

```python
import random  # 随机数模块
import time  # 时间模块
import re  # 正则表达式模块
import os  # 操作系统模块
```

---

## 实用技巧

### 1. 变量命名规则
- 由字母、下划线、数字组成
- 只能由字母和下划线开头
- Python 区分大小写
- `id()` 可以输出存放变量的地址

### 2. 打印技巧

```python
print(a, end=',')  # 输出并最后加逗号
```

### 3. pass 语句

```python
pass  # 代表代码结束（占位符，不重要）
```

---

## 综合示例

### 示例1：九九乘法表

```python
for i in range(1, 10):
    for j in range(1, i + 1):
        print('%d * %d = %d' % (i, j, i * j), end='\t')
    print()
```

### 示例2：猜数字游戏

```python
import random

a = random.randint(0, 100)
x = 0

while x != a:
    x = int(input("请输入一个数字："))

    if x > a:
        print('猜大了')
    elif x < a:
        print('猜小了')
    elif x == a:
        print('猜对了，是 %d' % x)
```

---

**提示**: 这份笔记涵盖了 Python 的核心数据结构和基础语法，适合初学者快速入门。
