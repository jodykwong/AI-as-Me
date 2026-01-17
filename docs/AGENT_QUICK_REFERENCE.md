# AI-as-Me Agent 集成快速参考

## 安装 Agents

### OpenCode
```bash
npx -y opencode-ai
```

### Claude Code
```bash
npx -y @anthropic-ai/claude-code
```

## CLI 命令

### 列出 Agents
```bash
ai-as-me agent list
```

### 执行任务
```bash
# 自动选择
ai-as-me agent execute task-001

# 指定 agent
ai-as-me agent execute task-001 --agent opencode

# 不触发进化
ai-as-me agent execute task-001 --no-evolution
```

## Python API

### 基本使用
```python
from ai_as_me.agents import AgentExecutor

executor = AgentExecutor()
result = executor.execute_with_fallback(task)

if result.success:
    print(result.output)
```

### Kanban 集成
```python
from ai_as_me.kanban.vibe_manager import VibeManager

vibe = VibeManager()
result = vibe.execute_task('task-001')
```

## REST API

### 执行任务
```bash
POST /api/kanban/tasks/{task_id}/execute
```

## 目录结构
```
src/ai_as_me/agents/
├── base.py               # BaseAgent + AgentResult
├── claude_agent.py       # Claude Code
├── opencode_agent.py     # OpenCode
├── registry.py           # 注册表
└── executor.py           # 编排器
```

## 扩展新 Agent

1. 创建 agent 类继承 `BaseAgent`
2. 实现 `execute()`, `is_available()`, `get_capabilities()`
3. 在 `registry.py` 中注册

详见：[docs/AGENT_INTEGRATION_SOP.md](AGENT_INTEGRATION_SOP.md)
