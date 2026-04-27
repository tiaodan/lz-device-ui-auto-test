"""
UI异常场景视觉测试
通过JavaScript注入模拟前端界面异常
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from playwright.sync_api import sync_playwright
from config.config_loader import get_config
from pages.login_page import LoginPage
from visual_test.base import VisualTest
from utils.ssl_handler import safe_navigate


class UIAnomalySimulator:
    """UI异常模拟器 - 通过JS注入模拟前端界面异常"""

    def __init__(self, page):
        self.page = page

    # ==================== 样式异常 ====================

    def hide_element(self, selector: str):
        """隐藏元素"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) el.style.display = 'none';
            }}
        """)
        print(f"[UI异常] 隐藏元素: {selector}")

    def break_element_position(self, selector: str):
        """破坏元素定位（位置错乱）"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.style.position = 'absolute';
                    el.style.left = Math.random() * 100 + 'px';
                    el.style.top = Math.random() * 100 + 'px';
                    el.style.transform = 'rotate(' + Math.random() * 30 + 'deg)';
                }}
            }}
        """)
        print(f"[UI异常] 位置错乱: {selector}")

    def break_element_style(self, selector: str):
        """破坏元素样式（颜色/字体异常）"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.style.backgroundColor = '#ff0000';
                    el.style.color = '#0000ff';
                    el.style.fontSize = '5px';
                    el.style.border = '10px dashed yellow';
                }}
            }}
        """)
        print(f"[UI异常] 样式异常: {selector}")

    def overflow_text(self, selector: str):
        """文字溢出"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.value = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA';
                    el.style.width = '50px';
                }}
            }}
        """)
        print(f"[UI异常] 文字溢出: {selector}")

    # ==================== 功能异常 ====================

    def disable_button(self, selector: str):
        """禁用按钮"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.disabled = true;
                    el.style.opacity = '0.5';
                    el.style.cursor = 'not-allowed';
                }}
            }}
        """)
        print(f"[UI异常] 禁用按钮: {selector}")

    def break_input(self, selector: str):
        """破坏输入框（无法输入）"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.readOnly = true;
                    el.style.backgroundColor = '#ddd';
                    el.value = 'ERROR: Input Disabled';
                }}
            }}
        """)
        print(f"[UI异常] 输入框失效: {selector}")

    def break_slider(self, selector: str):
        """破坏滑块（无法拖动）"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.style.pointerEvents = 'none';
                    el.style.opacity = '0.3';
                }}
            }}
        """)
        print(f"[UI异常] 滑块失效: {selector}")

    # ==================== 图片异常 ====================

    def break_image(self, selector: str):
        """图片加载失败"""
        self.page.evaluate(f"""
            () => {{
                const el = document.querySelector('{selector}');
                if (el) {{
                    el.src = 'data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg"><rect fill="red" width="100%" height="100%"/><text x="50%" y="50%" fill="white" text-anchor="middle">IMG ERROR</text></svg>';
                    el.alt = 'Image Load Failed';
                }}
            }}
        """)
        print(f"[UI异常] 图片加载失败: {selector}")

    # ==================== 响应式异常 ====================

    def simulate_mobile_view(self):
        """模拟移动端视图（布局错乱）"""
        self.page.evaluate("""
            () => {
                const style = document.createElement('style');
                style.textContent = `
                    body { width: 375px; }
                    .isoSignInForm, .page-signin-form { transform: scale(0.5); }
                    #username, #password { width: 50%; }
                    .lBtn { width: 100px; }
                `;
                document.head.appendChild(style);
            }
        """)
        print("[UI异常] 模拟移动端视图")

    # ==================== 综合异常 ====================

    def inject_error_overlay(self, message: str = "UI ERROR"):
        """注入错误遮罩层"""
        self.page.evaluate(f"""
            () => {{
                const overlay = document.createElement('div');
                overlay.style.cssText = 'position:fixed;top:0;left:0;width:100%;height:100%;background:rgba(255,0,0,0.3);z-index:9999;display:flex;justify-content:center;align-items:center;font-size:48px;color:white;';
                overlay.textContent = '{message}';
                document.body.appendChild(overlay);
            }}
        """)
        print(f"[UI异常] 注入错误遮罩: {message}")


# ==================== 测试用例 ====================

def test_ui_element_hidden():
    """测试：登录按钮被隐藏"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: UI异常视觉测试")
    print("测试场景: 登录按钮被隐藏")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )
        simulator = UIAnomalySimulator(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # ==================== Step 1: 正常状态基准图 ====================
        print("\n[Step 1] 检查/创建正常状态基准图")
        if not visual.has_baseline("login_normal_state"):
            print("  [首次运行] 创建基准图")
            visual.save_baseline("login_normal_state")
        else:
            print("  [已有基准图] 使用现有基准图")

        # ==================== Step 2: 截取当前正常状态并对比 ====================
        print("\n[Step 2] 截取当前正常状态")
        visual.take_screenshot("login_normal_state")

        print("\n[对比] 正常状态与基准图对比")
        normal_cmp = visual.compare_images("login_normal_state")
        if normal_cmp["match"]:
            print(f"  [PASS] 正常状态一致，差异 {normal_cmp['diff_percent']}%")
        else:
            print(f"  [WARN] 正常状态有差异 {normal_cmp['diff_percent']}%")

        # ==================== Step 3: 模拟异常 ====================
        print("\n[Step 3] 模拟UI异常：隐藏登录按钮")
        simulator.hide_element(".lBtn")
        page.wait_for_timeout(300)

        # ==================== Step 4: 截取异常状态 ====================
        print("\n[Step 4] 截取异常状态")
        visual.take_screenshot("login_button_hidden")

        # ==================== Step 5: 异常状态与正常基准对比 ====================
        print("\n[对比] 异常状态与正常基准图对比")
        # 这里对比的是异常状态和正常状态，应该有明显差异
        # 使用正常状态基准图作为参照
        anomaly_cmp = visual.compare_with_baseline("login_button_hidden", "login_normal_state")
        if anomaly_cmp and anomaly_cmp["diff_percent"] > 5:  # 异常应该有明显差异
            print(f"  [PASS] 异常检测成功，差异 {anomaly_cmp['diff_percent']}%（预期有明显差异）")
        else:
            print(f"  [WARN] 异常差异较小 {anomaly_cmp['diff_percent']}%")

        # ==================== Step 6: 验证按钮确实被隐藏 ====================
        print("\n[Step 6] 验证异常生效")
        button_visible = page.locator(".lBtn").is_visible()
        if not button_visible:
            print("[PASS] 登录按钮已被隐藏")
        else:
            print("[FAIL] 登录按钮仍然可见")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 登录按钮隐藏测试通过")
    else:
        print("[FAIL] 测试失败")
    print("="*50)

    return result


def test_ui_input_style_broken():
    """测试：输入框样式异常"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: UI异常视觉测试")
    print("测试场景: 输入框样式异常")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )
        simulator = UIAnomalySimulator(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # 正常状态截图
        print("\n[Step 1] 截取正常状态")
        visual.take_screenshot("login_inputs_normal")

        # 模拟异常：破坏输入框样式
        print("\n[Step 2] 模拟UI异常：输入框样式异常")
        simulator.break_element_style("#username")
        simulator.break_element_style("#password")
        page.wait_for_timeout(300)

        # 异常状态截图
        print("\n[Step 3] 截取异常状态")
        visual.take_screenshot("login_inputs_style_broken")
        visual.take_element_screenshot("username_broken_style", "#username")
        visual.take_element_screenshot("password_broken_style", "#password")

        # 验证样式确实改变
        print("\n[Step 4] 验证异常生效")
        username_bg = page.locator("#username").evaluate("el => el.style.backgroundColor")
        if username_bg == "#ff0000" or "rgb(255, 0, 0)" in username_bg:
            print("[PASS] 用户名输入框样式已改变")
        else:
            print("[FAIL] 用户名输入框样式未改变")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 输入框样式异常测试通过")
    else:
        print("[FAIL] 测试失败")
    print("="*50)

    return result


def test_ui_button_disabled():
    """测试：登录按钮被禁用"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: UI异常视觉测试")
    print("测试场景: 登录按钮被禁用")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )
        simulator = UIAnomalySimulator(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # 正常状态截图
        print("\n[Step 1] 截取正常状态")
        visual.take_screenshot("login_button_normal")
        visual.take_element_screenshot("login_button_enabled", ".lBtn")

        # 模拟异常：禁用登录按钮
        print("\n[Step 2] 模拟UI异常：禁用登录按钮")
        simulator.disable_button(".lBtn")
        page.wait_for_timeout(300)

        # 异常状态截图
        print("\n[Step 3] 截取异常状态")
        visual.take_screenshot("login_button_disabled")
        visual.take_element_screenshot("login_button_disabled_state", ".lBtn")

        # 验证按钮确实被禁用
        print("\n[Step 4] 验证异常生效")
        button_disabled = page.locator(".lBtn").evaluate("el => el.disabled")
        button_opacity = page.locator(".lBtn").evaluate("el => el.style.opacity")
        if button_disabled:
            print(f"[PASS] 登录按钮已禁用, opacity={button_opacity}")
        else:
            print("[FAIL] 登录按钮未禁用")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 登录按钮禁用测试通过")
    else:
        print("[FAIL] 测试失败")
    print("="*50)

    return result


def test_ui_slider_broken():
    """测试：滑块功能失效"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: UI异常视觉测试")
    print("测试场景: 滑块功能失效")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )
        simulator = UIAnomalySimulator(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # 正常状态截图
        print("\n[Step 1] 截取正常状态")
        visual.take_screenshot("slider_normal_state")
        visual.take_element_screenshot("slider_enabled", ".drag, .page-slide-wrap")

        # 模拟异常：禁用滑块
        print("\n[Step 2] 模拟UI异常：滑块失效")
        simulator.break_slider(".drag, .page-slide-wrap")
        page.wait_for_timeout(300)

        # 异常状态截图
        print("\n[Step 3] 截取异常状态")
        visual.take_screenshot("slider_broken_state")
        visual.take_element_screenshot("slider_disabled", ".drag, .page-slide-wrap")

        # 验证滑块确实失效
        print("\n[Step 4] 验证异常生效")
        slider_opacity = page.locator(".drag, .page-slide-wrap").evaluate("el => el.style.opacity")
        if slider_opacity == "0.3":
            print("[PASS] 滑块已失效, opacity=0.3")
        else:
            print("[FAIL] 滑块未失效")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 滑块失效测试通过")
    else:
        print("[FAIL] 测试失败")
    print("="*50)

    return result


def test_ui_element_position_broken():
    """测试：元素位置错乱"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: UI异常视觉测试")
    print("测试场景: 元素位置错乱")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )
        simulator = UIAnomalySimulator(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # 正常状态截图
        print("\n[Step 1] 截取正常状态")
        visual.take_screenshot("login_layout_normal")

        # 模拟异常：位置错乱
        print("\n[Step 2] 模拟UI异常：元素位置错乱")
        simulator.break_element_position("#username")
        simulator.break_element_position("#password")
        simulator.break_element_position(".lBtn")
        page.wait_for_timeout(300)

        # 异常状态截图
        print("\n[Step 3] 截取异常状态")
        visual.take_screenshot("login_layout_broken")

        # 验证位置确实改变
        print("\n[Step 4] 验证异常生效")
        username_position = page.locator("#username").evaluate("el => el.style.position")
        if username_position == "absolute":
            print("[PASS] 元素位置已改变为absolute")
        else:
            print("[FAIL] 元素位置未改变")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 元素位置错乱测试通过")
    else:
        print("[FAIL] 测试失败")
    print("="*50)

    return result


def test_ui_text_overflow():
    """测试：文字溢出"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: UI异常视觉测试")
    print("测试场景: 文字溢出")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )
        simulator = UIAnomalySimulator(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # 正常状态截图
        print("\n[Step 1] 截取正常状态")
        visual.take_screenshot("login_text_normal")

        # 模拟异常：文字溢出
        print("\n[Step 2] 模拟UI异常：文字溢出")
        simulator.overflow_text("#username")
        page.wait_for_timeout(300)

        # 异常状态截图
        print("\n[Step 3] 截取异常状态")
        visual.take_screenshot("login_text_overflow")
        visual.take_element_screenshot("username_overflow", "#username")

        # 验证文字溢出
        print("\n[Step 4] 验证异常生效")
        username_width = page.locator("#username").evaluate("el => el.style.width")
        if username_width == "50px":
            print("[PASS] 输入框宽度已缩小，文字溢出")
        else:
            print("[FAIL] 输入框宽度未改变")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 文字溢出测试通过")
    else:
        print("[FAIL] 测试失败")
    print("="*50)

    return result


def test_ui_comprehensive_anomaly():
    """测试：综合UI异常"""

    config = get_config(reload=True)
    config.ensure_directories()

    print("\n" + "="*50)
    print("测试类型: UI异常视觉测试")
    print("测试场景: 综合UI异常")
    print("="*50)

    result = True

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        context = browser.new_context(ignore_https_errors=config.ignore_ssl_errors)
        page = context.new_page()

        login_page = LoginPage(page)
        visual = VisualTest(
            page,
            baseline_path=config.baseline_path,
            current_path=config.current_path,
            diff_path=config.diff_path,
            threshold=config.visual_threshold
        )
        simulator = UIAnomalySimulator(page)

        safe_navigate(page, config.base_url)
        page.wait_for_timeout(1000)

        # 正常状态截图
        print("\n[Step 1] 截取正常状态")
        visual.take_screenshot("login_comprehensive_normal")

        # 模拟多个异常
        print("\n[Step 2] 模拟综合UI异常")
        simulator.break_element_style("#username")
        simulator.disable_button(".lBtn")
        simulator.break_slider(".drag, .page-slide-wrap")
        simulator.inject_error_overlay("UI ANOMALY TEST")
        page.wait_for_timeout(500)

        # 异常状态截图
        print("\n[Step 3] 截取异常状态")
        visual.take_screenshot("login_comprehensive_anomaly")

        # 验证异常生效
        print("\n[Step 4] 验证综合异常生效")
        anomalies_detected = 0

        # 检查输入框样式
        username_bg = page.locator("#username").evaluate("el => el.style.backgroundColor")
        if username_bg and ("#ff0000" in username_bg or "rgb(255" in username_bg):
            anomalies_detected += 1
            print("  [OK] 输入框样式异常")

        # 检查按钮禁用
        button_disabled = page.locator(".lBtn").evaluate("el => el.disabled")
        if button_disabled:
            anomalies_detected += 1
            print("  [OK] 按钮已禁用")

        # 检查滑块失效
        slider_opacity = page.locator(".drag, .page-slide-wrap").evaluate("el => el.style.opacity")
        if slider_opacity == "0.3":
            anomalies_detected += 1
            print("  [OK] 滑块已失效")

        # 检查错误遮罩
        overlay_exists = page.locator("body > div:last-child").count() > 0
        if overlay_exists:
            anomalies_detected += 1
            print("  [OK] 错误遮罩已注入")

        print(f"\n共检测到 {anomalies_detected} 个异常")
        if anomalies_detected >= 3:
            print("[PASS] 综合异常测试通过")
        else:
            print("[FAIL] 异常数量不足")
            result = False

        browser.close()

    print("\n" + "="*50)
    if result:
        print("[PASS] 综合UI异常测试通过")
    else:
        print("[FAIL] 测试失败")
    print("="*50)

    return result


def run_all_ui_anomaly_tests():
    """运行所有UI异常测试"""

    print("\n" + "="*60)
    print("运行UI异常视觉测试")
    print("="*60)

    tests = [
        ("登录按钮被隐藏", test_ui_element_hidden),
        ("输入框样式异常", test_ui_input_style_broken),
        ("登录按钮被禁用", test_ui_button_disabled),
        ("滑块功能失效", test_ui_slider_broken),
        ("元素位置错乱", test_ui_element_position_broken),
        ("文字溢出", test_ui_text_overflow),
        ("综合UI异常", test_ui_comprehensive_anomaly),
    ]

    results = []
    for name, test_func in tests:
        try:
            passed = test_func()
            results.append((name, passed))
        except Exception as e:
            print(f"[ERROR] {name}: {e}")
            results.append((name, False))

    # 汇总
    print("\n" + "-"*60)
    print("测试结果汇总")
    print("-"*60)
    for name, passed in results:
        status = "[PASS]" if passed else "[FAIL]"
        print(f"{status} {name}")

    passed_count = sum(1 for _, p in results if p)
    print(f"\n通过: {passed_count}/{len(results)}")
    return passed_count == len(results)


if __name__ == "__main__":
    import sys
    test_name = sys.argv[1] if len(sys.argv) > 1 else "all"

    if test_name == "hidden":
        test_ui_element_hidden()
    elif test_name == "style":
        test_ui_input_style_broken()
    elif test_name == "disabled":
        test_ui_button_disabled()
    elif test_name == "slider":
        test_ui_slider_broken()
    elif test_name == "position":
        test_ui_element_position_broken()
    elif test_name == "overflow":
        test_ui_text_overflow()
    elif test_name == "comprehensive":
        test_ui_comprehensive_anomaly()
    elif test_name == "all":
        run_all_ui_anomaly_tests()
    else:
        print(f"未知测试: {test_name}")
        print("可用测试: hidden, style, disabled, slider, position, overflow, comprehensive, all")