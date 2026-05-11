"""
视觉测试模板
截图对比、视觉回归
"""

from playwright.sync_api import Page
import os
from PIL import Image
import pixelmatch  # 需要 pip install pixelmatch


class VisualTestTemplate:
    """视觉测试基类"""

    def __init__(self, page: Page,
                 baseline_path: str = "screenshots/baseline",
                 current_path: str = "screenshots/current",
                 diff_path: str = "screenshots/diff",
                 threshold: float = 0.1):
        self.page = page
        self.baseline_path = baseline_path
        self.current_path = current_path
        self.diff_path = diff_path
        self.threshold = threshold

        # 确保目录存在
        for path in [baseline_path, current_path, diff_path]:
            os.makedirs(path, exist_ok=True)

    # ==================== 截图 ====================

    def take_screenshot(self, name: str) -> str:
        """截图保存到 current 目录"""
        path = f"{self.current_path}/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        return path

    def take_element_screenshot(self, name: str, selector: str) -> str:
        """元素截图"""
        element = self.page.locator(selector)
        path = f"{self.current_path}/{name}.png"
        element.screenshot(path=path)
        return path

    # ==================== 对比 ====================

    def compare_images(self, name: str) -> dict:
        """对比截图与基准图"""
        baseline_file = f"{self.baseline_path}/{name}.png"
        current_file = f"{self.current_path}/{name}.png"
        diff_file = f"{self.diff_path}/{name}.png"

        # 如果没有基准图，创建基准图
        if not os.path.exists(baseline_file):
            self.page.screenshot(path=baseline_file, full_page=True)
            return {"status": "baseline_created", "diff_percent": 0}

        # 对比
        img1 = Image.open(baseline_file)
        img2 = Image.open(current_file)

        # 确保尺寸一致
        if img1.size != img2.size:
            img2 = img2.resize(img1.size)

        diff = Image.new("RGB", img1.size)
        diff_pixels = pixelmatch.pixelmatch(
            img1, img2, diff,
            threshold=self.threshold
        )

        total_pixels = img1.size[0] * img1.size[1]
        diff_percent = diff_pixels / total_pixels * 100

        # 保存差异图
        if diff_percent > 0:
            diff.save(diff_file)

        return {
            "status": "compared",
            "diff_percent": diff_percent,
            "diff_file": diff_file if diff_percent > 0 else None,
            "passed": diff_percent <= self.threshold * 100
        }

    # ==================== 基准图管理 ====================

    def create_baseline(self, name: str):
        """创建基准图"""
        path = f"{self.baseline_path}/{name}.png"
        self.page.screenshot(path=path, full_page=True)
        return path

    def update_baseline(self, name: str):
        """更新基准图（用当前截图覆盖）"""
        current_file = f"{self.current_path}/{name}.png"
        baseline_file = f"{self.baseline_path}/{name}.png"

        if os.path.exists(current_file):
            import shutil
            shutil.copy(current_file, baseline_file)
            return baseline_file
        return None

    # ==================== 验证 ====================

    def verify_visual(self, name: str, max_diff: float = None) -> bool:
        """验证视觉效果"""
        threshold = max_diff or self.threshold * 100

        self.take_screenshot(name)
        result = self.compare_images(name)

        if result["passed"]:
            print(f"✓ 视觉测试通过: {name}")
            return True
        else:
            print(f"✗ 视觉测试失败: {name}, 差异 {result['diff_percent']:.2f}%")
            return False


# ==================== 测试用例示例 ====================

"""
# test_visual.py

def test_login_page_visual(page, config):
    '''登录页视觉测试'''
    visual = VisualTestTemplate(page)

    # 导航
    page.goto(config.base_url)

    # 验证
    assert visual.verify_visual("login_page")

def test_button_visual(page):
    '''按钮视觉测试'''
    visual = VisualTestTemplate(page)

    # 元素截图
    visual.take_element_screenshot("submit_button", ".submit-btn")

    # 对比
    result = visual.compare_images("submit_button")
    assert result["passed"] or result["status"] == "baseline_created"
"""