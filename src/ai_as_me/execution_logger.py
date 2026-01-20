import json
import os
from datetime import datetime
from typing import List, Dict, Optional


class ExecutionLogger:
    def __init__(self, task_id: str):
        self.task_id = task_id
        self.log_dir = f"/home/sunrise/AI-as-Me/data/tasks/{task_id}"
        self.log_file = f"{self.log_dir}/execution_log.jsonl"
        os.makedirs(self.log_dir, exist_ok=True)

    def log(self, log_type: str, content: str):
        """记录执行日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "type": log_type,
            "content": content,
        }
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(log_entry, ensure_ascii=False) + "\n")

    def get_logs(
        self, since_timestamp: Optional[str] = None, limit: int = 100
    ) -> List[Dict]:
        """获取执行日志"""
        if not os.path.exists(self.log_file):
            return []

        logs = []
        with open(self.log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    log_entry = json.loads(line.strip())
                    if since_timestamp and log_entry["timestamp"] <= since_timestamp:
                        continue
                    logs.append(log_entry)

        return logs[-limit:] if limit else logs
