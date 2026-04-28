"""
登录功能 - 正常场景测试
测试正确的用户名密码登录
"""

import pytest


@pytest.mark.api
@pytest.mark.login
def test_login_ok(api_test, test_logger, config):
    """测试：正常登录"""

    test_logger.section("API测试: 正常登录")

    test_logger.step(1, "发送登录请求")
    test_logger.info(f"URL: {config.login_url}")
    test_logger.info(f"方法: POST")
    test_logger.info(f"参数: username={config.username}, password={config.password}")

    result = api_test.login(config.username, config.password)

    test_logger.step(2, "验证响应")

    # 验证 HTTP 状态码
    if result.get("status_code") == 200:
        test_logger.pass_("HTTP 状态码: 200")
    else:
        test_logger.fail(f"HTTP 状态码: {result.get('status_code')}")
        pytest.fail(f"HTTP 状态码: {result.get('status_code')}")

    # 验证返回数据
    if result.get("token"):
        test_logger.pass_("返回包含 token")
        test_logger.info(f"Token: {result['token'][:40]}...")
        test_logger.info(f"有效期: {int(result['expLen']/1000)} 秒")
        test_logger.info(f"用户ID: {result['user']['id']}")
        test_logger.info(f"用户名: {result['user']['displayName']}")
        test_logger.info(f"角色: {result['user']['role']}")
        test_logger.section("测试结果")
        test_logger.pass_("登录测试通过")
    else:
        test_logger.fail("返回缺少 token")
        test_logger.error(f"错误: {result.get('msg', result)}")
        test_logger.section("测试结果")
        test_logger.fail("登录测试失败")
        pytest.fail(f"登录失败: {result.get('msg', result)}")