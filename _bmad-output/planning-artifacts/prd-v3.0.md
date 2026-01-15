---
stepsCompleted: ['step-01-init', 'step-02-discovery', 'step-03-success', 'step-04-journeys', 'step-05-domain', 'step-06-functional', 'step-07-nonfunctional', 'step-08-constraints', 'step-09-dependencies', 'step-10-risks', 'step-11-complete']
inputDocuments:
  - 'product-brief-AI-as-Me-2026-01-15.md'
  - '_bmad-output/project-context.md'
  - 'AI-as-Me_Project_Status_Report.md'
documentCounts:
  briefs: 1
  research: 0
  brainstorming: 0
  projectDocs: 1
  projectContext: 1
classification:
  projectType: 'developer_tool'
  domain: 'ai_ml'
  complexity: 'medium'
  projectContext: 'brownfield'
workflowType: 'prd'
version: 'v3.0'
status: 'complete'
completedAt: '2026-01-15'
---

# Product Requirements Document - AI-as-Me v3.0

**Author:** Jody
**Date:** 2026-01-15

## Success Criteria

### User Success

**核心成功指标：结果采纳率**

用户成功的定义：AI 分身产出的结果被用户直接采纳或仅需少量修改即可使用。

| 指标 | v2.x 目标 | v3.0 目标 | 优先级 | 衡量方式 |
|------|-----------|-----------|--------|---------|
| 结果采纳率 | >80% | **>85%** | P0 | 用户直接采纳或少量修改的任务占比 |
| 任务完成率 | >70% | **>75%** | P0 | kanban Done/Total |
| 人工干预率 | <30% | **<25%** | P1 | 需要用户介入的任务占比 |
| 规则库增长 | >20条/月 | **自动增长** | P1 | soul/rules/learned/ 新增规则数 |
| 时间节省 | >5小时/周 | **>8小时/周** | P2 | 用户自我估算 |

**v3.0 新增：进化能力指标**

| 指标 | 目标值 | 优先级 | 衡量方式 |
|------|--------|--------|---------|
| 自创规则数量 | >10条/月 | P0 | soul/rules/learned/ 新增规则 |
| 规则应用率 | >60% | P1 | 自创规则被实际使用的比例 |
| 模式识别准确率 | >70% | P1 | experience → pattern 的准确性 |
| 进化闭环完整率 | 100% | P0 | 每个任务都触发反思和学习 |

**情感成功标准：信任**

用户对 AI 分身产生信任感，愿意将重要任务交给它处理，不再需要反复检查每一个输出。

**"Aha!" 时刻**

- 发现 soul/rules/learned/ 自动积累了有价值的规则
- AI 自动应用之前学到的经验解决新问题
- 观察到 AI 的决策质量随时间提升

### Business Success

**当前阶段：产品验证优先**

| 阶段 | 目标 | 成功标准 |
|------|------|---------|
| 30天验证期 | 核心价值验证 | P0 指标全部达标 |
| 验证成功后 | 探索商业化 | 获得 5 个付费用户（预配置套件） |

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
- ✅ 进化日志可查询和追踪

**质量标准：**
- ✅ 所有 P0 功能测试通过
- ✅ 代码覆盖率 >80%
- ✅ 文档完整（README、API docs）

---

## User Journeys

### Journey 1: Jody 的日常使用旅程

**场景：** 日常开发任务的 AI 辅助执行

**用户：** Jody（主要用户 - 技术型单人 AI 创业者）

**旅程步骤：**

1. **创建任务**
   - Jody 在 `kanban/inbox/` 创建新任务文件
   - 描述任务目标和上下文
   - 设置优先级（P1/P2/P3）

2. **AI 自动处理**
   - AI 读取任务，检查 `soul/rules/` 是否有相关规则
   - 如果任务简单且有规则 → 直接执行
   - 如果任务复杂 → 调用 `skills/bmad/` 获取方法论支持
   - 如果需要澄清 → 请求 Jody 确认

