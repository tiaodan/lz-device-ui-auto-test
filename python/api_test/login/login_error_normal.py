"""
登录功能 - 异常通用测试
测试参数缺失、格式错误等通用异常场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.config_loader import get_config
from api_test.base import ApiTest


def test_login_empty_username():
    """测试：用户名为空"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 用户名为空")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用空用户名登录")
    result = api.login("", config.password)

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误信息: {result.get('msg', result.get('code', '未知错误'))}")
        return True


def test_login_empty_password():
    """测试：密码为空"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 密码为空")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用空密码登录")
    result = api.login(config.username, "")

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误信息: {result.get('msg', result.get('code', '未知错误'))}")
        return True


def test_login_empty_both():
    """测试：用户名和密码都为空"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 用户名和密码都为空")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用空用户名和空密码登录")
    result = api.login("", "")

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误信息: {result.get('msg', result.get('code', '未知错误'))}")
        return True


def test_login_special_characters():
    """测试：用户名包含特殊字符"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 用户名包含特殊字符")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用特殊字符用户名登录")
    special_username = "root@#$%"
    result = api.login(special_username, config.password)

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误信息: {result.get('msg', result.get('code', '未知错误'))}")
        return True


def test_login_long_username():
    """测试：超长用户名"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 超长用户名")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用超长用户名登录")
    long_username = "a" * 1000
    result = api.login(long_username, config.password)

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误信息: {result.get('msg', result.get('code', '未知错误'))}")
        return True


def run_all_normal_error_tests():
    """运行所有通用异常测试"""

    print("\n" + "="*60)
    print("运行登录通用异常测试")
    print("="*60)

    tests = [
        ("用户名为空", test_login_empty_username),
        ("密码为空", test_login_empty_password),
        ("用户名密码都为空", test_login_empty_both),
        ("特殊字符用户名", test_login_special_characters),
        ("超长用户名", test_login_long_username),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            results.append((name, False))

    # 汇总
    print("\n" + "-"*60)
    print("测试结果汇总")
    print("-"*60)
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {name}")

    passed_count = sum(1 for _, p in results if p)
    print(f"\n通过: {passed_count}/{len(results)}")


if __name__ == "__main__":
    run_all_normal_error_tests()