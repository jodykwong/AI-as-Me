# Architecture Supplement - AI-as-Me v2.1

**Author:** BMad Master
**Date:** 2026-01-14
**Status:** Draft
**Base Document:** architecture-v2.0.md

---

## 1. 版本概述

v2.1 在 v2.0 架构基础上新增三个 P1 功能的技术设计。

---

## 2. 新增组件架构

### 2.1 项目结构变更

```
src/ai_as_me/
├── orchestrator/
│   ├── skill_matcher.py      # 新增: FR-05 多工具选择
│   └── ...
├── kanban/
│   ├── dashboard.py          # 扩展: FR-06 Web 仪表板
│   ├── api.py                # 扩展: REST API
│   └── sse.py                # 新增: SSE 事件流
├── rag/                      # 新增: FR-07 Agentic RAG
│   ├── __init__.py
│   ├── vectorstore.py        # 向量存储
│   ├── retriever.py          # 检索器
│   └── embeddings.py         # 嵌入处理
└── ...
```

---

## 3. FR-05: 多工具智能选择

### 3.1 组件设计

```
┌─────────────────────────────────────────────────────┐
│                   SkillMatcher                       │
├─────────────────────────────────────────────────────┤
│  TaskAnalyzer    ToolRegistry    HistoryTracker     │
│       │               │               │              │
│       ▼               ▼               ▼              │
│  [任务类型]      [工具能力]      [历史成功率]        │
│       │               │               │              │
│       └───────────────┼───────────────┘              │
│                       ▼                              │
│              ScoreCalculator                         │
│                       │                              │
│                       ▼                              │
│              [最优工具选择]                          │
└─────────────────────────────────────────────────────┘
```

### 3.2 核心类设计

```python
# orchestrator/skill_matcher.py

from enum import Enum
from dataclasses import dataclass

class TaskType(Enum):
    CODE_GENERATION = "code_generation"
    CODE_REVIEW = "code_review"
    DOCUMENTATION = "documentation"
    ARCHITECTURE = "architecture"
    DEBUG = "debug"

@dataclass
class ToolCapability:
    tool_name: str
    capabilities: dict[TaskType, float]  # 0.0-1.0

class SkillMatcher:
    def __init__(self, config: dict, history_db: Database):
        self.registry = ToolRegistry(config)
        self.analyzer = TaskAnalyzer()
        self.history = HistoryTracker(history_db)
    
    def match(self, task: Task) -> str:
        """返回最匹配的工具名称"""
        task_type = self.analyzer.analyze(task.description)
        scores = self._calculate_scores(task_type)
        return max(scores, key=scores.get)
    
    def _calculate_scores(self, task_type: TaskType) -> dict[str, float]:
        scores = {}
        for tool in self.registry.get_available():
            cap_score = self.registry.get_capability(tool, task_type)
            hist_score = self.history.get_success_rate(tool, task_type)
            scores[tool] = cap_score * 0.5 + hist_score * 0.3 + 1.0 * 0.2
        return scores
```

### 3.3 配置文件扩展

```yaml
# config/agents.yaml
agents:
  claude_code:
    command: ["npx", "-y", "@anthropic-ai/claude-code@2.0.76"]
    capabilities:
      code_generation: 0.9
      code_review: 0.9
      documentation: 0.7
      architecture: 0.9
      debug: 0.7
  
  opencode:
    command: ["npx", "-y", "opencode-ai@1.1.3"]
    capabilities:
      code_generation: 0.7
      code_review: 0.7
      documentation: 0.5
      architecture: 0.5
      debug: 0.9
  
  gemini_cli:
    command: ["npx", "-y", "@anthropic-ai/gemini-cli"]
    capabilities:
      code_generation: 0.7
      code_review: 0.7
      documentation: 0.9
      architecture: 0.7
      debug: 0.5
  
  qwen_code:
    command: ["npx", "-y", "qwen-code"]
    capabilities:
      code_generation: 0.7
      code_review: 0.5
      documentation: 0.7
      architecture: 0.5
      debug: 0.7
```

### 3.4 数据库扩展

```sql
-- 工具执行历史表
CREATE TABLE tool_history (
    id INTEGER PRIMARY KEY,
    task_id TEXT NOT NULL,
    tool_name TEXT NOT NULL,
    task_type TEXT NOT NULL,
    success BOOLEAN NOT NULL,
    execution_time REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_tool_history_tool ON tool_history(tool_name);
CREATE INDEX idx_tool_history_type ON tool_history(task_type);
```

---

## 4. FR-06: Web 仪表板

### 4.1 组件设计

```
┌─────────────────────────────────────────────────────┐
│                   Web Dashboard                      │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │   FastAPI   │  │    HTMX     │  │  Alpine.js  │ │
│  │   Backend   │  │  Frontend   │  │   State     │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │         │
│         ▼                ▼                ▼         │
│  ┌─────────────────────────────────────────────┐   │
│  │              SSE Event Stream               │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 4.2 API 设计

```python
# kanban/api.py

from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from pydantic import BaseModel

