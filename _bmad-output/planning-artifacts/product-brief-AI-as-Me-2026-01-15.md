---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - 'AI-as-Me_Project_Status_Report.md'
  - '_bmad-output/project-context.md'
  - 'docs/v2.0_iteration_plan.md'
date: 2026-01-15
author: Jody
version: v3.0
status: complete
---

# Product Brief: AI-as-Me v3.0

## Executive Summary

AI-as-Me v3.0 旨在实现项目的核心愿景：**让 AI 代理具有真正的自我进化能力**。

v2.3 虽然建立了完善的基础架构（任务管理、Web Dashboard、API），但缺少"AI 养蛊"方法论的核心机制——AI 无法将经验转化为自己的规则。v3.0 将补齐这一关键能力，实现从"AI-for-Me"到"AI-as-Me"的质变。

**核心目标：**
- 实现 AI 自创规则机制（soul/rules/learned/）
- 建立进化闭环（experience → pattern → rule）
- 完善能力补充机制（Skills 架构 + OpenCode 集成）
- 实现真正的"复利工程"

---

## Core Vision

### Problem Statement

**当前状态：** AI-as-Me v2.3 拥有完整的任务管理、Web 界面和 API，但存在致命缺陷：

1. **Soul 是只读的** - AI 无法将学到的经验固化为自己的规则，每次都是"从零开始"
2. **经验只用于检索** - Agentic RAG 只是"查过去"，不是"从过去成长"
3. **缺少进化闭环** - 没有 experience → pattern → rule 的自动转化机制
4. **能力补充不明确** - _bmad/ 方法论存在但调用逻辑不清晰
5. **工具集成不完整** - 缺少 OpenCode 配置，MVP 工具栈不完整

**本质问题：** 项目更像是"AI-for-Me"（AI 为我服务），而非"AI-as-Me"（AI 成为我）。

### Problem Impact

**对用户的影响：**
- AI 无法从历史中学习，重复犯同样的错误
- 每次任务执行都需要人工指导，无法自主改进
- 无法实现"复利工程"——每次迭代应该比上次更好
- 违背"AI 养蛊"核心理念——AI 应该能自己生成规则

**对项目的影响：**
- 核心愿景（自我进化）未实现，完成度仅 10%
- 与"AI 养蛊"方法论的承诺不符
- MVP 工具策略（OpenCode + Claude Code）不完整
- 无法作为 XLeRobot 等未来整合的"大脑"

### Why Existing Solutions Fall Short

**传统 AI 工具（Claude、Cursor、Copilot）：**
- ❌ 无个性化人格
- ❌ 无持久记忆
- ❌ 无自我进化能力
- ❌ 每次对话都是独立的

**AI-as-Me v2.3：**
- ✅ 有 Soul 人格系统（但静态）
- ✅ 有 RAG 记忆（但只检索不进化）
- ✅ 有任务管理（但无自主改进）
- ❌ **缺少核心：自我进化机制**

**差距：** 有"灵魂"的骨架，但缺少"进化"的血液。

### Proposed Solution

**v3.0 核心解决方案：**

#### 1. 自创规则机制（P0）
```
soul/
└── rules/
    ├── core/           # 人类定义的核心规则
    └── learned/        # 🆕 AI 自创的规则
        ├── task-patterns.md
        ├── tool-selection.md
        └── error-recovery.md
```

**机制：** AI 在任务执行后自动反思，识别模式，生成规则并写入 `learned/`

#### 2. 进化闭环（P0）
```
执行任务 → 记录到 experience/ → 模式识别 → 生成规则 → 写入 soul/rules/learned/ → 下次执行时加载
```

**关键：** 从"消费经验"到"生产能力"的闭环

#### 3. Skills 架构（P1）
```
skills/
├── bmad/
│   └── SKILL.md        # 封装 _bmad/ 调用接口
└── evolution/
    └── SKILL.md        # 封装进化逻辑
```

**机制：** 当 soul 能力不足时，动态调用外部 Skills 补充

#### 4. OpenCode 集成（P1）
```
.opencode/
├── config.yaml         # 全局配置
├── commands/           # 自定义命令
│   ├── soul-check.md
│   ├── evolve.md
│   └── bmad.md
└── agents/
    └── default.md      # 加载 soul 的 agent
```

