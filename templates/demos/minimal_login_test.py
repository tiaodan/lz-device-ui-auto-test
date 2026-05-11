"""
最小登录测试示例
完整可运行的示例，用于学习和调试
"""

from playwright.sync_api import sync_playwright, expect


def test_login_minimal():
    """最小登录测试示例"""

    with sync_playwright() as p:
        # 启动浏览器
        browser = p.chromium.launch(headless=False, slow_mo=100)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # 导航到登录页
        page.goto("https://192.168.1.100", wait_until="networkidle")

        # 填写用户名密码
        page.locator(".username-input").fill("root")
        page.locator(".password-input").fill("password")

        # 处理滑块（如果需要）
        # slider_handler = SliderHandler(page)
        # slider_handler.drag_slider()

        # 点击登录
        page.locator(".login-button").click()
        page.wait_for_timeout(3000)

        # 验证登录成功
        expect(page).to_have_url("https://192.168.1.100/home")

        # 截图
        page.screenshot(path="login_success.png")

        # 关闭
        context.close()
        browser.close()


if __name__ == "__main__":
    test_login_minimal()