app = FastAPI(title="AI-as-Me Dashboard")

class TaskCreate(BaseModel):
    description: str
    tool: str | None = None

class TaskResponse(BaseModel):
    id: str
    description: str
    status: str
    tool: str | None
    created_at: str

@app.get("/api/tasks")
async def list_tasks(status: str | None = None) -> list[TaskResponse]:
    """获取任务列表"""
    pass

@app.post("/api/tasks")
async def create_task(task: TaskCreate) -> TaskResponse:
    """创建新任务"""
    pass

@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str) -> TaskResponse:
    """获取任务详情"""
    pass

@app.put("/api/tasks/{task_id}/status")
async def update_status(task_id: str, status: str) -> TaskResponse:
    """更新任务状态"""
    pass

@app.get("/api/system/health")
async def health_check() -> dict:
    """系统健康检查"""
    pass
```

### 4.3 SSE 事件流

```python
# kanban/sse.py

import asyncio
from fastapi import Request
from fastapi.responses import StreamingResponse

class EventBus:
    def __init__(self):
        self.subscribers: list[asyncio.Queue] = []
    
    async def publish(self, event: str, data: dict):
        for queue in self.subscribers:
            await queue.put({"event": event, "data": data})
    
    async def subscribe(self) -> asyncio.Queue:
        queue = asyncio.Queue()
        self.subscribers.append(queue)
        return queue

event_bus = EventBus()

@app.get("/api/events")
async def event_stream(request: Request):
    async def generate():
        queue = await event_bus.subscribe()
        try:
            while True:
                if await request.is_disconnected():
                    break
                msg = await queue.get()
                yield f"event: {msg['event']}\ndata: {msg['data']}\n\n"
        finally:
            event_bus.subscribers.remove(queue)
    
    return StreamingResponse(generate(), media_type="text/event-stream")
```

### 4.4 前端模板

```html
<!-- templates/dashboard.html -->
<!DOCTYPE html>
<html lang="zh">
<head>
    <meta charset="UTF-8">
    <title>AI-as-Me Dashboard</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <script src="https://unpkg.com/alpinejs@3.13.3"></script>
    <script src="https://cdn.tailwindcss.com"></script>
</head>
<body class="bg-gray-100">
    <div class="container mx-auto p-4" x-data="dashboard()">
        <!-- Kanban Board -->
        <div class="grid grid-cols-4 gap-4">
            <template x-for="column in columns">
                <div class="bg-white rounded-lg p-4 shadow">
                    <h2 class="font-bold mb-4" x-text="column.title"></h2>
                    <div class="space-y-2">
                        <template x-for="task in getTasksByStatus(column.status)">
                            <div class="p-3 bg-gray-50 rounded border"
                                 hx-get="/api/tasks/${task.id}"
                                 hx-trigger="click">
                                <p x-text="task.description"></p>
                            </div>
                        </template>
                    </div>
                </div>
            </template>
        </div>
    </div>
    
    <script>
    function dashboard() {
        return {
            tasks: [],
            columns: [
                {title: 'Inbox', status: 'inbox'},
                {title: 'Todo', status: 'todo'},
                {title: 'Doing', status: 'doing'},
                {title: 'Done', status: 'done'}
            ],
            getTasksByStatus(status) {
                return this.tasks.filter(t => t.status === status);
            },
            init() {
                // SSE 连接
                const es = new EventSource('/api/events');
                es.onmessage = (e) => {
                    const data = JSON.parse(e.data);
                    this.handleEvent(data);
                };
            }
        }
    }
    </script>
</body>
</html>
```

---

## 5. FR-07: Agentic RAG 检索

### 5.1 组件设计

```
┌─────────────────────────────────────────────────────┐
│                   Agentic RAG                        │
├─────────────────────────────────────────────────────┤
│                                                      │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐ │
│  │  Embedder   │  │ VectorStore │  │  Retriever  │ │
│  │  (MiniLM)   │  │  (ChromaDB) │  │             │ │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘ │
│         │                │                │         │
│         ▼                ▼                ▼         │
│  ┌─────────────────────────────────────────────┐   │
│  │           Context Builder                    │   │
│  │     (构建注入 Soul 的上下文片段)              │   │
│  └─────────────────────────────────────────────┘   │
│                                                      │
└─────────────────────────────────────────────────────┘
```

### 5.2 核心类设计

```python
# rag/vectorstore.py

import chromadb
from sentence_transformers import SentenceTransformer

class VectorStore:
    def __init__(self, persist_dir: str = "~/.ai-as-me/rag"):
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.collection = self.client.get_or_create_collection("experiences")
        self.embedder = SentenceTransformer('all-MiniLM-L6-v2')
    
    def add(self, experience: TaskExperience) -> None:
        embedding = self.embedder.encode(experience.description)
        self.collection.add(
            ids=[experience.task_id],
            embeddings=[embedding.tolist()],
            metadatas=[{
                "tool": experience.tool_used,
                "success": experience.success,
                "created_at": experience.created_at.isoformat()
            }],
            documents=[experience.result_summary]
        )
    
    def query(self, text: str, top_k: int = 5) -> list[dict]:
        embedding = self.embedder.encode(text)
        results = self.collection.query(
            query_embeddings=[embedding.tolist()],
            n_results=top_k
        )
        return self._format_results(results)
