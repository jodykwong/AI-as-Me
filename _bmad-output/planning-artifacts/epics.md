---
stepsCompleted: [1, 2, 3, 4]
status: complete
inputDocuments:
  - "prd.md"
  - "architecture.md"
workflowType: 'epics'
project_name: 'AI-as-Me'
date: '2026-01-11'
---

# AI-as-Me - Epic Breakdown

## Overview

This document provides the complete epic and story breakdown for AI-as-Me, decomposing the requirements from the PRD and Architecture into implementable stories.

## Requirements Inventory

### Functional Requirements

**任务管理 (Task Management)**
- FR1: 用户可以在 inbox 目录中创建新任务文件
- FR2: 用户可以查看当前所有任务的状态（inbox/todo/doing/done）
- FR3: 系统可以自动将任务从一个状态目录移动到另一个状态目录
- FR4: 用户可以手动移动任务到任意状态目录
- FR5: 用户可以在任务文件中定义任务描述、上下文和期望输出

**灵魂文件系统 (Soul File System)**
- FR6: 用户可以创建和编辑 profile.md 记录个人履历和风格
- FR7: 用户可以创建和编辑 rules.md 存储决策规则
- FR8: 用户可以创建和编辑 mission.md 定义使命和目标
- FR9: 系统可以在任务执行时加载所有灵魂文件作为上下文
- FR10: 用户可以查看当前规则库中的所有规则

**任务执行 (Task Execution)**
- FR11: 系统可以从 todo 目录读取任务并开始执行
- FR12: 系统可以调用 LLM API 处理任务内容
- FR13: 系统可以将灵魂文件内容作为系统提示注入 LLM
- FR14: 系统可以生成结构化的任务输出结果
- FR15: 系统可以将完成的任务和结果移动到 done 目录
- FR16: 系统可以处理 LLM API 调用失败并进行重试

**混合式澄清 (Hybrid Clarification)**
- FR17: 系统可以在执行任务前分析任务复杂度
- FR18: 系统可以生成澄清问题向用户确认需求
- FR19: 用户可以回答澄清问题提供额外上下文
- FR20: 系统可以在获得用户确认后开始执行任务
- FR21: 用户可以跳过澄清直接要求执行（高信任模式）

**日志与追踪 (Logging & Tracking)**
- FR22: 系统可以记录每个任务的执行过程日志
- FR23: 系统可以记录 LLM API 的输入和输出
- FR24: 用户可以查看任意任务的执行日志
- FR25: 系统可以记录任务的开始时间、结束时间和耗时

**反思与进化 (Reflection & Evolution)**
- FR26: 用户可以手动触发反思模块分析已完成任务
- FR27: 系统可以从任务日志中提取潜在的新规则
- FR28: 系统可以向用户展示建议的新规则
- FR29: 用户可以确认或拒绝建议的规则
- FR30: 系统可以将用户确认的规则写入 rules.md
- FR31: 系统可以在后续任务中应用已积累的规则

**系统管理 (System Management)**
- FR32: 用户可以通过 CLI 启动 Agent 主循环
- FR33: 用户可以通过 CLI 查看系统状态
- FR34: 用户可以通过 CLI 手动触发反思
- FR35: 用户可以配置 LLM API 密钥和端点
- FR36: 系统可以作为后台服务持续运行
- FR37: 用户可以通过 git pull 更新系统

**硬件集成 (Hardware Integration)**
- FR38: 系统可以在 RDK X5 硬件上部署和运行
- FR39: 系统可以通过 WiFi 连接访问 LLM API
- FR40: 系统可以使用 SD 卡存储所有数据文件

### Non-Functional Requirements

**Performance**
- NFR1: LLM API 响应时间 <30 秒/请求
- NFR2: 任务状态流转 <1 秒
- NFR3: 灵魂文件加载 <2 秒
- NFR4: 日志写入异步/非阻塞

**Security**
- NFR5: 灵魂文件权限 chmod 600
- NFR6: API 密钥环境变量存储，不入版本控制
- NFR7: 所有用户数据本地存储，永不上云
- NFR8: 日志脱敏，不记录完整 API 密钥

**Reliability**
- NFR9: 24/7 长时间运行能力
- NFR10: 网络中断后自动重连，指数退避
- NFR11: LLM API 失败后最多重试 3 次
- NFR12: systemd 服务，崩溃后自动重启
- NFR13: 日志轮转，单文件 <10MB，保留 7 天

