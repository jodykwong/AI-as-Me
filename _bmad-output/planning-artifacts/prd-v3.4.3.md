# PRD: AI-as-Me v3.4.3

**版本**: v3.4.3  
**主题**: 统一 Dashboard + Vibe-Kanban 重构  
**日期**: 2026-01-17  
**状态**: Draft

---

## 1. 概述

### 1.1 背景
当前系统的任务管理使用数据库存储，不符合 vibe-kanban 的 Markdown 文件理念。同时 Web Dashboard 功能分散在两套 API 中，用户体验不统一。

### 1.2 目标
- 重构 Kanban 系统，使用 Markdown 文件存储任务
- 实现任务澄清流程，确保任务在执行前有明确定义
- 统一 Web Dashboard，提供一站式管理界面

---

## 2. 功能需求

### 2.1 Vibe-Kanban 任务系统

#### FR-1: Markdown 任务文件
- **FR-1.1**: 任务存储为 `kanban/{status}/{task-id}.md`
- **FR-1.2**: 任务文件包含 YAML frontmatter（id, status, priority, clarified）
- **FR-1.3**: 任务内容包含：描述、目标、验收标准、工具、时间估算、上下文

#### FR-2: 任务澄清流程
- **FR-2.1**: 新建任务默认进入 inbox，clarified=false
- **FR-2.2**: 澄清需填写：目标、验收标准（至少1条）
- **FR-2.3**: 澄清完成后 clarified=true
- **FR-2.4**: 只有 clarified=true 的任务可移动到 todo

#### FR-3: 状态流转
- **FR-3.1**: 支持状态：inbox → todo → doing → done
- **FR-3.2**: 支持回退：doing → todo, todo → inbox
- **FR-3.3**: 移动任务时自动移动文件到对应目录

### 2.2 统一 Web Dashboard

#### FR-4: API 统一
- **FR-4.1**: 所有 API 通过 dashboard/app.py 提供
- **FR-4.2**: Kanban API: /api/kanban/*
- **FR-4.3**: 保持现有 API 兼容（/api/inspirations, /api/rules 等）

#### FR-5: Kanban 看板页面
- **FR-5.1**: 四列布局显示 inbox/todo/doing/done
- **FR-5.2**: 每列显示任务卡片（标题、优先级、状态标签）
- **FR-5.3**: 点击任务显示详情
- **FR-5.4**: inbox 任务显示"澄清"按钮

#### FR-6: 任务澄清界面
- **FR-6.1**: 弹窗形式显示澄清表单
- **FR-6.2**: 表单字段：目标、验收标准、工具、时间估算
- **FR-6.3**: 提交后自动移动到 todo

#### FR-7: Soul 状态页面
- **FR-7.1**: 显示 profile.md 内容
- **FR-7.2**: 显示 mission.md 内容
- **FR-7.3**: 显示规则统计（core/learned 数量）

#### FR-8: 统一首页
- **FR-8.1**: 系统状态概览卡片
- **FR-8.2**: 各功能模块入口导航
- **FR-8.3**: 快速创建任务入口

---

## 3. 非功能需求

### NFR-1: 性能
- API 响应时间 < 100ms
- 页面加载时间 < 2s

### NFR-2: 兼容性
- 支持 Chrome, Firefox, Safari 最新版本
- 支持移动端访问（响应式）

### NFR-3: 可维护性
- 代码测试覆盖率 > 80%
- 遵循现有代码风格

---

## 4. 用户故事

### US-1: 创建任务
```
作为用户
我想要创建一个新任务
以便记录待办事项

验收标准：
- 输入任务描述后点击创建
- 任务出现在 inbox 列
- kanban/inbox/ 目录生成对应 .md 文件
```

### US-2: 澄清任务
```
作为用户
我想要澄清 inbox 中的任务
以便明确任务目标和验收标准

验收标准：
- 点击任务的"澄清"按钮
- 弹出澄清表单
- 填写目标和验收标准后提交
- 任务自动移动到 todo 列
```

### US-3: 查看看板
```
作为用户
我想要查看任务看板
以便了解所有任务的状态

验收标准：
- 访问 /kanban.html
- 看到四列：inbox/todo/doing/done
- 每列显示对应状态的任务
```

### US-4: 查看 Soul 状态
```
作为用户
我想要查看 AI 的 Soul 状态
以便了解 AI 的个性和规则

验收标准：
- 访问 /soul.html
- 显示 profile 和 mission
- 显示规则统计
```

---

## 5. 数据模型

### Task
```yaml
id: string          # 任务ID (task-YYYYMMDD-NNN)
title: string       # 任务标题
description: string # 任务描述
status: enum        # inbox|todo|doing|done
priority: enum      # P1|P2|P3
clarified: boolean  # 是否已澄清
clarification:
  goal: string              # 目标
  acceptance_criteria: list # 验收标准
  tool: string              # 工具选择
  time_estimate: string     # 时间估算
  context: string           # 上下文
created_at: datetime
updated_at: datetime
```

---

## 6. API 接口

### Kanban API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/kanban/board | 获取看板数据 |
| GET | /api/kanban/tasks/{id} | 获取任务详情 |
| POST | /api/kanban/tasks | 创建任务 |
| PUT | /api/kanban/tasks/{id}/clarify | 澄清任务 |
| PUT | /api/kanban/tasks/{id}/move | 移动任务 |
| DELETE | /api/kanban/tasks/{id} | 删除任务 |

### Soul API

| 方法 | 路径 | 说明 |
|------|------|------|
| GET | /api/soul/status | 获取 Soul 状态 |

---

## 7. 里程碑

| 阶段 | 内容 | 预计时间 |
|------|------|----------|
| M1 | Kanban 核心（模型+管理器+API） | 1.5h |
| M2 | Web 页面（kanban+soul+首页） | 1.5h |
| M3 | 测试与文档 | 0.5h |
