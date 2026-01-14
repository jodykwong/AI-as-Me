---
stepsCompleted: ["step-01-validate-prerequisites", "step-02-design-epics", "step-03-create-stories", "step-04-final-validation"]
inputDocuments: 
  - "v2.2-iteration-plan.md"
  - "code-review-v2.1.md"
  - "retrospective-v2.1.md"
workflowStatus: "completed"
completedAt: "2026-01-14T08:39:00+08:00"
---

# AI-as-Me v2.2 - Epic Breakdown

## Overview

v2.2 聚焦技术债务清理、性能优化和功能增强。

## Epic List

| Epic | 名称 | Stories | 预估 |
|------|------|---------|------|
| Epic 8 | 技术债务清理 | 4 | 2天 |
| Epic 9 | 性能优化 | 3 | 2天 |
| Epic 10 | 功能增强 | 4 | 3天 |

---

## Epic 8: 技术债务清理

处理 v2.1 Code Review 遗留的技术问题。

**FRs covered:** CR-M1, CR-M2, CR-M4, CR-L1
**预估工时:** 2天

### Story 8.1: SSE 前端重连机制

As a 用户,
I want SSE 连接断开后自动重连,
So that 我不会错过任务状态更新。

**Acceptance Criteria:**
- [ ] 连接断开后 3秒内自动重连
- [ ] 使用指数退避 (3s, 6s, 12s, max 30s)
- [ ] 显示连接状态指示器
- [ ] 重连成功后刷新任务列表

**Technical Notes:**
- 前端 JavaScript 实现
- 添加连接状态 UI 组件

---

### Story 8.2: 反馈权重持久化

As a 用户,
I want 我的反馈权重在重启后保留,
So that 系统能持续学习我的偏好。

**Acceptance Criteria:**
- [ ] 反馈权重存储到 SQLite
- [ ] 重启后自动加载权重
- [ ] 权重影响检索排序

**Technical Notes:**
- 新增 feedback_weights 表
- 修改 FeedbackLearner 类

---

### Story 8.3: 关键词预处理优化

As a 开发者,
I want 关键词列表预处理为小写,
So that 提升任务类型识别性能。

**Acceptance Criteria:**
- [ ] 关键词在初始化时转为小写
- [ ] 移除运行时 lower() 调用
- [ ] 性能测试验证提升

**Technical Notes:**
- 修改 TaskAnalyzer.KEYWORDS
- 类初始化时预处理

---

### Story 8.4: 类型注解完善

As a 开发者,
I want 代码有完整的类型注解,
So that IDE 提供更好的代码提示。

**Acceptance Criteria:**
- [ ] skill_matcher.py 完整类型注解
- [ ] retriever.py 完整类型注解
- [ ] api.py 完整类型注解
- [ ] mypy 检查通过

**Technical Notes:**
- 使用 Python 3.9+ 类型语法

---

## Epic 9: 性能优化

提升系统响应速度和资源利用率。

**预估工时:** 2天

### Story 9.1: 数据库连接池

As a 系统,
I want 使用数据库连接池,
So that 减少连接创建开销。

**Acceptance Criteria:**
- [ ] 使用连接池管理 SQLite 连接
- [ ] 配置最大连接数
- [ ] API 响应时间降低 >20%

**Technical Notes:**
- 使用 sqlite3 连接复用
- 或引入 SQLAlchemy

---

### Story 9.2: RAG 检索缓存

As a 系统,
I want 缓存常用检索结果,
So that 减少重复向量计算。

**Acceptance Criteria:**
- [ ] LRU 缓存检索结果
- [ ] 缓存命中率 >50%
- [ ] 检索响应时间降低 >30%

**Technical Notes:**
- 使用 functools.lru_cache
- 缓存大小可配置

---

### Story 9.3: 嵌入模型预加载

As a 系统,
I want 启动时预加载嵌入模型,
So that 首次检索不需要等待模型加载。

**Acceptance Criteria:**
- [ ] 应用启动时加载模型
- [ ] 首次检索响应 <500ms
- [ ] 模型加载状态可查询

**Technical Notes:**
- 修改 VectorStore 初始化
- 添加 warmup 机制

---

## Epic 10: 功能增强

扩展工具支持和用户体验。

**预估工时:** 3天

### Story 10.1: Gemini CLI 支持

As a 用户,
I want 系统支持 Gemini CLI,
So that 我有更多工具选择。

**Acceptance Criteria:**
- [ ] 配置文件支持 gemini_cli
- [ ] 工具选择算法包含 Gemini
- [ ] 健康检查包含 Gemini 状态

**Technical Notes:**
- 更新 agents.yaml
- 验证 npx 命令

---

### Story 10.2: Qwen Code 支持

As a 用户,
I want 系统支持 Qwen Code,
So that 我有更多工具选择。

**Acceptance Criteria:**
- [ ] 配置文件支持 qwen_code
- [ ] 工具选择算法包含 Qwen
- [ ] 健康检查包含 Qwen 状态

**Technical Notes:**
- 更新 agents.yaml
- 验证 npx 命令

---

### Story 10.3: Web 界面美化

As a 用户,
I want Web 界面更美观,
So that 使用体验更好。

**Acceptance Criteria:**
- [ ] 任务卡片样式优化
- [ ] 添加加载动画
- [ ] 响应式布局优化
- [ ] 深色模式支持

**Technical Notes:**
- Tailwind CSS 样式调整
- 添加 CSS 动画

---

### Story 10.4: BMAD 技能扩展基础

As a 用户,
I want 系统能检测能力缺口,
So that 未来可以动态加载 BMAD 技能。

**Acceptance Criteria:**
- [ ] 能力缺口检测机制
- [ ] 技能包加载接口定义
- [ ] 基础框架实现

**Technical Notes:**
- 设计扩展接口
- 预留 BMAD 集成点

---

## Summary

### Story 统计

| Epic | Stories | P1 | P2 | P3 |
|------|---------|----|----|-----|
| Epic 8 | 4 | 2 | 1 | 1 |
| Epic 9 | 3 | 0 | 3 | 0 |
| Epic 10 | 4 | 0 | 3 | 1 |
| **Total** | **11** | **2** | **7** | **2** |

### 实施顺序

```
Week 1:
├── Day 1-2: Epic 8 (技术债务)
│   ├── 8.1 SSE 重连 (P1)
│   ├── 8.2 反馈持久化 (P1)
│   ├── 8.3 关键词优化 (P2)
│   └── 8.4 类型注解 (P3)
│
├── Day 3-4: Epic 9 (性能优化)
│   ├── 9.1 连接池 (P2)
│   ├── 9.2 RAG 缓存 (P2)
│   └── 9.3 模型预加载 (P2)
│
└── Day 5-7: Epic 10 (功能增强)
    ├── 10.1 Gemini CLI (P2)
    ├── 10.2 Qwen Code (P2)
    ├── 10.3 界面美化 (P3)
    └── 10.4 BMAD 基础 (P2)
```

### 依赖关系

```
Epic 8 (独立) ──┐
               ├──▶ Epic 10
Epic 9 (独立) ──┘
```
