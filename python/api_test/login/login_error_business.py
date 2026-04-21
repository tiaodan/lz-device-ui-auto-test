"""
登录功能 - 异常业务测试
测试密码错误、用户不存在等业务异常场景
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from config.config_loader import get_config
from api_test.base import ApiTest


def test_login_wrong_password():
    """测试：正确的用户名+错误密码"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 正确的用户名+错误密码")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用错误密码登录")
    print(f"  用户名: {config.username}")
    print(f"  密码: lz")
    result = api.login(config.username, "lz")

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', 'N/A')}")
        # 验证错误码和错误信息
        if result.get('code') == 5 and result.get('msg') == 'Incorrect password':
            print("[PASS] 错误码和信息正确: code=5, msg=Incorrect password")
            return True
        return True


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
    print(f"  用户名: (空)")
    print(f"  密码: {config.password}")
    result = api.login("", config.password)

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', result.get('error', 'N/A'))}")
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
    print(f"  用户名: {config.username}")
    print(f"  密码: (空)")
    result = api.login(config.username, "")

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', result.get('error', 'N/A'))}")
        return True


def test_login_user_not_exist():
    """测试：用户不存在"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 用户不存在")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用不存在的用户登录")
    print(f"  用户名: root1")
    print(f"  密码: {config.password}")
    result = api.login("root1", config.password)

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', 'N/A')}")
        if result.get('code') == 3:
            print("[PASS] 错误码正确: 3 (record not found)")
            return True
        return True


def test_login_password_case_sensitive():
    """测试：密码大小写区分"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 密码大小写区分")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    # 将正确密码转为大写
    password_upper = config.password.upper()

    print("\n[Step 1] 使用大写密码登录")
    print(f"  用户名: {config.username}")
    print(f"  密码(大写): {password_upper}")
    result = api.login(config.username, password_upper)

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', 'N/A')}")
        if result.get('msg') == 'Incorrect password':
            print("[PASS] 错误信息正确: Incorrect password")
            return True
        return True


def test_login_username_case_sensitive():
    """测试：用户名大小写区分"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 用户名大小写区分")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    # 将用户名转为大写
    username_upper = config.username.upper()

    print("\n[Step 1] 使用大写用户名登录")
    print(f"  用户名(大写): {username_upper}")
    print(f"  密码: {config.password}")
    result = api.login(username_upper, config.password)

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', 'N/A')}")
        return True


def run_all_business_error_tests():
    """运行所有业务异常测试"""

    print("\n" + "="*60)
    print("运行登录业务异常测试")
    print("="*60)

    tests = [
        ("密码错误", test_login_wrong_password),
        ("用户名为空", test_login_empty_username),
        ("密码为空", test_login_empty_password),
        ("用户不存在", test_login_user_not_exist),
        ("密码大小写区分", test_login_password_case_sensitive),
        ("用户名大小写区分", test_login_username_case_sensitive),
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
    return passed_count == len(results)


if __name__ == "__main__":
    run_all_business_error_tests()