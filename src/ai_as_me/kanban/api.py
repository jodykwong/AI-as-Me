"""Web 仪表板 API - Epic 6"""
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from pathlib import Path
import asyncio
import json
import os
from datetime import datetime
from typing import Optional

# Story 12.2: API文档元数据
app = FastAPI(
    title="AI-as-Me Dashboard API",
    description="自进化AI数字分身系统 - 任务管理与智能工具编排",
    version="2.3.0",
    docs_url="/docs",
    redoc_url="/redoc",
    contact={
        "name": "AI-as-Me Team",
        "url": "https://github.com/your-repo/ai-as-me",
    },
    license_info={
        "name": "MIT",
    },
)

# M5 修复: 添加 CORS 支持
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# H1/H2 修复: 配置管理
CONFIG_PATH = Path(os.getenv("AI_AS_ME_CONFIG", "config/agents.yaml"))
DB_PATH = os.getenv("AI_AS_ME_DB", "data/tasks.db")

# 确保数据目录存在
Path(DB_PATH).parent.mkdir(parents=True, exist_ok=True)


# Story 6.3: 数据模型 (Story 14.1: 添加优先级)
class TaskCreate(BaseModel):
    description: str = Field(..., max_length=2000)
    tool: Optional[str] = None
    priority: Optional[str] = Field(default="P2", pattern="^P[1-3]$")


class TaskResponse(BaseModel):
    id: str
    description: str
    status: str
    tool: Optional[str]
    priority: str = "P2"
    created_at: str


# Story 6.1: 健康检查 (Story 12.2: 完善文档)
@app.get("/api/health", tags=["System"], summary="健康检查")
async def health_check():
    """
    系统健康检查
    
    返回系统当前状态和时间戳
    
    Returns:
        - status: 系统状态 (ok)
        - timestamp: 当前时间戳
    """
    return {"status": "ok", "timestamp": datetime.now().isoformat()}


# Story 6.2: 任务列表 (Story 12.2: 完善文档)
@app.get("/api/tasks", tags=["Tasks"], summary="获取任务列表")
async def list_tasks(status: Optional[str] = None):
    """
    获取任务列表
    
    Args:
        status: 可选，按状态过滤 (inbox/todo/doing/done)
    
    Returns:
        任务列表数组
    
    Example:
        GET /api/tasks?status=doing
    """
    from ai_as_me.kanban.database import Database
    
    db = Database(DB_PATH)
    tasks = db.get_all_tasks()
    
    if status:
        tasks = [t for t in tasks if t.get("status") == status]
    
    return [
        TaskResponse(
            id=t["id"],
            description=t["description"],
            status=t["status"],
            tool=t.get("tool"),
            priority=t.get("priority", "P2"),
            created_at=t.get("created_at", "")
        )
        for t in tasks
    ]


# Story 6.3: 创建任务 (Story 12.2: 完善文档)
@app.post("/api/tasks", tags=["Tasks"], summary="创建新任务", response_model=TaskResponse)
async def create_task(task: TaskCreate):
    """
    创建新任务
    
    系统会自动选择最适合的工具执行任务，也可手动指定工具。
    
    Args:
        task: 任务创建请求
            - description: 任务描述 (必填，最长2000字符)
            - tool: 执行工具 (可选，不指定则自动选择)
    
    Returns:
        创建的任务信息
    
    Example:
        ```json
        {
          "description": "实现一个快速排序算法",
          "tool": "claude_code"
        }
        ```
    """
    from ai_as_me.orchestrator.skill_matcher import SkillMatcher
    from ai_as_me.kanban.database import Database
    import uuid
    
    db = Database(DB_PATH)
    
    # 自动选择工具
    tool = task.tool
    if not tool:
        matcher = SkillMatcher(CONFIG_PATH, DB_PATH)
        tool = matcher.match(task.description)
    
    # 创建任务
    task_id = str(uuid.uuid4())[:8]
    db.create_task(task_id, task.description, tool, task.priority)
    
    # 发布事件
    await event_bus.publish("task_created", {
        "id": task_id,
        "description": task.description,
        "tool": tool,
        "priority": task.priority
    })
    
    return TaskResponse(
        id=task_id,
        description=task.description,
        status="inbox",
        tool=tool,
        priority=task.priority,
        created_at=datetime.now().isoformat()
    )


