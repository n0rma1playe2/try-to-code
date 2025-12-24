#!/usr/bin/env python3
"""
压缩包套娃解压工具
自动递归解压嵌套的压缩包，支持多种格式
"""
import os
import sys
import argparse
import subprocess
import shutil
from pathlib import Path

# 支持的压缩格式
SUPPORTED_FORMATS = {
    'zip': {'extensions': ['.zip'], 'module': 'zipfile'},
    'rar': {'extensions': ['.rar'], 'module': 'rarfile'},
    '7z': {'extensions': ['.7z'], 'module': 'py7zr'},
    'tar.gz': {'extensions': ['.tar.gz', '.tgz'], 'module': None},
    'tar.bz2': {'extensions': ['.tar.bz2', '.tbz2'], 'module': None},
    'tar.xz': {'extensions': ['.tar.xz', '.txz'], 'module': None},
    'gz': {'extensions': ['.gz'], 'module': None},
    'bz2': {'extensions': ['.bz2'], 'module': None},
    'xz': {'extensions': ['.xz'], 'module': None},
}

def detect_archive_type(filepath):
    """检测压缩包类型（使用 file 命令和扩展名）"""
    # 尝试使用 file 命令
    try:
        result = subprocess.run(['file', filepath],
                              capture_output=True, text=True, timeout=5)
        output = result.stdout.lower()

        if 'gzip compressed data' in output:
            if filepath.endswith('.tar.gz') or filepath.endswith('.tgz'):
                return 'tar.gz'
            return 'gz'
        elif 'bzip2 compressed data' in output:
            if filepath.endswith('.tar.bz2') or filepath.endswith('.tbz2'):
                return 'tar.bz2'
            return 'bz2'
        elif 'xz compressed data' in output:
            if filepath.endswith('.tar.xz') or filepath.endswith('.txz'):
                return 'tar.xz'
            return 'xz'
        elif 'zip archive' in output:
            return 'zip'
        elif '7-zip archive' in output:
            return '7z'
        elif 'rar archive' in output:
            return 'rar'
    except (subprocess.TimeoutExpired, FileNotFoundError):
        pass

    # 根据扩展名判断
    filepath_lower = filepath.lower()
    for format_type, info in SUPPORTED_FORMATS.items():
        for ext in info['extensions']:
            if filepath_lower.endswith(ext):
                return format_type

    return None

