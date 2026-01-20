"""
Enhanced Dashboard with SSE and Database Backend
Inspired by Vibe-Kanban
"""

import json
import asyncio
from pathlib import Path
from datetime import datetime
from typing import AsyncGenerator

try:
    from fastapi import FastAPI, Request, HTTPException
    from fastapi.responses import HTMLResponse, StreamingResponse
    from pydantic import BaseModel
    import uvicorn

    HAS_FASTAPI = True
except ImportError:
    HAS_FASTAPI = False

from .database import KanbanDB, TaskStatus


class CreateTaskRequest(BaseModel):
    title: str
    description: str = None
    needs_approval: bool = False


class UpdateTaskRequest(BaseModel):
    status: str = None
    approved: bool = None


def create_app(db_path: Path, soul_dir: Path = None):
    """Create FastAPI app with database backend."""
    if not HAS_FASTAPI:
        raise ImportError("pip install fastapi uvicorn pydantic")

    app = FastAPI(title="AI-as-Me Kanban")
    db = KanbanDB(db_path)

    # SSE state tracking
    _last_stats = {}

    @app.get("/api/stats")
    async def get_stats():
        return db.get_stats()

    @app.get("/api/tasks")
    async def list_tasks(status: str = None):
        if status:
            return [t.to_dict() for t in db.list_tasks(TaskStatus(status))]
        return [t.to_dict() for t in db.list_tasks()]

    @app.post("/api/tasks")
    async def create_task(req: CreateTaskRequest):
        task = db.create_task(req.title, req.description, req.needs_approval)
        return task.to_dict()

    @app.get("/api/tasks/{task_id}")
    async def get_task(task_id: str):
        task = db.get_task(task_id)
        if not task:
            raise HTTPException(404, "Task not found")
        return task.to_dict()

    @app.patch("/api/tasks/{task_id}")
    async def update_task(task_id: str, req: UpdateTaskRequest):
        task = db.get_task(task_id)
        if not task:
            raise HTTPException(404, "Task not found")

        if req.status:
            db.update_task_status(task_id, TaskStatus(req.status))
        if req.approved:
            db.approve_task(task_id)

        return db.get_task(task_id).to_dict()

    @app.delete("/api/tasks/{task_id}")
    async def delete_task(task_id: str):
        db.delete_task(task_id)
        return {"ok": True}

    @app.post("/api/tasks/{task_id}/approve")
    async def approve_task(task_id: str):
        db.approve_task(task_id)
        return {"ok": True}

    @app.get("/api/tasks/{task_id}/executions")
    async def get_executions(task_id: str):
        exec = db.get_latest_execution(task_id)
        return exec.to_dict() if exec else None

    @app.get("/api/rules")
    async def get_rules():
        return db.get_rules()

    @app.get("/api/stream")
    async def stream_updates():
        """SSE endpoint for real-time updates."""

        async def event_generator() -> AsyncGenerator[str, None]:
            nonlocal _last_stats
            while True:
                stats = db.get_stats()
                tasks = [t.to_dict() for t in db.list_tasks()]

                data = {
                    "stats": stats,
                    "tasks": tasks,
                    "ts": datetime.now().isoformat(),
                }

                if data != _last_stats:
                    yield f"data: {json.dumps(data)}\n\n"
                    _last_stats = data

                await asyncio.sleep(1)

        return StreamingResponse(
            event_generator(),
            media_type="text/event-stream",
            headers={"Cache-Control": "no-cache", "Connection": "keep-alive"},
        )

    @app.get("/", response_class=HTMLResponse)
    async def index():
        stats = db.get_stats()

        return f"""<!DOCTYPE html>
<html><head>
<title>AI-as-Me Kanban</title>
<meta name="viewport" content="width=device-width,initial-scale=1">
<style>
* {{ box-sizing: border-box; margin: 0; padding: 0; }}
body {{ font-family: system-ui; background: #0f172a; color: #e2e8f0; min-height: 100vh; }}
header {{ background: #1e293b; padding: 1rem; display: flex; justify-content: space-between; align-items: center; flex-wrap: wrap; gap: 1rem; }}
h1 {{ font-size: 1.25rem; }}
.stats {{ font-size: 0.875rem; color: #94a3b8; }}
.add-btn {{ background: #3b82f6; color: white; border: none; padding: 0.5rem 1rem; border-radius: 6px; cursor: pointer; }}
.add-btn:hover {{ background: #2563eb; }}
.board {{ display: grid; grid-template-columns: repeat(5, 1fr); gap: 0.75rem; padding: 1rem; height: calc(100vh - 70px); overflow-x: auto; }}
.column {{ background: #1e293b; border-radius: 8px; padding: 0.75rem; display: flex; flex-direction: column; min-width: 200px; }}
.column h2 {{ font-size: 0.75rem; color: #94a3b8; margin-bottom: 0.5rem; display: flex; justify-content: space-between; align-items: center; }}
.column h2 span {{ background: #334155; padding: 2px 8px; border-radius: 10px; font-size: 0.7rem; }}
.tasks {{ flex: 1; overflow-y: auto; }}
.task {{ background: #334155; border-radius: 6px; padding: 0.6rem; margin-bottom: 0.5rem; cursor: grab; transition: all 0.2s; border-left: 3px solid transparent; }}
.task:hover {{ background: #475569; transform: translateY(-1px); }}
.task.dragging {{ opacity: 0.5; }}
.task.running {{ border-left-color: #22c55e; animation: pulse 2s infinite; }}
.task.failed {{ border-left-color: #ef4444; }}
.task-title {{ font-weight: 500; font-size: 0.8rem; word-break: break-word; }}
.task-desc {{ font-size: 0.7rem; color: #94a3b8; margin-top: 0.25rem; max-height: 40px; overflow: hidden; }}
.task-meta {{ display: flex; gap: 0.25rem; margin-top: 0.4rem; flex-wrap: wrap; }}
.badge {{ font-size: 0.6rem; padding: 2px 6px; border-radius: 4px; }}
.badge-approval {{ background: #f59e0b; color: #000; cursor: pointer; }}
.badge-approved {{ background: #22c55e; color: #000; }}
.column.drag-over {{ background: #334155; }}
.modal {{ display: none; position: fixed; top: 0; left: 0; right: 0; bottom: 0; background: rgba(0,0,0,0.7); justify-content: center; align-items: center; z-index: 100; }}
.modal.show {{ display: flex; }}
.modal-content {{ background: #1e293b; padding: 1.5rem; border-radius: 8px; width: 90%; max-width: 500px; }}
.modal input, .modal textarea {{ width: 100%; padding: 0.5rem; margin: 0.5rem 0; background: #334155; border: 1px solid #475569; border-radius: 4px; color: #e2e8f0; }}
.modal textarea {{ min-height: 100px; }}
.modal-btns {{ display: flex; gap: 0.5rem; margin-top: 1rem; }}
.modal-btns button {{ flex: 1; padding: 0.5rem; border: none; border-radius: 4px; cursor: pointer; }}
.btn-primary {{ background: #3b82f6; color: white; }}
.btn-secondary {{ background: #475569; color: white; }}
@keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.7; }} }}
@media (max-width: 900px) {{ .board {{ grid-template-columns: repeat(2, 1fr); }} }}
@media (max-width: 500px) {{ .board {{ grid-template-columns: 1fr; }} }}
</style>
</head>
<body>
<header>
  <h1>🤖 AI-as-Me Kanban</h1>
  <div class="stats">
    📊 Rules: <span id="rules-count">{stats.get('rules', 0)}</span> |
    ⚡ Running: <span id="running-count">{stats.get('running', 0)}</span> |
    🕐 <span id="time"></span>
  </div>
  <button class="add-btn" onclick="showAddModal()">+ New Task</button>
</header>

<div class="board" id="board">
  <div class="column" data-status="todo"><h2>📋 Todo <span id="cnt-todo">0</span></h2><div class="tasks" id="col-todo"></div></div>
  <div class="column" data-status="in_progress"><h2>⚡ In Progress <span id="cnt-in_progress">0</span></h2><div class="tasks" id="col-in_progress"></div></div>
  <div class="column" data-status="in_review"><h2>👀 Review <span id="cnt-in_review">0</span></h2><div class="tasks" id="col-in_review"></div></div>
  <div class="column" data-status="done"><h2>✅ Done <span id="cnt-done">0</span></h2><div class="tasks" id="col-done"></div></div>
  <div class="column" data-status="cancelled"><h2>🚫 Cancelled <span id="cnt-cancelled">0</span></h2><div class="tasks" id="col-cancelled"></div></div>
</div>

<div class="modal" id="addModal">
  <div class="modal-content">
    <h3>New Task</h3>
    <input type="text" id="taskTitle" placeholder="Task title">
    <textarea id="taskDesc" placeholder="Description (optional)"></textarea>
    <label><input type="checkbox" id="taskApproval"> Requires approval</label>
    <div class="modal-btns">
      <button class="btn-secondary" onclick="hideAddModal()">Cancel</button>
      <button class="btn-primary" onclick="createTask()">Create</button>
    </div>
  </div>
</div>

<script>
let draggedTask = null;
let tasks = [];

function renderTasks(data) {{
  tasks = data.tasks || [];
  const stats = data.stats || {{}};
  
  // Update stats
  document.getElementById('rules-count').textContent = stats.rules || 0;
  document.getElementById('running-count').textContent = stats.running || 0;
  
  // Clear columns
  ['todo','in_progress','in_review','done','cancelled'].forEach(status => {{
    document.getElementById('col-' + status).innerHTML = '';
    document.getElementById('cnt-' + status).textContent = stats[status] || 0;
  }});
  
  // Render tasks
  tasks.forEach(t => {{
    const col = document.getElementById('col-' + t.status);
    if (!col) return;
    
    const div = document.createElement('div');
    div.className = 'task';
    div.draggable = true;
    div.dataset.id = t.id;
    
    let badges = '';
    if (t.needs_approval && !t.approved) {{
      badges += `<span class="badge badge-approval" onclick="approveTask('${{t.id}}')">⏸ Approve</span>`;
    }} else if (t.approved) {{
      badges += `<span class="badge badge-approved">✓</span>`;
    }}
    
    div.innerHTML = `
      <div class="task-title">${{t.title}}</div>
      ${{t.description ? `<div class="task-desc">${{t.description.substring(0,100)}}</div>` : ''}}
      <div class="task-meta">${{badges}}</div>
    `;
    col.appendChild(div);
  }});
  
  setupDragDrop();
}}

function setupDragDrop() {{
  document.querySelectorAll('.task').forEach(task => {{
    task.addEventListener('dragstart', e => {{
      draggedTask = e.target;
      e.target.classList.add('dragging');
    }});
    task.addEventListener('dragend', e => {{
      e.target.classList.remove('dragging');
      document.querySelectorAll('.column').forEach(c => c.classList.remove('drag-over'));
    }});
  }});
  
  document.querySelectorAll('.column').forEach(col => {{
    col.addEventListener('dragover', e => {{ e.preventDefault(); col.classList.add('drag-over'); }});
    col.addEventListener('dragleave', () => col.classList.remove('drag-over'));
    col.addEventListener('drop', async e => {{
      e.preventDefault();
      col.classList.remove('drag-over');
      if (draggedTask) {{
        const taskId = draggedTask.dataset.id;
        const status = col.dataset.status;
        await fetch(`/api/tasks/${{taskId}}`, {{
          method: 'PATCH',
          headers: {{'Content-Type': 'application/json'}},
          body: JSON.stringify({{status}})
        }});
      }}
    }});
  }});
}}

async function approveTask(taskId) {{
  await fetch(`/api/tasks/${{taskId}}/approve`, {{method: 'POST'}});
}}

function showAddModal() {{ document.getElementById('addModal').classList.add('show'); }}
function hideAddModal() {{ document.getElementById('addModal').classList.remove('show'); }}

async function createTask() {{
  const title = document.getElementById('taskTitle').value;
  const description = document.getElementById('taskDesc').value;
  const needs_approval = document.getElementById('taskApproval').checked;
  
  if (!title) return alert('Title required');
  
  await fetch('/api/tasks', {{
    method: 'POST',
    headers: {{'Content-Type': 'application/json'}},
    body: JSON.stringify({{title, description, needs_approval}})
  }});
  
  hideAddModal();
  document.getElementById('taskTitle').value = '';
  document.getElementById('taskDesc').value = '';
  document.getElementById('taskApproval').checked = false;
}}

// SSE
const evtSource = new EventSource('/api/stream');
evtSource.onmessage = e => renderTasks(JSON.parse(e.data));
evtSource.onerror = () => setTimeout(() => location.reload(), 5000);

// Time
setInterval(() => {{
  document.getElementById('time').textContent = new Date().toLocaleTimeString();
}}, 1000);

// Initial load
fetch('/api/tasks').then(r => r.json()).then(tasks => {{
  fetch('/api/stats').then(r => r.json()).then(stats => {{
    renderTasks({{tasks, stats}});
  }});
}});
</script>
</body></html>"""

    return app


def run_dashboard(db_path: Path, soul_dir: Path = None, port: int = 8000):
    """Run the dashboard server."""
    app = create_app(db_path, soul_dir)
    uvicorn.run(app, host="0.0.0.0", port=port)


if __name__ == "__main__":
    db_path = Path(__file__).parent.parent.parent.parent / "kanban.db"
    run_dashboard(db_path)
