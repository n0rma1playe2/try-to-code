#!/usr/bin/env python3
"""
Short Ook / Brainfuck 解码工具
支持 Short Ook (。？！ 符号) 到 Brainfuck 的转换和执行
"""
import sys
import argparse

# Short Ook -> Brainfuck 映射表
SHORT_OOK_MAPPING = {
    "。。": "+",  # 加 1
    "！！": "-",  # 减 1
    "。？": ">",  # 指针右移
    "？。": "<",  # 指针左移
    "！？": "[",  # 循环开始
    "？！": "]",  # 循环结束
    "！。": ".",  # 输出
    "。！": ","   # 输入
}

def short_ook_to_brainfuck(code):
    """将 Short Ook 代码转换为 Brainfuck"""
    bf_code = ""
    i = 0

    while i < len(code) - 1:
        pair = code[i:i+2]
        if pair in SHORT_OOK_MAPPING:
            bf_code += SHORT_OOK_MAPPING[pair]
            i += 2
        else:
            # 跳过不成对的字符
            i += 1

    return bf_code

def execute_brainfuck(bf_code, memory_size=30000, verbose=False):
    """执行 Brainfuck 代码"""
    cells = [0] * memory_size
    ptr = 0
    pc = 0
    output = []

    # 预处理循环跳转位置
    loop_stack = []
    loops = {}

    for idx, command in enumerate(bf_code):
        if command == '[':
            loop_stack.append(idx)
        elif command == ']':
            if not loop_stack:
                print(f"[!] 错误: 第 {idx} 位置的 ']' 没有对应的 '['", file=sys.stderr)
                return None
            start = loop_stack.pop()
            loops[start] = idx
            loops[idx] = start

    if loop_stack:
        print(f"[!] 错误: 有 {len(loop_stack)} 个未闭合的 '['", file=sys.stderr)
        return None

    if verbose:
        print(f"[*] Brainfuck 代码长度: {len(bf_code)}")
        print(f"[*] 循环数量: {len(loop_stack)}")
        print()

    # 执行 Brainfuck 代码
    try:
        while pc < len(bf_code):
            command = bf_code[pc]

            if command == '>':
                ptr += 1
                if ptr >= memory_size:
                    print(f"[!] 错误: 指针越界 (>{memory_size})", file=sys.stderr)
                    return None
            elif command == '<':
                ptr -= 1
                if ptr < 0:
                    print(f"[!] 错误: 指针越界 (<0)", file=sys.stderr)
                    return None
            elif command == '+':
                cells[ptr] = (cells[ptr] + 1) % 256
            elif command == '-':
                cells[ptr] = (cells[ptr] - 1) % 256
            elif command == '.':
                output.append(chr(cells[ptr]))
            elif command == ',':
                # CTF 通常不需要输入
                cells[ptr] = 0
            elif command == '[':
                if cells[ptr] == 0:
                    pc = loops[pc]
            elif command == ']':
                if cells[ptr] != 0:
                    pc = loops[pc]

            pc += 1

    except KeyboardInterrupt:
        print("\n[!] 执行被中断", file=sys.stderr)
        return None
    except Exception as e:
        print(f"[!] 执行错误: {e}", file=sys.stderr)
        return None

    return ''.join(output)

def main():
    parser = argparse.ArgumentParser(
        description='Short Ook / Brainfuck 解码工具',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Short Ook 符号映射:
  。。 -> +    (加 1)
  ！！ -> -    (减 1)
  。？ -> >    (指针右移)
  ？。 -> <    (指针左移)
  ！？ -> [    (循环开始)
  ？！ -> ]    (循环结束)
  ！。 -> .    (输出)
  。！ -> ,    (输入)

示例:
  %(prog)s -c "。。。。！？！！。？？！"
  %(prog)s -f cipher.txt
  %(prog)s -f cipher.txt --show-bf
        """
    )

    parser.add_argument('-c', '--code', help='Short Ook 密文')
    parser.add_argument('-f', '--file', help='从文件读取密文')
    parser.add_argument('--show-bf', action='store_true',
                       help='显示转换后的 Brainfuck 代码')
    parser.add_argument('-m', '--memory', type=int, default=30000,
                       help='内存大小 (默认: 30000)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细信息')

    args = parser.parse_args()

    # 读取密文
    if args.file:
        try:
            with open(args.file, 'r', encoding='utf-8') as f:
                code = f.read().strip()
        except Exception as e:
            print(f"[!] 错误: 无法读取文件 '{args.file}': {e}", file=sys.stderr)
            sys.exit(1)
    elif args.code:
        code = args.code
    else:
        print("[!] 错误: 请提供 Short Ook 密文或使用 -f 指定文件", file=sys.stderr)
        parser.print_help()
        sys.exit(1)

    if args.verbose:
        print(f"[*] Short Ook 密文长度: {len(code)}")

    # 转换为 Brainfuck
    bf_code = short_ook_to_brainfuck(code)

    if args.show_bf or args.verbose:
        print(f"[*] Brainfuck 代码: {bf_code}\n")

    # 执行 Brainfuck
    print("[*] 执行结果:")
    result = execute_brainfuck(bf_code, memory_size=args.memory, verbose=args.verbose)

    if result:
        print(result)
    else:
        print("[!] 执行失败", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()