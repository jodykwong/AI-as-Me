---
stepsCompleted: [1, 2, 3, 4, 5, 6, 7, 8]
inputDocuments:
  - "prd.md"
  - "product-brief-AI-as-Me-2026-01-10.md"
documentCounts:
  prd: 1
  briefs: 1
  uxDesign: 0
  research: 0
  projectDocs: 0
  projectContext: 0
workflowType: 'architecture'
lastStep: 8
status: 'complete'
completedAt: '2026-01-10'
project_name: 'AI-as-Me'
user_name: 'Jody'
date: '2026-01-10'
---

# Architecture Decision Document

_This document builds collaboratively through step-by-step discovery. Sections are appended as we work through each architectural decision together._

## Project Context Analysis

### Requirements Overview

**Functional Requirements:**
40 个 FRs 组织为 8 个功能模块，核心围绕"任务生命周期管理"展开：
- 任务创建 → 澄清确认 → 执行 → 日志记录 → 反思 → 规则积累
- 灵魂文件系统提供持久化的用户上下文
- CLI 接口作为主要交互方式

**Non-Functional Requirements:**
20 个 NFRs 驱动以下架构决策：
- **性能**: LLM 响应 <30s，文件操作 <1s，异步日志
- **安全**: 本地存储，chmod 600，API 密钥环境变量
- **可靠性**: 24/7 运行，自动重启，网络重连，日志轮转
- **集成**: DeepSeek API（OpenAI 兼容），Python 3.9+

**Scale & Complexity:**
- Primary domain: 嵌入式 AI Agent + CLI 工具
- Complexity level: 中等
- Estimated architectural components: 6-8 个核心模块

### Technical Constraints & Dependencies

| 约束 | 影响 |
|------|------|
| RDK X5 硬件 | SD 卡存储，WiFi 网络，长时间运行 |
| XLeRobot 依赖 | 基础环境和部署脚本 |
| DeepSeek API | 需要网络连接，无离线模式 |
| Python 3.9+ | 语言和生态系统选择 |
| 单人开发 | 简化架构，避免过度工程 |

### Cross-Cutting Concerns Identified

1. **错误处理与重试** — API 调用、文件 I/O、网络通信统一策略
2. **日志与可观测性** — 结构化日志、轮转机制、调试追踪
3. **安全与权限** — 文件权限、密钥管理、数据本地化
4. **进程生命周期** — systemd 集成、优雅关闭、崩溃恢复

## Starter Template Evaluation

### Primary Technology Domain

**Python CLI 工具 + 嵌入式 AI Agent** — 基于项目需求分析

### Starter Options Considered

| 选项 | 评估 |
|------|------|
| cookiecutter-python | 功能全面但对于 MVP 过于复杂 |
| 手动 src layout | 简洁可控，适合单人开发 |
| Poetry 模板 | 依赖管理优秀，但增加复杂度 |

### Selected Approach: 手动 src layout + pyproject.toml

**选择理由：**
1. 最小复杂度，适合单人开发和快速迭代
2. 现代 Python 打包标准（PEP 518/621）
3. 无额外工具依赖，降低 RDK X5 部署难度
4. 可在 Phase 2 按需引入更多工具

**初始化命令：**

```bash
mkdir -p ai-as-me/src/ai_as_me ai-as-me/soul ai-as-me/kanban/{inbox,todo,doing,done} ai-as-me/logs ai-as-me/tests
touch ai-as-me/src/ai_as_me/__init__.py
touch ai-as-me/pyproject.toml
```

### Architectural Decisions Provided by This Approach

**Language & Runtime:**
- Python 3.9+
- 类型提示（Type Hints）增强代码可读性

**CLI Framework:**
- Typer — 现代、简洁、自动补全

**Build Tooling:**
- pyproject.toml + hatchling（轻量级构建后端）
- 可选 pip install -e . 开发模式

**Testing Framework:**
- pytest（标准选择，简单易用）

**Code Organization:**
- src layout 模式（隔离源码和测试）
- 模块化设计（cli/agent/kanban/soul/llm/reflection）

**Development Experience:**
- python -m ai_as_me 开发运行
- ai-as-me CLI 生产运行

**Note:** 项目初始化应作为第一个实现 story。

## Core Architectural Decisions

### Decision Priority Analysis

**Critical Decisions (Block Implementation):**
- 日志格式：JSON Lines
- LLM API 封装：openai SDK + 自定义 LLMClient
- 服务化方案：systemd

