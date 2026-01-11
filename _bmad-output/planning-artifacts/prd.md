---
stepsCompleted: [1, 2, 3, 4, 6, 7, 8, 9, 10, 11]
inputDocuments:
  - "product-brief-AI-as-Me-2026-01-10.md"
documentCounts:
  briefs: 1
  research: 0
  projectDocs: 0
  projectContext: 0
workflowType: 'prd'
lastStep: 11
skippedSteps: [5]
completedAt: '2026-01-10'
status: 'complete'
---

# Product Requirements Document - AI-as-Me

**Author:** Jody
**Date:** 2026-01-10

## Executive Summary

**AI-as-Me** 是一个开源的自进化 AI 数字分身系统，为技术型单人 AI 创业者打造一个能真正"替你打工"的智能伙伴。

**核心问题：** AI 创业者需要身兼多职（商业分析、技术开发、市场运营），但时间精力有限。现有 AI 工具无法真正替人工作——没有持久记忆、不了解用户偏好和决策风格、只能被动回应而非主动推进目标。

**解决方案：** 通过三大核心机制实现"越用越强"的 AI 分身：
1. **灵魂注入 (Soul Injection)** — 注入用户的履历、规则和使命
2. **Self-Evolution Loop（自进化循环）** — 任务执行 → 日志记录 → 反思总结 → 规则更新 → 持续进化
3. **混合式澄清 (Hybrid Clarification)** — 平衡自主性与可控性的智能交互模式

**优先部署平台：** RDK X5 机器人（XLeRobot），实现云端智能 + 物理执行的具身 AI。

### What Makes This Special

**核心差异化：卖结果，不卖工具**

AI-as-Me 不是又一个 AI 框架或工具集，而是聚焦于可衡量的价值交付：
- 每周完成 X 个任务
- 节省 Y 小时时间
- 结果采纳率 >80%

**关键差异点：**
| 差异化 | 说明 |
|--------|------|
| Self-Evolution Loop | 独创的自进化循环，让 AI 从经验中学习，越用越强 |
| 混合式澄清 | 简单任务直接执行，复杂任务先澄清，高风险必须审批 |
| 具身优先 | Day 1 即部署在 RDK X5，数字智能 + 物理执行 |
| 开源核心 | MIT/Apache 2.0 协议，社区友好，商业化通过预配置套件和企业支持 |

## Project Classification

**Technical Type:** `developer_tool` + `iot_embedded`
**Domain:** Scientific (AI/ML Agent System)
**Complexity:** Medium
**Project Context:** Greenfield — 全新项目

本项目是一个 AI Agent 开发框架，同时具备嵌入式硬件部署能力。属于 AI/ML 领域，复杂度中等（无强监管合规要求）。作为全新项目，将从零构建核心功能并在 RDK X5 平台上验证。

## Success Criteria

### User Success

**核心成功指标：结果采纳率 >80%**

用户成功的定义：AI 分身产出的结果（商业分析报告、市场调研等）被用户直接采纳或仅需少量修改即可使用。

| 指标 | 目标值 | 优先级 | 衡量方式 |
|------|--------|--------|---------|
| 结果采纳率 | >80% | P0 | 用户直接采纳或少量修改的任务占比 |
| 任务完成率 | >70% | P0 | 看板 Done/Total |
| 人工干预率 | <30% | P1 | 需要用户介入的任务占比 |
| 规则库增长 | >20 条/月 | P1 | rules.md 新增规则数 |
| 时间节省 | >5 小时/周 | P2 | 用户自我估算 |

**情感成功标准：信任**

用户对 AI 分身产生信任感，愿意将重要任务交给它处理，不再需要反复检查每一个输出。

**"Aha!"时刻**

用户发现规则库自动积累了有价值的经验法则——这是 Self-Evolution Loop 生效的直接证据，也是"越用越强"价值主张的具象化体现。

### Business Success

**当前阶段：产品验证优先**

| 阶段 | 目标 | 成功标准 |
|------|------|---------|
| 30天验证期 | 核心价值验证 | P0 指标全部达标 |
| 验证成功后 | 探索商业化 | 获得 **5 个付费用户**（预配置 RDK X5 套件） |

