# 网络安全练习脚本集

这个目录包含了从 main.py 中分割出来的各种网络安全相关脚本，主要用于 CTF 比赛和安全学习。

## 目录结构

```
codingforexercise/
├── 1_beautifulsoup_parser.py     # BeautifulSoup 网页解析
├── 2_sql_blind_injection.py      # SQL 盲注二分法
├── 3_shop_page_finder.py         # 商城页面遍历查找
├── 4_multi_decrypt.py            # 多重加密解密
├── main.py                       # 原始脚本（已注释）
└── README.md                     # 本文件
```

## 脚本说明

### 1. BeautifulSoup 网页解析器
**文件**: `1_beautifulsoup_parser.py`
**功能**: 使用 BeautifulSoup 库解析网页内容
**依赖**: `pip install requests beautifulsoup4 lxml`
**用途**:
- 网页爬取
- HTML 内容解析
- 数据提取

**快速使用**:
```bash
python 1_beautifulsoup_parser.py
```

---

### 2. SQL 盲注二分法工具
**文件**: `2_sql_blind_injection.py`
**功能**: 使用二分法进行 SQL 盲注攻击，逐字符提取数据
**依赖**: `pip install requests`
**用途**:
- CTF Web 题目
- 授权渗透测试
- SQL 注入学习

**快速使用**:
```bash
python 2_sql_blind_injection.py
```

**重要提示**:
- 仅用于授权的安全测试和 CTF 比赛
- 未经授权的攻击是违法行为

---

### 3. 商城页面遍历查找工具
**文件**: `3_shop_page_finder.py`
**功能**: 遍历商城页面，查找特定关键词或内容
**依赖**: `pip install requests`
**用途**:
- CTF 题目中查找隐藏信息
- 批量页面内容检索
- 自动化查找特定商品

**快速使用**:
```bash
python 3_shop_page_finder.py
```

---

### 4. 多重加密解密工具
**文件**: `4_multi_decrypt.py`
**功能**: 对多层加密的字符串进行解密（ROT13 + 翻转 + Base64 + ASCII 偏移）
**依赖**: 无（使用 Python 标准库）
**用途**:
- CTF Crypto 题目
- 多层编码数据还原
- 混淆字符串解密

**解密流程**:
```
密文 -> ROT13 -> 翻转 -> Base64 解码 -> ASCII -1 -> 翻转 -> 明文
```

**快速使用**:
```bash
python 4_multi_decrypt.py
```

---

## 安装所有依赖

```bash
pip install requests beautifulsoup4 lxml
```

## 使用注意事项

### 法律和道德规范
1. 所有脚本仅用于授权的安全测试、CTF 比赛和学习目的
2. 未经授权对他人系统进行渗透测试是违法行为
3. 使用这些工具时请遵守相关法律法规和职业道德

### 技术注意事项
1. 根据实际情况调整脚本参数（URL、关键词、延迟等）
2. 注意请求频率，避免对目标服务器造成过大压力
3. 某些脚本需要根据具体环境修改 payload 格式
4. 建议在虚拟环境中运行

### CTF 使用建议
1. 先理解题目要求和目标
2. 根据实际情况修改脚本参数
3. 注意观察脚本输出，及时调整策略
4. 保存成功的配置，方便后续复用

## 学习资源

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [CTF Wiki](https://ctf-wiki.org/)
- [BeautifulSoup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)
- [SQL 注入学习](https://portswigger.net/web-security/sql-injection)

## 版本历史

- v1.0 (2025): 初始版本，从 main.py 分割并重构

## 许可证

仅用于教育和授权安全测试目的。

---

**提示**: 每个脚本文件内部都包含详细的使用说明和示例代码，建议打开文件查看完整文档。
