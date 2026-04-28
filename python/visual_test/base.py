"""
图片识别测试基础模块
提供截图对比、视觉回归等功能
"""

import os
from playwright.sync_api import Page
from PIL import Image
from utils.test_logger import get_default_logger


class VisualTest:
    """图片识别测试基类"""

    def __init__(
        self,
        page: Page,
        baseline_path: str = "screenshots/baseline",
        current_path: str = "screenshots/current",
        diff_path: str = "screenshots/diff",
        threshold: float = 0.1
    ):
        self.logger = get_default_logger()
        self.page = page
        self.baseline_path = baseline_path
        self.current_path = current_path
        self.diff_path = diff_path
        self.threshold = threshold

        os.makedirs(baseline_path, exist_ok=True)
        os.makedirs(current_path, exist_ok=True)
        os.makedirs(diff_path, exist_ok=True)

    # ==================== 截图方法 ====================

    def take_screenshot(self, name: str, full_page: bool = False) -> str:
        """截图"""
        path = f"{self.current_path}/{name}.png"
        self.page.screenshot(path=path, full_page=full_page)
        self.logger.info(f"截图保存: {path}")
        return path

    def take_element_screenshot(self, name: str, selector: str) -> str:
        """元素截图"""
        element = self.page.locator(selector)
        path = f"{self.current_path}/{name}.png"
        element.screenshot(path=path)
        self.logger.info(f"元素截图保存: {path}")
        return path

    def take_region_screenshot(self, name: str, x: int, y: int, width: int, height: int) -> str:
        """区域截图"""
        path = f"{self.current_path}/{name}.png"
        self.page.screenshot(
            path=path,
            clip={"x": x, "y": y, "width": width, "height": height}
        )
        self.logger.info(f"区域截图保存: {path}")
        return path

    # ==================== 基准图管理 ====================

    def save_baseline(self, name: str, full_page: bool = False) -> str:
        """保存基准图"""
        path = f"{self.baseline_path}/{name}.png"
        self.page.screenshot(path=path, full_page=full_page)
        self.logger.info(f"基准图保存: {path}")
        return path

    def has_baseline(self, name: str) -> bool:
        """检查基准图是否存在"""
        return os.path.exists(f"{self.baseline_path}/{name}.png")

    def get_baseline_path(self, name: str) -> str:
        """获取基准图路径"""
        return f"{self.baseline_path}/{name}.png"

    def update_baseline(self, name: str):
        """更新基准图"""
        current = f"{self.current_path}/{name}.png"
        baseline = f"{self.baseline_path}/{name}.png"
        if os.path.exists(current):
            Image.open(current).save(baseline)
            self.logger.pass_(f"基准图已更新: {baseline}")

    # ==================== 图片对比 ====================

    def compare_images(self, name: str) -> dict:
        """对比图片"""
        baseline_file = f"{self.baseline_path}/{name}.png"
        current_file = f"{self.current_path}/{name}.png"
        diff_file = f"{self.diff_path}/{name}.png"

        return self._do_compare(baseline_file, current_file, diff_file)

    def compare_with_baseline(self, current_name: str, baseline_name: str) -> dict:
        """对比当前截图与指定基准图"""
        baseline_file = f"{self.baseline_path}/{baseline_name}.png"
        current_file = f"{self.current_path}/{current_name}.png"
        diff_file = f"{self.diff_path}/{current_name}_vs_{baseline_name}.png"

        return self._do_compare(baseline_file, current_file, diff_file)

    def _do_compare(self, baseline_file: str, current_file: str, diff_file: str) -> dict:

        if not os.path.exists(baseline_file):
            self.logger.fail(f"基准图不存在: {baseline_file}")
            return {"match": False, "error": "baseline_not_found"}

        if not os.path.exists(current_file):
            self.logger.fail(f"当前截图不存在: {current_file}")
            return {"match": False, "error": "current_not_found"}

        baseline_img = Image.open(baseline_file)
        current_img = Image.open(current_file)

        if baseline_img.size != current_img.size:
            self.logger.fail(f"图片尺寸不同: {baseline_img.size} vs {current_img.size}")
            return {"match": False, "error": "size_mismatch"}

        baseline_pixels = baseline_img.load()
        current_pixels = current_img.load()
        width, height = baseline_img.size

        diff_pixels = 0
        total_pixels = width * height

        diff_img = Image.new("RGB", (width, height))
        diff_pixels_img = diff_img.load()

        for x in range(width):
            for y in range(height):
                bp = baseline_pixels[x, y]
                cp = current_pixels[x, y]

                if not self._pixels_similar(bp, cp):
                    diff_pixels += 1
                    diff_pixels_img[x, y] = (255, 0, 0)
                else:
                    diff_pixels_img[x, y] = cp

        diff_percent = (diff_pixels / total_pixels) * 100

        if diff_pixels > 0:
            diff_img.save(diff_file)
            self.logger.info(f"差异图保存: {diff_file}")

        match = diff_percent <= self.threshold * 100

        result = {
            "match": match,
            "diff_percent": round(diff_percent, 2),
            "diff_pixels": diff_pixels,
            "total_pixels": total_pixels,
            "baseline_path": baseline_file,
            "current_path": current_file,
            "diff_path": diff_file if diff_pixels > 0 else None
        }

        if match:
            self.logger.pass_(f"图片匹配，差异 {diff_percent:.2f}%")
        else:
            self.logger.fail(f"图片不匹配，差异 {diff_percent:.2f}%")

        return result

    def _pixels_similar(self, p1: tuple, p2: tuple, tolerance: int = 10) -> bool:
        """比较两个像素是否相似"""
        if len(p1) >= 3 and len(p2) >= 3:
            r_diff = abs(p1[0] - p2[0])
            g_diff = abs(p1[1] - p2[1])
            b_diff = abs(p1[2] - p2[2])
            return r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance
        return p1 == p2

    # ==================== 测试流程 ====================

    def visual_test(self, name: str, auto_update: bool = False) -> bool:
        """执行视觉测试流程"""
        self.take_screenshot(name)

        if not self.has_baseline(name):
            if auto_update:
                self.update_baseline(name)
                self.logger.pass_(f"自动创建基准图: {name}")
                return True
            else:
                self.logger.fail("无基准图，请先创建基准图")
                return False

        result = self.compare_images(name)

        if not result["match"] and auto_update:
            self.update_baseline(name)
            self.logger.pass_("基准图已自动更新")
            return True

        return result["match"]