# Story 6.2: 任务详情
@app.get("/api/tasks/{task_id}")
async def get_task(task_id: str):
    """获取任务详情"""
    from ai_as_me.kanban.database import Database
    
    db = Database(DB_PATH)
    task = db.get_task(task_id)
    
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    return TaskResponse(
        id=task["id"],
        description=task["description"],
        status=task["status"],
        tool=task.get("tool"),
        priority=task.get("priority", "P2"),
        created_at=task.get("created_at", "")
    )


# Story 14.2: 执行历史API
@app.get("/api/tasks/{task_id}/history", tags=["Tasks"], summary="获取任务执行历史")
async def get_task_history(task_id: str):
    """
    获取任务执行历史
    
    返回任务的所有执行记录，包括成功率和执行时间
    """
    from ai_as_me.kanban.database import Database
    
    db = Database(DB_PATH)
    history = db.get_task_history(task_id)
    
    return {
        "task_id": task_id,
        "history": history,
        "total_executions": len(history),
        "success_count": sum(1 for h in history if h.get("success"))
    }


@app.get("/api/tools/{tool_name}/stats", tags=["Tools"], summary="获取工具统计")
async def get_tool_stats(tool_name: str):
    """
    获取工具统计信息
    
    返回工具的执行次数、成功率和平均执行时间
    """
    from ai_as_me.kanban.database import Database
    
    db = Database(DB_PATH)
    stats = db.get_tool_stats(tool_name)
    
    return {
        "tool_name": tool_name,
        **stats
    }


