"""
登录功能断言测试
测试元素可见性、文本、属性等
"""

import pytest
from playwright.sync_api import expect


@pytest.mark.assertion
@pytest.mark.login
def test_login_page_elements(login_page, assertion_test, test_logger, config):
    """测试：登录页面元素可见性"""

    test_logger.section("断言测试: 登录页面元素验证")

    test_logger.step(1, "验证元素可见性")
    assertion_test.assert_visible(login_page.username_input, "用户名输入框")
    assertion_test.assert_visible(login_page.password_input, "密码输入框")
    assertion_test.assert_visible(login_page.slider, "滑块验证码")
    assertion_test.assert_visible(login_page.login_button, "登录按钮")
    assertion_test.assert_visible(login_page.logo, "Logo")
    test_logger.pass_("所有元素可见")

    test_logger.step(2, "验证元素可用性")
    assertion_test.assert_enabled(login_page.username_input, "用户名输入框")
    assertion_test.assert_enabled(login_page.password_input, "密码输入框")
    assertion_test.assert_enabled(login_page.login_button, "登录按钮")
    test_logger.pass_("所有元素可用")

    test_logger.step(3, "验证占位符文本")
    assertion_test.assert_attribute(login_page.username_input, "placeholder", "Username", "用户名提示")
    assertion_test.assert_attribute(login_page.password_input, "placeholder", "Password", "密码提示")
    test_logger.pass_("占位符文本正确")

    test_logger.step(4, "验证按钮文本")
    assertion_test.assert_text_contains(login_page.login_button, "Sign in", "登录按钮")
    test_logger.pass_("按钮文本正确")

    test_logger.step(5, "验证滑块提示")
    assertion_test.assert_text_contains(login_page.slider_text, "slide", "滑块提示")
    test_logger.pass_("滑块提示正确")

    login_page.page.screenshot(path=f"{config.assertion_screenshot_path}/login_elements.png")

    test_logger.section("测试结果")
    test_logger.pass_("断言测试全部通过")


@pytest.mark.assertion
@pytest.mark.login
def test_login_slider_progress(login_page, test_logger, config):
    """测试：滑块进度验证"""

    test_logger.section("断言测试: 滑块进度验证")

    test_logger.step(1, "验证初始进度")
    initial_progress = login_page.get_slider_progress()
    test_logger.info(f"初始进度: {initial_progress}")

    test_logger.step(2, "拖动滑块")
    login_page.drag_slider()
    test_logger.pass_("滑块拖动完成")

    test_logger.step(3, "验证拖动后进度")
    final_progress = login_page.get_slider_progress()
    test_logger.info(f"最终进度: {final_progress}")

    assert login_page.is_slider_unlocked(), "滑块未解锁"
    test_logger.pass_("滑块解锁成功")

    login_page.page.screenshot(path=f"{config.assertion_screenshot_path}/slider_progress.png")

    test_logger.section("测试结果")
    test_logger.pass_("滑块断言测试通过")


@pytest.mark.assertion
@pytest.mark.login
def test_login_form_fill(login_page, assertion_test, test_logger, config):
    """测试：表单填写验证"""

    test_logger.section("断言测试: 表单填写验证")

    test_logger.step(1, "填写用户名")
    login_page.fill_credentials(config.username, config.password)
    test_logger.pass_("表单填写完成")

    test_logger.step(2, "验证填写值")
    values = login_page.get_input_values()
    assertion_test.assert_input_value(login_page.username_input, config.username, "用户名")
    assertion_test.assert_input_value(login_page.password_input, config.password, "密码")
    test_logger.pass_("填写值正确")

    login_page.page.screenshot(path=f"{config.assertion_screenshot_path}/form_filled.png")

    test_logger.section("测试结果")
    test_logger.pass_("表单断言测试通过")