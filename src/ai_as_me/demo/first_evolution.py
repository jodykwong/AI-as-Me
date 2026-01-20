"""First Evolution Demo - 首次进化体验."""

from pathlib import Path

from rich.console import Console
from rich.panel import Panel

from ..evolution.engine import EvolutionEngine
from .sample_task import SampleTask
from .progress_tracker import ProgressTracker


class FirstEvolutionDemo:
    """首次进化 Demo."""

    def __init__(self):
        self.console = Console()
        config = {
            "experience_dir": "experience",
            "vector_store": None,
            "llm_client": None,
            "soul_dir": "soul",
        }
        self.evolution_engine = EvolutionEngine(config)
        self.sample_task = SampleTask()
        self.progress = ProgressTracker(total_steps=5)

    async def run(self) -> dict:
        """执行完整 Demo 流程."""
        self._show_welcome()

        try:
            # Step 1: 执行示例任务
            self.progress.update(1, "执行示例任务：检查 requirements.txt")
            task_result = await self.sample_task.execute()
            self.progress.complete(1)

            # Step 2: 收集经验
            self.progress.update(2, "收集经验到 experience/")
            experience = self.evolution_engine.collector.collect(
                task_result["task"],
                task_result["result"],
                task_result["success"],
                task_result.get("duration", 0.0),
            )
            self.progress.complete(2)

            # Step 3: 识别模式
            self.progress.update(3, "识别可复用模式")
            patterns = self.evolution_engine.recognizer.recognize([experience])
            pattern = patterns[0] if patterns else None
            if not pattern:
                raise Exception("未识别到模式")
            self.progress.complete(3)

            # Step 4: 生成规则
            self.progress.update(4, "生成规则")
            rule = self.evolution_engine.generator.generate(pattern)
            self.progress.complete(4)

            # Step 5: 写入 Soul
            self.progress.update(5, "写入 soul/rules/learned/")
            rule_path = self.evolution_engine.writer.write(rule)
            self.progress.complete(5)

            # 显示完成摘要
            self._show_completion(rule_path, rule)

            return {
                "success": True,
                "rule_path": str(rule_path),
                "rule_name": rule.get("name", "unknown"),
            }

        except Exception as e:
            self.console.print(f"\n[red]❌ Demo 执行失败：{e}[/red]")
            self.console.print("\n可能的原因：")
            self.console.print("  • 网络连接问题")
            self.console.print("  • LLM API 配置错误")
            self.console.print(
                "\n[yellow]提示：运行 'ai-as-me demo first-evolution --help' 查看帮助[/yellow]"
            )
            return {"success": False, "error": str(e)}

    def _show_welcome(self):
        """显示欢迎信息."""
        welcome = Panel(
            "[bold cyan]🎉 开始你的首次进化体验[/bold cyan]\n\n"
            "让 AI 自己学会第一个技能\n\n"
            "[dim]预计时间：5-8 分钟[/dim]",
            title="AI-as-Me Demo",
            border_style="cyan",
        )
        self.console.print(welcome)
        self.console.print()

    def _show_completion(self, rule_path: Path, rule: dict):
        """显示完成摘要."""
        self.console.print("\n")
        completion = Panel(
            f"[bold green]✅ 首次进化完成！[/bold green]\n\n"
            f"AI 生成了第一条规则：\n"
            f"[cyan]{rule.get('name', 'unknown')}[/cyan]\n\n"
            f"规则文件：[dim]{rule_path}[/dim]\n\n"
            f"[bold]下一步：[/bold]\n"
            f"  • 查看规则：[yellow]cat {rule_path}[/yellow]\n"
            f"  • 查看统计：[yellow]ai-as-me evolve stats[/yellow]\n"
            f'  • 运行任务：[yellow]ai-as-me task create "你的任务"[/yellow]',
            title="Demo 完成",
            border_style="green",
        )
        self.console.print(completion)
