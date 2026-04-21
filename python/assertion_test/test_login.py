"""
登录功能断言测试
测试元素可见性、文本、属性等
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from config.config_loader import get_config
from pages.login_page import LoginPage
from assertion_test.base import AssertionTest
from utils.ssl_handler import safe_navigate


def test_login_page_elements():
    """测试：登录页面元素可见性"""

    config = get_config()
    config.ensure_directories()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        # 创建测试对象
        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        print("\n" + "="*50)
        print("测试类型: 断言测试 (Assertion)")
        print("测试用例: 登录页面元素验证")
        print("="*50)

        # 安全导航（自动处理 SSL）
        safe_navigate(page, config.base_url)

        # 执行断言测试
        print("\n[Step 1] 验证元素可见性")
        assertion.assert_visible(login_page.username_input, "用户名输入框")
        assertion.assert_visible(login_page.password_input, "密码输入框")
        assertion.assert_visible(login_page.slider, "滑块验证码")
        assertion.assert_visible(login_page.login_button, "登录按钮")
        assertion.assert_visible(login_page.logo, "Logo")

        print("\n[Step 2] 验证元素可用性")
        assertion.assert_enabled(login_page.username_input, "用户名输入框")
        assertion.assert_enabled(login_page.password_input, "密码输入框")
        assertion.assert_enabled(login_page.login_button, "登录按钮")

        print("\n[Step 3] 验证占位符文本")
        assertion.assert_attribute(login_page.username_input, "placeholder", "Username", "用户名提示")
        assertion.assert_attribute(login_page.password_input, "placeholder", "Password", "密码提示")

        print("\n[Step 4] 验证按钮文本")
        assertion.assert_text_contains(login_page.login_button, "Sign in", "登录按钮")

        print("\n[Step 5] 验证滑块提示")
        assertion.assert_text_contains(login_page.slider_text, "slide", "滑块提示")

        # 截图
        page.screenshot(path=f"{config.assertion_screenshot_path}/login_elements.png")

        browser.close()
        print("\n[TEST COMPLETE] 断言测试全部通过")


def test_login_slider_progress():
    """测试：滑块进度验证"""

    config = get_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        print("\n" + "="*50)
        print("测试类型: 断言测试 (Assertion)")
        print("测试用例: 滑块进度验证")
        print("="*50)

        safe_navigate(page, config.base_url)

        # 检查初始进度
        print("\n[Step 1] 验证初始进度")
        initial_progress = login_page.get_slider_progress()
        print(f"初始进度: {initial_progress}")

        # 拖动滑块
        print("\n[Step 2] 拖动滑块")
        login_page.drag_slider()

        # 检查拖动后进度
        print("\n[Step 3] 验证拖动后进度")
        final_progress = login_page.get_slider_progress()
        print(f"最终进度: {final_progress}")

        # 断言进度变化
        assert login_page.is_slider_unlocked(), "滑块未解锁"
        print("[ASSERT PASS] 滑块解锁成功")

        # 截图
        page.screenshot(path=f"{config.assertion_screenshot_path}/slider_progress.png")

        browser.close()
        print("\n[TEST COMPLETE] 滑块断言测试通过")


def test_login_form_fill():
    """测试：表单填写验证"""

    config = get_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        print("\n" + "="*50)
        print("测试类型: 断言测试 (Assertion)")
        print("测试用例: 表单填写验证")
        print("="*50)

        safe_navigate(page, config.base_url)

        # 填写表单
        print("\n[Step 1] 填写用户名")
        login_page.fill_credentials(config.username, config.password)

        # 验证填写值
        print("\n[Step 2] 验证填写值")
        values = login_page.get_input_values()
        assertion.assert_input_value(login_page.username_input, config.username, "用户名")
        assertion.assert_input_value(login_page.password_input, config.password, "密码")

        # 截图
        page.screenshot(path=f"{config.assertion_screenshot_path}/form_filled.png")

        browser.close()
        print("\n[TEST COMPLETE] 表单断言测试通过")


if __name__ == "__main__":
    import sys
    test_name = sys.argv[1] if len(sys.argv) > 1 else "all"

    if test_name == "elements":
        test_login_page_elements()
    elif test_name == "slider":
        test_login_slider_progress()
    elif test_name == "form":
        test_login_form_fill()
    else:
        test_login_page_elements()
        test_login_slider_progress()
        test_login_form_fill()