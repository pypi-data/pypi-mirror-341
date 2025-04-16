#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
日志工具包使用示例
"""

import time
from src.utils.logger import (
    setup_logger,
    debug,
    info,
    warning,
    error,
    critical,
    log_function,
    set_level
)

# 示例1: 基本用法
def basic_usage():
    # 设置日志级别（可选，默认为INFO）
    set_level("DEBUG")
    
    # 记录不同级别的日志
    debug("这是一条调试日志")
    info("这是一条信息日志")
    warning("这是一条警告日志")
    error("这是一条错误日志")
    critical("这是一条严重错误日志")

# 示例2: 使用日志装饰器
@log_function
def example_function():
    """被装饰的函数，会自动记录函数调用开始和结束"""
    info("函数正在执行中...")
    time.sleep(1)  # 模拟函数执行
    return "函数执行成功"

@log_function(level="INFO")
def example_function_with_level():
    """指定日志级别的装饰器用法"""
    info("函数正在执行中...")
    time.sleep(1)  # 模拟函数执行
    return "函数执行成功"

# 示例3: 带异常的函数
@log_function
def function_with_exception():
    """演示异常记录功能"""
    info("函数开始执行，即将产生异常...")
    time.sleep(0.5)
    raise ValueError("这是一个示例异常")

# 示例4: 自定义日志存储位置和名称
def custom_logger_setup():
    # 初始化日志系统，自定义日志目录和文件名
    setup_logger(
        level="DEBUG",
        log_dir="./custom_logs",
        log_name="my_app"
    )
    info("使用自定义日志配置记录的日志")

if __name__ == "__main__":
    print("=== 示例1: 基本用法 ===")
    basic_usage()
    
    print("\n=== 示例2: 使用日志装饰器 ===")
    example_function()
    example_function_with_level()
    
    print("\n=== 示例3: 带异常的函数 ===")
    try:
        function_with_exception()
    except Exception as e:
        print(f"捕获到异常: {e}")
    
    print("\n=== 示例4: 自定义日志配置 ===")
    custom_logger_setup()
    
    print("\n所有日志都已保存到logs目录下的对应日期文件中") 