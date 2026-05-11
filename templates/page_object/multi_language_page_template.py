"""
支持多语言的页面对象模板
从配置文件加载定位器和期望值
"""

from playwright.sync_api import Page, Locator, expect
from typing import Dict, Any
import yaml
import os


class MultiLanguagePageTemplate:
    """多语言页面对象模板"""

    def __init__(self, page: Page, language: str = "zh_CN", config_path: str = None):
        self.page = page
        self._language = language
        self._config = self._load_config(config_path)

        # 从配置初始化定位器
        locators = self._config.get("locators", {})
        self.main_button = page.locator(locators.get("main_button", ".btn"))
        self.input_field = page.locator(locators.get("input_field", ".input"))

        # 加载当前语言的期望值
        self._expectations = self._load_expectations(language)

    def _load_config(self, config_path: str) -> Dict[str, Any]:
        """加载模块配置"""
        if config_path and os.path.exists(config_path):
            with open(config_path, "r", encoding="utf-8") as f:
                return yaml.safe_load(f)
        return {}

    def _load_expectations(self, language: str) -> Dict[str, str]:
        """加载语言期望值（从独立语言文件）"""
        lang_file = f"config/{language}.yaml"
        if os.path.exists(lang_file):
            with open(lang_file, "r", encoding="utf-8") as f:
                return yaml.safe_load(f).get("expectations", {})
        return {}

    # ==================== 语言切换 ====================

    def switch_language(self, target_lang: str):
        """切换页面语言"""
        # 根据实际页面实现
        pass

    def get_expectations(self, language: str = None) -> Dict[str, str]:
        """获取期望值"""
        lang = language or self._language
        return self._load_expectations(lang)

    # ==================== 验证方法（带期望值） ====================

    def verify_button_text(self):
        """验证按钮文本（使用配置期望值）"""
        expected = self._expectations.get("button_text", "")
        if expected:
            expect(self.main_button).to_contain_text(expected)

    def verify_placeholder(self):
        """验证占位符（使用配置期望值）"""
        expected = self._expectations.get("input_placeholder", "")
        if expected:
            expect(self.input_field).to_have_attribute("placeholder", expected)


# ==================== 配置文件示例 ====================

"""
# config/module_config.yaml
locators:
  main_button: ".submit-btn"
  input_field: ".username-input"

# config/zh_CN.yaml
expectations:
  button_text: "提交"
  input_placeholder: "请输入用户名"

# config/en_US.yaml
expectations:
  button_text: "Submit"
  input_placeholder: "Enter username"
"""