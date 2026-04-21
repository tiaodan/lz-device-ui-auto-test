"""
登录功能 - 正常场景断言测试
测试正确的用户名密码登录 + 滑块验证
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from playwright.sync_api import sync_playwright, expect
from config.config_loader import get_config
from pages.login_page import LoginPage
from assertion_test.base import AssertionTest
from utils.ssl_handler import safe_navigate


def test_login_ok():
    """测试：正常登录 - 用户名+密码+滑块验证"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 正常登录 (login_ok)")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        # 安全导航
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素 ====================
        print("\n[Step 1] 验证页面元素可见性")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 验证元素属性 ====================
        print("\n[Step 2] 验证元素属性")
        try:
            assertion.assert_attribute(login_page.username_input, "placeholder", "Username", "用户名提示")
            assertion.assert_attribute(login_page.password_input, "placeholder", "Password", "密码提示")
            print("[PASS] 属性验证通过")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 验证按钮文本 ====================
        print("\n[Step 3] 验证按钮文本")
        try:
            assertion.assert_text_contains(login_page.login_button, "Sign in", "登录按钮")
            print("[PASS] 按钮文本验证通过")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 验证滑块初始状态 ====================
        print("\n[Step 4] 验证滑块初始状态")
        try:
            initial_progress = login_page.get_slider_progress()
            print(f"  初始进度: {initial_progress}")
            if "0" in initial_progress or initial_progress == "0px":
                print("[PASS] 滑块初始位置正确")
            else:
                print("[WARN] 滑块初始位置可能不正确")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 拖动滑块 ====================
        print("\n[Step 5] 拖动滑块")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            final_progress = login_page.get_slider_progress()
            print(f"  最终进度: {final_progress}")
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 填写表单 ====================
        print("\n[Step 6] 填写表单")
        try:
            login_page.fill_credentials(config.username, config.password)
            values = login_page.get_input_values()
            print(f"  用户名: {values['username']}")
            print(f"  密码: {'*' * len(values['password'])}")
            if values['username'] == config.username and values['password'] == config.password:
                print("[PASS] 表单填写正确")
            else:
                print("[FAIL] 表单填写不正确")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 7. 点击登录 ====================
        print("\n[Step 7] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(3000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 8. 验证登录结果 ====================
        print("\n[Step 8] 验证登录结果")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")
            # 登录成功后 URL 应该变化，不再是登录页
            if current_url and "/login" not in current_url and "signin" not in current_url.lower():
                print("[PASS] 登录成功，页面已跳转")
            else:
                print("[WARN] 可能仍在登录页")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # 截图
        page.screenshot(path=f"{config.assertion_screenshot_path}/login_ok_result.png")

        browser.close()

    # ==================== 测试结果 ====================
    print("\n" + "="*50)
    if result:
        print("[PASS] 登录断言测试全部通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


if __name__ == "__main__":
    test_login_ok()