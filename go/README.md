# Go 自动化测试

## 运行

```bash
cd go
go run main.go
```

## GraphQL 使用

```go
package main

import "lz-device-ui-auto-test/graphql"

func main() {
    client := graphql.NewClient("https://192.168.100.100/rf/graphql")
    client.Login("root", "password")

    // 查询无人机
    drones, _ := client.GetAllDrones()

    // 精准打击
    client.Attack("ABC123", false)

    // 添加黑名单
    client.AddBlacklist("ABC123", "DJI Mavic", "")
}
```

## 目录结构

```
go/
├── graphql/          # GraphQL API 模块
│   ├── client.go
│   └── templates.go
├── tests/            # 测试用例（待添加）
├── pages/            # 页面对象（待添加）
├── config/           # 配置文件（待添加）
├── utils/            # 工具函数（待添加）
├── fixtures/         # 测试数据（待添加）
├── reports/          # 测试报告（待添加）
├── main.go           # 入口文件
└── go.mod            # Go 模块定义
```