"""
Base64 + ROT13 多重解密脚本

功能：对多重加密的字符串进行解密（ROT13 -> 翻转 -> Base64 -> 字符偏移）
适用场景：CTF 密码学题目、多层编码解密
"""

import base64
import string


def rot13_decrypt(text):
    """
    ROT13 解密（大小写字母移位 13 位）

    参数：
        text: 待解密的字符串

    返回：
        解密后的字符串
    """
    upper_dict = {}
    lower_dict = {}
    upper_letters = string.ascii_uppercase
    lower_letters = string.ascii_lowercase

    # 构建 ROT13 映射字典
    for i in range(len(lower_letters)):
        if i < 13:
            lower_dict[lower_letters[i]] = lower_letters[i + 13]
        else:
            lower_dict[lower_letters[i]] = lower_letters[i - 13]

    for i in range(len(upper_letters)):
        if i < 13:
            upper_dict[upper_letters[i]] = upper_letters[i + 13]
        else:
            upper_dict[upper_letters[i]] = upper_letters[i - 13]

    # 执行转换
    result = []
    for ch in text:
        if ch in lower_dict:
            result.append(lower_dict[ch])
        elif ch in upper_dict:
            result.append(upper_dict[ch])
        else:
            result.append(ch)

    return ''.join(result)


def multi_layer_decrypt(encrypted_text):
    """
    多层解密流程

    解密顺序：
    1. ROT13 解密
    2. 字符串翻转
    3. Base64 解码
    4. 字符 ASCII 值 -1

    参数：
        encrypted_text: 加密的字符串

    返回：
        解密后的明文
    """
    print(f"[*] 原始密文: {encrypted_text}\n")

    # 步骤 1: ROT13 解密
    step1 = rot13_decrypt(encrypted_text)
    print(f"[1] ROT13 解密后: {step1}")

    # 步骤 2: 字符串翻转
    step2 = step1[::-1]
    print(f"[2] 翻转后: {step2}")

    # 步骤 3: Base64 解码
    try:
        step3 = base64.b64decode(step2.encode('utf-8'))
        print(f"[3] Base64 解码后: {step3}")
    except Exception as e:
        print(f"[!] Base64 解码失败: {e}")
        return None

    # 步骤 4: 字符 ASCII -1
    plaintext = ""
    for i in range(len(step3)):
        d = step3[i:i+1]
        c = ord(d) - 1
        plaintext = plaintext + chr(c)

    print(f"[4] ASCII -1 后: {plaintext}")

    # 步骤 5: 再次翻转得到最终明文
    final_text = plaintext[::-1]
    print(f"[5] 最终翻转后: {final_text}")

    return final_text


if __name__ == "__main__":
    # 使用示例
    encrypted = "a1zLbgQsCESEIqRLwuQAyMwLyq2L5VwBxqGA3RQAyumZ0tmMvSGM2ZwB4tws"

    print("=" * 60)
    print("多重加密解密工具 (ROT13 + 翻转 + Base64 + ASCII)")
    print("=" * 60)

    result = multi_layer_decrypt(encrypted)

    print("\n" + "=" * 60)
    if result:
        print(f"[√] 解密成功！")
        print(f"[√] 最终明文: {result}")
    else:
        print("[!] 解密失败")
    print("=" * 60)


"""
使用说明：
====================

1. 安装依赖：
   无需额外安装，使用 Python 标准库

2. 基本用法：
   python 4_multi_decrypt.py

3. 自定义解密：
   修改 encrypted 变量为你要解密的字符串

4. 加密流程（逆向理解）：
   原文 -> 翻转 -> ASCII +1 -> Base64 编码 -> 翻转 -> ROT13 -> 密文

5. 解密流程：
   密文 -> ROT13 -> 翻转 -> Base64 解码 -> ASCII -1 -> 翻转 -> 明文

6. ROT13 说明：
   - 字母表移位 13 位的替换加密
   - A->N, B->O, ..., N->A, O->B, ...
   - 大小写分别处理
   - 数字和特殊字符不变

7. 应用场景：
   - CTF Crypto 题目
   - 多层编码的数据还原
   - 混淆字符串的解密

8. 扩展功能：
   可以根据实际加密方式调整解密步骤顺序和方法：
   - 修改 ASCII 偏移量
   - 添加其他编码方式（如 URL 编码、十六进制等）
   - 调整翻转和 ROT13 的顺序

9. 调试建议：
   - 观察每一步的输出结果
   - 根据中间结果判断解密方向是否正确
   - 如果某一步失败，可能是加密顺序不同
"""
