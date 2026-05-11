"""
登录功能 - 正常场景断言测试
测试正确的用户名密码登录 + 滑块验证


推荐测试分类：
# 第1类：元素可见性（元素都在吗？）
# 第2类：属性（文本/placeholder对吗？，颜色对吗？图标对吗？）
# 第3类：行为（能操作吗？）显示/隐藏，点击，禁用
    assert_enabled(username_input)
    assert_enabled(password_input)
# 第4类：功能（操作后结果对吗？）
    fill_credentials()
    drag_slider()
    click_login()
    assert_url_changed()

日志描述使用 config.messages 统一管理，方便多语言支持。
"""

import pytest
from pages.login_page import LoginPage
from assertion_test.base import AssertionTest
from config.config_loader import Config
from utils.test_logger import StepLogger


def test_login_ok(login_page: LoginPage, assertion_test_not_logged: AssertionTest, test_logger: StepLogger, config: Config):
    """测试：正常登录 - 用户名+密码+滑块验证"""

    test_logger.section("断言测试: 正常登录 (login_ok)")
    result = True
    msg = config.messages  # 日志描述统一从配置读取

    # ==================== 第1类：元素可见性 ====================
    test_logger.step(1, msg["step_1"])
    try:
        assertion_test_not_logged.assert_visible(login_page.logo, login_page.desc["logo"])                      # logo
        assertion_test_not_logged.assert_visible(login_page.sys_name, login_page.desc["sys_name"])              # 系统名字
        assertion_test_not_logged.assert_visible(login_page.language_switch, login_page.desc["language_switch"]) # 语言切换按钮
        assertion_test_not_logged.assert_visible(login_page.username_input, login_page.desc["username_input"])  # 输入框，username, 固定描述，不变
        assertion_test_not_logged.assert_visible(login_page.password_input, login_page.desc["password_input"])  # 输入框，password
        assertion_test_not_logged.assert_visible(login_page.slider, login_page.desc["slider_container"])        # 滑块条
        assertion_test_not_logged.assert_visible(login_page.login_button, login_page.desc["login_button"])      # 登录按钮
        test_logger.pass_(msg["all_element_visible"])
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 第2类：属性（文本/placeholder对吗？，颜色对吗？图标对吗？） ====================
    test_logger.step(2, msg["step_2"])
    try:
        # -- 文本（用 assert_text 精确匹配，测试就是要测得准）
        assertion_test_not_logged.assert_attribute(login_page.logo, "alt", login_page.exp["logo_alt"], login_page.desc["logo"])  # logo alt 属性
        assertion_test_not_logged.assert_text(login_page.sys_name, login_page.exp["sys_name"], login_page.desc["sys_name"])  # 系统名文本
        # 表单 placeholder（HTML 属性，精确匹配）
        assertion_test_not_logged.assert_attribute(login_page.username_input, "placeholder", login_page.exp["username_placeholder"], login_page.desc["username_input"])
        assertion_test_not_logged.assert_attribute(login_page.password_input, "placeholder", login_page.exp["password_placeholder"], login_page.desc["password_input"])
        # 滑块和按钮文本（精确匹配）
        assertion_test_not_logged.assert_text(login_page.slider_text, login_page.exp["slider_text"], login_page.desc["slider_container"])
        assertion_test_not_logged.assert_text(login_page.login_button, login_page.exp["login_button_text"], login_page.desc["login_button"])

        # -- 图标（src 精确匹配，配置文件写完整路径）
        assertion_test_not_logged.assert_attribute(login_page.logo, "src", login_page.exp["logo_src"], login_page.desc["logo"])
        test_logger.pass_(msg["attribute_passed"])
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # ==================== 第3类：行为（能操作吗？）显示/隐藏，点击，禁用 ====================
    # ==================== 第4类：功能（操作后结果对吗？） ====================
    test_logger.step(4, msg["step_4"])

    # -- 填写表单
    test_logger.info("填写表单")
    try:
        login_page.fill_credentials(config.username, config.password)  # 输入用户名+密码
        values = login_page.get_input_values()   # 获取输入框当前值
        test_logger.info(f"用户名: {values['username']}")
        test_logger.info(f"密码: {'*' * len(values['password'])}")
        if values['username'] == config.username and values['password'] == config.password:  # 读出的结果 = 配置里配的，算通过
            test_logger.pass_(msg["form_filled_correct"])
        else:
            test_logger.fail(msg["form_filled_wrong"])
            result = False
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # -- 滑块初始
    test_logger.info("滑块初始验证")
    try:
        initial_progress = login_page.get_slider_progress()
        test_logger.info(f"初始进度: {initial_progress}")
        if "0" in initial_progress or initial_progress == "0px":
            test_logger.pass_(msg["slider_initial_correct"])
        else:
            test_logger.warn(msg["slider_initial_warn"])
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # -- 滑块拖动
    test_logger.info("滑块拖动")
    try:
        login_page.drag_slider()
        login_page.page.wait_for_timeout(500)
        final_progress = login_page.get_slider_progress()  # 最终进度条
        test_logger.info(f"最终进度: {final_progress}")
        if login_page.is_slider_unlocked():  # > 300px 就算解锁
            test_logger.pass_(msg["slider_unlocked"])
        else:
            test_logger.fail(msg["slider_not_unlocked"])
            result = False
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # -- 点击登录
    test_logger.info("点击登录")
    test_logger.info(f"点击前URL: {login_page.page.url}")
    try:
        login_page.click_login()
        login_page.page.wait_for_timeout(3000)  # 固定等待3秒
        test_logger.info(f"点击后URL: {login_page.page.url}")
        test_logger.pass_(msg["login_button_clicked"])
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # -- 验证登录结果
    test_logger.info("验证登录结果")
    try:
        current_url = login_page.page.url
        test_logger.info(f"当前URL: {current_url}")
        # 登录成功后 URL 应该变化，不再是登录页。判断条件：current_url存在，且不包含 "/login" 或 "signin"（大小写不敏感）-这2个有没有都没关系， 必须包含 "dashboard"
        if current_url and "/login" not in current_url and "signin" not in current_url.lower() and "dashboard" in current_url:
            test_logger.pass_(msg["login_success"])
        else:
            test_logger.warn(msg["login_page_warn"])
    except Exception as e:
        test_logger.fail(str(e))
        result = False

    # 截图（pytest 失败时自动截图到 screenshots/failures/，成功时是否截图由配置控制）
    if config.screenshot_on_success:
        login_page.page.screenshot(path=f"{config.assertion_screenshot_path}/login/login_ok_result.png")

    # ==================== 测试结果 ====================
    test_logger.section("测试结果")
    if result:
        test_logger.pass_(msg["test_all_passed"])
    else:
        test_logger.fail(msg["test_partial_failed"])
        pytest.fail(msg["test_partial_failed"])