"""Tests for Vibe-Kanban system."""
import pytest
from pathlib import Path
import shutil
from ai_as_me.kanban.models import Task, TaskStatus, TaskPriority, TaskClarification
from ai_as_me.kanban.vibe_manager import VibeKanbanManager


@pytest.fixture
def temp_kanban_dir(tmp_path):
    """临时 kanban 目录."""
    kanban_dir = tmp_path / "kanban"
    yield kanban_dir
    if kanban_dir.exists():
        shutil.rmtree(kanban_dir)


@pytest.fixture
def manager(temp_kanban_dir):
    """Kanban 管理器."""
    return VibeKanbanManager(temp_kanban_dir)


class TestTaskModel:
    """Task 模型测试."""
    
    def test_task_creation(self):
        """测试任务创建."""
        task = Task(
            id="task-001",
            title="测试任务",
            description="这是一个测试任务",
            status=TaskStatus.INBOX,
            priority=TaskPriority.P2
        )
        
        assert task.id == "task-001"
        assert task.status == TaskStatus.INBOX
        assert task.clarified is False
    
    def test_task_to_markdown(self):
        """测试 Markdown 序列化."""
        task = Task(
            id="task-001",
            title="测试任务",
            description="测试描述",
            status=TaskStatus.INBOX,
            priority=TaskPriority.P1
        )
        
        md = task.to_markdown()
        
        assert "id: task-001" in md
        assert "status: inbox" in md
        assert "priority: P1" in md
        assert "# 测试任务" in md
        assert "测试描述" in md
    
    def test_task_from_markdown(self):
        """测试 Markdown 反序列化."""
        md_content = """---
id: task-001
created: 2026-01-17T06:00:00
updated: 2026-01-17T06:00:00
status: inbox
priority: P2
clarified: false
---

# 测试任务

## 📝 描述
这是测试描述

## 🎯 目标
[待澄清]

## ✅ 验收标准
- [ ] 待定义

## 🔧 工具选择
[待配置]

## ⏱️ 时间估算
[待评估]

## 📎 上下文
[无]
"""
        
        task = Task.from_markdown(md_content)
        
        assert task.id == "task-001"
        assert task.title == "测试任务"
        assert task.description == "这是测试描述"
        assert task.status == TaskStatus.INBOX
        assert task.priority == TaskPriority.P2
        assert task.clarified is False


class TestVibeKanbanManager:
    """VibeKanbanManager 测试."""
    
    def test_create_task(self, manager, temp_kanban_dir):
        """测试创建任务."""
        task = manager.create_task("实现用户登录", "P1")
        
        assert task.id.startswith("task-")
        assert task.status == TaskStatus.INBOX
        assert task.priority == TaskPriority.P1
        
        # 验证文件创建
        file_path = temp_kanban_dir / "inbox" / f"{task.id}.md"
        assert file_path.exists()
    
    def test_get_task(self, manager):
        """测试获取任务."""
        task = manager.create_task("测试任务")
        retrieved = manager.get_task(task.id)
        
        assert retrieved.id == task.id
        assert retrieved.title == task.title
    
    def test_list_tasks(self, manager):
        """测试列出任务."""
        manager.create_task("任务1")
        manager.create_task("任务2")
        
        tasks = manager.list_tasks("inbox")
        assert len(tasks) == 2
    
    def test_clarify_task(self, manager):
        """测试澄清任务."""
        task = manager.create_task("测试任务")
        
        clarified = manager.clarify_task(task.id, {
            "goal": "实现功能",
            "acceptance_criteria": ["标准1", "标准2"],
            "tool": "Claude Code",
            "time_estimate": "2小时"
        })
        
        assert clarified.clarified is True
        assert clarified.clarification.goal == "实现功能"
        assert len(clarified.clarification.acceptance_criteria) == 2
    
    def test_move_task_success(self, manager):
        """测试移动任务（成功）."""
        task = manager.create_task("测试任务")
        
        # 先澄清
        manager.clarify_task(task.id, {
            "goal": "测试",
            "acceptance_criteria": ["标准1"]
        })
        
        # 移动到 todo
        moved = manager.move_task(task.id, "todo")
        
        assert moved.status == TaskStatus.TODO
    
    def test_move_task_without_clarify(self, manager):
        """测试未澄清任务无法移动."""
        task = manager.create_task("测试任务")
        
        with pytest.raises(ValueError, match="must be clarified"):
            manager.move_task(task.id, "todo")
    
    def test_delete_task(self, manager, temp_kanban_dir):
        """测试删除任务."""
        task = manager.create_task("测试任务")
        file_path = temp_kanban_dir / "inbox" / f"{task.id}.md"
        
        assert file_path.exists()
        
        success = manager.delete_task(task.id)
        
        assert success is True
        assert not file_path.exists()
    
    def test_get_board(self, manager):
        """测试获取看板."""
        manager.create_task("任务1")
        manager.create_task("任务2")
        
        board = manager.get_board()
        
        assert "inbox" in board
        assert "todo" in board
        assert "doing" in board
        assert "done" in board
        assert len(board["inbox"]) == 2


class TestTaskWorkflow:
    """任务工作流测试."""
    
    def test_complete_workflow(self, manager):
        """测试完整工作流."""
        # 1. 创建任务
        task = manager.create_task("实现功能", "P1")
        assert task.status == TaskStatus.INBOX
        
        # 2. 澄清任务（自动移到todo）
        clarified = manager.clarify_task(task.id, {
            "goal": "实现用户登录",
            "acceptance_criteria": ["用户可以登录", "返回 token"]
        })
        assert clarified.clarified is True
        assert clarified.status == TaskStatus.TODO  # 澄清后自动移到todo
        
        # 3. 开始执行
        doing_task = manager.move_task(clarified.id, "doing")
        assert doing_task.status == TaskStatus.DOING
        
        # 4. 完成
        done_task = manager.move_task(clarified.id, "done")
        assert done_task.status == TaskStatus.DONE
