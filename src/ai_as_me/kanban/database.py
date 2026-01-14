"""
AI-as-Me Kanban System - Inspired by Vibe-Kanban
SQLite-based task management with real-time updates
"""
import sqlite3
import uuid
import json
from pathlib import Path
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum
from dataclasses import dataclass, asdict
from contextlib import contextmanager
import threading


# Story 9.1: 数据库连接池 (M1 修复: 正确追踪连接数)
class ConnectionPool:
    """简单的 SQLite 连接池"""
    
    def __init__(self, db_path: str, max_connections: int = 5):
        self.db_path = db_path
        self.max_connections = max_connections
        self._pool: List[sqlite3.Connection] = []
        self._active_count = 0
        self._lock = threading.Lock()
    
    @contextmanager
    def get_connection(self):
        """获取连接（上下文管理器）"""
        conn = None
        with self._lock:
            if self._pool:
                conn = self._pool.pop()
            elif self._active_count < self.max_connections:
                conn = sqlite3.connect(self.db_path, check_same_thread=False)
                conn.row_factory = sqlite3.Row
                self._active_count += 1
        
        if conn is None:
            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
        
        try:
            yield conn
        finally:
            with self._lock:
                if len(self._pool) < self.max_connections:
                    self._pool.append(conn)
                else:
                    conn.close()
                    self._active_count = max(0, self._active_count - 1)


class TaskStatus(Enum):
    INBOX = "inbox"
    TODO = "todo"
    DOING = "doing"
    DONE = "done"
    IN_PROGRESS = "in_progress"
    IN_REVIEW = "in_review"
    CANCELLED = "cancelled"


class Database:
    """简化的数据库接口 - Epic 6 + Story 9.1 连接池"""
    
    def __init__(self, db_path: str):
        self.db_path = db_path
        self._pool = ConnectionPool(db_path)  # Story 9.1: 使用连接池
        self._init_db()
    
    def _init_db(self):
        """初始化数据库"""
        Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
        
        with self._pool.get_connection() as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    description TEXT NOT NULL,
                    status TEXT DEFAULT 'inbox',
                    tool TEXT,
                    priority TEXT DEFAULT 'P2',
                    created_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            conn.commit()
    
    def create_task(self, task_id: str, description: str, tool: str = None, priority: str = "P2"):
        """创建任务"""
        with self._pool.get_connection() as conn:
            conn.execute(
                "INSERT INTO tasks (id, description, tool, priority) VALUES (?, ?, ?, ?)",
                (task_id, description, tool, priority)
            )
            conn.commit()
    
    def get_all_tasks(self, order_by_priority: bool = True) -> List[Dict]:
        """获取所有任务（Story 14.1: 支持优先级排序）"""
        with self._pool.get_connection() as conn:
            if order_by_priority:
                cursor = conn.execute(
                    "SELECT * FROM tasks ORDER BY priority ASC, created_at DESC"
                )
            else:
                cursor = conn.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            return [dict(row) for row in cursor.fetchall()]
    
    def get_task(self, task_id: str) -> Optional[Dict]:
        """获取单个任务"""
        with self._pool.get_connection() as conn:
            cursor = conn.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()
            return dict(row) if row else None
    
    def update_task_status(self, task_id: str, status: str):
        """更新任务状态"""
        with self._pool.get_connection() as conn:
            conn.execute(
                "UPDATE tasks SET status = ? WHERE id = ?",
                (status, task_id)
            )
            conn.commit()
    
    def get_task_history(self, task_id: str) -> List[Dict]:
        """获取任务执行历史（Story 14.2）"""
        with self._pool.get_connection() as conn:
            cursor = conn.execute(
                "SELECT * FROM tool_history WHERE task_id = ? ORDER BY created_at DESC",
                (task_id,)
            )
            return [dict(row) for row in cursor.fetchall()]
    
    def get_tool_stats(self, tool_name: str) -> Dict:
        """获取工具统计信息（Story 14.2）"""
        with self._pool.get_connection() as conn:
            cursor = conn.execute("""
                SELECT 
                    COUNT(*) as total,
                    SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                    AVG(execution_time) as avg_time
                FROM tool_history
                WHERE tool_name = ?
            """, (tool_name,))
            row = cursor.fetchone()
            if row:
                return {
                    "total": row[0],
                    "successes": row[1],
                    "success_rate": row[1] / row[0] if row[0] > 0 else 0,
                    "avg_execution_time": row[2]
                }
            return {"total": 0, "successes": 0, "success_rate": 0, "avg_execution_time": 0}


