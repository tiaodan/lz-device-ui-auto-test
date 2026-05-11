"""
滑块验证码处理模板
模拟鼠标拖动事件序列
"""

from playwright.sync_api import Page, Locator


class SliderHandler:
    """滑块验证码处理器"""

    def __init__(self, page: Page):
        self.page = page

    def drag_slider(self,
                    slider_container: str = ".drag",
                    slider_btn: str = ".drag .btn",
                    offset: int = 10) -> bool:
        """
        拖动滑块验证码

        Args:
            slider_container: 滑块容器选择器
            slider_btn: 滑块按钮选择器
            offset: 边缘偏移量

        Returns:
            是否成功
        """
        # 等待滑块可见
        btn = self.page.locator(slider_btn)
        btn.wait_for(state="visible", timeout=5000)
        btn.hover()

        # 计算拖动距离
        container = self.page.locator(slider_container)
        drag_box = container.bounding_box()
        btn_box = btn.bounding_box()

        if not drag_box or not btn_box:
            return False

        target_x = drag_box["width"] - btn_box["width"] - offset

        # 执行拖动（模拟完整鼠标事件）
        self.page.evaluate(f"""() => {{
            const btn = document.querySelector('{slider_btn}');
            const drag = document.querySelector('{slider_container}');

            const startX = btn.offsetLeft;
            const startY = btn.offsetTop + btn.offsetHeight / 2;

            // mousedown
            btn.dispatchEvent(new MouseEvent('mousedown', {{
                bubbles: true,
                clientX: startX,
                clientY: startY,
                button: 0
            }}));

            // 分步移动（模拟真实拖动）
            const steps = 30;
            const targetLeft = {target_x};
            for (let i = 1; i <= steps; i++) {{
                const currentLeft = startX + (targetLeft - startX) * i / steps;
                const currentX = drag.offsetLeft + currentLeft + btn.offsetWidth / 2;

                document.dispatchEvent(new MouseEvent('mousemove', {{
                    bubbles: true,
                    clientX: currentX,
                    clientY: startY,
                    button: 0
                }}));
            }}

            // mouseup
            document.dispatchEvent(new MouseEvent('mouseup', {{
                bubbles: true,
                clientX: drag.offsetLeft + targetLeft + btn.offsetWidth / 2,
                clientY: startY,
                button: 0
            }}));
        }}""")

        self.page.wait_for_timeout(1000)
        return True

    def verify_success(self, success_text: str = "验证成功") -> bool:
        """验证是否成功"""
        # 根据实际页面调整验证方式
        try:
            text = self.page.locator(".slider-text").text_content()
            return success_text in text
        except:
            return False


# ==================== 使用示例 ====================

"""
# 在页面对象中使用
class LoginPage:
    def __init__(self, page: Page):
        self.page = page
        self.slider_handler = SliderHandler(page)

    def handle_slider(self):
        return self.slider_handler.drag_slider(
            slider_container=".drag",
            slider_btn=".drag .btn"
        )

# 在测试中使用
def test_login_with_slider(login_page):
    login_page.fill_credentials("user", "pass")
    login_page.handle_slider()
    login_page.click_login()
"""