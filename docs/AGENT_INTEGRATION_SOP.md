# AI-as-Me Agent 集成 SOP

## 概述
AI-as-Me Agent 集成模块提供统一的 Agent 执行接口，支持 Claude Code 和 OpenCode 两种 AI 编程助手。

## 架构

### 模块结构
```
src/ai_as_me/agents/
├── __init__.py           # 模块导出
├── base.py               # BaseAgent 抽象类 + AgentResult
├── claude_agent.py       # Claude Code 实现
├── opencode_agent.py     # OpenCode 实现
├── registry.py           # Agent 注册表和工厂
└── executor.py           # 任务执行编排器
```

### 核心组件

#### 1. BaseAgent (抽象类)
```python
class BaseAgent(ABC):
    @abstractmethod
    def execute(task) -> AgentResult
    
    @abstractmethod
    def is_available() -> bool
    
    @abstractmethod
    def get_capabilities() -> List[str]
    
    @property
    @abstractmethod
    def name() -> str
```

#### 2. AgentResult (数据类)
```python
@dataclass
class AgentResult:
    success: bool
    output: str
    error: str
    agent_name: str
    duration: float
    metadata: Dict = None
```

#### 3. AgentRegistry (注册表)
- 自动注册所有 agents
- 提供 agent 查询和发现
- 过滤可用 agents

#### 4. AgentExecutor (编排器)
- 执行任务
- 自动选择可用 agent
- Fallback 机制

## 使用方法

### 1. CLI 命令

#### 列出所有 agents
```bash
ai-as-me agent list
```

输出示例：
```
🤖 已注册的 Agents:

  claude-code: ✅ 可用
    能力: code, analysis, refactor, debug
  opencode: ✅ 可用
    能力: code, analysis, refactor, debug

可用: 2/2
```

#### 执行任务
```bash
# 自动选择可用 agent
ai-as-me agent execute <task_id>

# 指定 agent
ai-as-me agent execute <task_id> --agent opencode

# 指定 agent 和模型
ai-as-me agent execute <task_id> --agent "opencode:deepseek-chat"

# 不触发进化
ai-as-me agent execute <task_id> --no-evolution
```

### 2. 任务澄清时配置工具

在 Dashboard 的任务澄清界面，可以选择：

**Claude Code 选项：**
- `claude-code:claude-3-5-sonnet-20241022` - Sonnet 3.5
- `claude-code:claude-3-7-sonnet-20250219` - Sonnet 3.7

**OpenCode 选项：**
- `opencode:deepseek-chat` - DeepSeek
- `opencode:gpt-4o` - GPT-4o

**其他：**
- `manual` - 手动执行

配置后，执行任务时会自动使用指定的 agent 和模型。

### 3. Python API

#### 基本使用
```python
from ai_as_me.agents import AgentExecutor
from ai_as_me.kanban.models import Task

# 创建执行器
executor = AgentExecutor()

# 执行任务（自动选择 agent）
result = executor.execute_with_fallback(task)

# 指定 agent 执行
result = executor.execute_task(task, 'opencode')

# 指定 agent 和模型
result = executor.execute_task(task, 'opencode:deepseek-chat')

# 检查结果
if result.success:
    print(f"成功: {result.output}")
    print(f"模型: {result.metadata.get('model')}")
else:
    print(f"失败: {result.error}")
```

#### 任务配置工具
```python
from ai_as_me.kanban.models import Task, TaskClarification

task = Task(
    id='task-001',
    title='示例任务',
    description='任务描述',
    clarification=TaskClarification(
        goal='任务目标',
        tool='opencode:deepseek-chat'  # 指定工具和模型
    )
)

# 执行时会自动使用配置的工具
executor = AgentExecutor()
result = executor.execute_task(task)  # 自动使用 opencode:deepseek-chat
```

#### Kanban 集成
```python
from ai_as_me.kanban.vibe_manager import VibeManager

vibe = VibeManager()

# 执行任务（自动触发进化）
result = vibe.execute_task('task-001')

print(f"Agent: {result['result'].agent_name}")
print(f"进化: {result['evolution']}")
```

