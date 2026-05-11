"""
页面对象模板
复制后修改：类名、定位器、操作方法、验证方法
"""

from playwright.sync_api import Page, Locator, expect
from typing import Dict, Any


class PageTemplate:
    """页面对象模板 - 复制后修改"""

    def __init__(self, page: Page):
        self.page = page

        # ==================== 定位器 ====================
        # 根据实际页面修改
        self.main_button = page.locator(".main-button")
        self.input_field = page.locator(".input-field")
        self.submit_button = page.locator(".submit-btn")
        self.error_message = page.locator(".error-msg")

    # ==================== 导航 ====================

    def navigate(self):
        """导航到页面"""
        self.page.goto("/page-path", wait_until="networkidle")

    # ==================== 操作方法 ====================

    def fill_input(self, value: str):
        """填写输入框"""
        self.input_field.fill(value)

    def click_submit(self):
        """点击提交"""
        self.submit_button.click()
        self.page.wait_for_timeout(1000)  # 等待响应

    def do_action(self, *args):
        """自定义操作"""
        # 根据需求添加
        pass

    # ==================== 验证方法 ====================

    def verify_elements_visible(self):
        """验证元素可见"""
        expect(self.main_button).to_be_visible()
        expect(self.input_field).to_be_visible()

    def verify_text(self, locator: Locator, expected: str):
        """验证文本"""
        expect(locator).to_contain_text(expected)

    def verify_error_message(self, expected: str):
        """验证错误信息"""
        expect(self.error_message).to_contain_text(expected)

    # ==================== 辅助方法 ====================

    def take_screenshot(self, name: str, path: str = "screenshots"):
        """截图"""
        return self.page.screenshot(path=f"{path}/{name}.png")

    def get_current_url(self) -> str:
        """获取当前URL"""
        return self.page.url


# ==================== 使用示例 ====================

"""
# 在测试中使用
def test_page(login_page):
    page_obj = PageTemplate(login_page)
    page_obj.navigate()
    page_obj.fill_input("test value")
    page_obj.click_submit()
    page_obj.verify_elements_visible()
"""