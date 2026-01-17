from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.on("console", lambda msg: print(f"[Console] {msg.text}"))
    page.on("pageerror", lambda err: print(f"[Error] {err}"))
    page.on("response", lambda r: print(f"[API] {r.status} {r.url}") if '/api/' in r.url else None)
    
    page.goto("http://192.168.8.166:8080/kanban.html")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    page.fill("input[placeholder*='任务']", "测试任务from playwright")
    page.click("button:has-text('创建任务')")
    
    time.sleep(3)
    print("Done")
    browser.close()
