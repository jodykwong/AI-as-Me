#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    
    page.goto("http://192.168.8.166:8080/kanban.html")
    time.sleep(5)
    
    print(f"错误数: {len(errors)}")
    if errors:
        for e in errors[:3]:
            print(f"  {e}")
    
    # 尝试点击
    try:
        page.fill("input[x-model='newTask']", "测试")
        page.click("button:has-text('创建任务')")
        time.sleep(2)
        print("✓ 点击成功")
    except Exception as e:
        print(f"❌ 点击失败: {e}")
    
    browser.close()
