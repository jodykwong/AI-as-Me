---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8, 9]
inputDocuments:
  - "prd-v2.0-polished.md"
  - "product-brief-AI-as-Me-2026-01-13.md"
  - "ux-design-specification-v2.0.md"
  - "v2.0_iteration_plan.md"
documentCounts:
  prd: 1
  briefs: 1
  uxDesign: 1
  research: 0
  projectDocs: 1
  projectContext: 0
workflowType: 'architecture'
lastStep: 9
status: 'updated'
completedAt: '2026-01-13T06:00:16+08:00'
updatedAt: '2026-01-13T06:00:16+08:00'
project_name: 'AI-as-Me'
user_name: 'Jody'
date: '2026-01-13'
version: 'v2.0'
finalDocument: 'architecture-v2.0.md'
updateReason: 'Integrated UX Design Specification v2.0 requirements'
---

# Architecture Decision Document - AI-as-Me v2.0

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**基于 v2.0 PRD 的核心需求:**
- **编排模式**: "不造轮子，只做编排" - 调用外部 Agent CLI 工具
- **Soul 注入**: 个性化提示词注入到外部工具
- **养蛊循环**: 自进化学习机制
- **MVP 目标**: 4天实施，个人验证，>80% 采用率

**功能需求概览:**
- FR-01: Agent CLI 工具集成 (Claude Code, OpenCode)
- FR-02: Soul 注入机制 (profile.md, rules.md)
- FR-03: 任务生命周期管理 (CLI 命令)
- FR-04: 基础养蛊循环 (反思和规则积累)

**非功能需求约束:**
- 性能: Agent CLI 调用 <30秒，任务创建 <2秒
- 可靠性: >95% 可用性，故障恢复 <10秒
- 安全: 本地存储，API 密钥环境变量
- 兼容性: Python 3.9+, Node.js 16+ (npx 依赖)

### Technical Constraints & Dependencies

| 约束类型 | 具体约束 | 架构影响 |
|---------|---------|---------|
| 外部工具依赖 | npx + Node.js 环境 | 需要进程管理和错误处理 |
| 提示词限制 | 不同工具的 context window | Soul 注入需要模板化 |
| MVP 时间限制 | 4天实施 | 架构必须简化，避免过度设计 |
| 个人验证 | 单用户场景 | 暂不考虑多用户和并发 |

**Scale & Complexity:**
- Primary domain: Agent CLI 编排系统
- Complexity level: 中等 (编排逻辑，非底层实现)
- Estimated architectural components: 4-6 个核心模块
## Architectural Requirements Analysis

### Core System Purpose

**AI-as-Me v2.0** 是一个 Agent CLI 编排系统，核心理念是"不造轮子，只做编排"：
- **不实现** AI coding 能力
- **只负责** 调度和编排现有 Agent CLI 工具
- **通过 Soul 注入** 实现个性化
- **通过养蛊循环** 实现自进化学习

### Functional Requirements Analysis

**核心编排能力 (P0 - MVP):**

1. **FR-01: Agent CLI 工具集成**
   - 架构影响: 需要进程管理、错误处理、健康检查
   - 技术约束: 依赖 Node.js + npx 环境
   - 集成工具: Claude Code, OpenCode (MVP 阶段)

