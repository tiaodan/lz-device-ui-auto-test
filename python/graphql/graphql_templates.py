"""
无人机防御系统 GraphQL 请求模板
使用双花括号 {{}} 表示 GraphQL 结构，单花括号 {} 表示变量
"""

# ==================== 认证 ====================

LOGIN_MUTATION = """
mutation {{
  login(
    username: "{username}"
    password: "{password}"
  ) {{
    token
    expLen
    user {{
      id
      displayName
      role
    }}
  }}
}}
"""

# ==================== Query 查询 ====================

# 无人机信息
DRONE_QUERY = """
query {{
  drone(id: "{drone_id}") {{
    id
    name
    altitude
    height
    latitude
    longitude
    distance
    direction
    speed
    state
    attacking
    blacklisted
    whitelisted
    can_attack
    can_ctrl_landing
    in_ada
    created_time
    lastseen_time
    attack_type
    attack_bands
    image
    has_screenshot
    seen_sensor {{
      sensor_id
      detected_freq_khz
      signal_dbm
      snr_dB
      port
    }}
    initial_location {{
      lat
      lng
    }}
    rc_location {{
      lat
      lng
    }}
  }}
}}
"""

# 无人机列表（所有）
DRONES_ALL_QUERY = """
query {{
  drone {{
    id
    name
    state
    distance
    altitude
    latitude
    longitude
    attacking
    blacklisted
    whitelisted
    created_time
    lastseen_time
  }}
}}
"""

# 黑名单
BLACKLIST_QUERY = """
query {{
  blacklist {{
    id
    alias
    dronetype
    description
  }}
}}
"""

# 白名单
WHITELIST_QUERY = """
query {{
  whitelist {{
    id
    alias
    dronetype
    description
  }}
}}
"""

# 设备信息
DEVICES_QUERY = """
query {{
  devices(id: "{device_id}") {{
    id
    class
    config
    faults
    state
    status
    node
    gps_fixed
    toc
  }}
}}
"""

# 传感器信息
SENSOR_QUERY = """
query {{
  sensor(id: "{sensor_id}") {{
    id
    name
    mac
    node
    state
    faults
    ttl
    sensor_status {{
      ip_address
      version
      temperature
      first_seen
      last_seen
    }}
  }}
}}
"""

# 事件查询
EVENTS_QUERY = """
query {{
  events(
    drone_id: "{drone_id}"
    drone_type: "{drone_type}"
    begin_time: "{begin_time}"
    end_time: "{end_time}"
    from: {fromSeq}
  ) {{
    sequence
    id
    drone_type
    created_time
    deleted_time
    frequence
    attacked
    blacklisted
    whitelisted
    is_false_alarm
    severity
    first_pos
    last_pos
    seen_sensors
    image
    has_screenshot
  }}
}}
"""

# 事件聚合查询
EVENTS_AGGREGATION_QUERY = """
query {{
  events_aggregation(
    offset: {offset}
    limit: {limit}
    begin_time: "{begin_time}"
    end_time: "{end_time}"
    order: "{order}"
    order_by: "{order_by}"
    filter_severity: [SEVERITY_NA, SEVERITY_LOW, SEVERITY_MEDIUM, SEVERITY_HIGH]
  ) {{
    count
    data {{
      count
      data {{
        sequence
        id
        drone_type
        created_time
        attacked
        blacklisted
        whitelisted
      }}
    }}
  }}
}}
"""

# 历史轨迹
DRONE_TRACES_QUERY = """
query {{
  dronetraces(from: {fromSeq}, to: {toSeq}) {{
    id
    drone_type
    created_time
    center_lat
    center_lng
    points
    zoom
  }}
}}
"""

# 统计报告
REPORT_QUERY = """
query {{
  report(
    from: "{from_time}"
    to: "{to_time}"
  ) {{
    total_incidents
    total_drones
    total_duration
    total_mitigation
    avg_duration
    avg_per_day
    most_per_day
    most_per_hour
    longest_duration
    top_drone_type
    daily_data
    hourly_data
  }}
}}
"""

