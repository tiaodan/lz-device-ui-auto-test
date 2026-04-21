"""
浏览器启动辅助模块
统一处理 SSL 证书等配置
"""

from playwright.sync_api import sync_playwright, Browser, BrowserContext, Page
from config.config_loader import get_config


def create_browser(playwright_instance, config=None) -> Browser:
    """
    创建浏览器实例

    Args:
        playwright_instance: Playwright 实例
        config: 配置对象（可选，默认读取全局配置）

    Returns:
        Browser: 浏览器实例
    """
    if config is None:
        config = get_config()

    browser_type = config.browser_type
    headless = config.headless
    slow_mo = config.slow_mo

    # 启动浏览器（不在这里处理 SSL，应在 context 中处理）
    launch_options = {
        "headless": headless,
    }

    if slow_mo > 0:
        launch_options["slow_mo"] = slow_mo

    if browser_type == "chromium":
        return playwright_instance.chromium.launch(**launch_options)
    elif browser_type == "firefox":
        return playwright_instance.firefox.launch(**launch_options)
    elif browser_type == "webkit":
        return playwright_instance.webkit.launch(**launch_options)
    else:
        return playwright_instance.chromium.launch(**launch_options)


def create_context(browser: Browser, config=None) -> BrowserContext:
    """
    创建浏览器上下文，自动处理 SSL 等配置

    Args:
        browser: 浏览器实例
        config: 配置对象（可选）

    Returns:
        BrowserContext: 浏览器上下文
    """
    if config is None:
        config = get_config()

    return browser.new_context(
        ignore_https_errors=True  # 再次确认忽略 SSL
    )


def create_page(browser: Browser, config=None) -> Page:
    """
    创建页面，完整处理 SSL 配置

    Args:
        browser: 浏览器实例
        config: 配置对象（可选）

    Returns:
        Page: 页面实例
    """
    context = create_context(browser, config)
    return context.new_page()


def setup_test_environment(playwright_instance, config=None) -> tuple:
    """
    一键创建完整测试环境

    Args:
        playwright_instance: Playwright 实例
        config: 配置对象（可选）

    Returns:
        tuple: (browser, context, page)
    """
    if config is None:
        config = get_config()

    browser = create_browser(playwright_instance, config)
    context = create_context(browser, config)
    page = context.new_page()

    return browser, context, page


# 使用示例
if __name__ == "__main__":
    with sync_playwright() as p:
        browser, context, page = setup_test_environment(p)

        config = get_config()
        print(f"访问: {config.base_url}")

        page.goto(config.base_url)
        page.wait_for_timeout(2000)

        print("页面标题:", page.title())

        browser.close()
        print("测试环境创建成功！SSL 证书警告已自动处理。")