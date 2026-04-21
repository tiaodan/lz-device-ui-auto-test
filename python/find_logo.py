"""
查找 Logo 元素
"""

from playwright.sync_api import sync_playwright
from config.config_loader import get_config


def find_logo():
    """查找页面中的 Logo 元素"""

    config = get_config()

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        page.goto(config.base_url, wait_until="networkidle")
        page.wait_for_timeout(1000)

        print("\n=== 查找 Logo 元素 ===\n")

        # 查找所有 img 标签
        imgs = page.locator("img").all()
        print(f"找到 {len(imgs)} 个 img 标签:\n")

        for i, img in enumerate(imgs):
            try:
                src = img.get_attribute("src") or ""
                alt = img.get_attribute("alt") or ""
                class_name = img.get_attribute("class") or ""
                print(f"[{i+1}] src: {src}")
                print(f"    alt: {alt}")
                print(f"    class: {class_name}")
                print()
            except:
                pass

        # 查找可能包含 logo 的其他元素
        print("\n=== 其他可能的 Logo 元素 ===\n")

        # 查找 class 包含 logo 的元素
        logo_elements = page.locator("[class*='logo'], [class*='Logo']").all()
        print(f"class 包含 'logo' 的元素: {len(logo_elements)} 个")
        for i, el in enumerate(logo_elements):
            try:
                tag = el.evaluate("el => el.tagName")
                class_name = el.evaluate("el => el.className")
                print(f"  [{i+1}] {tag}, class: {class_name}")
            except:
                pass

        browser.close()


if __name__ == "__main__":
    find_logo()