**目标：** 补齐 MVP 工具栈（OpenCode + Claude Code）

#### 5. Experience 目录（P1）
```
experience/
├── successes/          # 成功案例
├── failures/           # 失败教训
└── patterns/           # 识别出的模式
```

**用途：** 为进化闭环提供数据源

### Key Differentiators

**v3.0 的独特优势：**

1. **唯一性** - 市面上唯一能"自己写规则"的个人 AI 代理系统
2. **方法论支撑** - "AI 养蛊"理念 + BMad Method 能力补充的完整实现
3. **技术优势** - OpenCode + Claude Code 双工具栈，Skills 原生支持
4. **复利工程** - 每次执行后自动变得更好，真正的"养蛊"
5. **开放架构** - Soul + Skills 分离，可扩展到 XLeRobot 等未来场景

**不可复制的优势：**
- 完整的"AI 养蛊"方法论实践
- 从 v2.0 到 v2.3 积累的 56 个 Stories 的经验
- BMad Method 的深度集成

---

## Target Users

### Primary User: 技术型单人 AI 创业者

**用户画像：**

**姓名：** Jody（项目创建者）
**角色：** AI 养蛊实践者、个人开发者、技术探索者
**背景：**
- 具备中高级编程能力（Python、系统架构）
- 对 AI Agent 系统有深入理解
- 需要身兼多职：商业分析、技术开发、项目管理
- 时间精力有限，需要 AI 真正"替自己打工"

**核心痛点：**
1. **时间精力有限** - 需要同时处理多个角色的工作
2. **现有 AI 工具不够智能** - 无持久记忆、不了解偏好、只能被动回应
3. **无法实现"复利工程"** - AI 不会从经验中学习和进化
4. **缺少真正的 AI 分身** - 需要一个能代表自己决策和行动的系统

**使用场景：**
- 日常开发任务的自动化执行
- 项目规划和架构设计
- 商业分析和市场调研
- 任务管理和进度追踪
- 知识积累和经验沉淀

**成功标准：**
- 结果采纳率 >80%（AI 产出可直接使用或少量修改）
- 任务完成率 >70%
- 人工干预率 <30%
- 每周节省 >5 小时时间
- 对 AI 分身产生信任感

**技术水平：**
- 熟悉命令行操作
- 理解 AI Agent 架构
- 能够编写和修改配置文件
- 可以阅读和理解 Python 代码

### Secondary Users: AI 养蛊方法论实践者

**用户画像：**

**角色：** 探索个人 AI 系统的开发者和技术爱好者
**背景：**
- 对"AI 养蛊"理念感兴趣
- 希望构建能自我进化的个人 AI 代理
- 具备一定的技术背景

**核心需求：**
- 学习和实践 AI Agent 设计模式
- 构建可控、可扩展的 AI 系统
- 实现个性化的 AI 助手

**使用场景：**
- 个人项目的 AI 辅助
- 知识管理和学习
- 技能积累和经验沉淀

### User Journey

**典型使用流程：**

1. **初始化阶段**
   - 部署 AI-as-Me 系统
   - 配置 Soul 文件（profile/rules/mission）
   - 设置 API 密钥和环境变量

2. **日常使用阶段**
   - 创建任务到 kanban/inbox/
   - AI 自动执行或请求澄清
   - 查看执行结果和日志
   - 确认或修改 AI 的输出

3. **进化阶段**（v3.0 新增）
   - AI 自动从执行中学习
   - 识别模式并生成新规则
   - 规则写入 soul/rules/learned/
   - 下次执行时自动应用新规则

4. **能力扩展阶段**
   - 遇到复杂任务时调用 Skills（如 BMad Method）
   - 执行结果记录到 experience/
   - 提取经验并固化为规则

**关键交互点：**
- 任务创建和管理（kanban 系统）
- 混合式澄清（简单任务直接执行，复杂任务先确认）
- 规则审查和确认（AI 建议规则，用户确认）
- 执行结果查看和反馈

---

## Success Metrics

### User Success Metrics

**核心指标：结果采纳率**

