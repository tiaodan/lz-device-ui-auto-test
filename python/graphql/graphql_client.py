"""
无人机防御系统 GraphQL 客户端
支持 Token 缓存，自动重新登录
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import requests
import json
import time
from typing import Optional, Dict, Any
from .graphql_templates import *
from utils.logger import get_default_logger

import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class GraphQLClient:
    """GraphQL API 客户端 - 支持 Token 缓存"""

    TOKEN_CACHE_FILE = "token_cache.json"
    TOKEN_EXPIRE_SECONDS = 604800

    def __init__(self, base_url: str, login_url: str = "", username: str = "", password: str = ""):
        self.logger = get_default_logger()
        self.base_url = base_url
        self.login_url = login_url or base_url.replace("/rf/graphql", "/login")
        self.username = username
        self.password = password
        self.token: Optional[str] = None
        self.token_expire_time: Optional[float] = None
        self.session = requests.Session()

        self._load_cached_token()

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
                            self.logger.pass_("使用缓存 Token")
                            return True
                        else:
                            self.logger.warn("缓存 Token 已过期")
            except Exception as e:
                self.logger.warn(f"加载缓存失败: {e}")
        return False

    def _save_token_cache(self):
        """保存 Token 到缓存"""
        cache_path = self._get_cache_path()
        cache = {
            "login_url": self.login_url,
            "graphql_url": self.base_url,
            "token": self.token,
            "expire_time": self.token_expire_time,
            "username": self.username
        }
        try:
            os.makedirs(os.path.dirname(cache_path), exist_ok=True)
            with open(cache_path, "w") as f:
                json.dump(cache, f)
            self.logger.pass_("Token 已缓存")
        except Exception as e:
            self.logger.warn(f"缓存保存失败: {e}")

    def _get_cache_path(self) -> str:
        """获取缓存文件路径"""
        return os.path.join(os.path.dirname(__file__), self.TOKEN_CACHE_FILE)

    def _clear_cache(self):
        """清除缓存"""
        cache_path = self._get_cache_path()
        if os.path.exists(cache_path):
            os.remove(cache_path)
        self.token = None
        self.token_expire_time = None

    def ensure_token(self) -> bool:
        """确保有有效的 Token"""
        if self.token and self.token_expire_time and time.time() < self.token_expire_time:
            return True

        if self.username and self.password:
            result = self.login(self.username, self.password)
            return result.get("token") is not None
        else:
            self.logger.fail("无用户名密码，无法自动登录")
            return False

    def login(self, username: str, password: str) -> Dict[str, Any]:
        """登录获取 Token"""
        self.username = username
        self.password = password

        try:
            response = self.session.post(
                self.login_url,
                json={"username": username, "password": password},
                verify=False,
                timeout=30
            )
            result = response.json()
            result["status_code"] = response.status_code

            if result.get("token"):
                self.token = result["token"]
                exp_len = result.get("expLen", 604800000) / 1000
                self.token_expire_time = time.time() + exp_len

                self.session.headers.update({
                    "Authorization": f"Bearer {self.token}"
                })
                self._save_token_cache()
                self.logger.pass_(f"登录成功，Token 有效期 {int(exp_len)} 秒")
                return result
            else:
                self.logger.fail(f"登录失败: {result.get('msg', result)}")
                return result

        except Exception as e:
            self.logger.fail(f"登录异常: {e}")
            return {"msg": str(e), "status_code": 500}

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

            if result.get("errors"):
                for error in result["errors"]:
                    error_msg = str(error.get("message", "")).lower()
                    if "unauthorized" in error_msg or "token" in error_msg or "expired" in error_msg:
                        self.logger.warn("Token 可能过期，尝试重新登录")
                        self._clear_cache()
                        if self.username and self.password:
                            self.login(self.username, self.password)
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

    # ==================== 查询接口 ====================

    def get_drone(self, drone_id: str) -> Dict[str, Any]:
        """查询单个无人机"""
        query = DRONE_QUERY.format(drone_id=drone_id)
        return self._execute(query)

    def get_all_drones(self) -> Dict[str, Any]:
        """查询所有无人机"""
        return self._execute(DRONES_ALL_QUERY)

    def get_blacklist(self) -> Dict[str, Any]:
        """查询黑名单"""
        return self._execute(BLACKLIST_QUERY)

    def get_whitelist(self) -> Dict[str, Any]:
        """查询白名单"""
        return self._execute(WHITELIST_QUERY)

    def get_devices(self, device_id: str = "") -> Dict[str, Any]:
        """查询设备"""
        query = DEVICES_QUERY.format(device_id=device_id)
        return self._execute(query)

    def get_sensor(self, sensor_id: str = "") -> Dict[str, Any]:
        """查询传感器"""
        query = SENSOR_QUERY.format(sensor_id=sensor_id)
        return self._execute(query)

    def get_events(self, drone_id: str = "", drone_type: str = "", begin_time: str = "", end_time: str = "", from_seq: int = 0) -> Dict[str, Any]:
        """查询事件"""
        query = EVENTS_QUERY.format(drone_id=drone_id, drone_type=drone_type, begin_time=begin_time, end_time=end_time, fromSeq=from_seq)
        return self._execute(query)

    def get_events_aggregation(self, offset: int = 0, limit: int = 10, begin_time: str = "", end_time: str = "", order: str = "desc", order_by: str = "created_time") -> Dict[str, Any]:
        """事件聚合查询"""
        query = EVENTS_AGGREGATION_QUERY.format(offset=offset, limit=limit, begin_time=begin_time, end_time=end_time, order=order, order_by=order_by)
        return self._execute(query)

    def get_drone_traces(self, from_seq: int, to_seq: int) -> Dict[str, Any]:
        """查询历史轨迹"""
        query = DRONE_TRACES_QUERY.format(fromSeq=from_seq, toSeq=to_seq)
        return self._execute(query)

    def get_report(self, from_time: str, to_time: str) -> Dict[str, Any]:
        """查询统计报告"""
        query = REPORT_QUERY.format(from_time=from_time, to_time=to_time)
        return self._execute(query)

    def get_detecting_bands(self) -> Dict[str, Any]:
        """查询检测频段"""
        return self._execute(DETECTING_BANDS_QUERY)

    def get_wideband_jammer(self, directional: bool = False) -> Dict[str, Any]:
        """查询宽频干扰"""
        query = WIDEBAND_JAMMER_QUERY.format(directional=str(directional).lower())
        return self._execute(query)

    def get_jammer_cooldown(self) -> Dict[str, Any]:
        """查询干扰器冷却"""
        return self._execute(JAMMER_COOLDOWN_QUERY)

    def get_auto_attack_status(self) -> Dict[str, Any]:
        """查询无人值守状态"""
        return self._execute(AUTO_ATTACK_QUERY)

    def get_auto_attack_config(self) -> Dict[str, Any]:
        """查询无人值守配置"""
        return self._execute(AUTO_ATTACK_CONFIG_QUERY)

    def get_air_defence_area(self) -> Dict[str, Any]:
        """查询防空区"""
        return self._execute(AIR_DEFENCE_AREA_QUERY)

    def get_spoof_status(self) -> Dict[str, Any]:
        """查询诱骗器状态"""
        return self._execute(SPOOF_STATUS_QUERY)

    def get_version(self) -> Dict[str, Any]:
        """查询设备版本"""
        return self._execute(VERSION_QUERY)

    def get_time(self) -> Dict[str, Any]:
        """查询系统时间"""
        return self._execute(TIME_QUERY)

    def get_timezone(self) -> Dict[str, Any]:
        """查询系统时区"""
        return self._execute(TIMEZONE_QUERY)

    def get_storage(self) -> Dict[str, Any]:
        """查询存储空间"""
        return self._execute(STORAGE_QUERY)

    def get_nodes(self, node_id: str = "") -> Dict[str, Any]:
        """查询组网节点"""
        query = NODES_QUERY.format(node_id=node_id)
        return self._execute(query)

    # ==================== 操作接口 ====================

    def add_blacklist(self, drone_id: str, drone_type: str, alias: str = "") -> Dict[str, Any]:
        """添加黑名单"""
        query = ADD_BLACKLIST_MUTATION.format(drone_id=drone_id, drone_type=drone_type, alias=alias)
        return self._execute(query)

    def delete_blacklist(self, drone_id: str) -> Dict[str, Any]:
        """移除黑名单"""
        query = DELETE_BLACKLIST_MUTATION.format(drone_id=drone_id)
        return self._execute(query)

    def add_whitelist(self, drone_id: str, drone_type: str, alias: str = "", timerange: str = "permanent,permanent") -> Dict[str, Any]:
        """添加白名单"""
        query = ADD_WHITELIST_MUTATION.format(drone_id=drone_id, drone_type=drone_type, alias=alias, timerange=timerange)
        return self._execute(query)

    def delete_whitelist(self, drone_id: str) -> Dict[str, Any]:
        """移除白名单"""
        query = DELETE_WHITELIST_MUTATION.format(drone_id=drone_id)
        return self._execute(query)

    def attack(self, drone_id: str, cancel: bool = False) -> Dict[str, Any]:
        """精准打击"""
        query = ATTACK_MUTATION.format(drone_id=drone_id, cancel=str(cancel).lower())
        return self._execute(query)

    def ctrl_landing(self, drone_id: str, enable: bool) -> Dict[str, Any]:
        """迫降"""
        query = CTRL_LANDING_MUTATION.format(drone_id=drone_id, enable=str(enable).lower())
        return self._execute(query)

    def set_auto_attack(self, on: bool, sa_enabled: bool = False, wb_enabled: bool = False, dir_wb_enabled: bool = False, spf_enabled: bool = False, protect_white: bool = False) -> Dict[str, Any]:
        """设置无人值守"""
        query = AUTO_ATTACK_MUTATION.format(on=str(on).lower(), sa_enabled=str(sa_enabled).lower(), wb_enabled=str(wb_enabled).lower(), dir_wb_enabled=str(dir_wb_enabled).lower(), spf_enabled=str(spf_enabled).lower(), protect_white=str(protect_white).lower())
        return self._execute(query)

    def wideband_attack(self, band: str, wb_status: bool, gain: int = 50, direction: int = -1, elevation: int = 0, directional: bool = False, jammer_list: str = "[\"1\"]") -> Dict[str, Any]:
        """宽频干扰"""
        query = WIDEBAND_ATTACK_MUTATION.format(band=band, wb_status=str(wb_status).lower(), gain=gain, direction=direction, elevation=elevation, directional=str(directional).lower(), jammer_list=jammer_list)
        return self._execute(query)

    def directional_attack(self, status: bool, band: str, gain: int, drone_id: str) -> Dict[str, Any]:
        """定向打击"""
        query = DIRECTIONAL_WB_ATTACK_MUTATION.format(status=str(status).lower(), band=band, gain=gain, drone_id=drone_id)
        return self._execute(query)

    def spoofer_switch(self, action: int, timeout: int = 0, direction: int = -1, spoofer_id: str = "") -> Dict[str, Any]:
        """诱骗设置"""
        query = SPOOFER_SWITCH_MUTATION.format(spoofer_id=spoofer_id, action=action, timeout=timeout, direction=direction)
        return self._execute(query)

    def set_air_defence_area(self, area_data: str) -> Dict[str, Any]:
        """绘制防空区"""
        query = AIR_DEFENCE_AREA_MUTATION.format(area_data=area_data)
        return self._execute(query)

    def set_detecting_band(self, band: str, enable: bool) -> Dict[str, Any]:
        """检测频段开关"""
        query = DETECTING_BANDS_MUTATION.format(band=band, enable=str(enable).lower())
        return self._execute(query)

    def delete_events(self, sequence_list: list) -> Dict[str, Any]:
        """删除事件"""
        query = DELETE_EVENTS_MUTATION.format(sequence_list=json.dumps(sequence_list))
        return self._execute(query)

    def delete_events_by_id(self, drone_id: str, drone_type: str, all: bool = False) -> Dict[str, Any]:
        """根据ID删除事件"""
        query = DELETE_EVENTS_BY_ID_MUTATION.format(drone_id=drone_id, drone_type=drone_type, all=str(all).lower())
        return self._execute(query)

    def mark_false_alarm(self, sequence_list: list) -> Dict[str, Any]:
        """标记误报"""
        query = MARK_FALSE_ALARM_MUTATION.format(sequence_list=json.dumps(sequence_list))
        return self._execute(query)

    def withdraw_false_alarm(self, drone_type: str, drone_id: str) -> Dict[str, Any]:
        """还原误报"""
        query = WITHDRAW_FALSE_ALARM_MUTATION.format(drone_type=drone_type, drone_id=drone_id)
        return self._execute(query)

    def tdoa_track(self, drone_id: str, enable: bool) -> Dict[str, Any]:
        """TDOA跟踪"""
        query = TDOA_TRACK_MUTATION.format(drone_id=drone_id, enable=str(enable).lower())
        return self._execute(query)

    def tracking(self, device_id: str, drone_uuid: str) -> Dict[str, Any]:
        """视觉跟踪"""
        query = TRACKING_MUTATION.format(device_id=device_id, drone_uuid=drone_uuid)
        return self._execute(query)

    def stage_reset(self, jammer_id: str, direction: float = 0, elevation: float = 0, track_enable: bool = False) -> Dict[str, Any]:
        """定向复位"""
        query = STAGE_RESET_MUTATION.format(jammer_id=jammer_id, direction=direction, elevation=elevation, track_enable=str(track_enable).lower())
        return self._execute(query)

    def reset_device(self, device_id: str, device_class: str, reason: str = "") -> Dict[str, Any]:
        """重启设备"""
        query = RESET_MUTATION.format(device_id=device_id, device_class=device_class, reason=reason)
        return self._execute(query)

    def set_time(self, timestamp: int) -> Dict[str, Any]:
        """设置系统时间"""
        query = TIME_MUTATION.format(timestamp=timestamp)
        return self._execute(query)

    def set_timezone(self, timezone: str, auto: bool = False) -> Dict[str, Any]:
        """设置时区"""
        query = TIMEZONE_MUTATION.format(timezone=timezone, auto=str(auto).lower())
        return self._execute(query)

    def set_geo_location(self, lat: float, lng: float) -> Dict[str, Any]:
        """设置设备位置"""
        query = SET_GEO_LOCATION_MUTATION.format(lat=lat, lng=lng)
        return self._execute(query)

    def clear_storage(self) -> Dict[str, Any]:
        """清除存储"""
        return self._execute(CLEAR_STORAGE_MUTATION)

    def upgrade_to(self, version_name: str, upgrade_by: str = "manual") -> Dict[str, Any]:
        """版本升级"""
        query = UPGRADE_TO_MUTATION.format(version_name=version_name, upgrade_by=upgrade_by)
        return self._execute(query)


if __name__ == "__main__":
    client = GraphQLClient("https://192.168.85.238/rf/graphql")
    result = client.login(username="root", password="password")
    client.logger.info(f"登录结果: {result}")
    drones = client.get_all_drones()
    client.logger.info(f"无人机列表: {drones}")