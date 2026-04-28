"""
登录功能图片识别测试
"""

import pytest


@pytest.mark.visual
@pytest.mark.login
def test_login_page_visual(visual_test_fresh, test_logger, config):
    """测试：登录页面视觉回归"""

    test_logger.section("视觉测试: 登录页面视觉回归")

    test_logger.step(1, "执行视觉对比测试")
    result = visual_test_fresh.visual_test("login_page", auto_update=config.auto_update_baseline)

    if result:
        test_logger.pass_("登录页面视觉一致")
    else:
        test_logger.fail("登录页面视觉差异")
        test_logger.warn("请检查差异图并确认是否需要更新基准图")
        pytest.fail("登录页面视觉差异")