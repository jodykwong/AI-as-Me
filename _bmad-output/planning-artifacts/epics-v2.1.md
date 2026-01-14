---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments: 
  - "prd-v2.1.md"
  - "architecture-v2.1.md"
workflowStatus: "completed"
completedAt: "2026-01-14T07:59:00+08:00"
---

# AI-as-Me v2.1 - Epic Breakdown

## Overview

v2.1 在 v2.0 基础上新增三个 P1 功能的 Epic 和 Story 分解。

## Requirements Inventory

### Functional Requirements (v2.1 新增)

FR-05: 多工具智能选择 - 系统根据任务特征自动选择最适合的 Agent CLI 工具
FR-06: Web 仪表板 - 提供可视化的任务管理和系统监控界面
FR-07: Agentic RAG 检索 - 系统能够检索和利用历史任务经验

### FR Coverage Map

FR-05: Epic 5 - 多工具智能选择
FR-06: Epic 6 - Web 仪表板
FR-07: Epic 7 - Agentic RAG 检索

---

## Epic 5: 多工具智能选择

用户能够让系统根据任务特征自动选择最适合的 Agent CLI 工具，提高任务执行效率和质量。

**FRs covered:** FR-05
**预估工时:** 2天
**依赖:** Epic 1, Epic 2 (v2.0)

### Story 5.1: 任务类型识别

As a 技术型独立AI创业者,
I want 系统能够自动识别任务类型（代码生成/审查/文档/架构/调试）,
So that 系统可以基于任务类型选择合适的工具。

**Acceptance Criteria:**

**Given** 用户创建一个任务 "写一个 Python 函数计算斐波那契数列"
**When** 系统分析任务描述
**Then** 系统识别任务类型为 `code_generation`
**And** 识别准确率 >80%

**Technical Notes:**
- 实现 `TaskAnalyzer` 类
- 使用关键词匹配 + 简单 NLP 分类
- 支持 5 种任务类型: code_generation, code_review, documentation, architecture, debug

---

### Story 5.2: 工具能力注册

As a 技术型独立AI创业者,
I want 系统维护各工具的能力矩阵配置,
So that 系统知道每个工具擅长什么类型的任务。

**Acceptance Criteria:**

**Given** 系统配置文件 `config/agents.yaml`
**When** 系统启动时加载配置
**Then** 系统能够读取每个工具的能力评分 (0.0-1.0)
**And** 支持 4 种工具: claude_code, opencode, gemini_cli, qwen_code

**Technical Notes:**
- 实现 `ToolRegistry` 类
- 配置格式见 architecture-v2.1.md
- 支持动态添加新工具

---

### Story 5.3: 历史成功率追踪

As a 技术型独立AI创业者,
I want 系统记录每个工具执行任务的成功率,
So that 系统可以基于历史数据优化工具选择。

**Acceptance Criteria:**

**Given** 工具执行完成一个任务
**When** 用户标记任务成功或失败
**Then** 系统记录执行历史到数据库
**And** 可以查询特定工具+任务类型的成功率

**Technical Notes:**
- 实现 `HistoryTracker` 类
- 新增 `tool_history` 数据库表
- 成功率 = 成功次数 / 总次数

---

### Story 5.4: 智能工具选择算法

As a 技术型独立AI创业者,
I want 系统综合任务类型、工具能力和历史成功率选择最优工具,
So that 我不需要每次手动指定工具。

**Acceptance Criteria:**

**Given** 用户创建任务但未指定工具
**When** 系统执行工具选择
**Then** 系统使用评分算法选择最优工具
**And** 评分公式: `score = capability * 0.5 + history * 0.3 + availability * 0.2`
**And** 选择决策记录到日志

**Technical Notes:**
- 实现 `SkillMatcher.match()` 方法
- 返回最高分工具
- 支持 `--tool` 参数手动覆盖

---

### Story 5.5: 手动工具覆盖

As a 技术型独立AI创业者,
I want 能够通过 `--tool` 参数手动指定工具,
So that 我可以在需要时覆盖系统的自动选择。

