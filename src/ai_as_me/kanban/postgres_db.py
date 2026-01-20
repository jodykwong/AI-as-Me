"""
AI-as-Me Kanban System - PostgreSQL Database Layer
"""

import os
import psycopg2
import psycopg2.extras
import json
from typing import List, Dict
from contextlib import contextmanager
import threading


class PostgreSQLDatabase:
    """PostgreSQL数据库连接"""

    def __init__(self, database_url: str = None):
        self.database_url = database_url or os.getenv(
            "DATABASE_URL",
            "postgresql://ai_user:ai_password_2026@localhost:5432/ai_as_me",
        )
        self._lock = threading.Lock()

    @contextmanager
    def get_connection(self):
        """获取数据库连接"""
        conn = psycopg2.connect(self.database_url)
        try:
            yield conn
        finally:
            conn.close()

    def get_all_tasks(self) -> List[Dict]:
        """获取所有任务"""
        with self.get_connection() as conn:
            cur = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
            cur.execute(
                """
                SELECT id, description as title, description, status, tool, priority,
                       created_at, updated_at, current_phase, progress, 
                       execution_status, has_result, steps, logs
                FROM tasks ORDER BY created_at DESC
            """
            )
            tasks = cur.fetchall()

            # 转换为字典并处理JSON字段
            result = []
            for task in tasks:
                task_dict = dict(task)
                # 处理JSON字段
                task_dict["steps"] = (
                    json.loads(task_dict["steps"]) if task_dict["steps"] else []
                )
                task_dict["logs"] = (
                    json.loads(task_dict["logs"]) if task_dict["logs"] else []
                )
                # 添加默认字段
                task_dict["clarified"] = True
                task_dict["clarification"] = {
                    "goal": "",
                    "acceptance_criteria": [],
                    "tool": task_dict["tool"],
                    "time_estimate": None,
                    "context": None,
                }
                result.append(task_dict)

            return result

    def update_task_phase(self, task_id: str, phase: str, progress: int = None):
        """更新任务执行阶段和进度"""
        with self.get_connection() as conn:
            cur = conn.cursor()
            if progress is not None:
                cur.execute(
                    "UPDATE tasks SET current_phase = %s, progress = %s WHERE id = %s",
                    (phase, progress, task_id),
                )
            else:
                cur.execute(
                    "UPDATE tasks SET current_phase = %s WHERE id = %s",
                    (phase, task_id),
                )
            conn.commit()


# 全局数据库实例
_db_instance = None


def get_database():
    """获取数据库实例"""
    global _db_instance
    if _db_instance is None:
        _db_instance = PostgreSQLDatabase()
    return _db_instance
