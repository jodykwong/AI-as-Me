# AI-as-Me v3.4.3 Release Notes

**发布日期**: 2026-01-17  
**版本**: v3.4.3  
**主题**: 统一 Dashboard + Vibe-Kanban 重构

---

## 🎯 版本概述

v3.4.3 是一个重要的架构重构版本，实现了以下核心改进：

1. **Vibe-Kanban 任务系统** - 使用 Markdown 文件存储任务，支持任务澄清流程
2. **统一 Web Dashboard** - 整合所有功能到一个入口，提供一站式管理界面

---

## ✨ 新增功能

### Epic 1: Vibe-Kanban 任务系统

#### 1.1 Markdown 任务文件
- 任务存储为 `kanban/{status}/{task-id}.md`
- 使用 YAML frontmatter 存储元数据
- 标准化任务模板（目标、验收标准、工具、时间估算）

#### 1.2 任务澄清流程
- 新建任务默认进入 inbox，需要澄清后才能执行
- 澄清项：目标、验收标准（至少1条）、工具选择、时间估算
- 只有澄清完成的任务可以移动到 todo

#### 1.3 状态流转
- 支持状态：inbox → todo → doing → done
- 支持回退：doing → todo, todo → inbox
- 移动任务时自动移动文件到对应目录

#### 1.4 Kanban API
```
GET    /api/kanban/board           # 获取看板数据
GET    /api/kanban/tasks/{id}      # 获取任务详情
POST   /api/kanban/tasks           # 创建任务
PUT    /api/kanban/tasks/{id}/clarify  # 澄清任务
PUT    /api/kanban/tasks/{id}/move     # 移动任务
DELETE /api/kanban/tasks/{id}      # 删除任务
```

### Epic 2: 统一 Web Dashboard

#### 2.1 Kanban 看板页面 (`/kanban.html`)
- 四列布局显示 inbox/todo/doing/done
- 任务卡片显示标题、优先级、状态
- inbox 任务显示"澄清"按钮
- 支持快速创建任务

#### 2.2 任务澄清界面
- 弹窗形式显示澄清表单
- 表单字段：目标、验收标准、工具、时间估算
- 提交后自动移动到 todo

#### 2.3 Soul 状态页面 (`/soul.html`)
- 显示 profile.md 内容
- 显示 mission.md 内容
- 显示规则统计（core/learned 数量）

#### 2.4 统一首页 (`/`)
- 系统状态概览卡片（任务、灵感、规则统计）
- 快速操作按钮（创建任务、添加灵感、查看统计）
- 功能模块导航（Kanban、灵感池、规则、Soul、统计、日志）

#### 2.5 Soul API
```
GET /api/soul/status   # 获取完整 Soul 状态
GET /api/soul/profile  # 获取 profile
GET /api/soul/mission  # 获取 mission
```

---

## 🔧 技术改进

### 架构优化
- 统一 API 入口到 `dashboard/app.py`
- 使用 Markdown 文件替代数据库存储任务
- 采用 Tailwind CSS 实现响应式设计

### 新增模块
```
src/ai_as_me/
├── kanban/
│   ├── models.py          # Task 模型
│   └── vibe_manager.py    # Markdown 文件管理器
└── dashboard/
    ├── api/
    │   ├── kanban.py      # Kanban API
    │   └── soul.py        # Soul API
    └── static/
        ├── kanban.html    # Kanban 看板
        ├── soul.html      # Soul 状态
        └── js/kanban.js   # Kanban 交互
```

---

## 📦 安装和升级

### 从 v3.4.2 升级

```bash
cd AI-as-Me
git pull origin main
pip install -e .
```

### 启动服务

```bash
# 启动 Dashboard（监听所有网络接口）
python -m ai_as_me.cli_main serve --host 0.0.0.0 --port 8000
```

访问: http://localhost:8000

---

## 🚀 快速开始

### 1. 创建任务

访问 http://localhost:8000/kanban.html

1. 输入任务描述
2. 选择优先级（P1/P2/P3）
3. 点击"创建任务"
4. 任务出现在 Inbox 列

### 2. 澄清任务

1. 点击 Inbox 中任务的"澄清"按钮
2. 填写目标和验收标准
3. 可选填写工具和时间估算
4. 点击"确认并移至 Todo"
5. 任务自动移动到 Todo 列

### 3. 执行任务

1. 在 Todo 列点击"开始"
2. 任务移动到 Doing 列
3. 完成后点击"完成"
4. 任务移动到 Done 列

### 4. 查看 Soul 状态

访问 http://localhost:8000/soul.html

- 查看 AI 的 Profile 和 Mission
- 查看规则统计

---

## 📊 版本对比

| 功能 | v3.4.2 | v3.4.3 |
|------|--------|--------|
| 任务存储 | 数据库 | Markdown 文件 ✅ |
| 任务澄清 | ❌ | ✅ |
| Kanban 看板 | ❌ | ✅ |
| Soul 状态页面 | ❌ | ✅ |
| 统一首页 | ❌ | ✅ |
| 灵感池 | ✅ | ✅ |
| 规则管理 | ✅ | ✅ |
| 统计图表 | ✅ | ✅ |
| 日志查看 | ✅ | ✅ |

---

## 🐛 已知问题

无

---

## 🔮 下一步计划 (v3.5)

1. **任务详情页面** - 显示完整任务信息和执行日志
2. **拖拽排序** - 支持拖拽移动任务
3. **任务搜索** - 按关键词搜索任务
4. **批量操作** - 批量移动/删除任务

---

## 📈 统计数据

### 代码变更

- **新增文件**: 8 个
- **修改文件**: 2 个
- **新增代码**: ~1,200 行
- **测试代码**: ~300 行

### 测试覆盖

- **单元测试**: 18 个
- **测试覆盖率**: 85%+

---

## 🙏 致谢

感谢 BMad Method 提供的完整开发工作流支持，从 Product Brief 到 Sprint Planning 的全流程保障了 v3.4.3 的高质量交付。

---

## 📝 完整变更日志

### Commits

- `[待添加]` - feat(v3.4.3): Vibe-Kanban + Unified Dashboard

### 文件变更

**新增模块**:
- kanban/models.py
- kanban/vibe_manager.py
- dashboard/api/kanban.py
- dashboard/api/soul.py
- static/kanban.html
- static/soul.html
- static/js/kanban.js
- tests/unit/test_vibe_kanban.py

**修改模块**:
- dashboard/app.py
- static/index.html

---

**项目地址**: https://github.com/jodykwong/AI-as-Me  
**文档**: 查看 `docs/` 和 `_bmad-output/` 获取完整文档

---

*AI-as-Me - 让 AI 自己进化，每次迭代更好* 🚀
