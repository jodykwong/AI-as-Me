"""Playwright测试 - 排查Kanban页面bug"""
import asyncio
from playwright.async_api import async_playwright

async def debug_kanban_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()
        page = await context.new_page()
        
        # 监听控制台错误
        page.on("console", lambda msg: print(f"[Console {msg.type}] {msg.text}"))
        page.on("pageerror", lambda err: print(f"[Page Error] {err}"))
        
        print("🔍 访问Kanban页面...")
        try:
            await page.goto("http://192.168.8.166:8080/kanban.html", timeout=10000)
            await page.wait_for_load_state("networkidle")
            print("✅ 页面加载完成")
        except Exception as e:
            print(f"❌ 页面加载失败: {e}")
            await browser.close()
            return
        
        # 等待Alpine.js初始化
        await asyncio.sleep(2)
        
        # 检查关键元素
        print("\n📋 检查页面元素...")
        
        # 1. 检查看板列
        for status in ['inbox', 'todo', 'doing', 'done']:
            list_el = await page.query_selector(f"#{status}-list")
            if list_el:
                print(f"✅ {status}-list 存在")
            else:
                print(f"❌ {status}-list 不存在")
        
        # 2. 检查右侧执行监控面板
        panel = await page.query_selector(".w-96.flex-shrink-0")
        if panel:
            print("✅ 执行监控面板存在")
        else:
            print("❌ 执行监控面板不存在")
        
        # 3. 检查JavaScript错误
        print("\n🔍 检查JavaScript错误...")
        js_errors = await page.evaluate("""
            () => {
                const errors = [];
                // 检查Alpine.js是否加载
                if (typeof Alpine === 'undefined') {
                    errors.push('Alpine.js未加载');
                }
                // 检查Sortable是否加载
                if (typeof Sortable === 'undefined') {
                    errors.push('Sortable.js未加载');
                }
                // 检查kanbanApp函数
                if (typeof kanbanApp === 'undefined') {
                    errors.push('kanbanApp函数未定义');
                }
                return errors;
            }
        """)
        
        if js_errors:
            print("❌ JavaScript错误:")
            for err in js_errors:
                print(f"  - {err}")
        else:
            print("✅ 无JavaScript错误")
        
        # 4. 检查API响应
        print("\n🌐 检查API响应...")
        try:
            response = await page.goto("http://192.168.8.166:8080/api/kanban/board")
            if response.status == 200:
                print("✅ API /api/kanban/board 正常")
            else:
                print(f"❌ API返回状态: {response.status}")
        except Exception as e:
            print(f"❌ API请求失败: {e}")
        
        # 5. 截图
        print("\n📸 保存截图...")
        await page.goto("http://192.168.8.166:8080/kanban.html")
        await asyncio.sleep(2)
        await page.screenshot(path="/home/sunrise/AI-as-Me/kanban_debug.png", full_page=True)
        print("✅ 截图已保存: kanban_debug.png")
        
        # 6. 获取控制台日志
        print("\n📝 等待5秒观察控制台...")
        await asyncio.sleep(5)
        
        await browser.close()
        print("\n✅ 调试完成")

if __name__ == "__main__":
    asyncio.run(debug_kanban_page())
