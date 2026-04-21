"""
详细分析登录页面元素
"""

from playwright.sync_api import sync_playwright
import json


def analyze_login_elements():
    """详细分析登录页面"""

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=True)
        page = context.new_page()

        # 访问真正的登录页
        page.goto("https://192.168.85.238/", wait_until="networkidle", timeout=15000)
        page.wait_for_timeout(2000)

        print("=== 登录页面详细分析 ===\n")

        # 截图
        page.screenshot(path="screenshots/login_full.png", full_page=True)

        # 分析所有输入框
        print("【输入框】")
        inputs = page.locator("input").all()
        for i, inp in enumerate(inputs):
            try:
                info = inp.evaluate("""el => ({
                    type: el.type,
                    name: el.name,
                    placeholder: el.placeholder,
                    id: el.id,
                    className: el.className,
                    value: el.value
                })""")
                print(f"  [{i+1}] {json.dumps(info, ensure_ascii=False)}")
            except Exception as e:
                print(f"  [{i+1}] 获取失败: {e}")

        # 分析所有按钮
        print("\n【按钮】")
        buttons = page.locator("button").all()
        for i, btn in enumerate(buttons):
            try:
                info = btn.evaluate("""el => ({
                    text: el.innerText,
                    type: el.type,
                    className: el.className,
                    disabled: el.disabled
                })""")
                print(f"  [{i+1}] {json.dumps(info, ensure_ascii=False)}")
            except Exception as e:
                print(f"  [{i+1}] 获取失败: {e}")

        # 分析滑块相关元素
        print("\n【滑块/验证码元素】")
        slider_keywords = ["slider", "drag", "verify", "captcha", "slide", "track"]
        for keyword in slider_keywords:
            elements = page.locator(f"[class*='{keyword}']").all()
            if elements:
                print(f"  关键词 '{keyword}' 找到 {len(elements)} 个元素")
                for j, el in enumerate(elements):
                    try:
                        info = el.evaluate("""el => ({
                            tagName: el.tagName,
                            className: el.className,
                            id: el.id,
                            innerText: el.innerText ? el.innerText.substring(0, 50) : ''
                        })""")
                        print(f"    [{j+1}] {json.dumps(info, ensure_ascii=False)}")
                    except:
                        pass

        # 分析图片
        print("\n【图片】")
        images = page.locator("img").all()
        for i, img in enumerate(images):
            try:
                info = img.evaluate("""el => ({
                    src: el.src,
                    alt: el.alt,
                    className: el.className
                })""")
                print(f"  [{i+1}] {json.dumps(info, ensure_ascii=False)}")
            except:
                pass

        # 分析表单
        print("\n【表单】")
        forms = page.locator("form").all()
        for i, form in enumerate(forms):
            try:
                info = form.evaluate("""el => ({
                    className: el.className,
                    id: el.id,
                    action: el.action
                })""")
                print(f"  [{i+1}] {json.dumps(info, ensure_ascii=False)}")
            except:
                pass

        # 查找可能的验证码容器
        print("\n【验证码容器】")
        captcha_containers = page.locator("div[class*='captcha'], div[class*='verify'], div[class*='slider']").all()
        if captcha_containers:
            for i, container in enumerate(captcha_containers):
                try:
                    html = container.evaluate("el => el.outerHTML.substring(0, 200)")
                    print(f"  [{i+1}] {html}")
                except:
                    pass
        else:
            print("  未找到明显的验证码容器")

        # 获取完整HTML结构保存到文件
        html = page.content()
        with open("screenshots/login_page_full.html", "w", encoding="utf-8") as f:
            f.write(html)
        print("\n完整HTML已保存到 screenshots/login_page_full.html")

        # 尝试获取React组件信息
        print("\n【React组件检测】")
        react_root = page.locator("#root, [data-reactroot]").first
        if react_root:
            print("  找到React根元素")

        browser.close()


if __name__ == "__main__":
    analyze_login_elements()