**商业模式验证逻辑：**
```
差异化（卖结果不卖工具）
    ↓
用户体验价值（高采纳率 + 信任 + 进化）
    ↓
用户愿意为预配置套件付费
    ↓
商业模式成立
```

### Technical Success

| 指标 | 目标 | 说明 |
|------|------|------|
| RDK X5 部署成功率 | 100% | Day 1 部署清单可复现 |
| LLM API 稳定性 | >95% | DeepSeek 调用成功率（含重试） |
| 任务执行无阻塞 | >90% | 不因技术问题中断的任务占比 |
| 灵魂文件加载 | 100% | profile/rules/mission 正确加载 |

### Measurable Outcomes

**30天验证期结束时的 Go/No-Go 决策：**

| 结果 | 判定 | 下一步 |
|------|------|--------|
| P0 指标全部达标 | ✅ Go | 进入 Phase 2，探索商业化 |
| P0 部分达标 | ⚠️ Iterate | 分析原因，迭代 MVP |
| P0 未达标 | ❌ Pivot | 重新评估产品方向 |

## Product Scope

### MVP - Minimum Viable Product

**4 周交付，验证核心价值**

| 模块 | 功能 | 说明 |
|------|------|------|
| 文件级看板 | 任务管理 | inbox/todo/doing/done 目录结构 |
| 任务执行引擎 | agent.py | 核心执行循环，调用 LLM API |
| 混合式澄清 | 智能交互 | MVP：全部先问用户确认 |
| 灵魂文件系统 | 个性化基础 | profile.md / rules.md / mission.md |
| 日志记录 | 执行追踪 | 任务执行过程的结构化记录 |
| 反思模块 V0.1 | 进化机制 | 手动触发反思 |
| 规则更新 | 知识积累 | 建议模式（AI 建议，用户确认写入）|
| XLeRobot 基础包 | 硬件支持 | RDK X5 环境部署 |

**第一个验证任务：** 使用 SmartFish-V1 项目进行市场调研

### Growth Features (Post-MVP)

**Phase 2 — 验证成功后**

| 功能 | 说明 |
|------|------|
| Web Dashboard | 可视化看板和系统状态 |
| n8n 集成 | 工作流自动化编排 |
| 反思模块 V0.2 | 自动反思（任务完成后自动执行）|
| 智能澄清 | 基于复杂度判断是否需要澄清 |
| 规则自动写入 | 移除人工确认步骤 |

### Vision (Future)

**Phase 3+ — 长期愿景**

| 功能 | 说明 |
|------|------|
| 机械臂控制 | SO-100 双臂控制集成 |
| 底盘控制 | 全向轮移动控制 |
| 多用户支持 | 团队协作功能 |
| 多机器人协作 | 多 RDK X5 设备协同 |

## User Journeys

### Journey 1: Jody Chen — 从"身兼多职"到"有人替我打工"

Jody 是一个单人 AI 创业者，手上有一个 SmartFish-V1 项目，他知道应该做市场调研来发现商业机会，但写代码、做运营、处理日常琐事已经占据了所有时间。每次想用 ChatGPT 帮忙分析，都要花 20 分钟解释项目背景、自己的偏好、想要的输出格式——然后下次还要再解释一遍。

一天晚上，Jody 在 GitHub 上发现了 AI-as-Me 项目，被"越用越强"的概念吸引。他决定在自己的 RDK X5 上试试。

**Day 1 部署：** Jody 按照部署清单，花了一个下午完成环境搭建。他上传了自己的"灵魂文件"——profile.md 记录了他的技术背景和做事风格，mission.md 写下了"通过 AI 产品帮助更多人"的使命。

**第一个任务：** Jody 在看板的 inbox 中创建了一个任务："用 SmartFish-V1 做市场调研，分析智能鱼缸市场的机会和竞争格局"。AI 分身读取任务后，先问了几个澄清问题：目标市场是国内还是海外？需要多深入的竞品分析？Jody 快速回答后，分身开始工作。

