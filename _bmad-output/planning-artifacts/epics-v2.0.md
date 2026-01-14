---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments: 
  - "prd-v2.0-polished.md"
  - "architecture-v2.0.md" 
  - "ux-design-specification-v2.0.md"
workflowStatus: "completed"
completedAt: "2026-01-13T06:14:36+08:00"
---

# AI-as-Me v2.0 - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for AI-as-Me v2.0, decomposing the requirements from the PRD, UX Design, and Architecture requirements into implementable stories.

## Requirements Inventory

### Functional Requirements

FR-01: Agent CLI 工具集成 - 系统能够调用外部 Agent CLI 工具执行任务，支持 Claude Code 和 OpenCode，包含工具可用性检测和健康检查
FR-02: Soul 注入机制 - 系统能够将个人化上下文注入到外部工具，读取 soul/profile.md 和 soul/rules.md，构建个性化提示词模板
FR-03: 任务生命周期管理 - 系统能够管理任务从创建到完成的全流程，支持 task add/list 命令，任务状态跟踪 (todo → doing → done)
FR-04: 基础养蛊循环 - 系统能够从执行结果中学习和改进，收集任务执行结果和用户反馈，提取成功/失败模式，更新规则文件
FR-05: 多工具智能选择 - 系统能够根据任务特征选择最适合的工具 (P1 - v2.1)
FR-06: Web 仪表板 - 提供可视化的任务管理和系统监控界面 (P1 - v2.1)
FR-07: Agentic RAG 检索 - 系统能够检索和利用历史经验 (P1 - v2.1)

### NonFunctional Requirements

NFR-01: 性能需求 - Agent CLI 调用响应时间 <30秒，任务创建 CLI 命令响应时间 <2秒，Soul 注入时间 <5秒
NFR-02: 可靠性需求 - 目标可用性 >95%，故障恢复 <10秒内切换备用方案，Soul 数据和任务历史 100% 持久化
NFR-03: 安全需求 - 所有 Soul 数据仅本地存储，API 密钥环境变量存储，Soul 文件权限 600
NFR-04: 可用性需求 - pip install ai-as-me 一键安装，5分钟内完成基础配置，CLI 命令符合 Unix 惯例
NFR-05: 兼容性需求 - 支持 Linux (主要), macOS (支持), Windows (基础)，Python 3.9+，Node.js 16+

### Additional Requirements

- **Starter Template**: 架构文档指定使用 Python 包结构，包含 src/ai_as_me/ 目录结构
- **进程管理**: 外部工具调用的超时和错误处理机制
- **文件系统管理**: Soul 数据通过 Markdown 文件管理，支持动态读取和更新
- **CLI 接口设计**: 符合 Unix 惯例的命令行界面，支持 --help 参数
- **模板引擎**: 支持个性化提示词模板构建和注入
- **状态机**: 任务生命周期状态管理 (todo → doing → done)
- **健康检查**: 定期验证外部工具可用性
- **本地缓存**: 缓存常用工具版本，减少网络依赖
- **降级机制**: 主工具失败时切换到备用工具

### FR Coverage Map

FR-01: Epic 1 & Epic 2 - Agent CLI 工具集成和健康检查
FR-02: Epic 3 - Soul 注入机制和个性化提示词
FR-03: Epic 2 - 任务生命周期管理和 CLI 命令
FR-04: Epic 4 - 基础养蛊循环和自进化学习
NFR-01: Epic 2 - 性能需求 (响应时间)
NFR-02: Epic 2 - 可靠性需求 (可用性和故障恢复)
NFR-03: Epic 3 - 安全需求 (本地存储和权限)
NFR-04: Epic 1 - 可用性需求 (安装和配置)
NFR-05: Epic 1 - 兼容性需求 (操作系统和版本)

## Epic List