**Integration**
- NFR14: 支持 DeepSeek API（OpenAI 兼容格式）
- NFR15: 请求超时 60 秒，连接超时 10 秒
- NFR16: 兼容 XLeRobot 基础包
- NFR17: 支持 Python 3.9+

**Maintainability**
- NFR18: 遵循 PEP 8，使用 black 格式化
- NFR19: 用户友好错误提示，包含解决建议
- NFR20: 所有配置通过环境变量或配置文件

### Additional Requirements (from Architecture)

**项目初始化**
- 手动 src layout + pyproject.toml（非 starter 模板）
- 目录结构：src/ai_as_me/{kanban,soul,llm,clarification,reflection,core}
- 运行时目录：soul/, kanban/{inbox,todo,doing,done}, logs/

**技术栈**
- Python 3.9+ with Type Hints
- Typer CLI 框架（≥0.9.0）
- openai SDK（≥1.0.0）+ 自定义 LLMClient 封装
- python-dotenv（≥1.0.0）+ PyYAML（≥6.0）
- pytest 测试框架
- black + mypy 代码质量

**部署**
- systemd 服务管理
- 轮询模式（5秒间隔）
- SIGTERM/SIGINT 优雅关闭
- scripts/setup.sh 一键部署

**日志格式**
- JSON Lines (.jsonl)
- 必填字段：ts, level, module, event
- 可选字段：data, error_code, message

**错误处理**
- 自定义 AgentError / LLMError 类
- 三层分类：可恢复/需干预/致命
- 失败任务保留在 doing/ + .error 文件

### FR Coverage Map

| FR | Epic | 简述 |
|----|------|------|
| FR1 | Epic 3 | inbox 创建任务 |
| FR2 | Epic 3 | 查看任务状态 |
| FR3 | Epic 3 | 自动状态流转 |
| FR4 | Epic 3 | 手动移动任务 |
| FR5 | Epic 3 | 任务文件格式 |
| FR6 | Epic 2 | profile.md 管理 |
| FR7 | Epic 2 | rules.md 管理 |
| FR8 | Epic 2 | mission.md 管理 |
| FR9 | Epic 2 | 灵魂文件加载 |
| FR10 | Epic 2 | 规则查看 |
| FR11 | Epic 4 | 读取 todo 任务 |
| FR12 | Epic 4 | 调用 LLM API |
| FR13 | Epic 4 | 灵魂上下文注入 |
| FR14 | Epic 4 | 生成结构化输出 |
| FR15 | Epic 4 | 移动到 done |
| FR16 | Epic 4 | API 重试 |
| FR17 | Epic 5 | 分析任务复杂度 |
| FR18 | Epic 5 | 生成澄清问题 |
| FR19 | Epic 5 | 用户回答澄清 |
| FR20 | Epic 5 | 确认后执行 |
| FR21 | Epic 5 | 跳过澄清 |
| FR22 | Epic 6 | 执行日志 |
| FR23 | Epic 6 | API 输入输出记录 |
| FR24 | Epic 6 | 查看日志 |
| FR25 | Epic 6 | 时间记录 |
| FR26 | Epic 7 | 手动触发反思 |
| FR27 | Epic 7 | 提取潜在规则 |
| FR28 | Epic 7 | 展示建议规则 |
| FR29 | Epic 7 | 确认/拒绝规则 |
| FR30 | Epic 7 | 写入 rules.md |
| FR31 | Epic 7 | 应用积累规则 |
| FR32 | Epic 1 | CLI 启动 |
| FR33 | Epic 1 | CLI 状态查看 |
| FR34 | Epic 7 | CLI 触发反思 |
| FR35 | Epic 1 | 配置 API 密钥 |
| FR36 | Epic 1 | 后台服务运行 |
| FR37 | Epic 1 | git pull 更新 |
| FR38 | Epic 1 | RDK X5 部署 |
| FR39 | Epic 1 | WiFi 连接 |
| FR40 | Epic 1 | SD 卡存储 |

## Epic List

### Epic 1: 系统基础与 CLI
用户可以在 RDK X5 上部署、配置和运行 AI-as-Me 系统
**FRs covered:** FR32, FR33, FR35, FR36, FR37, FR38, FR39, FR40

### Epic 2: 灵魂注入系统
用户可以创建和管理个性化的 AI 身份（profile/rules/mission）
**FRs covered:** FR6, FR7, FR8, FR9, FR10

