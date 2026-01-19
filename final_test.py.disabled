from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.on("console", lambda m: print(f"[LOG] {m.text}"))
    
    page.goto("http://192.168.8.166:8080/kanban.html")
    page.wait_for_load_state("networkidle")
    page.wait_for_function("() => document.querySelector('[x-data]')?.__x?.$data?.board")
    time.sleep(1)
    
    initial = page.evaluate("() => document.querySelector('[x-data]').__x.$data.board.inbox.length")
    print(f"初始任务数: {initial}")
    
    page.fill("input[placeholder*='任务']", "最终测试")
    page.click("button:has-text('创建任务')")
    time.sleep(3)
    
    final = page.evaluate("() => document.querySelector('[x-data]').__x.$data.board.inbox.length")
    print(f"最终任务数: {final}")
    print(f"结果: {'✓ 成功' if final > initial else '✗ 失败'}")
    
    browser.close()
