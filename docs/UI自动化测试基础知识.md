# UI 自动化测试基础知识

## 一、主流方案对比

| 方案 | 语言 | 特点 | 适用场景 |
|------|------|------|----------|
| **Selenium** | Java/Python/JS/C# | 老牌、生态成熟、跨浏览器 | 传统Web应用 |
| **Playwright** | TypeScript/Python/Java/.NET | 微软出品、现代、自动等待、支持多浏览器 | 新项目首选 |
| **Cypress** | JavaScript/TypeScript | 开发体验好、调试强、仅Chrome系 | 前端团队 |
| **Puppeteer** | JavaScript/TypeScript | Google出品、仅Chrome | 爬虫/简单测试 |
| **Appium** | Java/Python/JS | 移动端自动化 | App测试 |

### 推荐选择

**Web UI自动化：Playwright + TypeScript/Python**
- 目前最热门，GitHub Star增速最快
- 自动等待机制，不用写sleep
- 内置录制、截图、trace功能
- 支持并行执行

**如果你有前端背景：** TypeScript + Playwright
**如果你熟悉Python：** Python + Playwright

### 成熟方案对比

- **Selenium** → 最成熟，但API较老，需要手动处理等待
- **Playwright** → 现代首选，2020年发布，已非常成熟
- **Cypress** → 成熟但局限性大（跨域、多浏览器支持弱）

---

## 二、UI自动化测试包含的内容

| 类型 | 测试内容 | 举例 |
|------|----------|------|
| **功能测试** | 验证功能是否正常工作 | 登录成功、表单提交、搜索返回结果 |
| **UI展示测试** | 界面元素是否正确渲染 | 按钮显示、文字无截断、样式正确 |
| **交互测试** | 用户操作是否响应正确 | 点击跳转、下拉选择、弹窗关闭 |
| **兼容性测试** | 不同环境表现一致 | 不同浏览器、不同分辨率 |
| **性能测试** | 页面加载、响应时间 | 首屏3秒内加载完成 |
| **回归测试** | 新代码不影响旧功能 | 每次发版前跑全部用例 |

---

## 三、如何判断UI是否有问题

### 1. 断言（Assertion）

```python
# 功能断言
assert "登录成功" in page.text  # 文案出现
assert page.is_visible("#welcome")  # 元素可见

# 属性断言
assert page.get_attribute("#btn", "disabled") == "true"
assert page.input_value("#search") == "关键词"
```

### 2. 视觉对比（Visual Regression）

- 截图与基准图对比，发现布局错位、样式异常

### 3. 元素状态验证

- 可见/不可见
- 可点击/禁用
- 选中/未选中

### 4. 行为验证

- 点击后是否跳转正确页面
- 提交后是否显示成功提示

---

## 四、实际工作建议

大多数UI自动化**侧重功能测试**（输入→操作→验证结果），纯UI展示问题通常靠人工或视觉回归工具发现。