**惊喜时刻：** 第二天早上，Jody 看到 done 目录里的市场调研报告。报告不仅结构清晰，而且用词风格、分析角度都很像他自己会写的。他只改了两处细节就直接用了。这是他第一次觉得 AI 真的"懂他"。

**进化开始：** 一周后，Jody 查看 rules.md，发现分身自动积累了 8 条新规则："Jody 偏好数据驱动的分析而非纯定性描述"、"市场规模估算需要注明数据来源"、"竞品分析要包含技术栈对比"……这些都是他过去反复强调的偏好，现在分身记住了。

**新常态：** 一个月后，Jody 的工作节奏变了。早上花 10 分钟在看板部署任务，晚上审阅结果。商业分析从"没时间做"变成了"每周都有新产出"。他终于可以把 80% 的时间花在写代码上——这才是他真正热爱的事。

### Journey Requirements Summary

| 能力领域 | 需求来源 | MVP 必需 |
|---------|---------|---------|
| 部署体验 | Day 1 部署阶段 | ✅ |
| 任务管理 | 任务创建、状态流转 | ✅ |
| 智能交互 | 澄清问答、上下文理解 | ✅ |
| 执行引擎 | 任务执行、LLM 调用 | ✅ |
| 结果输出 | 结构化报告、风格一致性 | ✅ |
| 进化机制 | 规则提取、知识积累 | ✅ |

## Innovation & Novel Patterns

### Detected Innovation Areas

**核心创新：Self-Evolution Loop（自进化循环）**

AI-as-Me 的核心创新在于将"自我进化"机制产品化。与现有 AI 工具的关键区别：

| 维度 | 现有工具 | AI-as-Me |
|------|---------|----------|
| 记忆 | 会话级或无 | 永久规则库 |
| 学习 | 无或单任务内 | 跨任务积累 |
| 个性化 | 通用模型 | 用户专属规则 |
| 可解释性 | 黑盒 | rules.md 可读可编辑 |

**创新组合：**
- 灵魂注入（Soul Injection）+ 自进化循环（Self-Evolution Loop）+ 混合式澄清（Hybrid Clarification）

这三者的组合创造了一个"越用越懂你"的 AI 分身，而非"永远是新手"的工具。

### Market Context & Competitive Landscape

**相关先例：**
- **Voyager (NVIDIA)**: 在 Minecraft 中积累技能库，证明了"AI 技能积累"的可行性
- **Reflexion (MIT)**: 学术研究验证了"自我反思"能提升 Agent 性能
- **MemGPT**: 探索了 AI 长期记忆的工程实现

**市场空白：**
目前没有面向"个人 AI 助手"的产品化自进化系统。现有工具要么是通用框架（LangChain），要么缺乏学习机制（ChatGPT、Claude）。

### Validation Approach

**创新验证计划：**

| 验证点 | 方法 | 成功标准 |
|--------|------|---------|
| 规则提取有效性 | 30天后检查 rules.md 质量 | >20 条有价值规则 |
| 规则改进输出 | A/B 对比有无规则的输出 | 采纳率提升 >10% |
| 用户感知进化 | 用户反馈"分身变聪明了" | 定性确认 |

### Risk Mitigation

**创新风险与应对：**

| 风险 | 影响 | 应对策略 |
|------|------|---------|
| 规则提取质量差 | 进化失效 | Fallback: 手动规则整理 |
| 规则冲突/噪音 | 输出不稳定 | 规则优先级 + 人工审核 |
| 进化太慢 | 用户失去耐心 | 预置规则模板快速启动 |
| 隐私担忧 | 用户不愿分享偏好 | 本地存储，用户完全控制 |

## Developer Tool + IoT Embedded 特定需求

### Project-Type Overview

AI-as-Me 是一个混合型项目：
- **Developer Tool 属性**：Python 包、CLI 接口、可编程 API
- **IoT Embedded 属性**：部署在 RDK X5 边缘设备上，需要考虑硬件约束

### Hardware Requirements (RDK X5)

