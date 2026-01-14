# Story 5.2: 工具能力注册

**Epic:** Epic 5 - 多工具智能选择
**Status:** ready-for-dev
**Created:** 2026-01-14T08:06:00+08:00

---

## User Story

As a 技术型独立AI创业者,
I want 系统维护各工具的能力矩阵配置,
So that 系统知道每个工具擅长什么类型的任务。

---

## Acceptance Criteria

- [ ] **AC1:** 系统启动时加载 `config/agents.yaml`
- [ ] **AC2:** 读取 4 种工具配置: claude_code, opencode, gemini_cli, qwen_code
- [ ] **AC3:** 每个工具包含 5 种任务类型的能力评分 (0.0-1.0)
- [ ] **AC4:** 支持查询工具对特定任务类型的能力评分

---

## Dev Checklist

### 1. 创建工具能力数据模型

**File:** `src/ai_as_me/orchestrator/skill_matcher.py`

```python
from dataclasses import dataclass

@dataclass
class ToolCapability:
    tool_name: str
    capabilities: dict[TaskType, float]  # 0.0-1.0
```

### 2. 创建配置文件

**File:** `config/agents.yaml`

```yaml
agents:
  claude_code:
    command: ["npx", "-y", "@anthropic-ai/claude-code@2.0.76"]
    capabilities:
      code_generation: 0.9
      code_review: 0.9
      documentation: 0.7
      architecture: 0.9
      debug: 0.7
  
  opencode:
    command: ["npx", "-y", "opencode-ai@1.1.3"]
    capabilities:
      code_generation: 0.7
      code_review: 0.7
      documentation: 0.5
      architecture: 0.5
      debug: 0.9
  
  gemini_cli:
    command: ["npx", "-y", "@google/gemini-cli"]
    capabilities:
      code_generation: 0.7
      code_review: 0.7
      documentation: 0.9
      architecture: 0.7
      debug: 0.5
  
  qwen_code:
    command: ["npx", "-y", "qwen-code"]
    capabilities:
      code_generation: 0.7
      code_review: 0.5
      documentation: 0.7
      architecture: 0.5
      debug: 0.7
```

### 3. 实现 ToolRegistry 类

**File:** `src/ai_as_me/orchestrator/skill_matcher.py`

```python
import yaml
from pathlib import Path

class ToolRegistry:
    def __init__(self, config_path: Path):
        with open(config_path) as f:
            self.config = yaml.safe_load(f)
        self.tools = self._load_tools()
    
    def _load_tools(self) -> dict[str, ToolCapability]:
        tools = {}
        for name, data in self.config.get('agents', {}).items():
            caps = {
                TaskType[k.upper()]: v 
                for k, v in data.get('capabilities', {}).items()
            }
            tools[name] = ToolCapability(name, caps)
        return tools
    
    def get_capability(self, tool_name: str, task_type: TaskType) -> float:
        tool = self.tools.get(tool_name)
        if not tool:
            return 0.0
        return tool.capabilities.get(task_type, 0.0)
    
    def get_available(self) -> list[str]:
        return list(self.tools.keys())
```

### 4. 添加单元测试

**File:** `tests/unit/test_skill_matcher.py`

```python
def test_tool_registry():
    registry = ToolRegistry(Path("config/agents.yaml"))
    
    # 测试工具加载
    assert "claude_code" in registry.get_available()
    assert len(registry.get_available()) == 4
    
    # 测试能力查询
    cap = registry.get_capability("claude_code", TaskType.CODE_GENERATION)
    assert cap == 0.9
```

### 5. 验证步骤

```bash
# 创建配置目录
mkdir -p config

# 运行测试
pytest tests/unit/test_skill_matcher.py::test_tool_registry -v
```

---

## Files to Create/Modify

| 文件 | 操作 |
|------|------|
| `config/agents.yaml` | 创建 |
| `src/ai_as_me/orchestrator/skill_matcher.py` | 修改 (添加类) |
| `tests/unit/test_skill_matcher.py` | 修改 (添加测试) |

---

## Dependencies

- PyYAML (已有依赖)
- Story 5.1 (TaskType 枚举)

---

## Definition of Done

- [ ] agents.yaml 配置文件已创建
- [ ] ToolCapability 数据类已定义
- [ ] ToolRegistry 类已实现
- [ ] 可查询 4 种工具的能力评分
- [ ] 单元测试通过