**Important Decisions (Shape Architecture):**
- 配置管理：.env + YAML 混合
- 重试策略：指数退避
- 错误处理：三层分类

**Deferred Decisions (Post-MVP):**
- 文件监控（watchdog）— Phase 2
- 缓存策略 — Phase 2
- 多 LLM 支持 — Phase 3

### Data Architecture

| 决策 | 选择 | 理由 |
|------|------|------|
| 日志格式 | JSON Lines (.jsonl) | 结构化便于反思模块解析，支持增量读取 |
| 配置管理 | .env（密钥）+ YAML（复杂配置） | 安全标准 + 灵活性平衡 |
| 数据存储 | 文件系统（已由 PRD 确定） | 无数据库依赖，简化部署 |

### LLM Integration

| 决策 | 选择 | 理由 |
|------|------|------|
| API 封装 | openai SDK + 自定义 LLMClient | 最小依赖，DeepSeek 原生兼容 |
| 重试策略 | 指数退避（3次，初始1s，最大30s） | 平衡可靠性和响应速度 |
| 请求超时 | 60 秒 | 商业分析任务可接受等待时间 |
| 上下文注入 | mission → profile → rules → 任务 | 优先级从高到低 |

**LLMClient 核心接口：**
```python
class LLMClient:
    def __init__(self, api_key: str, base_url: str, model: str)
    def complete(self, messages: list[dict], **kwargs) -> str
    def complete_with_retry(self, messages: list[dict]) -> str
```

### Process Management & Deployment

| 决策 | 选择 | 理由 |
|------|------|------|
| 服务化 | systemd 服务 | Linux 原生，自动重启，journald 集成 |
| 运行模式 | 轮询（MVP） | 简单可靠，避免 SD 卡 watchdog 问题 |
| 轮询间隔 | 5 秒（可配置） | 平衡响应性和资源消耗 |
| 信号处理 | SIGTERM/SIGINT 优雅关闭 | 完成当前任务后安全退出 |

