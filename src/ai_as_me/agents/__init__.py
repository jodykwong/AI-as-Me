"""AI-as-Me Agent 集成模块"""
from .base import BaseAgent, AgentResult
from .registry import AgentRegistry
from .executor import AgentExecutor

__all__ = ['BaseAgent', 'AgentResult', 'AgentRegistry', 'AgentExecutor']
