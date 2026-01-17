"""Agent 执行编排器"""
import logging
from typing import List, Optional
from .base import AgentResult
from .registry import AgentRegistry


class AgentExecutor:
    """Agent 任务执行编排器"""
    
    def __init__(self, registry: AgentRegistry = None):
        self.registry = registry or AgentRegistry()
        self.logger = logging.getLogger('AgentExecutor')
    
    def execute_task(self, task, agent_name: str = None) -> AgentResult:
        """执行任务
        
        Args:
            task: 任务对象
            agent_name: 指定 agent 名称，None 则使用第一个可用的
                       格式: "agent-name" 或 "agent-name:model"
        
        Returns:
            AgentResult
        """
        # 解析 agent 和 model
        model = None
        if agent_name and ':' in agent_name:
            agent_name, model = agent_name.split(':', 1)
        
        # 如果任务有工具配置，优先使用
        if hasattr(task, 'clarification') and task.clarification and task.clarification.tool:
            tool_config = task.clarification.tool
            if ':' in tool_config:
                agent_name, model = tool_config.split(':', 1)
            else:
                agent_name = tool_config
        
        if agent_name:
            agent = self.registry.get(agent_name)
            if not agent:
                return AgentResult(
                    success=False,
                    output='',
                    error=f'Agent 不存在: {agent_name}',
                    agent_name=agent_name,
                    duration=0
                )
            if not agent.is_available():
                return AgentResult(
                    success=False,
                    output='',
                    error=f'Agent 不可用: {agent_name}',
                    agent_name=agent_name,
                    duration=0
                )
        else:
            available = self.registry.get_available()
            if not available:
                return AgentResult(
                    success=False,
                    output='',
                    error='没有可用的 Agent',
                    agent_name='none',
                    duration=0
                )
            agent = available[0]
        
        self.logger.info(f"使用 {agent.name} 执行任务: {task.id}" + (f" (模型: {model})" if model else ""))
        return agent.execute(task, model=model)
    
    def execute_with_fallback(self, task, agents: List[str] = None) -> AgentResult:
        """执行任务，失败时自动切换备用 agent
        
        Args:
            task: 任务对象
            agents: agent 名称列表，None 则使用所有可用的
        
        Returns:
            AgentResult
        """
        if agents is None:
            agents = [a.name for a in self.registry.get_available()]
        
        if not agents:
            return AgentResult(
                success=False,
                output='',
                error='没有可用的 Agent',
                agent_name='none',
                duration=0
            )
        
        attempts = []
        for agent_name in agents:
            self.logger.info(f"尝试 agent: {agent_name}")
            result = self.execute_task(task, agent_name)
            attempts.append({
                'agent': agent_name,
                'success': result.success,
                'error': result.error
            })
            
            if result.success:
                result.metadata['attempts'] = attempts
                self.logger.info(f"Agent {agent_name} 执行成功")
                return result
            else:
                self.logger.warning(f"Agent {agent_name} 失败: {result.error[:100]}")
        
        # 所有 agents 都失败
        self.logger.error("所有 agents 执行失败")
        return AgentResult(
            success=False,
            output='',
            error=f"所有 agents 执行失败。尝试了: {', '.join(agents)}",
            agent_name='none',
            duration=0,
            metadata={'attempts': attempts}
        )
