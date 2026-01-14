"""Kanban任务管理模块"""
import json
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional
import uuid


class TaskManager:
    """任务管理器"""
    
    def __init__(self, kanban_dir: Path = None):
        self.kanban_dir = kanban_dir or Path.cwd() / "kanban"
        self.tasks_file = self.kanban_dir / "tasks.json"
        self._ensure_kanban_dir()
    
    def _ensure_kanban_dir(self):
        """确保kanban目录存在"""
        self.kanban_dir.mkdir(exist_ok=True)
        if not self.tasks_file.exists():
            self.tasks_file.write_text("[]")
    
    def _load_tasks(self) -> List[Dict]:
        """加载任务列表"""
        try:
            return json.loads(self.tasks_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    
    def _save_tasks(self, tasks: List[Dict]):
        """保存任务列表"""
        self.tasks_file.write_text(json.dumps(tasks, indent=2, ensure_ascii=False))
    
    def add_task(self, description: str) -> Dict:
        """添加新任务"""
        tasks = self._load_tasks()
        task = {
            "id": str(uuid.uuid4())[:8],
            "description": description,
            "status": "todo",
            "created_at": datetime.now().isoformat()
        }
        tasks.append(task)
        self._save_tasks(tasks)
        return task
    
    def list_tasks(self, status: Optional[str] = None) -> List[Dict]:
        """列出任务"""
        tasks = self._load_tasks()
        if status:
            tasks = [t for t in tasks if t["status"] == status]
        return tasks
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """获取单个任务"""
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                return task
        return None
    
    def update_task_status(self, task_id: str, status: str) -> bool:
        """更新任务状态"""
        tasks = self._load_tasks()
        for task in tasks:
            if task["id"] == task_id:
                task["status"] = status
                task["updated_at"] = datetime.now().isoformat()
                self._save_tasks(tasks)
                return True
        return False
