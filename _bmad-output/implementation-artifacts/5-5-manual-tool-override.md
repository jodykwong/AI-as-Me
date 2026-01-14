# Story 5.5: 手动工具覆盖

**Epic:** Epic 5 - 多工具智能选择
**Status:** ready-for-dev
**Created:** 2026-01-14T08:06:00+08:00

---

## User Story

As a 技术型独立AI创业者,
I want 能够通过 `--tool` 参数手动指定工具,
So that 我可以在需要时覆盖系统的自动选择。

---

## Acceptance Criteria

- [ ] **AC1:** `ai-as-me task add "描述" --tool claude_code` 使用指定工具
- [ ] **AC2:** 指定工具不可用时提示错误
- [ ] **AC3:** 未指定工具时使用自动选择
- [ ] **AC4:** 工具名称验证

---

## Dev Checklist

### 1. 添加 CLI 参数

**File:** `src/ai_as_me/cli/commands/task.py`

```python
import click
from pathlib import Path

@click.group()
def task():
    """任务管理命令"""
    pass

@task.command()
@click.argument('description')
@click.option('--tool', type=str, help='指定使用的工具 (claude_code, opencode, gemini_cli, qwen_code)')
def add(description: str, tool: str = None):
    """创建新任务"""
    from ai_as_me.orchestrator.scheduler import TaskScheduler
    
    scheduler = TaskScheduler(
        db_path="data/tasks.db",
        config_path=Path("config/agents.yaml")
    )
    
    # 验证工具名称
    if tool:
        available = scheduler.skill_matcher.registry.get_available()
        if tool not in available:
            click.echo(f"错误: 工具 '{tool}' 不可用", err=True)
            click.echo(f"可用工具: {', '.join(available)}")
            return
    
    # 创建任务
    task_id = scheduler.create_task(description, tool=tool)
    
    if tool:
        click.echo(f"✓ 任务已创建 (ID: {task_id}, 工具: {tool})")
    else:
        selected = scheduler.get_task(task_id).tool_used
        click.echo(f"✓ 任务已创建 (ID: {task_id}, 自动选择: {selected})")
```

### 2. 更新 TaskScheduler

**File:** `src/ai_as_me/orchestrator/scheduler.py` (确认支持)

```python
def create_task(self, description: str, tool: str = None) -> str:
    """创建任务
    
    Args:
        description: 任务描述
        tool: 指定工具名称，None 则自动选择
    
    Returns:
        task_id: 任务 ID
    """
    # 自动选择或使用指定工具
    if tool is None:
        tool = self.skill_matcher.match(description)
    
    # 保存任务
    task_id = self._save_task(description, tool)
    return task_id
```

### 3. 添加集成测试

**File:** `tests/integration/test_cli_task.py`

```python
from click.testing import CliRunner
from ai_as_me.cli.commands.task import task

def test_task_add_with_tool():
    runner = CliRunner()
    
    # 指定工具
    result = runner.invoke(task, ['add', '写代码', '--tool', 'claude_code'])
    assert result.exit_code == 0
    assert 'claude_code' in result.output
    
    # 无效工具
    result = runner.invoke(task, ['add', '写代码', '--tool', 'invalid'])
    assert result.exit_code != 0
    assert '不可用' in result.output

def test_task_add_auto_select():
    runner = CliRunner()
    
    # 自动选择
    result = runner.invoke(task, ['add', '写一个排序算法'])
    assert result.exit_code == 0
    assert '自动选择' in result.output
```

### 4. 更新帮助文档

**File:** `README.md` (添加示例)

```markdown
## 使用示例

### 创建任务

```bash
# 自动选择工具
ai-as-me task add "写一个 Python 函数计算斐波那契数列"

# 手动指定工具
ai-as-me task add "审查代码安全性" --tool claude_code

# 查看可用工具
ai-as-me task add --help
```
```

---

## Files to Create/Modify

| 文件 | 操作 |
|------|------|
| `src/ai_as_me/cli/commands/task.py` | 修改 (添加 --tool 参数) |
| `src/ai_as_me/orchestrator/scheduler.py` | 确认 (tool 参数支持) |
| `tests/integration/test_cli_task.py` | 创建 |
| `README.md` | 修改 (添加示例) |

---

## Dependencies

- Story 5.4 (SkillMatcher)
- v2.0 CLI 框架

---

## Definition of Done

- [ ] --tool 参数已添加
- [ ] 工具名称验证正常
- [ ] 错误提示清晰
- [ ] 集成测试通过
- [ ] 文档已更新