### 3. Dashboard API

#### 执行任务
```bash
POST /api/kanban/tasks/{task_id}/execute
```

请求参数：
- `agent_name` (可选): 指定 agent

响应示例：
```json
{
  "success": true,
  "agent": "opencode",
  "duration": 30.5,
  "output": "任务执行结果...",
  "error": "",
  "evolution": {
    "patterns": 2,
    "rules": 1
  }
}
```

## 集成点

### 1. Kanban 系统
- `VibeManager.execute_task()` - 执行任务并保存结果
- 结果保存在 `kanban/doing/{task_id}-result.md`
- 自动更新任务执行状态

### 2. 进化引擎
- 任务执行成功后自动触发进化
- 收集经验、识别模式、生成规则
- 可通过 `--no-evolution` 禁用

### 3. Soul 注入
- 通过 `AgentCLI` 自动注入 Soul
- 提示词包含个人档案和规则
- 确保 AI 行为符合个性化设定

## 扩展新 Agent

### 1. 创建 Agent 类
```python
from .base import BaseAgent, AgentResult

class MyAgent(BaseAgent):
    @property
    def name(self) -> str:
        return "my-agent"
    
    def execute(self, task) -> AgentResult:
        # 实现执行逻辑
        pass
    
    def is_available(self) -> bool:
        # 检查是否可用
        pass
    
    def get_capabilities(self) -> List[str]:
        return ['capability1', 'capability2']
```

### 2. 注册 Agent
```python
# 在 registry.py 中添加
from .my_agent import MyAgent

class AgentRegistry:
    def _register_default_agents(self):
        self.register(ClaudeAgent())
        self.register(OpenCodeAgent())
        self.register(MyAgent())  # 添加新 agent
```

## 故障排查

### Agent 不可用
1. 检查 CLI 工具是否安装：
   ```bash
   npx -y @anthropic-ai/claude-code --version
   npx -y opencode-ai --version
   ```

2. 检查认证状态：
   ```bash
   ai-as-me agent list
   ```

3. 查看日志：
   ```bash
   tail -f logs/agent_calls.log
   ```

### 执行超时
- 默认超时：300 秒（5 分钟）
- 修改超时：在 `AgentCLI.call()` 中调整 `timeout` 参数

### Soul 注入失败
- 检查 `soul/` 目录是否存在
- 确保有 `soul/profile.md` 文件
- 查看 `SoulInjector` 日志

## 性能优化

### 1. Agent 可用性缓存
当前每次调用都检查 agent 可用性（5 秒超时）。可优化为：
- 启动时检查一次
- 定期刷新（如每小时）
- 失败时重新检查

### 2. 并行执行
当前 fallback 机制是串行的。可优化为：
- 并行调用多个 agents
- 返回最快成功的结果

### 3. 结果缓存
对相同任务的重复执行可以缓存结果。

## 测试

### 运行测试
```bash
python test_agent_integration.py
```

### 测试覆盖
- ✅ Agent 注册表
- ✅ Agent 执行器
- ✅ BaseAgent 抽象
- ✅ AgentResult 数据类
- ✅ OpenCode 集成
- ⚠️ Claude Code 集成（需要配置）

## 版本历史

### v1.0.0 (2026-01-17)
- ✅ 初始实现
- ✅ Claude Code 和 OpenCode 支持
- ✅ CLI 命令集成
- ✅ Kanban 集成
- ✅ 进化引擎集成
- ✅ Dashboard API

## 下一步计划

1. **Agent 能力匹配** - 根据任务类型自动选择最合适的 agent
2. **并行执行** - 支持多 agent 并行执行
3. **结果对比** - 多个 agent 执行同一任务，对比结果
4. **Agent 评分** - 根据执行历史评估 agent 质量
5. **自定义 Agent** - 支持用户自定义 agent 实现