class ExecutionStatus(Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    KILLED = "killed"


@dataclass
class Task:
    id: str
    title: str
    description: Optional[str]
    status: TaskStatus
    needs_approval: bool
    approved: bool
    created_at: str
    updated_at: str
    
    def to_dict(self) -> Dict:
        d = asdict(self)
        d['status'] = self.status.value
        return d


@dataclass
class Execution:
    id: str
    task_id: str
    status: ExecutionStatus
    executor: str
    prompt: Optional[str]
    result: Optional[str]
    iterations: int
    started_at: str
    completed_at: Optional[str]
    
    def to_dict(self) -> Dict:
        d = asdict(self)
        d['status'] = self.status.value
        return d


class KanbanDB:
    """SQLite-based Kanban database."""
    
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._init_db()
    
    def _init_db(self):
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        conn.executescript('''
            CREATE TABLE IF NOT EXISTS tasks (
                id TEXT PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'todo',
                needs_approval INTEGER DEFAULT 0,
                approved INTEGER DEFAULT 0,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE TABLE IF NOT EXISTS executions (
                id TEXT PRIMARY KEY,
                task_id TEXT NOT NULL,
                status TEXT DEFAULT 'pending',
                executor TEXT DEFAULT 'deepseek',
                prompt TEXT,
                result TEXT,
                iterations INTEGER DEFAULT 0,
                started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                completed_at TEXT,
                FOREIGN KEY (task_id) REFERENCES tasks(id)
            );
            
            CREATE TABLE IF NOT EXISTS execution_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                execution_id TEXT NOT NULL,
                level TEXT DEFAULT 'info',
                module TEXT,
                event TEXT,
                data TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (execution_id) REFERENCES executions(id)
            );
            
            CREATE TABLE IF NOT EXISTS rules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                content TEXT NOT NULL,
                source TEXT,
                created_at TEXT DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status);
            CREATE INDEX IF NOT EXISTS idx_executions_task ON executions(task_id);
            CREATE INDEX IF NOT EXISTS idx_executions_status ON executions(status);
        ''')
        conn.commit()
        conn.close()
    
    def _conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn
    
    # Task operations
    def create_task(self, title: str, description: str = None, 
                    needs_approval: bool = False) -> Task:
        task_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        conn = self._conn()
        conn.execute('''
            INSERT INTO tasks (id, title, description, needs_approval, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', (task_id, title, description, int(needs_approval), now, now))
        conn.commit()
        conn.close()
        
        return Task(
            id=task_id, title=title, description=description,
            status=TaskStatus.TODO, needs_approval=needs_approval,
            approved=False, created_at=now, updated_at=now
        )
    
    def get_task(self, task_id: str) -> Optional[Task]:
        conn = self._conn()
        row = conn.execute('SELECT * FROM tasks WHERE id = ?', (task_id,)).fetchone()
        conn.close()
        
        if row:
            return Task(
                id=row['id'], title=row['title'], description=row['description'],
                status=TaskStatus(row['status']), needs_approval=bool(row['needs_approval']),
                approved=bool(row['approved']), created_at=row['created_at'],
                updated_at=row['updated_at']
            )
        return None
    
    def list_tasks(self, status: TaskStatus = None) -> List[Task]:
        conn = self._conn()
        if status:
            rows = conn.execute(
                'SELECT * FROM tasks WHERE status = ? ORDER BY created_at DESC',
                (status.value,)
            ).fetchall()
        else:
            rows = conn.execute(
                'SELECT * FROM tasks ORDER BY created_at DESC'
            ).fetchall()
        conn.close()
        
        return [Task(
            id=r['id'], title=r['title'], description=r['description'],
            status=TaskStatus(r['status']), needs_approval=bool(r['needs_approval']),
            approved=bool(r['approved']), created_at=r['created_at'],
            updated_at=r['updated_at']
        ) for r in rows]
    
    def update_task_status(self, task_id: str, status: TaskStatus):
        conn = self._conn()
        conn.execute('''
            UPDATE tasks SET status = ?, updated_at = ? WHERE id = ?
        ''', (status.value, datetime.now().isoformat(), task_id))
        conn.commit()
        conn.close()
    
    def approve_task(self, task_id: str):
        conn = self._conn()
        conn.execute('''
            UPDATE tasks SET approved = 1, updated_at = ? WHERE id = ?
        ''', (datetime.now().isoformat(), task_id))
        conn.commit()
        conn.close()
    
    def delete_task(self, task_id: str):
        conn = self._conn()
        conn.execute('DELETE FROM executions WHERE task_id = ?', (task_id,))
        conn.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        conn.commit()
        conn.close()
    
    # Execution operations
    def create_execution(self, task_id: str, executor: str = "deepseek",
                        prompt: str = None) -> Execution:
        exec_id = str(uuid.uuid4())
        now = datetime.now().isoformat()
        
        conn = self._conn()
        conn.execute('''
            INSERT INTO executions (id, task_id, executor, prompt, started_at)
            VALUES (?, ?, ?, ?, ?)
        ''', (exec_id, task_id, executor, prompt, now))
        conn.commit()
        conn.close()
        
        return Execution(
            id=exec_id, task_id=task_id, status=ExecutionStatus.PENDING,
            executor=executor, prompt=prompt, result=None, iterations=0,
            started_at=now, completed_at=None
        )
    
    def update_execution(self, exec_id: str, status: ExecutionStatus = None,
                        result: str = None, iterations: int = None):
        conn = self._conn()
        updates = ["updated_at = ?"]
        params = [datetime.now().isoformat()]
        
        if status:
            updates.append("status = ?")
            params.append(status.value)
            if status in (ExecutionStatus.COMPLETED, ExecutionStatus.FAILED, ExecutionStatus.KILLED):
                updates.append("completed_at = ?")
                params.append(datetime.now().isoformat())
        
        if result is not None:
            updates.append("result = ?")
            params.append(result)
        
        if iterations is not None:
            updates.append("iterations = ?")
            params.append(iterations)
        
        params.append(exec_id)
        conn.execute(f'UPDATE executions SET {", ".join(updates)} WHERE id = ?', params)
        conn.commit()
        conn.close()
    
    def get_latest_execution(self, task_id: str) -> Optional[Execution]:
        conn = self._conn()
        row = conn.execute('''
            SELECT * FROM executions WHERE task_id = ? ORDER BY started_at DESC LIMIT 1
        ''', (task_id,)).fetchone()
        conn.close()
        
        if row:
            return Execution(
                id=row['id'], task_id=row['task_id'],
                status=ExecutionStatus(row['status']), executor=row['executor'],
                prompt=row['prompt'], result=row['result'],
                iterations=row['iterations'], started_at=row['started_at'],
                completed_at=row['completed_at']
            )
        return None
    
    def get_running_executions(self) -> List[Execution]:
        conn = self._conn()
        rows = conn.execute('''
            SELECT * FROM executions WHERE status = 'running'
        ''').fetchall()
        conn.close()
        
        return [Execution(
            id=r['id'], task_id=r['task_id'],
            status=ExecutionStatus(r['status']), executor=r['executor'],
            prompt=r['prompt'], result=r['result'],
            iterations=r['iterations'], started_at=r['started_at'],
            completed_at=r['completed_at']
        ) for r in rows]
    
    # Log operations
    def add_log(self, execution_id: str, level: str, module: str, 
                event: str, data: Dict = None):
        conn = self._conn()
        conn.execute('''
            INSERT INTO execution_logs (execution_id, level, module, event, data)
            VALUES (?, ?, ?, ?, ?)
        ''', (execution_id, level, module, event, json.dumps(data) if data else None))
        conn.commit()
        conn.close()
    
    def get_logs(self, execution_id: str, limit: int = 100) -> List[Dict]:
        conn = self._conn()
        rows = conn.execute('''
            SELECT * FROM execution_logs WHERE execution_id = ?
            ORDER BY created_at DESC LIMIT ?
        ''', (execution_id, limit)).fetchall()
        conn.close()
        
        return [{
            'level': r['level'], 'module': r['module'], 'event': r['event'],
            'data': json.loads(r['data']) if r['data'] else None,
            'created_at': r['created_at']
        } for r in rows]
    
    # Rule operations
    def add_rule(self, category: str, content: str, source: str = None):
        conn = self._conn()
        conn.execute('''
            INSERT INTO rules (category, content, source) VALUES (?, ?, ?)
        ''', (category, content, source))
        conn.commit()
        conn.close()
    
    def get_rules(self) -> List[Dict]:
        conn = self._conn()
        rows = conn.execute('SELECT * FROM rules ORDER BY created_at DESC').fetchall()
        conn.close()
        
        return [{'category': r['category'], 'content': r['content'], 
                 'source': r['source'], 'created_at': r['created_at']} for r in rows]
    
    # Stats
    def get_stats(self) -> Dict:
        conn = self._conn()
        stats = {}
        for status in TaskStatus:
            count = conn.execute(
                'SELECT COUNT(*) FROM tasks WHERE status = ?', (status.value,)
            ).fetchone()[0]
            stats[status.value] = count
        
        stats['running'] = conn.execute(
            "SELECT COUNT(*) FROM executions WHERE status = 'running'"
        ).fetchone()[0]
        
        stats['rules'] = conn.execute('SELECT COUNT(*) FROM rules').fetchone()[0]
        conn.close()
        
        return stats


# Migrate from file-based kanban
def migrate_from_files(kanban_dir: Path, db: KanbanDB):
    """Migrate existing file-based tasks to SQLite."""
    for col in ['inbox', 'todo', 'doing', 'done']:
        col_dir = kanban_dir / col
        if not col_dir.exists():
            continue
        
        status_map = {
            'inbox': TaskStatus.TODO,
            'todo': TaskStatus.TODO,
            'doing': TaskStatus.IN_PROGRESS,
            'done': TaskStatus.DONE
        }
        
        for f in col_dir.glob('*.md'):
            content = f.read_text()
            title = f.stem
            needs_approval = '[需要审批]' in content or '[NEEDS_APPROVAL]' in content
            approved = (col_dir / f'{f.stem}.approved').exists()
            
            task = db.create_task(title, content, needs_approval)
            if approved:
                db.approve_task(task.id)
            db.update_task_status(task.id, status_map[col])
            
            print(f"  Migrated: {f.name} → {status_map[col].value}")
