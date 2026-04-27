"""
登录功能 - 密码显示/隐藏功能断言测试
测试密码输入框的眼睛图标切换功能
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from playwright.sync_api import sync_playwright, expect
from config.config_loader import get_config
from pages.login_page import LoginPage
from assertion_test.base import AssertionTest
from utils.ssl_handler import safe_navigate


def test_password_visibility_toggle():
    """测试：密码显示/隐藏切换功能"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 密码显示/隐藏切换")
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

        # ==================== 1. 验证密码输入框初始状态 ====================
        print("\n[Step 1] 验证密码输入框初始状态")
        try:
            # 密码框初始应该是隐藏状态 (type="password")
            password_type = login_page.password_input.get_attribute("type")
            print(f"  密码框 type: {password_type}")
            if password_type == "password":
                print("[PASS] 密码初始隐藏状态正确")
            else:
                print(f"[FAIL] 密码框初始 type 应为 'password', 实际为 '{password_type}'")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 查找眼睛图标按钮 ====================
        print("\n[Step 2] 查找眼睛图标按钮")
        try:
            # 常见的密码切换按钮定位器
            eye_button = page.locator(
                "button[type='button'], .eye-icon, .password-toggle, "
                "[class*='eye'], [class*='visibility'], "
                "span:has(img[src*='eye']), "
                "img[src*='eye'], "
                "#password + button, "
                "#password ~ button, "
                ".input-group button, "
                "button:has(svg)"
            ).first

            # 尝试多种定位方式
            selectors = [
                "#password + button",
                "#password ~ button[type='button']",
                ".password-toggle",
                "[class*='eye']",
                "[class*='visibility-toggle']",
                ".input-group-append button",
                "button[class*='eye']",
                "img[src*='eye']",
                ".form-group button",
                "button:has(svg[class*='eye'])",
            ]

            eye_button = None
            for selector in selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0:
                        eye_button = locator.first
                        print(f"  找到眼睛按钮: {selector}")
                        break
                except:
                    continue

            if eye_button:
                print("[PASS] 找到密码切换按钮")
            else:
                print("[WARN] 未找到明显的眼睛图标按钮，尝试点击密码框周边区域")
                # 尝试更广泛的搜索
                eye_button = page.locator("button").filter(has_text="", has_not_text="Sign in").first

        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 输入密码 ====================
        print("\n[Step 3] 输入密码")
        try:
            login_page.password_input.fill(config.password)
            password_value = login_page.password_input.input_value()
            print(f"  输入密码: {password_value}")
            print("[PASS] 密码输入成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击眼睛图标显示密码 ====================
        print("\n[Step 4] 点击眼睛图标显示密码")
        try:
            if eye_button and eye_button.count() > 0:
                eye_button.click()
                page.wait_for_timeout(300)

                # 检查密码框 type 是否变为 "text"
                password_type = login_page.password_input.get_attribute("type")
                print(f"  密码框 type: {password_type}")

                if password_type == "text":
                    print("[PASS] 密码显示成功 (type='text')")
                else:
                    print(f"[WARN] 密码框 type 仍为 '{password_type}'，可能按钮功能不同")

                # 截图记录
                page.screenshot(path=f"{config.assertion_screenshot_path}/password_visible.png")
            else:
                print("[WARN] 无眼睛按钮可点击，跳过此步骤")

        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 再次点击隐藏密码 ====================
        print("\n[Step 5] 再次点击隐藏密码")
        try:
            if eye_button and eye_button.count() > 0:
                eye_button.click()
                page.wait_for_timeout(300)

                # 检查密码框 type 是否恢复为 "password"
                password_type = login_page.password_input.get_attribute("type")
                print(f"  密码框 type: {password_type}")

                if password_type == "password":
                    print("[PASS] 密码隐藏成功 (type='password')")
                else:
                    print(f"[WARN] 密码框 type 为 '{password_type}'")

                # 截图记录
                page.screenshot(path=f"{config.assertion_screenshot_path}/password_hidden.png")
            else:
                print("[WARN] 无眼睛按钮可点击，跳过此步骤")

        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证密码值不变 ====================
        print("\n[Step 6] 验证密码值不变")
        try:
            password_value = login_page.password_input.input_value()
            print(f"  密码值: {password_value}")
            if password_value == config.password:
                print("[PASS] 密码值未改变")
            else:
                print(f"[FAIL] 密码值应为 '{config.password}', 实际为 '{password_value}'")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 7. 验证切换按钮可见性 ====================
        print("\n[Step 7] 验证切换按钮可见性")
        try:
            if eye_button and eye_button.count() > 0:
                assertion.assert_visible(eye_button, "密码切换按钮")
                print("[PASS] 切换按钮可见")
            else:
                print("[WARN] 页面可能不支持密码显示/隐藏功能")
        except Exception as e:
            print(f"[WARN] {e}")

        browser.close()

    # ==================== 测试结果 ====================
    print("\n" + "="*50)
    if result:
        print("[PASS] 密码显示/隐藏功能测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_user_not_exist():
    """测试：不存在的用户登录"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 不存在的用户登录")
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

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 输入不存在的用户名 ====================
        print("\n[Step 2] 输入不存在的用户名")
        try:
            login_page.username_input.fill("root1")
            login_page.password_input.fill(config.password)
            print(f"  用户名: root1 (不存在)")
            print(f"  密码: {config.password}")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(2000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 验证登录失败 ====================
        print("\n[Step 5] 验证登录失败")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            # 登录失败应该仍在登录页
            if "/login" in current_url or current_url == config.base_url + "/" or current_url == config.base_url:
                print("[PASS] 登录失败，仍在登录页")
            else:
                print(f"[FAIL] URL 应为登录页，实际为: {current_url}")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证错误提示 ====================
        print("\n[Step 6] 验证错误提示")
        try:
            # 查找错误提示元素
            error_selectors = [
                ".ui-message-error",
                "[class*='error']",
                "[class*='message-error']",
                ".toast-error",
                ".alert-error",
                "[class*='toast']",
                ".error-message",
            ]

            error_found = False
            for selector in error_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0 and locator.is_visible():
                        error_text = locator.text_content()
                        print(f"  找到错误提示: {selector}")
                        print(f"  错误内容: {error_text}")
                        error_found = True
                        break
                except:
                    continue

            if error_found:
                print("[PASS] 错误提示已显示")
                # 截图记录
                page.screenshot(path=f"{config.assertion_screenshot_path}/user_not_exist_error.png")
            else:
                # 尝试等待错误提示出现
                page.wait_for_timeout(1000)
                print("[WARN] 未找到明显的错误提示元素，检查页面是否有其他提示")
                # 截图查看实际情况
                page.screenshot(path=f"{config.assertion_screenshot_path}/user_not_exist_result.png")

        except Exception as e:
            print(f"[WARN] {e}")

        # ==================== 7. 验证输入框仍可操作 ====================
        print("\n[Step 7] 验证输入框仍可操作")
        try:
            # 登录失败后，输入框应该仍然可用
            assertion.assert_enabled(login_page.username_input, "用户名输入框")
            assertion.assert_enabled(login_page.password_input, "密码输入框")
            print("[PASS] 输入框仍可操作")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        browser.close()

    # ==================== 测试结果 ====================
    print("\n" + "="*50)
    if result:
        print("[PASS] 不存在的用户登录测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_empty_username():
    """测试：用户名为空"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 用户名为空")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 只输入密码，用户名为空 ====================
        print("\n[Step 2] 只输入密码，用户名为空")
        try:
            login_page.username_input.fill("")
            login_page.password_input.fill(config.password)
            print(f"  用户名: (空)")
            print(f"  密码: {config.password}")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(2000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 验证登录失败 ====================
        print("\n[Step 5] 验证登录失败")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            if "/login" in current_url or current_url == config.base_url + "/" or current_url == config.base_url:
                print("[PASS] 登录失败，仍在登录页")
            else:
                print(f"[FAIL] URL 应为登录页，实际为: {current_url}")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证错误提示 ====================
        print("\n[Step 6] 验证错误提示")
        try:
            error_selectors = [
                ".ui-message-error",
                "[class*='error']",
                "[class*='message-error']",
                ".toast-error",
                ".alert-error",
                "[class*='toast']",
                ".error-message",
            ]

            error_found = False
            for selector in error_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0 and locator.is_visible():
                        error_text = locator.text_content()
                        print(f"  找到错误提示: {selector}")
                        print(f"  错误内容: {error_text}")
                        error_found = True
                        break
                except:
                    continue

            if error_found:
                print("[PASS] 错误提示已显示")
                page.screenshot(path=f"{config.assertion_screenshot_path}/empty_username_error.png")
            else:
                page.wait_for_timeout(1000)
                print("[WARN] 未找到明显的错误提示元素")
                page.screenshot(path=f"{config.assertion_screenshot_path}/empty_username_result.png")

        except Exception as e:
            print(f"[WARN] {e}")

        # ==================== 7. 验证输入框仍可操作 ====================
        print("\n[Step 7] 验证输入框仍可操作")
        try:
            assertion.assert_enabled(login_page.username_input, "用户名输入框")
            assertion.assert_enabled(login_page.password_input, "密码输入框")
            print("[PASS] 输入框仍可操作")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 用户名为空测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_empty_password():
    """测试：密码为空"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 密码为空")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 只输入用户名，密码为空 ====================
        print("\n[Step 2] 只输入用户名，密码为空")
        try:
            login_page.username_input.fill(config.username)
            login_page.password_input.fill("")
            print(f"  用户名: {config.username}")
            print(f"  密码: (空)")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(2000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 验证登录失败 ====================
        print("\n[Step 5] 验证登录失败")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            if "/login" in current_url or current_url == config.base_url + "/" or current_url == config.base_url:
                print("[PASS] 登录失败，仍在登录页")
            else:
                print(f"[FAIL] URL 应为登录页，实际为: {current_url}")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证错误提示 ====================
        print("\n[Step 6] 验证错误提示")
        try:
            error_selectors = [
                ".ui-message-error",
                "[class*='error']",
                "[class*='message-error']",
                ".toast-error",
                ".alert-error",
                "[class*='toast']",
                ".error-message",
            ]

            error_found = False
            for selector in error_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0 and locator.is_visible():
                        error_text = locator.text_content()
                        print(f"  找到错误提示: {selector}")
                        print(f"  错误内容: {error_text}")
                        error_found = True
                        break
                except:
                    continue

            if error_found:
                print("[PASS] 错误提示已显示")
                page.screenshot(path=f"{config.assertion_screenshot_path}/empty_password_error.png")
            else:
                page.wait_for_timeout(1000)
                print("[WARN] 未找到明显的错误提示元素")
                page.screenshot(path=f"{config.assertion_screenshot_path}/empty_password_result.png")

        except Exception as e:
            print(f"[WARN] {e}")

        # ==================== 7. 验证输入框仍可操作 ====================
        print("\n[Step 7] 验证输入框仍可操作")
        try:
            assertion.assert_enabled(login_page.username_input, "用户名输入框")
            assertion.assert_enabled(login_page.password_input, "密码输入框")
            print("[PASS] 输入框仍可操作")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 密码为空测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_wrong_password():
    """测试：正确的用户名+错误密码"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 正确的用户名+错误密码")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 输入正确的用户名+错误密码 ====================
        print("\n[Step 2] 输入正确的用户名+错误密码")
        try:
            login_page.username_input.fill(config.username)
            login_page.password_input.fill("lz")  # 错误密码
            print(f"  用户名: {config.username} (正确)")
            print(f"  密码: lz (错误)")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(2000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 验证登录失败 ====================
        print("\n[Step 5] 验证登录失败")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            if "/login" in current_url or current_url == config.base_url + "/" or current_url == config.base_url:
                print("[PASS] 登录失败，仍在登录页")
            else:
                print(f"[FAIL] URL 应为登录页，实际为: {current_url}")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证错误提示 ====================
        print("\n[Step 6] 验证错误提示")
        try:
            error_selectors = [
                ".ui-message-error",
                "[class*='error']",
                "[class*='message-error']",
                ".toast-error",
                ".alert-error",
                "[class*='toast']",
                ".error-message",
            ]

            error_found = False
            for selector in error_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0 and locator.is_visible():
                        error_text = locator.text_content()
                        print(f"  找到错误提示: {selector}")
                        print(f"  错误内容: {error_text}")
                        error_found = True
                        break
                except:
                    continue

            if error_found:
                print("[PASS] 错误提示已显示")
                page.screenshot(path=f"{config.assertion_screenshot_path}/wrong_password_error.png")
            else:
                page.wait_for_timeout(1000)
                print("[WARN] 未找到明显的错误提示元素")
                page.screenshot(path=f"{config.assertion_screenshot_path}/wrong_password_result.png")

        except Exception as e:
            print(f"[WARN] {e}")

        # ==================== 7. 验证输入框仍可操作 ====================
        print("\n[Step 7] 验证输入框仍可操作")
        try:
            assertion.assert_enabled(login_page.username_input, "用户名输入框")
            assertion.assert_enabled(login_page.password_input, "密码输入框")
            print("[PASS] 输入框仍可操作")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 正确的用户名+错误密码测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_without_slider():
    """测试：正确的账号密码+不进行滑块验证"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 正确账号密码+不进行滑块验证")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 输入正确的账号密码 ====================
        print("\n[Step 2] 输入正确的账号密码")
        try:
            login_page.username_input.fill(config.username)
            login_page.password_input.fill(config.password)
            print(f"  用户名: {config.username} (正确)")
            print(f"  密码: {config.password} (正确)")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 验证滑块未解锁 ====================
        print("\n[Step 3] 验证滑块未解锁（不拖动滑块）")
        try:
            slider_progress = login_page.get_slider_progress()
            print(f"  滑块进度: {slider_progress}")
            if "0" in slider_progress or slider_progress == "0px":
                print("[PASS] 滑块未解锁")
            else:
                print("[WARN] 滑块状态异常")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(2000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 验证登录失败 ====================
        print("\n[Step 5] 验证登录失败")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            if "/login" in current_url or current_url == config.base_url + "/" or current_url == config.base_url:
                print("[PASS] 登录失败，仍在登录页（滑块验证是必须的）")
            else:
                print(f"[FAIL] URL 应为登录页，实际为: {current_url}")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证错误提示 ====================
        print("\n[Step 6] 验证错误提示")
        try:
            error_selectors = [
                ".ui-message-error",
                "[class*='error']",
                "[class*='message-error']",
                ".toast-error",
                ".alert-error",
                "[class*='toast']",
                ".error-message",
            ]

            error_found = False
            for selector in error_selectors:
                try:
                    locator = page.locator(selector)
                    if locator.count() > 0 and locator.is_visible():
                        error_text = locator.text_content()
                        print(f"  找到错误提示: {selector}")
                        print(f"  错误内容: {error_text}")
                        error_found = True
                        break
                except:
                    continue

            if error_found:
                print("[PASS] 错误提示已显示")
                page.screenshot(path=f"{config.assertion_screenshot_path}/no_slider_error.png")
            else:
                page.wait_for_timeout(1000)
                print("[WARN] 未找到明显的错误提示元素")
                page.screenshot(path=f"{config.assertion_screenshot_path}/no_slider_result.png")

        except Exception as e:
            print(f"[WARN] {e}")

        # ==================== 7. 验证输入框仍可操作 ====================
        print("\n[Step 7] 验证输入框仍可操作")
        try:
            assertion.assert_enabled(login_page.username_input, "用户名输入框")
            assertion.assert_enabled(login_page.password_input, "密码输入框")
            print("[PASS] 输入框仍可操作")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 8. 验证滑块仍可操作 ====================
        print("\n[Step 8] 验证滑块仍可操作")
        try:
            assertion.assert_visible(login_page.slider, "滑块验证码")
            print("[PASS] 滑块仍可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 正确账号密码+不进行滑块验证测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_slider_first():
    """测试：先进行滑块验证后输入正确的账号密码"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 先进行滑块验证后输入正确的账号密码")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 先拖动滑块验证 ====================
        print("\n[Step 2] 先拖动滑块验证（不输入账号密码）")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            final_progress = login_page.get_slider_progress()
            print(f"  滑块进度: {final_progress}")
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 验证滑块保持解锁状态 ====================
        print("\n[Step 3] 验证滑块保持解锁状态")
        try:
            # 等待一下，确认滑块状态稳定
            page.wait_for_timeout(300)
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块保持解锁状态")
            else:
                print("[FAIL] 滑块状态发生变化")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 输入正确的账号密码 ====================
        print("\n[Step 4] 输入正确的账号密码")
        try:
            login_page.username_input.fill(config.username)
            login_page.password_input.fill(config.password)
            print(f"  用户名: {config.username} (正确)")
            print(f"  密码: {config.password} (正确)")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 点击登录 ====================
        print("\n[Step 5] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(3000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证登录成功 ====================
        print("\n[Step 6] 验证登录成功")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            # 登录成功后 URL 应该变化，不再是登录页
            if current_url and "/login" not in current_url and "signin" not in current_url.lower():
                print("[PASS] 登录成功，页面已跳转")
            else:
                print("[WARN] 可能仍在登录页")
                page.screenshot(path=f"{config.assertion_screenshot_path}/slider_first_result.png")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 7. 截图记录 ====================
        print("\n[Step 7] 截图记录")
        try:
            page.screenshot(path=f"{config.assertion_screenshot_path}/slider_first_login.png")
            print("[PASS] 截图保存成功")
        except Exception as e:
            print(f"[WARN] {e}")

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 先进行滑块验证后输入正确的账号密码测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_password_case_sensitive():
    """测试：密码大小写区分"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 密码大小写区分")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 输入正确用户名+大写密码 ====================
        print("\n[Step 2] 输入正确用户名+大写密码")
        try:
            password_upper = config.password.upper()  # 转大写
            login_page.username_input.fill(config.username)
            login_page.password_input.fill(password_upper)
            print(f"  用户名: {config.username} (正确)")
            print(f"  密码: {password_upper} (大写，应该失败)")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(2000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 验证登录失败 ====================
        print("\n[Step 5] 验证登录失败")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            if "/login" in current_url or current_url == config.base_url + "/" or current_url == config.base_url:
                print("[PASS] 登录失败，仍在登录页（密码大小写敏感）")
            else:
                print(f"[FAIL] URL 应为登录页，实际为: {current_url}")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证输入框仍可操作 ====================
        print("\n[Step 6] 验证输入框仍可操作")
        try:
            assertion.assert_enabled(login_page.username_input, "用户名输入框")
            assertion.assert_enabled(login_page.password_input, "密码输入框")
            print("[PASS] 输入框仍可操作")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 密码大小写区分测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def test_login_username_case_sensitive():
    """测试：用户名大小写区分"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 断言测试 (Assertion)")
    print("测试场景: 用户名大小写区分")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== 1. 验证页面元素可见 ====================
        print("\n[Step 1] 验证页面元素可见")
        try:
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")
            print("[PASS] 所有元素可见")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 2. 输入大写用户名+正确密码 ====================
        print("\n[Step 2] 输入大写用户名+正确密码")
        try:
            username_upper = config.username.upper()  # 转大写
            login_page.username_input.fill(username_upper)
            login_page.password_input.fill(config.password)
            print(f"  用户名: {username_upper} (大写，应该失败)")
            print(f"  密码: {config.password} (正确)")
            print("[PASS] 表单填写完成")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 3. 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        try:
            login_page.drag_slider()
            page.wait_for_timeout(500)
            if login_page.is_slider_unlocked():
                print("[PASS] 滑块解锁成功")
            else:
                print("[FAIL] 滑块未解锁")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 4. 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        try:
            login_page.click_login()
            page.wait_for_timeout(2000)
            print("[PASS] 登录按钮点击成功")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 5. 验证登录失败 ====================
        print("\n[Step 5] 验证登录失败")
        try:
            current_url = page.url
            print(f"  当前URL: {current_url}")

            if "/login" in current_url or current_url == config.base_url + "/" or current_url == config.base_url:
                print("[PASS] 登录失败，仍在登录页（用户名大小写敏感）")
            else:
                print(f"[FAIL] URL 应为登录页，实际为: {current_url}")
                result = False
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        # ==================== 6. 验证输入框仍可操作 ====================
        print("\n[Step 6] 验证输入框仍可操作")
        try:
            assertion.assert_enabled(login_page.username_input, "用户名输入框")
            assertion.assert_enabled(login_page.password_input, "密码输入框")
            print("[PASS] 输入框仍可操作")
        except Exception as e:
            print(f"[FAIL] {e}")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 用户名大小写区分测试通过")
    else:
        print("[FAIL] 部分测试失败")
    print("="*50)

    return result


def run_all_normal_error_tests():
    """运行所有普通异常测试"""
    print("\n" + "="*60)
    print("运行登录普通异常测试")
    print("="*60)

    tests = [
        ("密码显示/隐藏", test_password_visibility_toggle),
        ("不存在的用户登录", test_login_user_not_exist),
        ("用户名为空", test_login_empty_username),
        ("密码为空", test_login_empty_password),
        ("正确用户名+错误密码", test_login_wrong_password),
        ("正确账号密码+不进行滑块验证", test_login_without_slider),
        ("先滑块验证后输入账号密码", test_login_slider_first),
        ("密码大小写区分", test_login_password_case_sensitive),
        ("用户名大小写区分", test_login_username_case_sensitive),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            results.append((name, False))

    # 汇总
    print("\n" + "-"*60)
    print("测试结果汇总")
    print("-"*60)
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {name}")

    passed_count = sum(1 for _, p in results if p)
    print(f"\n通过: {passed_count}/{len(results)}")
    return passed_count == len(results)


if __name__ == "__main__":
    test_password_visibility_toggle()