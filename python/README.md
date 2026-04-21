# Python 自动化测试

无人机防御系统 UI 自动化测试框架，支持三种测试类型。

## 目录结构

```
python/
├── venv/                  # 虚拟环境（已创建）
│
├── config/               # 配置文件
│   ├── test_config.yaml  # 测试配置（重要！）
│   └── config_loader.py  # 配置读取模块
│
├── graphql/              # GraphQL API 模块
│   ├── graphql_client.py
│   ├── graphql_templates.py
│   └── graphql-templates.ts
│
├── pages/                # 页面对象
│   └── login_page.py
│
├── tests/                # 测试用例
│   ├── assertion/        # 断言测试
│   │   ├── base.py
│   │   └── test_login.py
│   │
│   ├── visual/           # 图片识别测试
│   │   ├── base.py
│   │   └── test_login.py
│   │
│   └── api/              # 接口测试
│       ├── base.py
│       └── test_login.py
│
├── screenshots/          # 截图目录
│   ├── baseline/         # 基准图
│   ├── current/          # 当前截图
│   ├── diff/             # 差异图
│   └── assertion/        # 断言测试截图
│
├── run_tests.py          # 统一测试入口
├── main.py
└── requirements.txt
```

## 安装依赖

```bash
cd python

# 创建虚拟环境（已创建）
python -m venv venv

# 激活虚拟环境
# Windows CMD:
venv\Scripts\activate.bat
# Windows PowerShell:
venv\Scripts\Activate.ps1
# Linux/Mac:
source venv/bin/activate

# 安装依赖
pip install -r requirements.txt

# 安装浏览器
playwright install chromium
```

## 配置文件

编辑 `config/test_config.yaml`：

```yaml
# 测试环境
base_url: "https://192.168.85.238"
graphql_url: "https://192.168.100.100/rf/graphql"

# 登录信息
username: "root"
password: "your_password"  # 替换为真实密码

# 启用的测试类型
test_types:
  - assertion  # 断言测试
  - visual     # 图片识别
  - api        # 接口测试

# 图片对比阈值
visual:
  threshold: 0.1  # 10% 差异容忍度
```

## 运行测试

### 运行所有测试

```bash
python run_tests.py
```

### 运行指定类型

```bash
# 运行断言测试
python run_tests.py assertion

# 运行图片识别测试
python run_tests.py visual

# 运行接口测试
python run_tests.py api
```

### 运行单个测试

```bash
# 断言测试
python run_tests.py assertion elements
python run_tests.py assertion slider
python run_tests.py assertion form

# 图片识别测试
python run_tests.py visual page
python run_tests.py visual slider
python run_tests.py visual button

# 接口测试
python run_tests.py api login
python run_tests.py api drones
python run_tests.py api blacklist
```

### 创建基准图

```bash
python run_tests.py visual baseline
```

## 三种测试类型

### 1. 断言测试 (Assertion)

验证元素、文本、属性：

```python
assertion.assert_visible(locator, "元素可见")
assertion.assert_text_contains(locator, "Sign in", "按钮文本")
assertion.assert_attribute(locator, "placeholder", "Username")
```

### 2. 图片识别测试 (Visual)

截图对比、视觉回归：

```python
visual.take_screenshot("login_page")
visual.compare_images("login_page")
```

### 3. 接口测试 (API)

GraphQL API 验证：

```python
api.login(username, password)
api.query_drones()
api.verify_ui_data_consistency(ui_count, api_count)
```

## 滑块验证码处理

系统自动处理滑块验证码：

```python
login_page.drag_slider()  # 自动拖动到解锁位置
```

## 测试报告

测试完成后查看：
- 截图：`screenshots/`
- 差异图：`screenshots/diff/`