```

```python
# rag/retriever.py

from dataclasses import dataclass
from datetime import datetime

@dataclass
class TaskExperience:
    task_id: str
    description: str
    tool_used: str
    result_summary: str
    success: bool
    user_feedback: str | None
    created_at: datetime

class ExperienceRetriever:
    def __init__(self, vectorstore: VectorStore):
        self.store = vectorstore
    
    def store_experience(self, exp: TaskExperience) -> None:
        self.store.add(exp)
    
    def retrieve(self, query: str, top_k: int = 5) -> list[TaskExperience]:
        results = self.store.query(query, top_k)
        # 过滤成功案例
        return [r for r in results if r.get("success", False)]
    
    def build_context(self, experiences: list[TaskExperience], max_tokens: int = 2000) -> str:
        """构建注入上下文，限制 token 数"""
        context_parts = []
        total_len = 0
        
        for exp in experiences:
            part = f"[历史经验] {exp.description}\n结果: {exp.result_summary[:200]}\n"
            if total_len + len(part) > max_tokens * 4:  # 粗略估算
                break
            context_parts.append(part)
            total_len += len(part)
        
        return "\n".join(context_parts)
```

### 5.3 Soul 注入集成

```python
# orchestrator/soul_injector.py (扩展)

class SoulInjector:
    def __init__(self, template_dir: Path, retriever: ExperienceRetriever):
        self.env = Environment(loader=FileSystemLoader(template_dir))
        self.retriever = retriever
    
    def inject(self, template_name: str, soul_data: dict, task_data: dict) -> str:
        # 检索相关经验
        experiences = self.retriever.retrieve(task_data["description"])
        rag_context = self.retriever.build_context(experiences)
        
        template = self.env.get_template(f"{template_name}.j2")
        return template.render(
            profile=soul_data.get('profile', ''),
            rules=soul_data.get('rules', ''),
            rag_context=rag_context,  # 新增
            task=task_data
        )
```

### 5.4 模板扩展

```jinja2
{# templates/default.j2 #}
## 个人档案
{{ profile }}

## 工作规则
{{ rules }}

{% if rag_context %}
## 相关历史经验
{{ rag_context }}
{% endif %}

## 当前任务
{{ task.description }}
```

---

## 6. 依赖更新

```toml
# pyproject.toml 新增依赖

[project.dependencies]
# 现有依赖...

# v2.1 新增
chromadb = ">=0.4.0"
sentence-transformers = ">=2.2.0"
htmx = ">=1.9.0"  # 前端通过 CDN
```

---

## 7. 数据流图

```
┌──────────────────────────────────────────────────────────────┐
│                        v2.1 数据流                            │
├──────────────────────────────────────────────────────────────┤
│                                                               │
│  用户输入                                                      │
│     │                                                         │
│     ▼                                                         │
│  ┌─────────┐    ┌─────────────┐    ┌─────────────┐           │
│  │ CLI/Web │───▶│ TaskManager │───▶│ SkillMatcher│           │
│  └─────────┘    └─────────────┘    └──────┬──────┘           │
│                                           │                   │
│                                           ▼                   │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │  RAG检索    │◀───│ SoulInjector│◀───│ 选择工具    │       │
│  └──────┬──────┘    └──────┬──────┘    └─────────────┘       │
│         │                  │                                  │
│         ▼                  ▼                                  │
│  ┌─────────────────────────────────────┐                     │
│  │         Agent CLI 执行               │                     │
│  └──────────────────┬──────────────────┘                     │
│                     │                                         │
│                     ▼                                         │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐       │
│  │ 结果存储    │───▶│ RAG向量化   │───▶│ 养蛊学习    │       │
│  └─────────────┘    └─────────────┘    └─────────────┘       │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

---

## 8. 实施顺序建议

| 顺序 | 功能 | 依赖 | 工时 |
|------|------|------|------|
| 1 | FR-05 SkillMatcher | v2.0 完成 | 2天 |
| 2 | FR-07 RAG 基础 | 无 | 1.5天 |
| 3 | FR-07 RAG + Soul 集成 | FR-07 基础 | 0.5天 |
| 4 | FR-06 API 后端 | v2.0 完成 | 1天 |
| 5 | FR-06 Web 前端 | API 后端 | 1.5天 |
| 6 | FR-06 SSE 集成 | Web 前端 | 0.5天 |

**总计**: 7天

---

## 9. 风险与缓解

| 风险 | 缓解措施 |
|------|----------|
| ChromaDB 性能问题 | 限制向量库大小 <10000 条 |
| SSE 连接不稳定 | 前端自动重连机制 |
| 工具选择不准确 | 保留 `--tool` 手动覆盖 |
| 嵌入模型加载慢 | 首次加载后缓存模型 |
