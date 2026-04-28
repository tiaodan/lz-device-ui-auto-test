"""
测试日志器 - 基于 loguru
提供测试专用日志方法，与原有 logger.py API 兼容
"""

import sys
import os
from loguru import logger
from datetime import datetime


def setup_loguru(log_dir: str = "logs", level: str = "INFO"):
    """
    配置 loguru

    Args:
        log_dir: 日志目录
        level: 日志级别
    """
    os.makedirs(log_dir, exist_ok=True)

    date_str = datetime.now().strftime("%Y-%m-%d")
    log_file = os.path.join(log_dir, f"test_{date_str}.log")

    logger.remove()

    logger.add(
        sys.stderr,
        level=level,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> [<level>{level}</level>] {message}",
        colorize=True
    )

    logger.add(
        log_file,
        level=level,
        format="{time:YYYY-MM-DD HH:mm:ss} [{level}] {message}",
        encoding="utf-8",
        rotation="10 MB",
        retention="7 days"
    )

    return logger


class TestLogger:
    """
    测试日志器封装类
    与原有 logger.py API 兼容
    """

    def __init__(self, log_dir: str = "logs", level: str = "INFO"):
        self._logger = setup_loguru(log_dir, level)

    def step(self, step_num: int, message: str):
        """记录测试步骤"""
        self._logger.info(f"[Step {step_num}] {message}")

    def pass_(self, message: str):
        """记录测试通过"""
        self._logger.success(f"[PASS] {message}")

    def fail(self, message: str):
        """记录测试失败"""
        self._logger.error(f"[FAIL] {message}")

    def warn(self, message: str):
        """记录警告"""
        self._logger.warning(f"[WARN] {message}")

    def debug(self, message: str):
        """记录调试信息"""
        self._logger.debug(f"[DEBUG] {message}")

    def info(self, message: str):
        """记录普通信息"""
        self._logger.info(message)

    def error(self, message: str):
        """记录错误"""
        self._logger.error(message)

    def section(self, title: str):
        """记录分节标题"""
        self._logger.info("=" * 50)
        self._logger.info(title)
        self._logger.info("=" * 50)

    def result(self, passed: int, total: int):
        """记录测试结果汇总"""
        self._logger.info("-" * 50)
        self._logger.info(f"测试结果: 通过 {passed}/{total}")
        self._logger.info("-" * 50)


_default_logger = None


def init_default_logger(log_dir: str = "logs", level: str = "INFO"):
    """初始化默认日志器"""
    global _default_logger
    _default_logger = TestLogger(log_dir, level)
    return _default_logger


def get_default_logger():
    """获取默认日志器"""
    global _default_logger
    if _default_logger is None:
        _default_logger = TestLogger()
    return _default_logger