### Epic 3: 任务管理看板
用户可以通过文件级看板创建和管理任务
**FRs covered:** FR1, FR2, FR3, FR4, FR5

### Epic 4: LLM 驱动的任务执行
用户的任务被 AI 执行，产出高质量结果
**FRs covered:** FR11, FR12, FR13, FR14, FR15, FR16

### Epic 5: 混合式澄清
用户在任务执行前获得智能澄清，确保需求清晰
**FRs covered:** FR17, FR18, FR19, FR20, FR21

### Epic 6: 执行透明度（日志与追踪）
用户可以查看任务执行的完整历史和详情
**FRs covered:** FR22, FR23, FR24, FR25

### Epic 7: 自进化循环
用户看到 AI 从经验中学习，规则库自动积累
**FRs covered:** FR26, FR27, FR28, FR29, FR30, FR31, FR34

---

## Epic 1: 系统基础与 CLI

**Goal:** 用户可以在 RDK X5 上部署、配置和运行 AI-as-Me 系统

**FRs covered:** FR32, FR33, FR35, FR36, FR37, FR38, FR39, FR40

### Story 1.1: 项目初始化与目录结构

As a **开发者**,
I want **初始化 AI-as-Me 项目结构**,
So that **所有模块有统一的代码组织和依赖管理**.

**Acceptance Criteria:**

**Given** 空的项目目录
**When** 执行初始化脚本
**Then** 创建完整的 src layout 结构
**And** pyproject.toml 包含所有依赖声明
**And** 运行时目录 (soul/, kanban/, logs/) 被创建

### Story 1.2: 环境配置与 API 密钥管理

As a **用户**,
I want **通过 .env 文件配置 API 密钥和端点**,
So that **系统能安全连接 LLM 服务而不泄露敏感信息**.

**Acceptance Criteria:**

**Given** 项目已初始化
**When** 用户创建 .env 文件并设置 DEEPSEEK_API_KEY
**Then** 系统能从环境变量读取配置
**And** .env 文件被 .gitignore 排除
**And** 缺失配置时显示友好错误提示

### Story 1.3: CLI 入口与帮助命令

As a **用户**,
I want **通过 `ai-as-me` 命令启动 CLI**,
So that **我能查看可用命令和使用帮助**.

**Acceptance Criteria:**

**Given** 系统已安装
**When** 执行 `ai-as-me --help`
**Then** 显示所有可用命令列表
**And** 每个命令有清晰的帮助文档
**And** 退出码符合规范 (成功=0)

### Story 1.4: 系统状态查看命令

As a **用户**,
I want **执行 `ai-as-me status` 查看系统状态**,
So that **我能了解当前任务队列和服务运行状态**.

**Acceptance Criteria:**

**Given** 系统已配置
**When** 执行 `ai-as-me status`
**Then** 显示各队列 (inbox/todo/doing/done) 任务数量
**And** 显示 API 连接状态
**And** 显示灵魂文件加载状态

### Story 1.5: Agent 主循环启动

As a **用户**,
I want **执行 `ai-as-me run` 启动 Agent 主循环**,
So that **系统开始自动处理任务队列**.

**Acceptance Criteria:**

**Given** 系统配置完整
**When** 执行 `ai-as-me run`
**Then** Agent 进入轮询模式 (5秒间隔)
**And** 自动检测 todo 目录中的新任务
**And** 支持 SIGTERM/SIGINT 优雅关闭
**And** 记录启动日志

### Story 1.6: systemd 服务配置

As a **用户**,
I want **将 AI-as-Me 配置为 systemd 服务**,
So that **系统能在后台持续运行并自动重启**.

**Acceptance Criteria:**

**Given** AI-as-Me 已安装
**When** 执行 `scripts/setup.sh`
**Then** 创建 systemd service 文件
**And** 服务崩溃后自动重启
**And** 可通过 `systemctl status ai-as-me` 查看状态

### Story 1.7: 一键部署脚本

As a **用户**,
I want **在 RDK X5 上执行一键部署脚本**,
So that **系统完成所有依赖安装和配置**.

**Acceptance Criteria:**

**Given** RDK X5 已连接 WiFi
**When** 执行 `scripts/setup.sh`
**Then** 安装 Python 依赖
**And** 创建运行时目录结构
**And** 配置 systemd 服务
**And** 检测 SD 卡存储路径

---

## Epic 2: 灵魂注入系统

