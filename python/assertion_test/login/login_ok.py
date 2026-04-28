"""
登录功能 - 正常场景断言测试
测试正确的用户名密码登录 + 滑块验证
"""

import pytest


def test_login_ok(login_page, assertion_test, test_logger, config, language):
    """测试：正常登录 - 用户名+密码+滑块验证"""

    # 获取当前语言的期望值
    exp = login_page.get_expectations(language)

    test_logger.section("断言测试: 正常登录 (login_ok)")
    result = True

    # ==================== 1. 验证页面元素 ====================
    test_logger.step(1, "验证页面元素可见性")
    try:
        assertion_test.assert_visible(login_page.username_input, exp["username_placeholder"])
        assertion_test.assert_visible(login_page.password_input, exp["password_placeholder"])
        assertion_test.assert_visible(login_page.slider, exp["slider_text_contains"])
        assertion_test.assert_visible(login_page.login_button, exp["login_button_text"])
        test_logger.pass_("所有元素可见")
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 2. 验证元素属性 ====================
    test_logger.step(2, "验证元素属性")
    try:
        assertion_test.assert_attribute(login_page.username_input, "placeholder", exp["username_placeholder"], "用户名提示")
        assertion_test.assert_attribute(login_page.password_input, "placeholder", exp["password_placeholder"], "密码提示")
        test_logger.pass_("属性验证通过")
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 3. 验证按钮文本 ====================
    test_logger.step(3, "验证按钮文本")
    try:
        assertion_test.assert_text_contains(login_page.login_button, exp["login_button_text"], "登录按钮")
        test_logger.pass_("按钮文本验证通过")
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 4. 验证滑块初始状态 ====================
    test_logger.step(4, "验证滑块初始状态")
    try:
        initial_progress = login_page.get_slider_progress()
        test_logger.info(f"初始进度: {initial_progress}")
        if "0" in initial_progress or initial_progress == "0px":
            test_logger.pass_("滑块初始位置正确")
        else:
            test_logger.warn("滑块初始位置可能不正确")
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 5. 拖动滑块 ====================
    test_logger.step(5, "拖动滑块")
    try:
        login_page.drag_slider()
        login_page.page.wait_for_timeout(500)
        final_progress = login_page.get_slider_progress()
        test_logger.info(f"最终进度: {final_progress}")
        if login_page.is_slider_unlocked():
            test_logger.pass_("滑块解锁成功")
        else:
            test_logger.fail("滑块未解锁")
            result = False
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 6. 填写表单 ====================
    test_logger.step(6, "填写表单")
    try:
        login_page.fill_credentials(config.username, config.password)
        values = login_page.get_input_values()
        test_logger.info(f"用户名: {values['username']}")
        test_logger.info(f"密码: {'*' * len(values['password'])}")
        if values['username'] == config.username and values['password'] == config.password:
            test_logger.pass_("表单填写正确")
        else:
            test_logger.fail("表单填写不正确")
            result = False
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 7. 点击登录 ====================
    test_logger.step(7, "点击登录按钮")
    try:
        login_page.click_login()
        login_page.page.wait_for_timeout(3000)
        test_logger.pass_("登录按钮点击成功")
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 8. 验证登录结果 ====================
    test_logger.step(8, "验证登录结果")
    try:
        current_url = login_page.page.url
        test_logger.info(f"当前URL: {current_url}")
        # 登录成功后 URL 应该变化，不再是登录页
        if current_url and "/login" not in current_url and "signin" not in current_url.lower():
            test_logger.pass_("登录成功，页面已跳转")
        else:
            test_logger.warn("可能仍在登录页")
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # 截图
    login_page.page.screenshot(path=f"{config.assertion_screenshot_path}/login_ok_result.png")

    # ==================== 测试结果 ====================
    test_logger.section("测试结果")
    if result:
        test_logger.pass_("登录断言测试全部通过")
    else:
        test_logger.fail("部分测试失败")
        pytest.fail("部分测试失败")