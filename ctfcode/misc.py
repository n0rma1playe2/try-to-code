# # 要搜索的字符列表
# search_items = [
#     "key", "password", "dasctf", "k3y", "p@ssword", "passw0rd",
#     "p@ssw0rd", "secret", "s3cret", "s3cr3t", "s3cre4","F14ggg",
#     "Ic4unq1U", "ISCC"
#     # 遇到⼀个加⼀个，CTFer的好习惯
# ]
import re

# 要搜索的字符列表
search_items = [
    b"key", b"password", b"dasctf", b"k3y", b"p@ssword", b"passw0rd",
    b"p@ssw0rd", b"secret", b"s3cret", b"s3cr3t", b"s3cre4",b"F14ggg"
    # 遇到⼀个加⼀个，CTFer的好习惯
]

file_path = "test.txt"

with open(file_path,'rb') as f:
    data = f.read()
    
for item in search_items:
    # re.escape(item) 用于转义 item 中的特殊字符, 确保它们被当作普通字符处理
    # re.IGNORECASE 标志使得匹配不区分大小写。
    regex = re.compile(re.escape(item) + b'.*', re.IGNORECASE)
    for match in regex.finditer(data): # finditer 返回一个迭代器，每次迭代返回一个匹配对象
        matched_text = match.group() # 返回匹配到的完整文本
        # 若匹配到，则显示前50个字节
        print(f"[+] Found {item.decode()} match: {matched_text[:50]}...")
# 各种常用关键字的bash64编码
# flag                          Zmxh
# F14g                          RjE0
# DASCTF                        REFTQ1RGe
# s3cr3t                        czNjcjN0
# secret                        c2VjcmV0
# password                      cGFzc3dvc
# PNG文件头                      iVBORw0KGgo
# ZIP文件头                      UEsDBA
table = 'ACGT'
dic = {'AAA': 'a', 'AAC': 'b', 'AAG': 'c',
       'AAT': 'd', 'ACA': 'e', 'ACC': 'f', 'ACG': 'g', 'ACT': 'h', 'AGA': 'i', 'AGC': 'j', 'AGG': 'k', 'AGT': 'l', 'ATA': 'm', 'ATC': 'n', 'ATG': 'o', 'ATT': 'p', 'CAA': 'q', 'CAC': 'r', 'CAG': 's', 'CAT': 't', 'CCA': 'u', 'CCC': 'v', 'CCG': 'w', 'CCT': 'x', 'CGA': 'y', 'CGC': 'z', 'CGG': 'A', 'CGT': 'B', 'CTA': 'C', 'CTC': 'D', 'CTG': 'E', 'CTT': 'F', 'GAA': 'G', 'GAC': 'H', 'GAG': 'I', 'GAT': 'J', 'GCA': 'K', 'GCC': 'L', 'GCG': 'M', 'GCT': 'N', 'GGA': 'O', 'GGC': 'P', 'GGG': 'Q', 'GGT': 'R', 'GTA': 'S', 'GTC': 'T', 'GTG': 'U', 'GTT': 'V', 'TAA': 'W', 'TAC': 'X', 'TAG': 'Y', 'TAT': 'Z', 'TCA': '1', 'TCC': '2', 'TCG': '3', 'TCT': '4', 'TGA': '5', 'TGC': '6', 'TGG': '7', 'TGT': '8', 'TTA': '9', 'TTC': '0', 'TTG': ' '}
cipher = 'TCATCAACAAAT'
plain = ''
for i in range(0, len(cipher), 3):
    plain += dic[cipher[i:i+3]]
print(plain)