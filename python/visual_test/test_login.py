"""
登录功能图片识别测试
测试截图对比、视觉回归
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright
from config.config_loader import get_config
from pages.login_page import LoginPage
from visual_test.base import VisualTest


def test_login_page_visual():
    """测试：登录页面视觉回归"""

    config = get_config()
    config.ensure_directories()

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

        print("\n" + "="*50)
        print("测试类型: 图片识别测试 (Visual)")
        print("测试用例: 登录页面视觉回归")
        print("="*50)

        # 访问页面
        page.goto(config.base_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 执行视觉测试
        print("\n[Step 1] 执行视觉对比测试")
        result = visual.visual_test("login_page", auto_update=config.auto_update_baseline)

        if result:
            print("[VISUAL PASS] 登录页面视觉一致")
        else:
            print("[VISUAL FAIL] 登录页面视觉差异")
            print("请检查差异图并确认是否需要更新基准图")

        browser.close()


def test_login_slider_visual():
    """测试：滑块视觉变化"""

    config = get_config()

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

        print("\n" + "="*50)
        print("测试类型: 图片识别测试 (Visual)")
        print("测试用例: 滑块拖动视觉变化")
        print("="*50)

        page.goto(config.base_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 截取滑块初始状态
        print("\n[Step 1] 截取滑块初始状态")
        visual.take_element_screenshot("slider_initial", ".drag")

        # 拖动滑块
        print("\n[Step 2] 拖动滑块")
        login_page.drag_slider()

        # 截取滑块拖动后状态
        print("\n[Step 3] 截取滑块拖动后状态")
        visual.take_element_screenshot("slider_final", ".drag")

        # 对比
        print("\n[Step 4] 创建滑块基准图（首次运行）")
        if not visual.has_baseline("slider_final"):
            visual.update_baseline("slider_final")
            print("[VISUAL] 滑块基准图已创建")

        browser.close()


def test_login_button_visual():
    """测试：登录按钮视觉"""

    config = get_config()

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

        print("\n" + "="*50)
        print("测试类型: 图片识别测试 (Visual)")
        print("测试用例: 登录按钮视觉")
        print("="*50)

        page.goto(config.base_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 截取登录按钮
        print("\n[Step 1] 截取登录按钮")
        visual.take_element_screenshot("login_button", ".lBtn")

        # 创建基准图
        if not visual.has_baseline("login_button"):
            visual.update_baseline("login_button")
            print("[VISUAL] 登录按钮基准图已创建")

        browser.close()


def create_all_baselines():
    """创建所有基准图（用于初始化）"""

    config = get_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 有头模式方便观察
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)

        print("\n" + "="*50)
        print("创建基准图")
        print("="*50)

        page.goto(config.base_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        # 保存页面基准图
        print("\n[1] 页面基准图")
        login_page.take_screenshot("login_page", config.baseline_path)

        # 保存滑块基准图
        print("\n[2] 滑块基准图")
        login_page.drag_slider()
        page.wait_for_timeout(500)
        login_page.take_element_screenshot("slider_final", ".drag", config.baseline_path)

        # 保存按钮基准图
        print("\n[3] 按钮基准图")
        login_page.take_element_screenshot("login_button", ".lBtn", config.baseline_path)

        print("\n[完成] 所有基准图已创建")

        browser.close()


if __name__ == "__main__":
    import sys
    test_name = sys.argv[1] if len(sys.argv) > 1 else "all"

    if test_name == "page":
        test_login_page_visual()
    elif test_name == "slider":
        test_login_slider_visual()
    elif test_name == "button":
        test_login_button_visual()
    elif test_name == "baseline":
        create_all_baselines()
    else:
        test_login_page_visual()
        test_login_slider_visual()
        test_login_button_visual()