"""
提取滑块验证码的HTML结构
"""

from playwright.sync_api import sync_playwright


def extract_slider_html():
    """提取滑块HTML结构"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        page.goto("https://192.168.85.238/", wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(2000)

        # 找到滑块元素
        slider = page.locator(".drag").first

        if slider:
            # 获取滑块的外部HTML
            slider_html = slider.evaluate("el => el.outerHTML")
            print("=== 滑块元素HTML ===\n")
            print(slider_html)

            # 获取滑块的父容器
            parent = slider.evaluate("el => el.parentElement.outerHTML.substring(0, 500)")
            print("\n=== 滑块父容器 ===\n")
            print(parent)

            # 获取滑块的尺寸
            box = slider.bounding_box()
            if box:
                print(f"\n=== 滑块位置和尺寸 ===")
                print(f"  x: {box['x']}, y: {box['y']}")
                print(f"  width: {box['width']}, height: {box['height']}")

            # 尝试找到滑块内部的拖动按钮
            print("\n=== 滑块内部元素 ===")
            children = slider.evaluate("""el => {
                let result = [];
                for (let child of el.children) {
                    result.push({
                        tagName: child.tagName,
                        className: child.className,
                        innerText: child.innerText.substring(0, 50)
                    });
                }
                return result;
            }""")
            print(children)

            # 截取滑块区域的截图
            try:
                slider.screenshot(path="screenshots/slider_element.png")
                print("\n滑块截图保存: screenshots/slider_element.png")
            except:
                print("\n滑块截图失败")

        else:
            print("未找到滑块元素")

        browser.close()


if __name__ == "__main__":
    extract_slider_html()