| 规格 | 详情 |
|------|------|
| 处理器 | D-Robotics Sunrise®5 智能计算芯片 |
| 存储 | Micro SD（≥16GB）+ eMMC + QSPI NAND |
| 连接 | WiFi（板载天线）+ 千兆以太网 + 4x USB 3.0 |
| 电源 | USB Type-C，5V/5A |
| GPIO | 40-pin（3.3V，可选 1.8V） |
| 摄像头 | 2x MIPI CSI（双摄支持） |

**运行要求：**
- 长时间稳定运行（24/7）
- WiFi 连接用于 LLM API 调用
- SD 卡存储灵魂文件、日志、规则库

### Installation & Deployment

**MVP 安装流程：**
```bash
# 1. 克隆仓库
git clone https://github.com/[user]/ai-as-me.git
cd ai-as-me

# 2. 运行部署脚本
./setup.sh  # 安装依赖、配置环境、验证硬件

# 3. 初始化灵魂文件
./init-soul.sh  # 创建 profile.md, rules.md, mission.md 模板
```

**未来规划（Phase 2+）：**
```bash
pip install ai-as-me
ai-as-me init
```

### API Surface

**MVP 接口设计：**

| 接口 | 类型 | 说明 | 优先级 |
|------|------|------|--------|
| `ai-as-me run` | CLI | 启动 Agent 主循环 | P0 |
| `ai-as-me status` | CLI | 查看当前任务状态 | P0 |
| `ai-as-me reflect` | CLI | 手动触发反思 | P0 |
| kanban/ 目录 | 文件 | inbox/todo/doing/done 任务管理 | P0 |
| soul/ 目录 | 文件 | profile.md, rules.md, mission.md | P0 |
| Python API | 代码 | `from ai_as_me import Agent` | P1 |

**核心目录结构：**
```
ai-as-me/
├── soul/
│   ├── profile.md      # 用户履历和风格
│   ├── rules.md        # 积累的规则
│   └── mission.md      # 使命和目标
├── kanban/
│   ├── inbox/          # 待处理任务
│   ├── todo/           # 已确认任务
│   ├── doing/          # 执行中任务
│   └── done/           # 已完成任务
├── logs/               # 执行日志
└── agent.py            # 核心执行引擎
```

### Security Model

**灵魂文件安全策略：**

| 层面 | 方案 | 优先级 |
|------|------|--------|
| 存储位置 | 本地存储，永不上云 | P0 |
| 文件权限 | `chmod 600`（仅用户可读写） | P0 |
| 数据所有权 | 用户完全控制，随时可删除 | P0 |
| 可选加密 | GPG 加密敏感规则 | P1 |
| API 密钥 | 环境变量或 .env 文件，不入库 | P0 |

### Update Mechanism

| 阶段 | 更新方式 | 说明 |
|------|---------|------|
| MVP | `git pull && ./setup.sh` | 手动更新，简单可靠 |
| Phase 2 | 版本检查 + 提示更新 | `ai-as-me update` 命令 |
| Phase 3 | 自动 OTA（可选） | 后台检查，用户确认后更新 |

### Connectivity Requirements

| 需求 | 说明 |
|------|------|
| WiFi | 用于 LLM API 调用（DeepSeek） |
| 离线模式 | MVP 不支持，需要网络连接 |
| 带宽 | 低带宽要求（文本为主） |
| 稳定性 | 需要处理网络中断和重试 |

### Implementation Considerations

**长时间运行优化：**
- 使用 systemd 服务管理 Agent 进程
- 日志轮转防止磁盘占满
- 内存泄漏监控
- 网络重连机制

**RDK X5 特定考虑：**
- 依赖 XLeRobot 基础包
- SD 卡 I/O 优化（减少写入频率）
- 温度监控（长时间运行）

## Project Scoping & Phased Development

### MVP Strategy & Philosophy

**MVP 类型：** Problem-Solving MVP（问题解决型）

**核心验证假设：**
1. AI 分身能产出高质量商业分析（采纳率 >80%）
2. Self-Evolution Loop 能有效积累规则（>20 条/月）
3. 用户愿意为"卖结果"付费（5 个付费用户）

