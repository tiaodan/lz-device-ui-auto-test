package graphql

// 认证
const LoginMutation = `
mutation {
  login(
    username: "{{.Username}}"
    password: "{{.Password}}"
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
`

// ==================== Query 查询 ====================

// 无人机信息
const DroneQuery = `
query {
  drone(id: "{{.DroneID}}") {
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
  }
}
`

// 无人机列表（所有）
const DronesAllQuery = `
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
`

// 黑名单
const BlacklistQuery = `
query {
  blacklist {
    id
    alias
    dronetype
    description
  }
}
`

// 白名单
const WhitelistQuery = `
query {
  whitelist {
    id
    alias
    dronetype
    description
  }
}
`

// 设备信息
const DevicesQuery = `
query {
  devices(id: "{{.DeviceID}}") {
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
`

// 传感器信息
const SensorQuery = `
query {
  sensor(id: "{{.SensorID}}") {
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
`

// 事件查询
const EventsQuery = `
query {
  events(
    drone_id: "{{.DroneID}}"
    drone_type: "{{.DroneType}}"
    begin_time: "{{.BeginTime}}"
    end_time: "{{.EndTime}}"
    from: {{.From}}
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
`

// 事件聚合查询
const EventsAggregationQuery = `
query {
  events_aggregation(
    offset: {{.Offset}}
    limit: {{.Limit}}
    begin_time: "{{.BeginTime}}"
    end_time: "{{.EndTime}}"
    order: "{{.Order}}"
    order_by: "{{.OrderBy}}"
    filter_severity: [SEVERITY_NA, SEVERITY_LOW, SEVERITY_HIGH, SEVERITY_MEDIUM]
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
`

// 历史轨迹
const DroneTracesQuery = `
query {
  dronetraces(from: {{.From}}, to: {{.To}}) {
    id
    drone_type
    created_time
    center_lat
    center_lng
    points
    zoom
  }
}
`

// 统计报告
const ReportQuery = `
query {
  report(
    from: "{{.FromTime}}"
    to: "{{.ToTime}}"
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
`

// 检测频段状态
const DetectingBandsQuery = `
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
`

// 宽频干扰状态
const WidebandJammerQuery = `
query {
  widebandJammer(directional: {{.Directional}}) {
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
`

// 干扰器冷却状态
const JammerCooldownQuery = `
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
`

// 无人值守状态
const AutoAttackQuery = `
query {
  autoAttack
}
`

// 无人值守配置
const AutoAttackConfigQuery = `
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
`

// 防空区
const AirDefenceAreaQuery = `
query {
  airDefenceArea {
    data
  }
}
`

// 诱骗器状态
const SpoofStatusQuery = `
query {
  spoofStatus {
    switch
  }
}
`

// 设备版本
const VersionQuery = `
query {
  version
}
`

// 系统时间
const TimeQuery = `
query {
  time {
    sysTime
  }
}
`

// 系统时区
const TimezoneQuery = `
query {
  timeZone {
    sysTimeZone
    allTimeZone
  }
}
`

// 存储空间
const StorageQuery = `
query {
  storage {
    internalSize
    externalSize
  }
}
`

// 组网节点
const NodesQuery = `
query {
  nodes(id: "{{.NodeID}}") {
    id
    name
    ip
    latitude
    longitude
    type
    info
  }
}
`

// ==================== Mutation 操作 ====================

// 添加黑名单
const AddBlacklistMutation = `
mutation {
  addBlacklist(
    id: "{{.DroneID}}"
    dronetype: "{{.DroneType}}"
    alias: "{{.Alias}}"
  )
}
`

// 移除黑名单
const DeleteBlacklistMutation = `
mutation {
  deleteBlacklist(id: "{{.DroneID}}")
}
`

// 添加白名单
const AddWhitelistMutation = `
mutation {
  addWhitelist(
    id: "{{.DroneID}}"
    dronetype: "{{.DroneType}}"
    alias: "{{.Alias}}"
    timerange: "{{.TimeRange}}"
  )
}
`

// 移除白名单
const DeleteWhitelistMutation = `
mutation {
  deleteWhitelist(id: "{{.DroneID}}")
}
`

// 精准打击
const AttackMutation = `
mutation {
  attack(
    id: "{{.DroneID}}"
    cancel: {{.Cancel}}
  )
}
`

// 迫降
const CtrlLandingMutation = `
mutation {
  ctrl_landing(
    id: "{{.DroneID}}"
    enable: {{.Enable}}
  )
}
`

