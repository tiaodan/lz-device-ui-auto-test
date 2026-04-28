"""
断言测试有效性验证
模拟各种异常场景，验证断言测试能否检测到问题
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import sync_playwright, expect
from config.config_loader import get_config
from pages.login_page import LoginPage
from assertion_test.base import AssertionTest
from utils.ssl_handler import safe_navigate
from utils.logger import init_default_logger
from mock_test_this_testtool.anomaly_simulator import AnomalySimulator, ANOMALY_SCENARIOS


def run_anomaly_test(anomaly_name: str, simulate_func: callable, logger):
    """运行单个异常测试验证"""
    config = get_config(reload=True)

    logger.section(f"异常场景: {anomaly_name}")

    detected = False
    error_msg = ""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        assertion = AssertionTest(page, config.assertion_screenshot_path)
        simulator = AnomalySimulator(page)

        # 导航到登录页
        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # 模拟异常
        simulate_func(simulator)
        page.wait_for_timeout(500)

        # 运行断言测试，看能否发现问题
        logger.info("[验证] 运行断言测试...")
        try:
            # Step 1: 验证元素可见性
            assertion.assert_visible(login_page.username_input, "用户名输入框")
            assertion.assert_visible(login_page.password_input, "密码输入框")
            assertion.assert_visible(login_page.slider, "滑块验证码")
            assertion.assert_visible(login_page.login_button, "登录按钮")

            # Step 2: 验证元素属性
            assertion.assert_attribute(login_page.username_input, "placeholder", "Username", "用户名提示")
            assertion.assert_attribute(login_page.password_input, "placeholder", "Password", "密码提示")

            # Step 3: 验证按钮文本
            assertion.assert_text_contains(login_page.login_button, "Sign in", "登录按钮")

            logger.fail("未检测到异常 - 测试用例有问题！")

        except Exception as e:
            detected = True
            error_msg = str(e)
            logger.pass_("成功检测到异常")
            logger.error(str(e))

        # 截图记录
        screenshot_path = f"{config.assertion_screenshot_path}/anomaly_{anomaly_name.replace(' ', '_')}.png"
        page.screenshot(path=screenshot_path)
        logger.info(f"[截图] {screenshot_path}")

        browser.close()

    return detected, error_msg


def main():
    """运行所有异常场景验证"""
    config = get_config(reload=True)
    config.ensure_directories()

    # 初始化日志器
    logger = init_default_logger(log_dir=config.log_path)

    logger.section("断言测试有效性验证")
    logger.info("模拟异常场景，验证断言测试能否检测")

    # 使用预定义的异常场景
    anomalies = [
        ("用户名输入框缺失", lambda s: s.simulate_element_missing("#username")),
        ("密码输入框缺失", lambda s: s.simulate_element_missing("#password")),
        ("登录按钮缺失", lambda s: s.simulate_element_missing(".lBtn")),
        ("滑块缺失", lambda s: s.simulate_element_missing(".drag")),
        ("用户名输入框隐藏", lambda s: s.simulate_element_hidden("#username")),
        ("用户名输入框禁用", lambda s: s.simulate_element_disabled("#username")),
        ("登录按钮禁用", lambda s: s.simulate_element_disabled(".lBtn")),
        ("placeholder错误", lambda s: s.simulate_wrong_placeholder("#username", "WrongHint")),
        ("按钮文本错误", lambda s: s.simulate_wrong_button_text(".lBtn", "WrongText")),
        ("白屏", lambda s: s.simulate_white_screen()),
        ("用户名输入框重复", lambda s: s.simulate_element_duplicate("#username")),
        ("元素位置错误", lambda s: s.simulate_element_position_wrong("#username")),
    ]

    results = []

    for name, simulate_func in anomalies:
        detected, error_msg = run_anomaly_test(name, simulate_func, logger)
        results.append((name, detected, error_msg))

    # 汇总结果
    logger.section("验证结果汇总")

    passed = 0
    failed = 0

    for name, detected, error_msg in results:
        if detected:
            logger.pass_(f"{name}: 能检测")
            passed += 1
        else:
            logger.fail(f"{name}: 未检测 - 测试用例需改进")
            failed += 1

    logger.result(passed, len(results))

    if failed > 0:
        logger.warn("部分异常场景未检测到，建议改进测试用例")

    return failed == 0


if __name__ == "__main__":
    main()