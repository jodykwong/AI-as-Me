# Sprint Plan: AI-as-Me v3.4.3

**版本**: v3.4.3  
**Sprint 周期**: 2026-01-17  
**目标**: 统一 Dashboard + Vibe-Kanban 重构

---

## 🎯 Sprint 目标

1. ✅ 实现 Vibe-Kanban Markdown 任务系统
2. ✅ 实现任务澄清流程
3. ✅ 统一 Web Dashboard
4. ✅ 新增 Kanban 看板和 Soul 状态页面

---

## 📋 任务清单

### Phase 1: Kanban 核心 (P0)

| # | 任务 | 文件 | 估时 | 状态 |
|---|------|------|------|------|
| 1 | Task 模型 | kanban/models.py | 20m | ✅ |
| 2 | VibeKanbanManager | kanban/vibe_manager.py | 40m | ✅ |
| 3 | Kanban API | dashboard/api/kanban.py | 30m | ✅ |
| 4 | 注册路由 | dashboard/app.py | 10m | ✅ |

### Phase 2: Web 页面 (P0-P1)

| # | 任务 | 文件 | 估时 | 状态 |
|---|------|------|------|------|
| 5 | Kanban 页面 | static/kanban.html | 30m | ✅ |
| 6 | Kanban JS | static/js/kanban.js | 20m | ✅ |
| 7 | Soul API | dashboard/api/soul.py | 15m | ✅ |
| 8 | Soul 页面 | static/soul.html | 20m | ✅ |
| 9 | 首页重构 | static/index.html | 20m | ✅ |
| 10 | 样式更新 | static/css/style.css | 15m | ⬜ (使用 Tailwind) |

### Phase 3: 测试与文档 (P2)

| # | 任务 | 文件 | 估时 | 状态 |
|---|------|------|------|------|
| 11 | 单元测试 | tests/unit/test_vibe_kanban.py | 20m | ✅ |
| 12 | 发布说明 | RELEASE_NOTES_v3.4.3.md | 10m | ✅ |

---

## 🚀 执行顺序

```
Phase 1: Kanban 核心
├── 1. Task 模型
├── 2. VibeKanbanManager  
├── 3. Kanban API
└── 4. 注册路由

Phase 2: Web 页面
├── 5. Kanban 页面 + 6. JS
├── 7. Soul API + 8. Soul 页面
├── 9. 首页重构
└── 10. 样式更新

Phase 3: 收尾
├── 11. 单元测试
└── 12. 发布说明
```

---

## ✅ Definition of Done

- [x] 创建任务后文件出现在 kanban/inbox/*.md
- [x] 未澄清任务无法移动到 todo
- [x] /kanban.html 显示四列看板
- [x] /soul.html 显示 profile 和 mission
- [x] 首页显示所有功能入口
- [x] 所有测试通过 (12 passed)
- [ ] 代码推送到 GitHub

---

## 📊 估时汇总

| Phase | 估时 |
|-------|------|
| Phase 1 | 100m |
| Phase 2 | 120m |
| Phase 3 | 30m |
| **总计** | **250m (~4h)** |
