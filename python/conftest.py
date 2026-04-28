"""
pytest 全局配置
提供 fixtures、hooks 和配置
"""

import pytest
import os
import sys
import json
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import get_config, Config
from config.module_config_loader import get_module_config, get_expectations
from pages.login_page import LoginPage
from utils.test_logger import TestLogger, init_default_logger

# 登录状态文件路径
STORAGE_STATE_FILE = "auth_state.json"


@pytest.fixture(scope="session")
def config():
    """配置 fixture (session 级别)"""
    cfg = get_config(reload=True)
    cfg.ensure_directories()
    return cfg


@pytest.fixture(scope="session")
def test_logger(config):
    """测试日志器 fixture (session 级别)"""
    return init_default_logger(log_dir=config.log_path, level=config.log_level)


@pytest.fixture(scope="session")
def login_config():
    """登录模块配置 fixture"""
    return get_module_config("login")


@pytest.fixture(scope="session")
def language(config):
    """当前测试语言（从全局配置读取，格式：zh_CN, en_US 等）"""
    return getattr(config, 'language', 'zh_CN') if hasattr(config, 'language') else 'zh_CN'


@pytest.fixture(scope="session")
def browser_context_args(config):
    """扩展 browser_context_args"""
    return {
        "ignore_https_errors": config.ignore_ssl_errors,
    }


@pytest.fixture(scope="session")
def browser_type_launcher_args(config):
    """浏览器启动参数"""
    return {
        "headless": config.headless,
    }


@pytest.fixture(scope="session")
def saved_auth_state(launch_browser, browser_context_args, config, login_config, language):
    """Session 级别：使用 pytest-playwright 的 launcher 登录并保存状态"""
    # 如果已有有效状态文件，直接返回
    if os.path.exists(STORAGE_STATE_FILE):
        with open(STORAGE_STATE_FILE, "r", encoding="utf-8") as f:
            state = json.load(f)
            if state.get("cookies") or state.get("origins"):
                return STORAGE_STATE_FILE

    # 使用 pytest-playwright 的 launch_browser 创建浏览器
    browser = launch_browser()
    context_args = {**browser_context_args, "ignore_https_errors": config.ignore_ssl_errors}
    context = browser.new_context(**context_args)
    # 页面加载前注入语言设置（key 是 locale，不是 language）
    context.add_init_script(f"""
        localStorage.setItem('locale', '{language}');
        sessionStorage.setItem('locale', '{language}');
        Object.defineProperty(document, 'lanType', {{ value: '{language}', writable: true }});
    """)
    page = context.new_page()

    page.goto(config.base_url, wait_until="load")
    page.wait_for_timeout(1000)

    login_page = LoginPage(page)
    test_data = login_config["test_data"]["valid"]
    login_page.fill_credentials(test_data["username"], test_data["password"])
    login_page.drag_slider()
    login_page.click_login()
    page.wait_for_timeout(3000)

    context.storage_state(path=STORAGE_STATE_FILE)
    context.close()
    browser.close()

    return STORAGE_STATE_FILE


@pytest.fixture
def fresh_page(browser, config, test_logger, language):
    """全新页面（用于登录测试）- 不加载任何存储状态"""
    context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
    # 页面加载前注入语言设置
    context.add_init_script(f"""
        localStorage.setItem('locale', '{language}');
        sessionStorage.setItem('locale', '{language}');
        Object.defineProperty(document, 'lanType', {{ value: '{language}', writable: true }});
    """)
    page = context.new_page()
    page.goto(config.base_url, wait_until="load")
    page.wait_for_timeout(1000)
    yield page
    context.close()


@pytest.fixture
def page(browser, config, test_logger, saved_auth_state, language):
    """已登录页面 - 加载保存的登录状态"""
    context = browser.new_context(
        ignore_https_errors=config.ignore_ssl_errors,
        storage_state=saved_auth_state
    )
    # 页面加载前注入语言设置
    context.add_init_script(f"""
        localStorage.setItem('locale', '{language}');
        sessionStorage.setItem('locale', '{language}');
        Object.defineProperty(document, 'lanType', {{ value: '{language}', writable: true }});
    """)
    page = context.new_page()
    page.goto(config.base_url, wait_until="load")
    page.wait_for_timeout(1000)
    yield page
    context.close()


@pytest.fixture
def login_page(fresh_page, language):
    """登录页面对象 fixture（使用全新页面，用于登录测试）"""
    return LoginPage(fresh_page, language=language)


@pytest.fixture
def assertion_test(page, config):
    """断言测试 fixture"""
    from assertion_test.base import AssertionTest
    return AssertionTest(page, screenshot_path=config.assertion_screenshot_path)


@pytest.fixture
def visual_test(page, config):
    """视觉测试 fixture（已登录状态）"""
    from visual_test.base import VisualTest
    return VisualTest(
        page,
        baseline_path=config.baseline_path,
        current_path=config.current_path,
        diff_path=config.diff_path,
        threshold=config.visual_threshold
    )


@pytest.fixture
def visual_test_fresh(fresh_page, config):
    """视觉测试 fixture（未登录状态，用于登录页测试）"""
    from visual_test.base import VisualTest
    return VisualTest(
        fresh_page,
        baseline_path=config.baseline_path,
        current_path=config.current_path,
        diff_path=config.diff_path,
        threshold=config.visual_threshold
    )


@pytest.fixture
def api_test(config, test_logger):
    """API 测试 fixture"""
    from api_test.base import ApiTest
    return ApiTest(
        graphql_url=config.graphql_url,
        login_url=config.base_url,
        username=config.username,
        password=config.password
    )


# ==================== 清理钩子 ====================

def pytest_sessionfinish(session, exitstatus):
    """测试结束后清理登录状态文件（可选）"""
    # 如果需要每次重新登录，取消下面的注释
    # if os.path.exists(STORAGE_STATE_FILE):
    #     os.remove(STORAGE_STATE_FILE)
    pass


def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line("markers", "assertion: Assertion tests")
    config.addinivalue_line("markers", "visual: Visual tests")
    config.addinivalue_line("markers", "api: API tests")
    config.addinivalue_line("markers", "login: Login related tests")
    config.addinivalue_line("markers", "slow: Slow running tests")


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """失败时自动截图"""
    outcome = yield
    report = outcome.get_result()

    if report.when == "call" and report.failed:
        try:
            if "page" in item.fixturenames:
                page = item.funcargs["page"]
                screenshot_dir = "screenshots/failures"
                os.makedirs(screenshot_dir, exist_ok=True)
                screenshot_path = os.path.join(
                    screenshot_dir,
                    f"{item.name}_failure.png"
                )
                page.screenshot(path=screenshot_path)
        except Exception as e:
            print(f"截图失败: {e}")