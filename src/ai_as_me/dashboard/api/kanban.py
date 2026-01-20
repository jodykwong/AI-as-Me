"""Kanban API - Vibe-Kanban REST API."""

from fastapi import APIRouter, HTTPException, Depends
from pathlib import Path
from datetime import datetime

from ...kanban.models import TaskCreate, TaskClarifyRequest, TaskMoveRequest
from ...kanban.vibe_manager import VibeKanbanManager

router = APIRouter()


def get_manager() -> VibeKanbanManager:
    """依赖注入：获取 Kanban 管理器."""
    import os

    # 使用环境变量或默认路径
    kanban_dir = Path(os.getenv("KANBAN_DIR", "/home/sunrise/AI-as-Me/kanban"))
    return VibeKanbanManager(kanban_dir)


@router.get("/kanban/board")
async def get_board(manager: VibeKanbanManager = Depends(get_manager)) -> dict:
    """获取看板数据."""
    print(f"DEBUG: get_board called, kanban_dir: {manager.kanban_dir}")
    board = manager.get_board()
    print(f"DEBUG: board data - doing: {len(board['doing'])}")
    return {
        "inbox": [t.dict() for t in board["inbox"] if t.id],
        "todo": [t.dict() for t in board["todo"] if t.id],
        "doing": [t.dict() for t in board["doing"] if t.id],
        "done": [t.dict() for t in board["done"] if t.id],
    }


@router.get("/kanban/tasks/{task_id}")
async def get_task(
    task_id: str, manager: VibeKanbanManager = Depends(get_manager)
) -> dict:
    """获取任务详情."""
    try:
        task = manager.get_task(task_id)
        return task.dict()
    except FileNotFoundError:
        raise HTTPException(404, f"Task {task_id} not found")


@router.post("/kanban/tasks")
async def create_task(
    task_create: TaskCreate, manager: VibeKanbanManager = Depends(get_manager)
) -> dict:
    """创建任务到 inbox."""
    try:
        task = manager.create_task(
            description=task_create.description, priority=task_create.priority.value
        )
        return task.dict()
    except ValueError as e:
        raise HTTPException(400, str(e))


@router.put("/kanban/tasks/{task_id}")
async def update_task(
    task_id: str,
    task_update: TaskCreate,
    manager: VibeKanbanManager = Depends(get_manager),
) -> dict:
    """更新任务内容."""
    task = manager.get_task(task_id)
    task.description = task_update.description
    task.title = task_update.description[:50] + (
        "..." if len(task_update.description) > 50 else ""
    )
    task.priority = task_update.priority
    task.updated_at = datetime.now()

    file_path = manager._find_task_file(task_id)
    file_path.write_text(task.to_markdown(), encoding="utf-8")

    return {"id": task_id, "message": "任务已更新"}


@router.put("/kanban/tasks/{task_id}/clarify")
async def clarify_task(
    task_id: str,
    clarify_req: TaskClarifyRequest,
    manager: VibeKanbanManager = Depends(get_manager),
) -> dict:
    """澄清任务."""
    try:
        task = manager.clarify_task(task_id, clarify_req.dict())
        return task.dict()
    except FileNotFoundError:
        raise HTTPException(404, f"Task {task_id} not found")
    except Exception as e:
        raise HTTPException(400, str(e))


@router.put("/kanban/tasks/{task_id}/move")
async def move_task(
    task_id: str,
    move_req: TaskMoveRequest,
    manager: VibeKanbanManager = Depends(get_manager),
) -> dict:
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
async def delete_task(
    task_id: str, manager: VibeKanbanManager = Depends(get_manager)
) -> dict:
    """删除任务."""
    success = manager.delete_task(task_id)
    if not success:
        raise HTTPException(404, f"Task {task_id} not found")
    return {"success": True}


@router.post("/kanban/tasks/{task_id}/execute")
async def execute_task(
    task_id: str,
    agent_name: str = None,
    manager: VibeKanbanManager = Depends(get_manager),
) -> dict:
    """执行任务

    Args:
        task_id: 任务 ID
        agent_name: 指定 agent (可选)

    Returns:
        {success: bool, agent: str, duration: float, output: str, evolution: dict}
    """
    try:
        result = manager.execute_task(task_id, agent_name, trigger_evolution=True)
        return {
            "success": result["success"],
            "agent": result["result"].agent_name,
            "duration": result["result"].duration,
            "output": result["result"].output[:500],
            "error": result["result"].error,
            "evolution": (
                {
                    "patterns": (
                        len(result["evolution"]["patterns"])
                        if result["evolution"]
                        else 0
                    ),
                    "rules": (
                        len(result["evolution"]["rules"]) if result["evolution"] else 0
                    ),
                }
                if result["evolution"]
                else None
            ),
        }
    except FileNotFoundError:
        raise HTTPException(404, f"Task {task_id} not found")
    except Exception as e:
        raise HTTPException(500, str(e))


@router.put("/kanban/tasks/{task_id}/phase")
async def update_task_phase(
    task_id: str, phase_data: dict, manager: VibeKanbanManager = Depends(get_manager)
) -> dict:
    """更新任务执行阶段和进度

    Args:
        task_id: 任务ID
        phase_data: {"phase": "EXECUTING", "progress": 70}

    Returns:
        更新结果
    """
    try:
        phase = phase_data.get("phase")
        progress = phase_data.get("progress")

        if not phase:
            raise HTTPException(status_code=400, detail="Missing phase")

        manager.update_task_phase(task_id, phase, progress)

        return {"success": True, "phase": phase, "progress": progress}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
