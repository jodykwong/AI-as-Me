"""Kanban Task Execution API - 集成Agent执行能力."""

from fastapi import APIRouter, HTTPException, BackgroundTasks
from pathlib import Path
from typing import Optional
from datetime import datetime

router = APIRouter()

# 全局执行状态跟踪
execution_status = {}


def get_executor():
    """获取TaskExecutor实例."""
    import os
    from dotenv import load_dotenv
    from ai_as_me.llm.client import LLMClient
    from ai_as_me.llm.executor import TaskExecutor
    from ai_as_me.soul.loader import load_soul_context

    # 加载环境变量
    load_dotenv()

    api_key = os.getenv("DEEPSEEK_API_KEY")
    base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com")
    model = os.getenv("DEEPSEEK_MODEL", "deepseek-chat")

    if not api_key:
        raise ValueError("DEEPSEEK_API_KEY not found in environment")

    llm_client = LLMClient(api_key=api_key, base_url=base_url, model=model)
    soul_context = load_soul_context(Path("soul"))
    return TaskExecutor(llm_client, soul_context)


def get_task_from_file(task_id: str) -> Optional[dict]:
    """从Markdown文件加载任务."""
    from ai_as_me.kanban.models import Task

    kanban_dir = Path("kanban")
    for status in ["inbox", "todo", "doing", "done"]:
        task_file = kanban_dir / status / f"{task_id}.md"
        if task_file.exists():
            task = Task.from_markdown(task_file.read_text(encoding="utf-8"))
            return {"task": task, "file_path": task_file, "status": status}
    return None


async def execute_task_background(task_id: str):
    """后台执行任务."""
    execution_status[task_id] = {
        "status": "running",
        "started_at": datetime.now().isoformat(),
        "logs": [],
        "result": None,
    }

    try:
        task_data = get_task_from_file(task_id)
        if not task_data:
            raise Exception(f"Task {task_id} not found")

        task = task_data["task"]

        # 记录日志
        execution_status[task_id]["logs"].append(
            {
                "time": datetime.now().isoformat(),
                "level": "INFO",
                "message": f"开始执行任务: {task.title}",
            }
        )

        # 执行任务
        executor = get_executor()

        # 构建执行上下文
        class TaskContext:
            def __init__(self, task_obj):
                self.title = task_obj.title
                self.context = task_obj.description
                if task_obj.clarification:
                    self.context += f"\n\n目标: {task_obj.clarification.goal}"
                    self.context += "\n\n验收标准:\n"
                    for i, ac in enumerate(
                        task_obj.clarification.acceptance_criteria, 1
                    ):
                        self.context += f"{i}. {ac}\n"
                self.expected_output = None
                self.file_path = task_data["file_path"]

        task_ctx = TaskContext(task)
        result = executor.execute(task_ctx)

        if result:
            execution_status[task_id]["status"] = "completed"
            execution_status[task_id]["result"] = result
            execution_status[task_id]["logs"].append(
                {
                    "time": datetime.now().isoformat(),
                    "level": "SUCCESS",
                    "message": "任务执行成功",
                }
            )
        else:
            raise Exception("执行失败，未返回结果")

    except Exception as e:
        execution_status[task_id]["status"] = "failed"
        execution_status[task_id]["error"] = str(e)
        execution_status[task_id]["logs"].append(
            {
                "time": datetime.now().isoformat(),
                "level": "ERROR",
                "message": f"执行失败: {str(e)}",
            }
        )

    execution_status[task_id]["completed_at"] = datetime.now().isoformat()


@router.post("/kanban/tasks/{task_id}/execute")
async def execute_task(task_id: str, background_tasks: BackgroundTasks):
    """手动触发任务执行."""
    task_data = get_task_from_file(task_id)
    if not task_data:
        raise HTTPException(404, f"Task {task_id} not found")

    if task_data["status"] != "doing":
        raise HTTPException(400, "只能执行doing状态的任务")

    # 检查是否已在执行
    if task_id in execution_status and execution_status[task_id]["status"] == "running":
        raise HTTPException(400, "任务正在执行中")

    # 后台执行
    background_tasks.add_task(execute_task_background, task_id)

    return {"message": "任务已开始执行", "task_id": task_id, "status": "running"}


@router.get("/kanban/tasks/{task_id}/execution")
async def get_execution_status(task_id: str):
    """获取任务执行状态."""
    if task_id not in execution_status:
        return {"task_id": task_id, "status": "not_started", "message": "任务尚未执行"}

    return {"task_id": task_id, **execution_status[task_id]}


@router.get("/kanban/execution/active")
async def get_active_executions():
    """获取所有活跃的执行."""
    active = {
        task_id: status
        for task_id, status in execution_status.items()
        if status["status"] == "running"
    }
    return {"active_executions": active, "count": len(active)}