3. **执行和记录**
   - AI 执行任务，生成结果
   - 执行过程记录到 `experience/successes/` 或 `experience/failures/`
   - 任务移动到 `kanban/done/`

4. **查看结果**
   - Jody 查看执行结果
   - 结果采纳率 >85% → 直接使用或少量修改
   - 结果不满意 → 提供反馈

5. **AI 自动学习（v3.0 核心）**
   - AI 自动触发反思机制
   - 从 `experience/` 识别模式
   - 生成新规则写入 `soul/rules/learned/`
   - 记录到进化日志

**关键时刻：**
- ✨ AI 直接执行复杂任务无需干预
- ✨ 发现 AI 自动应用了之前学到的规则
- ✨ 观察到 AI 决策质量随时间提升

---

### Journey 2: Jody 的进化观察旅程

**场景：** 监控和验证 AI 的自我进化能力

**用户：** Jody（主要用户）

**旅程步骤：**

1. **查看进化日志**
   - 打开 `logs/evolution.jsonl` 或通过 API
   - 查看最近的进化事件
   - 了解 AI 学到了什么

2. **审查新规则**
   - 查看 `soul/rules/learned/` 新增的规则
   - 阅读规则内容和来源
   - 理解规则的触发条件

3. **验证规则效果**
   - 观察新规则在实际任务中的应用
   - 检查规则应用率（>60%）
   - 评估规则对任务完成率的影响

4. **调整和优化**
   - 如果规则有问题 → 手动修改或删除
   - 如果规则有效 → 保留并观察
   - 提供反馈帮助 AI 改进

5. **观察长期改进**
   - 每周查看进化统计
   - 对比结果采纳率的提升
   - 验证"复利工程"效果

**关键时刻：**
- ✨ 发现 AI 自动生成了有价值的规则
- ✨ 观察到规则库持续增长
- ✨ 感受到 AI 越来越"懂我"

---

### Journey 3: 新用户的初始化旅程

**场景：** 首次部署和配置 AI-as-Me

**用户：** AI 养蛊方法论实践者（次要用户）

**旅程步骤：**

1. **系统部署**
   - 克隆仓库
   - 运行 `scripts/setup.sh`
   - 配置环境变量（API keys）

2. **Soul 配置**
   - 编辑 `soul/profile.md` - 定义 AI 人格
   - 编辑 `soul/rules/core/` - 设置核心规则
   - 编辑 `soul/mission.md` - 定义使命

3. **OpenCode 集成**
   - 配置 `.opencode/config.yaml`
   - 测试自定义命令
   - 验证 agent 加载

4. **第一个任务**
   - 创建简单测试任务
   - 观察 AI 执行过程
   - 验证基础功能

5. **进入日常使用**
   - 开始创建真实任务
   - 观察 AI 学习过程
   - 进入 Journey 1 循环

---

### Journey 4: 管理员的维护旅程

**场景：** 系统监控和优化

**用户：** 系统管理员/维护者

**旅程步骤：**

1. **健康检查**
   - 访问 `/api/health` 端点
   - 检查组件状态
   - 验证进化闭环运行

2. **规则库管理**
   - 查看 `soul/rules/learned/` 规则数量
   - 清理无效规则
   - 备份重要规则

3. **性能监控**
   - 查看 Skills 加载时间
   - 检查 LLM API 稳定性
   - 监控任务执行成功率

4. **日志分析**
   - 查看进化日志
   - 分析失败案例
   - 识别改进机会

5. **系统优化**
   - 调整配置参数
   - 更新 Soul 规则
   - 优化进化算法

---

## Domain Requirements

### AI/ML Domain Specifics

**领域特性：**
- AI Agent 系统开发
- 机器学习模式识别
- 自然语言处理（LLM 集成）
- 知识图谱和规则引擎

**领域复杂度：** Medium
- 无强监管要求（非医疗/金融）
- 技术复杂但无合规限制
- 开源友好

**关键领域考量：**

1. **LLM 依赖**
   - DeepSeek API 作为主要推理引擎
   - 需要处理 API 限流和错误
   - Token 成本优化