| 指标 | 目标值 | 优先级 | 衡量方式 |
|------|--------|--------|---------|
| 结果采纳率 | >85% | P0 | AI 产出可直接使用或少量修改的任务占比 |
| 任务完成率 | >75% | P0 | kanban Done/Total |
| 人工干预率 | <25% | P1 | 需要用户介入的任务占比 |
| 时间节省 | >8小时/周 | P2 | 用户自我估算 |

**v3.0 新增：进化能力指标**

| 指标 | 目标值 | 优先级 | 衡量方式 |
|------|--------|--------|---------|
| 自创规则数量 | >10条/月 | P0 | soul/rules/learned/ 新增规则 |
| 规则应用率 | >60% | P1 | 自创规则被实际使用的比例 |
| 模式识别准确率 | >70% | P1 | experience → pattern 的准确性 |
| 进化闭环完整率 | 100% | P0 | 每个任务都触发反思和学习 |

**Skills 调用指标**

| 指标 | 目标值 | 优先级 | 衡量方式 |
|------|--------|--------|---------|
| Skills 调用成功率 | >90% | P1 | bmad/evolution 调用成功 |
| 能力补充有效率 | >75% | P1 | Skills 调用后任务完成率 |

**情感成功标准：**
- 用户对 AI 分身产生信任感
- 愿意将重要任务交给 AI 处理
- 不再需要反复检查每一个输出

**"Aha!" 时刻：**
- 发现 soul/rules/learned/ 自动积累了有价值的规则
- AI 自动应用之前学到的经验解决新问题
- 观察到 AI 的决策质量随时间提升

### Business Success

**当前阶段：产品验证优先**

| 阶段 | 目标 | 成功标准 |
|------|------|---------|
| 30天验证期 | 核心价值验证 | P0 指标全部达标 |
| 验证成功后 | 探索商业化 | 获得 5 个付费用户 |

**30天验证期 Go/No-Go 决策：**

| 结果 | 判定 | 下一步 |
|------|------|--------|
| P0 指标全部达标 | ✅ Go | 进入 Phase 2，探索商业化 |
| P0 部分达标 | ⚠️ Iterate | 分析原因，迭代优化 |
| P0 未达标 | ❌ Pivot | 重新评估产品方向 |

**P0 验证标准：**
- 进化闭环正常运行（100%）
- 自创规则数量 >5条
- 结果采纳率 >80%
- 任务完成率 >70%

### Technical Success

| 指标 | 目标 | 说明 |
|------|------|------|
| OpenCode 集成成功率 | 100% | 配置正确加载和使用 |
| 进化闭环稳定性 | >95% | experience → rule 转化成功率 |
| Skills 加载时间 | <2秒 | 动态加载性能 |
| LLM API 稳定性 | >95% | DeepSeek 调用成功率（含重试） |
| 任务执行无阻塞 | >90% | 不因技术问题中断的任务占比 |
| Soul 文件加载 | 100% | profile/rules/mission 正确加载 |

### Measurable Outcomes

**v3.0 交付时的验收标准：**

**核心功能：**
- ✅ soul/rules/learned/ 目录创建并可写入
- ✅ experience/ 目录结构完整
- ✅ 进化闭环完整实现（task → experience → pattern → rule）
- ✅ skills/bmad/SKILL.md 创建并可调用
- ✅ .opencode/ 配置完整

**质量标准：**
- ✅ 所有 P0 功能测试通过
- ✅ 代码覆盖率 >80%
- ✅ 文档完整（README、API docs）

---

## Product Scope

### MVP - v3.0 核心范围

**交付时间：** 4-6 周
**核心目标：** 实现真正的自我进化能力

#### P0 - 核心缺失（必须完成）

**1. 自创规则机制**
```
soul/
└── rules/
    ├── core/           # 人类定义的核心规则
    └── learned/        # 🆕 AI 自创的规则
        ├── task-patterns.md
        ├── tool-selection.md
        └── error-recovery.md
```

**功能：**
- AI 在任务执行后自动反思
- 识别可复用的模式
- 生成规则并写入 `learned/`
- 下次执行时自动加载和应用

