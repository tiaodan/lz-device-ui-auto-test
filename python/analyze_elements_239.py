"""
精确分析新网站 192.168.85.239 的登录页面元素
"""

from playwright.sync_api import sync_playwright


def analyze_elements():
    """精确分析页面元素"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto("https://192.168.85.239", timeout=30000)
        page.wait_for_timeout(3000)

        print("\n" + "="*60)
        print("新网站 (192.168.85.239) 登录页面分析")
        print("="*60)

        print(f"\n页面标题: {page.title()}")

        # 输入框
        print("\n[输入框]")
        inputs = page.locator("input").all()
        for i, inp in enumerate(inputs):
            info = inp.evaluate("""el => ({
                type: el.type,
                id: el.id,
                name: el.name,
                placeholder: el.placeholder,
                className: el.className
            })""")
            print(f"  [{i+1}] {info}")

        # 按钮
        print("\n[按钮]")
        buttons = page.locator("button").all()
        for i, btn in enumerate(buttons):
            info = btn.evaluate("""el => ({
                text: el.innerText,
                type: el.type,
                className: el.className
            })""")
            print(f"  [{i+1}] {info}")

        # 滑块相关
        print("\n[滑块相关]")
        keywords = ["slider", "drag", "slide", "verify", "captcha"]
        for kw in keywords:
            count = page.locator(f"[class*='{kw}']").count()
            if count > 0:
                print(f"  '{kw}' 找到 {count} 个")

        # 检查 .drag 是否存在
        drag_count = page.locator(".drag").count()
        print(f"\n[检查] .drag 元素数量: {drag_count}")

        # 查找所有 div，看有没有可拖动的
        print("\n[可拖动元素 (touch-action)]")
        touch_elements = page.locator("[style*='touch-action']").all()
        for i, el in enumerate(touch_elements):
            info = el.evaluate("el => ({ className: el.className, style: el.style.touchAction })")
            print(f"  [{i+1}] {info}")

        # 表单
        print("\n[表单]")
        forms = page.locator("form").all()
        for i, form in enumerate(forms):
            info = form.evaluate("el => ({ className: el.className, id: el.id })")
            print(f"  [{i+1}] {info}")

        browser.close()


if __name__ == "__main__":
    analyze_elements()