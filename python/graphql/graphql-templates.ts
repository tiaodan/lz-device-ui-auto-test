/**
 * 无人机防御系统 GraphQL 请求模板
 * Base URL: https://192.168.100.100/rf/graphql
 */

// ==================== 认证 ====================

export const LOGIN_MUTATION = `
mutation {
  login(
    username: "${username}"
    password: "${password}"
  ) {
    token
    expLen
    user {
      id
      displayName
      role
    }
  }
}
`;

// ==================== Query 查询 ====================

// 无人机信息
export const DRONE_QUERY = `
query {
  drone(id: "${droneId}") {
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
    seen_sensor {
      sensor_id
      detected_freq_khz
      signal_dbm
      snr_dB
      port
    }
    initial_location {
      lat
      lng
    }
    rc_location {
      lat
      lng
    }
    tracing {
      lastlen
      origin {
        lat
        lng
      }
      points
    }
  }
}
`;

// 无人机列表（无参数，查询所有）
export const DRONES_ALL_QUERY = `
query {
  drone {
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
  }
}
`;

// 黑名单
export const BLACKLIST_QUERY = `
query {
  blacklist {
    id
    alias
    dronetype
    description
  }
}
`;

// 白名单
export const WHITELIST_QUERY = `
query {
  whitelist {
    id
    alias
    dronetype
    description
  }
}
`;

// 设备信息
export const DEVICES_QUERY = `
query {
  devices(id: "${deviceId}") {
    id
    class
    config
    faults
    state
    status
    node
    gps_fixed
    toc
  }
}
`;

// 传感器信息
export const SENSOR_QUERY = `
query {
  sensor(id: "${sensorId}") {
    id
    name
    mac
    node
    state
    faults
    ttl
    sensor_status {
      ip_address
      version
      temperature
      first_seen
      last_seen
    }
  }
}
`;

// 事件查询
export const EVENTS_QUERY = `
query {
  events(
    drone_id: "${droneId}"
    drone_type: "${droneType}"
    begin_time: "${beginTime}"
    end_time: "${endTime}"
    from: ${from}
  ) {
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
  }
}
`;

// 事件聚合查询
export const EVENTS_AGGREGATION_QUERY = `
query {
  events_aggregation(
    offset: ${offset}
    limit: ${limit}
    begin_time: "${beginTime}"
    end_time: "${endTime}"
    order: "${order}"
    order_by: "${orderBy}"
    filter_severity: [SEVERITY_NA, SEVERITY_LOW, SEVERITY_MEDIUM, SEVERITY_HIGH]
  ) {
    count
    data {
      count
      data {
        sequence
        id
        drone_type
        created_time
        attacked
        blacklisted
        whitelisted
      }
    }
  }
}
`;

// 历史轨迹
export const DRONE_TRACES_QUERY = `
query {
  dronetraces(from: ${from}, to: ${to}) {
    id
    drone_type
    created_time
    center_lat
    center_lng
    points
    zoom
  }
}
`;

// 统计报告
export const REPORT_QUERY = `
query {
  report(
    from: "${fromTime}"
    to: "${toTime}"
  ) {
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
  }
}
`;

// 检测频段状态
export const DETECTING_BANDS_QUERY = `
query {
  detectingBands {
    band4
    band9
    band12
    band14
    band15
    band18
    band24
    band58
    Boost24
  }
}
`;

// 宽频干扰状态
export const WIDEBAND_JAMMER_QUERY = `
query {
  widebandJammer(directional: ${directional}) {
    band4
    band9
    band12
    band14
    band15
    band18
    band24
    band58
  }
}
`;

// 干扰器冷却状态
export const JAMMER_COOLDOWN_QUERY = `
query {
  JammerCooldownStatus {
    band4
    band9
    band12
    band14
    band15
    band18
    band24
    band58
  }
}
`;

// 无人值守状态
export const AUTO_ATTACK_QUERY = `
query {
  autoAttack
}
`;