**Goal:** 用户可以创建和管理个性化的 AI 身份（profile/rules/mission）

**FRs covered:** FR6, FR7, FR8, FR9, FR10

### Story 2.1: 灵魂目录初始化

As a **用户**,
I want **系统自动创建 soul/ 目录和模板文件**,
So that **我能快速开始定义 AI 身份**.

**Acceptance Criteria:**

**Given** 系统首次运行
**When** soul/ 目录不存在
**Then** 自动创建 soul/ 目录
**And** 创建 profile.md, rules.md, mission.md 模板文件
**And** 模板包含示例内容和说明注释
**And** 文件权限设为 600

### Story 2.2: 个人履历管理 (profile.md)

As a **用户**,
I want **编辑 profile.md 记录个人履历和写作风格**,
So that **AI 能用我的身份和风格回应**.

**Acceptance Criteria:**

**Given** profile.md 文件存在
**When** 用户编辑文件内容
**Then** 系统能解析 markdown 格式
**And** 支持个人背景、专业领域、语言风格等字段
**And** 文件变更后下次任务执行自动生效

### Story 2.3: 决策规则管理 (rules.md)

As a **用户**,
I want **编辑 rules.md 存储决策规则和偏好**,
So that **AI 能按照我的习惯做决策**.

**Acceptance Criteria:**

**Given** rules.md 文件存在
**When** 用户添加新规则
**Then** 系统能解析规则列表
**And** 支持规则分类（沟通、技术、生活等）
**And** 规则格式支持 markdown 列表

### Story 2.4: 使命定义管理 (mission.md)

As a **用户**,
I want **编辑 mission.md 定义使命和长期目标**,
So that **AI 能在任务中体现我的价值观**.

**Acceptance Criteria:**

**Given** mission.md 文件存在
**When** 用户定义使命和目标
**Then** 系统能解析使命陈述
**And** 支持短期/长期目标定义
**And** 目标可被后续反思模块引用

### Story 2.5: 灵魂文件加载器

As a **系统**,
I want **在任务执行时加载所有灵魂文件**,
So that **LLM 能获得完整的身份上下文**.

**Acceptance Criteria:**

**Given** 任务开始执行
**When** 系统准备 LLM 上下文
**Then** 加载 profile.md, rules.md, mission.md
**And** 合并为结构化的系统提示
**And** 加载时间 <2 秒
**And** 文件不存在时优雅降级（不中断执行）

### Story 2.6: 规则查看命令

As a **用户**,
I want **执行 `ai-as-me rules` 查看当前规则库**,
So that **我能确认 AI 已学习的所有规则**.

**Acceptance Criteria:**

**Given** rules.md 包含规则
**When** 执行 `ai-as-me rules`
**Then** 以格式化列表显示所有规则
**And** 显示规则分类和数量统计
**And** 空规则库时显示提示信息

---

## Epic 3: 任务管理看板

**Goal:** 用户可以通过文件级看板创建和管理任务

**FRs covered:** FR1, FR2, FR3, FR4, FR5

### Story 3.1: 看板目录结构初始化

As a **用户**,
I want **系统自动创建看板目录结构**,
So that **我能立即开始使用任务管理功能**.

**Acceptance Criteria:**

**Given** 系统首次运行
**When** kanban/ 目录不存在
**Then** 创建 kanban/inbox/, kanban/todo/, kanban/doing/, kanban/done/
**And** 各目录有适当的文件系统权限

### Story 3.2: 创建新任务

As a **用户**,
I want **在 inbox 目录中创建任务文件**,
So that **我能快速记录待处理的事项**.

**Acceptance Criteria:**

**Given** kanban/inbox/ 目录存在
**When** 用户创建 .md 文件
**Then** 文件被识别为新任务
**And** 支持 YAML frontmatter 定义元数据
**And** 支持 markdown 正文描述任务内容

### Story 3.3: 任务文件格式定义

As a **用户**,
I want **在任务文件中定义描述、上下文和期望输出**,
So that **AI 能准确理解任务需求**.

**Acceptance Criteria:**

**Given** 任务文件存在
**When** 解析任务内容
**Then** 支持 title 字段（任务标题）
**And** 支持 context 字段（背景信息）
**And** 支持 expected_output 字段（期望结果格式）
**And** 支持 priority 字段（可选，默认 normal）

### Story 3.4: 查看任务状态命令

As a **用户**,
I want **执行 `ai-as-me tasks` 查看所有任务状态**,
So that **我能了解当前任务队列情况**.

