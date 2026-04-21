"""
配置文件读取模块
支持 YAML 配置文件
"""

import yaml
import os
from typing import Dict, List, Any


class Config:
    """测试配置类"""

    def __init__(self, config_path: str = "config/test_config.yaml"):
        self.config_path = config_path
        self._config = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        """加载配置文件"""
        if not os.path.exists(self.config_path):
            raise FileNotFoundError(f"配置文件不存在: {self.config_path}")

        with open(self.config_path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f)

    # ==================== 基础配置 ====================

    @property
    def base_url(self) -> str:
        """测试环境 URL"""
        return self._config.get("base_url", "https://192.168.85.238")

    @property
    def login_url(self) -> str:
        """登录接口 URL"""
        return self._config.get("login_url", f"{self.base_url}/login")

    @property
    def graphql_url(self) -> str:
        """GraphQL API URL"""
        return self._config.get("graphql_url", f"{self.base_url}/rf/graphql")

    @property
    def username(self) -> str:
        """用户名"""
        return self._config.get("username", "root")

    @property
    def password(self) -> str:
        """密码"""
        return self._config.get("password", "password")

    @property
    def ignore_ssl_errors(self) -> bool:
        """忽略 SSL 错误"""
        return self._config.get("ignore_ssl_errors", True)

    # ==================== 浏览器配置 ====================

    @property
    def browser_type(self) -> str:
        """浏览器类型"""
        return self._config.get("browser", {}).get("type", "chromium")

    @property
    def headless(self) -> bool:
        """无头模式"""
        return self._config.get("browser", {}).get("headless", True)

    @property
    def slow_mo(self) -> int:
        """操作延迟"""
        return self._config.get("browser", {}).get("slow_mo", 0)

    # ==================== 测试类型配置 ====================

    @property
    def test_types(self) -> List[str]:
        """启用的测试类型"""
        return self._config.get("test_types", ["assertion", "visual", "api"])

    def is_test_type_enabled(self, test_type: str) -> bool:
        """检查测试类型是否启用"""
        return test_type in self.test_types

    # ==================== 断言测试配置 ====================

    @property
    def assertion_config(self) -> Dict[str, Any]:
        """断言测试配置"""
        return self._config.get("assertion", {})

    @property
    def assertion_timeout(self) -> int:
        """断言超时时间"""
        return self.assertion_config.get("timeout", 5000)

    @property
    def assertion_retries(self) -> int:
        """断言重试次数"""
        return self.assertion_config.get("retries", 3)

    @property
    def assertion_screenshot_path(self) -> str:
        """断言截图路径"""
        return self.assertion_config.get("screenshot_path", "screenshots/assertion")

    @property
    def screenshot_on_failure(self) -> bool:
        """失败时截图"""
        return self.assertion_config.get("screenshot_on_failure", True)

    # ==================== 图片识别测试配置 ====================

    @property
    def visual_config(self) -> Dict[str, Any]:
        """图片识别测试配置"""
        return self._config.get("visual", {})

    @property
    def baseline_path(self) -> str:
        """基准图路径"""
        return self.visual_config.get("baseline_path", "screenshots/baseline")

    @property
    def current_path(self) -> str:
        """当前截图路径"""
        return self.visual_config.get("current_path", "screenshots/current")

    @property
    def diff_path(self) -> str:
        """差异图路径"""
        return self.visual_config.get("diff_path", "screenshots/diff")

    @property
    def visual_threshold(self) -> float:
        """对比阈值"""
        return self.visual_config.get("threshold", 0.1)

    @property
    def auto_update_baseline(self) -> bool:
        """自动更新基准图"""
        return self.visual_config.get("auto_update_baseline", False)

    # ==================== 接口测试配置 ====================

    @property
    def api_config(self) -> Dict[str, Any]:
        """接口测试配置"""
        return self._config.get("api", {})

    @property
    def api_timeout(self) -> int:
        """API 超时时间"""
        return self.api_config.get("timeout", 30000)

    @property
    def verify_ui_consistency(self) -> bool:
        """验证 UI 与 API 数据一致性"""
        return self.api_config.get("verify_ui_consistency", True)

    @property
    def common_queries(self) -> List[str]:
        """常用查询接口"""
        return self.api_config.get("common_queries", ["drone", "blacklist", "whitelist"])

    # ==================== 测试用例配置 ====================

    @property
    def test_cases(self) -> Dict[str, Any]:
        """测试用例配置"""
        return self._config.get("test_cases", {})

    def get_test_case(self, case_name: str) -> Dict[str, Any]:
        """获取测试用例配置"""
        return self.test_cases.get(case_name, {})

    def is_test_case_enabled(self, case_name: str) -> bool:
        """检查测试用例是否启用"""
        case = self.get_test_case(case_name)
        return case.get("enabled", False)

    def get_test_case_types(self, case_name: str) -> List[str]:
        """获取测试用例的测试类型"""
        case = self.get_test_case(case_name)
        return case.get("types", [])

    # ==================== 辅助方法 ====================

    def ensure_directories(self):
        """确保所有必要目录存在"""
        directories = [
            self.assertion_screenshot_path,
            self.baseline_path,
            self.current_path,
            self.diff_path,
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)

    def reload(self):
        """重新加载配置"""
        self._config = self._load_config()

    def __repr__(self):
        return f"Config(base_url={self.base_url}, test_types={self.test_types})"


# 全局配置实例
_config = None
_config_path = None


def get_config(config_path: str = "config/test_config.yaml", reload: bool = False) -> Config:
    """
    获取配置实例

    Args:
        config_path: 配置文件路径
        reload: 是否强制重新加载（每次运行测试时建议设为 True）

    Returns:
        Config 实例
    """
    global _config, _config_path

    # 如果配置路径改变或要求重新加载，则重新加载
    if reload or _config is None or _config_path != config_path:
        _config = Config(config_path)
        _config_path = config_path
    return _config


def reload_config():
    """强制重新加载配置"""
    global _config
    if _config:
        _config.reload()
    return _config