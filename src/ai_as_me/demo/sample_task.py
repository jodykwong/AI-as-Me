"""Sample Task - 示例任务."""
from pathlib import Path


class SampleTask:
    """示例任务：检查 Python 项目依赖."""
    
    async def execute(self) -> dict:
        """执行示例任务."""
        # 检查 requirements.txt 是否存在
        req_file = Path("requirements.txt")
        
        if req_file.exists():
            result = {
                "task": "check_python_dependencies",
                "action": "检查 requirements.txt",
                "result": "found",
                "details": f"找到依赖文件，包含 {len(req_file.read_text().splitlines())} 个依赖",
                "success": True
            }
        else:
            result = {
                "task": "check_python_dependencies",
                "action": "检查 requirements.txt",
                "result": "not_found",
                "details": "未找到 requirements.txt，建议创建",
                "success": True  # 任务成功执行，只是结果是未找到
            }
        
        return result
