"""Story 13.1: 移动端响应式测试"""
import pytest
from playwright.sync_api import Page, expect


@pytest.fixture(scope="module")
def base_url():
    return "http://localhost:8000"


def test_mobile_viewport_320px(page: Page, base_url: str):
    """测试320px宽度（小屏手机）"""
    page.set_viewport_size({"width": 320, "height": 568})
    page.goto(base_url)
    
    # 验证标题可见
    expect(page.locator("h1")).to_be_visible()
    
    # 验证任务输入框可见
    expect(page.locator("input[placeholder*='任务']")).to_be_visible()


def test_mobile_viewport_768px(page: Page, base_url: str):
    """测试768px宽度（平板）"""
    page.set_viewport_size({"width": 768, "height": 1024})
    page.goto(base_url)
    
    # 验证看板列可见
    expect(page.locator("text=Inbox")).to_be_visible()
    expect(page.locator("text=Todo")).to_be_visible()


def test_responsive_grid(page: Page, base_url: str):
    """测试响应式网格布局"""
    # 移动端：单列
    page.set_viewport_size({"width": 375, "height": 667})
    page.goto(base_url)
    expect(page.locator(".grid")).to_have_class("grid-cols-1")
    
    # 平板：2列
    page.set_viewport_size({"width": 768, "height": 1024})
    page.reload()
    expect(page.locator(".grid")).to_have_class("md:grid-cols-2")
    
    # 桌面：4列
    page.set_viewport_size({"width": 1280, "height": 800})
    page.reload()
    expect(page.locator(".grid")).to_have_class("lg:grid-cols-4")
