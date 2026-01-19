"""测试工具和模型配置"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from ai_as_me.kanban.models import Task, TaskStatus, TaskPriority, TaskClarification
from ai_as_me.agents import AgentExecutor

print("=" * 60)
print("测试工具和模型配置")
print("=" * 60 + "\n")

# 测试 1: 任务配置 OpenCode + 正确模型
print("🧪 测试 1: 任务配置 opencode:opencode/big-pickle")
task1 = Task(
    id='test-001',
    title='计算 3+3',
    description='请计算 3+3',
    status=TaskStatus.TODO,
    priority=TaskPriority.P2,
    clarification=TaskClarification(
        goal='计算结果',
        tool='opencode:opencode/big-pickle'
    )
)

executor = AgentExecutor()
result1 = executor.execute_task(task1)

print(f"  成功: {result1.success}")
print(f"  Agent: {result1.agent_name}")
print(f"  模型: {result1.metadata.get('model')}")
print(f"  输出: {result1.output.strip()[:50]}")
print()

# 测试 2: 命令行指定模型（覆盖任务配置）
print("🧪 测试 2: 命令行指定 claude-code:sonnet")
task2 = Task(
    id='test-002',
    title='计算 4+4',
    description='请计算 4+4',
    status=TaskStatus.TODO,
    priority=TaskPriority.P2
)

result2 = executor.execute_task(task2, 'claude-code:sonnet')

print(f"  成功: {result2.success}")
print(f"  Agent: {result2.agent_name}")
print(f"  模型: {result2.metadata.get('model')}")
if result2.success:
    print(f"  输出: {result2.output.strip()[:50]}")
else:
    print(f"  错误: {result2.error[:100]}")
print()

# 测试 3: 无配置（自动选择）
print("🧪 测试 3: 无配置，自动选择")
task3 = Task(
    id='test-003',
    title='计算 5+5',
    description='请计算 5+5',
    status=TaskStatus.TODO,
    priority=TaskPriority.P2
)

result3 = executor.execute_task(task3)

print(f"  成功: {result3.success}")
print(f"  Agent: {result3.agent_name}")
print(f"  模型: {result3.metadata.get('model')}")
print(f"  输出: {result3.output.strip()[:50]}")
print()

print("=" * 60)
print("✅ 测试完成")
print("=" * 60)
