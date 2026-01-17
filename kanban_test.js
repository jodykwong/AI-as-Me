const { chromium } = require('playwright');

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // 监听控制台错误
  page.on('console', msg => console.log('CONSOLE:', msg.text()));
  page.on('pageerror', err => console.log('PAGE ERROR:', err.message));
  
  try {
    console.log('访问 Kanban 页面...');
    await page.goto('http://192.168.8.166:8080/kanban.html');
    
    console.log('等待页面加载...');
    await page.waitForLoadState('networkidle');
    
    console.log('查找创建任务按钮...');
    const createButton = await page.locator('button:has-text("创建"), button:has-text("Create"), [id*="create"], [class*="create"]').first();
    
    if (await createButton.count() > 0) {
      console.log('找到创建按钮，尝试点击...');
      await createButton.click();
      await page.waitForTimeout(2000);
    } else {
      console.log('未找到创建任务按钮');
    }
    
  } catch (error) {
    console.log('ERROR:', error.message);
  }
  
  await browser.close();
})();
