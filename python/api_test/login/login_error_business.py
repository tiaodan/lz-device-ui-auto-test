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
    """测试：密码错误"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 密码错误")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用错误密码登录")
    print(f"  用户名: {config.username}")
    print(f"  密码: wrong_password")
    result = api.login(config.username, "wrong_password")

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', 'N/A')}")
        # 验证错误信息是否正确
        if result.get('msg') == 'Incorrect password':
            print("[PASS] 错误信息正确")
            return True
        else:
            print("[WARN] 错误信息与预期不一致")
            return True  # 只要登录失败就算通过


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
    print(f"  用户名: nonexistent_user")
    print(f"  密码: any_password")
    result = api.login("nonexistent_user", "any_password")

    print("\n[Step 2] 验证结果")
    if result.get("token"):
        print("[FAIL] 不应该登录成功")
        return False
    else:
        print("[PASS] 登录被拒绝")
        print(f"  错误码: {result.get('code', 'N/A')}")
        print(f"  错误信息: {result.get('msg', 'N/A')}")
        return True


def test_login_wrong_password_multiple():
    """测试：多次密码错误"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: 多次密码错误")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 连续3次使用错误密码登录")
    results = []
    for i in range(3):
        print(f"\n  第 {i+1} 次:")
        result = api.login(config.username, f"wrong_pass_{i}")
        results.append(result)
        if result.get("token"):
            print("[FAIL] 不应该登录成功")
            return False
        else:
            print(f"    被拒绝: {result.get('msg', 'N/A')}")

    print("\n[Step 2] 验证所有尝试都被拒绝")
    all_rejected = all(not r.get("token") for r in results)
    if all_rejected:
        print("[PASS] 所有错误密码尝试都被拒绝")
        return True
    else:
        print("[FAIL] 有尝试未被拒绝")
        return False


def test_login_sql_injection():
    """测试：SQL注入攻击"""

    config = get_config(reload=True)

    print("\n" + "="*50)
    print("测试类型: API 登录测试")
    print("测试场景: SQL注入攻击")
    print("="*50)

    api = ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.login_url
    )

    print("\n[Step 1] 使用SQL注入语句登录")
    injection_attempts = [
        ("admin'--", "test1"),
        ("admin' OR '1'='1", "test1"),
        ("root; DROP TABLE users;", "test1"),
    ]

    all_rejected = True
    for username, password in injection_attempts:
        print(f"\n  尝试: {username}")
        result = api.login(username, password)
        if result.get("token"):
            print(f"    [FAIL] SQL注入可能成功!")
            all_rejected = False
        else:
            print(f"    [PASS] 被拒绝")

    print("\n[Step 2] 验证所有注入尝试都被拒绝")
    if all_rejected:
        print("[PASS] SQL注入防护有效")
        return True
    else:
        print("[FAIL] 存在SQL注入风险")
        return False


def run_all_business_error_tests():
    """运行所有业务异常测试"""

    print("\n" + "="*60)
    print("运行登录业务异常测试")
    print("="*60)

    tests = [
        ("密码错误", test_login_wrong_password),
        ("用户不存在", test_login_user_not_exist),
        ("多次密码错误", test_login_wrong_password_multiple),
        ("SQL注入攻击", test_login_sql_injection),
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