**资源需求：**
- 团队规模：1 人（Jody 自己）
- 技能需求：Python、AI/ML、嵌入式基础
- 时间投入：4 周全职

### MVP Feature Set (Phase 1)

**核心用户旅程：** Jody — 从"身兼多职"到"有人替我打工"

**必须具备的能力：**

| 能力 | 模块 | 验收标准 |
|------|------|---------|
| 任务管理 | 文件级看板 | inbox → todo → doing → done 流转正常 |
| 任务执行 | agent.py | 能调用 LLM 完成商业分析任务 |
| 智能交互 | 混合式澄清 | 任务开始前能问澄清问题 |
| 个性化 | 灵魂文件系统 | 能加载 profile/rules/mission |
| 执行追踪 | 日志记录 | 任务过程有结构化记录 |
| 进化机制 | 反思模块 V0.1 | 手动触发能生成规则建议 |
| 规则积累 | 规则更新 | 用户确认后能写入 rules.md |
| 硬件支持 | XLeRobot 基础包 | RDK X5 环境部署成功 |

**第一个验证任务：** 使用 SmartFish-V1 项目进行市场调研

### Post-MVP Features

**Phase 2（验证成功后）：**

| 功能 | 价值 | 前置条件 |
|------|------|---------|
| Web Dashboard | 可视化操作 | MVP 核心稳定 |
| n8n 集成 | 工作流自动化 | 任务执行引擎成熟 |
| 反思模块 V0.2 | 自动反思 | 规则质量验证通过 |
| 智能澄清 | 减少人工干预 | 澄清模式验证有效 |
| 规则自动写入 | 更高自主性 | 用户信任度建立 |

**Phase 3（长期愿景）：**

| 功能 | 价值 | 依赖 |
|------|------|------|
| 机械臂控制 | 物理任务执行 | SO-100 集成 |
| 底盘控制 | 移动能力 | 全向轮驱动 |
| 多用户支持 | 团队协作 | 权限系统 |
| 多机器人协作 | 规模化 | 通信协议 |

### Risk Mitigation Strategy

**技术风险缓解：**
- LLM API：DeepSeek 主用 + 重试机制 + 超时处理
- 规则质量：手动整理 fallback + 预置模板
- 环境兼容：依赖 XLeRobot 验证配置

**市场风险验证：**
- 30 天验证期：P0 指标全部达标 → Go
- 用户信任：MVP 阶段全部先问后做
- 进化感知：定期展示规则库增长

**资源风险应对：**
- 最小 MVP：砍掉所有非核心功能
- 时间缓冲：4 周计划，预留 1 周 buffer
- 外部依赖：XLeRobot 已验证，降低硬件风险

## Functional Requirements

### 任务管理 (Task Management)

- **FR1:** 用户可以在 inbox 目录中创建新任务文件
- **FR2:** 用户可以查看当前所有任务的状态（inbox/todo/doing/done）
- **FR3:** 系统可以自动将任务从一个状态目录移动到另一个状态目录
- **FR4:** 用户可以手动移动任务到任意状态目录
- **FR5:** 用户可以在任务文件中定义任务描述、上下文和期望输出

### 灵魂文件系统 (Soul File System)

- **FR6:** 用户可以创建和编辑 profile.md 记录个人履历和风格
- **FR7:** 用户可以创建和编辑 rules.md 存储决策规则
- **FR8:** 用户可以创建和编辑 mission.md 定义使命和目标
- **FR9:** 系统可以在任务执行时加载所有灵魂文件作为上下文
- **FR10:** 用户可以查看当前规则库中的所有规则

### 任务执行 (Task Execution)

- **FR11:** 系统可以从 todo 目录读取任务并开始执行
- **FR12:** 系统可以调用 LLM API 处理任务内容
- **FR13:** 系统可以将灵魂文件内容作为系统提示注入 LLM
- **FR14:** 系统可以生成结构化的任务输出结果
- **FR15:** 系统可以将完成的任务和结果移动到 done 目录
- **FR16:** 系统可以处理 LLM API 调用失败并进行重试

### 混合式澄清 (Hybrid Clarification)

