"""
登录测试 - Mock 异常验证
通过 JS 注入模拟 UI 异常，验证断言测试能否检测到问题
适配多语言：期望值通过 login_page.exp 获取

==============================
Mock 测试断言效果的常见方面
==============================

第1类：元素缺失
  删除按钮、输入框、表格等

第2类：属性错误
  placeholder、文本、颜色、尺寸

第3类：白屏/错误页
  页面空白、网络错误、404

第4类：元素隐藏
  display:none、visibility:hidden

  需要验证元素 hidden 的场景：
  - 弹窗/对话框：关闭弹窗后，弹窗消失
  - 下拉菜单：点击后菜单收起，菜单隐藏
  - 折叠面板：Accordion 折叠后，内容区隐藏
  - 侧边栏：点击收起按钮，侧边栏隐藏
  - Toast 提示：提示消息消失后隐藏
  - 加载动画：数据加载完成后，loading 隐藏
  - 空状态提示：有数据时，空状态占位符隐藏
  - 错误提示：输入正确后，错误提示隐藏
  - 密码显示切换：点击眼睛图标，密码明文输入框隐藏（切换到密码框）
  - Tab 切换：切换到其他 Tab，当前 Tab 内容隐藏
  - 模态遮罩：关闭弹窗，遮罩层隐藏
  - 悬浮提示：鼠标移开，Tooltip 隐藏
  - 搜索建议：清空搜索框，下拉建议列表隐藏
  - 级联选择器：选择完成，子级菜单隐藏
  - 分页组件：最后一页，下一页按钮隐藏
  - 权限控制：无权限时，操作按钮隐藏
  - 响应式布局：切换到移动端视图，某些导航项隐藏
  核心逻辑：任何"由显→隐"的状态切换，都需要验证 to_be_hidden()

第5类：元素禁用
  disabled、readonly

==============================
下面不太好实现，先不看
==============================
第6类：位置错误
  元素跑到屏幕外、重叠

第7类：元素重复
  同 ID 元素出现多次

第8类：数据异常
  空数据、乱码、超长文本

第9类：响应延迟
  元素晚出现、请求超时

第10类：交互失效
  点击无效、拖拽失败

==============================
断言 vs 视觉 适用场景
==============================

断言适合（功能验证）：
  ✅ 元素缺失
  ✅ 文本错误
  ✅ 属性错误

视觉适合（布局验证）：
  ✅ 位置偏移
  ✅ 元素互换
  ✅ 样式微调
"""

import pytest
from mock_test_this_testtool.anomaly_simulator import AnomalySimulator


@pytest.fixture
def simulator(fresh_page, login_page):
    """异常模拟器 fixture"""
    return AnomalySimulator(fresh_page, module_name="login")


# ==================== 第1类：元素缺失 ====================

def test_username_missing(login_page, assertion_test_not_logged, simulator, test_logger, config):
    """Mock：用户名输入框不存在，断言应检测到"""
    test_logger.section("Mock测试: 用户名输入框缺失")

    count_before = login_page.username_input.count()
    test_logger.info(f"删除前 #username count: {count_before}")

    simulator.simulate_element_missing("username_input")
    # 不需要等待，JS注入立即生效

    count_after = login_page.username_input.count()
    test_logger.info(f"删除后 #username count: {count_after}")

    if config.mock_pause_for_debug:
        login_page.page.pause()

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_visible(login_page.username_input, login_page.exp["username_placeholder"])

    test_logger.pass_("成功检测到：用户名输入框缺失")


def test_password_missing(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：密码输入框不存在，断言应检测到"""
    test_logger.section("Mock测试: 密码输入框缺失")
    simulator.simulate_element_missing("password_input")

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_visible(login_page.password_input, login_page.exp["password_placeholder"])

    test_logger.pass_("成功检测到：密码输入框缺失")


def test_login_button_missing(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：登录按钮不存在，断言应检测到"""
    test_logger.section("Mock测试: 登录按钮缺失")
    simulator.simulate_element_missing("login_button")

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_visible(login_page.login_button, login_page.exp["login_button_text"])

    test_logger.pass_("成功检测到：登录按钮缺失")


def test_slider_missing(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：滑块不存在，断言应检测到"""
    test_logger.section("Mock测试: 滑块缺失")
    simulator.simulate_element_missing("slider_container")

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_visible(login_page.slider, login_page.exp["slider_text_contains"])

    test_logger.pass_("成功检测到：滑块缺失")


# ==================== 第2类：属性错误 placeholder、文本、颜色、尺寸 ====================

# placeholder - username 文本不对
def test_username_wrong_placeholder(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：placeholder 文本错误，断言应检测到"""
    test_logger.section("Mock测试: placeholder文本错误")
    simulator.simulate_wrong_placeholder("username_input", "WRONG_TEXT")

    with pytest.raises(Exception):
        # 断言属性
        assertion_test_not_logged.assert_attribute(
            login_page.username_input, "placeholder",
            login_page.exp["username_placeholder"], "用户名提示"
        )

    test_logger.pass_("成功检测到：placeholder文本错误")


# placeholder - pasword 文本不对
def test_password_wrong_placeholder(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：密码输入框 placeholder 文本错误，断言应检测到"""
    test_logger.section("Mock测试: 密码输入框 placeholder 文本错误")
    simulator.simulate_wrong_placeholder("password_input", "WRONG_password")

    with pytest.raises(Exception):
        # 断言属性
        assertion_test_not_logged.assert_attribute(
            login_page.password_input, "placeholder",
            login_page.exp["password_placeholder"], "密码提示"
        )

    test_logger.pass_("成功检测到：密码输入框 placeholder 文本错误")

# 滑块 - text 错误
def test_slider_wrong_test(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：滑块提示文本错误，断言应检测到"""
    test_logger.section("Mock测试: 滑块提示文本错误")
    simulator.simulate_wrong_text("slider_text", "wrong_slider_text")

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_text_contains(
            login_page.slider_text,
            login_page.exp["slider_text_contains"], "滑块提示"
        )

    test_logger.pass_("成功检测到：滑块提示文本错误")

# 登录按钮 - text 错误
def test_wrong_button_text(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：登录按钮文本错误，断言应检测到"""
    test_logger.section("Mock测试: 登录按钮文本错误")
    simulator.simulate_wrong_text("login_button", "wrong-buttton-text")

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_text_contains(
            login_page.login_button,
            login_page.exp["login_button_text"], "登录按钮"
        )

    test_logger.pass_("成功检测到：登录按钮文本错误")


# ==================== 第3类：白屏 ====================

def test_white_screen(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：白屏，断言应检测到"""
    test_logger.section("Mock测试: 白屏")
    simulator.simulate_white_screen()

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_visible(login_page.username_input, login_page.exp["username_placeholder"])

    test_logger.pass_("成功检测到：白屏")


# ==================== 第4类：元素禁用 ====================

def test_username_disabled(login_page, assertion_test_not_logged, simulator, test_logger):
    """Mock：用户名输入框禁用，断言应检测到"""
    test_logger.section("Mock测试: 用户名输入框禁用")
    simulator.simulate_element_disabled("username_input")

    with pytest.raises(Exception):
        assertion_test_not_logged.assert_enabled(login_page.username_input, login_page.exp["username_placeholder"])

    test_logger.pass_("成功检测到：用户名输入框禁用")