**Acceptance Criteria:**

**Given** 看板目录包含任务
**When** 执行 `ai-as-me tasks`
**Then** 分状态列出所有任务 (inbox/todo/doing/done)
**And** 显示每个任务的标题和创建时间
**And** 显示各状态任务数量统计

### Story 3.5: 手动移动任务

As a **用户**,
I want **执行 `ai-as-me move <task> <status>` 手动移动任务**,
So that **我能手动控制任务状态流转**.

**Acceptance Criteria:**

**Given** 任务文件存在于某状态目录
**When** 执行移动命令
**Then** 任务文件移动到目标状态目录
**And** 操作时间 <1 秒
**And** 无效状态或任务时显示错误提示

### Story 3.6: 自动状态流转

As a **系统**,
I want **在任务执行时自动更新任务状态**,
So that **用户无需手动跟踪任务进度**.

**Acceptance Criteria:**

**Given** 任务在 todo 目录
**When** Agent 开始执行任务
**Then** 任务移动到 doing 目录
**And** 执行完成后移动到 done 目录
**And** 状态变更记录到日志

---

## Epic 4: LLM 驱动的任务执行

**Goal:** 用户的任务被 AI 执行，产出高质量结果

**FRs covered:** FR11, FR12, FR13, FR14, FR15, FR16

### Story 4.1: LLM 客户端封装

As a **系统**,
I want **封装 OpenAI 兼容的 LLM 客户端**,
So that **可以统一调用 DeepSeek 或其他兼容 API**.

**Acceptance Criteria:**

**Given** API 密钥和端点已配置
**When** 初始化 LLMClient
**Then** 创建 openai SDK 客户端实例
**And** 支持自定义 base_url 指向 DeepSeek
**And** 设置请求超时 60 秒，连接超时 10 秒

### Story 4.2: 任务读取与解析

As a **系统**,
I want **从 todo 目录读取并解析任务文件**,
So that **能提取任务内容准备执行**.

**Acceptance Criteria:**

**Given** todo 目录包含任务文件
**When** Agent 轮询检测到新任务
**Then** 解析 YAML frontmatter 元数据
**And** 提取 markdown 正文作为任务描述
**And** 验证必填字段存在

### Story 4.3: 灵魂上下文注入

As a **系统**,
I want **将灵魂文件内容注入 LLM 系统提示**,
So that **AI 以用户身份执行任务**.

**Acceptance Criteria:**

**Given** 灵魂文件已加载
**When** 构建 LLM 请求
**Then** profile.md 内容作为身份背景
**And** rules.md 内容作为决策约束
**And** mission.md 内容作为目标导向
**And** 系统提示结构清晰有层次

### Story 4.4: LLM API 调用与响应

As a **系统**,
I want **调用 LLM API 处理任务并获取响应**,
So that **任务能被 AI 智能处理**.

**Acceptance Criteria:**

**Given** LLM 请求已构建
**When** 调用 API
**Then** 发送完整的上下文和任务描述
**And** 响应时间 <30 秒
**And** 正确解析 API 返回的内容

### Story 4.5: API 调用失败重试

As a **系统**,
I want **在 API 调用失败时自动重试**,
So that **临时性网络问题不会中断任务执行**.

**Acceptance Criteria:**

**Given** API 调用失败
**When** 错误类型为可恢复（网络超时、5xx 错误）
**Then** 使用指数退避策略重试
**And** 最多重试 3 次
**And** 每次重试记录到日志
**And** 超过重试次数后标记任务失败

### Story 4.6: 结构化输出生成

As a **系统**,
I want **将 LLM 响应格式化为结构化输出**,
So that **任务结果易于保存和查看**.

**Acceptance Criteria:**

**Given** LLM 返回响应
**When** 处理输出
**Then** 生成 result.md 文件包含输出内容
**And** 包含任务元信息（执行时间、模型等）
**And** 保留原始任务文件引用

### Story 4.7: 任务完成与归档

As a **系统**,
I want **将完成的任务和结果移动到 done 目录**,
So that **任务生命周期完整闭环**.

**Acceptance Criteria:**

**Given** 任务执行成功
**When** 输出生成完成
**Then** 任务文件移动到 done 目录
**And** 结果文件保存在任务同目录
**And** 记录完成时间戳

---

## Epic 5: 混合式澄清

**Goal:** 用户在任务执行前获得智能澄清，确保需求清晰

