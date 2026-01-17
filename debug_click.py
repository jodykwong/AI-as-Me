from playwright.sync_api import sync_playwright
import time

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    page = browser.new_page()
    
    page.on("console", lambda msg: print(f"[JS] {msg.text}"))
    
    page.goto("http://192.168.8.166:8080/kanban.html")
    page.wait_for_load_state("networkidle")
    time.sleep(2)
    
    # Check if Alpine is loaded
    alpine_loaded = page.evaluate("() => typeof Alpine !== 'undefined'")
    print(f"Alpine loaded: {alpine_loaded}")
    
    # Check if x-data is initialized
    has_xdata = page.evaluate("() => document.querySelector('[x-data]') !== null")
    print(f"Has x-data: {has_xdata}")
    
    # Fill input
    page.fill("input[placeholder*='任务']", "测试")
    print("Input filled")
    
    # Try to click button
    button = page.locator("button:has-text('创建任务')")
    print(f"Button count: {button.count()}")
    print(f"Button visible: {button.is_visible()}")
    print(f"Button disabled: {button.is_disabled()}")
    
    # Check Alpine scope
    scope = page.evaluate("""() => {
        const el = document.querySelector('[x-data]');
        return el ? el.__x?.$data : null;
    }""")
    print(f"Alpine scope: {scope}")
    
    button.click()
    time.sleep(2)
    
    browser.close()
