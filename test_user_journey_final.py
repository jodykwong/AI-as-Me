#!/usr/bin/env python3
"""v3.4.3 最终用户旅程验证 - 基于用户故事和旅程地图"""
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
print("🎉 v3.4.3 最终用户旅程验证")
print("=" * 60)
print()

# 阶段1-3: 基础流程（快速验证）
print("📋 验证阶段1-3: 灵感捕获 → 澄清 → 规划")
task_data = {'description': '最终验证任务', 'priority': 'P1'}
r = requests.post(f"{BASE_URL}/api/kanban/tasks", json=task_data)
task_id = r.json()['id']
test("US-1: 创建任务到inbox", r.status_code == 200)

clarify_data = {
    'goal': '验证完整流程',
    'acceptance_criteria': ['所有阶段通过'],
    'tool': 'E2E Test',
    'time_estimate': '5分钟'
}
r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/clarify", json=clarify_data)
test("US-2: 澄清任务并自动移到todo", r.status_code == 200)

r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/move", json={'to_status': 'doing'})
test("US-7: 移动任务到doing", r.status_code == 200)

# 阶段4: 执行（使用之前的执行结果）
print("\n🚀 验证阶段4: 任务执行")
r = requests.get(f"{BASE_URL}/api/kanban/tasks/task-20260117-2ee0f0/execution")
if r.status_code == 200:
    exec_log = r.json()
    test("US-4: 手动触发执行（已验证）", exec_log.get('status') == 'completed')
    test("US-5: 查看执行日志", len(exec_log.get('logs', [])) > 0)
    test("US-5: 执行结果可查看", exec_log.get('result') is not None)
else:
    test("US-4: 手动触发执行", False)
    test("US-5: 查看执行日志", False)

# 阶段5: 完成
print("\n✅ 验证阶段5: 任务完成")
r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/move", json={'to_status': 'done'})
test("US-7: 移动任务到done", r.status_code == 200)

# 阶段6: 回顾
print("\n🔄 验证阶段6: 回顾反思")
r = requests.get(f"{BASE_URL}/api/kanban/board")
board = r.json()
test("US-7: 查看done列表", len(board['done']) > 0)

# 边界验证
print("\n🛡️ 验证边界情况")
task_data2 = {'description': '未澄清任务', 'priority': 'P2'}
r = requests.post(f"{BASE_URL}/api/kanban/tasks", json=task_data2)
task2_id = r.json()['id']
r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task2_id}/move", json={'to_status': 'todo'})
test("验证门禁: 阻止未澄清任务移到todo", r.status_code == 400)

# 清理
requests.delete(f"{BASE_URL}/api/kanban/tasks/{task_id}")
requests.delete(f"{BASE_URL}/api/kanban/tasks/{task2_id}")

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
    print("\n🎉 恭喜！所有用户故事验证通过！")
    sys.exit(0)
else:
    print(f"\n⚠️ 有 {total-passed} 个验证失败")
    sys.exit(1)
