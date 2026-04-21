# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 项目概述

无人机防御系统 UI 自动化测试工具，支持 **Python** 和 **Go** 两套语言实现。

**API 类型**：GraphQL
- **Base URL**：`https://192.168.100.100/rf/graphql`
- **WebSocket**：`wss://192.168.100.100/sub/subscriptions`

## 项目结构

```
├── python/           # Python 版本
│   ├── graphql/      # GraphQL API 模块
│   ├── tests/        # 测试用例（待添加）
│   ├── pages/        # 页面对象（待添加）
│   ├── config/       # 配置文件（待添加）
│   ├── main.py       # 入口文件
│   └── requirements.txt
│
├── go/               # Go 版本
│   ├── graphql/      # GraphQL API 模块
│   ├── tests/        # 测试用例（待添加）
│   ├── pages/        # 页面对象（待添加）
│   ├── config/       # 配置文件（待添加）
│   ├── main.go       # 入口文件
│   └── go.mod
│
├── docs/             # 文档
└── 接口文档/          # API 文档
```

## 使用方式

### Python

```bash
cd python
pip install -r requirements.txt
python main.py
```

```python
from graphql import GraphQLClient

client = GraphQLClient()
client.login("root", "password")
drones = client.get_all_drones()
client.attack(drone_id="ABC123")
```

### Go

```bash
cd go
go run main.go
```

```go
client := graphql.NewClient("https://192.168.100.100/rf/graphql")
client.Login("root", "password")
drones, _ := client.GetAllDrones()
client.Attack("ABC123", false)
```

## 主要接口

| 类型 | 功能 |
|------|------|
| **Query** | 查询无人机、设备、事件、统计等 |
| **Mutation** | 打击、诱骗、黑白名单、设备配置等 |
| **Subscription** | 实时推送无人机、消息、通知 |

## 编码规范

- 使用页面对象模式 (Page Object Model)
- 测试用例命名清晰
- 断言信息明确
- 测试数据与逻辑分离

## 参考资料

- [接口文档/历正科技应用接口说明v3.17.pdf](接口文档/) - GraphQL API 文档