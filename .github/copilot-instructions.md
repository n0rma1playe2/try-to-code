## 仓库概览与目标

这是一个以示例脚本和练习为主的小型 Python 仓库，文件均位于仓库根目录。主要用作练手、解析/爬虫和 CTF 解题实验。AI 代理的主要目标是：快速定位可运行脚本、识别常见依赖（如 requests、BeautifulSoup）、并在不改变原意的前提下重构或补充文档和测试。

## 重要文件与模式（可搜索示例）
- `calc.py`: 小工具风格模块，导出基础算术函数：`plus/minus/multiply/divide`。适合作为可测试的单元示例。
- `pizza.py`: 展示了简单函数与可变参数（`make_pizza(size, *toppings)`）的模块/导入用例。
- `ringerzer0ctf.1.py` / `ringerctfzer0ctf.2.py`: 包含对外部 HTTP 服务的调用（使用 `requests`、`bs4`、`re`）来抓取并解析挑战页面——这是仓库中唯一明显的“集成/网络”代码路径。
- `test.py`、`lianxi.py`: 大量注释/练习代码，包含文件读写、字符串处理与常见数据结构模式，可作为重构或提取函数的来源。
- `encode.txt`: 存放编码字符串（Base64 风格），有时被脚本读取作为练习输入。

## 设计与约定（仅可发现的事实）
- 这是一个“脚本集合”而非库/包：没有 `setup.py` / `pyproject.toml` / `requirements.txt`。默认运行方式是直接使用 Python 运行单个脚本（例如 `python .\calc.py`）。
- 代码里大量注释与样例片段（练习/教学用途），因此改动时请尽量保留原注释或将其移入单元测试作为示例输入。
- 对外请求集中在 `ringer*` 文件：任何对这些文件的更改要特别注意不要无意中暴露凭证或对远程服务造成压力。

## 开发工作流 & 运行示例（供 AI 参考）
- 在 Windows PowerShell 下运行脚本：
  - python .\\calc.py
  - python .\\ringerzer0ctf.1.py
- 建议的临时虚拟环境与依赖安装（仓库未提供）:
  - python -m venv .venv
  - .\\.venv\\Scripts\\Activate.ps1
  - pip install requests beautifulsoup4 lxml
 说明：仅在修改或运行网络脚本时需要安装这些包。

## 提示与可操作任务（AI 应优先执行）
1. 当任务是“提取可测试逻辑”时，优先把小的独立函数（比如 `calc.py` 的算术函数或 `pizza.py` 的 `make_pizza`）改写为可导入模块并补充单元测试。
2. 对含网络请求的脚本（`ringer*`）做修改前，应添加开关（例如 `if __name__ == '__main__':`）并把外部请求抽象成可注入的函数以便单元测试（用模拟替代真实 HTTP 请求）。
3. 保持注释与练习段落：若要删除应先将其归档到 `docs/` 或测试示例，以保留教学价值。

## 风格与限制（从代码中推断）
- 代码更像教学/练习风格而非生产级：短小的脚本、未处理的异常、直接 print 输出。AI 不要自动把所有 print 替换为日志，除非 PR 明确要求。
- 不要添加全局依赖或构建系统（例如 CI 配置、requirements 文件）除非用户明确要求；可在 PR 描述中建议新增 `requirements.txt` 或 `pyproject.toml`。

## 示例片段（可直接引用以生成测试或重构）
- 算术函数（`calc.py`）:
  - plus(a,b) / minus(a,b) / multiply(a,b) / divide(a,b)
- 网络抓取（`ringerctfzer0ctf.2.py`）:
  - 使用 `requests.get(base_url)`，然后用 `BeautifulSoup(..., 'lxml')` 提取 `div.message` 并用正则提取数字。

## 当不确定时请询问
- 若需要修改网络交互（提交答案、跟远端交互），请先询问是否允许对外请求或是否应使用模拟数据。
- 如果要大规模重构（拆包、引入构建文件、添加 CI），请先列出预期改动清单以供确认。

---
请审阅此草稿并指出任何不准确或缺失的本地惯例；我可以根据你的反馈进行迭代更新。
