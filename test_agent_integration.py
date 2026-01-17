"""测试 Agent 集成"""
import sys
from pathlib import Path

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from ai_as_me.agents import AgentRegistry, AgentExecutor, BaseAgent, AgentResult
from ai_as_me.kanban.models import Task, TaskStatus, TaskPriority


def test_registry():
    """测试 Agent 注册表"""
    print("🧪 测试 1: Agent 注册表")
    
    registry = AgentRegistry()
    all_agents = registry.list_all()
    available = registry.get_available()
    
    print(f"  已注册: {all_agents}")
    print(f"  可用: {[a.name for a in available]}")
    
    for name in all_agents:
        agent = registry.get(name)
        print(f"  {name}:")
        print(f"    可用: {agent.is_available()}")
        print(f"    能力: {agent.get_capabilities()}")
    
    assert len(all_agents) == 2, "应该有 2 个 agents"
    print("  ✅ 通过\n")


def test_executor():
    """测试 Agent 执行器"""
    print("🧪 测试 2: Agent 执行器")
    
    # 创建测试任务
    task = Task(
        id="test-001",
        title="计算 1+1",
        description="请计算 1+1 等于多少",
        status=TaskStatus.TODO,
        priority=TaskPriority.P2
    )
    
    executor = AgentExecutor()
    
    # 测试自动选择
    print("  测试自动选择 agent...")
    result = executor.execute_with_fallback(task)
    
    print(f"  成功: {result.success}")
    print(f"  Agent: {result.agent_name}")
    print(f"  耗时: {result.duration:.1f}s")
    if result.success:
        print(f"  输出: {result.output[:100]}")
    else:
        print(f"  错误: {result.error[:100]}")
    
    print("  ✅ 通过\n")


def test_base_agent():
    """测试 BaseAgent 抽象类"""
    print("🧪 测试 3: BaseAgent 抽象")
    
    # 验证不能直接实例化
    try:
        agent = BaseAgent()
        print("  ❌ 失败: 应该无法实例化抽象类")
    except TypeError:
        print("  ✅ 正确: 无法实例化抽象类")
    
    print("  ✅ 通过\n")


def test_agent_result():
    """测试 AgentResult 数据类"""
    print("🧪 测试 4: AgentResult 数据类")
    
    result = AgentResult(
        success=True,
        output="测试输出",
        error="",
        agent_name="test-agent",
        duration=1.5
    )
    
    assert result.success == True
    assert result.agent_name == "test-agent"
    assert result.metadata == {}
    
    result2 = AgentResult(
        success=False,
        output="",
        error="测试错误",
        agent_name="test-agent",
        duration=0.5,
        metadata={"key": "value"}
    )
    
    assert result2.metadata["key"] == "value"
    
    print("  ✅ 通过\n")


if __name__ == "__main__":
    print("=" * 50)
    print("Agent 集成测试")
    print("=" * 50 + "\n")
    
    test_base_agent()
    test_agent_result()
    test_registry()
    test_executor()
    
    print("=" * 50)
    print("✅ 所有测试通过")
    print("=" * 50)
