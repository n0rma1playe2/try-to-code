#!/usr/bin/env python3
"""
CTF MISC 工具集
包含关键字搜索、DNA编码解码等常用功能
"""
import re
import argparse
import sys

# 常用关键字列表
DEFAULT_KEYWORDS = [
    b"flag", b"FLAG", b"F14g", b"key", b"password", b"dasctf", b"DASCTF",
    b"k3y", b"p@ssword", b"passw0rd", b"p@ssw0rd",
    b"secret", b"s3cret", b"s3cr3t", b"s3cre4",
    b"F14ggg", b"Ic4unq1U", b"ISCC"
]

# 常用 Base64 编码的关键字
BASE64_HINTS = """
常用关键字的 Base64 编码:
  flag          -> Zmxh
  F14g          -> RjE0
  DASCTF        -> REFTQ1RGe
  s3cr3t        -> czNjcjN0
  secret        -> c2VjcmV0
  password      -> cGFzc3dvc
  PNG文件头      -> iVBORw0KGgo
  ZIP文件头      -> UEsDBA
"""

# DNA 编码映射表 (标准 3-to-1 编码)
DNA_DECODE_TABLE = {
    'AAA': 'a', 'AAC': 'b', 'AAG': 'c', 'AAT': 'd',
    'ACA': 'e', 'ACC': 'f', 'ACG': 'g', 'ACT': 'h',
    'AGA': 'i', 'AGC': 'j', 'AGG': 'k', 'AGT': 'l',
    'ATA': 'm', 'ATC': 'n', 'ATG': 'o', 'ATT': 'p',
    'CAA': 'q', 'CAC': 'r', 'CAG': 's', 'CAT': 't',
    'CCA': 'u', 'CCC': 'v', 'CCG': 'w', 'CCT': 'x',
    'CGA': 'y', 'CGC': 'z', 'CGG': 'A', 'CGT': 'B',
    'CTA': 'C', 'CTC': 'D', 'CTG': 'E', 'CTT': 'F',
    'GAA': 'G', 'GAC': 'H', 'GAG': 'I', 'GAT': 'J',
    'GCA': 'K', 'GCC': 'L', 'GCG': 'M', 'GCT': 'N',
    'GGA': 'O', 'GGC': 'P', 'GGG': 'Q', 'GGT': 'R',
    'GTA': 'S', 'GTC': 'T', 'GTG': 'U', 'GTT': 'V',
    'TAA': 'W', 'TAC': 'X', 'TAG': 'Y', 'TAT': 'Z',
    'TCA': '1', 'TCC': '2', 'TCG': '3', 'TCT': '4',
    'TGA': '5', 'TGC': '6', 'TGG': '7', 'TGT': '8',
    'TTA': '9', 'TTC': '0', 'TTG': ' '
}

def search_keywords(file_path, keywords=None, case_insensitive=True, max_display=50):
    """在文件中搜索关键字"""
    if keywords is None:
        keywords = DEFAULT_KEYWORDS

    try:
        with open(file_path, 'rb') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"[!] 错误: 文件不存在 '{file_path}'", file=sys.stderr)
        return
    except Exception as e:
        print(f"[!] 错误: 无法读取文件 '{file_path}': {e}", file=sys.stderr)
        return

    print(f"[*] 在文件 '{file_path}' 中搜索关键字 ({len(data)} 字节)")
    print(f"[*] 关键字数量: {len(keywords)}\n")

    found_any = False
    for item in keywords:
        flags = re.IGNORECASE if case_insensitive else 0
        regex = re.compile(re.escape(item) + b'.*', flags)

        matches = list(regex.finditer(data))
        if matches:
            found_any = True
            keyword_str = item.decode('utf-8', errors='replace')
            print(f"[+] 找到关键字: {keyword_str}")

            for idx, match in enumerate(matches, 1):
                matched_text = match.group()
                display_text = matched_text[:max_display]

                # 尝试解码为可读文本
                try:
                    decoded = display_text.decode('utf-8', errors='replace')
                    print(f"    [{idx}] {decoded}")
                except:
                    print(f"    [{idx}] {display_text.hex()}")

                if len(matched_text) > max_display:
                    print(f"        ... (截断 {len(matched_text) - max_display} 字节)")
            print()

    if not found_any:
        print("[!] 未找到任何关键字")

def dna_decode(cipher_text):
    """解码 DNA 编码"""
    cipher_text = cipher_text.upper().strip()

    # 验证输入
    if not all(c in 'ACGT' for c in cipher_text):
        print("[!] 错误: DNA 序列只能包含 A, C, G, T", file=sys.stderr)
        return None

    if len(cipher_text) % 3 != 0:
        print(f"[!] 警告: DNA 序列长度不是 3 的倍数 ({len(cipher_text)})", file=sys.stderr)

    plain = ''
    for i in range(0, len(cipher_text) - 2, 3):
        codon = cipher_text[i:i+3]
        if codon in DNA_DECODE_TABLE:
            plain += DNA_DECODE_TABLE[codon]
        else:
            plain += '?'
            print(f"[!] 警告: 未知密码子 '{codon}'", file=sys.stderr)

    return plain

def main():
    parser = argparse.ArgumentParser(
        description='CTF MISC 工具集 - 关键字搜索、DNA解码等',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )

    subparsers = parser.add_subparsers(dest='command', help='子命令')

    # 关键字搜索子命令
    search_parser = subparsers.add_parser('search', help='在文件中搜索关键字')
    search_parser.add_argument('file', help='要搜索的文件路径')
    search_parser.add_argument('-k', '--keywords', nargs='+',
                              help='自定义关键字列表 (默认使用内置列表)')
    search_parser.add_argument('-c', '--case-sensitive', action='store_true',
                              help='区分大小写')
    search_parser.add_argument('-m', '--max-display', type=int, default=50,
                              help='每个匹配显示的最大字节数 (默认: 50)')

    # DNA 解码子命令
    dna_parser = subparsers.add_parser('dna', help='DNA 编码解码')
    dna_parser.add_argument('cipher', nargs='?', help='要解码的 DNA 序列')
    dna_parser.add_argument('-f', '--file', help='从文件读取 DNA 序列')

    # Base64 提示子命令
    b64_parser = subparsers.add_parser('base64-hints', help='显示常用 Base64 编码')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    if args.command == 'search':
        keywords = DEFAULT_KEYWORDS
        if args.keywords:
            keywords = [k.encode() for k in args.keywords]

        search_keywords(
            args.file,
            keywords=keywords,
            case_insensitive=not args.case_sensitive,
            max_display=args.max_display
        )

    elif args.command == 'dna':
        if args.file:
            try:
                with open(args.file, 'r') as f:
                    cipher = f.read().strip()
            except Exception as e:
                print(f"[!] 错误: 无法读取文件 '{args.file}': {e}", file=sys.stderr)
                sys.exit(1)
        elif args.cipher:
            cipher = args.cipher
        else:
            print("[!] 错误: 请提供 DNA 序列或使用 -f 指定文件", file=sys.stderr)
            sys.exit(1)

        print(f"[*] DNA 密文: {cipher}")
        result = dna_decode(cipher)
        if result:
            print(f"[+] 解码结果: {result}")

    elif args.command == 'base64-hints':
        print(BASE64_HINTS)

if __name__ == "__main__":
    main()