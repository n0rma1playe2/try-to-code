# -*- coding: utf-8 -*-
"""
高校选课抢课程序
功能：自动化监控和抢选课程
作者：AI助手
日期：2024
"""

import json
import time
import random
import re
import os
import traceback
import requests
from typing import Dict, List, Optional, Tuple, Any
from datetime import datetime
from bs4 import BeautifulSoup
from logging.handlers import RotatingFileHandler

# 配置日志
import logging

# 确保日志目录存在
log_dir = "logs"
os.makedirs(log_dir, exist_ok=True)

# 配置日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# 清除已有的处理器
if logger.handlers:
    logger.handlers.clear()

# 创建文件日志处理器（带轮转）
file_handler = RotatingFileHandler(
    os.path.join(log_dir, "course_grabber.log"),
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5
)
file_handler.setLevel(logging.INFO)
file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(funcName)s - %(message)s')
file_handler.setFormatter(file_formatter)

# 创建控制台日志处理器
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

# 尝试使用彩色日志
try:
    import colorlog
    console_formatter = colorlog.ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )
    console_handler.setFormatter(console_formatter)
except ImportError:
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

# 添加处理器到logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 自定义异常类
class CourseGrabberError(Exception):
    """抢课程序基础异常类"""
    pass

class LoginError(CourseGrabberError):
    """登录相关错误"""
    pass

class NetworkError(CourseGrabberError):
    """网络相关错误"""
    pass

class CourseError(CourseGrabberError):
    """课程相关错误"""
    pass

# 创建日志目录
log_dir = 'logs'
os.makedirs(log_dir, exist_ok=True)

# 添加文件日志处理器，支持日志轮转
log_file = os.path.join(log_dir, f'course_grabber_{datetime.now().strftime("%Y%m%d")}.log')
file_handler = RotatingFileHandler(
    log_file,
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5  # 最多保留5个备份
)
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
))
logger.addHandler(file_handler)

# 添加控制台彩色日志支持
try:
    from colorlog import ColoredFormatter
    # 创建彩色控制台处理器
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)
    
    # 定义彩色格式
    formatter = ColoredFormatter(
        '%(log_color)s%(asctime)s - %(levelname)s - %(message)s%(reset)s',
        datefmt='%Y-%m-%d %H:%M:%S',
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white'
        }
    )
    console.setFormatter(formatter)
    
    # 移除默认的控制台处理器，添加彩色处理器
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler) and handler != file_handler:
            logger.removeHandler(handler)
    logger.addHandler(console)
except ImportError:
    logger.info("未安装colorlog库，使用默认日志格式")
    pass

# 自定义异常类
class CourseGrabberError(Exception):
    """抢课程序自定义异常基类"""
    def __init__(self, message, error_code=0):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)

class LoginError(CourseGrabberError):
    """登录相关异常"""
    def __init__(self, message, error_code=1001):
        super().__init__(message, error_code)

class NetworkError(CourseGrabberError):
    """网络相关异常"""
    def __init__(self, message, error_code=1002):
        super().__init__(message, error_code)

class CourseError(CourseGrabberError):
    """课程相关异常"""
    def __init__(self, message, error_code=1003):
        super().__init__(message, error_code)


