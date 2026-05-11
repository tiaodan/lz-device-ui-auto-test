"""
登录页面对象
从配置文件读取定位器，支持多语言
"""

from playwright.sync_api import Page, Locator, expect
from config.module_config_loader import get_module_config, get_expectations, get_descriptions


class LoginPage:
    """登录页面对象"""

    def __init__(self, page: Page, language: str = "zh_CN"):
        """
        初始化登录页面对象
        Args:
            page (Page): 页面对象
            language (str): 当前语言，如 'zh_CN', 'en_US'
        """
        self.page = page
        self._language = language

        # 加载配置
        self._config = get_module_config("login")
        locators = self._config["locators"]

        # 加载描述名词（不随语言切换）
        self.desc = get_descriptions("login")

        # 直接加载当前语言的期望值
        self.exp = self.get_expectations(language)

        # 从配置初始化定位器
        self.username_input = page.locator(locators["username_input"])
        self.password_input = page.locator(locators["password_input"])
        self.login_button = page.locator(locators["login_button"])
        self.slider = page.locator(locators["slider_container"])
        self.slider_btn = page.locator(locators["slider_btn"])
        self.slider_progress = page.locator(locators["slider_progress"])
        self.slider_text = page.locator(locators["slider_text"])
        self.form = page.locator(locators["form"])
        self.logo = page.locator(locators["logo"])
        self.sys_name = page.locator(locators["sys_name"])
        self.error_message = page.locator(locators["error_message"])

        # 语言切换相关定位器
        self.language_switch = page.locator(locators.get("language_switch", ".topbarLocal"))
        self.language_item = page.locator(locators.get("language_item", ".ui-popover-inner-content .ui-space-item"))

    # ==================== 配置访问方法 ====================

    def get_locators(self) -> dict:
        """获取定位器配置"""
        return self._config["locators"]

    def get_expectations(self, language: str = None) -> dict:
        """
        获取断言期望值（从独立语言文件加载）
        Args:
            language: 语言代码，如 'zh_CN', 'en_US'，不传则使用当前语言
        """
        lang = language or self._language
        return get_expectations("login", lang)

    def get_test_data(self) -> dict:
        """获取测试数据"""
        return self._config["test_data"]

    def get_current_language(self) -> str:
        """获取当前语言"""
        return self._language

    def set_language(self, language: str):
        """设置当前语言"""
        self._language = language

    # ==================== 语言切换操作 ====================

    def switch_language(self, target_lang: str = "zh"):
        """
        切换页面语言

        Args:
            target_lang: 目标语言，'en' 或 'zh'

        Returns:
            bool: 是否切换成功
        """
        if target_lang == self._language:
            return True  # 已经是目标语言

        try:
            # 点击语言切换按钮
            self.language_switch.click()
            self.page.wait_for_timeout(500)

            # 点击对应的语言选项
            # 第一个是中文，第二个是英文
            if target_lang == "zh":
                self.language_item.first.click()
            else:
                self.language_item.nth(1).click()

            self.page.wait_for_timeout(1000)
            self._language = target_lang

            return True
        except Exception as e:
            print(f"切换语言失败: {e}")
            return False

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
        # 用 JS 点击，避免 Playwright click() 不触发响应
        self.page.evaluate("document.querySelector('.lBtn').click()")

    def wait_for_response(self, timeout: int = 3000):
        """等待响应"""
        self.page.wait_for_timeout(timeout)

    # ==================== 滑块验证码处理 ====================

    def drag_slider(self):
        """拖动滑块验证码"""
        # 等待滑块按钮可见
        self.slider_btn.wait_for(state="visible", timeout=5000)

        # 悬停到滑块按钮上
        self.slider_btn.hover()

        # 计算拖动距离（滑块容器宽度 - 按钮宽度）
        drag_box = self.slider.bounding_box()
        btn_box = self.slider_btn.bounding_box()

        if not drag_box or not btn_box:
            return False

        # 目标位置
        target_x = drag_box["width"] - btn_box["width"] - 10

        # 使用 Playwright 的 drag_to 方法
        # 创建一个虚拟目标元素来拖动到
        self.page.evaluate(f"""() => {{
            const btn = document.querySelector('.drag .btn');
            const drag = document.querySelector('.drag');

            // 模拟真实拖动
            const startX = btn.offsetLeft;
            const startY = btn.offsetTop + btn.offsetHeight / 2;

            // 触发mousedown
            btn.dispatchEvent(new MouseEvent('mousedown', {{
                bubbles: true,
                clientX: startX,
                clientY: startY,
                button: 0
            }}));

            // 分步移动，触发mousemove
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

            // 触发mouseup
            document.dispatchEvent(new MouseEvent('mouseup', {{
                bubbles: true,
                clientX: drag.offsetLeft + targetLeft + btn.offsetWidth / 2,
                clientY: startY,
                button: 0
            }}));
        }}""")

        self.page.wait_for_timeout(1000)

        # 验证是否成功（检查文字）
        text = self.slider_text.text_content()
        return "验证成功" in text or "success" in text.lower()

    def is_slider_verified(self) -> bool:
        """检查滑块是否验证成功"""
        text = self.slider_text.text_content()
        return "验证成功" in text or "√" in text

    def get_slider_progress(self) -> str:
        """获取滑块进度"""
        return self.slider_progress.evaluate("el => el.style.width || '0px'")

    def is_slider_unlocked(self) -> bool:
        """检查滑块是否解锁"""
        progress = self.get_slider_progress()
        try:
            px = int(progress.replace("px", ""))
            return px > 300
        except:
            return False

    # ==================== 断言测试方法 ====================

    def verify_elements_visible(self):
        """验证元素可见性"""
        expect(self.username_input).to_be_visible()
        expect(self.password_input).to_be_visible()
        expect(self.slider).to_be_visible()
        expect(self.login_button).to_be_visible()

    def verify_elements_enabled(self):
        """验证元素可用性"""
        expect(self.username_input).to_be_enabled()
        expect(self.password_input).to_be_enabled()
        expect(self.login_button).to_be_enabled()

    def verify_placeholder_text(self, language: str = None):
        """验证占位符文本（使用配置期望值）"""
        expectations = self.get_expectations(language)
        expect(self.username_input).to_have_attribute("placeholder", expectations["username_placeholder"])
        expect(self.password_input).to_have_attribute("placeholder", expectations["password_placeholder"])

    def verify_slider_text(self, language: str = None):
        """验证滑块提示文本"""
        expectations = self.get_expectations(language)
        expect(self.slider_text).to_contain_text(expectations["slider_text_contains"])

    def verify_login_button_text(self, language: str = None):
        """验证登录按钮文本"""
        expectations = self.get_expectations(language)
        expect(self.login_button).to_contain_text(expectations["login_button_text"])

    # ==================== 视觉测试方法 ====================

    def take_screenshot(self, name: str, path: str = "screenshots/current"):
        """截图保存"""
        full_path = f"{path}/{name}.png"
        self.page.screenshot(path=full_path)
        return full_path

    def take_element_screenshot(self, name: str, selector: str, path: str = "screenshots/current"):
        """元素截图"""
        element = self.page.locator(selector)
        full_path = f"{path}/{name}.png"
        element.screenshot(path=full_path)
        return full_path

    # ==================== API测试方法 ====================

    def get_input_values(self) -> dict:
        """获取输入框当前值"""
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