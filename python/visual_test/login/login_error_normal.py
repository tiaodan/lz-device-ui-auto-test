"""
登录功能 - 密码显示/隐藏功能视觉测试
测试密码输入框的眼睛图标切换视觉效果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from playwright.sync_api import sync_playwright
from config.config_loader import get_config
from pages.login_page import LoginPage
from visual_test.base import VisualTest
from utils.ssl_handler import safe_navigate


def test_password_visibility_visual():
    """测试：密码显示/隐藏功能视觉效果"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 视觉测试 (Visual)")
    print("测试场景: 密码显示/隐藏功能")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # ==================== Step 1: 访问登录页 ====================
        print("\n[Step 1] 访问登录页面")
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== Step 2: 输入密码 ====================
        print("\n[Step 2] 输入密码")
        login_page.password_input.fill(config.password)  # lzno1root
        page.wait_for_timeout(300)

        # ==================== Step 3: 截取密码隐藏状态 ====================
        print("\n[Step 3] 截取密码隐藏状态 (type=password)")
        # 密码框显示为 ********* (9个星号)
        visual.take_screenshot("password_hidden_state")
        visual.take_element_screenshot("password_input_hidden", "#password")

        # ==================== Step 4: 查找并点击眼睛图标 ====================
        print("\n[Step 4] 点击眼睛图标显示密码")

        # 查找眼睛按钮
        eye_selectors = [
            "[class*='eye']",
            ".password-toggle",
            "[class*='visibility']",
            "#password + button",
            "#password ~ button",
            "button[class*='eye']",
        ]

        eye_button = None
        for selector in eye_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0:
                    eye_button = locator.first
                    print(f"  找到眼睛按钮: {selector}")
                    break
            except:
                continue

        if eye_button:
            # 截取眼睛图标初始状态
            visual.take_element_screenshot("eye_icon_initial", eye_selectors[0])

            eye_button.click()
            page.wait_for_timeout(300)
        else:
            print("[WARN] 未找到眼睛按钮")
            browser.close()
            return False

        # ==================== Step 5: 截取密码显示状态 ====================
        print("\n[Step 5] 截取密码显示状态 (type=text)")
        # 密码框显示为 lzno1root (真实密码)
        visual.take_screenshot("password_visible_state")
        visual.take_element_screenshot("password_input_visible", "#password")
        visual.take_element_screenshot("eye_icon_clicked", eye_selectors[0])

        # ==================== Step 6: 再次点击隐藏密码 ====================
        print("\n[Step 6] 再次点击眼睛图标隐藏密码")
        eye_button.click()
        page.wait_for_timeout(300)

        # ==================== Step 7: 截取密码再次隐藏状态 ====================
        print("\n[Step 7] 截取密码再次隐藏状态")
        visual.take_screenshot("password_hidden_again")
        visual.take_element_screenshot("password_input_hidden_again", "#password")
        visual.take_element_screenshot("eye_icon_reset", eye_selectors[0])

        # ==================== Step 8: 视觉对比 ====================
        print("\n[Step 8] 执行视觉对比")

        # 8.1 对比密码隐藏状态
        print("\n--- 对比: 密码隐藏状态 ---")
        if visual.has_baseline("password_hidden_state"):
            cmp_result = visual.compare_images("password_hidden_state")
            if cmp_result["match"]:
                print("[PASS] 密码隐藏状态视觉一致")
            else:
                print(f"[FAIL] 密码隐藏状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("password_hidden_state")

        # 8.2 对比密码输入框隐藏状态
        print("\n--- 对比: 密码输入框隐藏状态 ---")
        if visual.has_baseline("password_input_hidden"):
            cmp_result = visual.compare_images("password_input_hidden")
            if cmp_result["match"]:
                print("[PASS] 密码输入框隐藏状态视觉一致")
            else:
                print(f"[FAIL] 密码输入框隐藏状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("password_input_hidden")

        # 8.3 对比密码显示状态
        print("\n--- 对比: 密码显示状态 ---")
        if visual.has_baseline("password_visible_state"):
            cmp_result = visual.compare_images("password_visible_state")
            if cmp_result["match"]:
                print("[PASS] 密码显示状态视觉一致")
            else:
                print(f"[FAIL] 密码显示状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("password_visible_state")

        # 8.4 对比密码输入框显示状态
        print("\n--- 对比: 密码输入框显示状态 ---")
        if visual.has_baseline("password_input_visible"):
            cmp_result = visual.compare_images("password_input_visible")
            if cmp_result["match"]:
                print("[PASS] 密码输入框显示状态视觉一致")
            else:
                print(f"[FAIL] 密码输入框显示状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("password_input_visible")

        # 8.5 对比眼睛图标初始状态
        print("\n--- 对比: 眼睛图标初始状态 ---")
        if visual.has_baseline("eye_icon_initial"):
            cmp_result = visual.compare_images("eye_icon_initial")
            if cmp_result["match"]:
                print("[PASS] 眼睛图标初始状态视觉一致")
            else:
                print(f"[FAIL] 眼睛图标初始状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("eye_icon_initial")

        # 8.6 对比眼睛图标点击后状态
        print("\n--- 对比: 眼睛图标点击后状态 ---")
        if visual.has_baseline("eye_icon_clicked"):
            cmp_result = visual.compare_images("eye_icon_clicked")
            if cmp_result["match"]:
                print("[PASS] 眼睛图标点击后状态视觉一致")
            else:
                print(f"[FAIL] 眼睛图标点击后状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("eye_icon_clicked")

        # 8.7 对比密码再次隐藏状态
        print("\n--- 对比: 密码再次隐藏状态 ---")
        if visual.has_baseline("password_hidden_again"):
            cmp_result = visual.compare_images("password_hidden_again")
            if cmp_result["match"]:
                print("[PASS] 密码再次隐藏状态视觉一致")
            else:
                print(f"[FAIL] 密码再次隐藏状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("password_hidden_again")

        browser.close()

    # ==================== 测试结果 ====================
    print("\n" + "="*50)
    if result:
        print("[PASS] 密码显示/隐藏视觉测试全部通过")
    else:
        print("[FAIL] 部分视觉测试失败")
    print("="*50)

    return result


def create_password_visibility_baselines():
    """创建密码显示/隐藏视觉测试基准图"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("创建密码显示/隐藏视觉测试基准图")
    print("="*50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 有头模式方便观察
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.baseline_path,  # 直接保存到 baseline
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # 输入密码
        print("\n[1] 输入密码")
        login_page.password_input.fill(config.password)
        page.wait_for_timeout(300)

        # 查找眼睛按钮
        eye_selectors = ["[class*='eye']", ".password-toggle", "[class*='visibility']"]
        eye_button = None
        for selector in eye_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0:
                    eye_button = locator.first
                    break
            except:
                continue

        # 截取隐藏状态
        print("\n[2] 密码隐藏状态基准图")
        visual.take_screenshot("password_hidden_state")
        visual.take_element_screenshot("password_input_hidden", "#password")
        if eye_button:
            visual.take_element_screenshot("eye_icon_initial", eye_selectors[0])

        # 点击显示密码
        print("\n[3] 点击眼睛图标显示密码")
        if eye_button:
            eye_button.click()
            page.wait_for_timeout(300)

        # 截取显示状态
        print("\n[4] 密码显示状态基准图")
        visual.take_screenshot("password_visible_state")
        visual.take_element_screenshot("password_input_visible", "#password")
        if eye_button:
            visual.take_element_screenshot("eye_icon_clicked", eye_selectors[0])

        # 再次隐藏
        print("\n[5] 再次点击隐藏密码")
        if eye_button:
            eye_button.click()
            page.wait_for_timeout(300)

        # 截取再次隐藏状态
        print("\n[6] 密码再次隐藏状态基准图")
        visual.take_screenshot("password_hidden_again")

        print("\n[完成] 密码显示/隐藏所有基准图已创建")

        browser.close()


def test_login_wrong_password_visual():
    """测试：正确的用户名+错误密码视觉效果"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 视觉测试 (Visual)")
    print("测试场景: 正确的用户名+错误密码 (login_error_business)")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # ==================== Step 1: 访问登录页 ====================
        print("\n[Step 1] 访问登录页面")
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual.take_screenshot("login_page_initial_business")

        # ==================== Step 2: 输入正确用户名+错误密码 ====================
        print("\n[Step 2] 输入正确用户名+错误密码")
        login_page.username_input.fill(config.username)  # root (正确)
        login_page.password_input.fill("lz")  # lz (错误密码)
        page.wait_for_timeout(300)

        print(f"  用户名: {config.username} (正确)")
        print(f"  密码: lz (错误)")

        visual.take_screenshot("login_page_wrong_password_filled")
        visual.take_element_screenshot("username_input_filled", "#username")
        visual.take_element_screenshot("password_input_wrong", "#password")

        # ==================== Step 3: 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        login_page.drag_slider()
        page.wait_for_timeout(500)

        visual.take_screenshot("login_page_slider_unlocked_business")

        # ==================== Step 4: 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        login_page.click_login()
        page.wait_for_timeout(2000)

        # ==================== Step 5: 截取登录失败状态 ====================
        print("\n[Step 5] 截取登录失败状态")
        visual.take_screenshot("login_failed_wrong_password")

        # 截取错误提示区域（如果有）
        error_selectors = [
            ".ui-message-error",
            "[class*='error']",
            "[class*='message-error']",
            ".toast-error",
            ".alert-error",
        ]

        for selector in error_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0 and locator.is_visible():
                    visual.take_element_screenshot("error_message_display", selector)
                    print(f"  找到错误提示: {selector}")
                    break
            except:
                continue

        # ==================== Step 6: 截取页面仍在登录页 ====================
        print("\n[Step 6] 截取页面状态（验证仍在登录页）")
        current_url = page.url
        print(f"  当前URL: {current_url}")

        visual.take_screenshot("login_page_after_fail")

        # 截取输入框状态（应该仍可操作）
        visual.take_element_screenshot("username_input_after_fail", "#username")
        visual.take_element_screenshot("password_input_after_fail", "#password")

        # ==================== Step 7: 视觉对比 ====================
        print("\n[Step 7] 执行视觉对比")

        # 7.1 对比登录页面初始状态
        print("\n--- 对比: 登录页面初始状态 ---")
        if visual.has_baseline("login_page_initial_business"):
            cmp_result = visual.compare_images("login_page_initial_business")
            if cmp_result["match"]:
                print("[PASS] 登录页面初始状态视觉一致")
            else:
                print(f"[FAIL] 登录页面初始状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_page_initial_business")

        # 7.2 对比表单填写状态
        print("\n--- 对比: 表单填写状态 ---")
        if visual.has_baseline("login_page_wrong_password_filled"):
            cmp_result = visual.compare_images("login_page_wrong_password_filled")
            if cmp_result["match"]:
                print("[PASS] 表单填写状态视觉一致")
            else:
                print(f"[FAIL] 表单填写状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_page_wrong_password_filled")

        # 7.3 对比用户名输入框
        print("\n--- 对比: 用户名输入框 ---")
        if visual.has_baseline("username_input_filled"):
            cmp_result = visual.compare_images("username_input_filled")
            if cmp_result["match"]:
                print("[PASS] 用户名输入框视觉一致")
            else:
                print(f"[FAIL] 用户名输入框差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("username_input_filled")

        # 7.4 对比密码输入框
        print("\n--- 对比: 密码输入框 ---")
        if visual.has_baseline("password_input_wrong"):
            cmp_result = visual.compare_images("password_input_wrong")
            if cmp_result["match"]:
                print("[PASS] 密码输入框视觉一致")
            else:
                print(f"[FAIL] 密码输入框差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("password_input_wrong")

        # 7.5 对比登录失败页面
        print("\n--- 对比: 登录失败页面 ---")
        if visual.has_baseline("login_failed_wrong_password"):
            cmp_result = visual.compare_images("login_failed_wrong_password")
            if cmp_result["match"]:
                print("[PASS] 登录失败页面视觉一致")
            else:
                print(f"[FAIL] 登录失败页面差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_failed_wrong_password")

        # 7.6 对比登录后页面状态
        print("\n--- 对比: 登录后页面状态 ---")
        if visual.has_baseline("login_page_after_fail"):
            cmp_result = visual.compare_images("login_page_after_fail")
            if cmp_result["match"]:
                print("[PASS] 登录后页面状态视觉一致")
            else:
                print(f"[FAIL] 登录后页面状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_page_after_fail")

        # 7.7 对比用户名输入框失败后状态
        print("\n--- 对比: 用户名输入框失败后状态 ---")
        if visual.has_baseline("username_input_after_fail"):
            cmp_result = visual.compare_images("username_input_after_fail")
            if cmp_result["match"]:
                print("[PASS] 用户名输入框失败后状态视觉一致")
            else:
                print(f"[FAIL] 用户名输入框失败后状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("username_input_after_fail")

        # 7.8 对比密码输入框失败后状态
        print("\n--- 对比: 密码输入框失败后状态 ---")
        if visual.has_baseline("password_input_after_fail"):
            cmp_result = visual.compare_images("password_input_after_fail")
            if cmp_result["match"]:
                print("[PASS] 密码输入框失败后状态视觉一致")
            else:
                print(f"[FAIL] 密码输入框失败后状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("password_input_after_fail")

        browser.close()

    # ==================== 测试结果 ====================
    print("\n" + "="*50)
    if result:
        print("[PASS] 正确用户名+错误密码视觉测试全部通过")
    else:
        print("[FAIL] 部分视觉测试失败")
    print("="*50)

    return result


def create_wrong_password_baselines():
    """创建正确用户名+错误密码视觉测试基准图"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("创建正确用户名+错误密码视觉测试基准图")
    print("="*50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 有头模式方便观察
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.baseline_path,  # 直接保存到 baseline
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # 1. 登录页面初始状态
        print("\n[1] 登录页面初始状态基准图")
        visual.take_screenshot("login_page_initial_business")

        # 2. 填写表单（正确用户名+错误密码）
        print("\n[2] 填写表单基准图")
        login_page.username_input.fill(config.username)  # root
        login_page.password_input.fill("lz")  # 错误密码
        page.wait_for_timeout(300)
        visual.take_screenshot("login_page_wrong_password_filled")
        visual.take_element_screenshot("username_input_filled", "#username")
        visual.take_element_screenshot("password_input_wrong", "#password")

        # 3. 拖动滑块
        print("\n[3] 滑块解锁状态基准图")
        login_page.drag_slider()
        page.wait_for_timeout(500)
        visual.take_screenshot("login_page_slider_unlocked_business")

        # 4. 点击登录
        print("\n[4] 点击登录")
        login_page.click_login()
        page.wait_for_timeout(2000)

        # 5. 登录失败状态
        print("\n[5] 登录失败状态基准图")
        visual.take_screenshot("login_failed_wrong_password")

        # 6. 页面失败后状态
        print("\n[6] 页面失败后状态基准图")
        visual.take_screenshot("login_page_after_fail")
        visual.take_element_screenshot("username_input_after_fail", "#username")
        visual.take_element_screenshot("password_input_after_fail", "#password")

        print("\n[完成] 正确用户名+错误密码所有基准图已创建")

        browser.close()


def test_login_empty_username_visual():
    """测试：用户名为空视觉效果"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 视觉测试 (Visual)")
    print("测试场景: 用户名为空")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # ==================== Step 1: 访问登录页 ====================
        print("\n[Step 1] 访问登录页面")
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual.take_screenshot("login_page_initial_empty_username")

        # ==================== Step 2: 只输入密码，用户名为空 ====================
        print("\n[Step 2] 只输入密码，用户名为空")
        login_page.username_input.fill("")  # 空
        login_page.password_input.fill(config.password)  # lzno1root
        page.wait_for_timeout(300)

        print(f"  用户名: (空)")
        print(f"  密码: {config.password}")

        visual.take_screenshot("login_page_empty_username_filled")
        visual.take_element_screenshot("username_input_empty", "#username")
        visual.take_element_screenshot("password_input_valid", "#password")

        # ==================== Step 3: 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        login_page.drag_slider()
        page.wait_for_timeout(500)

        visual.take_screenshot("login_page_slider_unlocked_empty")

        # ==================== Step 4: 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        login_page.click_login()
        page.wait_for_timeout(2000)

        # ==================== Step 5: 截取登录失败状态 ====================
        print("\n[Step 5] 截取登录失败状态")
        visual.take_screenshot("login_failed_empty_username")

        # 截取错误提示区域
        error_selectors = [
            ".ui-message-error",
            "[class*='error']",
            "[class*='message-error']",
            ".toast-error",
        ]

        for selector in error_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0 and locator.is_visible():
                    visual.take_element_screenshot("error_message_empty_username", selector)
                    break
            except:
                continue

        # ==================== Step 6: 截取页面状态 ====================
        print("\n[Step 6] 截取页面状态")
        current_url = page.url
        print(f"  当前URL: {current_url}")

        visual.take_screenshot("login_page_after_empty_username_fail")

        # ==================== Step 7: 视觉对比 ====================
        print("\n[Step 7] 执行视觉对比")

        comparisons = [
            ("登录页面初始状态", "login_page_initial_empty_username"),
            ("表单填写状态", "login_page_empty_username_filled"),
            ("用户名输入框空", "username_input_empty"),
            ("密码输入框有效", "password_input_valid"),
            ("登录失败页面", "login_failed_empty_username"),
            ("登录后页面状态", "login_page_after_empty_username_fail"),
        ]

        for desc, name in comparisons:
            print(f"\n--- 对比: {desc} ---")
            if visual.has_baseline(name):
                cmp_result = visual.compare_images(name)
                if cmp_result["match"]:
                    print(f"[PASS] {desc}视觉一致")
                else:
                    print(f"[FAIL] {desc}差异 {cmp_result['diff_percent']}%")
                    result = False
            else:
                print("[WARN] 无基准图，创建基准图")
                visual.update_baseline(name)

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 用户名为空视觉测试全部通过")
    else:
        print("[FAIL] 部分视觉测试失败")
    print("="*50)

    return result


def test_login_empty_password_visual():
    """测试：密码为空视觉效果"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 视觉测试 (Visual)")
    print("测试场景: 密码为空")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # ==================== Step 1: 访问登录页 ====================
        print("\n[Step 1] 访问登录页面")
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual.take_screenshot("login_page_initial_empty_password")

        # ==================== Step 2: 只输入用户名，密码为空 ====================
        print("\n[Step 2] 只输入用户名，密码为空")
        login_page.username_input.fill(config.username)  # root
        login_page.password_input.fill("")  # 空
        page.wait_for_timeout(300)

        print(f"  用户名: {config.username}")
        print(f"  密码: (空)")

        visual.take_screenshot("login_page_empty_password_filled")
        visual.take_element_screenshot("username_input_valid", "#username")
        visual.take_element_screenshot("password_input_empty", "#password")

        # ==================== Step 3: 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        login_page.drag_slider()
        page.wait_for_timeout(500)

        visual.take_screenshot("login_page_slider_unlocked_empty_pwd")

        # ==================== Step 4: 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        login_page.click_login()
        page.wait_for_timeout(2000)

        # ==================== Step 5: 截取登录失败状态 ====================
        print("\n[Step 5] 截取登录失败状态")
        visual.take_screenshot("login_failed_empty_password")

        # 截取错误提示区域
        error_selectors = [
            ".ui-message-error",
            "[class*='error']",
            "[class*='message-error']",
            ".toast-error",
        ]

        for selector in error_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0 and locator.is_visible():
                    visual.take_element_screenshot("error_message_empty_password", selector)
                    break
            except:
                continue

        # ==================== Step 6: 截取页面状态 ====================
        print("\n[Step 6] 截取页面状态")
        current_url = page.url
        print(f"  当前URL: {current_url}")

        visual.take_screenshot("login_page_after_empty_password_fail")

        # ==================== Step 7: 视觉对比 ====================
        print("\n[Step 7] 执行视觉对比")

        comparisons = [
            ("登录页面初始状态", "login_page_initial_empty_password"),
            ("表单填写状态", "login_page_empty_password_filled"),
            ("用户名输入框有效", "username_input_valid"),
            ("密码输入框空", "password_input_empty"),
            ("登录失败页面", "login_failed_empty_password"),
            ("登录后页面状态", "login_page_after_empty_password_fail"),
        ]

        for desc, name in comparisons:
            print(f"\n--- 对比: {desc} ---")
            if visual.has_baseline(name):
                cmp_result = visual.compare_images(name)
                if cmp_result["match"]:
                    print(f"[PASS] {desc}视觉一致")
                else:
                    print(f"[FAIL] {desc}差异 {cmp_result['diff_percent']}%")
                    result = False
            else:
                print("[WARN] 无基准图，创建基准图")
                visual.update_baseline(name)

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 密码为空视觉测试全部通过")
    else:
        print("[FAIL] 部分视觉测试失败")
    print("="*50)

    return result


def create_empty_credentials_baselines():
    """创建用户名或密码为空视觉测试基准图"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("创建用户名或密码为空视觉测试基准图")
    print("="*50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.baseline_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # ===== 用户名为空基准图 =====
        print("\n--- 用户名为空基准图 ---")

        print("\n[1] 登录页面初始状态")
        visual.take_screenshot("login_page_initial_empty_username")

        print("\n[2] 只输入密码，用户名为空")
        login_page.username_input.fill("")
        login_page.password_input.fill(config.password)
        page.wait_for_timeout(300)
        visual.take_screenshot("login_page_empty_username_filled")
        visual.take_element_screenshot("username_input_empty", "#username")
        visual.take_element_screenshot("password_input_valid", "#password")

        print("\n[3] 拖动滑块")
        login_page.drag_slider()
        page.wait_for_timeout(500)
        visual.take_screenshot("login_page_slider_unlocked_empty")

        print("\n[4] 点击登录")
        login_page.click_login()
        page.wait_for_timeout(2000)

        print("\n[5] 登录失败状态")
        visual.take_screenshot("login_failed_empty_username")
        visual.take_screenshot("login_page_after_empty_username_fail")

        # 刷新页面
        page.reload()
        page.wait_for_timeout(1000)

        # ===== 密码为空基准图 =====
        print("\n--- 密码为空基准图 ---")

        print("\n[6] 登录页面初始状态")
        visual.take_screenshot("login_page_initial_empty_password")

        print("\n[7] 只输入用户名，密码为空")
        login_page.username_input.fill(config.username)
        login_page.password_input.fill("")
        page.wait_for_timeout(300)
        visual.take_screenshot("login_page_empty_password_filled")
        visual.take_element_screenshot("username_input_valid", "#username")
        visual.take_element_screenshot("password_input_empty", "#password")

        print("\n[8] 拖动滑块")
        login_page.drag_slider()
        page.wait_for_timeout(500)
        visual.take_screenshot("login_page_slider_unlocked_empty_pwd")

        print("\n[9] 点击登录")
        login_page.click_login()
        page.wait_for_timeout(2000)

        print("\n[10] 登录失败状态")
        visual.take_screenshot("login_failed_empty_password")
        visual.take_screenshot("login_page_after_empty_password_fail")

        print("\n[完成] 用户名或密码为空所有基准图已创建")

        browser.close()


def test_login_user_not_exist_visual():
    """测试：不存在的用户登录视觉效果"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 视觉测试 (Visual)")
    print("测试场景: 不存在的用户登录")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # ==================== Step 1: 访问登录页 ====================
        print("\n[Step 1] 访问登录页面")
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual.take_screenshot("login_page_initial_user_not_exist")

        # ==================== Step 2: 输入不存在的用户名+正确密码 ====================
        print("\n[Step 2] 输入不存在的用户名+正确密码")
        login_page.username_input.fill("root1")  # 不存在的用户名
        login_page.password_input.fill(config.password)  # lzno1root
        page.wait_for_timeout(300)

        print(f"  用户名: root1 (不存在)")
        print(f"  密码: {config.password} (正确)")

        visual.take_screenshot("login_page_user_not_exist_filled")
        visual.take_element_screenshot("username_input_not_exist", "#username")
        visual.take_element_screenshot("password_input_correct", "#password")

        # ==================== Step 3: 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块")
        login_page.drag_slider()
        page.wait_for_timeout(500)

        visual.take_screenshot("login_page_slider_unlocked_not_exist")

        # ==================== Step 4: 点击登录 ====================
        print("\n[Step 4] 点击登录按钮")
        login_page.click_login()
        page.wait_for_timeout(2000)

        # ==================== Step 5: 截取登录失败状态 ====================
        print("\n[Step 5] 截取登录失败状态")
        visual.take_screenshot("login_failed_user_not_exist")

        # 截取错误提示区域
        error_selectors = [
            ".ui-message-error",
            "[class*='error']",
            "[class*='message-error']",
            ".toast-error",
        ]

        for selector in error_selectors:
            try:
                locator = page.locator(selector)
                if locator.count() > 0 and locator.is_visible():
                    visual.take_element_screenshot("error_message_user_not_exist", selector)
                    print(f"  找到错误提示: {selector}")
                    break
            except:
                continue

        # ==================== Step 6: 截取页面状态 ====================
        print("\n[Step 6] 截取页面状态")
        current_url = page.url
        print(f"  当前URL: {current_url}")

        visual.take_screenshot("login_page_after_user_not_exist_fail")

        # 截取输入框失败后状态
        visual.take_element_screenshot("username_input_after_not_exist_fail", "#username")
        visual.take_element_screenshot("password_input_after_not_exist_fail", "#password")

        # ==================== Step 7: 视觉对比 ====================
        print("\n[Step 7] 执行视觉对比")

        comparisons = [
            ("登录页面初始状态", "login_page_initial_user_not_exist"),
            ("表单填写状态", "login_page_user_not_exist_filled"),
            ("用户名输入框不存在用户", "username_input_not_exist"),
            ("密码输入框正确", "password_input_correct"),
            ("登录失败页面", "login_failed_user_not_exist"),
            ("登录后页面状态", "login_page_after_user_not_exist_fail"),
            ("用户名输入框失败后", "username_input_after_not_exist_fail"),
            ("密码输入框失败后", "password_input_after_not_exist_fail"),
        ]

        for desc, name in comparisons:
            print(f"\n--- 对比: {desc} ---")
            if visual.has_baseline(name):
                cmp_result = visual.compare_images(name)
                if cmp_result["match"]:
                    print(f"[PASS] {desc}视觉一致")
                else:
                    print(f"[FAIL] {desc}差异 {cmp_result['diff_percent']}%")
                    result = False
            else:
                print("[WARN] 无基准图，创建基准图")
                visual.update_baseline(name)

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 不存在的用户登录视觉测试全部通过")
    else:
        print("[FAIL] 部分视觉测试失败")
    print("="*50)

    return result


def create_user_not_exist_baselines():
    """创建不存在的用户登录视觉测试基准图"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("创建不存在的用户登录视觉测试基准图")
    print("="*50)

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.baseline_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )

        # 1. 登录页面初始状态
        print("\n[1] 登录页面初始状态基准图")
        visual.take_screenshot("login_page_initial_user_not_exist")

        # 2. 填写表单（不存在的用户名+正确密码）
        print("\n[2] 填写表单基准图")
        login_page.username_input.fill("root1")  # 不存在
        login_page.password_input.fill(config.password)
        page.wait_for_timeout(300)
        visual.take_screenshot("login_page_user_not_exist_filled")
        visual.take_element_screenshot("username_input_not_exist", "#username")
        visual.take_element_screenshot("password_input_correct", "#password")

        # 3. 拖动滑块
        print("\n[3] 滑块解锁状态基准图")
        login_page.drag_slider()
        page.wait_for_timeout(500)
        visual.take_screenshot("login_page_slider_unlocked_not_exist")

        # 4. 点击登录
        print("\n[4] 点击登录")
        login_page.click_login()
        page.wait_for_timeout(2000)

        # 5. 登录失败状态
        print("\n[5] 登录失败状态基准图")
        visual.take_screenshot("login_failed_user_not_exist")

        # 6. 页面失败后状态
        print("\n[6] 页面失败后状态基准图")
        visual.take_screenshot("login_page_after_user_not_exist_fail")
        visual.take_element_screenshot("username_input_after_not_exist_fail", "#username")
        visual.take_element_screenshot("password_input_after_not_exist_fail", "#password")

        print("\n[完成] 不存在的用户登录所有基准图已创建")

        browser.close()


def run_all_business_error_visual_tests():
    """运行所有业务异常视觉测试"""

    print("\n" + "="*60)
    print("运行登录业务异常视觉测试")
    print("="*60)

    tests = [
        ("正确用户名+错误密码", test_login_wrong_password_visual),
        ("用户名为空", test_login_empty_username_visual),
        ("密码为空", test_login_empty_password_visual),
        ("不存在的用户登录", test_login_user_not_exist_visual),
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
    return passed_count == len(results)


if __name__ == "__main__":
    import sys
    test_name = sys.argv[1] if len(sys.argv) > 1 else "test"

    if test_name == "baseline":
        create_password_visibility_baselines()
    elif test_name == "password":
        test_password_visibility_visual()
    elif test_name == "password_baseline":
        create_password_visibility_baselines()
    elif test_name == "wrong_password":
        test_login_wrong_password_visual()
    elif test_name == "wrong_password_baseline":
        create_wrong_password_baselines()
    elif test_name == "empty_username":
        test_login_empty_username_visual()
    elif test_name == "empty_password":
        test_login_empty_password_visual()
    elif test_name == "empty_baseline":
        create_empty_credentials_baselines()
    elif test_name == "user_not_exist":
        test_login_user_not_exist_visual()
    elif test_name == "user_not_exist_baseline":
        create_user_not_exist_baselines()
    elif test_name == "business":
        run_all_business_error_visual_tests()
    else:
        test_password_visibility_visual()
        test_password_visibility_visual()