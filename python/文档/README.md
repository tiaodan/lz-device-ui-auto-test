# 文档索引

## 文档列表

| 文档 | 内容 |
|-----|------|
| [项目说明.md](项目说明.md) | 项目概述、结构、配置、依赖 |
| [pytest框架说明.md](pytest框架说明.md) | pytest改造、配置、fixtures、loguru |
| [测试类型说明.md](测试类型说明.md) | 断言/视觉/API三种测试详解 |
| [运行命令.md](运行命令.md) | pytest常用命令汇总 |
| [登录测试说明.md](登录测试说明.md) | 登录流程、元素定位、滑块处理 |
| [Mock测试说明.md](Mock测试说明.md) | Meta测试、UI异常模拟、检测有效性 |
| [配置化说明.md](配置化说明.md) | 定位器配置化分离、YAML配置结构 |

## 快速开始

1. **安装依赖**：
```bash
cd python
pip install -r requirements.txt
playwright install chromium
```

2. **运行测试**：
```bash
pytest                # 全部测试
pytest -m assertion   # 断言测试
pytest -m visual      # 视觉测试
pytest -m api         # API测试
```

3. **生成报告**：
```bash
pytest --html=reports/report.html --self-contained-html
```

## 关键文件

| 文件路径 | 说明 |
|---------|------|
| `pyproject.toml` | pytest配置 |
| `conftest.py` | 全局fixtures |
| `config/test_config.yaml` | 测试配置 |
| `utils/test_logger.py` | loguru日志 |
| `pages/login_page.py` | 登录页面对象 |

## 测试统计

- **总测试数**: 23
- **断言测试**: 13
- **视觉测试**: 4
- **API测试**: 6