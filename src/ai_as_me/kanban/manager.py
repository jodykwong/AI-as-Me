"""Kanban task manager."""

from pathlib import Path
from typing import Dict, List, Optional
import yaml


class Task:
    """Represent a task."""

    def __init__(self, file_path: Path):
        self.file_path = file_path
        self.title = ""
        self.context = ""
        self.expected_output = ""
        self.priority = "normal"
        self.created_at = None
        self.status = self._get_status_from_path()

        self._parse()

    def _get_status_from_path(self) -> str:
        """Get task status from directory."""
        parent = self.file_path.parent.name
        return parent if parent in ["inbox", "todo", "doing", "done"] else "unknown"

    def _parse(self):
        """Parse task file content."""
        try:
            content = self.file_path.read_text()
        except Exception:
            self.title = self.file_path.stem
            self.context = ""
            return

        # Try to parse YAML frontmatter
        if content.startswith("---"):
            parts = content.split("---", 2)
            if len(parts) >= 3:
                try:
                    metadata = yaml.safe_load(parts[1])
                    if metadata and isinstance(metadata, dict):
                        self.title = metadata.get("title", self.file_path.stem)
                        self.context = metadata.get("context", "")
                        self.expected_output = metadata.get("expected_output", "")
                        self.priority = metadata.get("priority", "normal")
                        self.created_at = metadata.get("created_at")

                    # Body is after second ---
                    body = parts[2].strip()
                    if not self.context and body:
                        self.context = body
                except Exception:
                    # Fallback: treat entire content as context
                    self.title = self.file_path.stem
                    self.context = content
            else:
                self.title = self.file_path.stem
                self.context = content
        else:
            # No frontmatter, use filename as title and content as context
            self.title = self.file_path.stem
            self.context = content


class KanbanManager:
    """Manage task kanban board."""

    def __init__(self, kanban_dir: Path):
        self.kanban_dir = kanban_dir
        self.inbox = kanban_dir / "inbox"
        self.todo = kanban_dir / "todo"
        self.doing = kanban_dir / "doing"
        self.done = kanban_dir / "done"

    def get_task_counts(self) -> Dict[str, int]:
        """Get task counts for each status.

        Returns:
            Dict with counts for inbox, todo, doing, done
        """
        return {
            "inbox": len(list(self.inbox.glob("*.md"))) if self.inbox.exists() else 0,
            "todo": len(list(self.todo.glob("*.md"))) if self.todo.exists() else 0,
            "doing": len(list(self.doing.glob("*.md"))) if self.doing.exists() else 0,
            "done": len(list(self.done.glob("*.md"))) if self.done.exists() else 0,
        }

    def get_tasks(self, status: Optional[str] = None) -> List[Task]:
        """Get tasks by status.

        Args:
            status: Filter by status (inbox/todo/doing/done), or None for all

        Returns:
            List of Task objects
        """
        tasks = []

        if status:
            status_dir = self.kanban_dir / status
            if status_dir.exists():
                for file_path in sorted(status_dir.glob("*.md")):
                    tasks.append(Task(file_path))
        else:
            # Get all tasks
            for status_name in ["inbox", "todo", "doing", "done"]:
                tasks.extend(self.get_tasks(status_name))

        return tasks

    def move_task(self, task_file: str, target_status: str) -> bool:
        """Move task to target status.

        Args:
            task_file: Task filename (without path)
            target_status: Target status (inbox/todo/doing/done)

        Returns:
            True if successful, False otherwise
        """
        if target_status not in ["inbox", "todo", "doing", "done"]:
            return False

        # Find task in any directory
        source_path = None
        for status in ["inbox", "todo", "doing", "done"]:
            candidate = self.kanban_dir / status / task_file
            if candidate.exists():
                source_path = candidate
                break

        if not source_path:
            return False

        # Check target doesn't already exist
        target_path = self.kanban_dir / target_status / task_file
        if target_path.exists():
            return False

        # Move to target
        source_path.rename(target_path)
        return True