# 检测频段状态
DETECTING_BANDS_QUERY = """
query {{
  detectingBands {{
    band4
    band9
    band12
    band14
    band15
    band18
    band24
    band58
    Boost24
  }}
}}
"""

# 宽频干扰状态
WIDEBAND_JAMMER_QUERY = """
query {{
  widebandJammer(directional: {directional}) {{
    band4
    band9
    band12
    band14
    band15
    band18
    band24
    band58
  }}
}}
"""

# 干扰器冷却状态
JAMMER_COOLDOWN_QUERY = """
query {{
  JammerCooldownStatus {{
    band4
    band9
    band12
    band14
    band15
    band18
    band24
    band58
  }}
}}
"""

# 无人值守状态
AUTO_ATTACK_QUERY = """
query {{
  autoAttack
}}
"""

# 无人值守配置
AUTO_ATTACK_CONFIG_QUERY = """
query {{
  autoAttackConfig {{
    on
    saEnabled
    wbEnabled
    dirWbEnabled
    spfEnabled
    protectWhite
  }}
}}
"""

# 防空区
AIR_DEFENCE_AREA_QUERY = """
query {{
  airDefenceArea {{
    data
  }}
}}
"""

# 诱骗器状态
SPOOF_STATUS_QUERY = """
query {{
  spoofStatus {{
    switch
  }}
}}
"""

# 设备版本
VERSION_QUERY = """
query {{
  version
}}
"""

# 系统时间
TIME_QUERY = """
query {{
  time {{
    sysTime
  }}
}}
"""

# 系统时区
TIMEZONE_QUERY = """
query {{
  timeZone {{
    sysTimeZone
    allTimeZone
  }}
}}
"""

# 存储空间
STORAGE_QUERY = """
query {{
  storage {{
    internalSize
    externalSize
  }}
}}
"""

# 组网节点
NODES_QUERY = """
query {{
  nodes(id: "{node_id}") {{
    id
    name
    ip
    latitude
    longitude
    type
    info
  }}
}}
"""

# ==================== Mutation 操作 ====================

# 添加黑名单
ADD_BLACKLIST_MUTATION = """
mutation {{
  addBlacklist(
    id: "{drone_id}"
    dronetype: "{drone_type}"
    alias: "{alias}"
  )
}}
"""

# 移除黑名单
DELETE_BLACKLIST_MUTATION = """
mutation {{
  deleteBlacklist(id: "{drone_id}")
}}
"""

# 添加白名单
ADD_WHITELIST_MUTATION = """
mutation {{
  addWhitelist(
    id: "{drone_id}"
    dronetype: "{drone_type}"
    alias: "{alias}"
    timerange: "{timerange}"
  )
}}
"""

# 移除白名单
DELETE_WHITELIST_MUTATION = """
mutation {{
  deleteWhitelist(id: "{drone_id}")
}}
"""

# 精准打击
ATTACK_MUTATION = """
mutation {{
  attack(
    id: "{drone_id}"
    cancel: {cancel}
  )
}}
"""

# 迫降
CTRL_LANDING_MUTATION = """
mutation {{
  ctrl_landing(
    id: "{drone_id}"
    enable: {enable}
  )
}}
"""

# 无人值守配置
AUTO_ATTACK_MUTATION = """
mutation {{
  autoAttack(
    on: {on}
    saEnabled: {sa_enabled}
    wbEnabled: {wb_enabled}
    dirWbEnabled: {dir_wb_enabled}
    spfEnabled: {spf_enabled}
    protectWhite: {protect_white}
  )
}}
"""

# 宽频干扰
WIDEBAND_ATTACK_MUTATION = """
mutation {{
  wideband_attack(
    band: "{band}"
    wb_status: {wb_status}
    gain: {gain}
    direction: {direction}
    elevation: {elevation}
    directional: {directional}
    jammer_list: {jammer_list}
  ) {{
    band4
    band9
    band12
    band14
    band24
    band58
  }}
}}
"""

# 定向打击
DIRECTIONAL_WB_ATTACK_MUTATION = """
mutation {{
  directionalWBAttack(
    status: {status}
    band: "{band}"
    gain: {gain}
    droneId: "{drone_id}"
  ) {{
    band4
    band9
    band12
    band14
    band24
    band58
  }}
}}
"""

