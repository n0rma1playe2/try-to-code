import os
import subprocess
import py7zr

input_file = 'shell9999.tar.gz'  # 更改为你的文件路径

def get_compressed_type(filepath: str) -> str:
    cmd = ['file', filepath]
    file_cmd_output = subprocess.run(cmd, stdout=subprocess.PIPE).stdout.decode().strip()

    if 'gzip compressed data' in file_cmd_output:
        return 'tar.gz'
    if 'Zip archive data' in file_cmd_output:
        return 'zip'
    if '7-zip archive data' in file_cmd_output:
        return '7z'
    if 'gzip compressed data' in file_cmd_output:
        return 'gzip'
    if 'XZ compressed data' in file_cmd_output:
        return 'xz'
    if 'bzip2 compressed data' in file_cmd_output:
        return 'bzip2'
    if 'LZMA compressed data' in file_cmd_output:
        return 'lzma'
    if 'Zstandard compressed data' in file_cmd_output:
        return 'zstd'
    return ''

while True:
    ctype = get_compressed_type(input_file)
    if ctype == "tar.gz":
        cmd = ['tar', '-xzf', input_file]
        subprocess.run(cmd)
    elif ctype == "zip":
        cmd = ['unzip', input_file]
        subprocess.run(cmd)
    elif ctype == "7z":
        with py7zr.SevenZipFile(input_file, mode='r') as z:
            z.extractall()
    elif ctype == "gzip":
        tmp_file = input_file + ".gz"
        cmd = "mv {} {}; gunzip {}".format(input_file, tmp_file, tmp_file)
    elif ctype == "xz":
        tmp_file = input_file + ".xz"
        cmd = "mv {} {}; unxz {}".format(input_file, tmp_file, tmp_file)
    elif ctype == "bzip2":
        tmp_file = input_file + ".bz2"
        cmd = "mv {} {}; bunzip2 {}".format(input_file, tmp_file, tmp_file)
    elif ctype == "lzma":
        tmp_file = input_file + ".lzma"
        cmd = "mv {} {}; unlzma {}".format(input_file, tmp_file, tmp_file)
    elif ctype == "zstd":
        tmp_file = input_file + ".zst"
        cmd = "mv {} {}; unzstd --force {}".format(input_file, tmp_file, tmp_file)
    else:
        print("Unsupported file type or done extracting!")
        break

    # 删除已解压的文件并更新input_file为新解压的文件
    os.remove(input_file)
    files = [f for f in os.listdir() if os.path.isfile(f) and f != "test.py"]
    if len(files) == 1:
        input_file = files[0]
    else:
        print("Unexpected number of files in directory!")
        break