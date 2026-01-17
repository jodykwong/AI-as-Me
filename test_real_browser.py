#!/usr/bin/env python3
"""真实浏览器E2E测试 - 创建任务功能"""
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 使用无头Chrome
options = webdriver.ChromeOptions()
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

driver = webdriver.Chrome(options=options)

try:
    print("🧪 访问看板页面...")
    driver.get("http://192.168.8.166:8080/kanban.html")
    time.sleep(3)
    
    print("📸 页面标题:", driver.title)
    
    # 检查Alpine.js是否加载
    alpine_loaded = driver.execute_script("return typeof Alpine !== 'undefined'")
    print(f"✓ Alpine.js 加载: {alpine_loaded}")
    
    # 查找输入框
    print("🔍 查找任务输入框...")
    task_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "input[x-model='newTask']"))
    )
    print("✓ 找到输入框")
    
    # 输入任务
    print("⌨️  输入任务描述...")
    task_input.send_keys("E2E测试任务")
    
    # 查找创建按钮
    print("🔍 查找创建按钮...")
    create_btn = driver.find_element(By.XPATH, "//button[contains(text(), '创建任务')]")
    print("✓ 找到按钮")
    
    # 点击按钮
    print("🖱️  点击创建按钮...")
    create_btn.click()
    time.sleep(2)
    
    # 检查是否有错误
    errors = driver.find_elements(By.CSS_SELECTOR, ".text-red-600")
    if errors:
        print(f"❌ 发现错误: {errors[0].text}")
    
    # 检查控制台日志
    logs = driver.get_log('browser')
    if logs:
        print("\n📋 浏览器控制台日志:")
        for log in logs:
            print(f"  {log['level']}: {log['message']}")
    
    print("\n✅ E2E测试完成")
    
except Exception as e:
    print(f"\n❌ 测试失败: {e}")
    print(f"\n📸 页面源码（前500字符）:")
    print(driver.page_source[:500])
    
finally:
    driver.quit()
