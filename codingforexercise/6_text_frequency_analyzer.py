"""
文本词频统计分析工具

功能：读取文本文件，统计词频，并按出现次数排序输出
适用场景：文本分析、数据处理、英文文章词频统计
"""

import re


def analyze_text_file(file_path, top_n=20):
    """
    分析文本文件的词频

    参数：
        file_path: 文本文件路径
        top_n: 显示前 N 个高频词，默认 20

    返回：
        词频字典
    """
    print(f"[*] 正在分析文件: {file_path}")
    print(f"[*] 显示前 {top_n} 个高频词\n")

    try:
        # 打开文件并读取内容
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

            # 使用正则表达式去除标点符号
            # 将常见标点符号替换为空格
            content = re.sub(r"[,./;%&!?\"'()\[\]{}:—\-]", " ", content)

            # 将所有单词转为小写，并按空格/换行分割
            # split() 默认以空格和换行分割
            words = [word.lower() for word in content.split()]

            print(f"[+] 总词数（含重复）: {len(words)}")

            # 去重，获取唯一单词集合
            unique_words = set(words)
            print(f"[+] 唯一词数: {len(unique_words)}\n")

            # 统计每个单词出现的次数（字典推导式）
            word_freq = {word: words.count(word) for word in unique_words}

            # 按出现次数排序（降序）
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

            # 输出前 N 个高频词
            print("=" * 60)
            print(f"{'排名':<6} {'单词':<20} {'出现次数':<10}")
            print("=" * 60)

            for rank, (word, count) in enumerate(sorted_words[:top_n], 1):
                print(f"{rank:<6} {word:<20} {count:<10}")

            print("=" * 60)

            return word_freq

    except FileNotFoundError:
        print(f"[!] 错误: 文件 '{file_path}' 不存在")
        return None
    except Exception as e:
        print(f"[!] 发生错误: {e}")
        return None


def analyze_text_optimized(file_path, top_n=20, min_word_length=1):
    """
    优化版文本分析（使用 Counter，性能更好）

    参数：
        file_path: 文本文件路径
        top_n: 显示前 N 个高频词
        min_word_length: 最小单词长度（过滤短词）

    返回：
        词频字典
    """
    from collections import Counter

    print(f"[*] 正在分析文件: {file_path}")
    print(f"[*] 最小单词长度: {min_word_length}")
    print(f"[*] 显示前 {top_n} 个高频词\n")

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            content = file.read()

            # 去除标点符号
            content = re.sub(r"[,./;%&!?\"'()\[\]{}:—\-]", " ", content)

            # 分割并转小写
            words = [word.lower() for word in content.split()]

            # 过滤短词
            words = [word for word in words if len(word) >= min_word_length]

            print(f"[+] 总词数（含重复）: {len(words)}")
            print(f"[+] 唯一词数: {len(set(words))}\n")

            # 使用 Counter 统计词频（性能更好）
            word_freq = Counter(words)

            # 获取前 N 个最常见的词
            most_common = word_freq.most_common(top_n)

            # 输出结果
            print("=" * 60)
            print(f"{'排名':<6} {'单词':<20} {'出现次数':<10}")
            print("=" * 60)

            for rank, (word, count) in enumerate(most_common, 1):
                print(f"{rank:<6} {word:<20} {count:<10}")

            print("=" * 60)

            return dict(word_freq)

    except FileNotFoundError:
        print(f"[!] 错误: 文件 '{file_path}' 不存在")
        return None
    except Exception as e:
        print(f"[!] 发生错误: {e}")
        return None


def save_results(word_freq, output_file):
    """
    将词频统计结果保存到文件

    参数：
        word_freq: 词频字典
        output_file: 输出文件路径
    """
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            # 按词频降序排序
            sorted_words = sorted(word_freq.items(), key=lambda x: x[1], reverse=True)

            f.write("单词,出现次数\n")
            for word, count in sorted_words:
                f.write(f"{word},{count}\n")

        print(f"\n[√] 结果已保存到: {output_file}")

    except Exception as e:
        print(f"[!] 保存失败: {e}")


if __name__ == "__main__":
    # 使用示例
    file_path = "sample.txt"  # 替换为实际文件路径

    print("=" * 60)
    print("文本词频统计分析工具")
    print("=" * 60)
    print()

    # 方法1：基础版本
    # word_freq = analyze_text_file(file_path, top_n=20)

    # 方法2：优化版本（推荐）
    word_freq = analyze_text_optimized(
        file_path=file_path,
        top_n=20,
        min_word_length=2  # 过滤单字符词
    )

    # 保存结果到 CSV 文件
    if word_freq:
        save_results(word_freq, "word_frequency.csv")


"""
使用说明：
====================

1. 安装依赖：
   无需额外安装，使用 Python 标准库

2. 基本用法：
   python 6_text_frequency_analyzer.py

3. 自定义参数：
   - file_path: 要分析的文本文件路径
   - top_n: 显示前 N 个高频词（默认 20）
   - min_word_length: 最小单词长度，用于过滤短词（默认 1）

4. 功能说明：

   4.1 文本预处理：
       - 去除标点符号（使用正则表达式）
       - 转换为小写（统一大小写）
       - 按空格和换行分割单词

   4.2 词频统计：
       - 基础版本：使用字典推导式 + count()
       - 优化版本：使用 collections.Counter（推荐）

   4.3 结果排序：
       - 按出现次数降序排序
       - 支持显示前 N 个高频词

   4.4 结果保存：
       - 可以保存为 CSV 格式
       - 方便后续分析和可视化

5. 两种实现方式对比：

   方法1（基础版）：
   - 使用列表推导式 + count()
   - 代码简单易懂
   - 性能较差（大文件慢）

   方法2（优化版）：
   - 使用 collections.Counter
   - 性能更好
   - 功能更强大（推荐使用）

6. 正则表达式说明：
   re.sub(r"[,./;%&!?\"'()\[\]{}:—\-]", " ", content)

   替换以下字符为空格：
   , . / ; % & ! ? " ' ( ) [ ] { } : — -

7. 应用场景：
   - 英文文章词频分析
   - 文本数据挖掘
   - 关键词提取
   - 文学作品分析
   - SEO 关键词分析

8. 扩展功能：

   8.1 停用词过滤：
       常见停用词如 the, a, an, is, are 等
       可以创建停用词列表进行过滤

   8.2 词云生成：
       可以使用 wordcloud 库生成词云图
       pip install wordcloud matplotlib

   8.3 多文件分析：
       批量处理多个文件
       比较不同文件的词频分布

   8.4 中文支持：
       需要使用 jieba 分词
       pip install jieba

9. 优化建议：
   - 对于大文件，使用 Counter 而非 count()
   - 过滤停用词提高分析质量
   - 使用多进程处理大量文件
   - 添加进度条显示处理进度

10. 示例输出：

    ==========================================================
    排名     单词                   出现次数
    ==========================================================
    1      the                  245
    2      and                  189
    3      to                   156
    4      of                   142
    ==========================================================

11. 注意事项：
    - 确保文件编码为 UTF-8
    - 文件路径中的反斜杠要转换或使用 r"path"
    - 处理大文件时注意内存使用
    - 可以根据需要调整正则表达式匹配规则
"""
