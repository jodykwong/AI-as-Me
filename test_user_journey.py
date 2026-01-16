#!/usr/bin/env python3
"""
E2E User Journey Validation - v3.4.3
基于用户旅程地图的完整端到端测试
"""
import requests
import json
import time
from pathlib import Path

BASE_URL = "http://localhost:8000"
KANBAN_DIR = Path("/home/sunrise/AI-as-Me/kanban")

class Colors:
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    END = '\033[0m'

def log_stage(stage, emoji):
    print(f"\n{'='*60}")
    print(f"{emoji} {stage}")
    print('='*60)

def log_step(step, status=""):
    symbol = "✅" if status == "PASS" else "❌" if status == "FAIL" else "🔍"
    print(f"{symbol} {step}")

def verify_file(path, should_exist=True):
    exists = path.exists()
    if should_exist:
        if exists:
            log_step(f"文件存在: {path.name}", "PASS")
            return True
        else:
            log_step(f"文件不存在: {path.name}", "FAIL")
            return False
    else:
        if not exists:
            log_step(f"文件已删除: {path.name}", "PASS")
            return True
        else:
            log_step(f"文件仍存在: {path.name}", "FAIL")
            return False

results = []
task_id = None

try:
    # ========================================
    # 阶段1: 灵感捕获 💡
    # ========================================
    log_stage("阶段1: 灵感捕获", "💡")
    
    log_step("1.1 访问Kanban页面")
    r = requests.get(f"{BASE_URL}/kanban.html", timeout=5)
    if r.status_code == 200:
        log_step("Kanban页面可访问", "PASS")
        results.append(("访问Kanban页面", True))
    else:
        log_step(f"Kanban页面访问失败: {r.status_code}", "FAIL")
        results.append(("访问Kanban页面", False))
    
    log_step("1.2 创建新任务到inbox")
    task_data = {
        "title": "E2E测试任务 - 用户旅程验证",
        "description": "这是一个完整的用户旅程测试任务，用于验证v3.4.3的所有功能",
        "priority": "P1"
    }
    r = requests.post(f"{BASE_URL}/api/kanban/tasks", json=task_data, timeout=5)
    if r.status_code == 200:
        task = r.json()
        task_id = task.get("id")
        log_step(f"任务创建成功: {task_id}", "PASS")
        results.append(("创建任务", True))
        
        log_step("1.3 验证任务在inbox")
        r = requests.get(f"{BASE_URL}/api/kanban/board", timeout=5)
        board = r.json()
        inbox_tasks = [t for t in board["inbox"] if t["id"] == task_id]
        if inbox_tasks:
            log_step("任务出现在inbox列", "PASS")
            results.append(("任务在inbox", True))
        else:
            log_step("任务未出现在inbox列", "FAIL")
            results.append(("任务在inbox", False))
        
        log_step("1.4 验证Markdown文件创建")
        task_file = KANBAN_DIR / "inbox" / f"{task_id}.md"
        if verify_file(task_file):
            results.append(("创建inbox文件", True))
        else:
            results.append(("创建inbox文件", False))
    else:
        log_step(f"任务创建失败: {r.status_code}", "FAIL")
        results.append(("创建任务", False))
        raise Exception("无法创建任务，终止测试")
    
    time.sleep(0.5)
    
    # ========================================
    # 阶段2: 任务澄清 🎯
    # ========================================
    log_stage("阶段2: 任务澄清", "🎯")
    
    log_step("2.1 获取任务详情")
    r = requests.get(f"{BASE_URL}/api/kanban/tasks/{task_id}", timeout=5)
    if r.status_code == 200:
        task = r.json()
        log_step(f"任务状态: {task['status']}, 已澄清: {task['clarified']}", "PASS")
        results.append(("获取任务详情", True))
    else:
        log_step(f"获取任务失败: {r.status_code}", "FAIL")
        results.append(("获取任务详情", False))
    
    log_step("2.2 澄清任务")
    clarify_data = {
        "goal": "验证v3.4.3的完整用户旅程，确保所有功能按预期工作",
        "acceptance_criteria": [
            "所有6个旅程阶段都能正常执行",
            "任务文件在各状态目录间正确移动",
            "验证门禁正确阻止非法状态转换",
            "UI显示正确的任务信息"
        ],
        "tool": "Python + requests + 文件系统验证",
        "time_estimate": "10分钟"
    }
    r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/clarify", json=clarify_data, timeout=5)
    if r.status_code == 200:
        log_step("任务澄清成功", "PASS")
        results.append(("澄清任务", True))
        
        log_step("2.3 验证任务自动移到todo")
        r = requests.get(f"{BASE_URL}/api/kanban/board", timeout=5)
        board = r.json()
        todo_tasks = [t for t in board["todo"] if t["id"] == task_id]
        if todo_tasks and todo_tasks[0]["clarified"]:
            log_step("任务已移到todo且clarified=true", "PASS")
            results.append(("任务移到todo", True))
        else:
            log_step("任务未正确移到todo", "FAIL")
            results.append(("任务移到todo", False))
        
        log_step("2.4 验证文件移动到todo目录")
        old_file = KANBAN_DIR / "inbox" / f"{task_id}.md"
        new_file = KANBAN_DIR / "todo" / f"{task_id}.md"
        if verify_file(old_file, should_exist=False) and verify_file(new_file):
            results.append(("文件移到todo", True))
        else:
            results.append(("文件移到todo", False))
    else:
        log_step(f"任务澄清失败: {r.status_code} - {r.text}", "FAIL")
        results.append(("澄清任务", False))
    
    time.sleep(0.5)
    
    # ========================================
    # 阶段3: 任务规划 📋
    # ========================================
    log_stage("阶段3: 任务规划", "📋")
    
    log_step("3.1 查看todo列表")
    r = requests.get(f"{BASE_URL}/api/kanban/board", timeout=5)
    board = r.json()
    todo_count = len(board["todo"])
    log_step(f"Todo列表有 {todo_count} 个任务", "PASS")
    results.append(("查看todo列表", True))
    
    log_step("3.2 移动任务到doing")
    move_data = {"to_status": "doing"}
    r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/move", json=move_data, timeout=5)
    if r.status_code == 200:
        log_step("任务移到doing成功", "PASS")
        results.append(("移动到doing", True))
        
        log_step("3.3 验证文件移动到doing目录")
        old_file = KANBAN_DIR / "todo" / f"{task_id}.md"
        new_file = KANBAN_DIR / "doing" / f"{task_id}.md"
        if verify_file(old_file, should_exist=False) and verify_file(new_file):
            results.append(("文件移到doing", True))
        else:
            results.append(("文件移到doing", False))
    else:
        log_step(f"移动失败: {r.status_code}", "FAIL")
        results.append(("移动到doing", False))
    
    time.sleep(0.5)
    
    # ========================================
    # 阶段4: 任务执行 🚀
    # ========================================
    log_stage("阶段4: 任务执行", "🚀")
    
    log_step("4.1 查看任务详情（执行中）")
    r = requests.get(f"{BASE_URL}/api/kanban/tasks/{task_id}", timeout=5)
    if r.status_code == 200:
        task = r.json()
        log_step(f"任务状态: {task['status']}", "PASS")
        
        if task.get("clarification"):
            clarif = task["clarification"]
            log_step(f"目标: {clarif.get('goal', '')[:50]}...", "PASS")
            log_step(f"验收标准数量: {len(clarif.get('acceptance_criteria', []))}", "PASS")
            log_step(f"工具: {clarif.get('tool', '')}", "PASS")
            log_step(f"时间估算: {clarif.get('time_estimate', '')}", "PASS")
            results.append(("查看执行详情", True))
        else:
            log_step("缺少澄清信息", "FAIL")
            results.append(("查看执行详情", False))
    else:
        log_step(f"获取任务失败: {r.status_code}", "FAIL")
        results.append(("查看执行详情", False))
    
    time.sleep(0.5)
    
    # ========================================
    # 阶段5: 任务完成 ✅
    # ========================================
    log_stage("阶段5: 任务完成", "✅")
    
    log_step("5.1 移动任务到done")
    move_data = {"to_status": "done"}
    r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/move", json=move_data, timeout=5)
    if r.status_code == 200:
        log_step("任务标记为完成", "PASS")
        results.append(("移动到done", True))
        
        log_step("5.2 验证文件移动到done目录")
        old_file = KANBAN_DIR / "doing" / f"{task_id}.md"
        new_file = KANBAN_DIR / "done" / f"{task_id}.md"
        if verify_file(old_file, should_exist=False) and verify_file(new_file):
            results.append(("文件移到done", True))
        else:
            results.append(("文件移到done", False))
    else:
        log_step(f"移动失败: {r.status_code}", "FAIL")
        results.append(("移动到done", False))
    
    time.sleep(0.5)
    
    # ========================================
    # 阶段6: 回顾反思 🔄
    # ========================================
    log_stage("阶段6: 回顾反思", "🔄")
    
    log_step("6.1 查看done列表")
    r = requests.get(f"{BASE_URL}/api/kanban/board", timeout=5)
    board = r.json()
    done_tasks = [t for t in board["done"] if t["id"] == task_id]
    if done_tasks:
        log_step(f"Done列表包含已完成任务", "PASS")
        results.append(("查看done列表", True))
    else:
        log_step("Done列表未找到任务", "FAIL")
        results.append(("查看done列表", False))
    
    log_step("6.2 查看已完成任务详情")
    r = requests.get(f"{BASE_URL}/api/kanban/tasks/{task_id}", timeout=5)
    if r.status_code == 200:
        task = r.json()
        log_step(f"任务最终状态: {task['status']}", "PASS")
        results.append(("查看完成详情", True))
    else:
        log_step("获取任务失败", "FAIL")
        results.append(("查看完成详情", False))
    
    # ========================================
    # 边界情况验证 🛡️
    # ========================================
    log_stage("边界情况验证", "🛡️")
    
    log_step("7.1 创建未澄清任务")
    task_data2 = {
        "title": "未澄清测试任务",
        "description": "用于测试验证门禁",
        "priority": "P2"
    }
    r = requests.post(f"{BASE_URL}/api/kanban/tasks", json=task_data2, timeout=5)
    if r.status_code == 200:
        task2 = r.json()
        task2_id = task2.get("id")
        log_step(f"创建测试任务: {task2_id}", "PASS")
        
        log_step("7.2 尝试移动未澄清任务到todo（应该失败）")
        move_data = {"to_status": "todo"}
        r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task2_id}/move", json=move_data, timeout=5)
        if r.status_code == 400:
            log_step("验证门禁正确阻止了非法移动", "PASS")
            results.append(("验证门禁", True))
        else:
            log_step(f"验证门禁失败，返回: {r.status_code}", "FAIL")
            results.append(("验证门禁", False))
        
        log_step("7.3 清理测试任务")
        r = requests.delete(f"{BASE_URL}/api/kanban/tasks/{task2_id}", timeout=5)
        if r.status_code == 200:
            log_step("测试任务已删除", "PASS")
            task2_file = KANBAN_DIR / "inbox" / f"{task2_id}.md"
            verify_file(task2_file, should_exist=False)
            results.append(("删除任务", True))
        else:
            log_step("删除失败", "FAIL")
            results.append(("删除任务", False))
    
    # ========================================
    # 清理主测试任务
    # ========================================
    log_stage("清理测试数据", "🧹")
    if task_id:
        r = requests.delete(f"{BASE_URL}/api/kanban/tasks/{task_id}", timeout=5)
        if r.status_code == 200:
            log_step(f"主测试任务已删除: {task_id}", "PASS")
        else:
            log_step(f"删除主任务失败: {r.status_code}", "FAIL")

except Exception as e:
    print(f"\n❌ 测试异常: {e}")
    results.append(("测试执行", False))

# ========================================
# 汇总报告
# ========================================
print("\n" + "="*60)
print("📊 用户旅程验证汇总")
print("="*60)

passed = sum(1 for _, ok in results if ok)
total = len(results)

for name, ok in results:
    status = f"{Colors.GREEN}✅ PASS{Colors.END}" if ok else f"{Colors.RED}❌ FAIL{Colors.END}"
    print(f"{status} - {name}")

print(f"\n总计: {passed}/{total} 通过 ({passed*100//total if total > 0 else 0}%)")

if passed == total:
    print(f"\n{Colors.GREEN}🎉 恭喜！完整用户旅程验证通过！{Colors.END}")
    exit(0)
else:
    print(f"\n{Colors.YELLOW}⚠️ 有 {total-passed} 个测试失败，需要修复{Colors.END}")
    exit(1)