### Epic 1: 系统基础设施与安装
用户能够安装、配置和验证 AI-as-Me 系统的基本运行环境，包括依赖检查和初始化设置
**FRs covered:** FR-01 (部分 - 工具检测), NFR-04 (安装), NFR-05 (兼容性)

### Epic 2: Agent CLI 编排核心
用户能够通过命令行创建任务并调用外部 Agent CLI 工具执行，实现基本的任务编排功能
**FRs covered:** FR-01 (Agent CLI集成), FR-03 (任务管理), NFR-01 (性能), NFR-02 (可靠性)

### Epic 3: Soul 注入与个性化
用户能够通过 Soul 文件定义个人偏好和规则，系统自动将这些个性化上下文注入到外部工具中
**FRs covered:** FR-02 (Soul注入机制), NFR-03 (安全)

### Epic 4: 养蛊自进化循环
用户能够通过系统的反思和学习机制，让 AI 分身根据执行结果自动优化和进化
**FRs covered:** FR-04 (养蛊循环)

## Epic 1: 系统基础设施与安装

用户能够安装、配置和验证 AI-as-Me 系统的基本运行环境，包括依赖检查和初始化设置

### Story 1.1: 系统包安装

As a 技术型独立AI创业者,
I want 通过 pip install ai-as-me 一键安装系统,
So that 我可以快速开始使用 AI-as-Me 而无需复杂的安装过程.

**Acceptance Criteria:**

**Given** 用户有 Python 3.9+ 环境
**When** 用户执行 `pip install ai-as-me`
**Then** 系统成功安装所有必需的 Python 依赖包
**And** 安装过程在 2 分钟内完成
**And** 安装后 `ai-as-me --version` 命令可用并显示版本信息

### Story 1.2: 环境依赖检查

As a 技术型独立AI创业者,
I want 系统自动检查和验证运行环境依赖,
So that 我可以确保系统能够正常运行而不会遇到环境问题.

**Acceptance Criteria:**

**Given** AI-as-Me 已安装
**When** 用户执行 `ai-as-me check-env`
**Then** 系统检查 Python 版本 >= 3.9
**And** 系统检查 Node.js 版本 >= 16 (用于 npx 调用)
**And** 系统显示所有依赖检查结果 (通过/失败)
**And** 如果有依赖缺失，提供明确的安装指导

### Story 1.3: 初始化配置和目录结构

As a 技术型独立AI创业者,
I want 系统自动创建必需的配置和目录结构,
So that 我可以立即开始使用系统而无需手动创建文件夹.

**Acceptance Criteria:**

**Given** 环境依赖检查通过
**When** 用户执行 `ai-as-me init`
**Then** 系统创建 `soul/` 目录结构
**And** 系统创建 `kanban/` 目录用于任务管理
**And** 系统创建 `logs/` 目录用于日志记录
**And** 系统生成默认的 `.env` 配置文件模板
**And** 所有目录权限设置为用户可读写 (700)

### Story 1.4: Agent CLI 工具可用性检测

As a 技术型独立AI创业者,
I want 系统验证外部 Agent CLI 工具的可用性,
So that 我可以确保系统能够成功调用外部工具执行任务.

**Acceptance Criteria:**

**Given** 系统初始化完成
**When** 用户执行 `ai-as-me check-tools`
**Then** 系统检测 `npx -y @anthropic-ai/claude-code@2.0.76` 可用性
**And** 系统检测 `npx -y opencode-ai@1.1.3` 可用性
**And** 系统显示每个工具的状态 (可用/不可用/版本信息)
**And** 如果工具不可用，提供安装或配置建议
**And** 检测过程在 30 秒内完成

## Epic 2: Agent CLI 编排核心

用户能够通过命令行创建任务并调用外部 Agent CLI 工具执行，实现基本的任务编排功能

### Story 2.1: 任务创建和管理

As a 技术型独立AI创业者,
I want 通过命令行创建和管理任务,
So that 我可以组织和跟踪需要 AI 协助完成的工作.

**Acceptance Criteria:**