**systemd 服务配置：**
```ini
[Unit]
Description=AI-as-Me Agent
After=network.target

[Service]
Type=simple
User=sunrise
WorkingDirectory=/home/sunrise/ai-as-me
ExecStart=/usr/bin/python -m ai_as_me run
Restart=on-failure
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### Error Handling

| 决策 | 选择 | 理由 |
|------|------|------|
| 错误分类 | 三层（可恢复/需干预/致命） | 清晰的处理策略 |
| 错误格式 | 结构化 AgentError 类 | 统一错误处理，便于日志分析 |
| 任务失败 | 保留 doing/ + .error 文件 | 不丢失任务，便于排查 |

**错误码规范：**
| 错误码 | 含义 | 可恢复 |
|--------|------|--------|
| LLM_TIMEOUT | API 请求超时 | ✅ |
| LLM_RATE_LIMIT | API 限流 | ✅ |
| LLM_ERROR | API 返回错误 | ❌ |
| TASK_INVALID | 任务格式错误 | ❌ |
| SOUL_MISSING | 灵魂文件缺失 | ❌ |
| CONFIG_ERROR | 配置错误 | ❌ |

### Decision Impact Analysis

**Implementation Sequence:**
1. 项目初始化（目录结构 + pyproject.toml）
2. 配置管理模块（.env + YAML 加载）
3. LLMClient 封装（重试逻辑）
4. 灵魂文件加载
5. 看板文件管理
6. 任务执行引擎
7. 错误处理集成
8. systemd 服务配置

**Cross-Component Dependencies:**
- LLMClient ← 配置管理（API 密钥）
- 任务执行 ← LLMClient + 灵魂文件 + 看板
- 错误处理 ← 贯穿所有模块

## Implementation Patterns & Consistency Rules

### Pattern Categories Defined

**Critical Conflict Points Identified:** 4 个主要领域需要统一规范

### Naming Patterns

**Python 代码命名（PEP 8）：**
| 类型 | 约定 | 示例 |
|------|------|------|
| 模块/文件 | snake_case | `llm_client.py` |
| 类 | PascalCase | `LLMClient` |
| 函数/方法 | snake_case | `get_task()` |
| 变量 | snake_case | `task_content` |
| 常量 | UPPER_SNAKE | `MAX_RETRIES` |
| 私有 | 前缀下划线 | `_internal_method()` |

**文件命名：**
| 类型 | 约定 | 示例 |
|------|------|------|
| 任务文件 | 日期前缀 | `2026-01-10_market-research.md` |
| 日志文件 | 日期后缀 | `agent_2026-01-10.jsonl` |
| 配置文件 | 小写 | `config.yaml`, `.env` |

### Structure Patterns

**模块组织（按功能）：**
```
src/ai_as_me/
├── cli.py           # CLI 入口
├── agent.py         # 主执行引擎
├── kanban/          # 看板模块
├── soul/            # 灵魂文件模块
├── llm/             # LLM 集成模块
├── reflection/      # 反思模块
└── core/            # 核心工具（config/errors/logging）
```

**测试组织：**
- 位置：`tests/` 目录，镜像 src 结构
- 命名：`test_<module>.py`
- 函数：`test_<function>_<scenario>()`

### Format Patterns

**JSON Lines 日志格式：**
```json
{"ts": "ISO8601", "level": "INFO", "module": "agent", "event": "task_started", "data": {}}
```

**必填字段：** ts, level, module, event
**可选字段：** data, error_code, message

**任务文件格式：**
```markdown
---
id: 日期_任务名
created: ISO8601
status: inbox|todo|doing|done
priority: low|medium|high
---
# 任务标题
## 任务描述
## 期望输出
```

### Process Patterns

**日志级别规范：**
| 级别 | 场景 |
|------|------|
| DEBUG | 开发调试 |
| INFO | 正常业务事件 |
| WARNING | 可恢复问题 |
| ERROR | 需关注错误 |

**异常处理规范：**
- 使用自定义 `AgentError` / `LLMError` 类
- 禁止裸 `except:` 或静默忽略
- 可恢复错误自动重试，不可恢复向上传播

**函数设计规范：**
- 使用类型提示（Type Hints）
- `load_*` 返回 `Optional[T]`，不存在返回 None
- `get_*` 返回 `T`，不存在抛异常

### Enforcement Guidelines

**All AI Agents MUST:**
1. 遵循 PEP 8 命名规范
2. 使用 black 格式化代码（line-length=88）
3. 为所有函数添加类型提示
4. 使用项目定义的错误类处理异常
5. 按规范格式记录日志

**Pattern Verification:**
- PR Review 检查模式一致性
- pytest 验证关键模式（如日志格式）
- black + mypy 自动检查

### Pattern Examples

**Good Examples:**
```python
# ✅ 正确的函数签名和错误处理
def load_soul_file(file_type: str) -> Optional[str]:
    """加载灵魂文件内容"""
    path = SOUL_DIR / f"{file_type}.md"
    if not path.exists():
        return None
    return path.read_text()

def get_soul_file(file_type: str) -> str:
    """获取灵魂文件，不存在则报错"""
    content = load_soul_file(file_type)
    if content is None:
        raise AgentError("SOUL_MISSING", f"灵魂文件缺失: {file_type}.md")
    return content
```

**Anti-Patterns:**
```python
# ❌ 错误：无类型提示，裸 except
def loadSoulFile(fileType):  # 命名错误
    try:
        return open(f"soul/{fileType}.md").read()
    except:  # 裸 except
        return ""  # 静默失败