**FRs covered:** FR17, FR18, FR19, FR20, FR21

### Story 5.1: 任务复杂度分析

As a **系统**,
I want **在执行任务前分析任务复杂度**,
So that **决定是否需要向用户澄清**.

**Acceptance Criteria:**

**Given** 任务文件已解析
**When** 分析任务内容
**Then** 评估任务描述的清晰度
**And** 检测模糊或多义的表达
**And** 返回复杂度评分（低/中/高）

### Story 5.2: 澄清问题生成

As a **系统**,
I want **为复杂任务生成澄清问题**,
So that **用户能补充必要的上下文**.

**Acceptance Criteria:**

**Given** 任务复杂度为中或高
**When** 生成澄清问题
**Then** 调用 LLM 分析任务缺失信息
**And** 生成 1-3 个针对性问题
**And** 问题保存到任务文件的 clarification 字段

### Story 5.3: 澄清问题展示

As a **用户**,
I want **看到系统生成的澄清问题**,
So that **我能理解 AI 需要什么信息**.

**Acceptance Criteria:**

**Given** 澄清问题已生成
**When** 任务进入待澄清状态
**Then** CLI 显示任务标题和澄清问题
**And** 提示用户回答或跳过
**And** 任务保留在 doing 目录等待回答

### Story 5.4: 用户回答澄清

As a **用户**,
I want **回答澄清问题提供额外上下文**,
So that **AI 能更准确地执行任务**.

**Acceptance Criteria:**

**Given** 澄清问题已展示
**When** 用户提供回答
**Then** 回答保存到任务文件的 answers 字段
**And** 更新任务状态为已澄清
**And** 触发任务继续执行

### Story 5.5: 确认后执行

As a **系统**,
I want **在获得用户确认后开始执行任务**,
So that **确保执行符合用户期望**.

**Acceptance Criteria:**

**Given** 澄清问题已回答
**When** 系统准备执行
**Then** 将用户回答合并到任务上下文
**And** 执行任务（调用 LLM）
**And** 记录澄清过程到日志

### Story 5.6: 跳过澄清（高信任模式）

As a **用户**,
I want **跳过澄清直接执行任务**,
So that **简单任务能快速完成**.

**Acceptance Criteria:**

**Given** 澄清问题已展示
**When** 用户选择跳过
**Then** 直接进入执行阶段
**And** 任务文件标记 skip_clarification: true
**And** 支持全局配置默认跳过澄清

---

## Epic 6: 执行透明度（日志与追踪）

**Goal:** 用户可以查看任务执行的完整历史和详情

**FRs covered:** FR22, FR23, FR24, FR25

### Story 6.1: JSON Lines 日志基础设施

As a **系统**,
I want **建立 JSON Lines 格式的日志系统**,
So that **所有事件能被结构化记录和查询**.

**Acceptance Criteria:**

**Given** 系统运行
**When** 任何事件发生
**Then** 写入 logs/ 目录的 .jsonl 文件
**And** 每行包含 ts, level, module, event 字段
**And** 日志写入异步/非阻塞

### Story 6.2: 任务执行日志记录

As a **系统**,
I want **记录每个任务的完整执行过程**,
So that **用户能追溯任务处理细节**.

**Acceptance Criteria:**

**Given** 任务开始执行
**When** 执行过程中
**Then** 记录任务开始事件
**And** 记录各阶段状态变更
**And** 记录任务完成或失败事件

### Story 6.3: LLM API 输入输出记录

As a **系统**,
I want **记录 LLM API 的请求和响应**,
So that **能调试和优化 AI 交互**.

**Acceptance Criteria:**

**Given** LLM API 调用
**When** 发送请求和接收响应
**Then** 记录请求的 messages 结构
**And** 记录响应内容和 token 用量
**And** API 密钥脱敏（只显示前4位）

### Story 6.4: 时间戳与耗时记录

As a **系统**,
I want **记录任务的时间信息**,
So that **能分析系统性能**.

**Acceptance Criteria:**

**Given** 任务执行
**When** 各阶段完成
**Then** 记录开始时间 (ISO 8601 格式)
**And** 记录结束时间
**And** 计算并记录总耗时（毫秒）

### Story 6.5: 日志查看命令

As a **用户**,
I want **执行 `ai-as-me logs` 查看执行日志**,
So that **我能了解任务执行历史**.

**Acceptance Criteria:**

