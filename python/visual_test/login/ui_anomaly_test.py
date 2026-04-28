"""
UI异常场景视觉测试
通过JavaScript注入模拟前端界面异常
"""

import pytest


class UIAnomalySimulator:
    """UI异常模拟器"""

    def __init__(self, page, test_logger):
        self.page = page
        self.logger = test_logger

    def hide_element(self, selector: str):
        """隐藏元素"""
        self.page.evaluate(f"const el = document.querySelector('{selector}'); if (el) el.style.display = 'none';")
        self.logger.info(f"[UI异常] 隐藏元素: {selector}")

    def break_element_position(self, selector: str):
        """破坏元素定位"""
        self.page.evaluate(f"""
            const el = document.querySelector('{selector}');
            if (el) {{
                el.style.position = 'absolute';
                el.style.left = Math.random() * 100 + 'px';
                el.style.top = Math.random() * 100 + 'px';
            }}
        """)
        self.logger.info(f"[UI异常] 位置错乱: {selector}")

    def break_element_style(self, selector: str):
        """破坏元素样式"""
        self.page.evaluate(f"""
            const el = document.querySelector('{selector}');
            if (el) {{
                el.style.background = 'red';
                el.style.color = 'white';
                el.style.fontSize = '50px';
            }}
        """)
        self.logger.info(f"[UI异常] 样式破坏: {selector}")

    def remove_element(self, selector: str):
        """移除元素"""
        self.page.evaluate(f"const el = document.querySelector('{selector}'); if (el) el.remove();")
        self.logger.info(f"[UI异常] 移除元素: {selector}")

    def duplicate_element(self, selector: str):
        """重复元素"""
        self.page.evaluate(f"""
            const el = document.querySelector('{selector}');
            if (el) {{
                const clone = el.cloneNode(true);
                el.parentNode.appendChild(clone);
            }}
        """)
        self.logger.info(f"[UI异常] 重复元素: {selector}")

    def white_screen(self):
        """白屏"""
        self.page.evaluate("document.body.innerHTML = '';")
        self.logger.info("[UI异常] 白屏")


@pytest.mark.visual
def test_ui_anomaly_visual(page, visual_test, test_logger):
    """测试：UI异常场景视觉检测"""

    test_logger.section("视觉测试: UI异常场景检测")

    anomalies = [
        ("隐藏用户名输入框", lambda s: s.hide_element("#username")),
        ("隐藏登录按钮", lambda s: s.hide_element(".lBtn")),
        ("登录按钮位置错乱", lambda s: s.break_element_position(".lBtn")),
        ("登录按钮样式破坏", lambda s: s.break_element_style(".lBtn")),
        ("白屏", lambda s: s.white_screen()),
    ]

    for name, simulate_func in anomalies:
        test_logger.section(f"异常场景: {name}")

        page.wait_for_timeout(1000)

        simulator = UIAnomalySimulator(page, test_logger)
        simulate_func(simulator)
        page.wait_for_timeout(500)

        visual_test.take_screenshot(f"anomaly_{name.replace(' ', '_')}")

        # 与正常状态对比
        if visual_test.has_baseline("login_page_initial"):
            result = visual_test.compare_with_baseline(f"anomaly_{name.replace(' ', '_')}", "login_page_initial")
            if not result["match"]:
                test_logger.pass_("成功检测到UI异常")
            else:
                test_logger.fail("未能检测到UI异常")
        else:
            test_logger.warn("无正常状态基准图")

    test_logger.section("测试完成")