```

## Project Structure & Boundaries

### Complete Project Directory Structure

```
ai-as-me/
├── README.md                          # 项目说明
├── LICENSE                            # MIT/Apache 2.0
├── pyproject.toml                     # 项目配置（依赖、构建、工具）
├── .env.example                       # 环境变量模板
├── .gitignore                         # Git 忽略规则
│
├── src/
│   └── ai_as_me/
│       ├── __init__.py                # 版本号、包元数据
│       ├── __main__.py                # python -m ai_as_me 入口
│       ├── cli.py                     # Typer CLI 定义（run/status/reflect）
│       ├── agent.py                   # 主执行引擎（轮询循环）
│       │
│       ├── kanban/                    # 看板模块
│       │   ├── __init__.py
│       │   ├── manager.py             # 任务 CRUD、状态流转
│       │   └── models.py              # Task 数据模型
│       │
│       ├── soul/                      # 灵魂文件模块
│       │   ├── __init__.py
│       │   ├── loader.py              # 灵魂文件加载
│       │   └── models.py              # SoulContext 数据模型
│       │
│       ├── llm/                       # LLM 集成模块
│       │   ├── __init__.py
│       │   ├── client.py              # LLMClient 封装（重试逻辑）
│       │   └── prompts.py             # 提示词模板
│       │
│       ├── clarification/             # 混合式澄清模块
│       │   ├── __init__.py
│       │   └── handler.py             # 澄清问答处理
│       │
│       ├── reflection/                # 反思模块
│       │   ├── __init__.py
│       │   ├── analyzer.py            # 日志分析、规则提取
│       │   └── updater.py             # 规则写入
│       │
│       └── core/                      # 核心工具
│           ├── __init__.py
│           ├── config.py              # 配置加载（.env + YAML）
│           ├── errors.py              # AgentError, LLMError 定义
│           └── logging.py             # JSON Lines 日志器
│
├── tests/                             # 测试目录（镜像 src 结构）
│   ├── __init__.py
│   ├── conftest.py                    # pytest fixtures
│   ├── test_cli.py
│   ├── test_agent.py
│   ├── kanban/
│   │   └── test_manager.py
│   ├── soul/
│   │   └── test_loader.py
│   ├── llm/
│   │   └── test_client.py
│   └── reflection/
│       └── test_analyzer.py
│
├── scripts/                           # 部署和工具脚本
│   ├── setup.sh                       # 一键部署脚本
│   ├── init-soul.sh                   # 灵魂文件初始化
│   └── health-check.sh                # 健康检查
│
├── systemd/                           # systemd 服务文件
│   └── ai-as-me.service               # 服务定义
│
├── config/                            # 配置文件目录
│   └── config.yaml.example            # YAML 配置模板
│
├── soul/                              # 运行时：灵魂文件（用户数据）
│   ├── profile.md
│   ├── rules.md
│   └── mission.md
│
├── kanban/                            # 运行时：任务目录（用户数据）
│   ├── inbox/
│   ├── todo/
│   ├── doing/
│   └── done/
│
└── logs/                              # 运行时：日志目录
    └── .gitkeep
```

### Architectural Boundaries

**模块边界（内部通信）：**

```
┌─────────────────────────────────────────────────────────┐
│                        cli.py                           │
│                    (用户交互层)                          │
└──────────────────────────┬──────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                       agent.py                          │
│                    (编排协调层)                          │
├─────────────┬─────────────┬─────────────┬───────────────┤
│   kanban/   │    soul/    │    llm/     │  reflection/  │
│  (任务管理)  │ (灵魂加载)  │ (LLM调用)   │   (规则提取)   │
└─────────────┴─────────────┴─────────────┴───────────────┘
                           │
