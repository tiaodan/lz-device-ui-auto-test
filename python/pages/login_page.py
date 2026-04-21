"""
登录页面对象
支持三种测试类型的操作
"""

from playwright.sync_api import Page, Locator, expect
import time


class LoginPage:
    """登录页面对象 - 自适应新旧网站"""

    # ==================== 定位器 ====================

    def __init__(self, page: Page):
        self.page = page

        # 输入框（新旧网站通用）
        self.username_input = page.locator("#username")
        self.password_input = page.locator("#password")

        # 按钮（自适应）
        self.login_button = page.locator(".lBtn, button:has-text('Sign in'), button:has-text('登录')")

        # 滑块验证码（自适应新旧网站）
        # 旧网站: .drag, .drag .btn, .drag .progress
        # 新网站: .page-slide-wrap, .page-slide-btn, .page-slide-progress
        self.slider = page.locator(".drag, .page-slide-wrap")
        self.slider_btn = page.locator(".drag .btn, .page-slide-btn")
        self.slider_progress = page.locator(".drag .progress, .page-slide-progress")
        self.slider_text = page.locator(".drag .text, .page-slide-text")

        # 表单
        self.form = page.locator(".isoSignInForm, .page-signin-form, form")

        # Logo
        self.logo = page.locator(".signin-logo img, img[src*='logo']")

        # 错误提示
        self.error_message = page.locator(".ui-message-error, [class*='error']")

    def _detect_slider_type(self) -> str:
        """检测滑块类型：'old' 或 'new'"""
        if self.page.locator(".drag").count() > 0:
            return "old"
        elif self.page.locator(".page-slide-wrap").count() > 0:
            return "new"
        return "unknown"

    # ==================== 基础操作 ====================

    def navigate(self):
        """访问登录页"""
        self.page.goto("/", wait_until="networkidle")

    def fill_credentials(self, username: str, password: str):
        """填写用户名密码"""
        self.username_input.fill(username)
        self.password_input.fill(password)

    def click_login(self):
        """点击登录按钮"""
        self.login_button.click()

    def wait_for_response(self, timeout: int = 3000):
        """等待响应"""
        self.page.wait_for_timeout(timeout)

    # ==================== 滑块验证码处理 ====================

    def drag_slider(self):
        """拖动滑块验证码 - 自适应新旧网站"""

        slider_type = self._detect_slider_type()

        if slider_type == "old":
            # 旧网站 (.drag 结构)
            self.page.evaluate("""() => {
                const btn = document.querySelector('.drag .btn');
                const drag = document.querySelector('.drag');
                const progress = document.querySelector('.drag .progress');

                if (!btn || !drag || !progress) return false;

                const dragWidth = drag.offsetWidth;
                const btnWidth = btn.offsetWidth;
                const targetLeft = dragWidth - btnWidth - 10;

                const steps = 20;
                for (let i = 0; i <= steps; i++) {
                    const currentLeft = (targetLeft / steps) * i;
                    btn.style.left = currentLeft + 'px';
                    progress.style.width = currentLeft + 'px';
                }

                btn.style.left = targetLeft + 'px';
                progress.style.width = targetLeft + 'px';

                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                document.dispatchEvent(new MouseEvent('mousemove', { bubbles: true, clientX: targetLeft }));
                document.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));

                return true;
            }""")
        elif slider_type == "new":
            # 新网站 (.page-slide-wrap 结构)
            self.page.evaluate("""() => {
                const wrap = document.querySelector('.page-slide-wrap');
                const btn = document.querySelector('.page-slide-btn');
                const progress = document.querySelector('.page-slide-progress');

                if (!wrap || !btn || !progress) return false;

                const wrapWidth = wrap.offsetWidth;
                const btnWidth = btn.offsetWidth || 40;
                const targetWidth = wrapWidth - btnWidth - 5;

                const steps = 20;
                for (let i = 0; i <= steps; i++) {
                    const currentWidth = (targetWidth / steps) * i;
                    btn.style.left = currentWidth + 'px';
                    progress.style.width = currentWidth + 'px';
                }

                btn.style.left = targetWidth + 'px';
                progress.style.width = targetWidth + 'px';

                btn.dispatchEvent(new MouseEvent('mousedown', { bubbles: true }));
                document.dispatchEvent(new MouseEvent('mousemove', { bubbles: true, clientX: targetWidth }));
                document.dispatchEvent(new MouseEvent('mouseup', { bubbles: true }));

                return true;
            }""")

        self.page.wait_for_timeout(500)

    def get_slider_progress(self) -> str:
        """获取滑块进度 - 自适应"""
        return self.slider_progress.evaluate("el => el.style.width || el.style.left || '0px'")

    def is_slider_unlocked(self) -> bool:
        """检查滑块是否解锁"""
        progress = self.get_slider_progress()
        # 如果进度超过 300px，认为已解锁
        try:
            px = int(progress.replace("px", ""))
            return px > 300
        except:
            return False

    # ==================== 断言测试方法 ====================

    def verify_elements_visible(self):
        """验证元素可见性（断言测试）"""
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.slider).to_be_visible()
        expect(self.login_button).to_be_visible()
        expect(self.logo).to_be_visible()

    def verify_elements_enabled(self):
        """验证元素可用性（断言测试）"""
        expect(self.username_input).to_be_enabled()
        expect(self.password_input).to_be_enabled()
        expect(self.login_button).to_be_enabled()

    def verify_placeholder_text(self):
        """验证占位符文本（断言测试）"""
        expect(self.username_input).to_have_attribute("placeholder", "Username")
        expect(self.password_input).to_have_attribute("placeholder", "Password")

    def verify_slider_text(self):
        """验证滑块提示文本（断言测试）"""
        expect(self.slider_text).to_contain_text("slide")

    def verify_login_button_text(self):
        """验证登录按钮文本（断言测试）"""
        expect(self.login_button).to_contain_text("Sign in")

    def verify_url_after_login(self, expected_change: bool = True):
        """验证登录后 URL 变化（断言测试）"""
        if expected_change:
            # URL 应该变化（跳转到其他页面）
            expect(self.page).not_to_have_url("/")
        else:
            # URL 不变（登录失败）
            expect(self.page).to_have_url("/")

    # ==================== 图片识别测试方法 ====================

    def take_screenshot(self, name: str, path: str = "screenshots/current"):
        """截图保存（图片识别测试）"""
        full_path = f"{path}/{name}.png"
        self.page.screenshot(path=full_path)
        return full_path

    def take_element_screenshot(self, name: str, selector: str, path: str = "screenshots/current"):
        """元素截图（图片识别测试）"""
        element = self.page.locator(selector)
        full_path = f"{path}/{name}.png"
        element.screenshot(path=full_path)
        return full_path

    def get_page_dimensions(self):
        """获取页面尺寸"""
        return self.page.evaluate("""() => ({
            width: window.innerWidth,
            height: window.innerHeight,
            scrollWidth: document.body.scrollWidth,
            scrollHeight: document.body.scrollHeight
        })""")

    # ==================== API 测试方法 ====================

    def get_form_action(self) -> str:
        """获取表单 action（API 测试辅助）"""
        return self.form.evaluate("el => el.action || ''")

    def get_input_values(self) -> dict:
        """获取输入框当前值（API 测试辅助）"""
        return {
            "username": self.username_input.input_value(),
            "password": self.password_input.input_value()
        }

    def get_current_url(self) -> str:
        """获取当前 URL"""
        return self.page.url

    def get_page_title(self) -> str:
        """获取页面标题"""
        return self.page.title()


# ==================== 主页面对象（登录后） ====================

class MainPage:
    """主页面对象（登录后）"""

    def __init__(self, page: Page):
        self.page = page

        # 常用元素定位器
        self.user_info = page.locator("[class*='user'], [class*='avatar']")
        self.navigation = page.locator("nav, [class*='nav'], [class*='menu']")
        self.drone_section = page.locator("[class*='drone'], [href*='drone']")
        self.blacklist_section = page.locator("[class*='blacklist'], [href*='blacklist']")

    def navigate_to_drones(self):
        """导航到无人机页面"""
        self.drone_section.click()

    def navigate_to_blacklist(self):
        """导航到黑名单页面"""
        self.blacklist_section.click()

    def take_screenshot(self, name: str, path: str = "screenshots/current"):
        """截图"""
        full_path = f"{path}/{name}.png"
        self.page.screenshot(path=full_path)
        return full_path