2. **模式识别**
   - 从执行历史中提取模式
   - 机器学习算法（可选）
   - 规则生成逻辑

3. **知识管理**
   - Soul 文件系统（Markdown）
   - Experience 数据库（JSON/SQLite）
   - 规则版本控制

4. **Agent 架构**
   - 反思循环（Reflection Loop）
   - 工具调用（Tool Calling）
   - 上下文管理

---

## Functional Requirements

### FR-1: 自创规则机制（P0）

**功能描述：** AI 能够自动生成规则并写入 soul/rules/learned/

**功能规格：**

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 规则生成 | 从 experience 识别模式并生成规则 | P0 |
| 规则写入 | 将规则写入 soul/rules/learned/ | P0 |
| 规则格式化 | 标准化规则格式（Markdown） | P0 |
| 来源追溯 | 记录规则来源（任务ID、时间戳） | P0 |

**验收标准：**
- [ ] AI 能自动生成规则
- [ ] 规则正确写入 learned/ 目录
- [ ] 规则格式符合标准
- [ ] 规则来源可追溯

**技术约束：**
- 规则文件格式：Markdown
- 规则命名：`{category}-{timestamp}.md`
- 权限：文件权限 644

---

### FR-2: 进化闭环（P0）

**功能描述：** 完整的 experience → pattern → rule 转化流程

**功能规格：**

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 经验记录 | 任务执行后自动记录到 experience/ | P0 |
| 模式识别 | 从 experience 识别可复用模式 | P0 |
| 规则生成 | 将模式转化为规则 | P0 |
| 规则应用 | 下次执行时自动加载和应用 | P0 |

**验收标准：**
- [ ] 每个任务都记录到 experience/
- [ ] 模式识别准确率 >70%
- [ ] 规则自动生成并应用
- [ ] 进化闭环完整率 100%

**技术约束：**
- Experience 格式：JSON Lines
- 模式识别：基于规则或简单 ML
- 触发时机：任务完成后自动

---

### FR-3: OpenCode 集成（P1）

**功能描述：** 完整的 OpenCode 配置和集成

**功能规格：**

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 配置文件 | .opencode/config.yaml | P1 |
| 自定义命令 | soul-check, evolve, bmad | P1 |
| Agent 定义 | 加载 soul 的 default agent | P1 |
| 测试验证 | 验证配置正确性 | P1 |

**验收标准：**
- [ ] config.yaml 配置正确
- [ ] 自定义命令可用
- [ ] agent 正确加载 soul
- [ ] 与 Claude Code 互补

---

### FR-4: Skills 架构（P1）

**功能描述：** Skills 调用接口和机制

**功能规格：**

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| SKILL.md 定义 | 定义 bmad/evolution skills | P1 |
| 触发条件 | 判断何时调用 skills | P1 |
| 动态加载 | 按需加载 skills 内容 | P1 |
| 结果反馈 | Skills 执行结果记录 | P1 |

**验收标准：**
- [ ] SKILL.md 格式规范
- [ ] 触发条件明确
- [ ] 加载时间 <2秒
- [ ] 调用成功率 >90%

---

### FR-5: Experience 目录（P1）

**功能描述：** 结构化存储执行经验

**功能规格：**

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 成功案例 | successes/ 目录 | P1 |
| 失败教训 | failures/ 目录 | P1 |
| 模式库 | patterns/ 目录 | P1 |
| 查询接口 | 支持检索和分析 | P1 |

**验收标准：**
- [ ] 目录结构完整
- [ ] 数据格式标准化
- [ ] 支持模式识别
- [ ] 可查询和检索

---

### FR-6: 进化日志（P1）

**功能描述：** 记录和追踪进化过程

**功能规格：**

| 子功能 | 描述 | 优先级 |
|--------|------|--------|
| 日志记录 | 每次进化都记录 | P1 |
| 日志格式 | JSON Lines 或 Markdown | P1 |
| 查询接口 | 支持日志查询 | P1 |
| 状态追踪 | 规则状态（建议/已采纳/已拒绝） | P1 |

