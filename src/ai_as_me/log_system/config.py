"""Logging Configuration - 日志配置管理."""
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Optional
from .formatter import JSONFormatter


_configured = False


def setup_logging(
    log_dir: Optional[Path] = None,
    level: str = "INFO",
    max_bytes: int = 10 * 1024 * 1024,  # 10MB
    backup_count: int = 7
):
    """配置统一日志系统.
    
    Args:
        log_dir: 日志目录，默认 logs/
        level: 日志级别
        max_bytes: 单文件最大字节数
        backup_count: 保留备份数量
    """
    global _configured
    if _configured:
        return
    
    log_dir = log_dir or Path('logs')
    log_dir.mkdir(parents=True, exist_ok=True)
    
    # JSON 格式化器
    json_formatter = JSONFormatter()
    
    # 文本格式化器（控制台）
    text_formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # 文件 handler（JSON + 轮转）
    file_handler = RotatingFileHandler(
        log_dir / 'agent.log',
        maxBytes=max_bytes,
        backupCount=backup_count,
        encoding='utf-8'
    )
    file_handler.setFormatter(json_formatter)
    file_handler.setLevel(getattr(logging, level))
    
    # 控制台 handler（文本）
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(text_formatter)
    console_handler.setLevel(getattr(logging, level))
    
    # 配置根 logger
    root_logger = logging.getLogger('ai_as_me')
    root_logger.setLevel(getattr(logging, level))
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    _configured = True


def get_logger(name: str) -> logging.Logger:
    """获取 logger 实例."""
    return logging.getLogger(f'ai_as_me.{name}')
