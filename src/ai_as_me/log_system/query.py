"""Log Query - 日志查询."""
import json
from pathlib import Path
from typing import List, Dict, Optional
from datetime import datetime


class LogQuery:
    """日志查询器."""
    
    def __init__(self, log_file: Path = None):
        self.log_file = log_file or Path('logs/agent.log')
    
    def query(
        self,
        level: Optional[str] = None,
        logger: Optional[str] = None,
        task_id: Optional[str] = None,
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        keyword: Optional[str] = None,
        limit: int = 100
    ) -> List[Dict]:
        """查询日志.
        
        Args:
            level: 日志级别筛选
            logger: Logger 名称筛选
            task_id: 任务 ID 筛选
            start_time: 开始时间
            end_time: 结束时间
            keyword: 关键词搜索
            limit: 返回数量限制
        
        Returns:
            日志记录列表
        """
        if not self.log_file.exists():
            return []
        
        results = []
        
        for line in self.log_file.read_text(encoding='utf-8').splitlines():
            if not line.strip():
                continue
            
            try:
                log_entry = json.loads(line)
                
                # 级别筛选
                if level and log_entry.get('level') != level:
                    continue
                
                # Logger 筛选
                if logger and not log_entry.get('logger', '').startswith(logger):
                    continue
                
                # Task ID 筛选
                if task_id and log_entry.get('task_id') != task_id:
                    continue
                
                # 时间范围筛选
                if start_time or end_time:
                    log_time = datetime.fromisoformat(log_entry.get('timestamp', ''))
                    if start_time and log_time < start_time:
                        continue
                    if end_time and log_time > end_time:
                        continue
                
                # 关键词搜索
                if keyword:
                    message = log_entry.get('message', '')
                    if keyword.lower() not in message.lower():
                        continue
                
                results.append(log_entry)
                
                if len(results) >= limit:
                    break
            
            except json.JSONDecodeError:
                continue
        
        return results
    
    def tail(self, n: int = 50) -> List[Dict]:
        """获取最后 N 条日志."""
        if not self.log_file.exists():
            return []
        
        lines = self.log_file.read_text(encoding='utf-8').splitlines()
        results = []
        
        for line in reversed(lines):
            if not line.strip():
                continue
            try:
                results.append(json.loads(line))
                if len(results) >= n:
                    break
            except json.JSONDecodeError:
                continue
        
        return list(reversed(results))
    
    def export(
        self,
        format: str = "json",
        start_time: Optional[datetime] = None,
        end_time: Optional[datetime] = None,
        level: Optional[str] = None
    ) -> bytes:
        """导出日志.
        
        Args:
            format: 导出格式 (json/csv)
            start_time: 开始时间
            end_time: 结束时间
            level: 日志级别
        
        Returns:
            导出的字节数据
        """
        logs = self.query(
            level=level,
            start_time=start_time,
            end_time=end_time,
            limit=10000
        )
        
        if format == "json":
            return json.dumps(logs, indent=2, ensure_ascii=False).encode('utf-8')
        
        elif format == "csv":
            import csv
            import io
            
            output = io.StringIO()
            if logs:
                writer = csv.DictWriter(output, fieldnames=logs[0].keys())
                writer.writeheader()
                writer.writerows(logs)
            
            return output.getvalue().encode('utf-8')
        
        else:
            raise ValueError(f"Unsupported format: {format}")
