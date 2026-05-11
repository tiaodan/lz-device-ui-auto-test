"""
最小 pytest 测试示例
使用 pytest + playwright 的最简结构
"""

import pytest
from playwright.sync_api import Page, expect


# ==================== 测试用例 ====================

def test_homepage_title(page):
    """测试首页标题"""
    page.goto("/")
    expect(page).to_have_title("系统名称")


def test_login_success(page):
    """测试登录成功"""
    # 操作
    page.locator(".username").fill("root")
    page.locator(".password").fill("password")
    page.locator(".login-btn").click()

    # 验证
    expect(page).to_have_url("/home")
    expect(page.locator(".user-info")).to_be_visible()


def test_login_error(page):
    """测试登录失败"""
    page.locator(".username").fill("wrong")
    page.locator(".password").fill("wrong")
    page.locator(".login-btn").click()

    expect(page.locator(".error-msg")).to_contain_text("用户名或密码错误")


# ==================== 运行方式 ====================

"""
# 运行所有测试
pytest test_minimal.py

# 运行单个测试
pytest test_minimal.py::test_login_success

# 显示详细输出
pytest test_minimal.py -v

# 失败时截图（在 pytest.ini 配置）
[pytest]
playwright_screenshot_on_failure = true
"""