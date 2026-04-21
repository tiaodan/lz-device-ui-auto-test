"""
滑块拖动演示 - 观察效果
"""

from playwright.sync_api import sync_playwright
from config.config_loader import get_config
from pages.login_page import LoginPage


def demo_slider():
    """演示滑块拖动（慢速，方便观察）"""

    config = get_config()

    with sync_playwright() as p:
        # 有头模式，慢速操作
        browser = p.chromium.launch(
            headless=False,
            slow_mo=1000  # 每步延迟1秒
        )
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        login_page = LoginPage(page)

        print("\n=== 滑块拖动演示 ===")
        print("请观察浏览器窗口中的滑块变化")

        # 打开页面
        print("\n[1] 打开登录页面...")
        page.goto(config.base_url, wait_until="networkidle")
        page.wait_for_timeout(2000)

        # 显示初始状态
        print("\n[2] 滑块初始状态")
        progress = login_page.get_slider_progress()
        print(f"  进度: {progress}")
        print("  请观察滑块位置（应该在最左边）")

        page.wait_for_timeout(3000)  # 等待3秒让你观察

        # 拖动滑块
        print("\n[3] 拖动滑块...")
        print("  请观察滑块向右移动")
        login_page.drag_slider()

        # 显示最终状态
        print("\n[4] 滑块最终状态")
        progress = login_page.get_slider_progress()
        print(f"  进度: {progress}")
        print("  滑块应该在右边，显示解锁状态")

        page.wait_for_timeout(5000)  # 等待5秒让你观察

        # 截图
        page.screenshot(path="screenshots/demo_slider.png")
        print(f"\n[5] 截图保存: screenshots/demo_slider.png")

        print("\n演示完成，浏览器将保持打开...")
        print("按 Ctrl+C 关闭")

        try:
            page.wait_for_timeout(60000)
        except KeyboardInterrupt:
            pass

        browser.close()


if __name__ == "__main__":
    demo_slider()