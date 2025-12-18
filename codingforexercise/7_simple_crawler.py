"""
简单网页爬虫示例

功能：使用 requests 库爬取网页内容
适用场景：网页数据采集、内容爬取学习
"""

import requests
import time
import random


def simple_fetch(url, headers=None):
    """
    简单的网页获取函数

    参数：
        url: 目标网页 URL
        headers: 请求头（可选）

    返回：
        网页内容或 None
    """
    try:
        # 如果没有提供 headers，使用默认的 User-Agent
        if headers is None:
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }

        print(f"[*] 正在爬取: {url}")

        # 发送 GET 请求
        response = requests.get(url, headers=headers, timeout=10)

        # 检查响应状态码
        if response.status_code == 200:
            print(f"[√] 爬取成功！状态码: {response.status_code}")
            print(f"[√] 内容长度: {len(response.content)} 字节\n")
            return response.content.decode('utf-8')
        else:
            print(f"[!] 爬取失败！状态码: {response.status_code}\n")
            return None

    except requests.RequestException as e:
        print(f"[!] 请求出错: {e}\n")
        return None


def fetch_with_retry(url, headers=None, max_retries=3, delay=1):
    """
    带重试机制的网页获取函数

    参数：
        url: 目标网页 URL
        headers: 请求头（可选）
        max_retries: 最大重试次数
        delay: 重试延迟（秒）

    返回：
        网页内容或 None
    """
    for attempt in range(1, max_retries + 1):
        try:
            if headers is None:
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }

            print(f"[*] 第 {attempt} 次尝试爬取: {url}")

            response = requests.get(url, headers=headers, timeout=10)

            if response.status_code == 200:
                print(f"[√] 爬取成功！\n")
                return response.content.decode('utf-8')
            else:
                print(f"[!] 状态码: {response.status_code}")

        except requests.RequestException as e:
            print(f"[!] 请求出错: {e}")

        # 如果不是最后一次尝试，等待后重试
        if attempt < max_retries:
            print(f"[*] {delay} 秒后重试...\n")
            time.sleep(delay)

    print(f"[!] 达到最大重试次数，爬取失败\n")
    return None


def batch_fetch(urls, delay_range=(1, 4), headers=None):
    """
    批量爬取多个网页

    参数：
        urls: URL 列表
        delay_range: 随机延迟范围（秒），例如 (1, 4) 表示 1-4 秒
        headers: 请求头（可选）

    返回：
        结果字典 {url: content}
    """
    results = {}

    print(f"[*] 开始批量爬取 {len(urls)} 个网页")
    print(f"[*] 随机延迟范围: {delay_range[0]}-{delay_range[1]} 秒\n")

    for i, url in enumerate(urls, 1):
        print(f"[{i}/{len(urls)}] 爬取: {url}")

        content = simple_fetch(url, headers)
        results[url] = content

        # 添加随机延迟，避免请求过快被封禁
        if i < len(urls):
            delay = random.uniform(delay_range[0], delay_range[1])
            print(f"[*] 等待 {delay:.2f} 秒...\n")
            time.sleep(delay)

    print(f"[√] 批量爬取完成！成功: {sum(1 for v in results.values() if v)} / {len(urls)}")
    return results


def save_content(content, filename):
    """
    保存网页内容到文件

    参数：
        content: 网页内容
        filename: 保存的文件名
    """
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f"[√] 内容已保存到: {filename}")
    except Exception as e:
        print(f"[!] 保存失败: {e}")