// 无人值守配置
export const AUTO_ATTACK_CONFIG_QUERY = `
query {
  autoAttackConfig {
    on
    saEnabled
    wbEnabled
    dirWbEnabled
    spfEnabled
    protectWhite
  }
}
`;

// 防空区
export const AIR_DEFENCE_AREA_QUERY = `
query {
  airDefenceArea {
    data
  }
}
`;

// 诱骗器状态
export const SPOOF_STATUS_QUERY = `
query {
  spoofStatus {
    switch
  }
}
`;

// 设备版本
export const VERSION_QUERY = `
query {
  version
}
`;

// 系统时间
export const TIME_QUERY = `
query {
  time {
    sysTime
  }
}
`;

// 系统时区
export const TIMEZONE_QUERY = `
query {
  timeZone {
    sysTimeZone
    allTimeZone
  }
}
`;

// 存储空间
export const STORAGE_QUERY = `
query {
  storage {
    internalSize
    externalSize
  }
}
`;

// 组网节点
export const NODES_QUERY = `
query {
  nodes(id: "${nodeId}") {
    id
    name
    ip
    latitude
    longitude
    type
    info
  }
}
`;

// ==================== Mutation 操作 ====================

// 添加黑名单
export const ADD_BLACKLIST_MUTATION = `
mutation {
  addBlacklist(
    id: "${droneId}"
    dronetype: "${droneType}"
    alias: "${alias}"
  )
}
`;

// 移除黑名单
export const DELETE_BLACKLIST_MUTATION = `
mutation {
  deleteBlacklist(id: "${droneId}")
}
`;

// 添加白名单
export const ADD_WHITELIST_MUTATION = `
mutation {
  addWhitelist(
    id: "${droneId}"
    dronetype: "${droneType}"
    alias: "${alias}"
    timerange: "${timerange}"
  )
}
`;

// 移除白名单
export const DELETE_WHITELIST_MUTATION = `
mutation {
  deleteWhitelist(id: "${droneId}")
}
`;

// 精准打击
export const ATTACK_MUTATION = `
mutation {
  attack(
    id: "${droneId}"
    cancel: ${cancel}
  )
}
`;

// 迫降
export const CTRL_LANDING_MUTATION = `
mutation {
  ctrl_landing(
    id: "${droneId}"
    enable: ${enable}
  )
}
`;

// 无人值守配置
export const AUTO_ATTACK_MUTATION = `
mutation {
  autoAttack(
    on: ${on}
    saEnabled: ${saEnabled}
    wbEnabled: ${wbEnabled}
    dirWbEnabled: ${dirWbEnabled}
    spfEnabled: ${spfEnabled}
    protectWhite: ${protectWhite}
  )
}
`;

// 宽频干扰
export const WIDEBAND_ATTACK_MUTATION = `
mutation {
  wideband_attack(
    band: "${band}"
    wb_status: ${wbStatus}
    gain: ${gain}
    direction: ${direction}
    elevation: ${elevation}
    directional: ${directional}
    jammer_list: ${jammerList}
  ) {
    band4
    band9
    band12
    band14
    band24
    band58
  }
}
`;

// 定向打击
export const DIRECTIONAL_WB_ATTACK_MUTATION = `
mutation {
  directionalWBAttack(
    status: ${status}
    band: "${band}"
    gain: ${gain}
    droneId: "${droneId}"
  ) {
    band4
    band9
    band12
    band14
    band24
    band58
  }
}
`;

// 诱骗设置
export const SPOOFER_SWITCH_MUTATION = `
mutation {
  spoofer_switch(
    id: "${spooferId}"
    action: ${action}
    timeout: ${timeout}
    direction: ${direction}
  ) {
    switch
  }
}
`;

// 绘制防空区
export const AIR_DEFENCE_AREA_MUTATION = `
mutation {
  airDefenceArea(
    data: "${areaData}"
  )
}
`;

// 检测频段开关
export const DETECTING_BANDS_MUTATION = `
mutation {
  detectingBands(
    band: "${band}"
    enable: ${enable}
  ) {
    band4
    band9
    band12
    band14
    band24
    band58
  }
}
`;

