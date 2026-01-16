"""Kanban API - Vibe-Kanban REST API."""
from fastapi import APIRouter, HTTPException, Depends
from pathlib import Path
from typing import List

from ...kanban.models import Task, TaskCreate, TaskClarifyRequest, TaskMoveRequest
from ...kanban.vibe_manager import VibeKanbanManager

router = APIRouter()


def get_manager() -> VibeKanbanManager:
    """依赖注入：获取 Kanban 管理器."""
    return VibeKanbanManager()


@router.get("/kanban/board")
async def get_board(manager: VibeKanbanManager = Depends(get_manager)) -> dict:
    """获取看板数据."""
    board = manager.get_board()
    return {
        "inbox": [t.dict() for t in board["inbox"]],
        "todo": [t.dict() for t in board["todo"]],
        "doing": [t.dict() for t in board["doing"]],
        "done": [t.dict() for t in board["done"]]
    }


@router.get("/kanban/tasks/{task_id}")
async def get_task(task_id: str, manager: VibeKanbanManager = Depends(get_manager)) -> dict:
    """获取任务详情."""
    try:
        task = manager.get_task(task_id)
        return task.dict()
    except FileNotFoundError:
        raise HTTPException(404, f"Task {task_id} not found")


@router.post("/kanban/tasks")
async def create_task(task_create: TaskCreate, manager: VibeKanbanManager = Depends(get_manager)) -> dict:
    """创建任务到 inbox."""
    try:
        task = manager.create_task(
            description=task_create.description,
            priority=task_create.priority.value
        )
        return task.dict()
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/kanban/tasks/{task_id}/clarify")
async def clarify_task(task_id: str, clarify_req: TaskClarifyRequest, manager: VibeKanbanManager = Depends(get_manager)) -> dict:
    """澄清任务."""
    try:
        task = manager.clarify_task(task_id, clarify_req.dict())
        return task.dict()
    except FileNotFoundError:
        raise HTTPException(404, f"Task {task_id} not found")
    except Exception as e:
        raise HTTPException(400, str(e))


@router.put("/kanban/tasks/{task_id}/move")
async def move_task(task_id: str, move_req: TaskMoveRequest, manager: VibeKanbanManager = Depends(get_manager)) -> dict:
    """移动任务状态."""
    try:
        task = manager.move_task(task_id, move_req.to_status.value)
        return task.dict()
    except FileNotFoundError:
        raise HTTPException(404, f"Task {task_id} not found")
    except ValueError as e:
        raise HTTPException(400, str(e))
    except Exception as e:
        raise HTTPException(500, str(e))


@router.delete("/kanban/tasks/{task_id}")
async def delete_task(task_id: str, manager: VibeKanbanManager = Depends(get_manager)) -> dict:
    """删除任务."""
    success = manager.delete_task(task_id)
    if not success:
        raise HTTPException(404, f"Task {task_id} not found")
    return {"success": True}
