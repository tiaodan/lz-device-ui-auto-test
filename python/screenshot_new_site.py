"""
简单截图查看新网站
"""

from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch(headless=True)
    context = browser.new_context(ignore_https_errors=True)
    page = context.new_page()

    print("\n访问新网站...")

    page.goto("https://192.168.85.239", timeout=30000)
    page.wait_for_timeout(2000)

    print(f"页面标题: {page.title()}")

    # 截图
    page.screenshot(path="screenshots/new_site_239.png", full_page=True)
    print("截图保存: screenshots/new_site_239.png")

    # 获取HTML
    html = page.content()
    with open("screenshots/new_site_239.html", "w", encoding="utf-8") as f:
        f.write(html)
    print("HTML保存: screenshots/new_site_239.html")

    browser.close()