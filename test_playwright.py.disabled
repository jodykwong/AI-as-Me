#!/usr/bin/env python3
"""Playwright E2E测试 - 创建任务功能"""
from playwright.sync_api import sync_playwright
import time

def test_kanban():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 监听控制台日志
        console_logs = []
        page.on("console", lambda msg: console_logs.append(f"{msg.type}: {msg.text}"))
        
        # 监听网络错误
        page.on("pageerror", lambda err: print(f"❌ 页面错误: {err}"))
        
        print("🧪 访问看板页面...")
        page.goto("http://192.168.8.166:8080/kanban.html")
        page.wait_for_load_state("networkidle")
        time.sleep(2)
        
        print(f"📸 页面标题: {page.title()}")
        
        # 检查Alpine.js
        alpine_loaded = page.evaluate("() => typeof Alpine !== 'undefined'")
        print(f"Alpine.js 加载: {alpine_loaded}")
        
        # 检查kanbanApp
        app_exists = page.evaluate("() => typeof kanbanApp === 'function'")
        print(f"kanbanApp 函数存在: {app_exists}")
        
        # 查找输入框
        print("\n🔍 查找任务输入框...")
        input_selector = "input[x-model='newTask']"
        if page.locator(input_selector).count() > 0:
            print("✓ 找到输入框")
            page.fill(input_selector, "Playwright测试任务")
            print("✓ 输入任务描述")
        else:
            print("❌ 未找到输入框")
            print(f"页面HTML: {page.content()[:500]}")
        
        # 查找创建按钮
        print("\n🔍 查找创建按钮...")
        btn_selector = "button:has-text('创建任务')"
        if page.locator(btn_selector).count() > 0:
            print("✓ 找到按钮")
            
            # 点击前检查按钮状态
            btn_disabled = page.locator(btn_selector).get_attribute("disabled")
            print(f"按钮disabled状态: {btn_disabled}")
            
            print("🖱️  点击创建按钮...")
            page.click(btn_selector)
            time.sleep(2)
            
            # 检查错误提示
            error_selector = ".text-red-600"
            if page.locator(error_selector).count() > 0:
                error_text = page.locator(error_selector).text_content()
                print(f"❌ 页面错误: {error_text}")
        else:
            print("❌ 未找到按钮")
        
        # 打印所有控制台日志
        print("\n📋 浏览器控制台日志:")
        for log in console_logs:
            print(f"  {log}")
        
        # 检查网络请求
        print("\n🌐 检查是否发送了POST请求...")
        
        browser.close()

if __name__ == "__main__":
    test_kanban()
