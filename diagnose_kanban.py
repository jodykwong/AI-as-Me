#!/usr/bin/env python3
"""Kanban创建任务诊断SOP"""
import requests
import json
from playwright.sync_api import sync_playwright
import time

BASE_URL = "http://192.168.8.166:8080"

print("=" * 60)
print("Kanban 创建任务诊断 SOP")
print("=" * 60)

# 1. 服务器连通性
print("\n[1/6] 检查服务器连通性...")
try:
    r = requests.get(f"{BASE_URL}/api/health", timeout=5)
    print(f"✓ 服务器响应: {r.status_code}")
except Exception as e:
    print(f"✗ 服务器无响应: {e}")
    exit(1)

# 2. API端点测试
print("\n[2/6] 测试API端点...")
try:
    r = requests.post(f"{BASE_URL}/api/kanban/tasks", 
                     json={"description": "SOP诊断测试", "priority": "P2"},
                     timeout=5)
    print(f"✓ POST /api/kanban/tasks: {r.status_code}")
    if r.status_code == 200:
        task_id = r.json().get('id')
        print(f"  任务ID: {task_id}")
    else:
        print(f"  错误: {r.text}")
except Exception as e:
    print(f"✗ API调用失败: {e}")

# 3. 看板数据完整性
print("\n[3/6] 检查看板数据...")
try:
    r = requests.get(f"{BASE_URL}/api/kanban/board", timeout=5)
    board = r.json()
    print(f"✓ 看板数据获取成功")
    for status in ['inbox', 'todo', 'doing', 'done']:
        tasks = board.get(status, [])
        empty_ids = [t for t in tasks if not t.get('id')]
        print(f"  {status}: {len(tasks)}个任务, {len(empty_ids)}个空ID")
        if empty_ids:
            print(f"    ✗ 发现空ID任务!")
except Exception as e:
    print(f"✗ 获取看板失败: {e}")

# 4. 前端页面加载
print("\n[4/6] 检查前端页面...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    
    page.goto(f"{BASE_URL}/kanban.html")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    # 检查Alpine初始化
    alpine_ok = page.evaluate("() => typeof Alpine !== 'undefined'")
    print(f"  Alpine.js加载: {'✓' if alpine_ok else '✗'}")
    
    # 检查x-data
    has_scope = page.evaluate("() => !!document.querySelector('[x-data]')?.__x?.$data")
    print(f"  Alpine作用域: {'✓' if has_scope else '✗'}")
    
    # 检查按钮
    btn = page.locator("button:has-text('创建任务')")
    print(f"  创建按钮存在: {'✓' if btn.count() > 0 else '✗'}")
    print(f"  按钮可见: {'✓' if btn.is_visible() else '✗'}")
    print(f"  按钮禁用: {'✗ 已禁用' if btn.is_disabled() else '✓ 可点击'}")
    
    if errors:
        print(f"  ✗ 页面错误: {len(errors)}个")
        for e in errors[:3]:
            print(f"    - {e[:100]}")
    else:
        print(f"  ✓ 无页面错误")
    
    browser.close()

# 5. 完整点击流程测试
print("\n[5/6] 测试完整点击流程...")
with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    console_logs = []
    api_calls = []
    
    page.on("console", lambda m: console_logs.append(m.text))
    page.on("response", lambda r: api_calls.append(f"{r.status} {r.url}") if '/api/' in r.url else None)
    
    page.goto(f"{BASE_URL}/kanban.html")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    # 获取初始任务数
    initial_count = page.evaluate("() => document.querySelector('[x-data]')?.__x?.$data?.board?.inbox?.length || 0")
    print(f"  初始inbox任务数: {initial_count}")
    
    # 填写并点击
    page.fill("input[placeholder*='任务']", "SOP完整测试")
    page.click("button:has-text('创建任务')")
    time.sleep(3)
    
    # 检查结果
    final_count = page.evaluate("() => document.querySelector('[x-data]')?.__x?.$data?.board?.inbox?.length || 0")
    print(f"  最终inbox任务数: {final_count}")
    print(f"  任务数变化: {'+' if final_count > initial_count else '='}{final_count - initial_count}")
    
    # 检查API调用
    create_calls = [c for c in api_calls if 'POST' in c or '/tasks' in c]
    print(f"  创建API调用: {len(create_calls)}次")
    for call in create_calls:
        print(f"    {call}")
    
    # 检查关键日志
    create_logs = [l for l in console_logs if 'createTask' in l or 'Response status' in l]
    print(f"  关键日志: {len(create_logs)}条")
    for log in create_logs[:5]:
        print(f"    {log}")
    
    browser.close()

# 6. 诊断结论
print("\n[6/6] 诊断结论")
print("=" * 60)
print("请检查以上输出，重点关注:")
print("1. 是否有空ID任务")
print("2. Alpine作用域是否正常")
print("3. 任务数是否增加")
print("4. API调用是否成功")
print("=" * 60)
