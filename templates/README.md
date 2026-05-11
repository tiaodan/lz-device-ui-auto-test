# 模板代码使用指南

从 `lz-device-ui-auto-test` 项目提炼的可复用模板。

---

## 目录结构

```
templates/
├── page_object/               # 页面对象模板
│   ├── page_template.py       # 基础页面对象
│   └── multi_language_page_template.py  # 多语言支持
│
├── config/                    # 配置模板
│   ├── conftest_template.py   # pytest 全局配置
│   ├── config_loader_template.py  # 配置读取类
│   └── test_config_template.yaml    # 配置文件
│
├── tests/                     # 测试模板
│   ├── assertion_test_template.py   # 断言测试
│   └── visual_test_template.py      # 视觉测试
│
├── utils/                     # 工具模板
│   ├── graphql_client_template.py   # GraphQL 客户端
│   └── slider_handler_template.py   # 滑块验证码
│
└── demos/                     # 最小示例
    ├── minimal_login_test.py  # 最小登录测试
    └── minimal_pytest_test.py # 最小 pytest 示例
```

---

## 快速使用

### 1. 新建 UI 自动化测试项目

```bash
# 1. 复制模板目录
cp templates/ new-project/

# 2. 安装依赖
pip install playwright pytest pytest-playwright pyyaml pixelmatch pillow
playwright install chromium

# 3. 修改配置
# 编辑 config/test_config_template.yaml → test_config.yaml

# 4. 修改页面对象
# 复制 page_object/page_template.py → pages/xxx_page.py
# 修改定位器、操作方法

# 5. 编写测试
# 复制 tests/assertion_test_template.py → tests/test_xxx.py

# 6. 运行
pytest tests/
```

### 2. 模板对应场景

| 场景 | 使用模板 |
|------|---------|
| 基础页面测试 | `page_template.py` + `assertion_test_template.py` |
| 多语言测试 | `multi_language_page_template.py` + 语言配置文件 |
| 视觉回归测试 | `visual_test_template.py` |
| GraphQL 接口测试 | `graphql_client_template.py` |
| 滑块验证码 | `slider_handler_template.py` |
| 快速原型验证 | `demos/minimal_login_test.py` |

---

## 模板详解

### page_template.py

**用途**：封装页面操作和验证

**复制后修改**：
- 类名（`PageTemplate` → `XxxPage`）
- 定位器（根据实际页面）
- 操作方法（`fill_input`, `click_submit` 等）
- 验证方法（`verify_xxx`）

### conftest_template.py

**用途**：pytest 全局配置、fixtures

**核心 fixtures**：
- `config`：配置对象
- `fresh_page`：未登录页面
- `page`：已登录页面
- `page_obj`：页面对象

### config_loader_template.py

**用途**：配置文件读取类

**扩展方式**：添加 `@property` 方法

```python
@property
def my_custom_config(self) -> str:
    return self._config.get("my_config", "default")
```

### test_config_template.yaml

**用途**：测试配置文件

**必须修改**：
- `base_url`：测试环境地址
- `username` / `password`：测试账号

### assertion_test_template.py

**用途**：断言测试封装

**常用方法**：
- `assert_visible()` / `assert_hidden()`
- `assert_text()` / `assert_text_contains()`
- `assert_attribute()` / `assert_placeholder()`

### visual_test_template.py

**用途**：视觉回归测试

**工作流程**：
1. `take_screenshot()` 截图
2. `compare_images()` 对比基准图
3. `verify_visual()` 验证通过

### graphql_client_template.py

**用途**：GraphQL API 客户端

**特性**：
- Token 缓存
- 自动重新登录
- 过期处理

**扩展方式**：添加查询方法

```python
def query_my_data(self, param: str) -> Dict[str, Any]:
    query = f"""query {{ myData(param: "{param}") {{ id name }} }}"""
    return self._execute(query)
```

### slider_handler_template.py

**用途**：处理滑块验证码

**原理**：模拟完整鼠标事件序列（mousedown → mousemove → mouseup）

---

## 学习路径

### 第一步：运行最小示例

```bash
# 直接运行（不依赖 pytest）
python templates/demos/minimal_login_test.py
```

### 第二步：理解 pytest 结构

```bash
# 需要先配置 conftest.py
pytest templates/demos/minimal_pytest_test.py
```

### 第三步：创建自己的页面对象

```python
# 复制模板
# 修改定位器
# 添加操作方法
# 添加验证方法
```

### 第四步：编写测试用例

```python
def test_my_feature(page_obj):
    page_obj.navigate()
    page_obj.do_action()
    page_obj.verify_result()
```

---

## 复用建议

| 复用程度 | 模板 |
|---------|------|
| **完全复用** | `conftest_template.py`, `config_loader_template.py` |
| **修改复用** | `page_template.py`, `assertion_test_template.py` |
| **参考实现** | `slider_handler_template.py`, `graphql_client_template.py` |
| **学习示例** | `demos/` |

---

## 常见问题

### Q: 如何添加新的测试类型？

复制 `assertion_test_template.py`，修改断言方法。

### Q: 如何支持其他 API 类型（REST）？

参考 `graphql_client_template.py`，改用 `requests.get/post`。

### Q: 如何处理其他验证码类型？

参考 `slider_handler_template.py` 的思路，模拟对应的交互事件。

### Q: 如何调试测试？

```bash
# 设置 slow_mo
python minimal_login_test.py  # headless=False, slow_mo=100

# 或在配置中设置
browser:
  headless: false
  slow_mo: 100
```