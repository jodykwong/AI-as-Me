"""Vibe-Kanban Manager - Markdown 文件管理."""
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import uuid
from .models import Task, TaskStatus, TaskPriority, TaskClarification


class VibeKanbanManager:
    def __init__(self, kanban_dir: Path = None):
        self.kanban_dir = kanban_dir or Path("kanban")
        self._ensure_dirs()
    
    def _ensure_dirs(self):
        for status in TaskStatus:
            (self.kanban_dir / status.value).mkdir(parents=True, exist_ok=True)
    
    def _generate_id(self) -> str:
        """生成唯一任务 ID（使用 UUID 避免竞态条件）."""
        now = datetime.now()
        return f"task-{now.strftime('%Y%m%d')}-{uuid.uuid4().hex[:6]}"
    
    def _get_file_path(self, task_id: str, status: TaskStatus) -> Path:
        return self.kanban_dir / status.value / f"{task_id}.md"
    
    def _find_task_file(self, task_id: str) -> Optional[Path]:
        for status in TaskStatus:
            file_path = self._get_file_path(task_id, status)
            if file_path.exists():
                return file_path
        return None
    
    def create_task(self, description: str, priority: str = "P2") -> Task:
        """创建新任务到 inbox."""
        if not description or not description.strip():
            raise ValueError("Task description cannot be empty")
        
        try:
            priority_enum = TaskPriority(priority)
        except ValueError:
            priority_enum = TaskPriority.P2
        
        task_id = self._generate_id()
        title = description[:50] + ("..." if len(description) > 50 else "")
        
        task = Task(
            id=task_id,
            title=title,
            description=description.strip(),
            status=TaskStatus.INBOX,
            priority=priority_enum,
            clarified=False
        )
        
        file_path = self._get_file_path(task_id, TaskStatus.INBOX)
        file_path.write_text(task.to_markdown(), encoding='utf-8')
        
        return task
    
    def get_task(self, task_id: str) -> Task:
        file_path = self._find_task_file(task_id)
        if not file_path:
            raise FileNotFoundError(f"Task {task_id} not found")
        
        content = file_path.read_text(encoding='utf-8')
        return Task.from_markdown(content)
    
    def list_tasks(self, status: Optional[str] = None) -> List[Task]:
        tasks = []
        
        if status:
            status_dir = self.kanban_dir / status
            if status_dir.exists():
                for file_path in status_dir.glob("*.md"):
                    try:
                        content = file_path.read_text(encoding='utf-8')
                        tasks.append(Task.from_markdown(content))
                    except Exception:
                        pass
        else:
            for status_enum in TaskStatus:
                tasks.extend(self.list_tasks(status_enum.value))
        
        return sorted(tasks, key=lambda t: t.created_at, reverse=True)
    
    def clarify_task(self, task_id: str, clarification: dict) -> Task:
        """澄清任务并自动移动到todo."""
        task = self.get_task(task_id)
        
        task.clarification = TaskClarification(**clarification)
        task.clarified = True
        task.updated_at = datetime.now()
        
        # 如果任务在inbox，澄清后自动移到todo
        if task.status == TaskStatus.INBOX:
            old_file = self._find_task_file(task_id)
            task.status = TaskStatus.TODO
            new_file = self._get_file_path(task_id, TaskStatus.TODO)
            
            new_file.write_text(task.to_markdown(), encoding='utf-8')
            old_file.unlink()
        else:
            # 如果不在inbox，只更新文件
            file_path = self._find_task_file(task_id)
            file_path.write_text(task.to_markdown(), encoding='utf-8')
        
        return task
    
    def move_task(self, task_id: str, to_status: str) -> Task:
        task = self.get_task(task_id)
        to_status_enum = TaskStatus(to_status)
        
        # 检查规则：inbox → todo 必须 clarified
        if task.status == TaskStatus.INBOX and to_status_enum == TaskStatus.TODO:
            if not task.clarified:
                raise ValueError("Task must be clarified before moving to todo")
        
        old_file = self._find_task_file(task_id)
        new_file = self._get_file_path(task_id, to_status_enum)
        
        task.status = to_status_enum
        task.updated_at = datetime.now()
        
        new_file.write_text(task.to_markdown(), encoding='utf-8')
        old_file.unlink()
        
        return task
    
    def delete_task(self, task_id: str) -> bool:
        file_path = self._find_task_file(task_id)
        if file_path:
            file_path.unlink()
            return True
        return False
    
    def get_board(self) -> dict:
        return {
            "inbox": self.list_tasks("inbox"),
            "todo": self.list_tasks("todo"),
            "doing": self.list_tasks("doing"),
            "done": self.list_tasks("done")
        }