**Acceptance Criteria:**

**Given** 用户执行 `ai-as-me task add "任务描述" --tool claude_code`
**When** 系统处理任务
**Then** 系统使用用户指定的工具而非自动选择
**And** 如果指定工具不可用，提示错误

**Technical Notes:**
- CLI 参数: `--tool <tool_name>`
- 验证工具名称有效性

---

## Epic 6: Web 仪表板

用户能够通过 Web 界面可视化管理任务和监控系统状态。

**FRs covered:** FR-06
**预估工时:** 3天
**依赖:** Epic 2 (v2.0)

### Story 6.1: Web 服务启动

As a 技术型独立AI创业者,
I want 通过 `ai-as-me serve` 命令启动 Web 仪表板,
So that 我可以通过浏览器访问系统。

**Acceptance Criteria:**

**Given** 用户执行 `ai-as-me serve`
**When** 服务启动成功
**Then** Web 服务在 `http://localhost:8080` 可访问
**And** 终端显示服务启动信息和访问地址
**And** 支持 `--port` 参数自定义端口

**Technical Notes:**
- 使用 FastAPI + Uvicorn
- 默认端口 8080
- 仅本地访问 (127.0.0.1)

---

### Story 6.2: 任务看板视图

As a 技术型独立AI创业者,
I want 在 Web 界面看到 Kanban 风格的任务看板,
So that 我可以直观地查看所有任务状态。

**Acceptance Criteria:**

**Given** 用户访问 Web 仪表板首页
**When** 页面加载完成
**Then** 显示四列看板: Inbox, Todo, Doing, Done
**And** 每个任务显示为卡片，包含描述和状态
**And** 页面加载时间 <3秒

**Technical Notes:**
- 使用 HTMX + Alpine.js
- Tailwind CSS 样式
- 响应式布局支持移动端

---

### Story 6.3: Web 任务创建

As a 技术型独立AI创业者,
I want 通过 Web 界面创建新任务,
So that 我不需要每次都使用命令行。

**Acceptance Criteria:**

**Given** 用户在 Web 界面点击"新建任务"
**When** 用户填写任务描述并提交
**Then** 任务创建成功并出现在 Inbox 列
**And** 可选择指定工具或使用自动选择

**Technical Notes:**
- POST /api/tasks 接口
- 表单验证
- 创建成功后刷新看板

---

### Story 6.4: 任务状态实时更新

As a 技术型独立AI创业者,
I want 任务状态变化时 Web 界面自动更新,
So that 我不需要手动刷新页面。

**Acceptance Criteria:**

**Given** 用户打开 Web 仪表板
**When** 后台任务状态发生变化
**Then** 界面在 2秒内自动更新显示新状态
**And** 无需手动刷新页面

**Technical Notes:**
- 使用 SSE (Server-Sent Events)
- EventBus 发布/订阅模式
- 前端自动重连机制

---

### Story 6.5: 系统健康监控

As a 技术型独立AI创业者,
I want 在 Web 界面查看系统和工具的健康状态,
So that 我可以及时发现问题。

**Acceptance Criteria:**

**Given** 用户访问系统状态页面
**When** 页面加载
**Then** 显示各 Agent CLI 工具的可用状态
**And** 显示系统资源使用情况 (内存、CPU)
**And** 不可用工具显示红色警告

**Technical Notes:**
- GET /api/system/health 接口
- 定期健康检查 (每 30 秒)
- 简单的状态指示器

---

## Epic 7: Agentic RAG 检索

用户能够让系统检索和利用历史任务经验，增强任务执行效果。

**FRs covered:** FR-07
**预估工时:** 2天
**依赖:** Epic 4 (v2.0)

### Story 7.1: 向量存储初始化

As a 技术型独立AI创业者,
I want 系统能够初始化本地向量数据库,
So that 可以存储和检索历史经验。

**Acceptance Criteria:**