@app.put("/api/tasks/{task_id}/status", tags=["Tasks"], summary="更新任务状态")
async def update_status(task_id: str, status: str):
    """
    更新任务状态
    
    Args:
        task_id: 任务ID
        status: 新状态 (inbox/todo/doing/done)
    """
    import re
    from ai_as_me.kanban.database import Database
    
    if not re.match(r'^[a-f0-9\-]{8,36}$', task_id):
        raise HTTPException(status_code=400, detail="Invalid task ID")
    valid_statuses = ["inbox", "todo", "doing", "done"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db = Database(DB_PATH)
    db.update_task_status(task_id, status)
    
    # 发布事件
    await event_bus.publish("task_updated", {
        "id": task_id,
        "status": status
    })
    
    return {"id": task_id, "status": status}


# Story 14.3: 批量任务操作
@app.put("/api/tasks/batch/status", tags=["Tasks"], summary="批量更新任务状态")
async def batch_update_status(task_ids: list[str], status: str):
    """
    批量更新任务状态
    
    Args:
        task_ids: 任务ID列表
        status: 新状态 (inbox/todo/doing/done)
    
    Returns:
        更新结果统计
    """
    from ai_as_me.kanban.database import Database
    
    valid_statuses = ["inbox", "todo", "doing", "done"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail="Invalid status")
    
    db = Database(DB_PATH)
    success_count = 0
    failed = []
    
    for task_id in task_ids:
        try:
            db.update_task_status(task_id, status)
            success_count += 1
            await event_bus.publish("task_updated", {"id": task_id, "status": status})
        except Exception as e:
            failed.append({"id": task_id, "error": str(e)})
    
    return {
        "total": len(task_ids),
        "success": success_count,
        "failed": failed
    }


@app.delete("/api/tasks/batch", tags=["Tasks"], summary="批量删除任务")
async def batch_delete_tasks(task_ids: list[str]):
    """
    批量删除任务
    
    Args:
        task_ids: 任务ID列表
    
    Returns:
        删除结果统计
    """
    from ai_as_me.kanban.database import Database
    
    db = Database(DB_PATH)
    success_count = 0
    failed = []
    
    for task_id in task_ids:
        try:
            with db._pool.get_connection() as conn:
                conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
                conn.commit()
            success_count += 1
            await event_bus.publish("task_deleted", {"id": task_id})
        except Exception as e:
            failed.append({"id": task_id, "error": str(e)})
    
    return {
        "total": len(task_ids),
        "success": success_count,
        "failed": failed
    }


# Story 6.5: 系统状态 (Story 13.3: 健康检查增强)
@app.get("/api/system/health", tags=["System"], summary="详细健康检查")
async def system_health():
    """
    系统健康检查（详细版）
    
    检查所有组件状态：
    - database: 数据库连接
    - rag: RAG服务
    - tools: 工具可用性
    
    Returns:
        详细的组件健康状态
    """
    from ai_as_me.orchestrator.skill_matcher import ToolRegistry
    from ai_as_me.kanban.database import Database
    
    components = {}
    
    # 检查数据库
    try:
        db = Database(DB_PATH)
        db.get_all_tasks()
        components["database"] = {"status": "healthy", "path": DB_PATH}
    except Exception as e:
        components["database"] = {"status": "unhealthy", "error": str(e)}
    
    # 检查RAG服务
    try:
        from ai_as_me.rag.retriever import VectorStore
        store = VectorStore()
        components["rag"] = {"status": "healthy", "model": "all-MiniLM-L6-v2"}
    except Exception as e:
        components["rag"] = {"status": "unhealthy", "error": str(e)}
    
    # 检查工具
    try:
        registry = ToolRegistry(CONFIG_PATH)
        tools = registry.get_available()
        components["tools"] = {
            "status": "healthy",
            "available": tools,
            "count": len(tools)
        }
    except Exception as e:
        components["tools"] = {"status": "unhealthy", "error": str(e)}
    
    # 整体状态
    overall_status = "healthy" if all(
        c.get("status") == "healthy" for c in components.values()
    ) else "degraded"
    
    return {
        "status": overall_status,
        "components": components,
        "timestamp": datetime.now().isoformat()
    }


# Story 6.4: SSE 事件流 (H1 修复: 防止内存泄漏)
class EventBus:
    def __init__(self, max_subscribers: int = 100):
        self.subscribers: list[asyncio.Queue] = []
        self.max_subscribers = max_subscribers
    
    async def publish(self, event: str, data: dict):
        """发布事件到所有订阅者"""
        dead = []
        for queue in self.subscribers:
            try:
                queue.put_nowait({"event": event, "data": data})
            except asyncio.QueueFull:
                dead.append(queue)
        for q in dead:
            self.subscribers.remove(q)
    
    async def subscribe(self) -> asyncio.Queue:
        """订阅事件"""
        # 清理满队列
        self.subscribers = [q for q in self.subscribers if q.qsize() < 50]
        if len(self.subscribers) >= self.max_subscribers:
            raise HTTPException(503, "Too many connections")
        queue = asyncio.Queue(maxsize=50)
        self.subscribers.append(queue)
        return queue
    
    def unsubscribe(self, queue: asyncio.Queue):
        """取消订阅"""
        if queue in self.subscribers:
            self.subscribers.remove(queue)


event_bus = EventBus()


@app.get("/api/events")
async def event_stream():
    """SSE 事件流"""
    async def generate():
        queue = await event_bus.subscribe()
        try:
            while True:
                msg = await asyncio.wait_for(queue.get(), timeout=30)
                yield f"event: {msg['event']}\ndata: {json.dumps(msg['data'])}\n\n"
        except asyncio.TimeoutError:
            yield ": keepalive\n\n"
        except:
            pass
        finally:
            event_bus.unsubscribe(queue)
    
    return StreamingResponse(
        generate(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
        }
    )


# Story 6.2: 主页面 (Story 11.2: 使用独立模板)
@app.get("/", response_class=HTMLResponse)
async def dashboard():
    """仪表板主页"""
    html_path = Path(__file__).parent / "templates" / "dashboard.html"
    if html_path.exists():
        return html_path.read_text()
    raise HTTPException(status_code=500, detail="Template not found")
