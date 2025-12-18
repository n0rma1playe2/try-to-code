"""
商城页面遍历查找脚本

功能：遍历商城页面，查找特定内容
适用场景：CTF、自动化查找特定商品或信息
"""

import requests
import time


def find_item_in_shop(base_url, target_keyword, max_pages=500, delay=0.05):
    """
    遍历商城页面查找特定关键词

    参数：
        base_url: 商城基础 URL（不含页码）
        target_keyword: 要查找的关键词
        max_pages: 最大遍历页数
        delay: 请求间隔（秒），避免请求过快

    返回：
        找到的页码，未找到返回 None
    """
    print(f"[*] 开始遍历商城页面...")
    print(f"[*] 查找关键词: {target_keyword}")
    print(f"[*] 最大页数: {max_pages}\n")

    for i in range(1, max_pages + 1):
        payload = base_url + str(i)

        try:
            # 添加延迟避免请求过快
            time.sleep(delay)

            # 发送请求
            r = requests.get(url=payload, timeout=10)

            # 检查是否包含目标关键词
            if target_keyword in r.text:
                print(f"[√] 找到了！{target_keyword} 在第 {i} 页")
                return i

            # 显示进度
            if i % 10 == 0:
                print(f"[*] 已检查 {i} 页...")

            time.sleep(delay)

        except requests.RequestException as e:
            print(f"[!] 第 {i} 页请求失败: {e}")
            continue

    print(f"[!] 遍历完 {max_pages} 页，未找到 {target_keyword}")
    return None


if __name__ == "__main__":
    # 使用示例（需要替换为实际的 URL）
    shop_url = "http://example.com/shop?page="
    target = "lv6.png"

    print("=" * 50)
    print("商城页面遍历工具")
    print("=" * 50)

    # 执行查找
    result_page = find_item_in_shop(
        base_url=shop_url,
        target_keyword=target,
        max_pages=500,
        delay=0.05
    )

    print("\n" + "=" * 50)
    if result_page:
        print(f"[√] 查找成功！目标在第 {result_page} 页")
        print(f"[√] 完整 URL: {shop_url}{result_page}")
    else:
        print("[!] 未找到目标内容")
    print("=" * 50)


"""
使用说明：
====================

1. 安装依赖：
   pip install requests

2. 基本用法：
   python 3_shop_page_finder.py

3. 自定义参数：
   - base_url: 商城页面的基础 URL（例如：http://example.com/shop?page=）
   - target_keyword: 要查找的关键词（例如：商品名称、图片文件名等）
   - max_pages: 最大遍历页数（默认 500）
   - delay: 请求间隔秒数（默认 0.05 秒，避免请求过快被封禁）

4. 工作原理：
   - 从第 1 页开始遍历
   - 逐页请求并检查响应内容
   - 找到关键词后立即返回页码
   - 添加延迟避免请求过快

5. 应用场景：
   - CTF 题目中查找隐藏在大量页面中的 flag
   - 自动化查找商城中的特定商品
   - 批量页面内容检索

6. 优化建议：
   - 根据服务器响应速度调整 delay 参数
   - 如果页面有限，可以减小 max_pages
   - 可以添加多线程加速（注意控制并发数）
   - 可以添加更复杂的匹配逻辑（正则表达式等）

7. 注意事项：
   - 遵守目标网站的访问频率限制
   - 避免对服务器造成过大压力
   - 仅用于授权场景和 CTF 比赛
"""