**Given** 日志文件存在
**When** 执行 `ai-as-me logs`
**Then** 显示最近 N 条日志（默认 20）
**And** 支持 --task 参数过滤特定任务
**And** 支持 --level 参数过滤日志级别

### Story 6.6: 日志轮转与清理

As a **系统**,
I want **自动轮转和清理旧日志**,
So that **磁盘空间不会被耗尽**.

**Acceptance Criteria:**

**Given** 日志文件持续增长
**When** 单文件超过 10MB
**Then** 创建新日志文件
**And** 旧文件重命名带时间戳
**And** 删除超过 7 天的日志文件

---

## Epic 7: 自进化循环

**Goal:** 用户看到 AI 从经验中学习，规则库自动积累

**FRs covered:** FR26, FR27, FR28, FR29, FR30, FR31, FR34

### Story 7.1: 反思命令触发

As a **用户**,
I want **执行 `ai-as-me reflect` 手动触发反思**,
So that **AI 能分析已完成任务并提炼规则**.

**Acceptance Criteria:**

**Given** done 目录包含已完成任务
**When** 执行 `ai-as-me reflect`
**Then** 开始反思分析流程
**And** 显示正在分析的任务数量
**And** 支持 --last N 参数限制分析范围

### Story 7.2: 任务日志分析

As a **系统**,
I want **分析已完成任务的执行日志**,
So that **能识别潜在的决策模式**.

**Acceptance Criteria:**

**Given** 反思流程启动
**When** 加载任务日志
**Then** 提取任务输入、输出和上下文
**And** 识别重复出现的决策场景
**And** 汇总分析结果

### Story 7.3: 潜在规则提取

As a **系统**,
I want **从任务分析中提取潜在的新规则**,
So that **AI 能学习用户的决策偏好**.

**Acceptance Criteria:**

**Given** 任务分析完成
**When** 调用 LLM 进行规则提取
**Then** 识别可泛化的决策模式
**And** 生成规则描述（If-Then 格式）
**And** 评估规则的置信度

### Story 7.4: 建议规则展示

As a **用户**,
I want **看到系统建议的新规则**,
So that **我能决定是否采纳**.

**Acceptance Criteria:**

**Given** 潜在规则已提取
**When** 展示给用户
**Then** 显示规则内容和来源任务
**And** 显示置信度评分
**And** 提示用户确认或拒绝

### Story 7.5: 规则确认与拒绝

As a **用户**,
I want **确认或拒绝建议的规则**,
So that **只有我认可的规则被采纳**.

**Acceptance Criteria:**

**Given** 建议规则已展示
**When** 用户做出选择
**Then** 确认的规则标记为待写入
**And** 拒绝的规则标记为已忽略
**And** 支持修改规则文本后确认

### Story 7.6: 规则写入 rules.md

As a **系统**,
I want **将确认的规则写入 rules.md**,
So that **规则库持续积累**.

**Acceptance Criteria:**

**Given** 规则被用户确认
**When** 写入规则
**Then** 追加到 rules.md 文件
**And** 添加来源标注（日期、任务）
**And** 保持规则格式一致

### Story 7.7: 规则应用验证

As a **系统**,
I want **在后续任务中应用已积累的规则**,
So that **AI 行为持续进化**.

**Acceptance Criteria:**

**Given** rules.md 包含规则
**When** 执行新任务
**Then** 规则作为决策约束注入 LLM
**And** 任务输出符合已定义规则
**And** 日志记录应用的规则

---

## Summary

| Epic | Stories | FRs Covered |
|------|---------|-------------|
| Epic 1: 系统基础与 CLI | 7 | FR32, FR33, FR35, FR36, FR37, FR38, FR39, FR40 |
| Epic 2: 灵魂注入系统 | 6 | FR6, FR7, FR8, FR9, FR10 |
| Epic 3: 任务管理看板 | 6 | FR1, FR2, FR3, FR4, FR5 |
| Epic 4: LLM 驱动的任务执行 | 7 | FR11, FR12, FR13, FR14, FR15, FR16 |
| Epic 5: 混合式澄清 | 6 | FR17, FR18, FR19, FR20, FR21 |
| Epic 6: 执行透明度 | 6 | FR22, FR23, FR24, FR25 |
| Epic 7: 自进化循环 | 7 | FR26, FR27, FR28, FR29, FR30, FR31, FR34 |
| **Total** | **45** | **40 FRs (100% coverage)** |

