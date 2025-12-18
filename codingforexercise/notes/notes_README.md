# Python 学习笔记与实用脚本集

本目录包含从"笔记.py"中分割出来的学习笔记和实用脚本，涵盖 Python 基础语法、CTF 工具和数据处理等内容。

## 目录结构

```
notes/
└── 1_python_basics.md           # Python 基础语法学习笔记

../
├── 5_ssti_injection.py          # SSTI 模板注入工具
├── 6_text_frequency_analyzer.py # 文本词频统计分析
├── 7_simple_crawler.py          # 简单网页爬虫
└── notes_README.md              # 本文件
```

---

## 内容概览

### 1. Python 基础语法学习笔记 (Markdown)

**文件**: `notes/1_python_basics.md`
**类型**: 学习笔记
**内容**:
- 列表 (List)
- 元组 (Tuple)
- 字典 (Dictionary)
- 集合 (Set)
- 字符串 (String)
- 排序 (sorted)
- Lambda 表达式
- 循环 (for/while)
- 条件判断
- 异常处理
- 文件操作
- 模块导入

**适合人群**: Python 初学者

**特点**:
- 系统化整理
- 代码示例丰富
- 中文注释详细
- 覆盖核心知识点

---

### 2. SSTI 模板注入利用工具

**文件**: `5_ssti_injection.py`
**功能**: 利用 Flask/Jinja2 模板注入漏洞执行系统命令
**依赖**: `pip install requests`

**核心功能**:
- SSTI 盲注提取（逐字符）
- 命令执行结果获取
- Cookie 绕过过滤
- 自定义字符集

**适用场景**:
- CTF Web 题目
- 授权渗透测试
- 漏洞研究学习

**快速使用**:
```bash
python 5_ssti_injection.py
```

**技术要点**:
- 使用 `attr()` 过滤器绕过点号过滤
- 字符串拼接绕过关键词检测
- 通过 Cookie 传递敏感参数
- 盲注技术逐字符提取数据

**重要提示**:
- 仅用于授权测试和 CTF
- 未经授权的攻击是违法的

---

### 3. 文本词频统计分析工具

**文件**: `6_text_frequency_analyzer.py`
**功能**: 读取文本文件，统计词频，按出现次数排序
**依赖**: 无（使用 Python 标准库）

**核心功能**:
- 文本预处理（去标点、转小写）
- 词频统计（基础版 + 优化版）
- 结果排序和显示
- 导出为 CSV 格式

**两种实现方式**:
1. **基础版**: 列表推导式 + count()
2. **优化版**: collections.Counter（推荐）

**快速使用**:
```bash
python 6_text_frequency_analyzer.py
```

**应用场景**:
- 英文文章词频分析
- 文本数据挖掘
- 关键词提取
- 文学作品分析

**扩展功能**:
- 停用词过滤
- 词云生成
- 多文件批量分析
- 中文分词支持

---

### 4. 简单网页爬虫工具

**文件**: `7_simple_crawler.py`
**功能**: 使用 requests 库爬取网页内容
**依赖**: `pip install requests`

**核心功能**:
- 单页爬取
- 带重试机制的爬取
- 批量爬取多个网页
- 自动添加随机延迟
- 保存网页内容

**快速使用**:
```bash
python 7_simple_crawler.py
```

**应用场景**:
- 数据采集
- 内容监控
- 价格追踪
- 新闻聚合

**技术要点**:
- 自定义 User-Agent
- 随机延迟避免封禁
- 异常处理和重试
- 批量处理和保存

**法律声明**:
- 仅用于学习和合法用途
- 遵守网站 robots.txt
- 尊重网站爬取政策

---

## 安装依赖

### 全部依赖

```bash
pip install requests
```

### 可选依赖（扩展功能）

```bash
# 词云生成
pip install wordcloud matplotlib

# 中文分词
pip install jieba

# 异步爬虫
pip install aiohttp
```

---

## 使用建议

### 学习路径

1. **Python 基础** → 阅读 `1_python_basics.md`
2. **文本处理** → 运行 `6_text_frequency_analyzer.py`
3. **网络爬虫** → 运行 `7_simple_crawler.py`
4. **CTF 进阶** → 学习 `5_ssti_injection.py`

### 实践项目

1. **文本分析项目**:
   - 爬取文章 → 词频统计 → 生成词云

2. **数据采集项目**:
   - 批量爬取网页 → 提取信息 → 保存数据库

3. **CTF 练习**:
   - 搭建本地靶场 → 测试 SSTI 工具 → 理解漏洞原理

---

## 注意事项

### 安全和法律

1. **SSTI 工具**:
   - 仅用于授权测试
   - CTF 比赛
   - 安全研究

2. **爬虫工具**:
   - 遵守 robots.txt
   - 控制请求频率
   - 尊重版权

3. **数据隐私**:
   - 不采集个人信息
   - 不用于商业目的
   - 遵守相关法律

### 技术注意

1. **编码问题**:
   - 文件统一使用 UTF-8
   - 注意中文路径处理

2. **性能优化**:
   - 大文件使用 Counter
   - 爬虫使用异步或多线程
   - 避免内存溢出

3. **错误处理**:
   - 使用 try-except
   - 添加日志记录
   - 优雅降级

---

## 学习资源

### Python 基础
- [Python 官方文档](https://docs.python.org/zh-cn/3/)
- [廖雪峰 Python 教程](https://www.liaoxuefeng.com/wiki/1016959663602400)

### 网络爬虫
- [Requests 文档](https://requests.readthedocs.io/)
- [Beautiful Soup 文档](https://www.crummy.com/software/BeautifulSoup/bs4/doc/)

### CTF 安全
- [CTF Wiki](https://ctf-wiki.org/)
- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [PortSwigger Web Security](https://portswigger.net/web-security)

### 数据分析
- [Python 数据分析实战](https://pandas.pydata.org/)
- [词云生成教程](https://github.com/amueller/word_cloud)

---

## 常见问题

### Q1: 文件路径问题
**问题**: Windows 路径反斜杠导致错误
**解决**: 使用 `r"路径"` 或将 `\` 改为 `/`

### Q2: 编码错误
**问题**: 中文显示乱码
**解决**: 指定 `encoding='utf-8'`

### Q3: 网络请求失败
**问题**: 爬虫无法访问网站
**解决**: 检查 User-Agent、网络连接、是否需要登录

### Q4: 依赖安装失败
**问题**: pip install 报错
**解决**: 使用清华镜像源 `pip install -i https://pypi.tuna.tsinghua.edu.cn/simple`

---

## 贡献与反馈

这些脚本是学习过程的整理和总结，如有问题或建议，欢迎交流改进。

---

## 版本历史

- **v1.0** (2025): 初始版本，从"笔记.py"分割并重构

---

## 许可证

仅用于教育、学习和授权安全测试目的。

---

**提示**: 每个脚本文件内部都包含详细的使用说明、代码示例和注意事项，建议打开文件查看完整文档。
