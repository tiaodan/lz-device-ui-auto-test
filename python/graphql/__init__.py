"""
无人机防御系统 GraphQL 模块

使用方法：
    from graphql import GraphQLClient

    client = GraphQLClient()
    client.login("root", "password")
    drones = client.get_all_drones()
"""

from .graphql_client import GraphQLClient
from .graphql_templates import *

__all__ = ["GraphQLClient"]