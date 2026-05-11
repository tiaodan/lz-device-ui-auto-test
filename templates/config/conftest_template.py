"""
pytest + playwright 全局配置模板
提供 fixtures、hooks 和配置
复制后修改：定位器、测试数据、路径
"""

import pytest
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from config.config_loader import get_config, Config
from pages.page_template import PageTemplate


# ==================== 存储状态文件 ====================

STORAGE_STATE_FILE = "auth_state.json"


# ==================== 配置 fixtures ====================

@pytest.fixture(scope="session")
def config():
    """配置 fixture (session 级别，只加载一次)"""
    cfg = get_config(reload=True)
    cfg.ensure_directories()
    return cfg


@pytest.fixture(scope="session")
def language(config):
    """当前测试语言"""
    return getattr(config, 'language', 'zh_CN')


# ==================== 浏览器配置 fixtures ====================

@pytest.fixture(scope="session")
def browser_context_args(config):
    """浏览器上下文参数"""
    return {
        "ignore_https_errors": config.ignore_ssl_errors,
    }


@pytest.fixture(scope="session")
def browser_type_launcher_args(config):
    """浏览器启动参数"""
    args = {"headless": config.headless}
    if config.slow_mo > 0:
        args["slow_mo"] = config.slow_mo
    return args


# ==================== 登录状态 fixtures ====================

@pytest.fixture(scope="session")
def saved_auth_state(launch_browser, browser_context_args, config, language):
    """Session 级别：登录并保存状态"""
    # 如果已有有效状态文件，直接返回
    if os.path.exists(STORAGE_STATE_FILE):
        import json
        with open(STORAGE_STATE_FILE, "r") as f:
            state = json.load(f)
            if state.get("cookies") or state.get("origins"):
                return STORAGE_STATE_FILE

    # 登录流程
    browser = launch_browser()
    context = browser.new_context(**browser_context_args)
    context.add_init_script(f"localStorage.setItem('locale', '{language}');")
    page = context.new_page()

    # 执行登录（根据实际页面修改）
    page.goto(config.base_url)
    # ... 登录操作 ...

    context.storage_state(path=STORAGE_STATE_FILE)
    context.close()
    browser.close()

    return STORAGE_STATE_FILE


# ==================== 页面 fixtures ====================

@pytest.fixture
def fresh_page(browser, config, language):
    """全新页面（不加载登录状态，用于登录测试）"""
    context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
    context.add_init_script(f"localStorage.setItem('locale', '{language}');")
    page = context.new_page()
    page.goto(config.base_url, wait_until="networkidle")
    yield page
    context.close()


@pytest.fixture
def page(browser, config, saved_auth_state, language):
    """已登录页面（加载保存的登录状态）"""
    context = browser.new_context(
        ignore_https_errors=config.ignore_ssl_errors,
        storage_state=saved_auth_state
    )
    context.add_init_script(f"localStorage.setItem('locale', '{language}');")
    page = context.new_page()
    page.goto(config.base_url)
    yield page
    context.close()


@pytest.fixture
def page_obj(fresh_page, language):
    """页面对象 fixture（未登录）"""
    return PageTemplate(fresh_page, language=language)


@pytest.fixture
def page_obj_logged(page, language):
    """页面对象 fixture（已登录）"""
    return PageTemplate(page, language=language)


# ==================== pytest hooks ====================

def pytest_configure(config):
    """pytest 配置钩子"""
    config.addinivalue_line("markers", "slow: Slow running tests")
    config.addinivalue_line("markers", "login: Login related tests")


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
                page.screenshot(path=f"{screenshot_dir}/{item.name}_failure.png")
        except Exception as e:
            print(f"截图失败: {e}")