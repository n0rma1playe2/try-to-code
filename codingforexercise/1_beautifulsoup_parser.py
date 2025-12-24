"""
BeautifulSoup 网页解析示例脚本

功能：使用 BeautifulSoup 库解析网页内容
适用场景：网页爬取、HTML 解析
"""

import requests
from bs4 import BeautifulSoup


def parse_webpage(url):
    """
    解析指定 URL 的网页内容

    参数：
        url: 目标网页地址

    返回：
        BeautifulSoup 对象
    """
    try:
        res = requests.get(url=url)
        res.raise_for_status()  # 检查请求是否成功

        # 使用 lxml 解析器（速度快，需要安装 lxml）
        soup = BeautifulSoup(res.content.decode('utf-8'), "lxml")

        return soup
    except Exception as e:
        print(f"请求失败: {e}")
        return None


if __name__ == "__main__":
    # 使用示例
    url = 'http://www.douban.com'
    soup = parse_webpage(url)

    if soup:
        print(soup.prettify()[:500])  # 打印前500个字符

        # 你可以在这里添加更多解析逻辑，例如：
        # title = soup.find('title')
        # links = soup.find_all('a')
        # print(f"页面标题: {title.text if title else '未找到'}")


"""
使用说明：
====================

1. 安装依赖：
   pip install requests beautifulsoup4 lxml

2. 基本用法：
   python 1_beautifulsoup_parser.py

3. 自定义使用：
   修改 url 变量为你想要解析的网页地址

4. 常用解析方法：
   - soup.find('tag')          # 查找第一个标签
   - soup.find_all('tag')      # 查找所有标签
   - soup.select('css选择器')   # 使用 CSS 选择器
   - soup.get_text()           # 获取所有文本内容

5. 注意事项：
   - 确保目标网站允许爬取
   - 遵守 robots.txt 规则
   - 添加适当的请求头避免被封禁
"""