┌──────────────────────────▼──────────────────────────────┐
│                        core/                            │
│            (config / errors / logging)                  │
└─────────────────────────────────────────────────────────┘
```

**外部集成边界：**

| 边界 | 接口 | 说明 |
|------|------|------|
| LLM API | `llm/client.py` | DeepSeek API（OpenAI 格式） |
| 文件系统 | `kanban/`, `soul/`, `logs/` | 本地文件读写 |
| systemd | `systemd/ai-as-me.service` | 进程管理 |
| 用户交互 | `cli.py` (stdin/stdout) | Typer CLI |

### Requirements to Structure Mapping

| FR | 功能 | 实现位置 |
|-----|------|---------|
| FR1-5 | 任务管理 | `kanban/manager.py` |
| FR6-10 | 灵魂文件 | `soul/loader.py` |
| FR11-16 | 任务执行 | `agent.py` + `llm/client.py` |
| FR17-21 | 混合式澄清 | `clarification/handler.py` |
| FR22-25 | 日志追踪 | `core/logging.py` |
| FR26-31 | 反思进化 | `reflection/analyzer.py` + `updater.py` |
| FR32-37 | 系统管理 | `cli.py` |
| FR38-40 | 硬件集成 | `scripts/setup.sh` + `systemd/`

## Architecture Validation Results

### Coherence Validation ✅

**Decision Compatibility:**
所有技术选择兼容：Python 3.9+ / Typer / openai SDK / pyproject.toml / systemd

**Pattern Consistency:**
所有模式一致：PEP 8 命名 / snake_case 文件 / Type Hints / pytest

**Structure Alignment:**
结构支持所有决策：清晰模块边界 / 明确依赖方向 / 分离运行时目录

### Requirements Coverage Validation ✅

**Functional Requirements Coverage:**
40/40 FRs 完全覆盖，每个 FR 类别都有明确的模块实现位置

**Non-Functional Requirements Coverage:**
20/20 NFRs 完全覆盖，性能/安全/可靠性/集成/可维护性全部有架构支持

### Implementation Readiness Validation ✅

**Decision Completeness:** 所有关键决策已记录，包含版本和理由
**Structure Completeness:** 完整目录结构，所有文件和目录已定义
**Pattern Completeness:** 命名/结构/格式/过程模式全部有示例

### Gap Analysis Results

**Critical Gaps:** 无
**Important Gaps:** 无
**Nice-to-Have (Post-MVP):** CI/CD 配置、Docker 支持、性能监控

### Architecture Completeness Checklist

**✅ Requirements Analysis**
- [x] 项目上下文分析完成
- [x] 规模和复杂度评估完成
- [x] 技术约束已识别
- [x] 跨切关注点已映射

**✅ Architectural Decisions**
- [x] 关键决策带版本号记录
- [x] 技术栈完全指定
- [x] 集成模式已定义
- [x] 性能考虑已处理

**✅ Implementation Patterns**
- [x] 命名约定已建立
- [x] 结构模式已定义
- [x] 格式模式已指定
- [x] 过程模式已记录

**✅ Project Structure**
- [x] 完整目录结构已定义
- [x] 组件边界已建立
- [x] 集成点已映射
- [x] 需求到结构映射完成

### Architecture Readiness Assessment

**Overall Status:** ✅ READY FOR IMPLEMENTATION

**Confidence Level:** 高

**Key Strengths:**
- 最小复杂度设计，适合单人开发
- 清晰的模块边界，易于维护
- 完整的 FR/NFR 覆盖
- 详细的实现模式指导

**Areas for Future Enhancement:**
- Phase 2: watchdog 文件监控
- Phase 2: CI/CD 流水线
- Phase 3: Docker 容器化

### Implementation Handoff

**AI Agent Guidelines:**
1. 严格遵循架构决策文档
2. 一致使用实现模式
3. 尊重项目结构和边界
4. 架构问题参考本文档

**First Implementation Priority:**
```bash
# 1. 创建项目结构
mkdir -p ai-as-me/src/ai_as_me/{kanban,soul,llm,clarification,reflection,core}
mkdir -p ai-as-me/{tests,scripts,systemd,config,soul,kanban/{inbox,todo,doing,done},logs}

# 2. 初始化 pyproject.toml
# 3. 实现 core/ 模块（config, errors, logging）
# 4. 按 Implementation Sequence 继续
```

## Architecture Completion Summary

### Workflow Completion

**Architecture Decision Workflow:** COMPLETED ✅
**Total Steps Completed:** 8
**Date Completed:** 2026-01-10
**Document Location:** _bmad-output/planning-artifacts/architecture.md

### Final Architecture Deliverables

**📋 Complete Architecture Document**
- 所有架构决策已记录，带具体版本
- 实现模式确保 AI agent 一致性
- 完整项目结构，所有文件和目录已定义
- 需求到架构的映射
- 验证确认一致性和完整性

**🏗️ Implementation Ready Foundation**
- 15+ 架构决策已做出
- 4 类实现模式已定义（命名/结构/格式/过程）
- 7 个架构组件已指定
- 40 FRs + 20 NFRs 完全支持

**📚 AI Agent Implementation Guide**
- 技术栈带验证版本
- 防止实现冲突的一致性规则
- 清晰边界的项目结构
- 集成模式和通信标准

### Development Sequence

1. 使用文档化的命令初始化项目结构
2. 按架构设置开发环境
3. 实现核心架构基础（core/ 模块）
4. 按已建立的模式构建功能
5. 保持与文档规则的一致性

### Quality Assurance Checklist

**✅ Architecture Coherence**
- [x] 所有决策协同工作无冲突
- [x] 技术选择兼容
- [x] 模式支持架构决策
- [x] 结构与所有选择对齐

**✅ Requirements Coverage**
- [x] 所有功能需求有支持
- [x] 所有非功能需求已处理
- [x] 跨切关注点已处理
- [x] 集成点已定义

**✅ Implementation Readiness**
- [x] 决策具体可执行
- [x] 模式防止 agent 冲突
- [x] 结构完整无歧义
- [x] 提供示例增强清晰度

---

**Architecture Status:** ✅ READY FOR IMPLEMENTATION

**Next Phase:** 使用本文档中的架构决策和模式开始实现

**Document Maintenance:** 实现过程中做出重大技术决策时更新本架构

