"""
SSL 证书警告页面自动处理
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import Page
from loguru import logger


def handle_ssl_warning(page: Page) -> bool:
    """自动处理 SSL 证书警告页面"""

    page.wait_for_timeout(500)

    try:
        page_content = page.content()

        if any(keyword in page_content.lower() for keyword in [
            "privacy error",
            "certificate",
            "您的连接不是私密连接",
            "not private",
            "安全证书"
        ]):
            logger.warning("检测到证书警告页面，尝试自动处理...")

            selectors = [
                "#proceed-link",
                "button#details-button",
                "#details-button",
                "a[href='#']",
                "button:has-text('继续前往')",
                "button:has-text('Proceed')",
                "a:has-text('继续前往')",
                "a:has-text('Proceed')",
                "#warning-button",
                "button[type='button']",
            ]

            for selector in selectors:
                try:
                    if page.locator(selector).count() > 0:
                        page.locator(selector).click()
                        logger.success(f"点击 '{selector}' 成功")
                        page.wait_for_timeout(1000)
                        return True
                except:
                    continue

            logger.error("无法自动处理证书警告，请手动点击")
            return False

        return False

    except Exception as e:
        logger.error(f"处理异常: {e}")
        return False


def safe_navigate(page: Page, url: str, wait_for: str = "networkidle") -> bool:
    """安全导航，自动处理 SSL 证书警告"""

    logger.info(f"导航到: {url}")

    try:
        page.goto(url, wait_until="load", timeout=30000)
        page.wait_for_timeout(1000)

        if handle_ssl_warning(page):
            page.wait_for_timeout(2000)
            logger.success("证书警告已处理，页面正常加载")

        try:
            page.wait_for_load_state(wait_for, timeout=10000)
        except:
            pass

        return True

    except Exception as e:
        logger.error(f"导航失败: {e}")
        return False


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        logger.info("SSL 证书警告自动处理测试")

        url = "https://192.168.85.239"
        success = safe_navigate(page, url)

        if success:
            logger.success(f"页面标题: {page.title()}")
            page.screenshot(path="screenshots/ssl_handled.png")
            logger.info("截图: screenshots/ssl_handled.png")

        logger.info("按 Ctrl+C 关闭...")
        try:
            page.wait_for_timeout(60000)
        except KeyboardInterrupt:
            pass

        browser.close()