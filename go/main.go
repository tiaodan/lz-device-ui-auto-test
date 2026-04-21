package main

import (
	"fmt"
	"lz-device-ui-auto-test/graphql"
)

func main() {
	// 创建客户端
	client := graphql.NewClient("https://192.168.100.100/rf/graphql")

	// 登录
	result, err := client.Login("root", "password")
	if err != nil {
		fmt.Println("登录失败:", err)
		return
	}
	fmt.Println("登录结果:", result)

	// 查询所有无人机
	drones, err := client.GetAllDrones()
	if err != nil {
		fmt.Println("查询失败:", err)
		return
	}
	fmt.Println("无人机列表:", drones)

	// 查询黑名单
	blacklist, err := client.GetBlacklist()
	if err != nil {
		fmt.Println("查询失败:", err)
		return
	}
	fmt.Println("黑名单:", blacklist)

	// 精准打击示例
	// attackResult, err := client.Attack("ABC123", false)
	// fmt.Println("打击结果:", attackResult)
}