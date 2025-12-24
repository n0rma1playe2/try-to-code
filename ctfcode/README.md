# CTF 工具集

这是一套用于 CTF 比赛的 Python 工具集，包含常用的解密、解码和文件处理工具。所有工具都支持命令行参数，方便在比赛中快速使用。

## 工具列表

### 1. CRC爆破.py - CRC32 反向爆破工具

反向推导已知 CRC32 值的原始数据。

**功能：**
- 支持自定义字符集
- 支持多个 CRC 值批量处理
- 支持可打印 ASCII 字符模式
- 自动识别十六进制和十进制输入

**使用示例：**
```bash
# 基本用法
python CRC爆破.py -c 0xf72c104b -l 5

# 使用自定义字符集
python CRC爆破.py -c f72c104b -l 5 --charset "0123456789abcdef"

# 仅使用可打印字符
python CRC爆破.py -c 0xf72c104b -l 4 --printable

# 批量处理多个 CRC 值
python CRC爆破.py -c 0xf72c104b 0x39004188 -l 5

# 显示所有结果（不限制显示数量）
python CRC爆破.py -c 0xf72c104b -l 5 --max-results 0
```

**参数说明：**
- `-c, --crc`: CRC32 值（必需，支持多个）
- `-l, --length`: 原始数据长度（必需）
- `--charset`: 自定义字符集
- `--printable`: 仅使用可打印 ASCII 字符
- `--max-results`: 显示的最大结果数（默认 10，0 表示全部）
- `-v, --verbose`: 显示详细信息

---

### 2. misc.py - MISC 工具集

包含文件关键字搜索、DNA 编码解码等常用功能。

**功能：**
- 文件中搜索常用关键字（flag, password, secret 等）
- DNA 编码解码（3-to-1 编码）
- Base64 编码提示

**使用示例：**

**搜索关键字：**
```bash
# 使用默认关键字列表搜索
python misc.py search output.txt

# 使用自定义关键字
python misc.py search data.bin -k flag password key

# 区分大小写搜索
python misc.py search file.txt -c

# 调整显示长度
python misc.py search file.txt -m 100
```

**DNA 解码：**
```bash
# 直接解码
python misc.py dna TCATCAACAAAT

# 从文件读取
python misc.py dna -f dna_cipher.txt
```

**查看 Base64 提示：**
```bash
python misc.py base64-hints
```

---

### 3. 。？！brainfuck.py - Short Ook/Brainfuck 解码工具

将 Short Ook 符号（。？！）转换为 Brainfuck 代码并执行。

**符号映射：**
- `。。` → `+` (加 1)
- `！！` → `-` (减 1)
- `。？` → `>` (指针右移)
- `？。` → `<` (指针左移)
- `！？` → `[` (循环开始)
- `？！` → `]` (循环结束)
- `！。` → `.` (输出)
- `。！` → `,` (输入)

**使用示例：**
```bash
# 直接解码
python 。？！brainfuck.py -c "。。。。！？！！。？？！"

# 从文件读取
python 。？！brainfuck.py -f cipher.txt

# 显示转换后的 Brainfuck 代码
python 。？！brainfuck.py -f cipher.txt --show-bf

# 调整内存大小
python 。？！brainfuck.py -f cipher.txt -m 50000

# 详细模式
python 。？！brainfuck.py -f cipher.txt -v
```

---

### 4. 压缩包套娃.py - 嵌套压缩包解压工具

自动递归解压嵌套的压缩包，支持多种格式。

**支持的格式：**
- zip, rar, 7z
- tar.gz, tar.bz2, tar.xz
- gz, bz2, xz

**使用示例：**
```bash
# 基本用法
python 压缩包套娃.py flag.zip

# 限制最大解压深度
python 压缩包套娃.py nested.tar.gz --max-depth 100

# 详细模式
python 压缩包套娃.py archive.7z -v
```

**注意事项：**
- 工具会自动检测压缩包类型（使用 `file` 命令和文件扩展名）
- 优先使用 Python 库，如果缺少则尝试使用系统命令
- 解压后的文件会保存在与原压缩包相同的目录

---

## 安装依赖

### Python 包
```bash
# 基础依赖
pip install argparse

# CRC 爆破工具依赖
# （内置库，无需安装）

# 压缩包工具依赖
pip install py7zr rarfile
```

### 系统工具（Linux/macOS）
```bash
# Ubuntu/Debian
sudo apt-get install file unrar p7zip-full

# macOS
brew install file unrar p7zip
```

### 系统工具（Windows）
- 安装 7-Zip: https://www.7-zip.org/
- 安装 WinRAR: https://www.winrar.com/

---

## 快速开始

1. **查看工具帮助：**
   ```bash
   python <工具名>.py --help
   ```

2. **常见使用场景：**

   **场景 1：解压嵌套压缩包**
   ```bash
   python 压缩包套娃.py challenge.zip -v
   ```

   **场景 2：在解压后的文件中搜索 flag**
   ```bash
   python misc.py search output.txt
   ```

   **场景 3：CRC32 爆破**
   ```bash
   python CRC爆破.py -c 0x12345678 -l 6 --printable
   ```

   **场景 4：解码奇怪的符号**
   ```bash
   python 。？！brainfuck.py -f strange_symbols.txt
   ```

---

## 文件说明

- **CRC爆破.py** - CRC32 反向爆破
- **misc.py** - 杂项工具集合
- **。？！brainfuck.py** - Short Ook/Brainfuck 解码器
- **压缩包套娃.py** - 嵌套压缩包解压（推荐使用）
- **压缩包套娃2.py** - 旧版本（已被合并到压缩包套娃.py）
- **ringerzer0ctf.1.py** - RingZer0 CTF 特定题目脚本
- **ringerctfzer0ctf.2.py** - BeautifulSoup 测试脚本

---

## 提示与技巧

1. **所有工具都支持 `-h` 或 `--help` 参数查看详细帮助**

2. **使用 `-v` 参数获取更多调试信息**

3. **在 CTF 比赛中的典型工作流：**
   ```bash
   # 1. 解压嵌套压缩包
   python 压缩包套娃.py challenge.zip -v

   # 2. 查看解压出什么文件
   ls -la

   # 3. 在所有文件中搜索关键字
   python misc.py search * -k flag key password
   ```

4. **遇到 DNA 编码？**
   ```bash
   python misc.py dna ACGTACGT...
   ```

5. **遇到 Short Ook 编码？**
   ```bash
   python 。？！brainfuck.py -f cipher.txt --show-bf
   ```

---

## 贡献

如果在使用过程中遇到新的编码类型或有用的工具，欢迎添加到这个工具集中！

## License

MIT License - 自由使用，用于学习和 CTF 比赛。
