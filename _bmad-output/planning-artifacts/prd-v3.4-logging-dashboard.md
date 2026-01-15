# AI-as-Me v3.4 PRD - 日志系统 & Web Dashboard

**创建日期**: 2026-01-15  
**状态**: Draft

---

## 1. 概述

v3.4 完善系统可观测性和用户体验，通过日志系统和 Web Dashboard 让 AI 成长过程可见、可控。

---

## 2. 功能需求

### 2.1 日志系统增强

**FR-2.1.1: 统一日志格式**
```json
{
  "timestamp": "2026-01-15T21:00:00Z",
  "level": "INFO",
  "module": "inspiration.pool",
  "event": "inspiration_added",
  "data": {"id": "insp_001", "content": "..."}
}
```

**FR-2.1.2: 日志配置**
- 配置文件：`config/logging.yaml`
- 支持级别：DEBUG/INFO/WARNING/ERROR
- 输出目标：文件 + 控制台

**FR-2.1.3: 日志轮转**
- 单文件最大 10MB
- 保留最近 7 天
- 自动压缩归档

**FR-2.1.4: 日志查询 API**
```python
GET /api/logs?level=ERROR&module=agent&limit=100
```

### 2.2 Web Dashboard

**FR-2.2.1: 首页概览**
- 灵感池统计（总数、成熟数）
- 规则统计（Core/Learned）
- 最近进化事件（时间线）
- 系统健康状态

**FR-2.2.2: 灵感池页面**
- 灵感列表（分页、筛选）
- 成熟度热力图
  - X轴：创建时间（按天）
  - Y轴：来源类型（conversation/task/manual）
  - 颜色：成熟度（0-1，绿色→红色）
- 灵感详情弹窗
- 转化操作按钮

**FR-2.2.3: 规则管理页面**
- 规则列表（Core/Learned）
- 版本历史查看
- 版本对比工具
- 回滚操作

**FR-2.2.4: 统计页面**
- 进化趋势图（折线图）
- 规则应用频率（条形图）
- 模式识别准确率（仪表盘）

**FR-2.2.5: 日志查看器**
- 实时日志流
- 级别筛选
- 关键词搜索
- 导出功能

---

## 3. API 设计

### 3.1 灵感池 API
```
GET    /api/inspirations          # 列表
GET    /api/inspirations/{id}     # 详情
POST   /api/inspirations          # 添加
PUT    /api/inspirations/{id}     # 更新
POST   /api/inspirations/{id}/convert  # 转化
```

### 3.2 规则 API
```
GET    /api/rules                 # 列表
GET    /api/rules/{name}/history  # 版本历史
GET    /api/rules/{name}/diff     # 版本对比
POST   /api/rules/{name}/rollback # 回滚
```

### 3.3 统计 API
```
GET    /api/stats                 # 综合统计
GET    /api/stats/evolution       # 进化统计
```

### 3.4 日志 API
```
GET    /api/logs                  # 日志查询
GET    /api/logs/stream           # 实时流（SSE）
```

### 3.5 导出 API
```
GET    /api/export/inspirations   # 导出灵感池（JSON/CSV）
GET    /api/export/rules          # 导出规则列表
GET    /api/export/stats          # 导出统计数据
```

---

## 4. UI 设计要点

### 4.1 布局
```
┌─────────────────────────────────────┐
│  Header: AI-as-Me Dashboard         │
├──────┬──────────────────────────────┤
│ Nav  │  Content Area                │
│ - 首页│                              │
│ - 灵感│                              │
│ - 规则│                              │
│ - 统计│                              │
│ - 日志│                              │
└──────┴──────────────────────────────┘
```

### 4.2 交互
- 响应式设计（支持移动端）
- 实时更新（WebSocket/SSE）
- 操作确认（删除、回滚）
- 加载状态提示

### 4.3 空状态设计
- **灵感池为空**: 显示引导图 + "添加第一个灵感" 按钮
- **规则列表为空**: 显示 "运行 Demo 生成第一条规则" 引导
- **日志为空**: 显示 "系统运行正常，暂无日志"
- **统计无数据**: 显示 "开始使用后将显示统计数据"

---

## 5. 非功能需求

### 5.1 性能
- API 响应 < 200ms
- Dashboard 加载 < 2s
- 支持 1000+ 灵感池

### 5.2 安全
- 本地访问（127.0.0.1）
- 可选 Token 认证
- CORS 配置

### 5.3 可维护性
- 代码覆盖率 > 80%
- API 文档自动生成
- 错误日志完整

---

## 6. 用户故事

### US-6.1: 查看灵感成熟度
**作为**用户  
**我想要**在 Dashboard 看到灵感成熟度热力图  
**以便**快速识别哪些灵感可以转化

### US-6.2: 回滚规则版本
**作为**用户  
**我想要**在 Web 界面一键回滚规则  
**以便**快速恢复错误的修改

### US-6.3: 实时查看日志
**作为**开发者  
**我想要**实时查看系统日志  
**以便**快速定位问题

---

**下一步**: 创建 v3.4 Architecture
