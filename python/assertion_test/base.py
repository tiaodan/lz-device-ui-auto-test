"""
断言测试基础模块
提供元素、文本、属性等断言功能
"""

from playwright.sync_api import Page, expect, Locator
from typing import Optional
import os


class AssertionTest:
    """断言测试基类"""

    def __init__(self, page: Page, screenshot_path: str = "screenshots/assertion"):
        self.page = page
        self.screenshot_path = screenshot_path
        os.makedirs(screenshot_path, exist_ok=True)

    # ==================== 元素断言 ====================

    def assert_visible(self, locator: Locator, description: str = ""):
        """断言元素可见"""
        expect(locator).to_be_visible()
        self._log_pass(f"元素可见: {description}")

    def assert_hidden(self, locator: Locator, description: str = ""):
        """断言元素隐藏"""
        expect(locator).not_to_be_visible()
        self._log_pass(f"元素隐藏: {description}")

    def assert_enabled(self, locator: Locator, description: str = ""):
        """断言元素可用"""
        expect(locator).to_be_enabled()
        self._log_pass(f"元素可用: {description}")

    def assert_disabled(self, locator: Locator, description: str = ""):
        """断言元素禁用"""
        expect(locator).to_be_disabled()
        self._log_pass(f"元素禁用: {description}")

    def assert_exists(self, locator: Locator, description: str = ""):
        """断言元素存在"""
        expect(locator).to_be_attached()
        self._log_pass(f"元素存在: {description}")

    # ==================== 文本断言 ====================

    def assert_text(self, locator: Locator, text: str, description: str = ""):
        """断言文本精确匹配"""
        expect(locator).to_have_text(text)
        self._log_pass(f"文本匹配 '{text}': {description}")

    def assert_text_contains(self, locator: Locator, text: str, description: str = ""):
        """断言文本包含"""
        expect(locator).to_contain_text(text)
        self._log_pass(f"文本包含 '{text}': {description}")

    def assert_text_not_contains(self, locator: Locator, text: str, description: str = ""):
        """断言文本不包含"""
        expect(locator).not_to_contain_text(text)
        self._log_pass(f"文本不包含 '{text}': {description}")

    def assert_input_value(self, locator: Locator, value: str, description: str = ""):
        """断言输入框值"""
        expect(locator).to_have_value(value)
        self._log_pass(f"输入值 '{value}': {description}")

    def assert_input_empty(self, locator: Locator, description: str = ""):
        """断言输入框为空"""
        expect(locator).to_be_empty()
        self._log_pass(f"输入框为空: {description}")

    # ==================== 属性断言 ====================

    def assert_attribute(self, locator: Locator, name: str, value: str, description: str = ""):
        """断言属性值"""
        expect(locator).to_have_attribute(name, value)
        self._log_pass(f"属性 {name}='{value}': {description}")

    def assert_attribute_contains(self, locator: Locator, name: str, value: str, description: str = ""):
        """断言属性包含"""
        attr_value = locator.get_attribute(name) or ""
        assert value in attr_value, f"属性 '{name}' 不包含 '{value}'"
        self._log_pass(f"属性 {name} 包含 '{value}': {description}")

    # ==================== URL/状态断言 ====================

    def assert_url(self, url: str):
        """断言 URL"""
        expect(self.page).to_have_url(url)
        self._log_pass(f"URL: {url}")

    def assert_url_contains(self, text: str):
        """断言 URL 包含"""
        expect(self.page).to_have_url(lambda url: text in url)
        self._log_pass(f"URL 包含 '{text}'")

    def assert_title(self, title: str):
        """断言标题"""
        expect(self.page).to_have_title(title)
        self._log_pass(f"标题: {title}")

    def assert_title_contains(self, text: str):
        """断言标题包含"""
        expect(self.page).to_have_title(lambda t: text in t)
        self._log_pass(f"标题包含 '{text}'")

    # ==================== 数量断言 ====================

    def assert_count(self, locator: Locator, count: int, description: str = ""):
        """断言元素数量"""
        expect(locator).to_have_count(count)
        self._log_pass(f"数量 {count}: {description}")

    def assert_count_greater_than(self, locator: Locator, count: int, description: str = ""):
        """断言元素数量大于"""
        actual = locator.count()
        assert actual > count, f"数量 {actual} 不大于 {count}"
        self._log_pass(f"数量 >{count}: {description}")

    # ==================== 辅助方法 ====================

    def screenshot_on_failure(self, name: str):
        """失败时截图"""
        path = f"{self.screenshot_path}/{name}.png"
        self.page.screenshot(path=path)
        return path

    def _log_pass(self, message: str):
        """记录通过的断言"""
        print(f"[ASSERT PASS] {message}")

    def run_test(self, test_func: callable, name: str):
        """运行测试，失败时截图"""
        try:
            test_func()
            print(f"[TEST PASS] {name}")
            return True
        except Exception as e:
            print(f"[TEST FAIL] {name}: {e}")
            self.screenshot_on_failure(f"{name}_failure")
            return False