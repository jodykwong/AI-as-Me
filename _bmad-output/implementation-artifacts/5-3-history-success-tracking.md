# Story 5.3: 历史成功率追踪

**Epic:** Epic 5 - 多工具智能选择
**Status:** ready-for-dev
**Created:** 2026-01-14T08:06:00+08:00

---

## User Story

As a 技术型独立AI创业者,
I want 系统记录每个工具执行任务的成功率,
So that 系统可以基于历史数据优化工具选择。

---

## Acceptance Criteria

- [ ] **AC1:** 任务完成后记录执行历史到数据库
- [ ] **AC2:** 记录包含: task_id, tool_name, task_type, success, execution_time
- [ ] **AC3:** 可查询特定工具+任务类型的成功率
- [ ] **AC4:** 成功率计算公式: 成功次数 / 总次数

---

## Dev Checklist

### 1. 创建数据库表

**File:** `src/ai_as_me/kanban/database.py`

```python
# 添加到现有 schema
CREATE_TOOL_HISTORY_TABLE = """
CREATE TABLE IF NOT EXISTS tool_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    task_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    execution_time REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);

CREATE INDEX IF NOT EXISTS idx_tool_history_tool 
ON tool_history(tool_name);

CREATE INDEX IF NOT EXISTS idx_tool_history_type 
ON tool_history(task_type);
"""
```

### 2. 实现 HistoryTracker 类

**File:** `src/ai_as_me/orchestrator/skill_matcher.py`

```python
from datetime import datetime
import sqlite3

class HistoryTracker:
    def __init__(self, db_path: str):
        self.db_path = db_path
    
    def record(self, task_id: str, tool_name: str, 
               task_type: TaskType, success: bool, 
               execution_time: float = None) -> None:
        """记录工具执行历史"""
        with sqlite3.connect(self.db_path) as conn:
            conn.execute("""
                INSERT INTO tool_history 
                (task_id, tool_name, task_type, success, execution_time)
                VALUES (?, ?, ?, ?, ?)
            """, (task_id, tool_name, task_type.value, success, execution_time))
    
    def get_success_rate(self, tool_name: str, 
                         task_type: TaskType) -> float:
        """获取工具在特定任务类型的成功率"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.execute("""
                SELECT 
                    SUM(CASE WHEN success THEN 1 ELSE 0 END) as successes,
                    COUNT(*) as total
                FROM tool_history
                WHERE tool_name = ? AND task_type = ?
            """, (tool_name, task_type.value))
            
            row = cursor.fetchone()
            if not row or row[1] == 0:
                return 0.5  # 默认 50% (无历史数据)
            
            return row[0] / row[1]
```

### 3. 集成到任务完成流程

**File:** `src/ai_as_me/orchestrator/scheduler.py` (修改)

```python
# 在任务完成后调用
def complete_task(self, task_id: str, success: bool, execution_time: float):
    # ... 现有逻辑 ...
    
    # 记录历史
    task = self.get_task(task_id)
    self.history_tracker.record(
        task_id=task_id,
        tool_name=task.tool_used,
        task_type=task.task_type,
        success=success,
        execution_time=execution_time
    )
```

### 4. 添加单元测试

**File:** `tests/unit/test_skill_matcher.py`

```python
def test_history_tracker():
    tracker = HistoryTracker(":memory:")
    
    # 创建表
    with sqlite3.connect(":memory:") as conn:
        conn.executescript(CREATE_TOOL_HISTORY_TABLE)
    
    # 记录历史
    tracker.record("task-1", "claude_code", TaskType.CODE_GENERATION, True, 10.5)
    tracker.record("task-2", "claude_code", TaskType.CODE_GENERATION, True, 12.0)
    tracker.record("task-3", "claude_code", TaskType.CODE_GENERATION, False, 8.0)
    
    # 查询成功率
    rate = tracker.get_success_rate("claude_code", TaskType.CODE_GENERATION)
    assert rate == 2/3  # 2 成功 / 3 总数
```

---

## Files to Create/Modify

| 文件 | 操作 |
|------|------|
| `src/ai_as_me/kanban/database.py` | 修改 (添加表) |
| `src/ai_as_me/orchestrator/skill_matcher.py` | 修改 (添加类) |
| `src/ai_as_me/orchestrator/scheduler.py` | 修改 (集成) |
| `tests/unit/test_skill_matcher.py` | 修改 (添加测试) |

---

## Dependencies

- Story 5.1 (TaskType)
- v2.0 数据库结构

---

## Definition of Done

- [ ] tool_history 表已创建
- [ ] HistoryTracker 类已实现
- [ ] 任务完成时自动记录历史
- [ ] 成功率查询功能正常
- [ ] 单元测试通过
