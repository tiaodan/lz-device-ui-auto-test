# pytest 框架说明

## 概述

项目已完成 pytest + loguru 改造，从原有的自定义框架迁移到标准 pytest 结构。

## 改造内容

### 新增文件

| 文件 | 说明 |
|-----|------|
| `pyproject.toml` | pytest 配置文件 |
| `conftest.py` | 全局 fixtures 和 hooks |
| `utils/test_logger.py` | loguru 日志器 |
| `assertion_test/conftest.py` | 断言测试 fixtures |
| `visual_test/conftest.py` | 视觉测试 fixtures |
| `api_test/conftest.py` | API测试 fixtures |

### 删除文件

| 文件 | 原因 |
|-----|------|
| `utils/logger.py` | 被 loguru 替代 |
| `run_tests.py` | 被 pytest 命令替代 |

### 改造要点

**测试文件改造模板**：

删除：
- 浏览器启动代码块 (`with sync_playwright() as p...`)
- 配置初始化代码 (`config = get_config(reload=True)...`)
- `if __name__ == "__main__"` 块
- `sys.path.insert` 语句

添加：
- `@pytest.mark.assertion/visual/api` 装饰器
- 使用 fixture 参数 (`page`, `login_page`, `config`, `test_logger`)

**改造前后对比**：

```python
# 改造前
def test_login_ok():
    config = get_config(reload=True)
    logger = init_default_logger()
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=config.headless)
        page = browser.new_context().new_page()
        login_page = LoginPage(page)
        # ... 测试逻辑 ...
        browser.close()

# 改造后
@pytest.mark.assertion
def test_login_ok(page, login_page, config, test_logger):
    # ... 测试逻辑 ...
```

## pytest 配置 (pyproject.toml)

```toml
[tool.pytest.ini_options]
testpaths = ["assertion_test", "visual_test", "api_test"]
python_files = ["test_*.py", "*_ok.py", "*_error*.py"]
python_functions = ["test_*"]
markers = [
    "assertion: Assertion tests",
    "visual: Visual tests",
    "api: API tests",
    "login: Login related tests",
    "slow: Slow running tests"
]
log_cli = true
log_cli_level = "INFO"
addopts = "-v --tb=short"
```

## 全局 Fixtures (conftest.py)

| Fixture | 级别 | 说明 |
|--------|------|-----|
| `config` | session | 配置对象 |
| `test_logger` | session | loguru 日志器 |
| `page` | function | Playwright page，自动导航登录页 |
| `login_page` | function | 登录页面对象 |
| `assertion_test` | function | 断言测试基类 |
| `visual_test` | function | 视觉测试基类 |
| `api_test` | function | API测试基类 |
| `logged_in_page` | function | 已登录的 page |

## pytest Hooks

```python
# pytest_configure - 注册 markers
def pytest_configure(config):
    config.addinivalue_line("markers", "assertion: ...")

# pytest_runtest_makereport - 失败自动截图
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # 测试失败时自动截图到 screenshots/failures/
```

## loguru 日志器

替代原有的 Python 标准 logging 模块。

**优势**：
- 配置更简洁
- 自动输出到控制台和文件
- 支持彩色输出
- 自动日志轮转和保留

**API兼容**：
```python
# utils/test_logger.py
class TestLogger:
    def step(self, step_num: int, message: str)  # 测试步骤
    def pass_(self, message: str)                # 通过
    def fail(self, message: str)                 # 失败
    def warn(self, message: str)                 # 警告
    def info(self, message: str)                 # 信息
    def section(self, title: str)                # 分节标题
    def result(self, passed: int, total: int)    # 结果汇总
```

## 测试发现

pytest 自动发现规则：
- 文件名：`test_*.py`, `*_ok.py`, `*_error*.py`
- 函数名：`test_*`
- 目录：`assertion_test/`, `visual_test/`, `api_test/`

当前项目共 **23 个测试**：
- assertion_test: 13 个
- visual_test: 4 个
- api_test: 6 个