2. **FR-02: Soul 注入机制**
   - 架构影响: 需要模板引擎、文件系统管理
   - 数据流: soul/*.md → 提示词模板 → 外部工具
   - 个性化: profile.md, rules.md 动态注入

3. **FR-03: 任务生命周期管理**
   - 架构影响: 需要状态机、持久化存储
   - CLI 接口: task add/list/serve/start 命令
   - 状态流: todo → doing → done

4. **FR-04: 基础养蛊循环**
   - 架构影响: 需要反思引擎、规则提取器
   - 学习流: 执行结果 → 反思分析 → 规则更新 → Soul 进化

### Non-Functional Requirements Analysis

**性能约束:**
- Agent CLI 调用响应时间 <30秒 → 需要异步处理和超时机制
- 任务创建响应时间 <2秒 → 需要轻量级 CLI 设计
- Soul 注入时间 <5秒 → 需要高效的模板处理

**可靠性约束:**
- 系统可用性 >95% → 需要故障恢复和降级机制
- 外部工具失败恢复 <10秒 → 需要工具健康检查和备用策略

**安全约束:**
- 本地存储优先 → 架构必须支持离线运行
- API 密钥环境变量 → 需要安全的配置管理
- Soul 文件权限 600 → 需要文件系统权限控制

**兼容性约束:**
- Python 3.9+ + Node.js 16+ → 混合技术栈架构
- 跨平台支持 (Linux/macOS/Windows) → 需要平台抽象层

### Scale & Complexity Assessment

**MVP 阶段简化:**
- 单用户场景 → 无需考虑多租户架构
- 串行任务执行 → 无需复杂的并发管理
- 2个工具集成 → 简化工具管理复杂度
- 4天实施限制 → 架构必须简洁实用

**未来扩展考虑:**
- v2.1: 多工具支持、并行执行、Web 仪表板 (基于UX设计规范)
- v2.2: BMAD 集成、智能调度、高级 RAG

### Key Architectural Drivers

1. **编排优先**: 系统核心是调度外部工具，不是实现 AI 能力
2. **个性化注入**: Soul 机制是差异化核心，需要灵活的模板系统
3. **自进化学习**: 养蛊循环是长期价值，需要可扩展的学习架构
4. **MVP 约束**: 4天实施限制，架构必须最小可行
5. **本地优先**: 数据安全和离线能力，架构偏向本地处理
## Technical Foundation Analysis

### Existing Technical Preferences

基于项目上下文和现有代码库分析：

**当前技术栈 (v1.0):**
- **Python 3.9+**: 主要开发语言，已有 FastAPI + SQLite 基础
- **FastAPI**: Web 框架，用于 Web 仪表板
- **SQLite**: 轻量级数据库，任务和状态存储
- **Click**: CLI 框架，命令行接口实现
- **Rich**: CLI 美化库，支持UX设计规范的视觉语言
- **文件系统**: Soul 数据本地存储 (soul/*.md)

**新增技术需求 (v2.0):**
- **Node.js 16+**: npx 工具调用依赖
- **进程管理**: subprocess/asyncio 处理外部工具
- **模板引擎**: Jinja2 用于 Soul 注入
- **配置管理**: YAML/JSON 配置文件

### Starter Template Evaluation

#### Option 1: 扩展现有架构 (推荐)

**优势:**
- 利用现有 FastAPI + SQLite 基础
- 保持技术栈一致性
- 快速 MVP 实现 (符合4天限制)
- 已有 CLI 框架 (Click)

**架构模式:**
```
ai_as_me/
├── orchestrator/     # 新增：编排层
│   ├── agent_cli.py     # Agent CLI 调用
│   ├── scheduler.py     # 任务调度
│   └── soul_injector.py # Soul 注入
├── yangu/           # 新增：养蛊层
│   ├── reflector.py     # 反思引擎
│   └── rule_extractor.py # 规则提取
├── kanban/          # 现有：任务管理
├── soul/            # 现有：个人化数据
└── cli/             # 现有：命令行接口
```

#### Option 2: 微服务架构

**劣势:**
- 过度复杂，不符合 MVP 约束
- 4天实施时间不足
- 单用户场景无需微服务

**结论**: 不适合 MVP 阶段

#### Option 3: 纯 CLI 工具

**劣势:**
- 缺少 Web 仪表板扩展性
- 不利于养蛊循环可视化
- 限制未来功能扩展
- 无法支持UX设计规范的丰富交互模式

**结论**: 不符合长期规划

### Recommended Technical Stack

**核心技术栈:**
- **Python 3.9+**: 主要开发语言
- **FastAPI**: Web 框架 (现有)
- **SQLite**: 数据存储 (现有)
- **Click**: CLI 框架 (现有)
- **Rich**: CLI 美化和响应式布局 (新增)
- **Jinja2**: 模板引擎 (Soul 注入 + Web模板)
- **asyncio**: 异步处理 (Agent CLI 调用)
- **subprocess**: 进程管理 (npx 调用)

**外部依赖:**
- **Node.js 16+**: npx 工具调用环境
- **Agent CLI 工具**: Claude Code, OpenCode

**配置和数据:**
- **YAML**: 配置文件格式
- **Markdown**: Soul 数据格式 (现有)
- **JSON**: Agent 配置和状态

### Architecture Foundation Decision

**选择**: 扩展现有架构模式

**理由:**
1. **快速实现**: 利用现有基础，符合4天 MVP 限制
2. **技术一致性**: 保持 Python 主导的技术栈
3. **渐进演进**: 支持从 MVP 到完整版本的平滑升级
4. **风险最小**: 基于已验证的技术选择
## Core Architectural Decisions

### Decision 1: System Architecture Pattern

**问题**: AI-as-Me v2.0 应该采用什么整体架构模式？

**选项分析:**

**A. 分层架构 (Layered Architecture)**
- 调度层 (Orchestrator) → 执行层 (Agent CLI) → 反思层 (Yangu)
- 优势: 清晰分离关注点，易于理解和维护
- 劣势: 可能存在性能开销

**B. 管道架构 (Pipeline Architecture)**  
- 任务输入 → Soul注入 → Agent执行 → 结果反思 → 规则更新
- 优势: 数据流清晰，适合批处理
- 劣势: 不适合交互式场景

**C. 事件驱动架构 (Event-Driven)**
- 基于任务事件的异步处理
- 优势: 高并发，松耦合
- 劣势: 复杂度高，不适合MVP

**决策**: **分层架构**

**理由**:
- 符合"调度→执行→反思"的三层概念模型
- 清晰的职责分离，便于4天MVP实现
- 支持未来扩展到更复杂的编排模式

### Decision 2: Agent CLI 集成策略

**问题**: 如何设计外部 Agent CLI 工具的集成机制？

**选项分析:**

**A. 直接进程调用**
```python
subprocess.run(["npx", "-y", "@anthropic-ai/claude-code", "--prompt", prompt])
```
- 优势: 简单直接，快速实现
- 劣势: 错误处理复杂，难以监控

**B. 抽象工具接口**
```python
class AgentCLI:
    def execute(self, prompt: str) -> Result
    
class ClaudeCode(AgentCLI):
    def execute(self, prompt: str) -> Result
```
- 优势: 统一接口，易于扩展新工具
- 劣势: 增加抽象层复杂度

**C. 配置驱动调用**
```yaml
agents:
  claude:
    command: ["npx", "-y", "@anthropic-ai/claude-code"]
    args: ["--prompt", "{prompt}"]
```
- 优势: 灵活配置，无需代码修改
- 劣势: 配置复杂度

**决策**: **抽象工具接口 + 配置驱动**

**理由**:
- 统一接口便于 MVP 快速实现
- 配置驱动支持未来工具扩展
- 平衡了简单性和扩展性

### Decision 3: Soul 注入机制设计

**问题**: Soul 个性化数据如何注入到外部工具？

**选项分析:**

**A. 简单字符串拼接**
```python
prompt = f"{profile_content}\n{rules_content}\n{task_description}"
```
- 优势: 实现简单
- 劣势: 不灵活，难以优化

**B. 模板引擎 (Jinja2)**
```python
template = """
{{ profile }}
{{ rules }}
Task: {{ task }}
"""
```
- 优势: 灵活的模板系统，支持条件逻辑
- 劣势: 增加依赖

**C. 结构化注入**
```python
soul_context = {
    "profile": profile_data,
    "rules": rules_data,
    "task": task_data
}
```
- 优势: 结构化数据，便于处理
- 劣势: 需要序列化处理

**决策**: **模板引擎 (Jinja2)**

**理由**:
- 支持灵活的提示词模板
- 便于不同工具的格式适配
- 支持条件逻辑和数据转换

### Decision 4: 任务状态管理

**问题**: 任务状态如何存储和管理？

**选项分析:**

**A. 文件系统 (现有 kanban/ 目录)**
- 优势: 简单，可视化，现有实现
- 劣势: 并发访问问题

**B. SQLite 数据库**
- 优势: ACID 特性，查询能力
- 劣势: 增加复杂度

**C. 混合模式**
- SQLite 存储状态，文件系统存储内容
- 优势: 结合两者优势
- 劣势: 复杂度最高

**决策**: **SQLite 数据库**

**理由**:
- 支持复杂查询和状态管理
- ACID 特性保证数据一致性
- 为未来 Web 仪表板提供 API 支持
- 支持UX设计规范的跨平台数据一致性

### Decision 5: 养蛊循环实现策略

**问题**: 自进化学习机制如何实现？

**选项分析:**

**A. 简单规则累积**
- 成功/失败模式 → 文本规则 → rules.md
- 优势: 简单直观
- 劣势: 规则冲突处理复杂

**B. 向量化存储**
- 任务和结果向量化 → 相似度检索
- 优势: 智能匹配
- 劣势: 复杂度高，不适合MVP

**C. 结构化学习**
- 分类存储：成功模式、失败模式、偏好设置
- 优势: 结构化管理
- 劣势: 需要复杂的分类逻辑

**决策**: **简单规则累积 + 结构化存储**

**理由**:
- MVP 阶段使用简单规则累积
- 为未来向量化学习预留接口
- 平衡实现复杂度和功能完整性
## Implementation Patterns & Consistency Rules

### Pattern 1: Agent CLI 集成模式

**一致性要求**: 所有 Agent CLI 工具必须通过统一接口调用

**实现模式**:
```python
# 抽象基类 - 强制一致性
class AgentCLI(ABC):
    @abstractmethod
    def execute(self, prompt: str, config: Dict) -> AgentResult
    
    @abstractmethod
    def health_check(self) -> bool
    
    @abstractmethod
    def get_version(self) -> str

# 具体实现 - 统一错误处理
class ClaudeCode(AgentCLI):
    def execute(self, prompt: str, config: Dict) -> AgentResult:
        try:
            result = subprocess.run(
                ["npx", "-y", "@anthropic-ai/claude-code", "--prompt", prompt],
                capture_output=True, text=True, timeout=30
            )
            return AgentResult.from_subprocess(result)
        except subprocess.TimeoutExpired:
            return AgentResult.timeout_error()
        except Exception as e:
            return AgentResult.execution_error(str(e))
```

**一致性规则**:
- 所有工具调用必须有超时机制 (30秒)
- 统一的错误处理和结果格式
- 健康检查接口必须实现
- 配置参数通过 Dict 传递

### Pattern 2: Soul 注入模式

**一致性要求**: Soul 数据注入必须使用统一的模板系统

**实现模式**:
```python
# 模板管理器 - 统一模板处理
class SoulInjector:
    def __init__(self, template_dir: Path):
        self.env = Environment(loader=FileSystemLoader(template_dir))
    
    def inject(self, template_name: str, soul_data: Dict, task_data: Dict) -> str:
        template = self.env.get_template(f"{template_name}.j2")
        return template.render(
            profile=soul_data.get('profile', ''),
            rules=soul_data.get('rules', ''),
            task=task_data
        )

# 模板文件结构 - 标准化格式
templates/
├── claude_code.j2
├── opencode.j2
└── default.j2
```

**一致性规则**:
- 所有模板必须支持 profile, rules, task 变量
- 模板文件命名: `{agent_name}.j2`
- 默认模板 `default.j2` 作为后备
- Soul 数据加载必须处理文件不存在的情况

### Pattern 3: 任务状态管理模式

**一致性要求**: 任务状态变更必须通过统一的状态机

**实现模式**:
```python
# 状态枚举 - 明确状态定义
class TaskStatus(Enum):
    TODO = "todo"
    DOING = "doing" 
    DONE = "done"
    FAILED = "failed"
    BLOCKED = "blocked"

# 状态管理器 - 统一状态转换
class TaskManager:
    def __init__(self, db: Database):
        self.db = db
    
    def transition_state(self, task_id: str, new_status: TaskStatus) -> bool:
        # 验证状态转换合法性
        current = self.get_task_status(task_id)
        if not self._is_valid_transition(current, new_status):
            raise InvalidStateTransition(current, new_status)
        
        # 更新状态并记录历史
        self.db.update_task_status(task_id, new_status, timestamp=datetime.now())
        return True
```

**一致性规则**:
- 状态转换必须验证合法性
- 所有状态变更必须记录时间戳
- 任务ID使用UUID格式
- 状态历史必须保留用于养蛊学习

### Pattern 4: 养蛊循环模式

**一致性要求**: 学习和反思必须遵循统一的数据格式

**实现模式**:
```python
# 反思数据结构 - 标准化格式
@dataclass
class ReflectionData:
    task_id: str
    agent_used: str
    prompt_template: str
    execution_result: str
    user_feedback: Optional[str]
    success_score: float  # 0.0 - 1.0
    timestamp: datetime

# 规则提取器 - 统一学习逻辑
class RuleExtractor:
    def extract_rules(self, reflections: List[ReflectionData]) -> List[Rule]:
        # 成功模式识别
        successful = [r for r in reflections if r.success_score > 0.8]
        # 失败模式识别  
        failed = [r for r in reflections if r.success_score < 0.3]
        
        return self._generate_rules(successful, failed)
```

**一致性规则**:
- 反思数据必须包含完整的执行上下文
- 成功评分使用 0.0-1.0 标准化分数
- 规则提取必须区分成功和失败模式
- 新规则必须验证与现有规则的冲突

### Pattern 5: 配置管理模式

**一致性要求**: 所有配置必须使用统一的配置系统

**实现模式**:
```python
# 配置结构 - 标准化配置格式
@dataclass
class AgentConfig:
    name: str
    command: List[str]
    timeout: int = 30
    retry_count: int = 3
    template: str = "default"

# 配置管理器 - 统一配置加载
class ConfigManager:
    def __init__(self, config_path: Path):
        self.config = self._load_config(config_path)
    
    def get_agent_config(self, agent_name: str) -> AgentConfig:
        agent_data = self.config.get('agents', {}).get(agent_name)
        if not agent_data:
            raise AgentNotConfigured(agent_name)
        return AgentConfig(**agent_data)
```

**一致性规则**:
- 配置文件使用 YAML 格式
- 所有超时和重试参数必须可配置
- 环境变量优先级高于配置文件
- 配置变更必须支持热重载

### Pattern 6: 错误处理和日志模式

**一致性要求**: 统一的错误处理和日志格式

**实现模式**:
```python
# 统一错误类型
class AIAsMeError(Exception):
    def __init__(self, message: str, error_code: str, context: Dict = None):
        self.message = message
        self.error_code = error_code
        self.context = context or {}

# 统一日志格式
import structlog
logger = structlog.get_logger()

def log_task_execution(task_id: str, agent: str, result: str):
    logger.info(
        "task_executed",
        task_id=task_id,
        agent=agent,
        result_length=len(result),
        timestamp=datetime.now().isoformat()
    )
```

**一致性规则**:
- 所有异常必须继承自 AIAsMeError
- 日志必须使用结构化格式 (JSON)
- 错误代码使用统一的命名规范
- 敏感信息不得出现在日志中

### 跨模块一致性规则

**数据传递规则**:
- 所有模块间数据传递使用 Pydantic 模型
- 异步操作使用 asyncio 统一处理
- 数据库操作必须使用事务

**测试规则**:
- 每个 Agent CLI 集成必须有健康检查测试
- Soul 注入必须有模板渲染测试
- 状态转换必须有完整的状态机测试

**性能规则**:
- Agent CLI 调用必须支持并发限制
- 大文件处理必须使用流式处理
- 缓存策略必须统一实现
## Project Structure & Component Boundaries

### Complete Project Structure

```
ai-as-me/
├── src/ai_as_me/
│   ├── __init__.py
│   ├── main.py                    # 应用入口点
│   │
│   ├── orchestrator/              # 调度层 - FR-01, FR-02, FR-03
│   │   ├── __init__.py
│   │   ├── agent_cli.py          # Agent CLI 抽象接口
│   │   ├── scheduler.py          # 任务调度器
│   │   ├── soul_injector.py      # Soul 注入机制
│   │   ├── task_manager.py       # 任务状态管理
│   │   └── agents/               # 具体 Agent 实现
│   │       ├── __init__.py
│   │       ├── claude_code.py    # Claude Code 集成
│   │       ├── opencode.py       # OpenCode 集成
│   │       └── base.py           # Agent 基类
│   │
│   ├── yangu/                    # 反思层 - FR-04
│   │   ├── __init__.py
│   │   ├── reflector.py          # 反思引擎
│   │   ├── rule_extractor.py     # 规则提取器
│   │   ├── learning_engine.py    # 学习引擎
│   │   └── models.py             # 反思数据模型
│   │
│   ├── kanban/                   # 任务管理层 (现有扩展)
│   │   ├── __init__.py
│   │   ├── database.py           # SQLite 数据库管理
│   │   ├── models.py             # 任务数据模型
│   │   ├── dashboard.py          # Web 仪表板 (v2.1)
│   │   ├── api.py                # REST API (v2.1)
│   │   └── components.py         # 跨平台组件接口 (新增)
│   │
│   ├── soul/                     # Soul 数据管理
│   │   ├── __init__.py
│   │   ├── loader.py             # Soul 数据加载器
│   │   ├── validator.py          # Soul 数据验证
│   │   └── models.py             # Soul 数据模型
│   │
│   ├── cli/                      # 命令行接口
│   │   ├── __init__.py
│   │   ├── main.py               # CLI 主入口
│   │   ├── components/           # CLI UX组件 (新增)
│   │   │   ├── __init__.py
│   │   │   ├── task_card.py      # 任务卡片组件
│   │   │   ├── learning_widget.py # 学习进展组件
│   │   │   ├── progress_bar.py   # 进度条组件
│   │   │   └── responsive.py     # 响应式布局管理
│   │   ├── commands/             # CLI 命令实现
│   │   │   ├── __init__.py
│   │   │   ├── task.py           # task add/list 命令
│   │   │   ├── serve.py          # serve 命令
│   │   │   ├── setup.py          # setup 命令
│   │   │   └── agent.py          # agent start 命令
│   │   ├── accessibility.py      # 可访问性支持 (新增)
│   │   └── utils.py              # CLI 工具函数
│   │
│   ├── config/                   # 配置管理
│   │   ├── __init__.py
│   │   ├── manager.py            # 配置管理器
│   │   ├── models.py             # 配置数据模型
│   │   └── defaults.py           # 默认配置
│   │
│   ├── utils/                    # 通用工具
│   │   ├── __init__.py
│   │   ├── logging.py            # 日志配置
│   │   ├── errors.py             # 异常定义
│   │   ├── validators.py         # 数据验证
│   │   └── helpers.py            # 辅助函数
│   │
│   └── rag/                      # Agentic RAG (v2.1)
│       ├── __init__.py
│       ├── vectorstore.py        # 向量存储
│       ├── retriever.py          # 检索器
│       └── embeddings.py         # 嵌入处理
│
├── soul/                         # Soul 数据目录
│   ├── profile.md                # 个人档案
│   ├── rules.md                  # 工作规则
│   ├── mission.md                # 任务目标
│   └── templates/                # 提示词模板
│       ├── claude_code.j2
│       ├── opencode.j2
│       └── default.j2
│
├── config/                       # 配置文件
│   ├── agents.yaml               # Agent 配置
│   ├── app.yaml                  # 应用配置
│   └── logging.yaml              # 日志配置
│
├── data/                         # 数据目录
│   ├── tasks.db                  # SQLite 数据库
│   ├── logs/                     # 日志文件
│   └── cache/                    # 缓存文件
│
├── tests/                        # 测试代码
│   ├── unit/                     # 单元测试
│   ├── integration/              # 集成测试
│   └── fixtures/                 # 测试数据
│
├── docs/                         # 文档
│   ├── architecture.md           # 架构文档
│   ├── api.md                    # API 文档
│   └── deployment.md             # 部署文档
│
├── scripts/                      # 脚本文件
│   ├── setup.sh                  # 环境设置
│   ├── install-service.sh        # 服务安装
│   └── health-check.py           # 健康检查
│
├── pyproject.toml                # Python 项目配置
├── requirements.txt              # 依赖列表
├── README.md                     # 项目说明
├── .env.example                  # 环境变量示例
└── .gitignore                    # Git 忽略文件
```

### Component Boundaries & Responsibilities

#### 1. Orchestrator Layer (调度层)

**边界**: 负责任务分发、Agent 选择、Soul 注入
**职责**:
- `agent_cli.py`: Agent CLI 抽象接口和工厂模式
- `scheduler.py`: 任务队列管理和调度逻辑
- `soul_injector.py`: Soul 数据注入和模板渲染
- `task_manager.py`: 任务状态管理和生命周期
- `agents/`: 具体 Agent CLI 实现

**依赖关系**:
- 依赖: config, soul, utils
- 被依赖: cli, yangu

#### 2. Yangu Layer (反思层)

**边界**: 负责执行结果分析、规则提取、学习优化
**职责**:
- `reflector.py`: 任务执行结果反思分析
- `rule_extractor.py`: 成功/失败模式提取
- `learning_engine.py`: 规则更新和冲突解决
- `models.py`: 反思数据结构定义

**依赖关系**:
- 依赖: soul, utils, config
- 被依赖: orchestrator

#### 3. Kanban Layer (任务管理层)

**边界**: 负责任务持久化、状态跟踪、Web 界面
**职责**:
- `database.py`: SQLite 数据库操作
- `models.py`: 任务数据模型定义
- `dashboard.py`: Web 仪表板 (v2.1)
- `api.py`: REST API 接口 (v2.1)

**依赖关系**:
- 依赖: config, utils
- 被依赖: orchestrator, cli

#### 4. Soul Layer (个性化层)

**边界**: 负责个人化数据管理和验证
**职责**:
- `loader.py`: Soul 文件加载和解析
- `validator.py`: Soul 数据格式验证
- `models.py`: Soul 数据结构定义

**依赖关系**:
- 依赖: utils
- 被依赖: orchestrator, yangu

#### 5. CLI Layer (命令行层)

**边界**: 负责用户交互和命令处理
**职责**:
- `main.py`: CLI 主入口和路由
- `commands/`: 具体命令实现
- `components/`: UX组件库 (新增)
- `accessibility.py`: 可访问性支持 (新增)
- `utils.py`: CLI 辅助功能

**依赖关系**:
- 依赖: orchestrator, kanban, config
- 被依赖: 无 (顶层接口)

### Requirements to Components Mapping

| 功能需求 | 主要组件 | 支持组件 |
|---------|---------|---------|
| FR-01: Agent CLI 集成 | orchestrator/agent_cli.py | orchestrator/agents/ |
| FR-02: Soul 注入机制 | orchestrator/soul_injector.py | soul/ |
| FR-03: 任务生命周期 | orchestrator/task_manager.py | kanban/database.py |
| FR-04: 养蛊循环 | yangu/ | soul/loader.py |
| CLI 命令 | cli/commands/ | cli/components/, orchestrator/ |
| UX组件系统 | cli/components/ | kanban/components.py |
| 可访问性支持 | cli/accessibility.py | cli/components/ |
| 配置管理 | config/ | utils/ |
| 错误处理 | utils/errors.py | utils/logging.py |

### Data Flow Architecture

```
CLI Commands → Orchestrator → Agent CLI → External Tools
     ↓              ↓              ↓
Task Manager → Soul Injector → Template Engine
     ↓              ↓              ↓
  Database ← Yangu Reflector ← Execution Results
     ↓              ↓              ↓
Web Dashboard ← Rule Extractor ← Learning Engine
```

### Module Dependencies Graph

```
cli/ → orchestrator/ → agents/
  ↓         ↓           ↓
kanban/ → soul/ → utils/
  ↓         ↓       ↓
yangu/ → config/ → logging
  ↓
rag/ (v2.1)
```

### MVP Implementation Priority

**Phase 1 (Day 1-2)**: 核心编排
- orchestrator/agent_cli.py
- orchestrator/agents/claude_code.py
- orchestrator/agents/opencode.py
- orchestrator/soul_injector.py

**Phase 2 (Day 2-3)**: 任务管理 + UX组件
- orchestrator/task_manager.py
- kanban/database.py
- cli/commands/task.py
- cli/components/task_card.py (新增)
- cli/components/responsive.py (新增)

**Phase 3 (Day 3-4)**: 养蛊循环 + 学习可视化
- yangu/reflector.py
- yangu/rule_extractor.py
- soul/loader.py
- cli/components/learning_widget.py (新增)
- cli/accessibility.py (新增)

**Phase 4 (Day 4)**: 集成测试
- CLI 命令集成
- 端到端测试
- 部署脚本
## Architecture Validation & Readiness Assessment

### Functional Requirements Coverage Validation

**✅ FR-01: Agent CLI 工具集成**
- 架构组件: `orchestrator/agent_cli.py`, `orchestrator/agents/`
- 实现模式: 抽象基类 + 具体实现
- 一致性规则: 统一接口、超时机制、错误处理
- 验证状态: **完全覆盖**

**✅ FR-02: Soul 注入机制**
- 架构组件: `orchestrator/soul_injector.py`, `soul/`
- 实现模式: Jinja2 模板引擎
- 一致性规则: 标准化模板格式、统一变量命名
- 验证状态: **完全覆盖**

**✅ FR-03: 任务生命周期管理**
- 架构组件: `orchestrator/task_manager.py`, `kanban/database.py`
- 实现模式: 状态机 + SQLite 持久化
- 一致性规则: 统一状态转换、时间戳记录
- 验证状态: **完全覆盖**

**✅ FR-04: 基础养蛊循环**
- 架构组件: `yangu/reflector.py`, `yangu/rule_extractor.py`
- 实现模式: 反思数据结构 + 规则提取
- 一致性规则: 标准化反思格式、成功评分机制
- 验证状态: **完全覆盖**

### Non-Functional Requirements Validation

**✅ 性能需求**
- Agent CLI 调用 <30秒: 超时机制在 `agent_cli.py` 实现
- 任务创建 <2秒: 轻量级 CLI 设计
- Soul 注入 <5秒: 高效模板处理
- 验证状态: **架构支持**

**✅ 可靠性需求**
- 系统可用性 >95%: 错误处理和降级机制
- 故障恢复 <10秒: 健康检查和备用策略
- 数据持久性: SQLite 事务保证
- 验证状态: **架构支持**

**✅ 安全需求**
- 本地存储: 架构设计本地优先
- API 密钥管理: 环境变量配置
- 权限控制: 文件系统权限设置
- 验证状态: **架构支持**

**✅ 兼容性需求**
- Python 3.9+ + Node.js 16+: 技术栈确认
- 跨平台支持: 平台抽象层设计
- 工具版本兼容: 配置驱动版本管理
- 验证状态: **架构支持**

### Architecture Coherence Analysis

**✅ 分层架构一致性**
- 调度层 → 执行层 → 反思层: 清晰的数据流
- 依赖关系单向: 避免循环依赖
- 职责分离明确: 每层职责边界清晰
- 验证状态: **架构连贯**

**✅ 模块边界清晰性**
- 接口定义明确: 抽象基类强制接口一致
- 数据传递标准: Pydantic 模型统一格式
- 错误处理统一: 继承体系和日志格式
- 验证状态: **边界清晰**

**✅ 扩展性设计**
- MVP → v2.1 → v2.2: 渐进演进路径清晰
- 新工具集成: 插件化 Agent 设计
- 功能模块扩展: 模块化架构支持
- 验证状态: **扩展友好**

### Implementation Readiness Assessment

**✅ 开发路径清晰**
- 4天 MVP 实施计划: 分阶段实现路径
- 组件依赖关系: 开发顺序明确
- 测试策略: 单元测试和集成测试覆盖
- 验证状态: **实施就绪**

**✅ AI 代理一致性**
- 实现模式定义: 6个核心模式覆盖关键场景
- 一致性规则: 防止代理实现冲突
- 代码规范: 统一的编码标准和接口
- 验证状态: **一致性保障**

**✅ 技术风险控制**
- 外部依赖管理: 健康检查和降级机制
- 混合技术栈: Python + Node.js 集成策略
- 配置管理: 统一配置系统和热重载
- 验证状态: **风险可控**

### Gap Analysis

**无关键缺口发现**
- 所有功能需求都有对应的架构组件
- 所有非功能需求都有架构支持
- 实现模式覆盖所有关键场景
- 项目结构支持完整开发流程

### Architecture Quality Metrics

**复杂度评估**: ⭐⭐⭐ (中等)
- 适合 MVP 4天实施限制
- 模块化设计降低单个组件复杂度
- 清晰的分层架构易于理解

**可维护性**: ⭐⭐⭐⭐⭐ (优秀)
- 职责分离明确
- 依赖关系清晰
- 统一的实现模式

**可扩展性**: ⭐⭐⭐⭐ (良好)
- 插件化 Agent 设计
- 模块化架构
- 渐进演进路径

**一致性保障**: ⭐⭐⭐⭐⭐ (优秀)
- 强制接口实现
- 统一数据格式
- 标准化错误处理

### Final Architecture Validation

**✅ 架构完整性**: 所有需求都有对应的架构决策
**✅ 实现可行性**: 4天 MVP 实施计划现实可行
**✅ 技术一致性**: 统一的技术栈和实现模式
**✅ 扩展兼容性**: 支持未来版本的功能扩展
**✅ 风险可控性**: 关键风险都有缓解策略

### Implementation Handoff Readiness

**架构文档状态**: ✅ 完整
**实现指导**: ✅ 详细的组件边界和接口定义
**开发路径**: ✅ 4天分阶段实施计划
**质量保障**: ✅ 一致性规则和测试策略
**风险管理**: ✅ 技术风险识别和缓解方案

**结论**: AI-as-Me v2.0 架构设计完整、连贯、可实施，已准备好进入实施阶段。

### Decision 9: UX架构集成策略

**问题**: 如何在架构层面支持UX设计规范的要求？

**UX设计规范要求分析:**
- **CLI视觉语言**: 需要Rich库支持颜色、图标、进度条
- **响应式CLI**: 需要终端尺寸检测和动态布局
- **跨平台一致性**: CLI和Web需要共享数据模型和状态
- **组件化设计**: 需要可复用的UI组件架构
- **可访问性**: 需要屏幕阅读器支持和键盘导航

**架构决策:**

**A. CLI层UX增强**
```python
# CLI响应式布局管理
class ResponsiveLayout:
    def __init__(self):
        self.console = Console()
        self.terminal_width = shutil.get_terminal_size().columns
    
    def get_layout_config(self):
        if self.terminal_width < 60:
            return "compact"
        elif self.terminal_width < 100:
            return "standard"
        else:
            return "expanded"

# UX组件系统
class TaskCard:
    def render(self) -> Panel:
        # 基于UX设计规范的任务卡片
        pass

class LearningWidget:
    def render(self) -> Panel:
        # 学习进展可视化组件
        pass
```

**B. 跨平台组件接口**
```python
# 统一组件接口
class ComponentInterface:
    def render_cli(self) -> str:
        """CLI渲染方法"""
        pass
    
    def render_web(self) -> dict:
        """Web数据方法"""
        pass

# 统一状态管理
class StateManager:
    def sync_cli_web_state(self):
        """CLI和Web状态同步"""
        pass
```

**C. Web架构预备 (v2.1)**
```python
# FastAPI + UX组件集成
@app.get("/dashboard")
async def dashboard():
    return templates.TemplateResponse("dashboard.html", {
        "tasks": get_tasks(),
        "learning_stats": get_learning_stats()
    })

# 响应式Web组件
# CSS Grid + Flexbox 支持移动端适配
```

**选择理由:**
- 支持UX设计规范的所有核心要求
- 保持MVP的简洁性，为v2.1预留扩展空间
- 确保CLI和Web的一致性体验
- 支持可访问性和响应式设计

### Decision 10: 可访问性架构支持

**问题**: 如何在架构层面支持WCAG 2.1 AA级别的可访问性要求？

**可访问性要求:**
- 屏幕阅读器支持
- 键盘导航
- 高对比度模式
- 减少动画偏好

**架构解决方案:**

**A. CLI可访问性层**
```python
class AccessibleCLI:
    def __init__(self, screen_reader_mode=False):
        self.screen_reader_mode = screen_reader_mode
        self.console = Console()
    
    def print_accessible(self, content, role="info"):
        """可访问的内容输出"""
        if self.screen_reader_mode:
            # 结构化输出用于屏幕阅读器
            print(f"{role.upper()}: {content}")
        else:
            # 富文本输出
            self.console.print(content)
```

**B. Web可访问性架构**
```html
<!-- 语义化HTML结构 -->
<main role="main" aria-label="AI-as-Me 主界面">
  <section aria-labelledby="tasks-heading">
    <h2 id="tasks-heading">当前任务</h2>
    <div aria-live="polite" aria-atomic="true">
      <!-- 动态状态更新 -->
    </div>
  </section>
</main>
```

**选择理由:**
- 确保产品的包容性设计
- 符合国际可访问性标准
- 为所有用户提供优质体验

## UX Architecture Integration Update

### UX设计规范集成总结

**更新时间**: 2026-01-13T06:00:16+08:00
**更新原因**: 集成UX Design Specification v2.0的架构要求

### 新增架构组件

#### 1. CLI UX组件系统
- **cli/components/**: 可复用的CLI UI组件库
  - `task_card.py`: 任务卡片显示组件
  - `learning_widget.py`: 学习进展可视化组件
  - `progress_bar.py`: 智能进度条组件
  - `responsive.py`: 响应式布局管理器

#### 2. 可访问性架构支持
- **cli/accessibility.py**: WCAG 2.1 AA级别支持
  - 屏幕阅读器兼容性
  - 键盘导航支持
  - 高对比度模式
  - 减少动画偏好处理

#### 3. 跨平台组件接口
- **kanban/components.py**: CLI和Web的统一组件接口
  - 数据层共享
  - 状态同步机制
  - 一致性保证

### 技术栈更新

#### 新增依赖
- **Rich**: CLI美化和响应式布局支持
- **Jinja2扩展**: Web模板系统支持

#### 架构决策更新
- **Decision 9**: UX架构集成策略
- **Decision 10**: 可访问性架构支持

### 实施计划调整

#### MVP阶段 (4天)
- Day 2-3: 集成基础UX组件 (task_card, responsive)
- Day 3-4: 添加学习可视化 (learning_widget) 和可访问性支持

#### v2.1阶段
- Web仪表板基于相同的组件接口
- 完整的响应式设计实现
- 高级可访问性特性

### 验证更新

#### 功能需求覆盖
- ✅ **UX一致性**: 通过统一组件接口保证
- ✅ **响应式设计**: 通过responsive.py实现
- ✅ **可访问性**: 通过accessibility.py支持
- ✅ **学习可视化**: 通过learning_widget.py实现

#### 非功能需求支持
- ✅ **性能**: UX组件不影响核心性能指标
- ✅ **可维护性**: 组件化设计提升代码复用
- ✅ **扩展性**: 为v2.1 Web界面奠定基础

这次架构更新确保了技术实现与UX设计规范的完全对齐，为开发团队提供了清晰的实施路径。