**Given** AI-as-Me 系统已初始化
**When** 用户执行 `ai-as-me task add "创建新的 API 接口"`
**Then** 系统创建新任务并分配唯一 ID
**And** 任务状态设置为 "todo"
**And** 任务信息保存到 `kanban/tasks.json` 文件
**And** 命令响应时间 < 2 秒
**And** 用户执行 `ai-as-me task list` 可以看到所有任务

### Story 2.2: Agent CLI 调用机制

As a 技术型独立AI创业者,
I want 系统能够调用外部 Agent CLI 工具,
So that 我可以利用现有的 AI 工具执行具体任务.

**Acceptance Criteria:**

**Given** 外部工具可用性检查通过
**When** 系统需要调用 Claude Code 工具
**Then** 系统执行 `npx -y @anthropic-ai/claude-code@2.0.76` 命令
**And** 系统捕获工具的输出和错误信息
**And** 系统记录调用日志到 `logs/agent_calls.log`
**And** 单次工具调用响应时间 < 30 秒
**And** 系统支持 OpenCode 工具的相同调用机制

### Story 2.3: 任务执行和状态跟踪

As a 技术型独立AI创业者,
I want 执行任务并跟踪其状态变化,
So that 我可以了解任务进展并获得执行结果.

**Acceptance Criteria:**

**Given** 任务已创建且状态为 "todo"
**When** 用户执行 `ai-as-me task start <task-id>`
**Then** 任务状态更新为 "doing"
**And** 系统根据任务描述选择合适的 Agent CLI 工具
**And** 系统调用选定的工具执行任务
**And** 任务完成后状态更新为 "done"
**And** 执行结果保存到 `kanban/results/<task-id>.md`

### Story 2.4: 错误处理和恢复机制

As a 技术型独立AI创业者,
I want 系统能够处理工具调用失败的情况,
So that 我的工作流程不会因为单个工具问题而中断.

**Acceptance Criteria:**

**Given** 主要 Agent CLI 工具不可用或调用失败
**When** 系统尝试执行任务
**Then** 系统在 10 秒内检测到失败
**And** 系统自动尝试备用工具 (Claude Code ↔ OpenCode)
**And** 如果所有工具都失败，任务状态设置为 "failed"
**And** 错误信息记录到日志文件
**And** 用户收到明确的错误提示和建议解决方案

## Epic 3: Soul 注入与个性化

用户能够通过 Soul 文件定义个人偏好和规则，系统自动将这些个性化上下文注入到外部工具中

### Story 3.1: Soul 文件管理

As a 技术型独立AI创业者,
I want 创建和编辑个人 Soul 档案文件,
So that 我可以定义个人偏好和工作风格让 AI 更好地理解我.

**Acceptance Criteria:**

**Given** AI-as-Me 系统已初始化
**When** 用户执行 `ai-as-me soul init`
**Then** 系统创建 `soul/profile.md` 个人档案模板
**And** 系统创建 `soul/rules.md` 工作规则模板
**And** 文件权限设置为 600 (仅用户可读写)
**And** 模板包含引导性问题帮助用户填写
**And** 用户可以使用任何文本编辑器修改这些文件

### Story 3.2: 提示词模板构建

As a 技术型独立AI创业者,
I want 系统基于我的 Soul 数据构建个性化提示词,
So that 外部 AI 工具能够按照我的风格和偏好工作.

**Acceptance Criteria:**

**Given** Soul 文件已创建并包含用户数据
**When** 系统准备调用外部工具
**Then** 系统读取 `soul/profile.md` 和 `soul/rules.md` 内容
**And** 系统构建包含个人上下文的提示词模板
**And** 模板包含用户的编程风格、偏好和约束
**And** 提示词构建过程在 5 秒内完成
**And** 构建的提示词不超过外部工具的 context window 限制

### Story 3.3: Soul 注入到外部工具