if __name__ == "__main__":
    print("=" * 60)
    print("简单网页爬虫工具")
    print("=" * 60)
    print()

    # 示例1：爬取单个网页
    url = "https://www.douban.com/"

    # 自定义请求头
    custom_headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
    }

    content = simple_fetch(url, headers=custom_headers)

    if content:
        # 显示前 500 个字符
        print("=" * 60)
        print("网页内容预览:")
        print("=" * 60)
        print(content[:500])
        print("...")
        print("=" * 60)

        # 保存到文件
        save_content(content, "webpage.html")

    # 示例2：批量爬取多个网页
    # urls_to_fetch = [
    #     "https://www.example1.com",
    #     "https://www.example2.com",
    #     "https://www.example3.com"
    # ]
    #
    # results = batch_fetch(urls_to_fetch, delay_range=(1, 3))
    #
    # # 保存所有结果
    # for i, (url, content) in enumerate(results.items(), 1):
    #     if content:
    #         save_content(content, f"page_{i}.html")


"""
使用说明：
====================

1. 安装依赖：
   pip install requests

2. 基本用法：
   python 7_simple_crawler.py

3. 功能说明：

   3.1 simple_fetch()：
       - 简单的单页爬取
       - 自动处理 UTF-8 编码
       - 返回网页内容

   3.2 fetch_with_retry()：
       - 带重试机制
       - 可配置重试次数和延迟
       - 更稳定可靠

   3.3 batch_fetch()：
       - 批量爬取多个网页
       - 自动添加随机延迟
       - 避免请求过快被封禁

   3.4 save_content()：
       - 保存网页内容到文件
       - 自动处理编码

4. 请求头 (Headers) 说明：

   User-Agent 是必须的，用于标识浏览器
   常见的 User-Agent：
   - Chrome: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
   - Firefox: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:120.0) Gecko/20100101 Firefox/120.0

   其他常用请求头：
   - Referer: 来源页面
   - Cookie: 登录凭证
   - Accept: 接受的内容类型

5. 延迟策略：

   为什么要添加延迟？
   - 避免对服务器造成过大压力
   - 防止被识别为机器人
   - 避免 IP 被封禁

   推荐延迟：
   - 普通网站：1-3 秒
   - 大型网站：2-5 秒
   - 随机延迟更好（模拟人类行为）

6. 状态码说明：
   - 200: 成功
   - 301/302: 重定向
   - 403: 禁止访问
   - 404: 页面不存在
   - 500: 服务器错误
   - 503: 服务不可用

7. 错误处理：
   - 网络超时
   - 连接错误
   - 编码错误
   - 建议使用 try-except 捕获异常

8. 应用场景：
   - 数据采集
   - 内容监控
   - 价格追踪
   - 新闻聚合
   - 学术研究

9. 进阶功能：

   9.1 使用代理：
       proxies = {
           'http': 'http://proxy.com:8080',
           'https': 'https://proxy.com:8080'
       }
       requests.get(url, proxies=proxies)

   9.2 处理 Cookie：
       session = requests.Session()
       session.get(login_url, data=login_data)
       session.get(target_url)

   9.3 处理 JSON 数据：
       response = requests.get(api_url)
       data = response.json()

   9.4 下载文件：
       response = requests.get(file_url, stream=True)
       with open('file.zip', 'wb') as f:
           for chunk in response.iter_content(chunk_size=8192):
               f.write(chunk)

10. 注意事项：
    - 遵守网站的 robots.txt 规则
    - 尊重网站的爬取政策
    - 不要频繁请求同一网站
    - 注意个人信息保护
    - 遵守相关法律法规

11. 法律声明：
    ⚠️  爬虫应仅用于学习和合法用途
    ⚠️  不得用于商业目的或侵犯他人权益
    ⚠️  遵守网站服务条款和相关法律

12. 优化建议：
    - 使用异步请求（aiohttp）提高效率
    - 使用多线程/多进程加速
    - 添加日志记录
    - 使用数据库存储结果
    - 实现断点续爬功能

13. 常见问题：

    Q: 为什么爬取失败？
    A: 检查 URL、网络连接、User-Agent、是否需要登录

    Q: 如何处理动态网页？
    A: 使用 Selenium 或 Playwright 模拟浏览器

    Q: 如何应对反爬虫？
    A: 使用代理池、降低请求频率、模拟真实用户行为
"""
