"""
登录功能 - 异常业务测试
测试密码错误、用户不存在等业务异常场景
"""

import pytest


@pytest.mark.api
@pytest.mark.login
def test_login_wrong_password(api_test, test_logger, config):
    """测试：正确的用户名+错误密码"""

    test_logger.section("API测试: 正确用户名+错误密码")

    test_logger.step(1, "使用错误密码登录")
    test_logger.info(f"用户名: {config.username}")
    test_logger.info(f"密码: lz")
    result = api_test.login(config.username, "lz")

    test_logger.step(2, "验证结果")
    if result.get("token"):
        test_logger.fail("不应该登录成功")
        pytest.fail("不应该登录成功")
    else:
        test_logger.pass_("登录被拒绝")
        test_logger.info(f"错误码: {result.get('code', 'N/A')}")
        test_logger.info(f"错误信息: {result.get('msg', 'N/A')}")
        if result.get('code') == 5 and result.get('msg') == 'Incorrect password':
            test_logger.pass_("错误码和信息正确: code=5, msg=Incorrect password")


@pytest.mark.api
@pytest.mark.login
def test_login_empty_username(api_test, test_logger, config):
    """测试：用户名为空"""

    test_logger.section("API测试: 用户名为空")

    test_logger.step(1, "使用空用户名登录")
    test_logger.info(f"用户名: (空)")
    test_logger.info(f"密码: {config.password}")
    result = api_test.login("", config.password)

    test_logger.step(2, "验证结果")
    if result.get("token"):
        test_logger.fail("不应该登录成功")
        pytest.fail("不应该登录成功")
    else:
        test_logger.pass_("登录被拒绝")
        test_logger.info(f"错误码: {result.get('code', 'N/A')}")
        test_logger.info(f"错误信息: {result.get('msg', result.get('error', 'N/A'))}")


@pytest.mark.api
@pytest.mark.login
def test_login_empty_password(api_test, test_logger, config):
    """测试：密码为空"""

    test_logger.section("API测试: 密码为空")

    test_logger.step(1, "使用空密码登录")
    test_logger.info(f"用户名: {config.username}")
    test_logger.info(f"密码: (空)")
    result = api_test.login(config.username, "")

    test_logger.step(2, "验证结果")
    if result.get("token"):
        test_logger.fail("不应该登录成功")
        pytest.fail("不应该登录成功")
    else:
        test_logger.pass_("登录被拒绝")
        test_logger.info(f"错误码: {result.get('code', 'N/A')}")
        test_logger.info(f"错误信息: {result.get('msg', result.get('error', 'N/A'))}")


@pytest.mark.api
@pytest.mark.login
def test_login_user_not_exist(api_test, test_logger, config):
    """测试：用户不存在"""

    test_logger.section("API测试: 用户不存在")

    test_logger.step(1, "使用不存在的用户登录")
    test_logger.info(f"用户名: root1")
    test_logger.info(f"密码: {config.password}")
    result = api_test.login("root1", config.password)

    test_logger.step(2, "验证结果")
    if result.get("token"):
        test_logger.fail("不应该登录成功")
        pytest.fail("不应该登录成功")
    else:
        test_logger.pass_("登录被拒绝")
        test_logger.info(f"错误码: {result.get('code', 'N/A')}")
        test_logger.info(f"错误信息: {result.get('msg', 'N/A')}")
        if result.get('code') == 3:
            test_logger.pass_("错误码正确: 3 (record not found)")


@pytest.mark.api
@pytest.mark.login
def test_login_password_case_sensitive(api_test, test_logger, config):
    """测试：密码大小写区分"""

    test_logger.section("API测试: 密码大小写区分")

    password_upper = config.password.upper()

    test_logger.step(1, "使用大写密码登录")
    test_logger.info(f"用户名: {config.username}")
    test_logger.info(f"密码(大写): {password_upper}")
    result = api_test.login(config.username, password_upper)

    test_logger.step(2, "验证结果")
    if result.get("token"):
        test_logger.fail("不应该登录成功")
        pytest.fail("不应该登录成功")
    else:
        test_logger.pass_("登录被拒绝")
        test_logger.info(f"错误码: {result.get('code', 'N/A')}")
        test_logger.info(f"错误信息: {result.get('msg', 'N/A')}")
        if result.get('msg') == 'Incorrect password':
            test_logger.pass_("错误信息正确: Incorrect password")


@pytest.mark.api
@pytest.mark.login
def test_login_username_case_sensitive(api_test, test_logger, config):
    """测试：用户名大小写区分"""

    test_logger.section("API测试: 用户名大小写区分")

    username_upper = config.username.upper()

    test_logger.step(1, "使用大写用户名登录")
    test_logger.info(f"用户名(大写): {username_upper}")
    test_logger.info(f"密码: {config.password}")
    result = api_test.login(username_upper, config.password)

    test_logger.step(2, "验证结果")
    if result.get("token"):
        test_logger.fail("不应该登录成功")
        pytest.fail("不应该登录成功")
    else:
        test_logger.pass_("登录被拒绝")
        test_logger.info(f"错误码: {result.get('code', 'N/A')}")
        test_logger.info(f"错误信息: {result.get('msg', 'N/A')}")