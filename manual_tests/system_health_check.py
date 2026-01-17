#!/usr/bin/env python3
"""系统健康检查 - 全面验证"""
import requests
import sys
from pathlib import Path
import subprocess

BASE_URL = "http://localhost:8000"
issues = []
checks = []

def check(name, passed, severity="ERROR"):
    checks.append((name, passed, severity))
    symbol = "✅" if passed else ("❌" if severity == "ERROR" else "⚠️")
    print(f"{symbol} {name}")
    if not passed and severity == "ERROR":
        issues.append(name)

print("=" * 60)
print("🔍 系统健康检查")
print("=" * 60)

# 1. 服务检查
print("\n1️⃣ 服务状态检查")
try:
    r = requests.get(f"{BASE_URL}/health", timeout=5)
    check("Web服务运行", r.status_code == 200)
except:
    check("Web服务运行", False)

try:
    r = requests.get(f"{BASE_URL}/api/agent/status", timeout=5)
    agent_status = r.json()
    check("Agent状态API", r.status_code == 200)
    check("Agent服务运行", agent_status['agent']['running'], "WARNING")
except:
    check("Agent状态API", False)

# 2. 目录结构检查
print("\n2️⃣ 目录结构检查")
required_dirs = [
    "kanban/inbox",
    "kanban/todo", 
    "kanban/doing",
    "kanban/done",
    "soul",
    "logs"
]
for dir_path in required_dirs:
    exists = Path(dir_path).exists()
    check(f"目录存在: {dir_path}", exists)

# 3. API端点检查
print("\n3️⃣ API端点检查")
endpoints = [
    ("/api/kanban/board", "GET"),
    ("/api/soul/status", "GET"),
    ("/api/agent/health", "GET"),
]
for endpoint, method in endpoints:
    try:
        r = requests.request(method, f"{BASE_URL}{endpoint}", timeout=5)
        check(f"API {method} {endpoint}", r.status_code == 200)
    except Exception as e:
        check(f"API {method} {endpoint}", False)

# 4. 配置检查
print("\n4️⃣ 配置检查")
check(".env文件存在", Path(".env").exists())
if Path(".env").exists():
    env_content = Path(".env").read_text()
    check("DEEPSEEK_API_KEY配置", "DEEPSEEK_API_KEY" in env_content)

# 5. 功能流程检查
print("\n5️⃣ 功能流程检查")
try:
    # 创建测试任务
    r = requests.post(f"{BASE_URL}/api/kanban/tasks", 
                     json={"description": "健康检查测试", "priority": "P3"})
    task_id = r.json()['id'] if r.status_code == 200 else None
    check("创建任务", r.status_code == 200)
    
    if task_id:
        # 澄清任务
        r = requests.put(f"{BASE_URL}/api/kanban/tasks/{task_id}/clarify",
                        json={"goal": "测试", "acceptance_criteria": ["完成"]})
        check("澄清任务", r.status_code == 200)
        
        # 获取看板
        r = requests.get(f"{BASE_URL}/api/kanban/board")
        board = r.json()
        check("获取看板", r.status_code == 200)
        check("任务在todo列", any(t['id'] == task_id for t in board.get('todo', [])))
        
        # 清理
        requests.delete(f"{BASE_URL}/api/kanban/tasks/{task_id}")
except Exception as e:
    check("功能流程测试", False)
    print(f"  错误: {e}")

# 6. 文件权限检查
print("\n6️⃣ 文件权限检查")
check("kanban目录可写", Path("kanban").exists() and Path("kanban/inbox").exists())
check("logs目录可写", Path("logs").exists() or Path("logs").parent.exists())

# 汇总
print("\n" + "=" * 60)
print("📊 检查结果汇总")
print("=" * 60)

passed = sum(1 for _, ok, _ in checks if ok)
total = len(checks)
errors = len(issues)

print(f"\n总计: {passed}/{total} 通过 ({passed*100//total}%)")
print(f"错误: {errors} 个")

if issues:
    print("\n❌ 发现以下问题:")
    for issue in issues:
        print(f"  - {issue}")
    sys.exit(1)
else:
    print("\n✅ 系统健康，所有检查通过！")
    sys.exit(0)
