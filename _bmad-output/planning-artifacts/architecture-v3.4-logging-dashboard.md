# AI-as-Me v3.4 Architecture - 日志系统 & Web Dashboard

**创建日期**: 2026-01-15

---

## 1. 系统架构

```
┌─────────────────────────────────────────────┐
│           Web Browser                        │
│  (HTMX + Alpine.js + Chart.js)              │
└─────────────────┬───────────────────────────┘
                  │ HTTP/SSE
┌─────────────────▼───────────────────────────┐
│         FastAPI Web Server                   │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│  │ API      │  │ SSE      │  │ Static   │  │
│  │ Routes   │  │ Stream   │  │ Files    │  │
│  └────┬─────┘  └────┬─────┘  └──────────┘  │
└───────┼─────────────┼─────────────────────┘
        │             │
┌───────▼─────────────▼─────────────────────┐
│         Service Layer                      │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐│
│  │ Pool     │  │ Version  │  │ Stats    ││
│  │ Service  │  │ Service  │  │ Service  ││
│  └────┬─────┘  └────┬─────┘  └────┬─────┘│
└───────┼─────────────┼──────────────┼──────┘
        │             │              │
┌───────▼─────────────▼──────────────▼──────┐
│         Storage Layer                      │
│  soul/inspiration/  soul/rules/.versions/  │
│  logs/             stats/                  │
└────────────────────────────────────────────┘
```

---

## 2. 日志系统架构

### 2.1 日志模块

```python
src/ai_as_me/logging/
├── __init__.py
├── config.py          # 日志配置
├── formatter.py       # JSON 格式化
├── handler.py         # 自定义 Handler
└── query.py           # 日志查询
```

### 2.2 日志流程

```
Application
  ↓
Logger (JSON formatter)
  ↓
Handler (File + Console)
  ↓
logs/
  ├── agent.log
  ├── inspiration.log
  ├── evolution.log
  └── api.log
```

### 2.3 日志格式

```json
{
  "timestamp": "2026-01-15T21:00:00.123Z",
  "level": "INFO",
  "logger": "ai_as_me.inspiration.pool",
  "message": "Inspiration added",
  "context": {
    "inspiration_id": "insp_001",
    "source": "manual",
    "priority": "high"
  },
  "trace_id": "abc123"
}
```

---

## 3. Web Dashboard 架构

### 3.1 后端结构

```python
src/ai_as_me/dashboard/
├── __init__.py
├── app.py             # FastAPI 应用
├── api/
│   ├── __init__.py
│   ├── inspirations.py
│   ├── rules.py
│   ├── stats.py
│   └── logs.py
├── models/
│   ├── __init__.py
│   └── responses.py   # Pydantic 模型
└── static/
    ├── index.html
    ├── css/
    │   └── styles.css
    └── js/
        ├── app.js
        └── charts.js
```

### 3.2 前端架构

```html
<!-- HTMX + Alpine.js 架构 -->
<div x-data="dashboard">
  <!-- HTMX 自动请求 -->
  <div hx-get="/api/inspirations" 
       hx-trigger="load, every 5s"
       hx-target="#inspiration-list">
  </div>
  
  <!-- Alpine.js 状态管理 -->
  <div x-show="loading">Loading...</div>
</div>
```

### 3.3 API 路由

```python
# app.py
from fastapi import FastAPI
from .api import inspirations, rules, stats, logs

app = FastAPI(title="AI-as-Me Dashboard")

app.include_router(inspirations.router, prefix="/api/inspirations")
app.include_router(rules.router, prefix="/api/rules")
app.include_router(stats.router, prefix="/api/stats")
app.include_router(logs.router, prefix="/api/logs")
```

---

## 4. 数据流

### 4.1 灵感池查询流程

```
Browser
  ↓ GET /api/inspirations
FastAPI Router
  ↓
InspirationService
  ↓
InspirationPool (复用)
  ↓
soul/inspiration/pool.jsonl
  ↓
JSON Response
```

### 4.2 实时日志流

```
Browser (EventSource)
  ↓ GET /api/logs/stream
FastAPI SSE Endpoint
  ↓
LogQuery.tail()
  ↓
logs/agent.log (tail -f)
  ↓
Server-Sent Events
```

---

## 5. 技术栈

| 层级 | 技术 | 版本 |
|------|------|------|
| 后端框架 | FastAPI | 0.104+ |
| ASGI 服务器 | Uvicorn | 0.24+ |
| 前端框架 | HTMX | 1.9+ |
| 状态管理 | Alpine.js | 3.13+ |
| 图表库 | Chart.js | 4.4+ |
| 样式 | Tailwind CSS | 3.3+ |

---

## 6. 部署架构

```
Development:
  uvicorn dashboard.app:app --reload

Production:
  uvicorn dashboard.app:app --host 0.0.0.0 --port 8080

Docker (Optional):
  docker run -p 8080:8080 ai-as-me-dashboard
```

---

## 7. 安全考虑

- 默认绑定 127.0.0.1（本地访问）
- 可选 API Token 认证
- CORS 白名单配置
- 文件路径验证（防止路径遍历）

---

**下一步**: 创建 v3.4 Epics & Stories
