"""Yangu模块 - 养蛊自进化 - 执行历史管理"""

import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict


class ExecutionHistory:
    """执行历史记录管理"""

    def __init__(self, logs_dir: Path = None):
        self.logs_dir = logs_dir or Path.cwd() / "logs"
        self.logs_dir.mkdir(exist_ok=True)
        self.history_file = self.logs_dir / "execution_history.json"

    def add_execution(
        self,
        task_id: str,
        tool: str,
        prompt: str,
        output: str,
        success: bool,
        rating: int = None,
        feedback: str = None,
    ) -> Dict:
        """添加执行记录"""
        record = {
            "task_id": task_id,
            "tool": tool,
            "prompt": prompt[:200],  # 截断过长的提示词
            "output": output[:500] if output else "",
            "success": success,
            "rating": rating,
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
        }

        # 加载现有历史
        history = self._load_history()
        history.append(record)

        # 保存
        self._save_history(history)
        return record

    def _load_history(self) -> List[Dict]:
        """加载执行历史"""
        if not self.history_file.exists():
            return []
        try:
            return json.loads(self.history_file.read_text())
        except:
            return []

    def _save_history(self, history: List[Dict]):
        """保存执行历史"""
        self.history_file.write_text(json.dumps(history, indent=2, ensure_ascii=False))

    def get_history(self, limit: int = None) -> List[Dict]:
        """获取执行历史"""
        history = self._load_history()
        if limit:
            return history[-limit:]
        return history

    def get_rated_tasks(
        self, min_rating: int = None, max_rating: int = None
    ) -> List[Dict]:
        """获取有评分的任务"""
        history = self._load_history()
        rated = [h for h in history if h.get("rating")]

        if min_rating:
            rated = [h for h in rated if h["rating"] >= min_rating]
        if max_rating:
            rated = [h for h in rated if h["rating"] <= max_rating]

        return rated
