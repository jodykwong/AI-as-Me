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
        import time
        start_time = time.time()
        
        # 更新任务状态为准备中
        self._update_task_phase(task, "PREPARING", 10)

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

        # 更新任务状态为分析中
        self._update_task_phase(task, "ANALYZING", 30)

        if agent_name:
            agent = self.registry.get(agent_name)
            if not agent:
                available_agents = self.registry.list_all()
                error_msg = f'Agent "{agent_name}" 不存在。可用的 Agents: {", ".join(available_agents)}'
                self.logger.error(error_msg)
                self._update_task_phase(task, "FAILED", 0)
                return AgentResult(
                    success=False,
                    output='',
                    error=error_msg,
                    agent_name=agent_name,
                    duration=time.time() - start_time,
                    metadata={'available_agents': available_agents, 'model': model}
                )
            if not agent.is_available():
                error_msg = f'Agent "{agent_name}" 不可用。请检查依赖配置。'
                self.logger.error(error_msg)
                return AgentResult(
                    success=False,
                    output='',
                    error=error_msg,
                    agent_name=agent_name,
                    duration=time.time() - start_time,
                    metadata={'model': model}
                )
        else:
            available = self.registry.get_available()
            if not available:
                error_msg = '没有可用的 Agent。请检查 Agent 配置。'
                self.logger.error(error_msg)
                return AgentResult(
                    success=False,
                    output='',
                    error=error_msg,
                    agent_name='none',
                    duration=time.time() - start_time
                )
            agent = available[0]

        task_id = getattr(task, 'id', getattr(task, 'title', 'unknown'))
        model_info = f" [模型: {model}]" if model else ""
        self.logger.info(f"执行任务 {task_id} 使用 Agent: {agent.name}{model_info}")

        # 更新任务状态为执行中
        self._update_task_phase(task, "EXECUTING", 50)
        
        result = agent.execute(task, model=model)

        # 更新任务状态为验证中
        self._update_task_phase(task, "VALIDATING", 90)

        # 增强元数据
        result.metadata['model'] = model
        result.metadata['task_id'] = task_id
        result.metadata['timestamp'] = start_time

        # 根据结果更新最终状态
        if result.success:
            self._update_task_phase(task, "COMPLETED", 100)
        else:
            self._update_task_phase(task, "FAILED", 0)

        self.logger.info(f"任务 {task_id} {'成功' if result.success else '失败'} (耗时: {result.duration:.2f}s)")
        return result
    
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
    def _update_task_phase(self, task, phase: str, progress: int = None):
        """更新任务执行阶段和进度"""
        try:
            from ..kanban.database import KanbanDatabase
            db = KanbanDatabase()
            db.update_task_phase(task.id, phase, progress)
        except Exception as e:
            self.logger.warning(f"更新任务阶段失败: {e}")