**Given** 系统首次启动或 RAG 功能启用
**When** 系统初始化向量存储
**Then** ChromaDB 数据库在 `~/.ai-as-me/rag/` 创建成功
**And** 嵌入模型 (MiniLM) 加载成功

**Technical Notes:**
- 使用 ChromaDB PersistentClient
- sentence-transformers/all-MiniLM-L6-v2
- 向量维度: 384

---

### Story 7.2: 任务经验存储

As a 技术型独立AI创业者,
I want 系统自动将完成的任务经验向量化存储,
So that 未来可以检索相似经验。

**Acceptance Criteria:**

**Given** 一个任务执行完成
**When** 系统处理任务结果
**Then** 任务描述和结果摘要被向量化
**And** 存储到 ChromaDB 包含元数据 (工具、成功状态、时间)

**Technical Notes:**
- 实现 `VectorStore.add()` 方法
- TaskExperience 数据结构
- 异步存储不阻塞主流程

---

### Story 7.3: 相似经验检索

As a 技术型独立AI创业者,
I want 系统能够检索与当前任务相似的历史经验,
So that 可以参考之前的成功案例。

**Acceptance Criteria:**

**Given** 用户创建一个新任务
**When** 系统准备执行任务
**Then** 系统检索 Top-5 相似历史任务
**And** 检索响应时间 <500ms
**And** 优先返回成功案例

**Technical Notes:**
- 实现 `ExperienceRetriever.retrieve()` 方法
- 余弦相似度检索
- 过滤 success=True 的记录

---

### Story 7.4: 上下文注入集成

As a 技术型独立AI创业者,
I want 检索到的历史经验自动注入到 Soul 提示词中,
So that AI 工具可以参考历史经验执行任务。

**Acceptance Criteria:**

**Given** 系统检索到相关历史经验
**When** 系统构建 Soul 提示词
**Then** 历史经验作为上下文片段注入模板
**And** 上下文长度限制在 2000 tokens 以内

**Technical Notes:**
- 扩展 `SoulInjector.inject()` 方法
- 更新 Jinja2 模板添加 `rag_context` 变量
- 实现 `build_context()` 方法

---

### Story 7.5: 用户反馈学习

As a 技术型独立AI创业者,
I want 系统根据我的反馈调整检索结果的权重,
So that 检索结果越来越符合我的需求。

**Acceptance Criteria:**

**Given** 用户对任务结果提供反馈 (满意/不满意)
**When** 系统处理反馈
**Then** 更新对应经验记录的权重
**And** 后续检索时高权重记录优先返回

**Technical Notes:**
- 添加 feedback 字段到 TaskExperience
- 简单的权重调整: 满意 +0.1, 不满意 -0.1
- 可选功能，MVP 可简化

---

## Summary

### Epic 统计

| Epic | 名称 | Story 数 | 预估工时 |
|------|------|----------|----------|
| Epic 5 | 多工具智能选择 | 5 | 2天 |
| Epic 6 | Web 仪表板 | 5 | 3天 |
| Epic 7 | Agentic RAG 检索 | 5 | 2天 |
| **总计** | | **15** | **7天** |

### 实施顺序建议

```
Week 1:
├── Epic 5: 多工具智能选择 (Day 1-2)
│   ├── Story 5.1 → 5.2 → 5.3 → 5.4 → 5.5
│
├── Epic 7: Agentic RAG (Day 3-4)
│   ├── Story 7.1 → 7.2 → 7.3 → 7.4 → 7.5
│
└── Epic 6: Web 仪表板 (Day 5-7)
    ├── Story 6.1 → 6.2 → 6.3 → 6.4 → 6.5
```

### 依赖关系图

```
v2.0 Epics
    │
    ├── Epic 1 (基础设施) ──┬──▶ Epic 5 (多工具选择)
    │                       │
    ├── Epic 2 (编排核心) ──┼──▶ Epic 6 (Web 仪表板)
    │                       │
    └── Epic 4 (养蛊循环) ──┴──▶ Epic 7 (RAG 检索)
```
