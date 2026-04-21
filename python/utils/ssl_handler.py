"""
SSL 证书警告页面自动处理
"""

from playwright.sync_api import Page
import time


def handle_ssl_warning(page: Page) -> bool:
    """
    自动处理 SSL 证书警告页面

    检测并点击"继续前往（不安全）"按钮

    Args:
        page: Playwright 页面对象

    Returns:
        bool: 是否处理了证书警告
    """

    # 等待页面加载
    page.wait_for_timeout(500)

    # 检测是否在证书警告页面
    # Chromium 的证书警告页面特征：
    # - 标题包含 "Privacy error" 或 "Certificate" 或 "安全"
    # - 有 "继续前往" 或 "Proceed" 按钮

    try:
        # 检查页面内容
        page_content = page.content()

        # 如果是证书警告页面
        if any(keyword in page_content.lower() for keyword in [
            "privacy error",
            "certificate",
            "您的连接不是私密连接",
            "not private",
            "安全证书"
        ]):
            print("[SSL] 检测到证书警告页面，尝试自动处理...")

            # 尝试多种方式点击"继续前往"按钮

            # 方法1: 点击链接或按钮
            selectors = [
                "#proceed-link",  # Firefox
                "button#details-button",  # Chrome 详细信息按钮
                "#details-button",
                "a[href='#']",  # 可能的链接
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
                        print(f"[SSL] 点击 '{selector}' 成功")
                        page.wait_for_timeout(1000)
                        return True
                except:
                    continue

            # 方法2: 使用键盘快捷键（某些浏览器）
            # Chrome: 无快捷键
            # Firefox: 无快捷键

            print("[SSL] 无法自动处理证书警告，请手动点击")
            return False

        return False  # 不在证书警告页面

    except Exception as e:
        print(f"[SSL] 处理异常: {e}")
        return False


def safe_navigate(page: Page, url: str, wait_for: str = "networkidle") -> bool:
    """
    安全导航，自动处理 SSL 证书警告

    Args:
        page: 页面对象
        url: 目标 URL
        wait_for: 等待条件

    Returns:
        bool: 是否成功到达目标页面
    """

    print(f"[NAV] 导航到: {url}")

    try:
        page.goto(url, wait_until="load", timeout=30000)
        page.wait_for_timeout(1000)

        # 检查并处理证书警告
        if handle_ssl_warning(page):
            # 处理成功后，等待页面真正加载
            page.wait_for_timeout(2000)
            print("[SSL] 证书警告已处理，页面正常加载")

        # 等待网络空闲
        try:
            page.wait_for_load_state(wait_for, timeout=10000)
        except:
            pass  # 某些页面可能不会达到 networkidle

        return True

    except Exception as e:
        print(f"[NAV] 导航失败: {e}")
        return False


if __name__ == "__main__":
    from playwright.sync_api import sync_playwright

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 有头模式测试
        context = browser.new_context()
        page = context.new_page()

        print("\n=== SSL 证书警告自动处理测试 ===\n")

        # 测试导航（会触发证书警告）
        url = "https://192.168.85.239"
        success = safe_navigate(page, url)

        if success:
            print(f"\n[成功] 页面标题: {page.title()}")
            page.screenshot(path="screenshots/ssl_handled.png")
            print("[截图] screenshots/ssl_handled.png")

        print("\n按 Ctrl+C 关闭...")
        try:
            page.wait_for_timeout(60000)
        except KeyboardInterrupt:
            pass

        browser.close()