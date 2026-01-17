"""Agent 注册表"""
from typing import Dict, List, Optional
from .base import BaseAgent
from .claude_agent import ClaudeAgent
from .opencode_agent import OpenCodeAgent


class AgentRegistry:
    """Agent 注册表和工厂"""
    
    def __init__(self):
        self._agents: Dict[str, BaseAgent] = {}
        self._register_default_agents()
    
    def _register_default_agents(self):
        """注册默认 agents"""
        self.register(ClaudeAgent())
        self.register(OpenCodeAgent())
    
    def register(self, agent: BaseAgent):
        """注册 agent"""
        self._agents[agent.name] = agent
    
    def get(self, name: str) -> Optional[BaseAgent]:
        """获取 agent"""
        return self._agents.get(name)
    
    def get_available(self) -> List[BaseAgent]:
        """获取所有可用的 agents"""
        return [a for a in self._agents.values() if a.is_available()]
    
    def list_all(self) -> List[str]:
        """列出所有已注册的 agent 名称"""
        return list(self._agents.keys())
