"""
分析登录页面结构
运行: python analyze_login_page.py
"""

from playwright.sync_api import sync_playwright
import os


def analyze_login_page():
    """访问登录页面并截图分析"""

    screenshots_dir = "screenshots"
    os.makedirs(screenshots_dir, exist_ok=True)

    with sync_playwright() as p:
        # 启动浏览器（忽略 SSL 证书错误）
        browser = p.chromium.launch(headless=True)  # 无头模式
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # 访问登录页
        print("正在访问登录页面...")
        page.goto("https://192.168.85.238/login", wait_until="networkidle", timeout=30000)

        # 等待页面加载
        page.wait_for_timeout(2000)

        # 截图
        screenshot_path = f"{screenshots_dir}/login_page.png"
        page.screenshot(path=screenshot_path, full_page=True)
        print(f"截图保存: {screenshot_path}")

        # 获取页面 HTML 结构
        html = page.content()
        html_path = f"{screenshots_dir}/login_page.html"
        with open(html_path, "w", encoding="utf-8") as f:
            f.write(html)
        print(f"HTML保存: {html_path}")

        # 分析页面元素
        print("\n=== 页面元素分析 ===")

        # 查找输入框
        inputs = page.locator("input").all()
        print(f"\n输入框数量: {len(inputs)}")
        for i, input_el in enumerate(inputs):
            try:
                tag = input_el.evaluate("el => el.tagName")
                type_attr = input_el.evaluate("el => el.type") or ""
                name_attr = input_el.evaluate("el => el.name") or ""
                placeholder = input_el.evaluate("el => el.placeholder") or ""
                class_name = input_el.evaluate("el => el.className") or ""
                print(f"  [{i+1}] type={type_attr}, name={name_attr}, placeholder='{placeholder}', class={class_name}")
            except:
                pass

        # 查找按钮
        buttons = page.locator("button").all()
        print(f"\n按钮数量: {len(buttons)}")
        for i, btn in enumerate(buttons):
            try:
                text = btn.inner_text()
                class_name = btn.evaluate("el => el.className") or ""
                print(f"  [{i+1}] 文本='{text}', class={class_name}")
            except:
                pass

        # 查找滑块/拖动元素
        print("\n查找滑块元素...")
        slider_candidates = [
            "div[class*='slider']",
            "div[class*='drag']",
            "div[class*='verify']",
            "div[class*='captcha']",
            "span[class*='slider']",
            "div[role='slider']",
        ]

        for selector in slider_candidates:
            elements = page.locator(selector).all()
            if elements:
                print(f"  找到 {len(elements)} 个: {selector}")
                for el in elements:
                    try:
                        class_name = el.evaluate("el => el.className") or ""
                        print(f"    class={class_name}")
                    except:
                        pass

        # 查找图片元素（可能是拼图验证码背景图）
        images = page.locator("img").all()
        print(f"\n图片数量: {len(images)}")
        for i, img in enumerate(images):
            try:
                src = img.evaluate("el => el.src") or ""
                alt = img.evaluate("el => el.alt") or ""
                print(f"  [{i+1}] src='{src}', alt='{alt}'")
            except:
                pass

        # 获取页面标题
        title = page.title()
        print(f"\n页面标题: {title}")

        # 检测技术栈
        print("\n=== 技术栈检测 ===")

        # 检查是否使用 Vue
        vue = page.evaluate("() => !!window.Vue || !!window.__VUE__")
        print(f"Vue: {vue}")

        # 检查是否使用 React
        react = page.evaluate("() => !!window.React || !!document.querySelector('[data-reactroot]')")
        print(f"React: {react}")

        # 检查是否有常见滑块验证码库
        captcha_libs = [
            "window.slideVerify",
            "window.sliderCaptcha",
            "window.captcha",
            "window.geetest",
            "window.aliyunCaptcha",
        ]
        for lib in captcha_libs:
            exists = page.evaluate(f"() => !!{lib}")
            if exists:
                print(f"验证码库: {lib}")

        # 直接关闭浏览器
        browser.close()


if __name__ == "__main__":
    analyze_login_page()