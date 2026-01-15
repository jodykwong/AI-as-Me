"""JSON Formatter - JSON 格式日志."""
import json
import logging
from datetime import datetime
from typing import Dict, Any


class JSONFormatter(logging.Formatter):
    """JSON 格式化器."""
    
    def format(self, record: logging.LogRecord) -> str:
        """格式化日志记录为 JSON."""
        log_data: Dict[str, Any] = {
            "timestamp": datetime.fromtimestamp(record.created).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }
        
        # 添加上下文信息
        if hasattr(record, 'task_id'):
            log_data["task_id"] = record.task_id
        
        if hasattr(record, 'trace_id'):
            log_data["trace_id"] = record.trace_id
        
        # 添加额外字段
        if hasattr(record, 'context'):
            log_data["context"] = record.context
        
        # 添加异常信息
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)
        
        return json.dumps(log_data, ensure_ascii=False)
