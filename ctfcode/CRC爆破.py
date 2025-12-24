#!/usr/bin/env python3
"""
CRC32 爆破工具 - 用于反向推导已知 CRC32 值的原始数据
支持自定义字符集、长度和多项式参数
"""
import binascii
import argparse
import sys

class CRC32Reverse:
    def __init__(self, crc32, length, tbl=bytes(range(256)), poly=0xEDB88320, accum=0):
        self.char_set = set(tbl)  # 支持所有字节
        self.crc32 = crc32
        self.length = length
        self.poly = poly
        self.accum = accum
        self.table = []
        self.table_reverse = []

    def init_tables(self, poly, reverse=True):
        """构建 CRC32 表及其反向查找表"""
        # CRC32 表构建
        for i in range(256):
            for j in range(8):
                if i & 1:
                    i >>= 1
                    i ^= poly
                else:
                    i >>= 1
            self.table.append(i)

        assert len(self.table) == 256, "CRC32 表的大小错误"

        # 构建反向查找表
        if reverse:
            for i in range(256):
                found = [j for j in range(256) if self.table[j] >> 24 == i]
                self.table_reverse.append(tuple(found))
            
            assert len(self.table_reverse) == 256, "反向查找表的大小错误"

    def calc(self, data, accum=0):
        """计算 CRC32 校验值"""
        accum = ~accum
        for b in data:
            accum = self.table[(accum ^ b) & 0xFF] ^ ((accum >> 8) & 0x00FFFFFF)
        accum = ~accum
        return accum & 0xFFFFFFFF

    def find_reverse(self, desired, accum):
        """查找反向字节序列"""
        solutions = set()
        accum = ~accum
        stack = [(~desired,)]
        
        while stack:
            node = stack.pop()
            for j in self.table_reverse[(node[0] >> 24) & 0xFF]:
                if len(node) == 4:
                    a = accum
                    data = []
                    node = node[1:] + (j,)
                    for i in range(3, -1, -1):
                        data.append((a ^ node[i]) & 0xFF)
                        a >>= 8
                        a ^= self.table[node[i]]
                    solutions.add(tuple(data))
                else:
                    stack.append(((node[0] ^ self.table[j]) << 8,) + node[1:] + (j,))
        
        return solutions

    def dfs(self, length, outlist=[b'']):
        """深度优先搜索生成字节序列"""
        if length == 0:
            return outlist
        tmp_list = [item + bytes([x]) for item in outlist for x in self.char_set]
        return self.dfs(length - 1, tmp_list)

    def run_reverse(self):
        """执行 CRC32 反向查找"""
        self.init_tables(self.poly)

        desired = self.crc32
        accum = self.accum
        result_list = []

        # 处理至少为 4 字节的情况
        if self.length >= 4:
            patches = self.find_reverse(desired, accum)
            for patch in patches:
                checksum = self.calc(patch, accum)
                # print(f"verification checksum: 0x{checksum:08x} ({'OK' if checksum == desired else 'ERROR'})")
            for item in self.dfs(self.length - 4):
                patch = list(item)
                patches = self.find_reverse(desired, self.calc(patch, accum))
                for last_4_bytes in patches:
                    patch.extend(last_4_bytes)
                    checksum = self.calc(patch, accum)
                    if checksum == desired:
                        result_list.append(bytes(patch))  # 添加符合条件的字节序列
        else:
            for item in self.dfs(self.length):
                if self.calc(item) == desired:
                    result_list.append(bytes(item))  # 添加符合条件的字节序列
        return result_list

def crc32_reverse(crc32, length, char_set=bytes(range(256)), poly=0xEDB88320, accum=0):
    obj = CRC32Reverse(crc32, length, char_set, poly, accum)
    return obj.run_reverse()  # 返回所有结果

def crc32(s):
    return binascii.crc32(s) & 0xFFFFFFFF

def main():
    parser = argparse.ArgumentParser(
        description='CRC32 爆破工具 - 反向推导原始数据',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  %(prog)s -c 0xf72c104b -l 5
  %(prog)s -c f72c104b -l 5 --charset "0123456789abcdef"
  %(prog)s -c 0xf72c104b 0x39004188 -l 5
  %(prog)s -c 0xf72c104b -l 4 --printable
        """
    )

    parser.add_argument('-c', '--crc', nargs='+', required=True,
                        help='CRC32 值 (支持十六进制格式: 0xf72c104b 或 f72c104b)')
    parser.add_argument('-l', '--length', type=int, required=True,
                        help='原始数据的长度')
    parser.add_argument('--charset', type=str,
                        help='自定义字符集 (默认: 所有字节 0-255)')
    parser.add_argument('--printable', action='store_true',
                        help='仅使用可打印 ASCII 字符 (0x20-0x7E)')
    parser.add_argument('--max-results', type=int, default=10,
                        help='每个 CRC 值显示的最大结果数 (默认: 10, 0=全部)')
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='显示详细信息')

    args = parser.parse_args()

    # 处理字符集
    if args.printable:
        char_set = bytes(range(0x20, 0x7F))  # 可打印 ASCII
    elif args.charset:
        char_set = args.charset.encode()
    else:
        char_set = bytes(range(256))  # 所有字节

    # 处理 CRC 值列表
    crc_values = []
    for crc_str in args.crc:
        try:
            # 支持 0x 前缀的十六进制和普通十六进制
            if crc_str.startswith('0x') or crc_str.startswith('0X'):
                crc_val = int(crc_str, 16)
            else:
                # 尝试十六进制解析
                try:
                    crc_val = int(crc_str, 16)
                except ValueError:
                    # 尝试十进制解析
                    crc_val = int(crc_str, 10)
            crc_values.append(crc_val)
        except ValueError:
            print(f"[!] 错误: 无法解析 CRC 值 '{crc_str}'", file=sys.stderr)
            sys.exit(1)

    if args.verbose:
        print(f"[*] 字符集大小: {len(char_set)}")
        print(f"[*] 数据长度: {args.length}")
        print(f"[*] CRC 值数量: {len(crc_values)}")
        print()

    # 对每个 CRC 值进行爆破
    for idx, crc_val in enumerate(crc_values, 1):
        print(f"[+] CRC32: 0x{crc_val:08x}")

        try:
            results = crc32_reverse(crc_val, args.length, char_set)

            if not results:
                print(f"    未找到匹配结果")
            else:
                total = len(results)
                display_count = total if args.max_results == 0 else min(total, args.max_results)

                for i, result in enumerate(results[:display_count], 1):
                    # 尝试解码为字符串
                    try:
                        decoded = result.decode('utf-8', errors='replace')
                        print(f"    [{i}] {result.hex()} | {repr(decoded)}")
                    except:
                        print(f"    [{i}] {result.hex()}")

                if total > display_count:
                    print(f"    ... 还有 {total - display_count} 个结果 (使用 --max-results 0 查看全部)")

                print(f"    总计: {total} 个结果")

        except Exception as e:
            print(f"[!] 错误: {e}", file=sys.stderr)
            if args.verbose:
                import traceback
                traceback.print_exc()

        if idx < len(crc_values):
            print()

if __name__ == "__main__":
    main()