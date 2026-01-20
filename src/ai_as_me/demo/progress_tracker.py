"""Progress Tracker - 进度追踪器."""

from rich.console import Console


class ProgressTracker:
    """进度追踪器."""

    def __init__(self, total_steps: int = 5):
        self.console = Console()
        self.total_steps = total_steps
        self.current_step = 0
        self.steps = ["执行示例任务", "收集经验", "识别模式", "生成规则", "写入 Soul"]

    def update(self, step: int, message: str):
        """更新进度."""
        self.current_step = step
        status = "⏳" if step <= self.total_steps else "✓"
        self.console.print(f"{status} 步骤 {step}/{self.total_steps}: {message}")

    def complete(self, step: int):
        """标记步骤完成."""
        # 用绿色勾替换
        pass  # Rich 会自动处理
