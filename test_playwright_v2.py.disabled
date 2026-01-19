#!/usr/bin/env python3
"""Playwright E2E测试 - 详细诊断"""
from playwright.sync_api import sync_playwright
import time

def test_kanban():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        
        # 监听所有控制台消息
        console_logs = []
        def handle_console(msg):
            log = f"[{msg.type}] {msg.text}"
            console_logs.append(log)
            print(log)
        page.on("console", handle_console)
        
        # 监听页面错误
        errors = []
        def handle_error(err):
            error_msg = f"❌ 页面错误: {err}"
            errors.append(error_msg)
            print(error_msg)
        page.on("pageerror", handle_error)
        
        print("🧪 访问看板页面...")
        page.goto("http://192.168.8.166:8080/kanban.html")
        page.wait_for_load_state("networkidle")
        time.sleep(3)
        
        print(f"\n📸 页面标题: {page.title()}")
        print(f"Alpine.js: {page.evaluate('() => typeof Alpine')}")
        print(f"kanbanApp: {page.evaluate('() => typeof kanbanApp')}")
        
        # 检查是否有初始化日志
        print(f"\n初始化日志数量: {len([l for l in console_logs if 'initialized' in l])}")
        
        # 查找输入框并输入
        print("\n🔍 测试输入框...")
        input_selector = "input[x-model='newTask']"
        page.fill(input_selector, "Playwright测试")
        
        # 获取输入框的值
        input_value = page.evaluate(f"() => document.querySelector('{input_selector}').value")
        print(f"输入框值: {input_value}")
        
        # 检查 Alpine 数据绑定
        try:
            new_task_value = page.evaluate("() => Alpine.raw(document.querySelector('[x-data]').__x.$data).newTask")
            print(f"Alpine newTask 值: {new_task_value}")
        except Exception as e:
            print(f"无法获取Alpine数据: {e}")
        
        # 点击按钮
        print("\n🖱️  点击创建按钮...")
        btn_selector = "button:has-text('创建任务')"
        page.click(btn_selector)
        time.sleep(3)
        
        print(f"\n📋 总共 {len(console_logs)} 条控制台日志")
        print(f"❌ 总共 {len(errors)} 个错误")
        
        if errors:
            print("\n错误详情:")
            for err in errors:
                print(f"  {err}")
        
        browser.close()

if __name__ == "__main__":
    test_kanban()
