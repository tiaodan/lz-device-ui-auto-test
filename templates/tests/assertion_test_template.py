"""
断言测试模板
验证元素、文本、属性等
"""

from playwright.sync_api import Page, expect
import pytest


class AssertionTestTemplate:
    """断言测试基类 - 复制后添加自定义断言"""

    def __init__(self, page: Page, screenshot_path: str = "screenshots"):
        self.page = page
        self.screenshot_path = screenshot_path

    # ==================== 元素断言 ====================

    def assert_visible(self, locator, description: str = ""):
        """断言元素可见"""
        expect(locator).to_be_visible()
        print(f"✓ 元素可见: {description}")

    def assert_hidden(self, locator, description: str = ""):
        """断言元素隐藏"""
        expect(locator).not_to_be_visible()
        print(f"✓ 元素隐藏: {description}")

    def assert_enabled(self, locator, description: str = ""):
        """断言元素可用"""
        expect(locator).to_be_enabled()
        print(f"✓ 元素可用: {description}")

    def assert_disabled(self, locator, description: str = ""):
        """断言元素禁用"""
        expect(locator).to_be_disabled()
        print(f"✓ 元素禁用: {description}")

    # ==================== 文本断言 ====================

    def assert_text(self, locator, text: str, description: str = ""):
        """断言文本精确匹配"""
        expect(locator).to_have_text(text)
        print(f"✓ 文本匹配 '{text}': {description}")

    def assert_text_contains(self, locator, text: str, description: str = ""):
        """断言文本包含"""
        expect(locator).to_contain_text(text)
        print(f"✓ 文本包含 '{text}': {description}")

    def assert_input_value(self, locator, value: str, description: str = ""):
        """断言输入框值"""
        expect(locator).to_have_value(value)
        print(f"✓ 输入值 '{value}': {description}")

    # ==================== 属性断言 ====================

    def assert_attribute(self, locator, name: str, value: str, description: str = ""):
        """断言属性值"""
        expect(locator).to_have_attribute(name, value)
        print(f"✓ 属性 {name}='{value}': {description}")

    def assert_placeholder(self, locator, value: str, description: str = ""):
        """断言占位符"""
        self.assert_attribute(locator, "placeholder", value, description)

    # ==================== URL/状态断言 ====================

    def assert_url(self, url: str):
        """断言 URL"""
        expect(self.page).to_have_url(url)
        print(f"✓ URL: {url}")

    def assert_url_contains(self, text: str):
        """断言 URL 包含"""
        expect(self.page).to_have_url(lambda u: text in u)
        print(f"✓ URL 包含 '{text}'")

    def assert_title(self, title: str):
        """断言标题"""
        expect(self.page).to_have_title(title)
        print(f"✓ 标题: {title}")

    # ==================== 数量断言 ====================

    def assert_count(self, locator, count: int, description: str = ""):
        """断言元素数量"""
        expect(locator).to_have_count(count)
        print(f"✓ 数量 {count}: {description}")

    # ==================== 辅助方法 ====================

    def screenshot(self, name: str):
        """截图"""
        path = f"{self.screenshot_path}/{name}.png"
        self.page.screenshot(path=path)
        return path


# ==================== 测试用例示例 ====================

"""
# test_login.py

def test_login_page_elements(page, config):
    '''测试登录页元素'''
    assertion = AssertionTestTemplate(page)

    # 导航到登录页
    page.goto(config.base_url)

    # 验证元素
    assertion.assert_visible(page.locator(".login-form"), "登录表单")
    assertion.assert_visible(page.locator(".username-input"), "用户名输入框")
    assertion.assert_visible(page.locator(".password-input"), "密码输入框")
    assertion.assert_visible(page.locator(".login-button"), "登录按钮")

    # 验证属性
    assertion.assert_placeholder(page.locator(".username-input"), "用户名")
    assertion.assert_placeholder(page.locator(".password-input"), "密码")

    # 验证文本
    assertion.assert_text_contains(page.locator(".login-button"), "登录")
"""