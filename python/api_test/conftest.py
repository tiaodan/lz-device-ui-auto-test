"""
API 测试目录 pytest 配置
"""

import pytest


def pytest_collection_modifyitems(config, items):
    """为 API 测试添加 marker"""
    for item in items:
        if not any(marker.name in ["assertion", "visual", "api"] for marker in item.iter_markers()):
            item.add_marker(pytest.mark.api)