#!/usr/bin/env python3
"""
统一日志配置模块
支持不同日志级别，便于调试和性能测试
"""

import logging
import os
import sys
from typing import Optional


class WarehouseLogger:
    """仓库系统统一日志器"""
    
    def __init__(self, name: str, level: Optional[str] = None):
        """
        初始化日志器
        
        Args:
            name: 日志器名称（通常是模块名）
            level: 日志级别，可选值：DEBUG, INFO, WARNING, ERROR, CRITICAL
        """
        self.logger = logging.getLogger(name)
        
        # 设置日志级别
        if level is None:
            level = os.getenv('LOG_LEVEL', 'INFO').upper()
        
        level_map = {
            'DEBUG': logging.DEBUG,
            'INFO': logging.INFO,
            'WARNING': logging.WARNING,
            'ERROR': logging.ERROR,
            'CRITICAL': logging.CRITICAL
        }
        
        log_level = level_map.get(level, logging.INFO)
        self.logger.setLevel(log_level)
        
        # 避免重复添加handler
        if not self.logger.handlers:
            # 创建控制台handler
            console_handler = logging.StreamHandler(sys.stdout)
            console_handler.setLevel(log_level)
            
            # 创建格式器
            formatter = logging.Formatter(
                '%(asctime)s | %(name)s | %(levelname)s | %(message)s',
                datefmt='%H:%M:%S'
            )
            console_handler.setFormatter(formatter)
            
            self.logger.addHandler(console_handler)
        
        # 确保日志器不会传播到父级
        self.logger.propagate = False
    
    def debug(self, message: str):
        """DEBUG级别日志 - 详细的调试信息"""
        self.logger.debug(message)
    
    def info(self, message: str):
        """INFO级别日志 - 一般信息"""
        self.logger.info(message)
    
    def warning(self, message: str):
        """WARNING级别日志 - 警告信息"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """ERROR级别日志 - 错误信息"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """CRITICAL级别日志 - 严重错误"""
        self.logger.critical(message)
    
    # 便捷方法，用于兼容原有的print风格
    def print_debug(self, message: str):
        """DEBUG级别的print风格日志"""
        self.debug(f"🔍 {message}")
    
    def print_info(self, message: str):
        """INFO级别的print风格日志"""
        self.info(f"ℹ️ {message}")
    
    def print_success(self, message: str):
        """INFO级别的成功日志"""
        self.info(f"✅ {message}")
    
    def print_warning(self, message: str):
        """WARNING级别的警告日志"""
        self.warning(f"⚠️ {message}")
    
    def print_error(self, message: str):
        """ERROR级别的错误日志"""
        self.error(f"❌ {message}")
    
    def print_critical(self, message: str):
        """CRITICAL级别的严重错误日志"""
        self.critical(f"🚨 {message}")


# 全局日志器实例
def get_logger(name: str) -> WarehouseLogger:
    """
    获取日志器实例
    
    Args:
        name: 日志器名称
        
    Returns:
        WarehouseLogger实例
    """
    return WarehouseLogger(name)


# 便捷函数
def debug_log(module_name: str, message: str):
    """快速DEBUG日志"""
    logger = get_logger(module_name)
    logger.print_debug(message)


def info_log(module_name: str, message: str):
    """快速INFO日志"""
    logger = get_logger(module_name)
    logger.print_info(message)


def success_log(module_name: str, message: str):
    """快速成功日志"""
    logger = get_logger(module_name)
    logger.print_success(message)


def warning_log(module_name: str, message: str):
    """快速警告日志"""
    logger = get_logger(module_name)
    logger.print_warning(message)


def error_log(module_name: str, message: str):
    """快速错误日志"""
    logger = get_logger(module_name)
    logger.print_error(message)


def critical_log(module_name: str, message: str):
    """快速严重错误日志"""
    logger = get_logger(module_name)
    logger.print_critical(message)
