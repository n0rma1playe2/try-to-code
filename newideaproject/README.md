# 抢课程序使用说明文档

## 1. 程序简介

本程序是一个自动化抢课工具，旨在帮助用户更高效地选择和监控课程。程序支持课程搜索、状态监控、自动抢课、批量选课等功能，并提供完善的异常处理和日志记录机制，确保程序稳定运行。

### 主要功能特点
- 自动登录和会话管理
- 智能课程搜索和状态查询
- 实时课程监控和自动抢课
- 批量选课功能
- 完善的异常处理和自动重试机制
- 详细的日志记录和进度保存
- 支持断点续传（批量选课时）

## 2. 安装与配置

### 2.1 环境要求
- Python 3.7 或更高版本
- 必要的Python库：requests, colorlog（可选，用于彩色日志输出）

### 2.2 安装依赖

使用pip安装所需依赖：

```bash
pip install requests colorlog
```

### 2.3 配置文件

程序首次运行时会自动创建默认配置文件 `config.json`，您需要修改其中的配置信息：

```json
{
    "username": "您的学号",
    "password": "您的密码",
    "monitor_interval": 1.0,
    "max_retries": 3,
    "timeout": 10
}
```

配置参数说明：
- `username`: 您的学生账号
- `password`: 您的账号密码
- `monitor_interval`: 课程监控间隔时间（秒）
- `max_retries`: 网络请求最大重试次数
- `timeout`: 网络请求超时时间（秒）

## 3. 使用方法

### 3.1 基本使用流程

1. 确保已正确配置 `config.json` 文件
2. 运行主程序：

```bash
python 抢课.py
```

3. 根据命令行提示进行操作

### 3.2 主要功能使用

#### 3.2.1 搜索课程

使用 `search_courses` 方法搜索课程：

```python
from 抢课 import CourseGrabber

# 初始化抢课器
course_grabber = CourseGrabber()

# 登录
course_grabber.login(username, password)

# 搜索课程
courses = course_grabber.search_courses(keyword="计算机", page=1)

# 处理搜索结果
for course in courses:
    print(f"课程ID: {course['id']}, 课程名称: {course['name']}")
```

#### 3.2.2 监控课程状态

使用 `monitor_courses` 方法监控课程并自动抢课：

```python
# 定义要监控的课程列表
courses_to_monitor = [
    {"id": "12345", "name": "数据结构"},
    {"id": "67890", "name": "算法设计与分析"}
]

# 开始监控，设置监控时间为300秒，每3秒检查一次
course_grabber.monitor_courses(
    courses_to_monitor,
    monitor_time=300,
    interval=3.0,
    auto_select=True
)
```

#### 3.2.3 批量选课

使用 `batch_select_courses` 方法进行批量选课：

```python
# 定义要选择的课程列表
courses_to_select = [
    {"id": "12345", "name": "数据结构"},
    {"id": "67890", "name": "算法设计与分析"}
]

# 批量选课，每门课最多重试3次，间隔0.5秒
results = course_grabber.batch_select_courses(
    courses_to_select,
    retry_count=3,
    interval=0.5
)

# 查看结果
print(f"成功选课: {results['success_count']}门")
print(f"失败选课: {results['failed_count']}门")
```

### 3.3 命令行使用

程序提供交互式命令行界面，运行主程序后，按照提示输入相应的操作：

```
欢迎使用自动抢课系统
请选择操作:
1. 登录系统
2. 搜索课程
3. 监控课程
4. 批量选课
5. 退出系统
```

## 4. 异常处理

程序定义了以下主要异常类型，您在使用时可以进行捕获处理：

- `LoginError`: 登录相关错误
- `NetworkError`: 网络请求错误
- `CourseError`: 课程操作相关错误

示例：

```python
try:
    course_grabber.select_course("12345")
except LoginError as e:
    print(f"登录错误: {str(e)}")
    # 重新登录
    course_grabber.login(username, password)
except NetworkError as e:
    print(f"网络错误: {str(e)}")
    # 等待后重试
    time.sleep(2)
except CourseError as e:
    print(f"课程操作错误: {str(e)}")
except Exception as e:
    print(f"未知错误: {str(e)}")
```

## 5. 日志系统

程序使用Python标准库的logging模块记录日志，日志文件保存在 `logs` 目录下：

- `grab_course.log`: 主要日志文件（保留最近5个日志文件，每个文件最大10MB）
- 控制台输出：显示彩色日志（如果安装了colorlog库）

日志级别包括：DEBUG、INFO、WARNING、ERROR、CRITICAL

## 6. 高级功能

### 6.1 断点续传

批量选课过程中，如果程序意外中断，重新运行时会自动加载上次的进度，继续处理剩余课程。进度信息保存在 `batch_progress.json` 文件中。

### 6.2 智能重试

程序实现了智能重试机制，对于网络错误和其他临时故障会自动尝试重新连接和操作：

- 指数退避策略：重试间隔随失败次数增加而增长
- 登录状态自动检测和恢复
- 网络请求超时和连接错误处理

## 7. 常见问题与解决方案

### 7.1 登录失败
- 检查用户名和密码是否正确
- 确认网络连接正常
- 查看日志文件了解具体错误原因

### 7.2 抢课失败
- 可能是课程已满，请尝试监控课程状态等待空位
- 检查网络连接是否稳定
- 确认账号权限是否足够

### 7.3 程序运行缓慢
- 减少监控间隔时间
- 减少同时监控的课程数量
- 关闭不必要的日志输出（将日志级别设置为INFO或WARNING）

### 7.4 进度保存失败
- 检查程序是否有文件写入权限
- 确保磁盘空间充足

## 8. 注意事项

1. **使用合规性**：请确保您的使用行为符合学校相关规定
2. **频率控制**：避免过于频繁的请求，以免对服务器造成压力
3. **密码安全**：请勿在公共场合或不安全环境中使用本程序
4. **定期更新**：如有系统更新，程序可能需要相应调整

## 9. 版本历史

### v1.0
- 初始版本
- 实现基本的登录、搜索和选课功能

### v1.1
- 增强异常处理机制
- 添加完善的日志系统
- 实现批量选课和进度保存

### v1.2
- 优化代码结构，提升稳定性
- 增加智能重试和自动重连功能
- 改进用户界面和使用体验

## 10. 联系方式

如有问题或建议，请通过以下方式联系开发者：

- Email: developer@example.com
- GitHub: [https://github.com/example/course-grabber](https://github.com/example/course-grabber)

---

**免责声明**：本程序仅供学习和研究使用，使用者应遵守相关法律法规和学校规定。因使用本程序造成的任何后果，由使用者自行承担。
