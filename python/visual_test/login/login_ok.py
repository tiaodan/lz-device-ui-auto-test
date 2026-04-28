"""
登录功能 - 正常场景视觉测试
"""

import pytest


@pytest.mark.visual
@pytest.mark.login
def test_login_ok_visual(login_page, visual_test, test_logger, config):
    """测试：正常登录视觉回归"""

    test_logger.section("视觉测试: 正常登录 (login_ok)")
    result = True

    # Step 1: 登录页面初始状态
    test_logger.step(1, "截取登录页面初始状态")
    visual_test.take_screenshot("login_page_initial")

    # Step 2: 填写表单
    test_logger.step(2, "填写表单并截取")
    login_page.username_input.fill(config.username)
    login_page.password_input.fill(config.password)
    login_page.page.wait_for_timeout(300)
    visual_test.take_screenshot("login_page_filled")

    # Step 3: 拖动滑块
    test_logger.step(3, "拖动滑块并截取")
    login_page.drag_slider()
    login_page.page.wait_for_timeout(500)
    visual_test.take_screenshot("login_page_slider_unlocked")
    visual_test.take_element_screenshot("slider_unlocked", ".drag")

    # Step 4: 点击登录
    test_logger.step(4, "点击登录并截取")
    login_page.click_login()
    login_page.page.wait_for_timeout(3000)

    # Step 5: 登录后页面
    test_logger.step(5, "截取登录后页面")
    test_logger.info(f"当前URL: {login_page.page.url}")
    visual_test.take_screenshot("login_after_submit")

    # Step 6: 视觉对比
    test_logger.step(6, "执行视觉对比")

    comparisons = [
        "login_page_initial",
        "login_page_filled",
        "login_page_slider_unlocked",
        "slider_unlocked",
        "login_after_submit"
    ]

    for name in comparisons:
        test_logger.info(f"对比: {name}")
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
        test_logger.pass_("登录视觉测试全部通过")
    else:
        test_logger.fail("部分视觉测试失败")
        pytest.fail("部分视觉测试失败")