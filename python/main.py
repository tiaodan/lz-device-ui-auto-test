"""
无人机防御系统自动化测试入口
"""

from graphql import GraphQLClient


def main():
    # 创建客户端
    client = GraphQLClient()

    # 登录
    result = client.login(username="root", password="password")
    print("登录结果:", result)

    # 查询所有无人机
    drones = client.get_all_drones()
    print("无人机列表:", drones)

    # 查询黑名单
    blacklist = client.get_blacklist()
    print("黑名单:", blacklist)

    # 精准打击示例
    # attack_result = client.attack(drone_id="ABC123", cancel=False)
    # print("打击结果:", attack_result)


if __name__ == "__main__":
    main()