- **FR17:** 系统可以在执行任务前分析任务复杂度
- **FR18:** 系统可以生成澄清问题向用户确认需求
- **FR19:** 用户可以回答澄清问题提供额外上下文
- **FR20:** 系统可以在获得用户确认后开始执行任务
- **FR21:** 用户可以跳过澄清直接要求执行（高信任模式）

### 日志与追踪 (Logging & Tracking)

- **FR22:** 系统可以记录每个任务的执行过程日志
- **FR23:** 系统可以记录 LLM API 的输入和输出
- **FR24:** 用户可以查看任意任务的执行日志
- **FR25:** 系统可以记录任务的开始时间、结束时间和耗时

### 反思与进化 (Reflection & Evolution)

- **FR26:** 用户可以手动触发反思模块分析已完成任务
- **FR27:** 系统可以从任务日志中提取潜在的新规则
- **FR28:** 系统可以向用户展示建议的新规则
- **FR29:** 用户可以确认或拒绝建议的规则
- **FR30:** 系统可以将用户确认的规则写入 rules.md
- **FR31:** 系统可以在后续任务中应用已积累的规则

### 系统管理 (System Management)

- **FR32:** 用户可以通过 CLI 启动 Agent 主循环
- **FR33:** 用户可以通过 CLI 查看系统状态
- **FR34:** 用户可以通过 CLI 手动触发反思
- **FR35:** 用户可以配置 LLM API 密钥和端点
- **FR36:** 系统可以作为后台服务持续运行
- **FR37:** 用户可以通过 git pull 更新系统

### 硬件集成 (Hardware Integration)

- **FR38:** 系统可以在 RDK X5 硬件上部署和运行
- **FR39:** 系统可以通过 WiFi 连接访问 LLM API
- **FR40:** 系统可以使用 SD 卡存储所有数据文件

## Non-Functional Requirements

### Performance

| NFR | 指标 | 目标值 | 说明 |
|-----|------|--------|------|
| NFR1 | LLM API 响应时间 | <30 秒/请求 | 商业分析任务可接受的等待时间 |
| NFR2 | 任务状态流转 | <1 秒 | 文件移动操作即时完成 |
| NFR3 | 灵魂文件加载 | <2 秒 | 系统启动时加载所有配置 |
| NFR4 | 日志写入 | 异步/非阻塞 | 不影响主任务执行 |

### Security

| NFR | 要求 | 实现方式 |
|-----|------|---------|
| NFR5 | 灵魂文件权限 | `chmod 600`，仅用户可读写 |
| NFR6 | API 密钥保护 | 环境变量或 .env 文件，不入版本控制 |
| NFR7 | 数据本地化 | 所有用户数据仅存储在本地，永不上传云端 |
| NFR8 | 日志脱敏 | 日志中不记录完整 API 密钥 |

### Reliability

| NFR | 要求 | 目标值 |
|-----|------|--------|
| NFR9 | 系统可用性 | 24/7 长时间运行能力 |
| NFR10 | 网络中断恢复 | 断网后自动重连，重试间隔指数退避 |
| NFR11 | LLM API 重试 | 失败后最多重试 3 次 |
| NFR12 | 进程管理 | systemd 服务，崩溃后自动重启 |
| NFR13 | 磁盘空间 | 日志轮转，单文件 <10MB，保留最近 7 天 |

### Integration

| NFR | 要求 | 说明 |
|-----|------|------|
| NFR14 | LLM API 兼容 | 支持 DeepSeek API（OpenAI 兼容格式） |
| NFR15 | API 超时设置 | 请求超时 60 秒，连接超时 10 秒 |
| NFR16 | XLeRobot 依赖 | 兼容 XLeRobot 基础包版本 |
| NFR17 | Python 版本 | 支持 Python 3.9+ |

### Maintainability

| NFR | 要求 | 说明 |
|-----|------|------|
| NFR18 | 代码风格 | 遵循 PEP 8，使用 black 格式化 |
| NFR19 | 错误信息 | 用户友好的错误提示，包含解决建议 |
| NFR20 | 配置外部化 | 所有可配置项通过环境变量或配置文件 |
