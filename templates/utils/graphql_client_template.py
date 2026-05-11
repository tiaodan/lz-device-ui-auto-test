"""
GraphQL 客户端模板
支持 Token 缓存、自动重新登录
"""

import requests
import json
import time
import os
from typing import Optional, Dict, Any


class GraphQLClientTemplate:
    """GraphQL API 客户端模板"""

    TOKEN_CACHE_FILE = "token_cache.json"
    TOKEN_EXPIRE_SECONDS = 604800  # 7天

    def __init__(self, base_url: str, login_url: str = "",
                 username: str = "", password: str = ""):
        self.base_url = base_url
        self.login_url = login_url or base_url.replace("/graphql", "/login")
        self.username = username
        self.password = password
        self.token: Optional[str] = None
        self.token_expire_time: Optional[float] = None
        self.session = requests.Session()

        self._load_cached_token()

    # ==================== Token 管理 ====================

    def _load_cached_token(self) -> bool:
        """加载缓存的 Token"""
        cache_path = self._get_cache_path()
        if os.path.exists(cache_path):
            try:
                with open(cache_path, "r") as f:
                    cache = json.load(f)
                    if cache.get("login_url") == self.login_url:
                        self.token = cache.get("token")
                        self.token_expire_time = cache.get("expire_time")
                        if self.token_expire_time and time.time() < self.token_expire_time:
                            self.session.headers.update({
                                "Authorization": f"Bearer {self.token}"
                            })
                            print("✓ 使用缓存 Token")
                            return True
            except Exception as e:
                print(f"加载缓存失败: {e}")
        return False

    def _save_token_cache(self):
        """保存 Token 到缓存"""
        cache = {
            "login_url": self.login_url,
            "graphql_url": self.base_url,
            "token": self.token,
            "expire_time": self.token_expire_time,
            "username": self.username
        }
        with open(self._get_cache_path(), "w") as f:
            json.dump(cache, f)
        print("✓ Token 已缓存")

    def _get_cache_path(self) -> str:
        """获取缓存文件路径"""
        return self.TOKEN_CACHE_FILE

    def _clear_cache(self):
        """清除缓存"""
        if os.path.exists(self._get_cache_path()):
            os.remove(self._get_cache_path())
        self.token = None
        self.token_expire_time = None

    # ==================== 登录 ====================

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """登录获取 Token"""
        self.username = username
        self.password = password

        try:
            response = self.session.post(
                self.login_url,
                json={"username": username, "password": password},
                verify=False,  # 测试环境忽略 SSL
                timeout=30
            )
            result = response.json()

            if result.get("token"):
                self.token = result["token"]
                exp_len = result.get("expLen", 604800000) / 1000
                self.token_expire_time = time.time() + exp_len

                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                self._save_token_cache()
                print(f"✓ 登录成功，Token 有效期 {int(exp_len)} 秒")
                return result
            else:
                print(f"✗ 登录失败: {result.get('msg', result)}")
                return result

        except Exception as e:
            print(f"✗ 登录异常: {e}")
            return {"msg": str(e), "status_code": 500}

    def ensure_token(self) -> bool:
        """确保有有效的 Token"""
        if self.token and self.token_expire_time and time.time() < self.token_expire_time:
            return True
        if self.username and self.password:
            result = self.login(self.username, self.password)
            return result.get("token") is not None
        return False

    # ==================== 执行查询 ====================

    def _execute(self, query: str) -> Dict[str, Any]:
        """执行 GraphQL 请求"""
        headers = {"Content-Type": "application/json"}
        if self.token:
            headers["Authorization"] = f"Bearer {self.token}"

        try:
            response = self.session.post(
                self.base_url,
                headers=headers,
                json={"query": query},
                verify=False,
                timeout=30
            )
            result = response.json()

            # 处理 Token 过期
            if result.get("errors"):
                for error in result["errors"]:
                    error_msg = str(error.get("message", "")).lower()
                    if "unauthorized" in error_msg or "token" in error_msg:
                        print("Token 过期，重新登录")
                        self._clear_cache()
                        if self.ensure_token():
                            headers["Authorization"] = f"Bearer {self.token}"
                            response = self.session.post(
                                self.base_url,
                                headers=headers,
                                json={"query": query},
                                verify=False,
                                timeout=30
                            )
                            return response.json()
            return result

        except Exception as e:
            return {"errors": [{"message": str(e)}]}

    # ==================== 查询接口（根据实际 API 添加） ====================

    def query_items(self) -> Dict[str, Any]:
        """查询列表（示例）"""
        query = """
        query {
            items {
                id
                name
                status
            }
        }
        """
        return self._execute(query)

    def query_item_by_id(self, item_id: str) -> Dict[str, Any]:
        """查询单个（示例）"""
        query = f"""
        query {{
            item(id: "{item_id}") {{
                id
                name
                status
            }}
        }}
        """
        return self._execute(query)


# ==================== 使用示例 ====================

"""
# test_api.py

def test_api_data(api_client):
    '''API 测试'''
    # 查询数据
    result = api_client.query_items()

    # 验证
    assert "errors" not in result
    assert len(result["data"]["items"]) > 0

# conftest.py
@pytest.fixture
def api_client(config):
    return GraphQLClientTemplate(
        base_url=config.graphql_url,
        username=config.username,
        password=config.password
    )
"""