# 诱骗设置
SPOOFER_SWITCH_MUTATION = """
mutation {{
  spoofer_switch(
    id: "{spoofer_id}"
    action: {action}
    timeout: {timeout}
    direction: {direction}
  ) {{
    switch
  }}
}}
"""

# 绘制防空区
AIR_DEFENCE_AREA_MUTATION = """
mutation {{
  airDefenceArea(
    data: "{area_data}"
  )
}}
"""

# 检测频段开关
DETECTING_BANDS_MUTATION = """
mutation {{
  detectingBands(
    band: "{band}"
    enable: {enable}
  ) {{
    band4
    band9
    band12
    band14
    band24
    band58
  }}
}}
"""

# 删除事件
DELETE_EVENTS_MUTATION = """
mutation {{
  deleteEvents(sequence: {sequence_list})
}}
"""

# 根据ID删除事件
DELETE_EVENTS_BY_ID_MUTATION = """
mutation {{
  deleteEventsByID(
    drone_id: "{drone_id}"
    drone_type: "{drone_type}"
    all: {all}
  )
}}
"""

# 标记误报
MARK_FALSE_ALARM_MUTATION = """
mutation {{
  markFalseAlarm(sequence: {sequence_list})
}}
"""

# 还原误报
WITHDRAW_FALSE_ALARM_MUTATION = """
mutation {{
  withdrawFalseAlarm(
    drone_type: "{drone_type}"
    drone_id: "{drone_id}"
  )
}}
"""

# TDOA跟踪
TDOA_TRACK_MUTATION = """
mutation {{
  tdoa_track(
    id: "{drone_id}"
    enable: {enable}
  )
}}
"""

# 视觉跟踪
TRACKING_MUTATION = """
mutation {{
  tracking(
    id: "{device_id}"
    uuid: "{drone_uuid}"
  )
}}
"""

# 定向复位
STAGE_RESET_MUTATION = """
mutation {{
  stageReset(
    id: "{jammer_id}"
    direction: {direction}
    elevation: {elevation}
    track_enable: {track_enable}
  )
}}
"""

# 重启设备
RESET_MUTATION = """
mutation {{
  reset(
    id: "{device_id}"
    class: "{device_class}"
    reason: "{reason}"
  )
}}
"""

# 设置系统时间
TIME_MUTATION = """
mutation {{
  time(setTime: {timestamp})
}}
"""

# 设置时区
TIMEZONE_MUTATION = """
mutation {{
  timeZone(
    setTimeZone: "{timezone}"
    auto: {auto}
  )
}}
"""

# 设置设备位置
SET_GEO_LOCATION_MUTATION = """
mutation {{
  setGeoLocation(
    lat: {lat}
    lng: {lng}
  )
}}
"""

# 清除存储
CLEAR_STORAGE_MUTATION = """
mutation {{
  clearStorage
}}
"""

# 版本升级
UPGRADE_TO_MUTATION = """
mutation {{
  upgradeTo(
    versionName: "{version_name}"
    upgradeBy: "{upgrade_by}"
  )
}}
"""

# ==================== Subscription 订阅 ====================

# WebSocket URL: wss://192.168.100.100/sub/subscriptions

# 无人机实时订阅
DRONE_SUBSCRIPTION = """
subscription {{
  drone {{
    id
    name
    state
    altitude
    latitude
    longitude
    distance
    direction
    speed
    attacking
    blacklisted
    whitelisted
    attack_type
    created_time
    lastseen_time
    seen_sensor {{
      sensor_id
      detected_freq_khz
      signal_dbm
      snr_dB
    }}
  }}
}}
"""

# 后台消息订阅
MESSAGE_SUBSCRIPTION = """
subscription {{
  message {{
    msg_type
    msg_key
    info
    source
  }}
}}
"""

# 通知订阅
NOTIFY_SUBSCRIPTION = """
subscription {{
  notify {{
    id
    key
    info
    source
    status
    time
    extra
  }}
}}
"""