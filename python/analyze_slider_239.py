"""
详细分析新网站滑块结构
"""

from playwright.sync_api import sync_playwright


def analyze_slider():
    """详细分析滑块元素结构"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto("https://192.168.85.239", timeout=30000)
        page.wait_for_timeout(3000)

        print("\n" + "="*60)
        print("滑块详细分析")
        print("="*60)

        # 1. 分析 slide 相关元素
        print("\n[slide 相关元素]")
        slide_elements = page.locator("[class*='slide']").all()
        for i, el in enumerate(slide_elements):
            try:
                info = el.evaluate("""el => ({
                    tagName: el.tagName,
                    className: el.className,
                    id: el.id,
                    innerHTML: el.innerHTML.substring(0, 100)
                })""")
                print(f"  [{i+1}] {info}")
            except Exception as e:
                print(f"  [{i+1}] Error: {e}")

        # 2. 分析 page-slide-wrap
        print("\n[page-slide-wrap 元素]")
        wrap_elements = page.locator(".page-slide-wrap").all()
        for i, el in enumerate(wrap_elements):
            try:
                info = el.evaluate("""el => ({
                    className: el.className,
                    childCount: el.children.length,
                    innerHTML: el.innerHTML.substring(0, 200)
                })""")
                print(f"  [{i+1}] {info}")
            except Exception as e:
                print(f"  [{i+1}] Error: {e}")

        # 3. 查找滑块按钮
        print("\n[查找滑块按钮]")
        possible_selectors = [
            ".page-slide-wrap .btn",
            ".page-slide-wrap button",
            ".page-slide-wrap [class*='btn']",
            ".page-slide-wrap [class*='slider']",
            ".page-slide-wrap [class*='drag']",
            "[class*='slide-btn']",
            "[class*='slider-btn']",
        ]

        for selector in possible_selectors:
            count = page.locator(selector).count()
            if count > 0:
                print(f"  {selector}: {count} 个")
                try:
                    el = page.locator(selector).first
                    info = el.evaluate("""el => ({
                        className: el.className,
                        text: el.innerText || el.textContent
                    })""")
                    print(f"    -> {info}")
                except:
                    pass

        # 4. 查找进度条相关
        print("\n[进度条相关]")
        progress_selectors = [
            "[class*='progress']",
            "[class*='bar']",
            "[style*='width']",
        ]

        for selector in progress_selectors:
            elements = page.locator(selector).all()
            if elements:
                print(f"  {selector}: {len(elements)} 个")
                for j, el in enumerate(elements[:3]):  # 只显示前3个
                    try:
                        info = el.evaluate("el => el.className || el.style.width")
                        print(f"    [{j+1}] {info}")
                    except:
                        pass

        # 5. 获取完整HTML结构（滑块区域）
        print("\n[滑块区域HTML]")
        try:
            slide_wrap = page.locator(".page-slide-wrap").first
            html = slide_wrap.evaluate("el => el.outerHTML")
            print(f"  {html[:500]}")
        except:
            print("  未找到 .page-slide-wrap")

        # 6. 截图
        page.screenshot(path="screenshots/slider_239.png")
        print("\n[截图] screenshots/slider_239.png")

        browser.close()


if __name__ == "__main__":
    analyze_slider()