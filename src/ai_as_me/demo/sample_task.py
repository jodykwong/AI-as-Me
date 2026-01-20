"""Sample Task - 示例任务."""

from pathlib import Path
from dataclasses import dataclass


@dataclass
class Task:
    """任务对象."""

    id: str
    description: str
    tool: str


class SampleTask:
    """示例任务：检查 Python 项目依赖."""

    async def execute(self) -> dict:
        """执行示例任务."""
        # 检查 requirements.txt 是否存在
        req_file = Path("requirements.txt")

        task = Task(
            id="check_python_dependencies",
            description="检查 requirements.txt 是否存在",
            tool="file_check",
        )

        if req_file.exists():
            result = (
                f"找到依赖文件，包含 {len(req_file.read_text().splitlines())} 个依赖"
            )
            success = True
        else:
            result = "未找到 requirements.txt，建议创建"
            success = True

        return {"task": task, "result": result, "success": success, "duration": 0.1}
