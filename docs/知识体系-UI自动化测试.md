# UI 自动化测试 - 知识体系

以 `lz-device-ui-auto-test` 项目为例，演示"道→骨架→枝叶→产出"体系。

---

## 一、道（核心规律）

### 1. UI 自动化测试的本质

```
用户操作 → 系统响应 → 结果验证
```

**核心循环：**
1. 模拟用户操作（点击、输入、拖动）
2. 等待系统响应
3. 验证结果是否符合预期

### 2. 三种测试类型的本质

| 类型 | 验证什么 | 本质 |
|------|---------|------|
| **断言测试** | 元素、文本、属性 | 验证"存在性和正确性" |
| **视觉测试** | 截图对比 | 验证"外观一致性" |
| **接口测试** | API 返回数据 | 验证"数据一致性" |

### 3. Page Object Model 的本质

```
页面 = 状态 + 操作 + 验证
```

- **状态**：定位器（元素在哪里）
- **操作**：方法（能做什么）
- **验证**：断言（结果应该是什么）

### 4. 配置分离的本质

```
代码 = 逻辑 + 数据
```

- **逻辑**：不变的部分（测试流程）
- **数据**：可变的部分（URL、账号、定位器、期望值）

---

## 二、骨架（标准流程）

### 1. 从需求到测试用例的流程

```
需求分析
    ↓
【拆解】这是什么类型的测试？
    ├── 登录流程 → 断言测试 + 接口测试
    ├── 页面布局 → 视觉测试
    └── 数据展示 → 接口测试（UI vs API）
    ↓
【设计】测试步骤是什么？
    ├── 前置条件（已登录/未登录）
    ├── 操作步骤（填写、点击、等待）
    └── 验证点（元素可见、文本正确、数据一致）
    ↓
【实现】用什么模式？
    ├── Page Object：封装页面操作
    ├── Fixture：管理测试环境
    └── Config：管理测试数据
    ↓
【执行】运行测试
    ↓
【复盘】哪里失败？为什么？
```

### 2. pytest + playwright 的标准骨架

```
conftest.py          # 全局配置、fixtures
    ↓
pages/               # 页面对象
    ↓
tests/               # 测试用例
    ├── assertion/   # 断言测试
    ├── visual/      # 视觉测试
    └── api/         # 接口测试
    ↓
config/              # 配置文件
```

### 3. 测试用例的标准结构

```python
def test_xxx(page, login_page, config):
    # 1. 前置（fixture 已处理）
    
    # 2. 操作
    login_page.fill_credentials(username, password)
    login_page.click_login()
    
    # 3. 验证
    expect(page).to_have_url(config.base_url + "/home")
    
    # 4. 清理（fixture 自动处理）
```

---

## 三、枝叶（知识库）

### 问题类型 → 方案映射

#### 1. "我要测试元素是否存在"

| 方案 | API | 示例 |
|------|-----|------|
| 元素可见 | `expect(locator).to_be_visible()` | 断言按钮显示 |
| 元素存在 | `expect(locator).to_be_attached()` | 断言 DOM 中存在 |
| 元素隐藏 | `expect(locator).not_to_be_visible()` | 断言弹窗消失 |

#### 2. "我要测试文本是否正确"

| 方案 | API | 示例 |
|------|-----|------|
| 精确匹配 | `expect(locator).to_have_text("登录")` | 按钮文字 |
| 包含匹配 | `expect(locator).to_contain_text("登录")` | 提示信息 |
| 输入值 | `expect(locator).to_have_value("root")` | 输入框内容 |

#### 3. "我要模拟用户操作"

| 方案 | API | 示例 |
|------|-----|------|
| 点击 | `locator.click()` | 点击按钮 |
| 填写 | `locator.fill("text")` | 输入文字 |
| 悬停 | `locator.hover()` | 鼠标悬停 |
| 拖动 | `locator.drag_to(target)` | 拖动元素 |

#### 4. "我要等待某个状态"

| 方案 | API | 示例 |
|------|-----|------|
| 等待可见 | `locator.wait_for(state="visible")` | 等弹窗出现 |
| 等待消失 | `locator.wait_for(state="hidden")` | 等加载消失 |
| 固定等待 | `page.wait_for_timeout(1000)` | 调试用 |

#### 5. "我要处理滑块验证码"

```python
# 方案：模拟鼠标拖动事件
page.evaluate("""() => {
    const btn = document.querySelector('.drag .btn');
    // 触发 mousedown → mousemove → mousemouseup
    btn.dispatchEvent(new MouseEvent('mousedown', {...}));
    // 分步移动
    for (let i = 1; i <= steps; i++) {
        document.dispatchEvent(new MouseEvent('mousemove', {...}));
    }
    document.dispatchEvent(new MouseEvent('mouseup', {...}));
}""")
```

#### 6. "我要做多语言测试"

| 方案 | 实现 |
|------|-----|
| 切换语言 | 配置文件按语言分离：`zh_CN.yaml`, `en_US.yaml` |
| 注入语言 | `context.add_init_script("localStorage.setItem('locale', 'zh_CN')")` |
| 验证文案 | 从配置读取期望值：`expect(locator).to_contain_text(config["button_text"])` |

