"""
分析新网站 192.168.85.239 的页面结构
"""

from playwright.sync_api import sync_playwright
from config.config_loader import get_config


def analyze_new_site():
    """分析新网站的登录页面结构"""

    config = get_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 有头模式观察
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        print("\n" + "="*60)
        print(f"分析网站: {config.base_url}")
        print("="*60)

        # 访问页面
        print("\n[1] 访问页面...")
        page.goto(config.base_url, wait_until="load", timeout=30000)
        page.wait_for_timeout(3000)

        # 截图
        page.screenshot(path="screenshots/new_site.png", full_page=True)
        print(f"[截图] screenshots/new_site.png")

        # 获取页面标题
        print(f"\n[2] 页面标题: {page.title()}")

        # 分析输入框
        print("\n[3] 输入框:")
        inputs = page.locator("input").all()
        for i, inp in enumerate(inputs):
            try:
                info = inp.evaluate("""el => ({
                    type: el.type,
                    id: el.id,
                    name: el.name,
                    placeholder: el.placeholder,
                    className: el.className
                })""")
                print(f"  [{i+1}] {info}")
            except:
                pass

        # 分析按钮
        print("\n[4] 按钮:")
        buttons = page.locator("button").all()
        for i, btn in enumerate(buttons):
            try:
                info = btn.evaluate("""el => ({
                    text: el.innerText,
                    type: el.type,
                    className: el.className
                })""")
                print(f"  [{i+1}] {info}")
            except:
                pass

        # 查找滑块相关元素
        print("\n[5] 滑块相关元素:")
        slider_keywords = ["slider", "drag", "verify", "captcha", "slide", "progress"]
        for keyword in slider_keywords:
            elements = page.locator(f"[class*='{keyword}']").all()
            if elements:
                print(f"  关键词 '{keyword}' 找到 {len(elements)} 个")
                for j, el in enumerate(elements):
                    try:
                        info = el.evaluate("el => el.className")
                        print(f"    [{j+1}] {info}")
                    except:
                        pass

        # 查找表单
        print("\n[6] 表单:")
        forms = page.locator("form").all()
        for i, form in enumerate(forms):
            try:
                info = form.evaluate("""el => ({
                    className: el.className,
                    action: el.action
                })""")
                print(f"  [{i+1}] {info}")
            except:
                pass

        # 检查是否和之前一样
        print("\n[7] 检查之前的定位器是否有效:")
        old_selectors = {
            "username": "#username",
            "password": "#password",
            "slider": ".drag",
            "login_button": ".lBtn"
        }

        for name, selector in old_selectors.items():
            count = page.locator(selector).count()
            status = "存在" if count > 0 else "不存在"
            print(f"  {name} ({selector}): {status}")

        print("\n[8] 请在浏览器中观察页面...")
        print("按 Ctrl+C 关闭")

        try:
            page.wait_for_timeout(120000)
        except KeyboardInterrupt:
            pass

        browser.close()


if __name__ == "__main__":
    analyze_new_site()