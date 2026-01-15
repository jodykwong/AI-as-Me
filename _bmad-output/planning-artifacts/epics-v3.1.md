---
stepsCompleted: [1, 2, 3, 4, 5]
inputDocuments:
  - '_bmad-output/planning-artifacts/prd-v3.1.md'
  - '_bmad-output/planning-artifacts/architecture-v3.1.md'
  - '_bmad-output/planning-artifacts/ux-design-specification-v3.1.md'
version: 'v3.1'
status: 'complete'
completedAt: '2026-01-15'
totalEpics: 3
totalStories: 9
---

# Epics & Stories - AI-as-Me v3.1

**Author:** Jody  
**Date:** 2026-01-15  
**Version:** v3.1

---

## Epic Overview

| Epic | 名称 | Stories | 优先级 | 预估 |
|------|------|---------|--------|------|
| E1 | 首次进化示例 | 3 | P0 | 3-4 天 |
| E2 | 规则冲突检测 | 3 | P0 | 2-3 天 |
| E3 | 增强进化统计 | 3 | P0 | 3-4 天 |

**总计：** 3 Epics, 9 Stories

---

## Epic 1: 首次进化示例 (First Evolution Demo)

**目标：** 让新用户在 5 分钟内看到 AI 自己生成规则，建立对系统的信心

**用户价值：** 降低体验门槛，快速展示"AI 养蛊"核心能力

**依赖：** v3.0 Evolution Engine

### Story 1.1: Demo 命令实现

**作为** 新用户  
**我想要** 运行一个简单的命令启动首次进化 Demo  
**以便** 快速体验 AI 自我进化能力

**验收标准：**
- [ ] CLI 命令 `ai-as-me demo first-evolution` 可执行
- [ ] 命令启动后显示欢迎信息和预计时间
- [ ] 支持 `--help` 显示使用说明
- [ ] 错误时显示友好提示和重试选项

**技术说明：**
- 新增 `src/ai_as_me/demo/first_evolution.py`
- 在 `cli_main.py` 注册 `demo` 子命令
- 调用 Evolution Engine 现有接口

**测试：**
- [ ] 单元测试：命令解析
- [ ] 集成测试：完整 Demo 流程

---

### Story 1.2: 示例任务与进度展示

**作为** 新用户  
**我想要** 看到 Demo 执行的实时进度  
**以便** 理解进化闭环的完整流程

**验收标准：**
- [ ] 执行内置示例任务：检查 requirements.txt
- [ ] 显示 5 个步骤的实时进度：
  1. 执行示例任务 ✓
  2. 收集经验 ✓
  3. 识别模式 ⏳
  4. 生成规则
  5. 写入 Soul
- [ ] 每步显示当前操作和进度百分比
- [ ] 步骤完成时显示绿色勾

**技术说明：**
- 新增 `src/ai_as_me/demo/sample_task.py`
- 新增 `src/ai_as_me/demo/progress_tracker.py`
- 使用 Rich 库实现终端进度条

**测试：**
- [ ] 单元测试：进度追踪器
- [ ] 集成测试：示例任务执行

---

### Story 1.3: 完成摘要与引导

**作为** 新用户  
**我想要** Demo 完成后看到清晰的摘要和下一步引导  
**以便** 知道 AI 学会了什么以及如何继续

**验收标准：**
- [ ] 显示生成的规则文件路径
- [ ] 显示规则内容摘要
- [ ] 提供"查看规则文件"的命令提示
- [ ] 提供"查看进化统计"的命令提示
- [ ] 提供"运行更多任务"的引导

**技术说明：**
- 在 `first_evolution.py` 中添加完成处理
- 生成规则到 `soul/rules/learned/python-dependency-check.md`

**测试：**
- [ ] 集成测试：完整 Demo 流程端到端

---

## Epic 2: 规则冲突检测 (Rule Conflict Detection)

**目标：** 确保 core rules 与 learned rules 不冲突，系统行为可预测

**用户价值：** 系统稳定可控，用户敢于启用进化功能

**依赖：** v3.0 Soul Loader

### Story 2.1: 冲突检测器实现

**作为** 持续使用者  
**我想要** 系统能自动检测规则冲突  
**以便** 避免 AI 生成的规则破坏系统

**验收标准：**
- [ ] 扫描 `soul/rules/core/` 和 `soul/rules/learned/`
- [ ] 检测直接矛盾（learned 说"用 A"，core 说"禁止 A"）
- [ ] 检测优先级覆盖（learned 覆盖 core 的关键规则）
- [ ] 返回冲突列表，包含冲突类型和涉及规则

**技术说明：**
- 新增 `src/ai_as_me/soul/conflict_detector.py`
- 使用 LLM 辅助语义冲突检测
- 支持关键词匹配作为快速检测

**测试：**
- [ ] 单元测试：各种冲突类型检测
- [ ] 集成测试：真实规则文件扫描

---

### Story 2.2: CLI 命令与自动扫描

