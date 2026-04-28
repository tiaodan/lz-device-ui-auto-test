"""
登录功能 - 密码显示/隐藏功能视觉测试
"""

import pytest


@pytest.mark.visual
@pytest.mark.login
def test_password_visibility_visual(login_page, visual_test, test_logger, config):
    """测试：密码显示/隐藏功能视觉效果"""

    test_logger.section("视觉测试: 密码显示/隐藏功能")
    result = True

    # Step 1: 访问登录页
    test_logger.step(1, "访问登录页面")
    visual_test.take_screenshot("login_page_initial_business")

    # Step 2: 输入密码
    test_logger.step(2, "输入密码")
    login_page.password_input.fill(config.password)
    login_page.page.wait_for_timeout(300)
    visual_test.take_screenshot("password_input_correct")

    # Step 3: 查找眼睛图标并点击
    test_logger.step(3, "查找眼睛图标并点击显示密码")
    selectors = ["#password + button", "#password ~ button", "[class*='eye']", "button[class*='eye']"]
    eye_button = None
    for selector in selectors:
        try:
            locator = login_page.page.locator(selector)
            if locator.count() > 0:
                eye_button = locator.first
                test_logger.info(f"找到眼睛按钮: {selector}")
                break
        except:
            continue

    if eye_button:
        # 点击显示密码
        eye_button.click()
        login_page.page.wait_for_timeout(300)
        visual_test.take_screenshot("password_visible_state")

        # 再次点击隐藏密码
        eye_button.click()
        login_page.page.wait_for_timeout(300)
        visual_test.take_screenshot("password_hidden_state")
    else:
        test_logger.warn("未找到眼睛图标按钮")

    # Step 4: 视觉对比
    test_logger.step(4, "执行视觉对比")
    comparisons = ["login_page_initial_business", "password_input_correct", "password_visible_state", "password_hidden_state"]

    for name in comparisons:
        if visual_test.has_baseline(name):
            cmp_result = visual_test.compare_images(name)
            if cmp_result["match"]:
                test_logger.pass_(f"{name} 视觉一致")
            else:
                test_logger.fail(f"{name} 差异 {cmp_result['diff_percent']}%")
                result = False
        else:
            test_logger.warn(f"无基准图 {name}，创建基准图")
            visual_test.update_baseline(name)

    test_logger.section("测试结果")
    if result:
        test_logger.pass_("密码显示/隐藏功能视觉测试通过")
    else:
        test_logger.fail("部分视觉测试失败")
        pytest.fail("部分视觉测试失败")