**验收标准：**
- [ ] 每次进化都记录
- [ ] 日志可查询
- [ ] 支持状态追踪
- [ ] 可视化展示（可选）

---

## Non-Functional Requirements

### NFR-1: 性能要求

| 指标 | 目标 | 说明 |
|------|------|------|
| Skills 加载时间 | <2秒 | 动态加载性能 |
| 规则应用延迟 | <100ms | 规则加载和匹配 |
| 模式识别时间 | <5秒 | 单次模式识别 |
| API 响应时间 | <200ms | Web Dashboard API |

### NFR-2: 可靠性要求

| 指标 | 目标 | 说明 |
|------|------|------|
| 进化闭环稳定性 | >95% | 转化成功率 |
| LLM API 稳定性 | >95% | 含重试机制 |
| 任务执行无阻塞 | >90% | 不因技术问题中断 |
| Soul 文件加载 | 100% | 必须成功加载 |

### NFR-3: 可维护性要求

- 代码覆盖率 >80%
- 类型注解覆盖率 >80%
- API 文档完整度 100%
- 所有配置文件有注释

### NFR-4: 安全性要求

- API 密钥只从环境变量读取
- Soul 文件权限 600
- 日志不包含敏感信息
- 规则写入需要验证

---

## Technical Constraints

### 技术栈约束

| 技术 | 版本 | 约束 |
|------|------|------|
| Python | ≥3.9 | 运行时要求 |
| FastAPI | latest | Web 框架 |
| SQLite | ≥3.35 | 数据库 |
| ChromaDB | latest | RAG 向量库 |

### 平台约束

- 主要平台：Linux (Ubuntu/Debian)
- 可选平台：macOS, RDK X5
- 不支持：Windows（暂时）

### 集成约束

- LLM API：DeepSeek（主要）
- 工具集成：OpenCode + Claude Code
- 版本控制：Git

---

## Dependencies

### 外部依赖

| 依赖 | 类型 | 关键程度 |
|------|------|----------|
| DeepSeek API | LLM 服务 | 关键 |
| OpenCode | AI 工具 | 重要 |
| Claude Code | AI 工具 | 重要 |
| _bmad/ | 方法论 | 重要 |

### 内部依赖

| 模块 | 依赖模块 | 说明 |
|------|----------|------|
| 进化闭环 | Experience 目录 | 数据源 |
| 规则生成 | 模式识别 | 前置步骤 |
| Skills 调用 | Soul 系统 | 能力判断 |
| 进化日志 | 规则生成 | 记录对象 |

---

## Risks & Mitigation

### 技术风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| LLM API 不稳定 | 高 | 中 | 重试机制 + 降级方案 |
| 模式识别不准确 | 中 | 高 | 人工审核 + 持续优化 |
| 规则冲突 | 中 | 中 | 优先级机制 + 冲突检测 |
| 性能瓶颈 | 低 | 低 | 异步处理 + 缓存 |

### 产品风险

| 风险 | 影响 | 概率 | 缓解措施 |
|------|------|------|----------|
| 用户不信任 AI 生成的规则 | 高 | 中 | 透明化 + 人工审核 |
| 进化效果不明显 | 高 | 中 | 30天验证期 + 快速迭代 |
| 学习曲线陡峭 | 中 | 低 | 完善文档 + 示例 |

---

## Appendix

### 术语表

| 术语 | 定义 |
|------|------|
| Soul | AI 的人格和规则系统 |
| Experience | 执行历史和经验数据 |
| Skills | 外部能力模块 |
| 进化闭环 | experience → pattern → rule 的完整流程 |
| 自创规则 | AI 自动生成的规则 |

### 参考文档

- Product Brief: `product-brief-AI-as-Me-2026-01-15.md`
- 项目状态评审: `AI-as-Me_Project_Status_Report.md`
- 项目上下文: `_bmad-output/project-context.md`
- v2.3 PRD: `prd.md`

---

**文档状态：** 完成
**版本：** v3.0
**最后更新：** 2026-01-15


