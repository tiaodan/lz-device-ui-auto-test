"""
图片识别测试基础模块
提供截图对比、视觉回归等功能
"""

from playwright.sync_api import Page
from PIL import Image
import os
import math


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
        self.page = page
        self.baseline_path = baseline_path
        self.current_path = current_path
        self.diff_path = diff_path
        self.threshold = threshold  # 差异容忍度

        # 确保目录存在
        os.makedirs(baseline_path, exist_ok=True)
        os.makedirs(current_path, exist_ok=True)
        os.makedirs(diff_path, exist_ok=True)

    # ==================== 截图方法 ====================

    def take_screenshot(self, name: str, full_page: bool = False) -> str:
        """截图"""
        path = f"{self.current_path}/{name}.png"
        self.page.screenshot(path=path, full_page=full_page)
        print(f"[VISUAL] 截图保存: {path}")
        return path

    def take_element_screenshot(self, name: str, selector: str) -> str:
        """元素截图"""
        element = self.page.locator(selector)
        path = f"{self.current_path}/{name}.png"
        element.screenshot(path=path)
        print(f"[VISUAL] 元素截图保存: {path}")
        return path

    def take_region_screenshot(self, name: str, x: int, y: int, width: int, height: int) -> str:
        """区域截图"""
        # 使用 clip 参数截图指定区域
        path = f"{self.current_path}/{name}.png"
        self.page.screenshot(
            path=path,
            clip={"x": x, "y": y, "width": width, "height": height}
        )
        print(f"[VISUAL] 区域截图保存: {path}")
        return path

    # ==================== 基准图管理 ====================

    def save_baseline(self, name: str, full_page: bool = False) -> str:
        """保存基准图"""
        path = f"{self.baseline_path}/{name}.png"
        self.page.screenshot(path=path, full_page=full_page)
        print(f"[VISUAL] 基准图保存: {path}")
        return path

    def has_baseline(self, name: str) -> bool:
        """检查基准图是否存在"""
        return os.path.exists(f"{self.baseline_path}/{name}.png")

    def get_baseline_path(self, name: str) -> str:
        """获取基准图路径"""
        return f"{self.baseline_path}/{name}.png"

    def update_baseline(self, name: str):
        """更新基准图（从当前截图）"""
        current = f"{self.current_path}/{name}.png"
        baseline = f"{self.baseline_path}/{name}.png"
        if os.path.exists(current):
            Image.open(current).save(baseline)
            print(f"[VISUAL] 基准图已更新: {baseline}")

    # ==================== 图片对比 ====================

    def compare_images(self, name: str) -> dict:
        """
        对比图片（当前截图与同名基准图对比）
        返回: {
            "match": bool,           # 是否匹配
            "diff_percent": float,   # 差异百分比
            "diff_pixels": int,      # 差异像素数
            "baseline_path": str,    # 基准图路径
            "current_path": str,     # 当前图路径
            "diff_path": str         # 差异图路径
        }
        """

        baseline_file = f"{self.baseline_path}/{name}.png"
        current_file = f"{self.current_path}/{name}.png"
        diff_file = f"{self.diff_path}/{name}.png"

        return self._do_compare(baseline_file, current_file, diff_file)

    def compare_with_baseline(self, current_name: str, baseline_name: str) -> dict:
        """
        对比当前截图与指定基准图（不同名称对比）
        用于：异常状态截图与正常状态基准图对比
        """
        baseline_file = f"{self.baseline_path}/{baseline_name}.png"
        current_file = f"{self.current_path}/{current_name}.png"
        diff_file = f"{self.diff_path}/{current_name}_vs_{baseline_name}.png"

        return self._do_compare(baseline_file, current_file, diff_file)

    def _do_compare(self, baseline_file: str, current_file: str, diff_file: str) -> dict:

        # 检查文件存在
        if not os.path.exists(baseline_file):
            print(f"[VISUAL] 基准图不存在: {baseline_file}")
            return {"match": False, "error": "baseline_not_found"}

        if not os.path.exists(current_file):
            print(f"[VISUAL] 当前截图不存在: {current_file}")
            return {"match": False, "error": "current_not_found"}

        # 加载图片
        baseline_img = Image.open(baseline_file)
        current_img = Image.open(current_file)

        # 检查尺寸
        if baseline_img.size != current_img.size:
            print(f"[VISUAL] 图片尺寸不同: {baseline_img.size} vs {current_img.size}")
            return {"match": False, "error": "size_mismatch"}

        # 对比像素
        baseline_pixels = baseline_img.load()
        current_pixels = current_img.load()
        width, height = baseline_img.size

        diff_pixels = 0
        total_pixels = width * height

        # 创建差异图
        diff_img = Image.new("RGB", (width, height))
        diff_pixels_img = diff_img.load()

        for x in range(width):
            for y in range(height):
                bp = baseline_pixels[x, y]
                cp = current_pixels[x, y]

                # 比较像素（允许小的颜色差异）
                if not self._pixels_similar(bp, cp):
                    diff_pixels += 1
                    # 差异像素标记为红色
                    diff_pixels_img[x, y] = (255, 0, 0)
                else:
                    # 相同像素保留原色
                    diff_pixels_img[x, y] = cp

        # 计算差异百分比
        diff_percent = (diff_pixels / total_pixels) * 100

        # 保存差异图
        if diff_pixels > 0:
            diff_img.save(diff_file)
            print(f"[VISUAL] 差异图保存: {diff_file}")

        # 判断是否匹配
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
            print(f"[VISUAL PASS] 图片匹配，差异 {diff_percent:.2f}%")
        else:
            print(f"[VISUAL FAIL] 图片不匹配，差异 {diff_percent:.2f}%")

        return result

    def _pixels_similar(self, p1: tuple, p2: tuple, tolerance: int = 10) -> bool:
        """比较两个像素是否相似"""
        # RGB 比较（允许一定误差）
        if len(p1) >= 3 and len(p2) >= 3:
            r_diff = abs(p1[0] - p2[0])
            g_diff = abs(p1[1] - p2[1])
            b_diff = abs(p1[2] - p2[2])
            return r_diff <= tolerance and g_diff <= tolerance and b_diff <= tolerance
        return p1 == p2

    # ==================== 测试流程 ====================

    def visual_test(self, name: str, auto_update: bool = False) -> bool:
        """
        执行视觉测试流程
        1. 截取当前图
        2. 与基准图对比（如果存在）
        3. 自动更新基准图（如果配置允许）
        """

        # 截取当前图
        self.take_screenshot(name)

        # 检查基准图
        if not self.has_baseline(name):
            if auto_update:
                self.update_baseline(name)
                print(f"[VISUAL] 自动创建基准图: {name}")
                return True
            else:
                print(f"[VISUAL] 无基准图，请先创建基准图")
                return False

        # 对比图片
        result = self.compare_images(name)

        # 如果不匹配且允许自动更新
        if not result["match"] and auto_update:
            self.update_baseline(name)
            print(f"[VISUAL] 基准图已自动更新")
            return True

        return result["match"]