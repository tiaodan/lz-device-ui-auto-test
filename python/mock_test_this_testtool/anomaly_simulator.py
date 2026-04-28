"""
异常场景模拟器
用于模拟各种UI异常场景，验证测试用例能否检测到问题
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from playwright.sync_api import Page
from utils.logger import get_default_logger


class AnomalySimulator:
    """异常场景模拟器"""

    def __init__(self, page: Page):
        self.page = page
        self.logger = get_default_logger()

    def simulate_element_missing(self, selector: str):
        """模拟元素缺失"""
        js_code = "const el = document.querySelector('" + selector + "'); if (el) el.remove();"
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] 元素缺失: {selector}")

    def simulate_element_hidden(self, selector: str):
        """模拟元素隐藏"""
        js_code = "const el = document.querySelector('" + selector + "'); if (el) el.style.display = 'none';"
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] 元素隐藏: {selector}")

    def simulate_element_duplicate(self, selector: str):
        """模拟元素重复"""
        js_code = """
            const el = document.querySelector('""" + selector + """');
            if (el) {
                const clone = el.cloneNode(true);
                clone.id = el.id;
                el.parentNode.appendChild(clone);
            }
        """
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] 元素重复: {selector}")

    def simulate_element_position_wrong(self, selector: str):
        """模拟元素位置错误"""
        js_code = """
            const el = document.querySelector('""" + selector + """');
            if (el) {
                el.style.position = 'absolute';
                el.style.left = '-9999px';
                el.style.top = '-9999px';
            }
        """
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] 元素位置错误: {selector}")

    def simulate_element_disabled(self, selector: str):
        """模拟元素禁用"""
        js_code = "const el = document.querySelector('" + selector + "'); if (el) el.disabled = true;"
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] 元素禁用: {selector}")

    def simulate_element_readonly(self, selector: str):
        """模拟元素只读"""
        js_code = "const el = document.querySelector('" + selector + "'); if (el) el.readOnly = true;"
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] 元素只读: {selector}")

    def simulate_white_screen(self):
        """模拟白屏"""
        self.page.evaluate("document.body.innerHTML = '';")
        self.logger.info("[模拟] 白屏")

    def simulate_network_error(self):
        """模拟网络错误"""
        self.page.evaluate("""
            document.body.innerHTML = '<div style="color:red;padding:20px;">Network Error</div>';
        """)
        self.logger.info("[模拟] 网络错误页面")

    def simulate_wrong_placeholder(self, selector: str, wrong_text: str):
        """模拟placeholder错误"""
        js_code = "const el = document.querySelector('" + selector + "'); if (el) el.placeholder = '" + wrong_text + "';"
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] placeholder错误: {selector} -> '{wrong_text}'")

    def simulate_wrong_button_text(self, selector: str, wrong_text: str):
        """模拟按钮文本错误"""
        js_code = "const el = document.querySelector('" + selector + "'); if (el) el.textContent = '" + wrong_text + "';"
        self.page.evaluate(js_code)
        self.logger.info(f"[模拟] 按钮文本错误: {selector} -> '{wrong_text}'")


# 预定义异常场景
ANOMALY_SCENARIOS = {
    # 元素缺失
    "username_missing": ("用户名输入框缺失", lambda s: s.simulate_element_missing("#username")),
    "password_missing": ("密码输入框缺失", lambda s: s.simulate_element_missing("#password")),
    "login_button_missing": ("登录按钮缺失", lambda s: s.simulate_element_missing(".lBtn")),
    "slider_missing": ("滑块缺失", lambda s: s.simulate_element_missing(".drag")),

    # 元素状态
    "username_hidden": ("用户名输入框隐藏", lambda s: s.simulate_element_hidden("#username")),
    "username_disabled": ("用户名输入框禁用", lambda s: s.simulate_element_disabled("#username")),
    "login_button_disabled": ("登录按钮禁用", lambda s: s.simulate_element_disabled(".lBtn")),

    # 元素重复
    "username_duplicate": ("用户名输入框重复", lambda s: s.simulate_element_duplicate("#username")),

    # 位置错误
    "username_position_wrong": ("用户名位置错误", lambda s: s.simulate_element_position_wrong("#username")),

    # 属性错误
    "placeholder_wrong": ("placeholder错误", lambda s: s.simulate_wrong_placeholder("#username", "WrongHint")),
    "button_text_wrong": ("按钮文本错误", lambda s: s.simulate_wrong_button_text(".lBtn", "WrongText")),

    # 页面级异常
    "white_screen": ("白屏", lambda s: s.simulate_white_screen()),
}