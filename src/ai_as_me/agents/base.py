"""Agent 基类"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AgentResult:
    """Agent 执行结果"""

    success: bool
    output: str
    error: str
    agent_name: str
    duration: float
    metadata: Dict = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

    def to_dict(self):
        """转换为字典格式，便于序列化"""
        return {
            "success": self.success,
            "output": self.output,
            "error": self.error,
            "agent_name": self.agent_name,
            "duration": self.duration,
            "metadata": self.metadata,
        }


class BaseAgent(ABC):
    """Agent 抽象基类"""

    @abstractmethod
    def execute(self, task, model: str = None) -> AgentResult:
        """执行任务

        Args:
            task: 任务对象
            model: 模型名称（可选）
        """
        pass

    @abstractmethod
    def is_available(self) -> bool:
        """检查 agent 是否可用"""
        pass

    @abstractmethod
    def get_capabilities(self) -> List[str]:
        """获取 agent 能力列表"""
        pass

    @property
    @abstractmethod
    def name(self) -> str:
        """Agent 名称"""
        pass
