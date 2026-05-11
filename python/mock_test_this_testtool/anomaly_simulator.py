"""
异常场景模拟器
通过 JS 注入模拟各种 UI 异常，验证测试用例能否检测到问题
使用 MutationObserver 持续阻止框架重新渲染
"""

from playwright.sync_api import Page
from loguru import logger
from config.module_config_loader import get_locators

_counter = 0


class AnomalySimulator:
    """异常场景模拟器"""

    def __init__(self, page: Page, module_name: str = "login"):
        self.page = page
        self._module_name = module_name
        self._locators = get_locators(module_name)

    def _get_selector(self, name: str) -> str:
        return self._locators[name]

    def _gen_key(self) -> str:
        global _counter
        _counter += 1
        return f"__mock_observer_{_counter}"

    def simulate_element_missing(self, locator_name: str):
        """模拟元素缺失（对于 input，删除外层 wrapper）"""
        selector = self._get_selector(locator_name)
        key = self._gen_key()

        self.page.evaluate(
            """
            ([selector, key]) => {
                const el = document.querySelector(selector);

                function removeElement() {
                    const el = document.querySelector(selector);
                    if (!el) return;

                    if (el.tagName === 'INPUT') {
                        const wrapper = el.closest('.ui-input-affix-wrapper');
                        if (wrapper) wrapper.remove();
                        else el.remove();
                    } else {
                        el.remove();
                    }
                }

                removeElement();

                const observer = new MutationObserver(removeElement);
                observer.observe(document.body, { childList: true, subtree: true });
                window[key] = observer;
            }
            """,
            [selector, key]
        )
        logger.info(f"[模拟] 元素缺失: {locator_name} ({selector})")

    def simulate_element_hidden(self, locator_name: str):
        """模拟元素隐藏"""
        selector = self._get_selector(locator_name)
        key = self._gen_key()

        self.page.evaluate(
            """
            ([selector, key]) => {
                function hide() {
                    const el = document.querySelector(selector);
                    if (el) el.style.display = 'none';
                }
                hide();

                const observer = new MutationObserver(hide);
                observer.observe(document.body, { childList: true, subtree: true, attributes: true });
                window[key] = observer;
            }
            """,
            [selector, key]
        )
        logger.info(f"[模拟] 元素隐藏: {locator_name} ({selector})")

    def simulate_element_disabled(self, locator_name: str):
        """模拟元素禁用"""
        selector = self._get_selector(locator_name)
        key = self._gen_key()

        self.page.evaluate(
            """
            ([selector, key]) => {
                function disable() {
                    const el = document.querySelector(selector);
                    if (el) el.disabled = true;
                }
                disable();

                const observer = new MutationObserver(disable);
                observer.observe(document.body, { childList: true, subtree: true, attributes: true });
                window[key] = observer;
            }
            """,
            [selector, key]
        )
        logger.info(f"[模拟] 元素禁用: {locator_name} ({selector})")

    def simulate_element_duplicate(self, locator_name: str):
        """模拟元素重复"""
        selector = self._get_selector(locator_name)
        self.page.evaluate(
            """
            (selector) => {
                const el = document.querySelector(selector);
                if (el) {
                    const clone = el.cloneNode(true);
                    clone.id = el.id;
                    el.parentNode.appendChild(clone);
                }
            }
            """,
            selector
        )
        logger.info(f"[模拟] 元素重复: {locator_name} ({selector})")

    def simulate_element_position_wrong(self, locator_name: str):
        """模拟元素位置错误"""
        selector = self._get_selector(locator_name)
        key = self._gen_key()

        self.page.evaluate(
            """
            ([selector, key]) => {
                function move() {
                    const el = document.querySelector(selector);
                    if (el) {
                        el.style.position = 'absolute';
                        el.style.left = '-9999px';
                        el.style.top = '-9999px';
                    }
                }
                move();

                const observer = new MutationObserver(move);
                observer.observe(document.body, { childList: true, subtree: true, attributes: true });
                window[key] = observer;
            }
            """,
            [selector, key]
        )
        logger.info(f"[模拟] 元素位置错误: {locator_name} ({selector})")

    def simulate_wrong_placeholder(self, locator_name: str, wrong_text: str):
        """模拟 placeholder 错误"""
        selector = self._get_selector(locator_name)
        key = self._gen_key()

        self.page.evaluate(
            """
            ([selector, wrongText, key]) => {
                function change() {
                    const el = document.querySelector(selector);
                    if (el) el.placeholder = wrongText;
                }
                change();

                const observer = new MutationObserver(change);
                observer.observe(document.body, { childList: true, subtree: true, attributes: true });
                window[key] = observer;
            }
            """,
            [selector, wrong_text, key]
        )
        logger.info(f"[模拟] placeholder错误: {locator_name} -> '{wrong_text}'")

    def simulate_wrong_text(self, locator_name: str, wrong_text: str):
        """模拟文本内容错误"""
        selector = self._get_selector(locator_name)
        key = self._gen_key()

        self.page.evaluate(
            """
            ([selector, wrongText, key]) => {
                function change() {
                    const el = document.querySelector(selector);
                    if (el) el.textContent = wrongText;
                }
                change();

                const observer = new MutationObserver(change);
                observer.observe(document.body, { childList: true, subtree: true, attributes: true });
                window[key] = observer;
            }
            """,
            [selector, wrong_text, key]
        )
        logger.info(f"[模拟] 文本错误: {locator_name} -> '{wrong_text}'")

    def simulate_white_screen(self):
        """模拟白屏"""
        key = self._gen_key()
        self.page.evaluate(
            """
            (key) => {
                document.body.innerHTML = '';
                const observer = new MutationObserver(() => {
                    document.body.innerHTML = '';
                });
                observer.observe(document.documentElement, { childList: true, subtree: true });
                window[key] = observer;
            }
            """,
            key
        )
        logger.info("[模拟] 白屏")

    def simulate_network_error(self):
        """模拟网络错误页面"""
        key = self._gen_key()
        self.page.evaluate(
            """
            (key) => {
                document.body.innerHTML = '<div style="color:red;padding:20px;">Network Error</div>';
                const observer = new MutationObserver(() => {
                    document.body.innerHTML = '<div style="color:red;padding:20px;">Network Error</div>';
                });
                observer.observe(document.documentElement, { childList: true, subtree: true });
                window[key] = observer;
            }
            """,
            key
        )
        logger.info("[模拟] 网络错误页面")

    def restore_all(self):
        """恢复所有模拟"""
        self.page.evaluate("""
            () => {
                for (const key of Object.keys(window)) {
                    if (key.startsWith('__mock_observer_')) {
                        window[key].disconnect();
                        delete window[key];
                    }
                }
            }
        """)
        logger.info("[模拟] 已恢复所有异常")