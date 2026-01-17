"""Agent状态监控API."""
from fastapi import APIRouter
from pathlib import Path
import psutil
from datetime import datetime

router = APIRouter()


def check_agent_running() -> dict:
    """检查Agent进程是否运行."""
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            cmdline = proc.info.get('cmdline', [])
            if cmdline and 'start_agent.py' in ' '.join(cmdline):
                return {
                    "running": True,
                    "pid": proc.info['pid'],
                    "started_at": datetime.fromtimestamp(proc.create_time()).isoformat()
                }
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue
    
    return {"running": False}


def get_doing_tasks() -> list:
    """获取doing目录中的任务."""
    doing_dir = Path("kanban/doing")
    if not doing_dir.exists():
        return []
    
    tasks = []
    for task_file in doing_dir.glob("*.md"):
        tasks.append({
            "id": task_file.stem,
            "file": task_file.name,
            "modified_at": datetime.fromtimestamp(task_file.stat().st_mtime).isoformat()
        })
    return tasks


@router.get("/agent/status")
async def get_agent_status():
    """获取Agent运行状态."""
    agent_info = check_agent_running()
    doing_tasks = get_doing_tasks()
    
    return {
        "agent": agent_info,
        "doing_tasks": doing_tasks,
        "doing_count": len(doing_tasks),
        "message": "Agent正在运行" if agent_info["running"] else "Agent未启动"
    }


@router.get("/agent/health")
async def agent_health():
    """Agent健康检查."""
    agent_info = check_agent_running()
    
    if agent_info["running"]:
        return {
            "status": "healthy",
            "agent_running": True,
            "message": "Agent运行正常"
        }
    else:
        return {
            "status": "stopped",
            "agent_running": False,
            "message": "Agent未启动，请运行: python start_agent.py"
        }