// 无人值守配置
const AutoAttackMutation = `
mutation {
  autoAttack(
    on: {{.On}}
    saEnabled: {{.SaEnabled}}
    wbEnabled: {{.WbEnabled}}
    dirWbEnabled: {{.DirWbEnabled}}
    spfEnabled: {{.SpfEnabled}}
    protectWhite: {{.ProtectWhite}}
  )
}
`

// 宽频干扰
const WidebandAttackMutation = `
mutation {
  wideband_attack(
    band: "{{.Band}}"
    wb_status: {{.WbStatus}}
    gain: {{.Gain}}
    direction: {{.Direction}}
    elevation: {{.Elevation}}
    directional: {{.Directional}}
    jammer_list: {{.JammerList}}
  ) {
    band4
    band9
    band12
    band14
    band24
    band58
  }
}
`

// 定向打击
const DirectionalWBAttackMutation = `
mutation {
  directionalWBAttack(
    status: {{.Status}}
    band: "{{.Band}}"
    gain: {{.Gain}}
    droneId: "{{.DroneID}}"
  ) {
    band4
    band9
    band12
    band14
    band24
    band58
  }
}
`

// 诱骗设置
const SpooferSwitchMutation = `
mutation {
  spoofer_switch(
    id: "{{.SpooferID}}"
    action: {{.Action}}
    timeout: {{.Timeout}}
    direction: {{.Direction}}
  ) {
    switch
  }
}
`

// 绘制防空区
const AirDefenceAreaMutation = `
mutation {
  airDefenceArea(
    data: "{{.AreaData}}"
  )
}
`

// 检测频段开关
const DetectingBandsMutation = `
mutation {
  detectingBands(
    band: "{{.Band}}"
    enable: {{.Enable}}
  ) {
    band4
    band9
    band12
    band14
    band24
    band58
  }
}
`

// 删除事件
const DeleteEventsMutation = `
mutation {
  deleteEvents(sequence: {{.SequenceList}})
}
`

// 根据ID删除事件
const DeleteEventsByIDMutation = `
mutation {
  deleteEventsByID(
    drone_id: "{{.DroneID}}"
    drone_type: "{{.DroneType}}"
    all: {{.All}}
  )
}
`

// 标记误报
const MarkFalseAlarmMutation = `
mutation {
  markFalseAlarm(sequence: {{.SequenceList}})
}
`

// 还原误报
const WithdrawFalseAlarmMutation = `
mutation {
  withdrawFalseAlarm(
    drone_type: "{{.DroneType}}"
    drone_id: "{{.DroneID}}"
  )
}
`

// TDOA跟踪
const TdoaTrackMutation = `
mutation {
  tdoa_track(
    id: "{{.DroneID}}"
    enable: {{.Enable}}
  )
}
`

// 视觉跟踪
const TrackingMutation = `
mutation {
  tracking(
    id: "{{.DeviceID}}"
    uuid: "{{.DroneUUID}}"
  )
}
`

// 定向复位
const StageResetMutation = `
mutation {
  stageReset(
    id: "{{.JammerID}}"
    direction: {{.Direction}}
    elevation: {{.Elevation}}
    track_enable: {{.TrackEnable}}
  )
}
`

// 重启设备
const ResetMutation = `
mutation {
  reset(
    id: "{{.DeviceID}}"
    class: "{{.DeviceClass}}"
    reason: "{{.Reason}}"
  )
}
`

// 设置系统时间
const TimeMutation = `
mutation {
  time(setTime: {{.Timestamp}})
}
`

// 设置时区
const TimezoneMutation = `
mutation {
  timeZone(
    setTimeZone: "{{.TimeZone}}"
    auto: {{.Auto}}
  )
}
`

// 设置设备位置
const SetGeoLocationMutation = `
mutation {
  setGeoLocation(
    lat: {{.Lat}}
    lng: {{.Lng}}
  )
}
`

// 清除存储
const ClearStorageMutation = `
mutation {
  clearStorage
}
`

// 版本升级
const UpgradeToMutation = `
mutation {
  upgradeTo(
    versionName: "{{.VersionName}}"
    upgradeBy: "{{.UpgradeBy}}"
  )
}
`

// ==================== Subscription 订阅 ====================

// WebSocket URL: wss://192.168.100.100/sub/subscriptions

// 无人机实时订阅
const DroneSubscription = `
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
`

// 后台消息订阅
const MessageSubscription = `
subscription {
  message {
    msg_type
    msg_key
    info
    source
  }
}
`

// 通知订阅
const NotifySubscription = `
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
`