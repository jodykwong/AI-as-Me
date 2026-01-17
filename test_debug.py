#!/usr/bin/env python3
from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    # 监听所有日志
    def log_console(msg):
        print(f"[{msg.type}] {msg.text}")
    page.on("console", log_console)
    
    page.goto("http://192.168.8.166:8080/kanban.html")
    time.sleep(3)
    
    # 检查Alpine是否初始化
    alpine_exists = page.evaluate("typeof Alpine")
    kanban_exists = page.evaluate("typeof kanbanApp")
    print(f"\nAlpine: {alpine_exists}, kanbanApp: {kanban_exists}")
    
    # 检查x-data是否绑定
    has_xdata = page.evaluate("""
        () => {
            const el = document.querySelector('[x-data]');
            return el ? {
                hasXData: true,
                hasX: !!el.__x,
                dataKeys: el.__x ? Object.keys(el.__x.$data) : []
            } : { hasXData: false };
        }
    """)
    print(f"x-data绑定: {has_xdata}")
    
    # 输入并点击
    page.fill("input[x-model='newTask']", "测试123")
    
    # 检查输入是否绑定到Alpine数据
    alpine_value = page.evaluate("""
        () => {
            const el = document.querySelector('[x-data]');
            return el.__x ? el.__x.$data.newTask : 'NO DATA';
        }
    """)
    print(f"Alpine newTask值: {alpine_value}")
    
    page.click("button:has-text('创建任务')")
    time.sleep(2)
    
    print("\n测试完成")
    browser.close()