def extract_archive(archive_path, output_dir=None, verbose=False):
    """解压单个压缩包"""
    archive_type = detect_archive_type(archive_path)

    if not archive_type:
        if verbose:
            print(f"[!] 无法识别的文件类型: {archive_path}")
        return None

    if output_dir is None:
        output_dir = os.path.dirname(archive_path) or '.'

    temp_dir = os.path.join(output_dir, '.unzip_temp')
    os.makedirs(temp_dir, exist_ok=True)

    try:
        if verbose:
            print(f"[*] 解压 {os.path.basename(archive_path)} ({archive_type})")

        # 使用对应的方法解压
        if archive_type == 'zip':
            import zipfile
            with zipfile.ZipFile(archive_path, 'r') as zip_ref:
                zip_ref.extractall(temp_dir)

        elif archive_type == 'rar':
            try:
                import rarfile
                with rarfile.RarFile(archive_path, 'r') as rar_ref:
                    rar_ref.extractall(temp_dir)
            except ImportError:
                print("[!] 缺少 rarfile 模块，尝试使用 unrar 命令")
                subprocess.run(['unrar', 'x', archive_path, temp_dir], check=True)

        elif archive_type == '7z':
            try:
                import py7zr
                with py7zr.SevenZipFile(archive_path, 'r') as z:
                    z.extractall(temp_dir)
            except ImportError:
                print("[!] 缺少 py7zr 模块，尝试使用 7z 命令")
                subprocess.run(['7z', 'x', f'-o{temp_dir}', archive_path], check=True)

        elif archive_type == 'tar.gz':
            subprocess.run(['tar', '-xzf', archive_path, '-C', temp_dir], check=True)

        elif archive_type == 'tar.bz2':
            subprocess.run(['tar', '-xjf', archive_path, '-C', temp_dir], check=True)

        elif archive_type == 'tar.xz':
            subprocess.run(['tar', '-xJf', archive_path, '-C', temp_dir], check=True)

        elif archive_type == 'gz':
            # 单独的 gzip 文件
            output_file = os.path.join(temp_dir, os.path.basename(archive_path)[:-3])
            subprocess.run(['gunzip', '-c', archive_path],
                         stdout=open(output_file, 'wb'), check=True)

        elif archive_type == 'bz2':
            output_file = os.path.join(temp_dir, os.path.basename(archive_path)[:-4])
            subprocess.run(['bunzip2', '-c', archive_path],
                         stdout=open(output_file, 'wb'), check=True)

        elif archive_type == 'xz':
            output_file = os.path.join(temp_dir, os.path.basename(archive_path)[:-3])
            subprocess.run(['unxz', '-c', archive_path],
                         stdout=open(output_file, 'wb'), check=True)

        # 检查解压出的文件
        extracted_files = os.listdir(temp_dir)

        if len(extracted_files) == 0:
            print(f"[!] 警告: 没有解压出任何文件")
            os.rmdir(temp_dir)
            return None

        # 将文件移动到输出目录
        for item in extracted_files:
            src = os.path.join(temp_dir, item)
            dst = os.path.join(output_dir, item)

            # 如果目标已存在，先删除
            if os.path.exists(dst):
                if os.path.isdir(dst):
                    shutil.rmtree(dst)
                else:
                    os.remove(dst)

            shutil.move(src, dst)

        os.rmdir(temp_dir)

        if verbose:
            print(f"[+] 解压成功: {', '.join(extracted_files)}")

        # 返回第一个文件（通常套娃压缩包只有一个文件）
        return os.path.join(output_dir, extracted_files[0])

    except Exception as e:
        print(f"[!] 解压失败: {e}")
        if os.path.exists(temp_dir):
            shutil.rmtree(temp_dir)
        return None

def recursive_extract(archive_path, max_depth=1000, verbose=False):
    """递归解压嵌套压缩包"""
    current_file = os.path.abspath(archive_path)
    depth = 0

    print(f"[*] 开始解压: {os.path.basename(current_file)}")

    while depth < max_depth:
        if not os.path.isfile(current_file):
            print(f"[!] 解压完成: 最终文件是目录或不存在")
            break

        archive_type = detect_archive_type(current_file)

        if not archive_type:
            print(f"[+] 解压完成: {current_file}")
            print(f"[+] 总共解压了 {depth} 层")
            break

        next_file = extract_archive(current_file, verbose=verbose)

        if next_file is None:
            print(f"[!] 解压停止在第 {depth} 层")
            break

        # 删除已解压的压缩包（可选）
        # os.remove(current_file)

        current_file = next_file
        depth += 1

        if verbose:
            print(f"[*] 当前深度: {depth}")

    if depth >= max_depth:
        print(f"[!] 达到最大深度 {max_depth}，停止解压")

def main():
    parser = argparse.ArgumentParser(
        description='压缩包套娃解压工具 - 自动递归解压嵌套压缩包',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
支持的格式:
  zip, rar, 7z, tar.gz, tar.bz2, tar.xz, gz, bz2, xz

示例:
  %(prog)s flag.zip
  %(prog)s nested.tar.gz --max-depth 100
  %(prog)s archive.7z -v
        """
    )

    parser.add_argument('archive', help='要解压的压缩包')
    parser.add_argument('--max-depth', type=int, default=1000,
                       help='最大递归深度 (默认: 1000)')
    parser.add_argument('-v', '--verbose', action='store_true',
                       help='显示详细信息')

    args = parser.parse_args()

    if not os.path.isfile(args.archive):
        print(f"[!] 错误: 文件不存在 '{args.archive}'", file=sys.stderr)
        sys.exit(1)

    recursive_extract(args.archive, max_depth=args.max_depth, verbose=args.verbose)

if __name__ == "__main__":
    main()