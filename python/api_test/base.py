"""
接口自动化测试基础模块
提供 GraphQL API 验证功能，支持与 UI 数据一致性对比
"""

from graphql.graphql_client import GraphQLClient
from playwright.sync_api import Page
from typing import Dict, Any, Optional
import json
from utils.test_logger import get_default_logger


class ApiTest:
    """接口测试基类 - 支持 Token 自动管理"""

    def __init__(self, graphql_url: str, login_url: str = "", username: str = "", password: str = "", page: Optional[Page] = None):
        self.logger = get_default_logger()
        self.client = GraphQLClient(
            base_url=graphql_url,
            login_url=login_url,
            username=username,
            password=password
        )
        self.page = page
        self.token: Optional[str] = None

    # ==================== 认证 ====================

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """登录获取 Token"""
        result = self.client.login(username=username, password=password)
        if result.get("token"):
            self.token = result["token"]
            self.logger.pass_("登录成功，Token 已缓存")
        else:
            self.logger.fail(f"登录失败: {result}")
        return result

    def ensure_token(self) -> bool:
        """确保有有效的 Token"""
        return self.client.ensure_token()

    def is_logged_in(self) -> bool:
        """检查是否已登录"""
        return self.client.token is not None

    # ==================== 查询接口 ====================

    def query_drones(self) -> Dict[str, Any]:
        """查询无人机列表"""
        result = self.client.get_all_drones()
        self._log_query("drone", result)
        return result

    def query_blacklist(self) -> Dict[str, Any]:
        """查询黑名单"""
        result = self.client.get_blacklist()
        self._log_query("blacklist", result)
        return result

    def query_whitelist(self) -> Dict[str, Any]:
        """查询白名单"""
        result = self.client.get_whitelist()
        self._log_query("whitelist", result)
        return result

    def query_devices(self, device_id: str = "") -> Dict[str, Any]:
        """查询设备"""
        result = self.client.get_devices(device_id=device_id)
        self._log_query("devices", result)
        return result

    def query_events(self, drone_id: str = "", drone_type: str = "", begin_time: str = "", end_time: str = "") -> Dict[str, Any]:
        """查询事件"""
        result = self.client.get_events(drone_id=drone_id, drone_type=drone_type, begin_time=begin_time, end_time=end_time)
        self._log_query("events", result)
        return result

    def query_report(self, from_time: str, to_time: str) -> Dict[str, Any]:
        """查询统计"""
        result = self.client.get_report(from_time=from_time, to_time=to_time)
        self._log_query("report", result)
        return result

    # ==================== 操作接口 ====================

    def add_blacklist(self, drone_id: str, drone_type: str, alias: str = "") -> Dict[str, Any]:
        """添加黑名单"""
        result = self.client.add_blacklist(drone_id=drone_id, drone_type=drone_type, alias=alias)
        self._log_mutation("add_blacklist", result)
        return result

    def delete_blacklist(self, drone_id: str) -> Dict[str, Any]:
        """删除黑名单"""
        result = self.client.delete_blacklist(drone_id=drone_id)
        self._log_mutation("delete_blacklist", result)
        return result

    def attack(self, drone_id: str, cancel: bool = False) -> Dict[str, Any]:
        """精准打击"""
        result = self.client.attack(drone_id=drone_id, cancel=cancel)
        self._log_mutation("attack", result)
        return result

    # ==================== 数据一致性验证 ====================

    def verify_ui_data_consistency(self, ui_data: Any, api_data: Any, field_name: str = "") -> bool:
        """验证 UI 与 API 数据一致性"""
        if ui_data == api_data:
            self.logger.pass_(f"{field_name}: UI与API数据一致")
            return True
        else:
            self.logger.fail(f"{field_name}: UI={ui_data}, API={api_data}")
            return False

    def verify_drone_count_consistency(self, ui_count: int) -> bool:
        """验证无人机数量一致性"""
        api_result = self.query_drones()
        if api_result.get("data"):
            api_count = len(api_result["data"]["drone"])
            return self.verify_ui_data_consistency(ui_count, api_count, "drone_count")
        return False

    def verify_blacklist_count_consistency(self, ui_count: int) -> bool:
        """验证黑名单数量一致性"""
        api_result = self.query_blacklist()
        if api_result.get("data"):
            api_count = len(api_result["data"]["blacklist"])
            return self.verify_ui_data_consistency(ui_count, api_count, "blacklist_count")
        return False

    def verify_whitelist_count_consistency(self, ui_count: int) -> bool:
        """验证白名单数量一致性"""
        api_result = self.query_whitelist()
        if api_result.get("data"):
            api_count = len(api_result["data"]["whitelist"])
            return self.verify_ui_data_consistency(ui_count, api_count, "whitelist_count")
        return False

    # ==================== 响应验证 ====================

    def assert_response_success(self, response: Dict[str, Any]) -> bool:
        """断言响应成功"""
        if response.get("data"):
            self.logger.pass_("响应成功")
            return True
        elif response.get("errors"):
            errors = response["errors"]
            self.logger.fail(f"响应错误: {errors[0]['message']}")
            return False
        else:
            self.logger.fail("响应格式异常")
            return False

    def assert_response_has_data(self, response: Dict[str, Any], field_name: str) -> bool:
        """断言响应包含指定字段"""
        if response.get("data") and response["data"].get(field_name):
            self.logger.pass_(f"响应包含字段 '{field_name}'")
            return True
        self.logger.fail(f"响应缺少字段 '{field_name}'")
        return False

    def assert_data_not_empty(self, response: Dict[str, Any], field_name: str) -> bool:
        """断言数据非空"""
        if response.get("data") and response["data"].get(field_name):
            data = response["data"][field_name]
            if data and len(data) > 0:
                self.logger.pass_(f"'{field_name}' 数据非空")
                return True
        self.logger.fail(f"'{field_name}' 数据为空")
        return False

    # ==================== 辅助方法 ====================

    def get_response_data(self, response: Dict[str, Any], path: str = "data") -> Any:
        """获取响应数据"""
        keys = path.split(".")
        data = response
        for key in keys:
            if data and isinstance(data, dict) and key in data:
                data = data[key]
            else:
                return None
        return data

    def _log_query(self, name: str, result: Dict[str, Any]):
        """记录查询"""
        if result.get("data"):
            self.logger.pass_(f"Query '{name}' 成功")
        else:
            self.logger.fail(f"Query '{name}' 失败")

    def _log_mutation(self, name: str, result: Dict[str, Any]):
        """记录操作"""
        if result.get("data"):
            self.logger.pass_(f"Mutation '{name}' 成功")
        else:
            self.logger.fail(f"Mutation '{name}' 失败")

    def save_response(self, name: str, response: Dict[str, Any]):
        """保存响应到文件"""
        path = f"screenshots/api/{name}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(response, f, indent=2, ensure_ascii=False)
        self.logger.info(f"响应保存: {path}")