As a 技术型独立AI创业者,
I want 系统将我的个性化上下文传递给 Agent CLI 工具,
So that 工具输出能够体现我的个人特征和偏好.

**Acceptance Criteria:**

**Given** 个性化提示词模板已构建
**When** 系统调用外部 Agent CLI 工具
**Then** 系统将 Soul 上下文作为系统提示词传递给工具
**And** 工具接收到完整的个人化上下文信息
**And** 工具输出体现用户的编程风格和偏好
**And** Soul 注入过程不影响工具调用的性能要求
**And** 注入过程对用户透明，无需额外操作

### Story 3.4: 安全和权限管理

As a 技术型独立AI创业者,
I want 确保我的 Soul 数据安全地存储在本地,
So that 我的个人信息和偏好不会泄露到外部系统.

**Acceptance Criteria:**

**Given** Soul 文件包含敏感的个人信息
**When** 系统处理 Soul 数据
**Then** 所有 Soul 数据仅在本地文件系统存储
**And** Soul 文件权限严格限制为用户可读写 (600)
**And** 系统不将 Soul 数据上传到任何云端服务
**And** API 密钥通过环境变量管理，不在 Soul 文件中存储
**And** 系统提供 Soul 数据备份和恢复功能

## Epic 4: 养蛊自进化循环

用户能够通过系统的反思和学习机制，让 AI 分身根据执行结果自动优化和进化

### Story 4.1: 执行结果收集

As a 技术型独立AI创业者,
I want 系统收集任务执行结果和我的反馈,
So that 系统能够学习什么方法有效什么方法需要改进.

**Acceptance Criteria:**

**Given** 任务执行完成
**When** 系统生成执行结果
**Then** 系统自动保存完整的执行日志到 `logs/execution_history.json`
**And** 系统记录使用的工具、提示词和输出结果
**And** 系统提示用户对结果进行评分 (1-5分)
**And** 用户可以添加文字反馈说明满意或不满意的原因
**And** 所有反馈数据与任务 ID 关联存储

### Story 4.2: 反思和模式提取

As a 技术型独立AI创业者,
I want 系统分析执行历史找出成功和失败的模式,
So that 系统能够识别哪些方法更适合我的工作风格.

**Acceptance Criteria:**

**Given** 系统积累了多次执行历史和用户反馈
**When** 用户执行 `ai-as-me reflect`
**Then** 系统分析高分任务 (4-5分) 的共同特征
**And** 系统识别低分任务 (1-2分) 的问题模式
**And** 系统提取成功的提示词模板和工具选择策略
**And** 系统生成反思报告保存到 `logs/reflection_<date>.md`
**And** 反思过程在 30 秒内完成

### Story 4.3: 规则自动更新

As a 技术型独立AI创业者,
I want 系统根据学习到的模式自动更新我的 Soul 规则,
So that 未来的任务执行能够自动应用这些改进.

**Acceptance Criteria:**

**Given** 反思分析已完成并识别出改进模式
**When** 系统发现可以改进的规则
**Then** 系统生成建议的规则更新内容
**And** 系统向用户展示建议的 `soul/rules.md` 修改
**And** 用户确认后系统自动更新规则文件
**And** 系统保留规则变更历史到 `soul/rules_history.json`
**And** 更新的规则在下次任务执行时自动生效

### Story 4.4: 学习效果验证

As a 技术型独立AI创业者,
I want 查看系统的学习进展和改进效果,
So that 我可以了解 AI 分身是否真正在进化和改善.

**Acceptance Criteria:**

**Given** 系统已运行一段时间并积累了学习数据
**When** 用户执行 `ai-as-me stats`
**Then** 系统显示任务满意度趋势图 (文本格式)
**And** 系统显示规则更新次数和类型统计
**And** 系统显示最常用的成功模式和工具选择
**And** 系统计算并显示学习效果指标 (如满意度提升百分比)
**And** 系统提供个性化程度评估 (相比初始状态的差异)
