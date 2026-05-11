"""
配置文件读取模板
支持 YAML 配置，属性访问
"""

import yaml
import os
from typing import Dict, List, Any


class Config:
    """测试配置类 - 复制后添加需要的属性"""

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
        return self._config.get("base_url", "https://localhost")

    @property
    def username(self) -> str:
        return self._config.get("username", "root")

    @property
    def password(self) -> str:
        return self._config.get("password", "password")

    @property
    def language(self) -> str:
        return self._config.get("language", "zh_CN")

    @property
    def ignore_ssl_errors(self) -> bool:
        return self._config.get("ignore_ssl_errors", True)

    # ==================== 浏览器配置 ====================

    @property
    def headless(self) -> bool:
        return self._config.get("browser", {}).get("headless", True)

    @property
    def slow_mo(self) -> int:
        return self._config.get("browser", {}).get("slow_mo", 0)

    # ==================== 路径配置 ====================

    @property
    def screenshot_path(self) -> str:
        return self._config.get("screenshot_path", "screenshots")

    @property
    def log_path(self) -> str:
        return self._config.get("log_path", "logs")

    # ==================== 辅助方法 ====================

    def ensure_directories(self):
        """确保目录存在"""
        for dir_path in [self.screenshot_path, self.log_path]:
            os.makedirs(dir_path, exist_ok=True)

    def reload(self):
        """重新加载配置"""
        self._config = self._load_config()


# ==================== 全局实例 ====================

_config = None


def get_config(config_path: str = "config/test_config.yaml", reload: bool = False) -> Config:
    """获取配置实例"""
    global _config
    if reload or _config is None:
        _config = Config(config_path)
    return _config