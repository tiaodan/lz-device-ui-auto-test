"""
统一测试运行入口
根据配置文件选择测试类型运行
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from config.config_loader import get_config


def run_tests():
    """根据配置运行测试"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*60)
    print("无人机防御系统自动化测试")
    print("="*60)
    print(f"测试环境: {config.base_url}")
    print(f"API 地址: {config.graphql_url}")
    print(f"测试类型: {config.test_types}")
    print("="*60)

    # 按配置的测试类型运行
    results = {}

    # 1. 断言测试
    if config.is_test_type_enabled("assertion"):
        print("\n>>> 运行断言测试 (Assertion)")
        try:
            from assertion_test.test_login import (
                test_login_page_elements,
                test_login_slider_progress,
                test_login_form_fill
            )

            assertion_results = []

            # 测试页面元素
            print("\n--- 测试: 页面元素验证 ---")
            try:
                test_login_page_elements()
                assertion_results.append(("页面元素", True))
            except Exception as e:
                print(f"失败: {e}")
                assertion_results.append(("页面元素", False))

            # 测试滑块进度
            print("\n--- 测试: 滑块进度验证 ---")
            try:
                test_login_slider_progress()
                assertion_results.append(("滑块进度", True))
            except Exception as e:
                print(f"失败: {e}")
                assertion_results.append(("滑块进度", False))

            # 测试表单填写
            print("\n--- 测试: 表单填写验证 ---")
            try:
                test_login_form_fill()
                assertion_results.append(("表单填写", True))
            except Exception as e:
                print(f"失败: {e}")
                assertion_results.append(("表单填写", False))

            results["assertion"] = assertion_results

        except Exception as e:
            print(f"断言测试加载失败: {e}")
            results["assertion"] = []

    # 2. 图片识别测试
    if config.is_test_type_enabled("visual"):
        print("\n>>> 运行图片识别测试 (Visual)")
        try:
            from visual_test.test_login import (
                test_login_page_visual,
                test_login_slider_visual,
                test_login_button_visual
            )

            visual_results = []

            # 测试页面视觉
            print("\n--- 测试: 页面视觉回归 ---")
            try:
                test_login_page_visual()
                visual_results.append(("页面视觉", True))
            except Exception as e:
                print(f"失败: {e}")
                visual_results.append(("页面视觉", False))

            # 测试滑块视觉
            print("\n--- 测试: 滑块视觉变化 ---")
            try:
                test_login_slider_visual()
                visual_results.append(("滑块视觉", True))
            except Exception as e:
                print(f"失败: {e}")
                visual_results.append(("滑块视觉", False))

            # 测试按钮视觉
            print("\n--- 测试: 按钮视觉 ---")
            try:
                test_login_button_visual()
                visual_results.append(("按钮视觉", True))
            except Exception as e:
                print(f"失败: {e}")
                visual_results.append(("按钮视觉", False))

            results["visual"] = visual_results

        except Exception as e:
            print(f"图片识别测试加载失败: {e}")
            results["visual"] = []

    # 3. 接口测试
    if config.is_test_type_enabled("api"):
        print("\n>>> 运行接口自动化测试 (API)")
        try:
            from api_test.login.login_ok import test_login_ok
            from api_test.login.login_error_business import run_all_business_error_tests

            api_results = []

            # 正常场景
            print("\n--- 测试: 登录正常场景 ---")
            try:
                result = test_login_ok()
                if result:
                    print("\n[PASS] 测试通过")
                else:
                    print("\n[FAIL] 测试失败")
                api_results.append(("登录-正常", result))
            except Exception as e:
                print(f"[ERROR] 失败: {e}")
                api_results.append(("登录-正常", False))

            # 异常业务
            print("\n--- 测试: 登录异常业务 ---")
            try:
                result = run_all_business_error_tests()
                api_results.append(("登录-异常业务", result))
            except Exception as e:
                print(f"[ERROR] 失败: {e}")
                api_results.append(("登录-异常业务", False))

            results["api"] = api_results

        except Exception as e:
            print(f"接口测试加载失败: {e}")
            results["api"] = []

    # 输出结果汇总
    print("\n" + "="*60)
    print("测试结果汇总")
    print("="*60)

    total_passed = 0
    total_failed = 0

    for test_type, test_results in results.items():
        print(f"\n{test_type.upper()} 测试:")
        passed = sum(1 for _, r in test_results if r)
        failed = sum(1 for _, r in test_results if not r)
        total_passed += passed
        total_failed += failed

        for name, result in test_results:
            status = "[PASS]" if result else "[FAIL]"
            print(f"  {status} {name}")

        print(f"  通过: {passed}, 失败: {failed}")

    print("\n" + "-"*60)
    print(f"总计: 通过 {total_passed}, 失败 {total_failed}")
    print("="*60)


def run_single_test(test_type: str, test_name: str):
    """运行单个测试"""

    config = get_config(reload=True)
    config.ensure_directories()

    print(f"\n运行测试: {test_type}/{test_name}")

    if test_type == "assertion":
        from assertion_test.test_login import (
            test_login_page_elements,
            test_login_slider_progress,
            test_login_form_fill
        )
        tests = {
            "elements": test_login_page_elements,
            "slider": test_login_slider_progress,
            "form": test_login_form_fill
        }
        if test_name in tests:
            tests[test_name]()
        else:
            print(f"未知的 assertion 测试: {test_name}")

    elif test_type == "visual":
        from visual_test.test_login import (
            test_login_page_visual,
            test_login_slider_visual,
            test_login_button_visual,
            create_all_baselines
        )
        tests = {
            "page": test_login_page_visual,
            "slider": test_login_slider_visual,
            "button": test_login_button_visual,
            "baseline": create_all_baselines
        }
        if test_name in tests:
            tests[test_name]()
        else:
            print(f"未知的 visual 测试: {test_name}")

    elif test_type == "api":
        # API 测试 - login 模块
        if test_name == "login_ok":
            from api_test.login.login_ok import test_login_ok
            result = test_login_ok()
            if result:
                print("\n[PASS] 测试通过")
            else:
                print("\n[FAIL] 测试失败")
        elif test_name == "login_error_business":
            from api_test.login.login_error_business import run_all_business_error_tests
            result = run_all_business_error_tests()
            if result:
                print("\n[PASS] 所有异常业务测试通过")
            else:
                print("\n[FAIL] 部分异常业务测试失败")
        elif test_name == "login":
            # 运行所有 login 测试
            from api_test.login.login_ok import test_login_ok
            from api_test.login.login_error_business import run_all_business_error_tests
            print("\n>>> 运行所有 login 测试")
            print("\n--- 正常场景 ---")
            test_login_ok()
            print("\n--- 异常业务 ---")
            run_all_business_error_tests()
        else:
            print(f"未知的 API 测试: {test_name}")
            print("可用测试: login, login_ok, login_error_business")

    else:
        print(f"未知测试类型: {test_type}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) == 1:
        # 无参数，运行所有配置的测试
        run_tests()

    elif len(sys.argv) == 2:
        # 一个参数，运行指定类型的所有测试
        test_type = sys.argv[1]
        if test_type == "api":
            run_single_test(test_type, "login")
        elif test_type in ["assertion", "visual"]:
            run_single_test(test_type, "all")
        else:
            print(f"未知测试类型: {test_type}")

    elif len(sys.argv) >= 3:
        # 两个参数，运行指定测试
        test_type = sys.argv[1]
        test_name = sys.argv[2]
        run_single_test(test_type, test_name)