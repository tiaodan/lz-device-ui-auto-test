"""
登录功能 - 正常场景视觉测试
测试正确用户名密码登录 + 滑块验证的视觉效果
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from playwright.sync_api import sync_playwright
from config.config_loader import get_config
from pages.login_page import LoginPage
from visual_test.base import VisualTest
from utils.ssl_handler import safe_navigate


def test_login_ok_visual():
    """测试：正常登录视觉回归"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: 视觉测试 (Visual)")
    print("测试场景: 正常登录 (login_ok)")
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

        # ==================== Step 1: 登录页面初始状态 ====================
        print("\n[Step 1] 截取登录页面初始状态")
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        visual.take_screenshot("login_page_initial")

        # ==================== Step 2: 填写表单 ====================
        print("\n[Step 2] 填写表单并截取")
        login_page.username_input.fill(config.username)
        login_page.password_input.fill(config.password)
        page.wait_for_timeout(300)

        visual.take_screenshot("login_page_filled")

        # ==================== Step 3: 拖动滑块 ====================
        print("\n[Step 3] 拖动滑块并截取")
        login_page.drag_slider()
        page.wait_for_timeout(500)

        visual.take_screenshot("login_page_slider_unlocked")
        visual.take_element_screenshot("slider_unlocked", ".drag, .page-slide-wrap")

        # ==================== Step 4: 点击登录 ====================
        print("\n[Step 4] 点击登录并截取")
        login_page.click_login()
        page.wait_for_timeout(3000)

        # ==================== Step 5: 登录后页面 ====================
        print("\n[Step 5] 截取登录后页面")
        current_url = page.url
        print(f"  当前URL: {current_url}")

        visual.take_screenshot("login_after_submit")

        # ==================== Step 6: 视觉对比 ====================
        print("\n[Step 6] 执行视觉对比")

        # 6.1 对比登录页面初始状态
        print("\n--- 对比: 登录页面初始状态 ---")
        if visual.has_baseline("login_page_initial"):
            cmp_result = visual.compare_images("login_page_initial")
            if cmp_result["match"]:
                print("[PASS] 登录页面初始状态视觉一致")
            else:
                print(f"[FAIL] 登录页面初始状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_page_initial")

        # 6.2 对比表单填写状态
        print("\n--- 对比: 表单填写状态 ---")
        if visual.has_baseline("login_page_filled"):
            cmp_result = visual.compare_images("login_page_filled")
            if cmp_result["match"]:
                print("[PASS] 表单填写状态视觉一致")
            else:
                print(f"[FAIL] 表单填写状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_page_filled")

        # 6.3 对比滑块解锁状态
        print("\n--- 对比: 滑块解锁状态 ---")
        if visual.has_baseline("login_page_slider_unlocked"):
            cmp_result = visual.compare_images("login_page_slider_unlocked")
            if cmp_result["match"]:
                print("[PASS] 滑块解锁状态视觉一致")
            else:
                print(f"[FAIL] 滑块解锁状态差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_page_slider_unlocked")

        # 6.4 对比滑块元素
        print("\n--- 对比: 滑块元素 ---")
        if visual.has_baseline("slider_unlocked"):
            cmp_result = visual.compare_images("slider_unlocked")
            if cmp_result["match"]:
                print("[PASS] 滑块元素视觉一致")
            else:
                print(f"[FAIL] 滑块元素差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("slider_unlocked")

        # 6.5 对比登录后页面
        print("\n--- 对比: 登录后页面 ---")
        if visual.has_baseline("login_after_submit"):
            cmp_result = visual.compare_images("login_after_submit")
            if cmp_result["match"]:
                print("[PASS] 登录后页面视觉一致")
            else:
                print(f"[FAIL] 登录后页面差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            print("[WARN] 无基准图，创建基准图")
            visual.update_baseline("login_after_submit")

        browser.close()

    # ==================== 测试结果 ====================
    print("\n" + "="*50)
    if result:
        print("[PASS] 登录视觉测试全部通过")
    else:
        print("[FAIL] 部分视觉测试失败")
    print("="*50)

    return result


def create_login_ok_baselines():
    """创建 login_ok 视觉测试基准图"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("创建 login_ok 视觉测试基准图")
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
        visual.take_screenshot("login_page_initial")

        # 2. 表单填写状态
        print("\n[2] 表单填写状态基准图")
        login_page.username_input.fill(config.username)
        login_page.password_input.fill(config.password)
        page.wait_for_timeout(300)
        visual.take_screenshot("login_page_filled")

        # 3. 滑块解锁状态
        print("\n[3] 滑块解锁状态基准图")
        login_page.drag_slider()
        page.wait_for_timeout(500)
        visual.take_screenshot("login_page_slider_unlocked")
        visual.take_element_screenshot("slider_unlocked", ".drag, .page-slide-wrap")

        # 4. 登录后页面
        print("\n[4] 登录后页面基准图")
        login_page.click_login()
        page.wait_for_timeout(3000)
        visual.take_screenshot("login_after_submit")

        print("\n[完成] login_ok 所有基准图已创建")

        browser.close()


if __name__ == "__main__":
    import sys
    test_name = sys.argv[1] if len(sys.argv) > 1 else "test"

    if test_name == "baseline":
        create_login_ok_baselines()
    else:
        test_login_ok_visual()