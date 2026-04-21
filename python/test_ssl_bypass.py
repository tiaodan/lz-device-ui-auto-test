"""
验证 SSL 证书警告是否自动跳过
"""

from playwright.sync_api import sync_playwright

print("\n=== SSL 证书警告自动跳过测试 ===\n")

with sync_playwright() as p:
    # 启动浏览器
    browser = p.chromium.launch(headless=False)  # 有头模式，可以看到效果

    # 关键：在 new_context 中设置 ignore_https_errors=True
    context = browser.new_context(ignore_https_errors=True)

    page = context.new_page()

    print("访问: https://192.168.85.239")
    print("如果 SSL 问题已解决，应该直接显示登录页面，不出现证书警告")

    # 直接访问
    page.goto("https://192.168.85.239", timeout=30000)
    page.wait_for_timeout(3000)

    print(f"\n页面标题: {page.title()}")

    # 检查是否有登录元素（证明已跳过SSL警告）
    username_count = page.locator("#username").count()

    if username_count > 0:
        print("\n[SUCCESS] SSL 证书警告已自动跳过！")
        print("[SUCCESS] 直接显示登录页面，找到用户名输入框")
    else:
        print("\n[FAILED] 仍在证书警告页面")
        print("[FAILED] 未找到登录元素")

    # 截图
    page.screenshot(path="screenshots/ssl_test_result.png")
    print("\n截图保存: screenshots/ssl_test_result.png")

    print("\n浏览器保持打开，请确认是否跳过了证书警告...")
    print("按 Ctrl+C 关闭")

    try:
        page.wait_for_timeout(30000)
    except KeyboardInterrupt:
        pass

    browser.close()