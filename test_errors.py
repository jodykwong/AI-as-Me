#!/usr/bin/env python3
from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    errors = []
    page.on("pageerror", lambda e: errors.append(str(e)))
    
    console_logs = []
    page.on("console", lambda m: console_logs.append(f"[{m.type}] {m.text}"))
    
    page.goto("http://192.168.8.166:8080/kanban.html")
    page.wait_for_timeout(5000)
    
    print("=== 页面错误 ===")
    for e in errors:
        print(e)
    
    print("\n=== 控制台日志 ===")
    for log in console_logs:
        if 'error' in log.lower() or 'warning' in log.lower():
            print(log)
    
    # 检查 kanbanApp 是否可调用
    try:
        result = page.evaluate("typeof kanbanApp")
        print(f"\nkanbanApp 类型: {result}")
        
        if result == "function":
            # 尝试调用
            test = page.evaluate("kanbanApp()")
            print(f"kanbanApp() 返回: {type(test)}")
    except Exception as e:
        print(f"\n调用 kanbanApp 失败: {e}")
    
    browser.close()
