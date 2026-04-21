"""
深入分析登录页面和系统结构
"""

from playwright.sync_api import sync_playwright
import os


def analyze_system():
    """分析系统结构"""

    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    urls_to_try = [
        "https://192.168.85.238/",
        "https://192.168.85.238/login",
        "https://192.168.85.238/index.html",
        "https://192.168.85.238/index",
        "http://192.168.85.238/",  # 尝试HTTP
        "http://192.168.85.238/login",
    ]

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)

        for url in urls_to_try:
            print(f"\n=== 尝试访问: {url} ===")
            page = context.new_page()

            try:
                page.goto(url, wait_until="networkidle", timeout=15000)
                page.wait_for_timeout(1000)

                # 获取响应内容
                content = page.content()
                title = page.title()

                print(f"页面标题: {title}")

                # 截图
                safe_name = url.replace("://", "_").replace("/", "_").replace(".", "_")
                screenshot_path = f"{screenshots_dir}/{safe_name}.png"
                page.screenshot(path=screenshot_path)
                print(f"截图: {screenshot_path}")

                # 保存HTML（只保存前500字符作为预览）
                html_preview = content[:500] if len(content) > 500 else content
                print(f"HTML预览: {html_preview}")

                # 如果页面有内容，详细分析
                if len(content) > 200 and "<pre>" not in content:
                    print("\n分析页面元素:")
                    inputs = page.locator("input").all()
                    print(f"  输入框: {len(inputs)}")

                    buttons = page.locator("button").all()
                    print(f"  按钮: {len(buttons)}")

                    divs = page.locator("div").all()
                    print(f"  DIV: {len(divs)}")

            except Exception as e:
                print(f"访问失败: {e}")

            page.close()

        browser.close()


if __name__ == "__main__":
    analyze_system()