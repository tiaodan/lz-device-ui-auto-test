"""
登录功能 - 正常场景测试
测试正确的用户名密码登录
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.config_loader import get_config
from api_test.base import ApiTest


def test_login_ok():
    """测试：正常登录"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 正常登录")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url,
        username=config.username,
        password=config.password
    )

    print(f"\n[Step 1] 发送登录请求")
    print(f"  URL: {config.login_url}")
    print(f"  方法: POST")
    print(f"  参数: JSON \"username\": \"{config.username}\", \"password\": \"{config.password}\"")

    result = api.login(config.username, config.password)

    print("\n[Step 2] 验证响应")

    # 验证 HTTP 状态码
    if result.get("status_code") == 200:
        print("[PASS] HTTP 状态码: 200")
    else:
        print(f"[FAIL] HTTP 状态码: {result.get('status_code')}")
        return False

    # 验证返回数据
    if result.get("token"):
        print("[PASS] 返回包含 token")
        print(f"  Token: {result['token'][:40]}...")
        print(f"  有效期: {int(result['expLen']/1000)} 秒")
        print(f"  用户ID: {result['user']['id']}")
        print(f"  用户名: {result['user']['displayName']}")
        print(f"  角色: {result['user']['role']}")
        return True
    else:
        print("[FAIL] 返回缺少 token")
        print(f"  错误: {result.get('msg', result)}")
        return False


if __name__ == "__main__":
    test_login_ok()