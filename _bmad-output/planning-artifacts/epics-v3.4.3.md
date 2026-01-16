# Epics: AI-as-Me v3.4.3

**版本**: v3.4.3  
**主题**: 统一 Dashboard + Vibe-Kanban 重构

---

## Epic 1: Vibe-Kanban 任务系统

### 目标
实现符合 vibe-kanban 理念的任务管理系统，使用 Markdown 文件存储，支持任务澄清流程。

### Stories

#### Story 1.1: Task 模型
**描述**: 创建 Pydantic 任务模型，支持 Markdown 序列化/反序列化

**验收标准**:
- [ ] Task 模型包含所有必要字段
- [ ] to_markdown() 生成标准格式
- [ ] from_markdown() 正确解析

**文件**: `src/ai_as_me/kanban/models.py`

---

#### Story 1.2: VibeKanbanManager
**描述**: 实现 Markdown 文件管理器

**验收标准**:
- [ ] create_task() 在 inbox/ 创建 .md 文件
- [ ] get_task() 读取并解析任务
- [ ] list_tasks() 列出指定状态任务
- [ ] delete_task() 删除任务文件

**文件**: `src/ai_as_me/kanban/vibe_manager.py`

---

#### Story 1.3: 任务澄清
**描述**: 实现任务澄清功能

**验收标准**:
- [ ] clarify_task() 更新任务澄清信息
- [ ] clarified 字段设为 true
- [ ] 更新 updated_at 时间戳

**文件**: `src/ai_as_me/kanban/vibe_manager.py`

---

#### Story 1.4: 状态流转
**描述**: 实现任务状态移动

**验收标准**:
- [ ] move_task() 移动文件到目标目录
- [ ] inbox→todo 检查 clarified=true
- [ ] 更新文件中的 status 字段

**文件**: `src/ai_as_me/kanban/vibe_manager.py`

---

#### Story 1.5: Kanban API
**描述**: 创建 Kanban REST API

**验收标准**:
- [ ] GET /api/kanban/board 返回看板数据
- [ ] POST /api/kanban/tasks 创建任务
- [ ] PUT /api/kanban/tasks/{id}/clarify 澄清任务
- [ ] PUT /api/kanban/tasks/{id}/move 移动任务

**文件**: `src/ai_as_me/dashboard/api/kanban.py`

---

## Epic 2: 统一 Web Dashboard

### 目标
整合所有功能到统一的 Web Dashboard，提供一站式管理界面。

### Stories

#### Story 2.1: 注册 Kanban API
**描述**: 在 app.py 中注册 Kanban 路由

**验收标准**:
- [ ] Kanban API 可通过 /api/kanban/* 访问
- [ ] 不影响现有 API

**文件**: `src/ai_as_me/dashboard/app.py`

---

#### Story 2.2: Kanban 看板页面
**描述**: 创建四列看板页面

**验收标准**:
- [ ] 显示 inbox/todo/doing/done 四列
- [ ] 每列显示对应任务卡片
- [ ] inbox 任务显示澄清按钮

**文件**: `src/ai_as_me/dashboard/static/kanban.html`

---

#### Story 2.3: 任务澄清弹窗
**描述**: 实现澄清表单弹窗

**验收标准**:
- [ ] 点击澄清按钮弹出表单
- [ ] 表单包含目标、验收标准等字段
- [ ] 提交后任务移动到 todo

**文件**: `src/ai_as_me/dashboard/static/kanban.html`, `js/kanban.js`

---

#### Story 2.4: Soul API
**描述**: 创建 Soul 状态 API

**验收标准**:
- [ ] GET /api/soul/status 返回完整状态
- [ ] 包含 profile、mission、规则统计

**文件**: `src/ai_as_me/dashboard/api/soul.py`

---

#### Story 2.5: Soul 状态页面
**描述**: 创建 Soul 状态展示页面

**验收标准**:
- [ ] 显示 profile 内容
- [ ] 显示 mission 内容
- [ ] 显示规则统计

**文件**: `src/ai_as_me/dashboard/static/soul.html`

---

#### Story 2.6: 统一首页
**描述**: 重构首页，整合所有功能入口

**验收标准**:
- [ ] 显示系统状态卡片
- [ ] 显示功能模块导航
- [ ] 显示快速操作按钮

**文件**: `src/ai_as_me/dashboard/static/index.html`

---

## Epic 3: 测试与文档

### Stories

#### Story 3.1: 单元测试
**描述**: 编写 Kanban 模块测试

**验收标准**:
- [ ] Task 模型测试
- [ ] VibeKanbanManager 测试
- [ ] 测试覆盖率 > 80%

**文件**: `tests/unit/test_vibe_kanban.py`

---

#### Story 3.2: 发布说明
**描述**: 编写 v3.4.3 发布说明

**验收标准**:
- [ ] 列出新功能
- [ ] 列出改进项
- [ ] 升级指南

**文件**: `RELEASE_NOTES_v3.4.3.md`

---

## 优先级排序

| 优先级 | Story | 依赖 |
|--------|-------|------|
| P0 | 1.1 Task 模型 | - |
| P0 | 1.2 VibeKanbanManager | 1.1 |
| P0 | 1.3 任务澄清 | 1.2 |
| P0 | 1.4 状态流转 | 1.2 |
| P0 | 1.5 Kanban API | 1.2, 1.3, 1.4 |
| P0 | 2.1 注册 API | 1.5 |
| P0 | 2.2 Kanban 页面 | 2.1 |
| P1 | 2.3 澄清弹窗 | 2.2 |
| P1 | 2.4 Soul API | - |
| P1 | 2.5 Soul 页面 | 2.4 |
| P1 | 2.6 统一首页 | 2.2 |
| P2 | 3.1 单元测试 | 1.* |
| P2 | 3.2 发布说明 | all |

---

## 估时汇总

| Epic | 估时 |
|------|------|
| Epic 1: Vibe-Kanban | 2h |
| Epic 2: Web Dashboard | 1.5h |
| Epic 3: 测试文档 | 0.5h |
| **总计** | **4h** |