// 删除事件
export const DELETE_EVENTS_MUTATION = `
mutation {
  deleteEvents(sequence: ${sequenceList})
}
`;

// 根据ID删除事件
export const DELETE_EVENTS_BY_ID_MUTATION = `
mutation {
  deleteEventsByID(
    drone_id: "${droneId}"
    drone_type: "${droneType}"
    all: ${all}
  )
}
`;

// 标记误报（光电）
export const MARK_FALSE_ALARM_MUTATION = `
mutation {
  markFalseAlarm(sequence: ${sequenceList})
}
`;

// 还原误报事件
export const WITHDRAW_FALSE_ALARM_MUTATION = `
mutation {
  withdrawFalseAlarm(
    drone_type: "${droneType}"
    drone_id: "${droneId}"
  )
}
`;

// TDOA跟踪
export const TDOA_TRACK_MUTATION = `
mutation {
  tdoa_track(
    id: "${droneId}"
    enable: ${enable}
  )
}
`;

// 视觉跟踪
export const TRACKING_MUTATION = `
mutation {
  tracking(
    id: "${deviceId}"
    uuid: "${droneUuid}"
  )
}
`;

// 定向复位
export const STAGE_RESET_MUTATION = `
mutation {
  stageReset(
    id: "${jammerId}"
    direction: ${direction}
    elevation: ${elevation}
    track_enable: ${trackEnable}
  )
}
`;

// 重启设备
export const RESET_MUTATION = `
mutation {
  reset(
    id: "${deviceId}"
    class: "${deviceClass}"
    reason: "${reason}"
  )
}
`;

// 设置系统时间
export const TIME_MUTATION = `
mutation {
  time(setTime: ${timestamp})
}
`;

// 设置时区
export const TIMEZONE_MUTATION = `
mutation {
  timeZone(
    setTimeZone: "${timezone}"
    auto: ${auto}
  )
}
`;

// 设置设备位置
export const SET_GEO_LOCATION_MUTATION = `
mutation {
  setGeoLocation(
    lat: ${lat}
    lng: ${lng}
  )
}
`;

// 清除存储
export const CLEAR_STORAGE_MUTATION = `
mutation {
  clearStorage
}
`;

// 版本升级
export const UPGRADE_TO_MUTATION = `
mutation {
  upgradeTo(
    versionName: "${versionName}"
    upgradeBy: "${upgradeBy}"
  )
}
`;

// ==================== Subscription 订阅 ====================

// WebSocket URL: wss://192.168.100.100/sub/subscriptions

// 无人机实时订阅
export const DRONE_SUBSCRIPTION = `
subscription {
  drone {
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
    seen_sensor {
      sensor_id
      detected_freq_khz
      signal_dbm
      snr_dB
    }
  }
}
`;

// 后台消息订阅
export const MESSAGE_SUBSCRIPTION = `
subscription {
  message {
    msg_type
    msg_key
    info
    source
  }
}
`;

// 通知订阅
export const NOTIFY_SUBSCRIPTION = `
subscription {
  notify {
    id
    key
    info
    source
    status
    time
    extra
  }
}
`;

// ==================== 请求示例（带参数替换说明） ====================

/**
 * 使用示例：
 *
 * 1. 替换模板中的变量：
 *    - ${variableName} 需要替换为实际值
 *    - 字符串类型：保持引号，如 "${droneId}" → "ABC123"
 *    - 数字/布尔类型：不带引号，如 ${enable} → true
 *    - 数组类型：JSON格式，如 ${sequenceList} → [1, 2, 3]
 *
 * 2. 发送请求：
 *    POST https://192.168.100.100/rf/graphql
 *    Headers:
 *      Content-Type: application/json
 *      Authorization: Bearer <token>  (登录后获取)
 *    Body:
 *      { "query": "<graphql_query_string>" }
 *
 * 3. WebSocket订阅：
 *    wss://192.168.100.100/sub/subscriptions
 *    发送格式：
 *    {
 *      "id": "1",
 *      "type": "start",
 *      "payload": {
 *        "query": "<subscription_query>"
 *      }
 *    }
 */