**验收标准：**
- ✅ learned/ 目录可写入
- ✅ 规则格式标准化
- ✅ 规则来源可追溯
- ✅ 规则自动加载生效

**2. 进化闭环**
```
experience/
├── successes/          # 成功案例
├── failures/           # 失败教训
└── patterns/           # 识别出的模式
```

**流程：**
```
执行任务 → 记录到 experience/ → 模式识别 → 生成规则 → 写入 soul/rules/learned/ → 下次执行时加载
```

**验收标准：**
- ✅ experience/ 目录结构完整
- ✅ 任务完成后自动记录
- ✅ 模式识别算法实现
- ✅ 规则生成逻辑完整
- ✅ 闭环完整率 100%

#### P1 - 逻辑完善（应该完成）

**3. OpenCode 集成**
```
.opencode/
├── config.yaml         # 全局配置
├── commands/           # 自定义命令
│   ├── soul-check.md   # 检查 soul 状态
│   ├── evolve.md       # 触发进化反思
│   └── bmad.md         # 调用 BMad Method
└── agents/
    └── default.md      # 加载 soul 的 agent
```

**验收标准：**
- ✅ config.yaml 配置正确
- ✅ 自定义命令可用
- ✅ agent 正确加载 soul
- ✅ 与 Claude Code 互补

**4. Skills 架构**
```
skills/
├── bmad/
│   └── SKILL.md        # 封装 _bmad/ 调用接口
└── evolution/
    └── SKILL.md        # 封装进化逻辑
```

**功能：**
- 定义 Skills 调用条件
- 封装 _bmad/ 方法论
- 动态加载机制
- 调用结果反馈

**验收标准：**
- ✅ SKILL.md 格式规范
- ✅ 调用条件明确
- ✅ 加载时间 <2秒
- ✅ 调用成功率 >90%

**5. Experience 目录**

**结构：**
- `successes/` - 成功案例（任务ID、执行过程、结果）
- `failures/` - 失败教训（错误类型、原因、解决方案）
- `patterns/` - 识别的模式（模式描述、出现频率、适用场景）

**验收标准：**
- ✅ 目录结构完整
- ✅ 数据格式标准化
- ✅ 支持模式识别
- ✅ 可查询和检索

**6. 进化日志**
```
logs/evolution.jsonl    # JSON Lines 格式
或
soul/evolution_log.md   # Markdown 格式
```

**内容：**
- 时间戳
- 触发任务
- 识别的模式
- 生成的规则
- 规则状态（建议/已采纳/已拒绝）
- 影响范围

**验收标准：**
- ✅ 每次进化都记录
- ✅ 日志可查询
- ✅ 支持状态追踪
- ✅ 可视化展示（可选）

### Post-MVP - 未来增强

**Phase 2（验证成功后）：**

**7. 灵感池机制**
- `kanban/exploration/` 或独立目录
- 闲时自主探索触发机制
- AI 自主提出改进提案

**8. 高级进化能力**
- 规则冲突检测和解决
- 规则优先级管理
- 规则版本控制和回滚
- A/B 测试规则效果

**9. XLeRobot 整合**
- voice skill 接口
- hardware skill 接口
- 具身 AI 能力

**10. Web Dashboard 增强**
- 进化历史可视化
- 规则管理界面
- 模式识别展示
- 实时进化监控

### Scope Boundaries

**In Scope（v3.0 必须有）：**
- ✅ AI 能自己写规则到 soul/rules/learned/
- ✅ 经验自动转化为规则（完整闭环）
- ✅ OpenCode 完整配置
- ✅ Skills 调用机制
- ✅ 进化日志和状态追踪

**Out of Scope（v3.0 不做）：**
- ❌ 灵感池（Phase 2）
- ❌ 规则冲突解决（Phase 2）
- ❌ XLeRobot 整合（Phase 2）
- ❌ Web Dashboard 重构（Phase 2）
- ❌ 多用户支持
- ❌ 云端部署

**Explicitly Not Doing（明确不做）：**
- ❌ 改变现有 v2.3 功能
- ❌ 重构已有代码（除非必要）
- ❌ 添加新的 AI 工具集成
- ❌ 性能优化（除非阻塞）

---
