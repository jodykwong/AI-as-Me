#!/usr/bin/env python3
"""Agent集成验证 - 基于更新的用户故事"""
import requests
import sys
from pathlib import Path

BASE_URL = "http://localhost:8000"
results = []

def test(name, passed):
    results.append((name, passed))
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status} - {name}")

print("=" * 60)
print("🤖 Agent集成验证")
print("=" * 60)
print()

# 阶段1-3: 基础流程
print("📋 验证阶段1-3: 灵感捕获 → 澄清 → 规划")
task_data = {'description': 'Agent集成测试任务', 'priority': 'P1'}
r = requests.post(f"{BASE_URL}/api/kanban/tasks", json=task_data)
task_id = r.json()['id']
test("US-1: 创建任务到inbox", r.status_code == 200)

clarify_data = {
    'goal': '验证Agent集成',
    'acceptance_criteria': ['Agent能检测任务', 'Agent能执行任务'],
    'tool': 'Agent',
    'time_estimate': '自动'
}
r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/clarify", json=clarify_data)
test("US-2: 澄清任务并自动移到todo", r.status_code == 200)

r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/move", json={'to_status': 'doing'})
test("US-3: 移动任务到doing", r.status_code == 200)

# 阶段4: Agent状态监控
print("\n🤖 验证阶段4: Agent状态监控")
r = requests.get(f"{BASE_URL}/api/agent/status")
if r.status_code == 200:
    agent_status = r.json()
    test("US-4: 获取Agent状态", True)
    test("US-4: Agent状态包含运行信息", 'agent' in agent_status)
    test("US-4: Agent状态包含doing任务数", 'doing_count' in agent_status)
    test("US-4: Agent状态包含消息", 'message' in agent_status)
    
    print(f"\n  Agent状态: {agent_status['message']}")
    print(f"  Doing任务数: {agent_status['doing_count']}")
    if agent_status['agent']['running']:
        print(f"  Agent PID: {agent_status['agent']['pid']}")
else:
    test("US-4: 获取Agent状态", False)

# Agent健康检查
r = requests.get(f"{BASE_URL}/api/agent/health")
test("US-4: Agent健康检查API", r.status_code == 200)

# 阶段5: 任务详情
print("\n📋 验证阶段5: 任务详情")
r = requests.get(f"{BASE_URL}/api/kanban/tasks/{task_id}")
if r.status_code == 200:
    task = r.json()
    test("US-7: 获取任务详情", True)
    test("US-7: 任务包含标题", 'title' in task)
    test("US-7: 任务包含描述", 'description' in task)
    test("US-7: 任务包含澄清信息", task.get('clarified') == True)
    test("US-7: 任务包含优先级", 'priority' in task)
else:
    test("US-7: 获取任务详情", False)

# 阶段6: 看板查看
print("\n📊 验证阶段6: 看板查看")
r = requests.get(f"{BASE_URL}/api/kanban/board")
if r.status_code == 200:
    board = r.json()
    test("US-6: 获取看板数据", True)
    test("US-6: 看板包含inbox列", 'inbox' in board)
    test("US-6: 看板包含todo列", 'todo' in board)
    test("US-6: 看板包含doing列", 'doing' in board)
    test("US-6: 看板包含done列", 'done' in board)
else:
    test("US-6: 获取看板数据", False)

# 清理
print("\n🧹 清理测试数据")
r = requests.delete(f"{BASE_URL}/api/kanban/tasks/{task_id}")
test("清理测试任务", r.status_code == 200)

# 汇总
print("\n" + "=" * 60)
print("📊 验证结果汇总")
print("=" * 60)
passed = sum(1 for _, ok in results if ok)
total = len(results)

for name, ok in results:
    status = "✅" if ok else "❌"
    print(f"{status} {name}")

print(f"\n总计: {passed}/{total} 通过 ({passed*100//total}%)")

if passed == total:
    print("\n🎉 恭喜！所有Agent集成验证通过！")
    print("\n💡 提示：启动Agent后台服务以实现自动执行：")
    print("   python start_agent.py")
    sys.exit(0)
else:
    print(f"\n⚠️ 有 {total-passed} 个验证失败")
    sys.exit(1)