#### 7. "我要做接口测试"

| 方案 | 实现 |
|------|-----|
| GraphQL 查询 | `client._execute(query_string)` |
| Token 管理 | 缓存到文件，过期自动重新登录 |
| 数据一致性 | UI 显示数量 vs API 返回数量 |

---

### 常用 API 速查

#### Playwright 核心

```python
# 定位元素
page.locator(".class")           # CSS 选择器
page.locator("#id")              # ID 选择器
page.locator("text=登录")        # 文本选择器
page.locator("[data-test='btn']") # 属性选择器

# 操作
locator.click()                  # 点击
locator.fill("text")             # 填写
locator.hover()                  # 悬停
locator.drag_to(target)          # 拖动

# 等待
locator.wait_for(state="visible")
page.wait_for_timeout(1000)
page.wait_for_load_state("networkidle")

# 断言
expect(locator).to_be_visible()
expect(locator).to_have_text("文本")
expect(locator).to_have_attribute("placeholder", "用户名")
expect(page).to_have_url("https://xxx")
```

#### pytest 核心

```python
# fixture 定义
@pytest.fixture(scope="session")  # 全局一次
@pytest.fixture(scope="function") # 每个测试一次

# fixture 使用
def test_xxx(page, config):       # 直接注入

# 标记
@pytest.mark.skip("原因")
@pytest.mark.slow
```

---

### 踩坑记录

| 坑 | 原因 | 解决 |
|----|------|------|
| SSL 证书错误 | 测试环境自签名证书 | `ignore_https_errors=True` |
| 点击不触发 | Playwright click() 有时无效 | 用 JS 点击 `page.evaluate("...click()")` |
| 滑块拖动失败 | 简单 drag_to 不触发验证 | 模拟完整鼠标事件序列 |
| 语言不切换 | 页面加载后才设置 | 用 `add_init_script` 提前注入 |
| Token 过期 | 缓存时间太长 | 检测过期自动重新登录 |

---

## 四、产出（成果）

### 1. 项目本身

```
lz-device-ui-auto-test/
├── python/           # Python 实现
│   ├── pages/        # 页面对象（可复用）
│   ├── graphql/      # API 客户端（可复用）
│   ├── config/       # 配置模板（可复用）
│   └── conftest.py   # pytest 配置（可复用）
├── go/               # Go 实现（备用）
└── docs/             # 知识文档
```

### 2. 可复用的产出

| 产出 | 价值 |
|------|------|
| `LoginPage` 类 | 其他项目可直接复制修改 |
| `GraphQLClient` 类 | GraphQL 项目通用 |
| `AssertionTest` 类 | 断言测试通用封装 |
| `conftest.py` 模板 | pytest fixture 标准配置 |
| 配置文件结构 | 多语言、多环境支持模板 |

### 3. 从项目提炼的模板

#### 页面对象模板

```python
class XxxPage:
    def __init__(self, page: Page, language: str = "zh_CN"):
        self.page = page
        self._language = language
        self._config = get_module_config("xxx")
        # 从配置初始化定位器
        self.xxx_button = page.locator(self._config["locators"]["xxx"])
    
    def do_something(self):
        """操作方法"""
        self.xxx_button.click()
    
    def verify_xxx(self):
        """验证方法"""
        expect(self.xxx_button).to_be_visible()
```

#### GraphQL 客户端模板

```python
class GraphQLClient:
    def __init__(self, base_url: str):
        self.base_url = base_url
        self.session = requests.Session()
        self._load_cached_token()
    
    def login(self, username: str, password: str):
        # 登录获取 Token，缓存
    
    def _execute(self, query: str):
        # 执行查询，处理过期
```

---

## 五、复盘总结

### 这个项目验证了哪些"道"？

1. **问题拆解**：登录测试 → 断言 + 滑块 + 接口
2. **模式识别**：Page Object + Fixture + Config 分离
3. **抽象思维**：三种测试类型各有基类
4. **概率匹配**：遇到滑块 → 模拟鼠标事件序列

### 下次遇到类似项目

```
问：要做 UI 自动化测试
答：
    1. 选框架：Playwright（现代首选）
    2. 定类型：断言/视觉/接口
    3. 设计结构：pages/tests/config
    4. 复用模板：conftest.py、Page 类、Client 类
```

---

## 六、知识库索引

| 问题类型 | 查什么 |
|---------|-------|
| 元素定位 | `page.locator()` |
| 元素操作 | `click()`, `fill()`, `drag_to()` |
| 等待策略 | `wait_for()`, `wait_for_timeout()` |
| 断言方法 | `expect(locator).to_xxx()` |
| 多语言处理 | 配置分离 + `add_init_script` |
| 特殊交互 | 滑块：模拟鼠标事件序列 |
| API 测试 | GraphQL 客户端 + Token 管理 |
| pytest fixture | `conftest.py` + `@pytest.fixture` |