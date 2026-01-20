"""Claude Code Agent"""

import time
from typing import List
from .base import BaseAgent, AgentResult
from ..orchestrator.agent_cli import AgentCLI


class ClaudeAgent(BaseAgent):
    """Claude Code Agent 实现"""

    def __init__(self, agent_cli: AgentCLI = None):
        self._cli = agent_cli or AgentCLI()

    @property
    def name(self) -> str:
        return "claude-code"

    def execute(self, task, model: str = None) -> AgentResult:
        """执行任务

        Args:
            task: 任务对象
            model: 模型名称（可选），如 claude-3-5-sonnet-20241022
        """
        start = time.time()
        prompt = self._build_prompt(task)

        # 如果指定了模型，添加到命令中
        result = self._cli.call("claude-code", prompt, timeout=300, model=model)
        duration = time.time() - start

        return AgentResult(
            success=result["success"],
            output=result["output"],
            error=result["error"],
            agent_name=self.name,
            duration=duration,
            metadata={
                "returncode": result.get("returncode"),
                "model": model,
                "tool": "claude-code",
                "cli_version": getattr(self._cli, "version", "unknown"),
            },
        )

    def is_available(self) -> bool:
        """检查是否可用"""
        # return self._cli.available_tools.get("claude-code", False)  # claude-code temporarily disabled
        return False  # Temporarily disabled

    def get_capabilities(self) -> List[str]:
        """获取能力列表"""
        return ["code", "analysis", "refactor", "debug"]

    def _build_prompt(self, task) -> str:
        """构建提示词"""
        title = getattr(task, "title", str(task))
        description = getattr(task, "description", None) or getattr(task, "context", "")
        return f"{title}\n\n{description}"