class CourseGrabber:
    """
    抢课程序主类
    提供登录、课程查询、监控和抢课功能
    """
    
    def __init__(self, config_path: str = "config.json"):
        """
        初始化抢课程序
        
        Args:
            config_path: 配置文件路径
        """
        self.session = requests.Session()
        self.is_logged_in = False
        self.user_info = {}
        self.target_courses = []
        self.config = self.load_config(config_path)
        self.login_url = self.config.get("login_url", "")
        self.course_list_url = self.config.get("course_list_url", "")
        self.select_course_url = self.config.get("select_course_url", "")
        self.headers = {
            "User-Agent": self.config.get("user_agent", "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"),
            "Referer": self.login_url,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
    def load_config(self, config_path: str) -> Dict:
        """
        加载配置文件
        
        Args:
            config_path: 配置文件路径
            
        Returns:
            配置字典
        """
        try:
            with open(config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"配置文件 {config_path} 未找到，使用默认配置")
            return self.get_default_config()
        except json.JSONDecodeError:
            logger.error(f"配置文件 {config_path} 格式错误")
            return self.get_default_config()
    
    def get_default_config(self) -> Dict:
        """
        获取默认配置
        
        Returns:
            默认配置字典
        """
        return {
            "login_url": "https://example.com/login",
            "course_list_url": "https://example.com/courses",
            "select_course_url": "https://example.com/select",
            "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "retry_interval": 1.0,
            "max_retries": 5
        }
    
    def login(self, username: str, password: str) -> bool:
        """
        登录选课系统
        
        Args:
            username: 用户名
            password: 密码
            
        Returns:
            是否登录成功
            
        Raises:
            LoginError: 登录过程中出现的特定错误，如用户名密码错误或认证失败
            NetworkError: 网络相关错误，如连接失败、请求超时或HTTP错误
        """
        try:
            # 第一步：获取登录页面，可能需要CSRF token等
            logger.info(f"正在登录系统，用户名: {username}")
            login_page = self.session.get(self.login_url, headers=self.headers, timeout=10)
            login_page.raise_for_status()  # 检查HTTP错误
            
            # 解析页面获取可能需要的token
            soup = BeautifulSoup(login_page.text, 'html.parser')
            
            # 尝试获取CSRF token (根据实际页面结构修改)
            csrf_token = None
            token_input = soup.find('input', {'name': 'csrfmiddlewaretoken'}) or \
                         soup.find('input', {'name': '__RequestVerificationToken'})
            if token_input:
                csrf_token = token_input.get('value')
                logger.info("成功获取CSRF Token")
            
            # 构建登录表单数据
            login_data = {
                'username': username,
                'password': password
            }
            
            # 如果有token，添加到表单数据
            if csrf_token:
                login_data[token_input.get('name')] = csrf_token
            
            # 随机延迟避免检测
            self._random_delay()
            
            # 发送登录请求
            response = self.session.post(
                self.login_url,
                data=login_data,
                headers=self.headers,
                allow_redirects=True,
                timeout=15
            )
            response.raise_for_status()  # 检查HTTP错误
            
            # 检查登录是否成功（根据实际系统响应修改）
            # 以下是几种常见的判断方式，请根据实际情况选择或组合使用
            success_conditions = [
                # 1. 检查响应状态码
                response.status_code == 200,
                
                # 2. 检查是否有跳转（通常登录成功后会跳转）
                len(response.history) > 0,
                
                # 3. 检查响应内容中是否有特定标记
                ('欢迎' in response.text or 'welcome' in response.text.lower()),
                
                # 4. 检查是否包含登录失败的提示
                ('用户名或密码错误' not in response.text and 
                 'login failed' not in response.text.lower()),
                
                # 5. 检查Cookie中是否有登录凭证
                bool(self.session.cookies)
            ]
            
            # 根据多个条件综合判断登录是否成功
            if any(success_conditions):
                self.is_logged_in = True
                self.user_info['username'] = username
                logger.info(f"登录成功，用户名: {username}")
                return True
            else:
                error_msg = "登录失败，可能原因: 用户名或密码错误，或系统有验证码等其他验证"
                logger.error(error_msg)
                # 记录登录失败时的响应信息用于调试
                if len(response.text) < 5000:  # 避免记录过大的响应
                    logger.debug(f"登录失败响应内容: {response.text[:500]}")
                raise LoginError(error_msg)
                
        except requests.ConnectionError as e:
            error_msg = f"网络连接错误: {str(e)}"
            logger.error(error_msg)
            raise NetworkError(error_msg) from e
        except requests.Timeout as e:
            error_msg = f"网络请求超时: {str(e)}"
            logger.error(error_msg)
            raise NetworkError(error_msg) from e
        except requests.HTTPError as e:
            error_msg = f"HTTP错误: {str(e)}"
            logger.error(error_msg)
            # 401/403通常表示认证失败
            if e.response.status_code in (401, 403):
                raise LoginError(f"认证失败: {str(e)}") from e
            raise NetworkError(error_msg) from e
        except LoginError:
            # 直接重新抛出LoginError类型的异常
            raise
        except Exception as e:
            error_msg = f"登录过程中发生未知错误: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise LoginError(error_msg) from e
    
    def search_courses(self, keyword: str) -> List[Dict]:
        """
        搜索课程
        
        Args:
            keyword: 搜索关键词
            
        Returns:
            课程列表
            
        Raises:
            LoginError: 未登录或登录状态已失效
            NetworkError: 网络相关错误
            CourseError: 课程搜索相关错误
        """
        try:
            if not self.is_logged_in:
                error_msg = "未登录，无法搜索课程"
                logger.error(error_msg)
                raise LoginError(error_msg)
            
            logger.info(f"搜索课程: {keyword}")
            
            # 构建搜索参数
            search_params = {
                'keyword': keyword,
                'page': 1,
                'pagesize': 50,
                'timestamp': str(int(time.time() * 1000))  # 添加时间戳
            }
            
            # 随机延迟避免检测
            self._random_delay()
            
            # 发送搜索请求
            response = self.session.get(
                self.course_list_url,
                params=search_params,
                headers=self.headers,
                timeout=30  # 设置超时
            )
            response.raise_for_status()  # 检查HTTP错误
            
            courses = []
            
            # 尝试解析HTML响应
            if 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 根据实际页面结构提取课程信息（这里是示例，需要根据实际情况修改）
                # 示例1：查找表格中的课程行
                course_rows = soup.find_all('tr', class_='course-row') or \
                              soup.select('table.course-table tr') or \
                              soup.find_all('div', class_='course-item')
                
                if not course_rows:
                    logger.warning(f"未找到课程元素，请检查选择器是否正确")
                    logger.debug(f"页面部分内容: {response.text[:500] if len(response.text) > 500 else response.text}")
                
                for row in course_rows:
                    # 提取课程ID
                    course_id = None
                    id_element = row.find('input', {'name': 'courseId'}) or \
                                row.find('a', href=True) or \
                                row.find('td', class_='course-id')
                    
                    if id_element and id_element.get('value'):
                        course_id = id_element.get('value')
                    elif id_element and id_element.get('href'):
                        # 尝试从链接中提取ID
                        import re
                        match = re.search(r'courseId=(\d+)', id_element.get('href'))
                        if match:
                            course_id = match.group(1)
                    elif id_element:
                        course_id = id_element.text.strip()
                    
                    # 提取课程名称
                    name_element = row.find('td', class_='course-name') or \
                                  row.find('div', class_='course-title') or \
                                  row.find('a', class_='course-link')
                    course_name = name_element.text.strip() if name_element else "未知课程"
                    
                    # 提取课程状态
                    status_element = row.find('td', class_='course-status') or \
                                   row.find('span', class_='status')
                    course_status = status_element.text.strip() if status_element else "未知状态"
                    
                    # 提取教师信息
                    teacher_element = row.find('td', class_='teacher') or \
                                     row.find('div', class_='teacher-info')
                    teacher = teacher_element.text.strip() if teacher_element else "未知教师"
                    
                    # 提取剩余名额
                    capacity_element = row.find('td', class_='capacity') or \
                                      row.find('span', class_='available')
                    capacity = capacity_element.text.strip() if capacity_element else "未知"
                    
                    if course_id:
                        course_info = {
                            'id': course_id,
                            'name': course_name,
                            'status': course_status,
                            'teacher': teacher,
                            'capacity': capacity,
                            'is_available': '可选' in course_status or 'available' in course_status.lower()
                        }
                        courses.append(course_info)
                        logger.debug(f"成功解析课程: {course_name} (ID: {course_id})")
            
            # 尝试解析JSON响应
            elif 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    data = response.json()
                    logger.debug(f"JSON响应数据类型: {type(data)}, 包含键: {list(data.keys()) if isinstance(data, dict) else None}")
                    
                    # 根据实际JSON结构提取课程信息
                    if isinstance(data, dict):
                        # 常见格式1：{'data': {'courses': [...]}}
                        courses_data = data.get('data', {}).get('courses', [])
                        # 常见格式2：{'courses': [...]}
                        if not courses_data:
                            courses_data = data.get('courses', [])
                        # 常见格式3：{'items': [...]}
                        if not courses_data:
                            courses_data = data.get('items', [])
                    elif isinstance(data, list):
                        courses_data = data
                    else:
                        courses_data = []
                    
                    # 处理课程数据
                    if isinstance(courses_data, list):
                        for course in courses_data:
                            course_info = {
                                'id': str(course.get('id', course.get('courseId', ''))),
                                'name': course.get('name', course.get('courseName', '未知课程')),
                                'status': course.get('status', '未知状态'),
                                'teacher': course.get('teacher', '未知教师'),
                                'capacity': f"{course.get('available', 0)}/{course.get('total', 0)}",
                                'is_available': bool(course.get('available', 0) > 0)
                            }
                            courses.append(course_info)
                            logger.debug(f"成功解析JSON课程: {course_info['name']} (ID: {course_info['id']})")
                    else:
                        logger.warning(f"课程数据不是列表格式: {type(courses_data)}")
                except json.JSONDecodeError as e:
                    error_msg = f"JSON响应格式错误: {str(e)}"
                    logger.error(error_msg)
                    logger.debug(f"响应内容: {response.text[:500]}")
                    raise CourseError(error_msg) from e
            else:
                # 处理未知响应类型
                content_type = response.headers.get('Content-Type', '未知')
                logger.warning(f"未知的响应类型: {content_type}")
                logger.debug(f"响应前500字符: {response.text[:500]}")
            
            logger.info(f"搜索完成，找到 {len(courses)} 门课程")
            return courses
            
        except requests.ConnectionError as e:
            error_msg = f"搜索课程时网络连接错误: {str(e)}"
            logger.error(error_msg)
            raise NetworkError(error_msg) from e
        except requests.Timeout as e:
            error_msg = f"搜索课程时请求超时: {str(e)}"
            logger.error(error_msg)
            raise NetworkError(error_msg) from e
        except requests.HTTPError as e:
            error_msg = f"搜索课程时HTTP错误: {str(e)}"
            logger.error(error_msg)
            # 如果是401或403错误，可能是登录状态已失效
            if e.response.status_code in [401, 403]:
                self.is_logged_in = False
                raise LoginError(f"登录状态已失效: {str(e)}") from e
            raise NetworkError(error_msg) from e
        except (LoginError, CourseError, NetworkError):
            # 直接重新抛出已知类型的异常
            raise
        except Exception as e:
            error_msg = f"搜索课程过程中发生未知错误: {str(e)}"
            logger.error(error_msg)
            logger.debug(traceback.format_exc())
            raise CourseError(error_msg) from e
    
    def get_course_status(self, course_id: str) -> Tuple[bool, str]:
        """
        获取课程状态
        
        Args:
            course_id: 课程ID
            
        Returns:
            (是否可抢, 状态描述)
            
        Raises:
            LoginError: 未登录或登录状态已失效
            NetworkError: 网络请求失败
            CourseError: 课程状态解析错误
        """
        try:
            # 检查是否已登录
            if not self.is_logged_in:
                error_msg = "未登录，无法获取课程状态"
                logger.error(error_msg)
                raise LoginError(error_msg)
            
            logger.info(f"获取课程状态，课程ID: {course_id}")
            
            # 随机延迟避免检测
            self._random_delay()
            
            # 构建查询参数
            status_params = {
                'courseId': course_id
            }
            
            # 发送状态查询请求
            # 这里使用课程列表URL加上课程ID参数，实际系统可能有专门的状态查询接口
            status_url = self.config.get("course_status_url", self.course_list_url)
            response = self.session.get(
                status_url,
                params=status_params,
                headers=self.headers,
                timeout=10
            )
            response.raise_for_status()  # 检查HTTP错误
            
            # 处理HTML响应
            if 'text/html' in response.headers.get('Content-Type', ''):
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # 查找课程状态信息
                status_element = soup.find('div', class_='course-status') or \
                                soup.find('span', class_='status') or \
                                soup.find('td', class_='course-status')
                
                if status_element:
                    status_text = status_element.text.strip()
                    # 判断是否可选
                    is_available = any(keyword in status_text for keyword in ['可选', 'available', '有剩余', '可抢']) or \
                                  any(keyword not in status_text for keyword in ['已满', 'closed', '不可选'])
                    return is_available, status_text
                else:
                    # 尝试查找容量信息来判断是否可选
                    capacity_element = soup.find('div', class_='capacity') or \
                                      soup.find('span', class_='available')
                    if capacity_element:
                        capacity_text = capacity_element.text.strip()
                        # 尝试从容量信息中提取可用数量
                        import re
                        match = re.search(r'(\d+)/(\d+)', capacity_text)
                        if match:
                            available = int(match.group(1))
                            total = int(match.group(2))
                            is_available = available > 0
                            return is_available, f"剩余 {available}/{total}"
                    
                    return False, "无法获取课程状态"
            
            # 处理JSON响应
            elif 'application/json' in response.headers.get('Content-Type', ''):
                try:
                    data = response.json()
                    # 尝试多种常见的JSON结构
                    if isinstance(data, dict):
                        # 格式1: {'status': '...', 'available': true}
                        if 'available' in data:
                            return bool(data['available']), data.get('status', '未知状态')
                        # 格式2: {'data': {'status': '...', 'capacity': {...}}}
                        elif 'data' in data:
                            data = data['data']
                            if 'available' in data:
                                return bool(data['available']), data.get('status', '未知状态')
                            elif 'capacity' in data:
                                capacity = data['capacity']
                                if isinstance(capacity, dict) and 'available' in capacity:
                                    available = capacity['available']
                                    total = capacity.get('total', available)
                                    return available > 0, f"剩余 {available}/{total}"
                    
                    return False, "无法解析状态信息"
                except json.JSONDecodeError as e:
                    logger.error("JSON响应格式错误")
                    # 记录响应内容用于调试
                    if len(response.text) < 5000:
                        logger.debug(f"无法解析的JSON响应内容: {response.text[:500]}")
                    raise CourseError("响应格式错误: 无法解析JSON数据") from e
            
            return False, "未知响应格式"
            
        except requests.exceptions.ConnectionError as e:
            error_msg = f"网络连接失败: {str(e)}"
            logger.error(error_msg)
            raise NetworkError(error_msg)
        except requests.exceptions.Timeout as e:
            error_msg = f"请求超时: {str(e)}"
            logger.error(error_msg)
            raise NetworkError(error_msg)
        except requests.exceptions.HTTPError as e:
            error_msg = f"HTTP错误: {str(e)}"
            logger.error(error_msg)
            # 如果是401或403错误，可能是登录状态已失效
            if e.response.status_code in [401, 403]:
                self.is_logged_in = False
                raise LoginError(f"登录状态已失效: {str(e)}") from e
            raise NetworkError(error_msg) from e
        except (LoginError, NetworkError, CourseError):
            raise  # 重新抛出这些异常
        except Exception as e:
            error_msg = f"获取课程状态时发生未知错误: {str(e)}"
            logger.error(error_msg, exc_info=True)
            raise CourseError(error_msg) from e
    
    def select_course(self, course_id: str) -> Tuple[bool, str]:
        """
        选择课程
        
        Args:
            course_id: 课程ID
            
        Returns:
            (是否成功, 消息)
            
        Raises:
            LoginError: 未登录或登录状态已失效
            NetworkError: 网络请求错误
            CourseError: 课程相关错误
        """
        # 参数验证
        if not course_id or not isinstance(course_id, str):
            logger.error(f"无效的课程ID: {course_id}")
            raise CourseError(f"无效的课程ID: {course_id}")
        
        # 检查登录状态
        if not self.is_logged_in:
            logger.error("未登录或登录已失效")
            raise LoginError("未登录或登录已失效，无法选课")
        
        # 确保会话有效
        if not hasattr(self, 'session') or self.session is None:
            logger.error("会话不存在")
            self.is_logged_in = False
            raise NetworkError("会话不存在，请重新登录")
        
        logger.info(f"尝试选择课程: {course_id}")
        
        try:
            # 构建选课请求
            headers = self._get_headers()
            headers['Content-Type'] = 'application/x-www-form-urlencoded'
            
            data = {
                'courseId': course_id,
                'operationType': 'select',
                'submitType': 'confirm'
            }
            
            # 添加随机延迟避免被检测
            self._random_delay(0.2, 0.1)
            
            # 发送选课请求
            response = self.session.post(
                self.config['api_urls']['select_course'],
                headers=headers,
                data=data,
                timeout=self.config['timeout']
            )
            
            # 检查HTTP状态码
            response.raise_for_status()
            logger.debug(f"选课请求响应状态码: {response.status_code}")
            
            # 处理JSON响应
            if response.headers.get('Content-Type', '').startswith('application/json'):
                try:
                    result = response.json()
                    logger.debug(f"选课JSON响应: {result}")
                    
                    # 解析JSON响应
                    if isinstance(result, dict):
                        # 检查常见的成功字段
                        if result.get('success') or result.get('code') == 200:
                            message = result.get('message', '选课成功')
                            return True, message
                        else:
                            message = result.get('message', result.get('error', '选课失败'))
                            return False, message
                    else:
                        return self._parse_result_message(str(result))
                except json.JSONDecodeError as e:
                    logger.error(f"JSON解析错误: {str(e)}")
                    logger.debug(f"原始响应: {response.text}")
                    # 尝试作为普通文本处理
                    return self._parse_result_message(response.text)
            
            # 处理HTML响应
            elif response.headers.get('Content-Type', '').startswith('text/html'):
                soup = BeautifulSoup(response.text, 'html.parser')
                # 尝试提取消息
                message_elem = soup.select_one('.message, .info, .result, #message')
                if message_elem:
                    message = message_elem.get_text().strip()
                else:
                    # 如果找不到特定元素，提取所有文本
                    message = soup.get_text().strip()
                logger.debug(f"HTML响应提取的消息: {message}")
                return self._parse_result_message(message)
            
            # 处理纯文本响应
            else:
                text = response.text.strip()
                logger.debug(f"纯文本响应: {text}")
                return self._parse_result_message(text)
                
        except requests.ConnectionError as e:
            logger.error(f"连接错误: {str(e)}")
            raise NetworkError(f"连接错误: {str(e)}") from e
        except requests.Timeout as e:
            logger.error(f"请求超时: {str(e)}")
            raise NetworkError(f"请求超时: {str(e)}") from e
        except requests.HTTPError as e:
            logger.error(f"HTTP错误: {str(e)}")
            # 检查是否是登录失效（401/403）
            if e.response.status_code in (401, 403):
                self.is_logged_in = False
                raise LoginError("登录已失效，请重新登录") from e
            raise NetworkError(f"HTTP错误: {str(e)}") from e
        except Exception as e:
            logger.error(f"选课过程中发生未知错误: {str(e)}", exc_info=True)
            raise CourseError(f"选课过程中发生错误: {str(e)}") from e

    def _parse_result_message(self, message: str) -> Tuple[bool, str]:
        """
        解析选课结果消息，判断是否成功
        
        Args:
            message: 原始消息文本
            
        Returns:
            (是否成功, 处理后的消息)
        """
        # 成功关键词列表
        success_keywords = [
            '成功', 'success', '选课成功', 'selected', '已选',
            '成功选', '选课完成', '已加入', '加入成功'
        ]
        
        # 失败关键词列表
        failure_keywords = [
            '失败', 'failure', '已满', 'closed', '不可选',
            '冲突', 'conflict', '已选过', '重复', 'error',
            '超时', 'timeout', '系统繁忙', '网络错误'
        ]
        
        # 转为小写进行匹配
        message_lower = message.lower()
        
        # 检查是否包含成功关键词
        for keyword in success_keywords:
            if keyword.lower() in message_lower:
                return True, message
        
        # 检查是否包含失败关键词
        for keyword in failure_keywords:
            if keyword.lower() in message_lower:
                return False, message
        
        # 默认情况，尝试根据消息内容判断
        # 如果消息很短或者包含某些特定字符，可能是错误
        if len(message) < 5:
            return False, f"未知响应: {message}"
        
        # 其他情况返回默认值
        return False, message
    
    def add_target_course(self, course_id: str, course_name: str):
        """
        添加目标课程
        
        Args:
            course_id: 课程ID
            course_name: 课程名称
        """
        self.target_courses.append({"id": course_id, "name": course_name})
        logger.info(f"已添加目标课程: {course_name} (ID: {course_id})")
    
    def monitor_courses(self, interval: float = 1.0, max_attempts: int = None):
        """
        监控目标课程并尝试抢课
        
        Args:
            interval: 监控间隔(秒)
            max_attempts: 最大尝试次数
            
        Raises:
            LoginError: 登录失败且无法自动重连
            NetworkError: 网络连接持续失败
            CourseError: 课程相关错误
        """
        # 验证参数
        if interval < 0.1:
            logger.warning(f"监控间隔过小 ({interval}s)，已调整为 0.1s")
            interval = 0.1
        
        if not self.is_logged_in:
            logger.error("未登录，无法监控课程")
            raise LoginError("未登录，无法监控课程")
        
        if not self.target_courses:
            logger.error("没有设置目标课程，请先添加目标课程")
            raise CourseError("没有设置目标课程，请先添加目标课程")
        
        logger.info(f"开始监控 {len(self.target_courses)} 门课程")
        logger.info(f"监控间隔: {interval}秒")
        if max_attempts:
            logger.info(f"最大尝试次数: {max_attempts}")
        
        attempt_count = 0
        success_count = 0
        start_time = datetime.now()
        consecutive_failures = 0
        max_consecutive_failures = 10  # 最大连续失败次数
        
        try:
            while True:
                # 检查是否达到最大尝试次数
                if max_attempts and attempt_count >= max_attempts:
                    logger.info(f"已达到最大尝试次数 {max_attempts}，停止监控")
                    break
                
                # 检查登录状态，如果已断开则尝试重新登录
                if not self.is_logged_in:
                    logger.warning("登录状态已断开，尝试重新登录...")
                    # 如果配置了自动重连功能
                    if hasattr(self, '_last_login_info') and self._last_login_info:
                        try:
                            username, password = self._last_login_info
                            logger.info(f"尝试使用保存的凭据重新登录用户: {username}")
                            self.login(username, password)
                            logger.info("重新登录成功")
                            consecutive_failures = 0  # 重置连续失败计数
                        except Exception as e:
                            logger.error(f"重新登录失败: {str(e)}")
                            consecutive_failures += 1
                            if consecutive_failures >= 3:
                                raise LoginError("连续3次重连失败，请手动重新登录") from e
                            # 等待一段时间后重试
                            time.sleep(3)
                            continue
                    else:
                        raise LoginError("登录已断开，无可用的登录凭据进行自动重连")
                
                # 检查所有目标课程
                for course in self.target_courses[:]:  # 使用副本，避免遍历时修改列表
                    # 跳过已经成功抢到的课程
                    if course.get('grabbed', False):
                        continue
                    
                    try:
                        # 获取课程状态
                        is_available, status_text = self.get_course_status(course['id'])
                        current_time = datetime.now().strftime('%H:%M:%S.%f')[:-3]
                        
                        if is_available:
                            logger.info(f"[{current_time}] 课程可抢！{course['name']} (ID: {course['id']}) - 状态: {status_text}")
                            print(f"\n[{current_time}] 发现可抢课程: {course['name']}！")
                            print(f"状态: {status_text}")
                            
                            # 尝试抢课
                            success, message = self.select_course(course['id'])
                            
                            if success:
                                logger.info(f"[{current_time}] 抢课成功！{course['name']} - 消息: {message}")
                                print(f"[{current_time}] ✅ 抢课成功: {course['name']}！")
                                print(f"消息: {message}")
                                
                                # 标记课程已抢到
                                course['grabbed'] = True
                                course['grab_time'] = current_time
                                course['message'] = message
                                success_count += 1
                                consecutive_failures = 0  # 重置连续失败计数
                                
                                # 如果所有课程都抢到了，停止监控
                                if all(c.get('grabbed', False) for c in self.target_courses):
                                    logger.info("所有目标课程都已抢到，停止监控")
                                    print("\n🎉 所有目标课程都已抢到！")
                                    return
                            else:
                                logger.warning(f"[{current_time}] 抢课失败: {course['name']} - 原因: {message}")
                                print(f"[{current_time}] ❌ 抢课失败: {course['name']}")
                                print(f"原因: {message}")
                                consecutive_failures += 1
                        else:
                            # 只在日志中记录不可抢的状态，避免输出过多
                            logger.debug(f"[{current_time}] 课程不可抢: {course['name']} - 状态: {status_text}")
                            # 课程不可抢不算失败
                            consecutive_failures = 0
                    except LoginError as e:
                        logger.error(f"登录错误: {str(e)}", exc_info=True)
                        self.is_logged_in = False
                        consecutive_failures += 1
                        # 跳出课程循环，重新尝试登录
                        break
                    except NetworkError as e:
                        logger.error(f"网络错误: {str(e)}", exc_info=True)
                        consecutive_failures += 1
                        # 网络错误时暂停一下再继续
                        time.sleep(1)
                    except CourseError as e:
                        logger.error(f"课程相关错误: {str(e)}", exc_info=True)
                        consecutive_failures += 1
                    except Exception as e:
                        logger.error(f"监控课程 {course['name']} 时出错: {str(e)}", exc_info=True)
                        consecutive_failures += 1
                
                # 检查连续失败次数
                if consecutive_failures >= max_consecutive_failures:
                    logger.error(f"连续失败 {consecutive_failures} 次，可能存在问题，停止监控")
                    print(f"\n❌ 连续失败次数过多，请检查网络或配置")
                    break
                
                # 增加尝试次数
                attempt_count += 1
                
                # 计算并显示进度
                elapsed = (datetime.now() - start_time).total_seconds()
                if attempt_count % 10 == 0:  # 每10次尝试显示一次进度
                    print(f"\r监控中... 已尝试 {attempt_count} 次, 耗时 {elapsed:.1f} 秒, 成功 {success_count} 门", end="", flush=True)
                
                # 随机延迟，避免被服务器检测
                actual_interval = interval + random.uniform(-0.2, 0.2)  # 添加小的随机变化
                if actual_interval < 0.2:  # 确保最小延迟
                    actual_interval = 0.2
                
                time.sleep(actual_interval)
                
        except KeyboardInterrupt:
            logger.info("用户中断监控")
            print("\n\n⚠️  监控已中断")
        except Exception as e:
            logger.error(f"监控过程中发生未知错误: {str(e)}", exc_info=True)
            print(f"\n❌ 监控出错: {str(e)}")
            raise
        finally:
            # 显示监控统计
            elapsed = (datetime.now() - start_time).total_seconds()
            logger.info(f"监控结束，共尝试 {attempt_count} 次，耗时 {elapsed:.1f} 秒，成功抢到 {success_count} 门课程")
            print(f"\n\n📊 监控统计:")
            print(f"  总尝试次数: {attempt_count}")
            print(f"  总耗时: {elapsed:.1f} 秒")
            print(f"  成功抢到: {success_count} 门课程")
            print(f"  连续失败: {consecutive_failures} 次")
            
            # 显示每门课程的状态
            if self.target_courses:
                print("\n📋 课程状态:")
                for course in self.target_courses:
                    status = "✅ 已抢到" if course.get('grabbed', False) else "❌ 未抢到"
                    grab_info = f" (抢到时间: {course.get('grab_time', '')})" if course.get('grabbed', False) else ""
                    print(f"  {status} - {course['name']}{grab_info}")
    
    def batch_select_courses(self, course_list: List[Dict], retry_count: int = 3, interval: float = 0.5):
        """
        批量选择课程
        
        Args:
            course_list: 课程列表，每门课程包含id和name字段
            retry_count: 每门课程失败后的重试次数
            interval: 课程间隔时间（秒）
            
        Returns:
            dict: 包含统计信息的字典
                - success_count: 成功课程数量
                - failed_count: 失败课程数量
                - results: 详细结果列表
                
        Raises:
            LoginError: 未登录或登录状态已失效
            NetworkError: 网络请求错误
            ValueError: 参数无效
        """
        # 参数验证
        if not isinstance(course_list, list):
            raise ValueError("course_list必须是列表类型")
        
        if not course_list:
            logger.warning("课程列表为空，无需批量选课")
            return {
                'success_count': 0,
                'failed_count': 0,
                'results': []
            }
        
        if retry_count < 0:
            logger.warning(f"重试次数为负数 ({retry_count})，已设为0")
            retry_count = 0
        
        if interval < 0:
            logger.warning(f"间隔时间为负数 ({interval})，已设为0.5秒")
            interval = 0.5
        
        # 检查登录状态
        if not self.is_logged_in:
            logger.error("未登录或登录已失效")
            raise LoginError("未登录或登录已失效，无法进行批量选课")
        
        logger.info(f"开始批量选课，共 {len(course_list)} 门课程")
        logger.info(f"每门课程最大尝试次数: {retry_count + 1}")
        logger.info(f"课程间隔时间: {interval}秒")
        
        success_count = 0
        failed_count = 0
        results = []
        start_time = datetime.now()
        
        # 课程进度跟踪
        progress_file = None
        progress_data = {}
        
        # 尝试加载之前的进度（如果有）
        try:
            if os.path.exists('batch_progress.json'):
                with open('batch_progress.json', 'r', encoding='utf-8') as f:
                    progress_data = json.load(f)
                logger.info(f"已加载之前的进度，剩余 {len(progress_data.get('remaining_courses', []))} 门课程")
                # 使用剩余课程列表
                if progress_data.get('remaining_courses'):
                    course_list = progress_data['remaining_courses']
        except Exception as e:
            logger.warning(f"加载进度文件失败: {str(e)}")
        
        try:
            # 打开进度文件用于实时保存
            progress_file = open('batch_progress.json', 'w', encoding='utf-8')
            
            for index, course in enumerate(course_list):
                # 参数检查
                if not isinstance(course, dict) or 'id' not in course:
                    logger.error(f"无效的课程数据: {course}")
                    failed_count += 1
                    results.append({
                        'course_id': 'unknown',
                        'course_name': 'unknown',
                        'success': False,
                        'message': '无效的课程数据',
                        'attempts': 0
                    })
                    continue
                
                course_id = course['id']
                course_name = course.get('name', f'课程_{course_id}')
                attempts = 0
                success = False
                final_message = "未尝试"
                
                logger.info(f"[{index+1}/{len(course_list)}] 开始处理课程: {course_name} (ID: {course_id})")
                
                # 尝试选课，包括重试
                for attempt in range(retry_count + 1):
                    attempts += 1
                    
                    try:
                        # 添加随机延迟，避免被检测
                        actual_interval = interval + random.uniform(-0.2, 0.2)
                        if actual_interval > 0:
                            time.sleep(actual_interval)
                        
                        logger.info(f"[{course_name}] 第 {attempts}/{retry_count+1} 次尝试选课")
                        
                        # 尝试选课
                        success, message = self.select_course(course_id)
                        final_message = message
                        
                        if success:
                            logger.info(f"[{course_name}] 选课成功: {message}")
                            success_count += 1
                            break
                        else:
                            logger.warning(f"[{course_name}] 第 {attempts} 次选课失败: {message}")
                            # 如果不是最后一次尝试，等待一段时间后重试
                            if attempt < retry_count:
                                # 指数退避策略
                                retry_delay = interval * (2 ** attempt) + random.uniform(0, 1)
                                logger.info(f"[{course_name}] 将在 {retry_delay:.2f} 秒后重试")
                                time.sleep(retry_delay)
                    except LoginError as e:
                        logger.error(f"[{course_name}] 登录错误: {str(e)}")
                        self.is_logged_in = False
                        # 尝试重新登录（如果有凭据）
                        if hasattr(self, '_last_login_info') and self._last_login_info:
                            try:
                                username, password = self._last_login_info
                                logger.info(f"尝试重新登录用户: {username}")
                                self.login(username, password)
                                logger.info("重新登录成功，继续选课")
                                # 重新进行本次尝试
                                attempt -= 1
                                continue
                            except Exception as re:
                                logger.error(f"重新登录失败: {str(re)}")
                                final_message = f"登录失败: {str(e)}"
                                break
                        else:
                            final_message = f"登录失败: {str(e)}"
                            break
                    except NetworkError as e:
                        logger.error(f"[{course_name}] 网络错误: {str(e)}")
                        # 网络错误可以重试
                        final_message = f"网络错误: {str(e)}"
                        if attempt < retry_count:
                            time.sleep(2)
                            continue
                        else:
                            break
                    except Exception as e:
                        logger.error(f"[{course_name}] 选课异常: {str(e)}", exc_info=True)
                        final_message = f"异常: {str(e)}"
                        # 其他异常也尝试重试
                        if attempt < retry_count:
                            time.sleep(1)
                            continue
                        else:
                            break
                
                if not success:
                    failed_count += 1
                
                # 记录结果
                results.append({
                    'course_id': course_id,
                    'course_name': course_name,
                    'success': success,
                    'message': final_message,
                    'attempts': attempts,
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                })
                
                # 更新进度信息
                remaining_courses = course_list[index+1:]
                progress_data = {
                    'processed_count': index + 1,
                    'total_count': len(course_list),
                    'success_count': success_count,
                    'failed_count': failed_count,
                    'remaining_courses': remaining_courses,
                    'last_updated': datetime.now().isoformat()
                }
                
                # 保存进度
                try:
                    progress_file.seek(0)
                    progress_file.truncate()
                    json.dump(progress_data, progress_file, ensure_ascii=False, indent=2)
                    progress_file.flush()
                except Exception as e:
                    logger.warning(f"保存进度失败: {str(e)}")
                
                # 显示进度
                elapsed = (datetime.now() - start_time).total_seconds()
                print(f"\r进度: {index+1}/{len(course_list)} ({(index+1)/len(course_list)*100:.1f}%) | "
                      f"成功: {success_count} | 失败: {failed_count} | "
                      f"耗时: {elapsed:.1f}秒", end="", flush=True)
            
            # 选课完成，删除进度文件
            try:
                if os.path.exists('batch_progress.json'):
                    os.remove('batch_progress.json')
                logger.info("批量选课完成，已删除进度文件")
            except Exception as e:
                logger.warning(f"删除进度文件失败: {str(e)}")
                
        except KeyboardInterrupt:
            logger.info("用户中断批量选课")
            print("\n\n⚠️  批量选课已中断")
        except Exception as e:
            logger.error(f"批量选课过程中发生未知错误: {str(e)}", exc_info=True)
            print(f"\n❌ 批量选课出错: {str(e)}")
        finally:
            # 关闭进度文件
            if progress_file and not progress_file.closed:
                try:
                    progress_file.close()
                except:
                    pass
            
            # 计算总耗时
            total_time = (datetime.now() - start_time).total_seconds()
            logger.info(f"批量选课结束，总耗时: {total_time:.1f}秒")
            logger.info(f"成功: {success_count}门，失败: {failed_count}门")
            
            # 显示总结
            print(f"\n\n📊 批量选课统计:")
            print(f"  总课程数: {len(course_list)}")
            print(f"  成功选课: {success_count} 门")
            print(f"  失败选课: {failed_count} 门")
            print(f"  总耗时: {total_time:.1f} 秒")
            print(f"  平均每门课耗时: {total_time/max(len(course_list), 1):.2f} 秒")
            
            # 构建返回结果
            return {
                'success_count': success_count,
                'failed_count': failed_count,
                'total_count': len(course_list),
                'total_time': total_time,
                'results': results
            }

    def logout(self):
        """
        退出登录
        """
        try:
            if not self.is_logged_in:
                logger.warning("未登录状态，无需退出")
                return
            
            # 尝试调用登出接口（如果有）
            logout_url = self.config.get("logout_url", "")
            if logout_url:
                response = self.session.get(logout_url, headers=self.headers)
                logger.info(f"调用登出接口，状态码: {response.status_code}")
            
            # 清除会话信息
            self.session.cookies.clear()
            self.is_logged_in = False
            self.user_info.clear()
            logger.info("退出登录成功，会话已清除")
            
        except Exception as e:
            logger.error(f"退出登录过程中发生错误: {str(e)}")
            # 即使出错也尝试清除本地状态
            self.is_logged_in = False
            self.user_info.clear()
    
    def _random_delay(self, base_delay: float = 0.5, variation: float = 0.3):
        """
        随机延迟，避免被服务器检测
        
        Args:
            base_delay: 基础延迟
            variation: 延迟变化范围
        """
        delay = base_delay + random.uniform(-variation, variation)
        if delay < 0.1:
            delay = 0.1
        time.sleep(delay)


def create_default_config(output_path: str = "config.json"):
    """
    创建默认配置文件
    
    Args:
        output_path: 输出路径
    """
    default_config = {
        "login_url": "https://example.com/login",
        "course_list_url": "https://example.com/courses",
        "select_course_url": "https://example.com/select",
        "user_agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "retry_interval": 1.0,
        "max_retries": 5,
        "monitor_interval": 0.5,
        "random_variation": 0.3
    }
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(default_config, f, ensure_ascii=False, indent=4)
    
    logger.info(f"默认配置文件已创建: {output_path}")


def main():
    """
    主函数，提供简单的命令行界面
    """
    print("=== 高校选课抢课程序 ===")
    
    # 检查是否有配置文件
    try:
        grabber = CourseGrabber()
    except Exception as e:
        print(f"初始化失败: {e}")
        print("正在创建默认配置文件...")
        create_default_config()
        print("请编辑 config.json 配置文件后重新运行")
        return
    
    # 这里将在后续实现中添加交互式命令行界面
    print("程序框架已创建，请根据实际选课系统完善具体实现")
    print("需要修改的主要功能：")
    print("1. 登录认证模块")
    print("2. 课程查询功能")
    print("3. 选课功能")
    print("4. 监控逻辑")


if __name__ == "__main__":
    main()