**作为** 持续使用者  
**我想要** 通过命令检查冲突，并在启动时自动扫描  
**以便** 及时发现和处理冲突

**验收标准：**
- [ ] CLI 命令 `ai-as-me soul check-conflicts` 可执行
- [ ] 显示冲突列表和详情
- [ ] 系统启动时自动扫描（可配置）
- [ ] 发现冲突时显示警告

**技术说明：**
- 在 `cli_main.py` 注册 `soul check-conflicts` 子命令
- 在 Agent 初始化时调用冲突检测

**测试：**
- [ ] 单元测试：命令解析
- [ ] 集成测试：启动时自动扫描

---

### Story 2.3: 冲突处理与日志

**作为** 持续使用者  
**我想要** 系统能自动处理冲突并记录日志  
**以便** 确保系统稳定且可审计

**验收标准：**
- [ ] 自动降低 learned rule 优先级（core 优先）
- [ ] 记录冲突到 `logs/rule-conflicts.jsonl`
- [ ] 日志包含：时间戳、冲突类型、涉及规则、处理方式
- [ ] 支持手动处理选项（CLI 交互）

**技术说明：**
- 新增 `src/ai_as_me/soul/conflict_resolver.py`
- JSON Lines 格式日志

**测试：**
- [ ] 单元测试：冲突处理逻辑
- [ ] 集成测试：日志记录

---

## Epic 3: 增强进化统计 (Enhanced Evolution Stats)

**目标：** 量化进化效果，让用户能基于数据管理规则

**用户价值：** 数据驱动决策，证明进化机制的价值

**依赖：** v3.0 Evolution Logger

### Story 3.1: 统计计算器实现

**作为** 持续使用者  
**我想要** 看到规则的应用频率和有效性  
**以便** 判断哪些规则有用、哪些无效

**验收标准：**
- [ ] 计算规则应用频率（次/天）
- [ ] 计算规则有效性评分（应用后成功率变化）
- [ ] 计算模式识别准确率（模式→规则转化率）
- [ ] 支持按时间范围筛选

**技术说明：**
- 新增 `src/ai_as_me/stats/calculator.py`
- 从 `logs/evolution.jsonl` 读取数据
- 从 `experience/` 读取任务结果

**测试：**
- [ ] 单元测试：各统计维度计算
- [ ] 集成测试：真实数据计算

---

### Story 3.2: CLI 命令增强

**作为** 开发者  
**我想要** 通过命令查看详细统计  
**以便** 验证算法改进效果

**验收标准：**
- [ ] `ai-as-me evolve stats` - 基础统计概览
- [ ] `ai-as-me evolve stats --detailed` - 详细统计
- [ ] `ai-as-me evolve stats --rule <name>` - 单条规则统计
- [ ] `ai-as-me evolve stats --days <n>` - 时间范围筛选
- [ ] 支持 JSON 输出格式 `--format json`

**技术说明：**
- 增强 `cli_main.py` 中的 `evolve stats` 命令
- 添加新参数支持

**测试：**
- [ ] 单元测试：命令参数解析
- [ ] 集成测试：各种查询场景

---

### Story 3.3: Dashboard 可视化

**作为** 持续使用者  
**我想要** 在 Dashboard 看到进化统计图表  
**以便** 直观了解进化效果

**验收标准：**
- [ ] 进化统计 Dashboard 页面
- [ ] 规则应用热力图
- [ ] 有效性趋势图
- [ ] 进化时间线
- [ ] 支持刷新和导出

**技术说明：**
- 新增 `src/ai_as_me/stats/visualizer.py`（后端）
- 新增前端组件：
  - `<StatsHeatmap />`
  - `<EffectivenessTrend />`
  - `<EvolutionTimeline />`
- 使用 Recharts 图表库

**测试：**
- [ ] 单元测试：数据转换
- [ ] E2E 测试：Dashboard 页面

---

## Implementation Order

**Week 1:**
1. Story 1.1: Demo 命令实现
2. Story 1.2: 示例任务与进度展示
3. Story 1.3: 完成摘要与引导
4. Story 2.1: 冲突检测器实现

**Week 2:**
5. Story 2.2: CLI 命令与自动扫描
6. Story 2.3: 冲突处理与日志
7. Story 3.1: 统计计算器实现
8. Story 3.2: CLI 命令增强
9. Story 3.3: Dashboard 可视化

---

## Definition of Done

**每个 Story 完成标准：**
- [ ] 代码实现完成
- [ ] 单元测试通过
- [ ] 集成测试通过
- [ ] 代码评审通过
- [ ] 文档更新（如需要）

**每个 Epic 完成标准：**
- [ ] 所有 Stories 完成
- [ ] E2E 测试通过
- [ ] 用户验收测试通过

**v3.1 发布标准：**
- [ ] 所有 Epics 完成
- [ ] 性能测试通过
- [ ] 安全审查通过
- [ ] Release Notes 完成
- [ ] 文档更新完成
