# GraphQL API 接口文档

- 生成时间：`2026-03-24T21:11:41+08:00`

## API 列表

### Query

| 接口名称 | 接口描述 |
| --- | --- |
| [`airDefenceArea`](#query-airdefencearea) | 查询防空区域；如果未设置区域则返回空。 |
| [`autoAttack`](#query-autoattack) | 查询自动打击开关状态。 |
| [`autoAttackConfig`](#query-autoattackconfig) | 查询自动打击配置。 |
| [`availableUpgrade`](#query-availableupgrade) | - |
| [`blacklist`](#query-blacklist) | 查询无人机黑名单列表信息。 |
| [`cameraPosts`](#query-cameraposts) | 获取用于遮罩/取消遮罩的摄像头点位。 |
| [`camManufacturer`](#query-cammanufacturer) | 获取摄像头厂商信息。 |
| [`camPTZ`](#query-camptz) | 获取摄像头 PTZ。 |
| [`check`](#query-check) | - |
| [`detectingBands`](#query-detectingbands) | 查询设备侦测频段状态（0: 不可用，1: 禁用，2: 启用）。 |
| [`device_event_log`](#query-device-event-log) | 查询设备事件日志。 |
| [`devices`](#query-devices) | 查询指定设备信息（例如 controller、engine、sensor、jammer）。 |
| [`deviceStat`](#query-devicestat) | 查询设备管理中的引擎运行状态以及收发包状态信息。 |
| [`dfgun`](#query-dfgun) | - |
| [`dhcpStatus`](#query-dhcpstatus) | 查询 DHCP 状态。 |
| [`downloadStatus`](#query-downloadstatus) | - |
| [`drone`](#query-drone) | 查询当前检测到的无人机信息。 |
| [`drone_event_log`](#query-drone-event-log) | 查询无人机事件日志。 |
| [`droneAdsB`](#query-droneadsb) | ADS-B（飞行信息）。 |
| [`droneIDs`](#query-droneids) | 根据 ID 字符串的一部分从历史事件中查询无人机 ID，支持模糊查询。 |
| [`dronetraces`](#query-dronetraces) | 查询历史事件中的无人机轨迹信息。 |
| [`dronetracesByTime`](#query-dronetracesbytime) | 按时间段查询历史事件中的无人机轨迹信息。 |
| [`dronetypes`](#query-dronetypes) | 从历史事件中查询无人机类型，支持模糊查询。 |
| [`engineUpgradeRecords`](#query-engineupgraderecords) | 查询无人机库本地升级记录。 |
| [`event_log`](#query-event-log) | 查询无人机事件日志和设备事件日志。 |
| [`events`](#query-events) | 已弃用。查询指定时间段内的历史无人机事件。 |
| [`events_aggregation`](#query-events-aggregation) | 按无人机类型和信号特征签名聚合查询无人机历史事件。结果可按发现时间、持续时间、无人机 ID、无人机类型排序，默认按发现时间。 |
| [`events_by_paging`](#query-events-by-paging) | 查询无人机历史事件。结果可按发现时间、持续时间、无人机 ID、无人机类型排序，默认按发现时间。 |
| [`get_gvs_conf`](#query-get-gvs-conf) | - |
| [`getSaveLogStat`](#query-getsavelogstat) | - |
| [`getSigParseImage`](#query-getsigparseimage) | - |
| [`gfskData`](#query-gfskdata) | - |
| [`gfskProto`](#query-gfskproto) | - |
| [`gvsAutocaliProgress`](#query-gvsautocaliprogress) | 以百分比形式查询自动校准进度。 |
| [`gvsAutotrainProgress`](#query-gvsautotrainprogress) | 以百分比形式查询自动训练进度。 |
| [`gvsBgLearning`](#query-gvsbglearning) | 背景学习是否已启用。 |
| [`gvsCaliPosList`](#query-gvscaliposlist) | 自动校准或手动校准时查询校准位置列表。 |
| [`gvsModelList`](#query-gvsmodellist) | 查询自动训练模型列表。 |
| [`gvsStreamers`](#query-gvsstreamers) | 查询指定 GVS 设备 ID 的摄像头视频流；如果 ID 为空，则返回全部摄像头视频流。 |
| [`gvsTrainingImages`](#query-gvstrainingimages) | 获取无人机训练图像列表。 |
| [`JammerCooldownStatus`](#query-jammercooldownstatus) | 获取干扰器冷却状态。 |
| [`linkNodeList`](#query-linknodelist) | - |
| [`ListSigRecords`](#query-listsigrecords) | 查询信号录制列表。 |
| [`localPatchInfo`](#query-localpatchinfo) | 查询可用于切换的本地补丁。 |
| [`nodes`](#query-nodes) | - |
| [`notify`](#query-notify) | - |
| [`PackageVersionOnline`](#query-packageversiononline) | 获取在线最新安装包版本。 |
| [`profileAliasList`](#query-profilealiaslist) | 查询无人机类型别名列表。 |
| [`profileList`](#query-profilelist) | 查询无人机属性列表。 |
| [`profilePatternList`](#query-profilepatternlist) | 查询用于匹配无人机 ID 的模式列表。 |
| [`radarTarget`](#query-radartarget) | 根据 ID 查询当前检测到的雷达目标；如果未提供 ID，则返回全部当前检测到的雷达目标。 |
| [`report`](#query-report) | 查询无人机事件统计报告信息。 |
| [`screenshot`](#query-screenshot) | - |
| [`sensor`](#query-sensor) | - |
| [`skySegmenter`](#query-skysegmenter) | 查询摄像头设备天空分割算法结果。 |
| [`spdReport`](#query-spdreport) | - |
| [`spoofStatus`](#query-spoofstatus) | - |
| [`startDownload`](#query-startdownload) | - |
| [`storage`](#query-storage) | - |
| [`sysCapability`](#query-syscapability) | 查询设备干扰能力（例如 Wideband、Smart-II）。 |
| [`time`](#query-time) | 查询设备当前系统时间。 |
| [`timeZone`](#query-timezone) | 查询设备当前系统时区以及全部时区列表。 |
| [`unknownSignal`](#query-unknownsignal) | - |
| [`unlinkNodeList`](#query-unlinknodelist) | - |
| [`upgrade`](#query-upgrade) | 查询可用于升级的本地版本。 |
| [`UpgradeStatusOnline`](#query-upgradestatusonline) | 获取在线升级状态：<br>"UpgradeStatusIdle"：升级任务未启动或已完成。<br>"UpgradeStatusDownloading"：正在下载升级文件。<br>"UpgradeStatusDownloadErr"：下载升级文件时发生错误。<br>"UpgradeStatusUnpacking"：正在解压升级文件。<br>"UpgradeStatusUnpackErr"：解压升级文件时发生错误。<br>"UpgradeStatusDoUpgrading"：正在执行升级过程。<br>"UpgradeStatusDoUpgradeErr"：升级过程中发生错误。<br>"UpgradeStatusRestarting"：升级完成后系统正在重启。 |
| [`version`](#query-version) | 查询设备当前版本信息。 |
| [`vsgevent`](#query-vsgevent) | - |
| [`vsgevents`](#query-vsgevents) | - |
| [`vsgeventsimage`](#query-vsgeventsimage) | - |
| [`whitelist`](#query-whitelist) | 查询无人机白名单列表信息。 |
| [`widebandJammer`](#query-widebandjammer) | - |
| [`widebandJammer2`](#query-widebandjammer2) | 查询宽带干扰器状态（0: 不可用，1: 空闲，2: 忙碌）。 |
| [`wifilist`](#query-wifilist) | 查询指定类型的 WiFi 列表信息，类型可为 Active、Inactive、Background。 |
| [`wifiStatus`](#query-wifistatus) | 查询 WiFi 状态。 |

### Mutation

| 接口名称 | 接口描述 |
| --- | --- |
| [`addBlacklist`](#mutation-addblacklist) | 将指定无人机添加至黑名单。 |
| [`addWhitelist`](#mutation-addwhitelist) | 将指定无人机添加至白名单。 |
| [`adjustbandAttack`](#mutation-adjustbandattack) | 使用可调频段干扰器执行干扰打击。 |
| [`airDefenceArea`](#mutation-airdefencearea) | 添加或移除防空区域。 |
| [`attack`](#mutation-attack) | 对指定无人机执行干扰打击。 |
| [`autoAttack`](#mutation-autoattack) | 切换自动打击开关状态。 |
| [`camControl`](#mutation-camcontrol) | 控制摄像头移动。 |
| [`camLocateControl`](#mutation-camlocatecontrol) | 选择摄像头区域。 |
| [`camSetPTZ`](#mutation-camsetptz) | 设置摄像头 PTZ。 |
| [`clearLogs`](#mutation-clearlogs) | 重置所有日志并重新开始记录。 |
| [`clearStorage`](#mutation-clearstorage) | 清空设备内部存储。 |
| [`control`](#mutation-control) | 接管功能专用的无人机控制器（执行接管操作）。 |
| [`ctrl_landing`](#mutation-ctrl-landing) | 对指定无人机执行受控降落（为 true 时启动，为 false 时停止）。 |
| [`deleteBlacklist`](#mutation-deleteblacklist) | 将无人机从黑名单移除。 |
| [`deleteEvents`](#mutation-deleteevents) | 删除无人机事件（软删除）。 |
| [`deleteEventsByID`](#mutation-deleteeventsbyid) | 根据无人机 ID 和类型删除无人机事件。 |
| [`deleteEventVideo`](#mutation-deleteeventvideo) | 根据无人机 ID 和类型删除无人机事件。 |
| [`deleteWhitelist`](#mutation-deletewhitelist) | 将无人机从白名单移除。 |
| [`detectingBands`](#mutation-detectingbands) | 启用或禁用某个侦测频段。 |
| [`device`](#mutation-device) | 设备设置。 |
| [`deviceTest`](#mutation-devicetest) | 在所有设备上启动或停止自检。 |
| [`dfgun`](#mutation-dfgun) | 查打枪（DFGun）的杂项配置。 |
| [`dhcpEnable`](#mutation-dhcpenable) | 设置 DHCP 开关状态（若关闭，其他字段均忽略）。 |
| [`directionalWBAttack`](#mutation-directionalwbattack) | 切换定向宽带干扰器的启用 / 禁用状态。 |
| [`drone`](#mutation-drone) | 设置无人机属性。 |
| [`drone_profile`](#mutation-drone-profile) | 添加或移除无人机属性配置。 |
| [`droneAdsB`](#mutation-droneadsb) | 启用或禁用 ADS-B（航空器飞行信息）功能。 |
| [`droneProfileAlias`](#mutation-droneprofilealias) | 为指定无人机类型添加或移除别名。 |
| [`droneProfilePattern`](#mutation-droneprofilepattern) | 添加或移除无人机正则匹配模式。 |
| [`droneSub`](#mutation-dronesub) | 订阅无人机属性更新。 |
| [`falseAlarmInvalid`](#mutation-falsealarminvalid) | 将摄像头事件标记为无效。 |
| [`gfsk`](#mutation-gfsk) | - |
| [`gvsAutoCalibration`](#mutation-gvsautocalibration) | GVS 自动校准。 |
| [`gvsAutoCalibrationAdjust`](#mutation-gvsautocalibrationadjust) | GVS 自动校准。 |
| [`gvsAutoTrain`](#mutation-gvsautotrain) | GVS 自动训练。 |
| [`gvsBgLearning`](#mutation-gvsbglearning) | 切换背景学习模式。 |
| [`gvsCalibrationCheck`](#mutation-gvscalibrationcheck) | 执行 GVS 校准检查。 |
| [`gvsCalibrationCheckCheck`](#mutation-gvscalibrationcheckcheck) | GVS 校准检查。 |
| [`gvsCalibrationCheckSelect`](#mutation-gvscalibrationcheckselect) | GVS 校准检查时选择图像。 |
| [`gvsFocusCalibration`](#mutation-gvsfocuscalibration) | 对 GVS 设备执行焦距校准。<br>该操作用于控制指定摄像头（带索引的广角（wide）或窄角（narrow）摄像头）的焦距校准流程。<br>在样本采集期间，系统会以摄像头 SN 和温度作为键记录焦距数据；如果未提供温度，则使用配置中的设备当前温度。<br>预置位动作要求存在且仅存在一个距离超过 500 米的地标，生成的预置位会被保存为校准参考。<br>Orient 动作会将 PTZ 转向该校准后的预置位方向。 |
| [`gvsHeadingCalibration`](#mutation-gvsheadingcalibration) | GVS 航向校准。 |
| [`gvsManualCalibration`](#mutation-gvsmanualcalibration) | GVS 手动校准。 |
| [`gvsManualCalibrationAdvanced`](#mutation-gvsmanualcalibrationadvanced) | GVS 手动校准。 |
| [`gvsWorkMode`](#mutation-gvsworkmode) | - |
| [`markFalseAlarm`](#mutation-markfalsealarm) | 将无人机事件标记为误报。 |
| [`markFalseAlarmByID`](#mutation-markfalsealarmbyid) | 将无人机事件标记为误报。 |
| [`node`](#mutation-node) | - |
| [`powerMode`](#mutation-powermode) | 设置电源模式，仅适用于便携设备。 |
| [`pullDroneVideo`](#mutation-pulldronevideo) | 播放无人机模拟图传（FPV）视频。 |
| [`remove_fake_drone`](#mutation-remove-fake-drone) | 移除伪目标无人机。 |
| [`reset`](#mutation-reset) | 重置设备。 |
| [`rollbackPatch`](#mutation-rollbackpatch) | 切换或升级 UI 版本。 |
| [`saveLogs`](#mutation-savelogs) | - |
| [`sendSkySegmenterResults`](#mutation-sendskysegmenterresults) | 发送分割结果。 |
| [`set_gvs_conf`](#mutation-set-gvs-conf) | - |
| [`set_pan_tilt`](#mutation-set-pan-tilt) | 摄像头云台参数设置。 |
| [`set_sensor_mode`](#mutation-set-sensor-mode) | 传感器模式设置。 |
| [`set_vsg_license`](#mutation-set-vsg-license) | 设置传感器许可证。 |
| [`setControllerLicense`](#mutation-setcontrollerlicense) | 设置控制器许可证。 |
| [`setGeoLocation`](#mutation-setgeolocation) | 设置设备位置，不做持久化。 |
| [`setTime`](#mutation-settime) | 设置系统时间。 |
| [`signalCap`](#mutation-signalcap) | 信号采集功能。 |
| [`signalRec`](#mutation-signalrec) | 信号录制功能。 |
| [`sigParse`](#mutation-sigparse) | 启动信号解析任务。 |
| [`spd`](#mutation-spd) | 频谱显示设置。 |
| [`spoofer_switch`](#mutation-spoofer-switch) | 诱骗器设置。 |
| [`stageReset`](#mutation-stagereset) | 重置定向干扰器转台位置。 |
| [`startTracking`](#mutation-starttracking) | 按无人机 ID 开始跟踪。 |
| [`startTrackingTarget`](#mutation-starttrackingtarget) | 按目标 ID 开始跟踪。 |
| [`stopTrackingByCamId`](#mutation-stoptrackingbycamid) | 停止指定摄像头 ID 对应的 GVS 无人机跟踪。 |
| [`stopTrackingByDroneId`](#mutation-stoptrackingbydroneid) | 停止指定无人机 ID 的跟踪任务。 |
| [`takeover`](#mutation-takeover) | 接管指定无人机控制权。 |
| [`tdoa_track`](#mutation-tdoa-track) | 启用或禁用对无人机的 TDOA 跟踪。 |
| [`time`](#mutation-time) | 设置时间；当存在 auto 参数时，setTime 参数无效。 |
| [`timeZone`](#mutation-timezone) | 设置时区。 |
| [`toa_measure`](#mutation-toa-measure) | 启用或禁用对无人机的 TOA 测量。 |
| [`unknownWifi`](#mutation-unknownwifi) | 为未知 WiFi 无人机添加标签。 |
| [`upgradeDefaultDroneModelLibrary`](#mutation-upgradedefaultdronemodellibrary) | 将无人机模型库回滚到默认版本。 |
| [`upgradeDroneModelLibrary`](#mutation-upgradedronemodellibrary) | 升级无人机库。 |
| [`UpgradeOnline`](#mutation-upgradeonline) | 在线升级到最新版本。 |
| [`upgradePatch`](#mutation-upgradepatch) | 升级补丁包。 |
| [`upgradeTo`](#mutation-upgradeto) | 升级到一个已存在的本地版本。 |
| [`versionPackage`](#mutation-versionpackage) | 从文件中解包版本包。 |
| [`vsgCollect`](#mutation-vsgcollect) | VSG 采集。 |
| [`wideband_attack`](#mutation-wideband-attack) | 切换宽带干扰器的启用 / 禁用状态。 |
| [`wifiBgLearning`](#mutation-wifibglearning) | 开始或停止对背景 WiFi 信号的学习。 |
| [`wifiConnect`](#mutation-wificonnect) | - |
| [`wifiRescan`](#mutation-wifirescan) | - |
| [`wifiStatus`](#mutation-wifistatus) | - |
| [`withdrawFalseAlarm`](#mutation-withdrawfalsealarm) | 撤回误报事件。 |

## Query 接口

<a id="query-airdefencearea"></a>
### `airDefenceArea`

- 接口类型：`Query`
- 返回类型：`[areaDefenceType]`
- 接口描述：查询防空区域；如果未设置区域则返回空。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：区域防御

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `data` | jsonStrType | 防空区域 |


<a id="query-autoattack"></a>
### `autoAttack`

- 接口类型：`Query`
- 返回类型：`Boolean`
- 接口描述：查询自动打击开关状态。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="query-autoattackconfig"></a>
### `autoAttackConfig`

- 接口类型：`Query`
- 返回类型：`AutoAttackConfig`
- 接口描述：查询自动打击配置。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：自动打击配置

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `on` | Boolean | - |
| `saEnabled` | Boolean | 是否启用精准打击 |
| `wbEnabled` | Boolean | 是否启用宽带打击 |
| `dirWbEnabled` | Boolean | 是否启用定向打击 |
| `spfEnabled` | Boolean | 是否启用 GNSS 诱骗器 |
| `protectWhite` | Boolean | 是否保护白名单无人机 |
| `naviEnabled` | Boolean | 是否启用导航防御 |
| `naviBand12Enabled` | Boolean | 是否启用导航防御 (1.2GHz) |
| `naviBand15Enabled` | Boolean | 是否启用导航防御 (1.5GHz) |
| `timeRanges` | [[String]] | []any{} | 每日时间范围列表（支持跨天），格式：[[开始时间，结束时间], ...]，时间格式为 HH:mm:ss。 |
| `allJammingOn` | Boolean | 是否开启所有频段的干扰器 |


<a id="query-availableupgrade"></a>
### `availableUpgrade`

- 接口类型：`Query`
- 返回类型：`img.VersionGraphType`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

暂未解析到返回字段定义。


<a id="query-blacklist"></a>
### `blacklist`

- 接口类型：`Query`
- 返回类型：`[blacklist]`
- 接口描述：查询无人机黑名单列表信息。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：黑名单

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 无人机的唯一 ID |
| `dronetype` | String | 无人机类型 |
| `alias` | String | 来自黑名单的无人机自定义别名 |
| `description` | String | 无人机详细描述 |
| `created_time` | String | 无人机创建时间 |


<a id="query-cameraposts"></a>
### `cameraPosts`

- 接口类型：`Query`
- 返回类型：`[cameraPost]`
- 接口描述：获取用于遮罩/取消遮罩的摄像头点位。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |

#### 返回值定义

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `cameraName` | String | - |
| `bgFilepath` | String | - |
| `positions` | [`[[cameraPosition]]`](#query-cameraposts-field-positions) | - |
| `showReverse` | Boolean | - |
| `isNight` | Boolean | - |

##### 子对象字段展开

<a id="query-cameraposts-field-positions"></a>
###### `positions` (`[[cameraPosition]]`)

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ptz` | `ptz` | - |
| `bgFilename` | `String` | - |
| `maskEnabled` | `Boolean` | - |


<a id="query-cammanufacturer"></a>
### `camManufacturer`

- 接口类型：`Query`
- 返回类型：`String`
- 接口描述：获取摄像头厂商信息。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `type` | `String` | - | 摄像头类型，取值范围：wide、narrow |

#### 返回值定义

标量类型，无字段定义。


<a id="query-camptz"></a>
### `camPTZ`

- 接口类型：`Query`
- 返回类型：`ptz`
- 接口描述：获取摄像头 PTZ。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `type` | `String` | - | 摄像头类型，取值范围：wide、narrow |

#### 返回值定义

- 返回值说明：摄像头 PTZ

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `pan` | Float | 方位角 |
| `tilt` | Float | 俯仰角 |
| `zoom` | Float | 变焦 |


<a id="query-check"></a>
### `check`

- 接口类型：`Query`
- 返回类型：`upgradeType`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `pkg_size` | `Float` | - | 安装包大小 |

#### 返回值定义

- 返回值说明：升级对象类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `prepare_status` | String | 升级目录准备状态 |
| `upgrade_status` | String | 升级状态 |
| `local_versions` | [`[versions]`](#query-check-field-local-versions) | 有效的本地版本 |
| `free_space` | Int | 新升级可用空间（单位 Mbytes） |
| `has_enough_space` | Boolean | 是否有足够空间用于新升级 |

##### 子对象字段展开

<a id="query-check-field-local-versions"></a>
###### `local_versions` (`[versions]`)

- 字段说明：本地版本状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `version_id` | `String` | 版本的唯一 ID |
| `version_status` | `String` | 版本状态及有效性 |
| `version_publish_time` | `String` | 发布时间 |


<a id="query-detectingbands"></a>
### `detectingBands`

- 接口类型：`Query`
- 返回类型：`DetectingBands`
- 接口描述：查询设备侦测频段状态（0: 不可用，1: 禁用，2: 启用）。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：侦测频段状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `band24` | Int | 2.4Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band58` | Int | 5.8Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band18` | Int | 1.8Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band14` | Int | 1.4Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band12` | Int | 1.2Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band9` | Int | 900MHz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band4` | Int | 433MHz 频段状态，0:不可用，1:禁用，2:启用。 |
| `bandext` | Int | 扩展频段状态，0:不可用，1:禁用，2:启用。 |
| `bandext8` | Int | 6-8GHz 频段状态，0:不可用，1:禁用，2:启用。 |
| `Boost24` | Int | 已弃用。测试功能，0:不可用，1:禁用，2:启用。 |


<a id="query-device-event-log"></a>
### `device_event_log`

- 接口类型：`Query`
- 返回类型：`DeviceEventLogPaging`
- 接口描述：查询设备事件日志。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `target` | `String` | - | 待查询的无人机 ID |
| `begin_time` | `String` | - | 事件开始时间 |
| `end_time` | `String` | - | 事件结束时间 |
| `type` | `String` | - | 事件类型 |
| `sub_type` | `String` | - | 事件子类型 |
| `action` | `String` | - | 事件动作 |
| `dev_id` | `String` | - | 事件的设备 ID |
| `offset` | `Int` | 0 | - |
| `limit` | `Int` | 15 | - |

#### 返回值定义

- 返回值说明：设备事件日志

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `count` | Int | 记录条数 |
| `data` | [`[EventLog]`](#query-device-event-log-field-data) | - |

##### 子对象字段展开

<a id="query-device-event-log-field-data"></a>
###### `data` (`[EventLog]`)

- 字段说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `target` | `String` | 无人机 ID |
| `type` | `String` | 事件类型 |
| `sub_type` | `String` | 事件子类型 |
| `action` | `String` | 事件动作日志 |
| `dev_id` | `String` | 事件的设备 ID |
| `source` | `String` | 事件来源 |
| `fault_reason` | `String` | 故障信息 |
| `time` | `DateTime` | 时间 |
| `applied` | `Boolean` | 是否已应用 |
| `meta` | `String` | 该记录的元数据 |
| `param` | `String` | 该记录的参数数据 |


<a id="query-devices"></a>
### `devices`

- 接口类型：`Query`
- 返回类型：`[Devices]`
- 接口描述：查询指定设备信息（例如 controller、engine、sensor、jammer）。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |

#### 返回值定义

- 返回值说明：设备实体

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 设备的 ID |
| `class` | String | 当前设备名称 |
| `state` | String | 当前设备状态：停止、运行中、降级运行、更新中 |
| `faults` | String | 当前设备的故障信息 |
| `status` | jsonStrType | 当前设备状态 |
| `config` | jsonStrType | 当前设备配置 |
| `scv_status` | jsonStrType | 传感器上的 SCV |
| `rec_status` | String | 引擎设备的信号录制状态 |
| `sigCap_status` | String | 引擎设备的信号采集状态 |
| `gps_fixed` | Boolean | GPS 是否已定位锁定 |
| `toc` | jsonStrType | 连接时间 |
| `history` | [`[DevicesHistory]`](#query-devices-field-history) | 连接丢失历史 |
| `node` | String | 设备所属节点 |
| `test_status` | jsonStrType | 当前设备测试状态 |

##### 子对象字段展开

<a id="query-devices-field-history"></a>
###### `history` (`[DevicesHistory]`)

- 字段说明：设备连接历史信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `dev_id` | `String` | 设备 ID |
| `dev_type` | `String` | 设备类型 |
| `time_of_connection` | `String` | 连接时间 |
| `time_of_disconnection` | `String` | 断开连接时间 |


<a id="query-devicestat"></a>
### `deviceStat`

- 接口类型：`Query`
- 返回类型：`[DeviceStat]`
- 接口描述：查询设备管理中的引擎运行状态以及收发包状态信息。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |

#### 返回值定义

- 返回值说明：设备统计

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 设备的 ID |
| `class` | String | 当前设备名称 |
| `pkt_stat` | jsonStrType | 按各传感器统计的引擎报文数据 |
| `run_stat` | jsonStrType | 来自引擎的运行状态 |


<a id="query-dfgun"></a>
### `dfgun`

- 接口类型：`Query`
- 返回类型：`dfgunStatus`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：查打枪状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `mode` | Int | 当前模式 |
| `rssi` | Int | 0~100 |
| `heading` | Float | 查打枪的航向 |
| `freq` | Int | 频率 |
| `droneid` | String | 无人机 ID |
| `dBm` | Float | dBm |
| `attack_freq_low` | Int | 可调功率放大器 |
| `attack_freq_high` | Int | 可调功率放大器 |


<a id="query-dhcpstatus"></a>
### `dhcpStatus`

- 接口类型：`Query`
- 返回类型：`dhcp`
- 接口描述：查询 DHCP 状态。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：DHCP 信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `on` | Boolean | DHCP 开关；如果关闭，则其他所有字段都应忽略 |
| `status` | Int | DHCP 状态，0: 未连接，1: 已连接 |
| `ip` | String | IP 地址 |
| `netmask` | String | 子网掩码 |
| `gateway` | String | 网关 |


<a id="query-downloadstatus"></a>
### `downloadStatus`

- 接口类型：`Query`
- 返回类型：`img.WorkStatusGraphType`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

暂未解析到返回字段定义。


<a id="query-drone"></a>
### `drone`

- 接口类型：`Query`
- 返回类型：`[Drone]`
- 接口描述：查询当前检测到的无人机信息。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |

#### 返回值定义

- 返回值说明：无人机信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 无人机的唯一 ID |
| `name` | String | 无人机名称 |
| `custom_name` | String | 来自黑名单或白名单的无人机自定义别名 |
| `description` | String | 无人机描述 |
| `image` | String | 无人机图像 |
| `state` | String | 无人机状态 |
| `direction` | Float | 无人机航向角。365 表示无效值 |
| `distance` | Float | 无人机距离 |
| `rc_distance` | Float | 无人机飞手距离，`-1` 表示无效值 |
| `longitude` | Float | 无人机经度；如果 `航向` 无效，则该值无效 |
| `latitude` | Float | 无人机纬度；如果 `方向` 无效，则该值无效 |
| `height` | Float | 无人机离地高度；如果 `航向` 无效，则该值无效 |
| `altitude` | Float | 无人机与海平面的垂直距离；如果 `航向` 无效，则该值无效 |
| `speed` | Float | 无人机速度(m/s)；如果 `航向` 无效，则该值无效 |
| `whitelisted` | Boolean | 无人机是否在白名单中 |
| `blacklisted` | Boolean | 无人机是否在黑名单中 |
| `confirmed` | Boolean | 无人机是否已确认，还是仅为可疑目标 |
| `reliability` | Int | 该检测结果的可信度。0 表示无效值 |
| `can_attack` | Boolean | 无人机是否可被打击 |
| `can_takeover` | Boolean | 无人机是否可被接管 |
| `attacking` | Boolean | 无人机是否正在被打击 |
| `directional_attack_state` | Int | 定向打击状态：`0: 空闲；1: 跟踪中；2: 已打击` |
| `attacking_ttl` | Int | 无人机处于打击状态时的打击时长，负值表示倒计时 |
| `can_tdoa` | Boolean | 无人机是否可通过 TDOA 进行跟踪 |
| `can_toa` | Boolean | 无人机是否可进行 TOA 测量 |
| `tdoa_tracking` | Boolean | 无人机是否处于 TDOA 跟踪状态 |
| `toa_measuring` | Boolean | 无人机是否处于 TOA 测量中 |
| `can_ctrl_landing` | Boolean | 无人机是否可执行受控降落 |
| `can_direction_finding` | Boolean | 无人机是否可被引导 |
| `ctrl_landing` | Boolean | 无人机是否处于受控降落中 |
| `in_ada` | Int | 无人机是否位于防空区域 (电子围栏) 内。0: 不可用，1: 不在区域内，2: 在预警区，3: 在防御区 |
| `created_time` | DateTime | 创建时间 |
| `deleted_time` | DateTime | 删除时间 |
| `lastseen_time` | DateTime | 最后出现时间 |
| `last_detected_time` | Float | 引擎最后一次检测到无人机信号的 UTC 时间（毫秒）。0: 不可用 |
| `lastseen` | String | 最后出现时间（已弃用） |
| `detectors` | [String] | 探测器列表，项包括：RID、CRPC、DroneID、摄像头、雷达 |
| `seen_sensor` | [`[SignalObject]`](#query-drone-field-seen-sensor) | 可看到该无人机的传感器 |
| `df_sensor` | String | 测向传感器 ID |
| `attack_bands` | [Int] | 待打击频段列表，单位 kHz |
| `attack_type` | String | 打击类型列表 |
| `tracing` | [`Tracing`](#query-drone-field-tracing) | 无人机轨迹 |
| `localization` | [`[GeoPoint]`](#query-drone-field-localization) | 无人机轨迹（已弃用） |
| `initial_location` | [`GeoPoint`](#query-drone-field-initial-location) | 无人机初始位置。`210` 表示无效值 |
| `rc_location` | [`GeoPoint`](#query-drone-field-rc-location) | RC 位置。`210` 表示无效值 |
| `home_position` | [`GeoPoint`](#query-drone-field-home-position) | 无人机起飞点位置。`210` 表示无效值 |
| `link_id` | String | 无人机关联 ID |
| `has_duplicate` | Boolean | true 表示伪目标无人机已被隐藏 |
| `jamming_conflicts` | [String] | 对该无人机实施干扰时将受影响的无人机 ID 列表 |
| `tracking_video` | String | 跟踪视频文件 |
| `has_screenshot` | Boolean | 无人机是否有截图 |
| `screenshot` | String | 该无人机的最新截图，JPG 格式 |
| `secret` | String | - |
| `current_ptz` | [`CurrentPtz`](#query-drone-field-current-ptz) | 该无人机最后一次被看到时的实时 PTZ |
| `camera_trackings` | [`[CameraTracking]`](#query-drone-field-camera-trackings) | 摄像头跟踪列表 |
| `can_camera_tracking` | Boolean | 无人机是否可由摄像头引导 |
| `extra_data` | String | 附加数据 |
| `operator_id` | String | remoteID 数据的操作员 ID |
| `can_drone_video` | Boolean | 无人机是否可显示模拟视频 |
| `video_sensor_id` | String | 播放模拟图传时占用的传感器 |
| `track_direction` | Int | 无人机航迹方向表示为相对于地理北顺时针测量的 0–360° 角度，表示无人机纵轴在水平面内的方向。取值 365 表示航向无效。 |

##### 子对象字段展开

<a id="query-drone-field-seen-sensor"></a>
###### `seen_sensor` (`[SignalObject]`)

- 字段说明：信号对象类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sensor_id` | `String` | 上报该信息的传感器 ID |
| `snr_dB` | `Float` | 信号的 SNR |
| `detected_freq_khz` | `Int` | 检测到的频率 |
| `bandwidth_khz` | `Int` | 信号带宽 |
| `signal_dbm` | `Int` | 天线处 RF 信号功率，相对 1 毫瓦的分贝差 |
| `noise_dbm` | `Int` | 天线处 RF 噪声功率，相对 1 毫瓦的分贝差 |
| `port` | `String` | VSG 边界框信息 |

<a id="query-drone-field-tracing"></a>
###### `tracing` (`Tracing`)

- 字段说明：无人机实时轨迹

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `origin` | `GeoPoint` | 起点地理位置 |
| `points` | `[[Float]]` | 轨迹点 |
| `lastlen` | `Int` | 最后一段点的长度 |

<a id="query-drone-field-localization"></a>
###### `localization` (`[GeoPoint]`)

- 字段说明：地理坐标点

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `lat` | `Float` | 纬度 |
| `lng` | `Float` | 经度 |

<a id="query-drone-field-initial-location"></a>
###### `initial_location` (`GeoPoint`)

- 字段说明：地理坐标点

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `lat` | `Float` | 纬度 |
| `lng` | `Float` | 经度 |

<a id="query-drone-field-rc-location"></a>
###### `rc_location` (`GeoPoint`)

- 字段说明：地理坐标点

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `lat` | `Float` | 纬度 |
| `lng` | `Float` | 经度 |

<a id="query-drone-field-home-position"></a>
###### `home_position` (`GeoPoint`)

- 字段说明：地理坐标点

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `lat` | `Float` | 纬度 |
| `lng` | `Float` | 经度 |

<a id="query-drone-field-current-ptz"></a>
###### `current_ptz` (`CurrentPtz`)

- 字段说明：摄像头使用的当前 PTZ

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `pan` | `Float` | 方位角 |
| `tilt` | `Float` | 俯仰角 |
| `zoom` | `Float` | 变焦 |

<a id="query-drone-field-camera-trackings"></a>
###### `camera_trackings` (`[CameraTracking]`)

- 字段说明：跟踪状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `device_id` | `String` | 摄像头设备 ID，一个摄像头设备可能包含多个摄像头 |
| `camera_name` | `String` | 摄像头名称，例如 wide_1、wide_2、wide_3 |
| `ip` | `String` | 视频流服务器的 IP 地址 |
| `status` | `Int` | 跟踪状态，1: 搜索中，2: 跟踪中(目标锁定)，3: 目标丢失，4: 失败 |
| `direction` | `Int` | 无人机航向角。365 表示无效值 |


<a id="query-drone-event-log"></a>
### `drone_event_log`

- 接口类型：`Query`
- 返回类型：`[EventLog]`
- 接口描述：查询无人机事件日志。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `target` | `String` | - | 待查询的无人机 ID |
| `begin_time` | `String` | - | 无人机事件开始时间 |
| `end_time` | `String` | - | 无人机事件结束时间 |

#### 返回值定义

- 返回值说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `target` | String | 无人机 ID |
| `type` | String | 事件类型 |
| `sub_type` | String | 事件子类型 |
| `action` | String | 事件动作日志 |
| `dev_id` | String | 事件的设备 ID |
| `source` | String | 事件来源 |
| `fault_reason` | String | 故障信息 |
| `time` | DateTime | 时间 |
| `applied` | Boolean | 是否已应用 |
| `meta` | String | 该记录的元数据 |
| `param` | String | 该记录的参数数据 |


<a id="query-droneadsb"></a>
### `droneAdsB`

- 接口类型：`Query`
- 返回类型：`AdsBStatus`
- 接口描述：ADS-B（飞行信息）。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：ADS-B 状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `support` | Boolean | 是否支持 |
| `switch` | Boolean | 开关状态 |
| `drone` | [`[DroneAdsB]`](#query-droneadsb-field-drone) | 无人机列表 |

##### 子对象字段展开

<a id="query-droneadsb-field-drone"></a>
###### `drone` (`[DroneAdsB]`)

- 字段说明：航空器 ADS-B 信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `String` | 航空器的 ICAO24 |
| `registration` | `String` | 航空器注册号 |
| `manufacturer` | `String` | 航空器制造商 |
| `model` | `String` | 航空器型号 |
| `typecode` | `String` | 航空器型号代码 |
| `owner` | `String` | 航空器所有者 |
| `longitude` | `Float` | 航空器经度 |
| `latitude` | `Float` | 航空器纬度 |
| `height` | `Float` | 航空器高度 |
| `speed` | `Float` | 航空器速度(m/s) |
| `detected_freq_khz` | `Int` | ADS-B 频率 |
| `confirmed` | `Boolean` | 航空器是否已确认，还是仅为可疑目标 |
| `yaw_angle` | `Float` | 航空器偏航角 |


<a id="query-droneids"></a>
### `droneIDs`

- 接口类型：`Query`
- 返回类型：`[String]`
- 接口描述：根据 ID 字符串的一部分从历史事件中查询无人机 ID，支持模糊查询。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `pattern` | `String` | - | 用于模糊搜索的模式 |
| `limit` | `Int` | - | 最大记录条数 |
| `begin_time` | `String` | - | 查询开始时间 |
| `end_time` | `String` | - | 查询结束时间 |

#### 返回值定义

标量类型，无字段定义。


<a id="query-dronetraces"></a>
### `dronetraces`

- 接口类型：`Query`
- 返回类型：`[DroneTrace]`
- 接口描述：查询历史事件中的无人机轨迹信息。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `from` | `Int` | - | - |
| `to` | `Int` | - | - |

#### 返回值定义

- 返回值说明：无人机历史轨迹

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `binding_id` | Int | 事件序号 |
| `id` | String | 无人机的唯一 ID |
| `drone_type` | String | 无人机类型 |
| `created_time` | DateTime | 创建时间 |
| `frequence` | String | 频率 |
| `points` | String | 基于中心点的轨迹点 |
| `center_lat` | String | 传感器中心纬度 |
| `center_lng` | String | 传感器中心经度 |
| `zoom` | Int | 地图默认缩放级别 |


<a id="query-dronetracesbytime"></a>
### `dronetracesByTime`

- 接口类型：`Query`
- 返回类型：`[DroneTrace]`
- 接口描述：按时间段查询历史事件中的无人机轨迹信息。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `begin_time` | `String` | - | [必填] 查询开始时间，RFC3399 格式：2006-01-02T15:04:05Z |
| `end_time` | `String` | - | [必填] 查询结束时间，RFC3399 格式：2006-01-02T15:04:05Z |

#### 返回值定义

- 返回值说明：无人机历史轨迹

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `binding_id` | Int | 事件序号 |
| `id` | String | 无人机的唯一 ID |
| `drone_type` | String | 无人机类型 |
| `created_time` | DateTime | 创建时间 |
| `frequence` | String | 频率 |
| `points` | String | 基于中心点的轨迹点 |
| `center_lat` | String | 传感器中心纬度 |
| `center_lng` | String | 传感器中心经度 |
| `zoom` | Int | 地图默认缩放级别 |


<a id="query-dronetypes"></a>
### `dronetypes`

- 接口类型：`Query`
- 返回类型：`[String]`
- 接口描述：从历史事件中查询无人机类型，支持模糊查询。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `pattern` | `String` | - | 用于模糊搜索的模式 |
| `all` | `Boolean` | false | 如果为 `true`，则先搜索所有类型，再搜索已有类型 |
| `limit` | `Int` | - | 最大记录条数 |
| `begin_time` | `String` | - | 查询开始时间 |
| `end_time` | `String` | - | 查询结束时间 |

#### 返回值定义

标量类型，无字段定义。


<a id="query-engineupgraderecords"></a>
### `engineUpgradeRecords`

- 接口类型：`Query`
- 返回类型：`[UpgradeEngineRecords]`
- 接口描述：查询无人机库本地升级记录。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：无人机库升级记录

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `version` | String | 无人机模型库版本 |
| `upgrade_time` | String | 无人机库升级时间 |


<a id="query-event-log"></a>
### `event_log`

- 接口类型：`Query`
- 返回类型：`[EventLog]`
- 接口描述：查询无人机事件日志和设备事件日志。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `target` | `String` | - | 待查询的无人机 ID |
| `type` | `String` | - | 无人机事件类型 |
| `sub_type` | `String` | - | 无人机事件子类型 |
| `begin_time` | `String` | - | 无人机事件开始时间 |
| `end_time` | `String` | - | 无人机事件结束时间 |

#### 返回值定义

- 返回值说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `target` | String | 无人机 ID |
| `type` | String | 事件类型 |
| `sub_type` | String | 事件子类型 |
| `action` | String | 事件动作日志 |
| `dev_id` | String | 事件的设备 ID |
| `source` | String | 事件来源 |
| `fault_reason` | String | 故障信息 |
| `time` | DateTime | 时间 |
| `applied` | Boolean | 是否已应用 |
| `meta` | String | 该记录的元数据 |
| `param` | String | 该记录的参数数据 |


<a id="query-events"></a>
### `events`

- 接口类型：`Query`
- 返回类型：`[Event]`
- 接口描述：已弃用。查询指定时间段内的历史无人机事件。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `from` | `Int` | - | 从该序号开始查询 |
| `drone_type` | `String` | - | 待查询的无人机类型 |
| `drone_id` | `String` | - | 待查询的无人机 ID |
| `begin_time` | `String` | - | 查询开始时间 |
| `end_time` | `String` | - | 查询结束时间 |

#### 返回值定义

- 返回值说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sequence` | Int | 事件序号 |
| `id` | String | 无人机的唯一 ID |
| `drone_type` | String | 无人机类型 |
| `image` | String | 无人机图像 |
| `created_time` | DateTime | 创建时间 |
| `deleted_time` | DateTime | 删除时间 |
| `frequence` | String | 频率 |
| `first_pos` | String | 首次发现位置 |
| `last_pos` | String | 最后发现位置 |
| `rc_pos` | String | 无人机飞手位置 |
| `attacked` | Boolean | 是否被打击 |
| `severity` | String | 严重级别：0: 不可用（unknown），1: 低，2: 中，3: 高 |
| `seen_sensors` | String | 由哪个传感器发现 |
| `is_false_alarm` | Boolean | 是否被标记为误报 |
| `false_alarm_type` | String | 误报类型[背景,鸟类,飞机,直升机,其他]，默认：其他 |
| `whitelisted` | Boolean | 是否为白名单无人机 |
| `blacklisted` | Boolean | 是否为黑名单无人机 |
| `has_screenshot` | Boolean | 是否有截图 |
| `siteLatitude` | Float | 站点纬度。`210` 表示无效 |
| `siteLongitude` | Float | 站点经度。`210` 表示无效 |
| `reliability` | Int | 该检测记录的可信度。0 表示无效值 |
| `invalid_time` | DateTime | 失效时间 |
| `video_records` | [`VideoRecordsType`](#query-events-field-video-records) | 视频信息，为空表示无视频 |
| `first_height` | Float | 首次发现位置高度。 |
| `last_height` | Float | 最后发现位置高度。 |
| `first_altitude` | Float | 首次发现位置海拔。 |
| `last_altitude` | Float | 最后发现位置海拔。 |
| `operator_id` | String | 无人机操作员 ID |

##### 子对象字段展开

<a id="query-events-field-video-records"></a>
###### `video_records` (`VideoRecordsType`)

- 字段说明：视频信息记录

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `videos` | `[VideoInfo]` | - |


<a id="query-events-aggregation"></a>
### `events_aggregation`

- 接口类型：`Query`
- 返回类型：`EventAggregation`
- 接口描述：按无人机类型和信号特征签名聚合查询无人机历史事件。结果可按发现时间、持续时间、无人机 ID、无人机类型排序，默认按发现时间。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `order` | `String` | desc | 数据排序，取值：`asc` 表示升序，`desc` 表示降序，默认：`desc` |
| `order_by` | `String` | created_time | 按该字段排序，取值：`created_time` 检测时间，`duration` 无人机持续时间，`drone_id` 无人机 ID，`drone_type` 无人机类型，`count` 无人机出现次数。默认：created_time |
| `offset` | `Int` | 0 | 从该字段开始查询，默认：0 |
| `limit` | `Int` | 10 | 每页记录条数，默认：10 |
| `drone_type` | `String` | - | 按无人机类型筛选 |
| `drone_id` | `String` | - | 按无人机 ID 筛选 |
| `pattern` | `String` | - | 匹配无人机 ID 或无人机类型 |
| `begin_time` | `String` | - | 查询开始时间 |
| `end_time` | `String` | - | 查询结束时间 |
| `min_duration` | `Int` | -1 | 允许的最短持续时间（秒），默认：禁用 |
| `max_duration` | `Int` | -1 | 允许的最长持续时间（秒），默认：禁用 |
| `data_num_limit` | `Boolean` | false | 是否限制返回的数据条数 |
| `filter_has_pos` | `Boolean` | - | 筛选包含位置数据的记录 |
| `filter_has_rc_pos` | `Boolean` | - | 筛选包含 RC 位置数据的记录 |
| `filter_has_trace` | `Boolean` | - | 筛选包含轨迹数据的记录 |
| `filter_attacked` | `Boolean` | - | 筛选被打击记录 |
| `filter_severity` | `[Severity]` | - | 筛选严重级别 |

#### 返回值定义

- 返回值说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `count` | Int | 记录条数 |
| `total_count` | Int | 记录总条数 |
| `data` | [`[EventPaging]`](#query-events-aggregation-field-data) | - |

##### 子对象字段展开

<a id="query-events-aggregation-field-data"></a>
###### `data` (`[EventPaging]`)

- 字段说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `count` | `Int` | 记录条数 |
| `data` | `[Event]` | - |


<a id="query-events-by-paging"></a>
### `events_by_paging`

- 接口类型：`Query`
- 返回类型：`EventPaging`
- 接口描述：查询无人机历史事件。结果可按发现时间、持续时间、无人机 ID、无人机类型排序，默认按发现时间。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `order` | `String` | desc | 数据排序，取值：`asc` 表示升序，`desc` 表示降序。默认：`desc` |
| `order_by` | `String` | created_time | 按该字段排序，取值：`created_time` 检测时间，`duration` 无人机持续时间，`drone_id` 无人机 ID，`drone_type` 无人机类型，默认：created_time |
| `offset` | `Int` | 0 | 从该字段开始查询，默认：0 |
| `limit` | `Int` | 10 | 每页记录条数，默认：10 |
| `drone_type` | `String` | - | 按无人机类型筛选 |
| `drone_id` | `String` | - | 按无人机 ID 筛选 |
| `pattern` | `String` | - | 匹配无人机 ID 或无人机类型 |
| `begin_time` | `String` | - | 查询开始时间 |
| `end_time` | `String` | - | 查询结束时间 |
| `min_duration` | `Int` | -1 | 允许的最短持续时间（秒），默认：禁用 |
| `max_duration` | `Int` | -1 | 允许的最长持续时间（秒），默认：禁用 |
| `is_false_alarm` | `Boolean` | false | 是否查看误报 |
| `filter_has_pos` | `Boolean` | - | 筛选包含位置数据的记录 |
| `filter_has_rc_pos` | `Boolean` | - | 筛选包含 RC 位置数据的记录 |
| `filter_has_trace` | `Boolean` | - | 筛选包含轨迹数据的记录 |
| `filter_attacked` | `Boolean` | - | 筛选被打击的记录 |
| `filter_severity` | `[Severity]` | - | 筛选严重级别 |

#### 返回值定义

- 返回值说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `count` | Int | 记录条数 |
| `data` | [`[Event]`](#query-events-by-paging-field-data) | - |

##### 子对象字段展开

<a id="query-events-by-paging-field-data"></a>
###### `data` (`[Event]`)

- 字段说明：无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sequence` | `Int` | 事件序号 |
| `id` | `String` | 无人机的唯一 ID |
| `drone_type` | `String` | 无人机类型 |
| `image` | `String` | 无人机图像 |
| `created_time` | `DateTime` | 创建时间 |
| `deleted_time` | `DateTime` | 删除时间 |
| `frequence` | `String` | 频率 |
| `first_pos` | `String` | 首次发现位置 |
| `last_pos` | `String` | 最后发现位置 |
| `rc_pos` | `String` | 无人机飞手位置 |
| `attacked` | `Boolean` | 是否被打击 |
| `severity` | `String` | 严重级别：0: 不可用（unknown），1: 低，2: 中，3: 高 |
| `seen_sensors` | `String` | 由哪个传感器发现 |
| `is_false_alarm` | `Boolean` | 是否被标记为误报 |
| `false_alarm_type` | `String` | 误报类型[背景,鸟类,飞机,直升机,其他]，默认：其他 |
| `whitelisted` | `Boolean` | 是否为白名单无人机 |
| `blacklisted` | `Boolean` | 是否为黑名单无人机 |
| `has_screenshot` | `Boolean` | 是否有截图 |
| `siteLatitude` | `Float` | 站点纬度。`210` 表示无效 |
| `siteLongitude` | `Float` | 站点经度。`210` 表示无效 |
| `reliability` | `Int` | 该检测记录的可信度。0 表示无效值 |
| `invalid_time` | `DateTime` | 失效时间 |
| `video_records` | `VideoRecordsType` | 视频信息，为空表示无视频 |
| `first_height` | `Float` | 首次发现位置高度。 |
| `last_height` | `Float` | 最后发现位置高度。 |
| `first_altitude` | `Float` | 首次发现位置海拔。 |
| `last_altitude` | `Float` | 最后发现位置海拔。 |
| `operator_id` | `String` | 无人机操作员 ID |


<a id="query-get-gvs-conf"></a>
### `get_gvs_conf`

- 接口类型：`Query`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |

#### 返回值定义

标量类型，无字段定义。


<a id="query-getsavelogstat"></a>
### `getSaveLogStat`

- 接口类型：`Query`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `deviceId` | `String` | - | 节点 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="query-getsigparseimage"></a>
### `getSigParseImage`

- 接口类型：`Query`
- 返回类型：`[String]`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `sensorId` | `String` | - | - |

#### 返回值定义

标量类型，无字段定义。


<a id="query-gfskdata"></a>
### `gfskData`

- 接口类型：`Query`
- 返回类型：`[GFSK]`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：GFSK 信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uid` | Int | GFSK 类型的唯一 ID |
| `protocol` | String | GFSK 协议 |
| `created_time` | DateTime | GFSK 的创建时间 |
| `chan_lis` | String | GFSK 的信道列表 |
| `bitrate` | Int | GFSK 的比特率 |
| `bandwidth` | Int | GFSK 的带宽 |
| `options` | String | GFSK 指定协议类型的属性 |


<a id="query-gfskproto"></a>
### `gfskProto`

- 接口类型：`Query`
- 返回类型：`ProtolcolType`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：获取 GFSK 信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `options` | [String] | 协议选项 |
| `A7106` | [String] | 协议 A706 |
| `CC2500` | [String] | 协议 CC2500 |
| `BK5811` | [String] | 协议 BK5811 |
| `CYRF6936` | [String] | 协议 CYRF6936 |
| `GFSK_Customized` | [String] | 协议 GFSK_Customized |


<a id="query-gvsautocaliprogress"></a>
### `gvsAutocaliProgress`

- 接口类型：`Query`
- 返回类型：`ProgressMsgType`
- 接口描述：以百分比形式查询自动校准进度。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |

#### 返回值定义

- 返回值说明：自动校准进度消息类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `details` | Int | 自动校准进度详情代码 0：停止 1：开始 2：完成 3：错误 |
| `percentage` | Int | 进度百分比 0~100 |
| `errorCode` | Int | 自动校准错误：0: 正常；1: 创建错误；2: 写入错误；3: 读取错误；4: PTZ 趋近错误；5: 获取 PTZ 错误；6: 采集错误；7: 计算失败；8: 连接错误；9: 取消；10: 超时 |


<a id="query-gvsautotrainprogress"></a>
### `gvsAutotrainProgress`

- 接口类型：`Query`
- 返回类型：`AutoTrainProgressMsgType`
- 接口描述：以百分比形式查询自动训练进度。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |

#### 返回值定义

- 返回值说明：自动训练进度消息类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `details` | Int | 自动训练进度详情代码 |
| `percentage` | Int | 自动训练进度百分比 0~100 |
| `errorCode` | Int | 自动训练错误 |


<a id="query-gvsbglearning"></a>
### `gvsBgLearning`

- 接口类型：`Query`
- 返回类型：`Boolean`
- 接口描述：背景学习是否已启用。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="query-gvscaliposlist"></a>
### `gvsCaliPosList`

- 接口类型：`Query`
- 返回类型：`[CaliPosMap]`
- 接口描述：自动校准或手动校准时查询校准位置列表。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |

#### 返回值定义

- 返回值说明：摄像头位置和校准结果

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `camera` | String | 校准摄像头：wide0、wide1、wide2 |
| `state` | [Int] | 校准状态：-1: 初始化，0: 进行中，1: 完成 |


<a id="query-gvsmodellist"></a>
### `gvsModelList`

- 接口类型：`Query`
- 返回类型：`[autotrainModel]`
- 接口描述：查询自动训练模型列表。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |

#### 返回值定义

- 返回值说明：自动训练模型类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `path` | String | 模型路径 |
| `name` | String | 模型名称 |
| `size` | Int | 模型文件大小 |
| `lastModified` | DateTime | 模型最后修改时间 |
| `isCurrent` | Boolean | 当前正在使用的模型 |


<a id="query-gvsstreamers"></a>
### `gvsStreamers`

- 接口类型：`Query`
- 返回类型：`[stream]`
- 接口描述：查询指定 GVS 设备 ID 的摄像头视频流；如果 ID 为空，则返回全部摄像头视频流。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | GVS 设备 ID |

#### 返回值定义

- 返回值说明：摄像头流列表

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 摄像头设备 ID，一个摄像头设备可能包含多个摄像头 |
| `ip` | String | 视频流服务器的 IP 地址 |
| `stream_list` | [String] | 视频流列表 |


<a id="query-gvstrainingimages"></a>
### `gvsTrainingImages`

- 接口类型：`Query`
- 返回类型：`[autoImageList]`
- 接口描述：获取无人机训练图像列表。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `begin_time` | `String` | - | 筛选图像的开始时间（ISO 8601 格式） |
| `end_time` | `String` | - | 筛选图像的结束时间（ISO 8601 格式） |

#### 返回值定义

- 返回值说明：训练图像信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `uuid` | String | 训练图像的唯一标识符 |
| `drone_id` | String | 图像中捕获到的无人机 ID |
| `drone_type` | String | 无人机类型（例如 DJI、Parrot） |
| `create_time` | DateTime | 图像捕获时间戳 |
| `image` | String | 训练图像的 URL 或路径 |


<a id="query-jammercooldownstatus"></a>
### `JammerCooldownStatus`

- 接口类型：`Query`
- 返回类型：`jammerCooldownStatus`
- 接口描述：获取干扰器冷却状态。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：干扰器冷却状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `band4` | Boolean | 433M 频段冷却状态 |
| `band9` | Boolean | 900M 频段冷却状态 |
| `band12` | Boolean | 1.2G 频段冷却状态 |
| `band14` | Boolean | 1.4G 频段冷却状态 |
| `band15` | Boolean | 1.5G 频段冷却状态 |
| `band18` | Boolean | 1.8G 频段冷却状态 |
| `band24` | Boolean | 2.4G 频段冷却状态 |
| `band58` | Boolean | 5.8G 频段冷却状态 |


<a id="query-linknodelist"></a>
### `linkNodeList`

- 接口类型：`Query`
- 返回类型：`[Node]`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：组网模式下所有远端节点的信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 节点的唯一 ID |
| `name` | String | 节点名称 |
| `info` | String | 节点描述 |
| `type` | String | 节点类型 |
| `ip` | String | 节点的 IP 地址 |
| `latitude` | Float | 节点纬度 |
| `longitude` | Float | 节点经度 |


<a id="query-listsigrecords"></a>
### `ListSigRecords`

- 接口类型：`Query`
- 返回类型：`[SigRecordInfo]`
- 接口描述：查询信号录制列表。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `offset` | `Int` | 0 | - |
| `limit` | `Int` | 15 | - |

#### 返回值定义

- 返回值说明：信号记录信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 信号记录的 ID |
| `updated_time` | DateTime | 最后更新时间 |
| `size` | Int | 记录文件大小 |


<a id="query-localpatchinfo"></a>
### `localPatchInfo`

- 接口类型：`Query`
- 返回类型：`upgradeDroneConfigType`
- 接口描述：查询可用于切换的本地补丁。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `class` | `String` | - | 补丁类型，当前仅支持：引擎、UI |

#### 返回值定义

- 返回值说明：无人机配置对象类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `local_versions` | [`[versions]`](#query-localpatchinfo-field-local-versions) | 有效的本地版本 |

##### 子对象字段展开

<a id="query-localpatchinfo-field-local-versions"></a>
###### `local_versions` (`[versions]`)

- 字段说明：本地版本状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `version_id` | `String` | 版本的唯一 ID |
| `version_status` | `String` | 版本状态及有效性 |
| `version_publish_time` | `String` | 发布时间 |


<a id="query-nodes"></a>
### `nodes`

- 接口类型：`Query`
- 返回类型：`[Node]`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |

#### 返回值定义

- 返回值说明：组网模式下所有远端节点的信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 节点的唯一 ID |
| `name` | String | 节点名称 |
| `info` | String | 节点描述 |
| `type` | String | 节点类型 |
| `ip` | String | 节点的 IP 地址 |
| `latitude` | Float | 节点纬度 |
| `longitude` | Float | 节点经度 |


<a id="query-notify"></a>
### `notify`

- 接口类型：`Query`
- 返回类型：`notifications`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `key` | `Int` | - | 常规通知的起始键 |

#### 返回值定义

- 返回值说明：通知消息列表

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `regularNotify` | [`[notifyType]`](#query-notify-field-regularnotify) | 用于只显示一次的通知 |
| `reservedNotify` | [`[notifyType]`](#query-notify-field-reservednotify) | 用于始终显示的通知 |

##### 子对象字段展开

<a id="query-notify-field-regularnotify"></a>
###### `regularNotify` (`[notifyType]`)

- 字段说明：通知消息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `source` | `String` | 当前通知来源 |
| `id` | `String` | ID |
| `status` | `String` | 通知状态 |
| `info` | `String` | 信息 |
| `extra` | `String` | 附加信息 |
| `time` | `String` | 时间戳 |
| `key` | `Int` | 消息 ID |

<a id="query-notify-field-reservednotify"></a>
###### `reservedNotify` (`[notifyType]`)

- 字段说明：通知消息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `source` | `String` | 当前通知来源 |
| `id` | `String` | ID |
| `status` | `String` | 通知状态 |
| `info` | `String` | 信息 |
| `extra` | `String` | 附加信息 |
| `time` | `String` | 时间戳 |
| `key` | `Int` | 消息 ID |


<a id="query-packageversiononline"></a>
### `PackageVersionOnline`

- 接口类型：`Query`
- 返回类型：`String`
- 接口描述：获取在线最新安装包版本。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="query-profilealiaslist"></a>
### `profileAliasList`

- 接口类型：`Query`
- 返回类型：`[ProfileAlias]`
- 接口描述：查询无人机类型别名列表。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：属性配置别名

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `drone_type` | String | 无人机类型 |
| `alias` | String | 别名 |
| `description` | String | 无人机描述 |
| `visible` | Boolean | true 表示显示无人机，false 表示隐藏无人机 |


<a id="query-profilelist"></a>
### `profileList`

- 接口类型：`Query`
- 返回类型：`[Profile]`
- 接口描述：查询无人机属性列表。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：属性配置

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `drone_id` | String | 无人机的 ID |
| `drone_link_id` | String | 用于与其他无人机合并的 ID |
| `drone_type` | String | 无人机自定义类型 |
| `description` | String | 无人机描述 |
| `visible` | Boolean | true 表示显示无人机，false 表示隐藏无人机 |
| `extra_data` | String | 无人机的附加数据 |


<a id="query-profilepatternlist"></a>
### `profilePatternList`

- 接口类型：`Query`
- 返回类型：`[ProfilePattern]`
- 接口描述：查询用于匹配无人机 ID 的模式列表。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：属性配置匹配规则

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `pattern` | String | 正则模式 |
| `drone_type` | String | 无人机自定义类型 |
| `description` | String | 无人机描述 |
| `visible` | Boolean | true 表示显示无人机，false 表示隐藏无人机 |


<a id="query-radartarget"></a>
### `radarTarget`

- 接口类型：`Query`
- 返回类型：`[RadarTarget]`
- 接口描述：根据 ID 查询当前检测到的雷达目标；如果未提供 ID，则返回全部当前检测到的雷达目标。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 雷达发现目标的 ID |
| `type` | `Int` | - | 雷达目标类型 |

#### 返回值定义

- 返回值说明：雷达轨迹

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 目标 ID |
| `device_type` | String | 设备类型 |
| `direction` | Float | 航向, 0-360 |
| `distance` | Float | 距离, 单位：米 |
| `latitude` | Float | 纬度，-90 至 90，210 表示无效值 |
| `longitude` | Float | 经度，-180 至 180，210 表示无效值 |
| `elevation` | Float | 俯仰角 |
| `speed` | Float | 目标速度，单位：米/秒 (m/s) |
| `radial_velocity` | Float | 目标相对雷达的径向速度 (m/s)。正值表示远离雷达，负值表示接近雷达。 |
| `course` | Float | 目标运动航迹角。范围: 0 ~ 360 度 (0 = 北, 90 = 东, 180 = 南, 270 = 西). |
| `altitude` | Float | 高度，单位：米 |
| `height` | Float | 高度，单位：米 |
| `quality_level` | Int | 0: 不可用, 1 ~ 255: 从低到高 |
| `rcs` | Float | RCS，单位：平方米 |
| `target_type` | Int | 目标类型，0: 未知，1: 无人机，2: 其他 |
| `confirmed` | Boolean | 是否已确认为无人机 |
| `tracing` | [`Tracing`](#query-radartarget-field-tracing) | 雷达目标轨迹 |
| `is_tracked` | Boolean | 是否由雷达跟踪 |
| `camera_trackings` | [`[CameraTracking]`](#query-radartarget-field-camera-trackings) | 摄像头跟踪列表 |

##### 子对象字段展开

<a id="query-radartarget-field-tracing"></a>
###### `tracing` (`Tracing`)

- 字段说明：无人机实时轨迹

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `origin` | `GeoPoint` | 起点地理位置 |
| `points` | `[[Float]]` | 轨迹点 |
| `lastlen` | `Int` | 最后一段点的长度 |

<a id="query-radartarget-field-camera-trackings"></a>
###### `camera_trackings` (`[CameraTracking]`)

- 字段说明：跟踪状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `device_id` | `String` | 摄像头设备 ID，一个摄像头设备可能包含多个摄像头 |
| `camera_name` | `String` | 摄像头名称，例如 wide_1、wide_2、wide_3 |
| `ip` | `String` | 视频流服务器的 IP 地址 |
| `status` | `Int` | 跟踪状态，1: 搜索中，2: 跟踪中(目标锁定)，3: 目标丢失，4: 失败 |
| `direction` | `Int` | 无人机航向角。365 表示无效值 |


<a id="query-report"></a>
### `report`

- 接口类型：`Query`
- 返回类型：`reportType`
- 接口描述：查询无人机事件统计报告信息。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `from` | `DateTime` | - | - |
| `to` | `DateTime` | - | - |

#### 返回值定义

- 返回值说明：报告对象类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `total_incidents` | Int | 事件总次数 |
| `total_drones` | Int | 无人机总架数 |
| `avg_per_day` | Int | 平均每日事件次数 |
| `avgdrn_per_day` | Int | 平均每日无人机架数 |
| `most_per_day` | Int | 单日事件最大次数 |
| `mostdrn_per_day` | Int | 单日无人机最大架数 |
| `most_per_hour` | Int | 每小时事件最大次数 |
| `mostdrn_per_hour` | Int | 每小时无人机最大架数 |
| `total_mitigation` | Int | 事件总拦截次数 |
| `totaldrn_mitigation` | Int | 无人机总拦截架次 |
| `total_in_alarm_region` | Int | 预警区事件总次数 |
| `totaldrn_in_alarm_region` | Int | 预警区无人机总架数 |
| `most_in_alarm_region_per_day` | Int | 预警区单日事件最大次数 |
| `mostdrn_in_alarm_region_per_day` | Int | 预警区单日无人机最大架数 |
| `total_duration` | Int | 被入侵总时长 |
| `longest_duration` | Int | 单次最长时间 |
| `avg_duration` | Int | 每次平均时长 |
| `top_drone_type` | [datatype] | 常见无人机机型 |
| `top_drones` | [datatype] | 常见无人机 |
| `daily_data` | [datatype] | 按天分组的事件次数 |
| `hourly_data` | [datatype] | 按小时分组的事件次数 |
| `moments` | [`[momentType]`](#query-report-field-moments) | 关键时刻 |

##### 子对象字段展开

<a id="query-report-field-moments"></a>
###### `moments` (`[momentType]`)

- 字段说明：关键时刻

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `seen_time` | `DateTime` | 发现时间戳 |
| `lost_time` | `DateTime` | 丢失时间戳 |
| `events` | `[Event]` | 时间范围内的事件 |


<a id="query-screenshot"></a>
### `screenshot`

- 接口类型：`Query`
- 返回类型：`ScreenshotData`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `seq` | `Int` | - | 截图事件序号 |
| `limit` | `Int` | - | 要返回的最大记录条数 |
| `offset` | `Int` | - | 要返回的首条记录偏移量 |
| `order` | `String` | - | 查询排序，取值：desc 表示降序，asc 表示升序 |

#### 返回值定义

- 返回值说明：无人机截图数据

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `count` | Int | 记录条数 |
| `data` | [`[Screenshot]`](#query-screenshot-field-data) | 截图数据列表 |

##### 子对象字段展开

<a id="query-screenshot-field-data"></a>
###### `data` (`[Screenshot]`)

- 字段说明：无人机截图

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | `Int` | 截图 ID |
| `drone_id` | `String` | 无人机 ID |
| `drone_type` | `String` | 无人机类型 |
| `event_sequence` | `Int` | 事件序号 |
| `create_time` | `DateTime` | 创建时间 |
| `file_path` | `String` | 文件路径 |
| `data` | `String` | 截图数据 |


<a id="query-sensor"></a>
### `sensor`

- 接口类型：`Query`
- 返回类型：`[Sensor]`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |

#### 返回值定义

- 返回值说明：传感器实体

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 传感器的唯一 ID |
| `mac` | String | 传感器 MAC 地址 |
| `name` | String | 传感器名称 |
| `ttl` | Int | TTL |
| `config` | jsonStrType | 当前传感器配置 |
| `sensor_status` | [`State`](#query-sensor-field-sensor-status) | 当前传感器状态 |
| `state` | String | 当前传感器状态, up 或者 down |
| `faults` | String | 当前传感器的故障信息 |
| `node` | String | 传感器所属节点 |

##### 子对象字段展开

<a id="query-sensor-field-sensor-status"></a>
###### `sensor_status` (`State`)

- 字段说明：SCV/控制器/传感器的状态。

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ip_address` | `String` | SCV/控制器/传感器的唯一 IP 地址 |
| `first_seen` | `String` | 当前 SCV/控制器/传感器的登录时间 |
| `last_seen` | `String` | 当前 SCV/控制器/传感器的登出时间 |
| `version` | `String` | SCV/控制器/传感器的唯一版本号 |
| `built_time` | `String` | SCV/控制器/传感器的唯一构建时间 |
| `git_hash` | `String` | SCV/控制器/传感器的唯一 Git 哈希值 |
| `temperature` | `Int` | SCV/控制器/传感器的温度 |
| `component_type` | `String` | SCV/控制器/传感器的组件类型 |


<a id="query-skysegmenter"></a>
### `skySegmenter`

- 接口类型：`Query`
- 返回类型：`[SkySegmenterResult]`
- 接口描述：查询摄像头设备天空分割算法结果。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | GVS 设备 ID |

#### 返回值定义

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `filepath` | String | - |
| `polyline` | [`[Point]`](#query-skysegmenter-field-polyline) | - |

##### 子对象字段展开

<a id="query-skysegmenter-field-polyline"></a>
###### `polyline` (`[Point]`)

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `x` | `Int` | - |
| `y` | `Int` | - |

<a id="query-spdreport"></a>

### `spdReport`

- 接口类型：`Query`
- 返回类型：`[spdReport]`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `freq_start` | `Int` | - | 频谱跨度起始频率，单位 kHz |
| `freq_stop` | `Int` | - | 频谱扫描结束频率，单位 kHz |

#### 返回值定义

- 返回值说明：SPD 报告信息

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `frequence` | Int | 信号频率 |
| `bandwidth` | Int | 信号带宽 |
| `description` | String | 信号描述 |


<a id="query-spoofstatus"></a>
### `spoofStatus`

- 接口类型：`Query`
- 返回类型：`spoofStatus`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：诱骗器状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `switch` | Int | 开关状态，0: 关闭，1: 开启，2: 降落，3: 驱离。 |


<a id="query-startdownload"></a>
### `startDownload`

- 接口类型：`Query`
- 返回类型：`Boolean`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `version` | `String` | - | 要下载的版本 |

#### 返回值定义

标量类型，无字段定义。


<a id="query-storage"></a>
### `storage`

- 接口类型：`Query`
- 返回类型：`storage`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：设备存储

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `internalSize` | Float | 设备内部可用空间（单位 Mbytes） |
| `externalSize` | Float | 设备外部可用空间（单位 Mbytes） |


<a id="query-syscapability"></a>
### `sysCapability`

- 接口类型：`Query`
- 返回类型：`[String]`
- 接口描述：查询设备干扰能力（例如 Wideband、Smart-II）。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="query-time"></a>
### `time`

- 接口类型：`Query`
- 返回类型：`time`
- 接口描述：查询设备当前系统时间。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：时间数据

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sysTime` | String | 系统时间 |


<a id="query-timezone"></a>
### `timeZone`

- 接口类型：`Query`
- 返回类型：`timeZone`
- 接口描述：查询设备当前系统时区以及全部时区列表。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：时区数据

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `sysTimeZone` | String | 系统时区字符串 |
| `allTimeZone` | [String] | 所有时区字符串数组 |


<a id="query-unknownsignal"></a>
### `unknownSignal`

- 接口类型：`Query`
- 返回类型：`[unknownSignal]`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：未知信号列表

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `freq` | String | 信号频率 |
| `bw` | String | 信号带宽 |
| `time` | String | 信号时间 |
| `mod` | String | 信号的调制方式 |
| `seen_sensors` | String | 检测到该信号的传感器 |


<a id="query-unlinknodelist"></a>
### `unlinkNodeList`

- 接口类型：`Query`
- 返回类型：`[site]`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：可用站点

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 站点 ID |
| `conn_type` | String | 连接类型 |
| `name` | String | 站点名称 |
| `info` | String | 站点信息 |


<a id="query-upgrade"></a>
### `upgrade`

- 接口类型：`Query`
- 返回类型：`upgradeType`
- 接口描述：查询可用于升级的本地版本。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：升级对象类型

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `prepare_status` | String | 升级目录准备状态 |
| `upgrade_status` | String | 升级状态 |
| `local_versions` | [`[versions]`](#query-upgrade-field-local-versions) | 有效的本地版本 |
| `free_space` | Int | 新升级可用空间（单位 Mbytes） |
| `has_enough_space` | Boolean | 是否有足够空间用于新升级 |

##### 子对象字段展开

<a id="query-upgrade-field-local-versions"></a>
###### `local_versions` (`[versions]`)

- 字段说明：本地版本状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `version_id` | `String` | 版本的唯一 ID |
| `version_status` | `String` | 版本状态及有效性 |
| `version_publish_time` | `String` | 发布时间 |


<a id="query-upgradestatusonline"></a>
### `UpgradeStatusOnline`

- 接口类型：`Query`
- 返回类型：`String`
- 接口描述：获取在线升级状态：<br>"UpgradeStatusIdle"：升级任务未启动或已完成。<br>"UpgradeStatusDownloading"：正在下载升级文件。<br>"UpgradeStatusDownloadErr"：下载升级文件时发生错误。<br>"UpgradeStatusUnpacking"：正在解压升级文件。<br>"UpgradeStatusUnpackErr"：解压升级文件时发生错误。<br>"UpgradeStatusDoUpgrading"：正在执行升级过程。<br>"UpgradeStatusDoUpgradeErr"：升级过程中发生错误。<br>"UpgradeStatusRestarting"：升级完成后系统正在重启。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="query-version"></a>
### `version`

- 接口类型：`Query`
- 返回类型：`String`
- 接口描述：查询设备当前版本信息。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="query-vsgevent"></a>
### `vsgevent`

- 接口类型：`Query`
- 返回类型：`[VSGEvent]`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `uuid` | `String` | - | - |

#### 返回值定义

- 返回值说明：VSG 无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 无人机的 UUID |
| `drone_type` | String | 无人机预测类型 |
| `distance_between_obj_and_cam` | Int | 预估距离 |
| `icon` | String | WebUI 图标文件路径 |
| `image` | String | 原始检测图像文件名 |
| `video` | String | 跟踪视频文件名 |
| `firstseen_time` | DateTime | 首次发现时间 |
| `lastseen_time` | DateTime | 最后出现时间 |
| `firstseen_ptz` | String | 首次发现时的 PTZ |
| `lastseen_ptz` | String | 最后发现时的 PTZ |
| `firstseen_size` | String | 首次发现大小 |
| `lastseen_size` | String | 最后发现时的尺寸 |
| `seen_sensors` | String | 由哪个传感器发现 |


<a id="query-vsgevents"></a>
### `vsgevents`

- 接口类型：`Query`
- 返回类型：`[VSGEvent]`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `from` | `Int` | - | - |
| `to` | `Int` | - | - |

#### 返回值定义

- 返回值说明：VSG 无人机历史事件

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 无人机的 UUID |
| `drone_type` | String | 无人机预测类型 |
| `distance_between_obj_and_cam` | Int | 预估距离 |
| `icon` | String | WebUI 图标文件路径 |
| `image` | String | 原始检测图像文件名 |
| `video` | String | 跟踪视频文件名 |
| `firstseen_time` | DateTime | 首次发现时间 |
| `lastseen_time` | DateTime | 最后出现时间 |
| `firstseen_ptz` | String | 首次发现时的 PTZ |
| `lastseen_ptz` | String | 最后发现时的 PTZ |
| `firstseen_size` | String | 首次发现大小 |
| `lastseen_size` | String | 最后发现时的尺寸 |
| `seen_sensors` | String | 由哪个传感器发现 |


<a id="query-vsgeventsimage"></a>
### `vsgeventsimage`

- 接口类型：`Query`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `uuid` | `String` | - | - |
| `history` | `Boolean` | - | - |

#### 返回值定义

标量类型，无字段定义。


<a id="query-whitelist"></a>
### `whitelist`

- 接口类型：`Query`
- 返回类型：`[Whitelist]`
- 接口描述：查询无人机白名单列表信息。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：白名单

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | String | 无人机的唯一 ID |
| `dronetype` | String | 无人机类型 |
| `alias` | String | 来自白名单的无人机自定义别名 |
| `description` | String | 无人机详细描述 |
| `created_time` | String | 无人机创建时间 |


<a id="query-widebandjammer"></a>
### `widebandJammer`

- 接口类型：`Query`
- 返回类型：`WidebandJammer`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `directional` | `Boolean` | - | 定向干扰器 |

#### 返回值定义

- 返回值说明：宽带干扰器实体（已弃用）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `band4` | Int | 433M 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band9` | Int | 900M 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band12` | Int | 1.2G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band14` | Int | 1.4G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band15` | Int | 1.5G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band18` | Int | 1.8G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band24` | Int | 2.4G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band58` | Int | 5.8G 频段状态，0:不可用，1:空闲，其他:忙碌。 |


<a id="query-widebandjammer2"></a>
### `widebandJammer2`

- 接口类型：`Query`
- 返回类型：`WidebandJammer2`
- 接口描述：查询宽带干扰器状态（0: 不可用，1: 空闲，2: 忙碌）。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `directional` | `Boolean` | - | 定向干扰器 |

#### 返回值定义

- 返回值说明：宽带干扰器实体

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `band4` | Int | 433M 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |
| `band9` | Int | 900M 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |
| `band12` | Int | 1.2G 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |
| `band14` | Int | 1.4G 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |
| `band15` | Int | 1.5G 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |
| `band18` | Int | 1.8G 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |
| `band24` | Int | 2.4G 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |
| `band58` | Int | 5.8G 频段状态，0:不可用，1:空闲，其他:忙碌（值为剩余时间） |


<a id="query-wifilist"></a>
### `wifilist`

- 接口类型：`Query`
- 返回类型：`[wifilist]`
- 接口描述：查询指定类型的 WiFi 列表信息，类型可为 Active、Inactive、Background。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `type` | `String` | - | 选择活跃/非活跃/后台列表 |

#### 返回值定义

- 返回值说明：WiFi 列表

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ssid` | String | 无人机 SSID |
| `mac` | String | 无人机 MAC 地址 |
| `reliability` | String | 判定为无人机的可信度 |
| `status` | Int | 无人机状态 |


<a id="query-wifistatus"></a>
### `wifiStatus`

- 接口类型：`Query`
- 返回类型：`wifiStatusType`
- 接口描述：查询 WiFi 状态。

#### 参数定义

无参数。

#### 返回值定义

- 返回值说明：WiFi 状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ifname` | String | WiFi 设备的接口名称 |
| `enabled` | Boolean | WiFi 设备状态 |
| `status` | String | 当前 WiFi 设备的状态，取值：`up`、`down`、`notExist` |
| `connected_wifi` | String | 当前已连接的 WiFi 网络 |
| `config` | [`ipConfig`](#query-wifistatus-field-config) | IP 配置：ip/mask/gateway |
| `available_wifi` | [`[wifiList]`](#query-wifistatus-field-available-wifi) | - |

##### 子对象字段展开

<a id="query-wifistatus-field-config"></a>
###### `config` (`ipConfig`)

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `ip` | `String` | 当前已连接 WiFi 的 IP 地址 |
| `mask` | `String` | 当前已连接 WiFi 的子网掩码 |
| `gateway` | `String` | 当前已连接 WiFi 的网关 |
| `status` | `String` | 当前已连接 WiFi 的状态 |

<a id="query-wifistatus-field-available-wifi"></a>
###### `available_wifi` (`[wifiList]`)

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `bssid` | `String` | WiFi 的 BSSID |
| `ssid` | `String` | WiFi 的 SSID |
| `chan` | `Int` | WiFi 信道 |
| `freq` | `Int` | WiFi 信号频率 (MHz) |
| `signal` | `Int` | WiFi 信号强度百分比 (0~100) |
| `security` | `[String]` | WiFi 加密方式 |
| `rate` | `Int` | WiFi 连接的数据传输速率（单位 Mbps） |
| `active` | `Boolean` | 指示此 WiFi 网络当前是否处于活动状态（已连接） |
| `in_use` | `Boolean` | 指示设备当前是否已连接到此 WiFi 网络 |


## Mutation 接口

<a id="mutation-addblacklist"></a>
### `addBlacklist`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将指定无人机添加至黑名单。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `dronetype` | `String` | - | 无人机类型 |
| `alias` | `String` | - | 无人机别名 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-addwhitelist"></a>
### `addWhitelist`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将指定无人机添加至白名单。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `dronetype` | `String` | - | 无人机类型 |
| `alias` | `String` | - | 无人机别名 |
| `timerange` | `String` | - | 有效时间范围，格式为 "begin_datetime,end_datetime"，长期有效使用 "permanent,permanent"。<br>无时区格式：2006-01-02 15:04:05，<br>带时区格式：2006-01-02T15:04:05±08:00 或 2006-01-02T15:04:05Z |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-adjustbandattack"></a>
### `adjustbandAttack`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：使用可调频段干扰器执行干扰打击。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `jammer_id` | `String` | - | 干扰器 ID |
| `status` | `Boolean` | - | 状态: true: 'on' / false: 'off' |
| `band_id` | `Int` | - | 频段 ID |
| `freq` | `Int` | - | 中心频率，单位 kHz |
| `bandwidth` | `Int` | - | 带宽，单位 kHz |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-airdefencearea"></a>
### `airDefenceArea`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：添加或移除防空区域。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `data` | `String` | - | 类型：0-删除，1-添加，JSON 字符串 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-attack"></a>
### `attack`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：对指定无人机执行干扰打击。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `cancel` | `Boolean` | false | 如果设置，则取消对目标无人机的打击 |
| `takeover` | `Boolean` | false | 如果设置，则接管目标无人机 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-autoattack"></a>
### `autoAttack`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：切换自动打击开关状态。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `on` | `Boolean` | - | 自动打击开关 |
| `saEnabled` | `Boolean` | true | 启用精准打击 |
| `wbEnabled` | `Boolean` | true | 启用宽带干扰 |
| `dirWbEnabled` | `Boolean` | true | 启用定向宽带干扰 |
| `spfEnabled` | `Boolean` | false | 启用 GNSS 诱骗器 |
| `naviEnabled` | `Boolean` | - | 启用导航防御 |
| `naviBands` | `[naviBands]` | - | 启用导航防御，枚举类型列表，可选值：band12(1.2GHz)、band15(1.5GHz) |
| `protectWhite` | `Boolean` | false | 是否保护白名单无人机；如果设置此项，影响白名单无人机的频段将不会启用 |
| `allJammingOn` | `Boolean` | - | 启用所有频段 |
| `timeRanges` | `[[String]]` | []any{} | 每日时间范围列表（支持跨天），格式：[[开始时间，结束时间], ...]，时间格式为 HH:mm:ss。 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-camcontrol"></a>
### `camControl`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：控制摄像头移动。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `type` | `String` | - | 摄像头类型，取值范围：wide、narrow |
| `opType` | `String` | - | 摄像头操作类型，取值范围：停止（stop）、移动（move）、对焦（focus）、变焦（zoom） |
| `operation` | `String` | - | 摄像头操作：1. 操作类型为移动，取值范围：上、下、左、右、左上、右上、左下、右下；2. 操作类型为对焦，取值范围：近、远；3. 操作类型为变焦，取值范围：放大、缩小 |
| `speed` | `Int` | - | 摄像头速度，范围 1~7 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-camlocatecontrol"></a>
### `camLocateControl`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：选择摄像头区域。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `type` | `String` | - | 摄像头类型，取值范围：wide、narrow |
| `xTop` | `Float` | - | 摄像头画面中选区左上角的 x 坐标 |
| `yTop` | `Float` | - | 摄像头画面中选区左上角的 y 坐标 |
| `xBottom` | `Float` | - | 摄像头画面中选区右下角的 x 坐标 |
| `yBottom` | `Float` | - | 摄像头画面中选区右下角的 y 坐标 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-camsetptz"></a>
### `camSetPTZ`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置摄像头 PTZ。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `type` | `String` | - | 摄像头类型，取值范围：wide、narrow |
| `pan` | `Int` | - | 摄像头水平角 |
| `tilt` | `Int` | - | 摄像头俯仰角 |
| `zoom` | `Int` | - | 摄像头变焦 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-clearlogs"></a>
### `clearLogs`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：重置所有日志并重新开始记录。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-clearstorage"></a>
### `clearStorage`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：清空设备内部存储。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-control"></a>
### `control`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：接管功能专用的无人机控制器（执行接管操作）。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `command` | `String` | - | 命令 |
| `chanValues` | `[Int]` | - | 数组长度为 5，各通道说明如下：<br>0: Chan1：右摇杆左右，对应左右移动。范围：-1000 到 1000，0 表示摇杆居中。<br>1: Chan2：右摇杆上下，对应前后移动。范围：-1000 到 1000，0 表示摇杆居中。<br>2: Chan3：左摇杆上下，对应油门。范围：-1000 到 1000，0 表示摇杆居中。<br>3: Chan4：左摇杆左右，对应偏航（四旋翼的旋转）。范围：-1000 到 1000， 0 表示摇杆居中。<br>4: Chan5：两档拨动开关：-1000 表示锁定，1000 表示解锁。仅有两个档位。 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-ctrl-landing"></a>
### `ctrl_landing`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：对指定无人机执行受控降落（为 true 时启动，为 false 时停止）。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `enable` | `Boolean` | true | 如果为 true，则开始对目标无人机执行受控降落；否则停止降落。 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-deleteblacklist"></a>
### `deleteBlacklist`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将无人机从黑名单移除。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-deleteevents"></a>
### `deleteEvents`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：删除无人机事件（软删除）。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `sequence` | `[Int]` | - | 要删除的事件序号列表 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-deleteeventsbyid"></a>
### `deleteEventsByID`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：根据无人机 ID 和类型删除无人机事件。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `all` | `Boolean` | - | 是否删除所有事件 |
| `drone_id` | `String` | - | 待查询的无人机 ID |
| `drone_type` | `String` | - | 待查询的无人机类型 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-deleteeventvideo"></a>
### `deleteEventVideo`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：根据无人机 ID 和类型删除无人机事件。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `sequence` | `Int` | - | 事件序号 |
| `videos` | `[String]` | - | 要删除的事件关联视频文件列表，空值表示删除所有视频 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-deletewhitelist"></a>
### `deleteWhitelist`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将无人机从白名单移除。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-detectingbands"></a>
### `detectingBands`

- 接口类型：`Mutation`
- 返回类型：`DetectingBands`
- 接口描述：启用或禁用某个侦测频段。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `band` | `String` | - | 以字符串指定一个频段，取值可为 band4/band9/band14/band24/band58/bandext/bandext8。 |
| `enable` | `Boolean` | true | 启用(true) 或 禁用(false) 侦测频段 |

#### 返回值定义

- 返回值说明：侦测频段状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `band24` | Int | 2.4Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band58` | Int | 5.8Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band18` | Int | 1.8Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band14` | Int | 1.4Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band12` | Int | 1.2Ghz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band9` | Int | 900MHz 频段状态，0:不可用，1:禁用，2:启用。 |
| `band4` | Int | 433MHz 频段状态，0:不可用，1:禁用，2:启用。 |
| `bandext` | Int | 扩展频段状态，0:不可用，1:禁用，2:启用。 |
| `bandext8` | Int | 6-8GHz 频段状态，0:不可用，1:禁用，2:启用。 |
| `Boost24` | Int | 已弃用。测试功能，0:不可用，1:禁用，2:启用。 |


<a id="mutation-device"></a>
### `device`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设备设置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 设备的 ID |
| `class` | `String` | - | 设备类别 |
| `config` | `jsonStrType` | - | 设备的 JSON 配置对象 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-devicetest"></a>
### `deviceTest`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：在所有设备上启动或停止自检。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | `Boolean` | - | 开始（enable=true）或停止（enable=false）测试 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-dfgun"></a>
### `dfgun`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：查打枪（DFGun）的杂项配置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `lan_type` | `Int` | - | - |
| `mode` | `Int` | - | - |
| `droneid` | `String` | - | - |
| `attack_freq_low` | `Int` | - | kHz，大于 300_000 |
| `attack_freq_high` | `Int` | - | kHz，小于 2000_000 |
| `cps_calib` | `Boolean` | - | 罗盘校准 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-dhcpenable"></a>
### `dhcpEnable`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置 DHCP 开关状态（若关闭，其他字段均忽略）。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `on` | `Boolean` | - | - |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-directionalwbattack"></a>
### `directionalWBAttack`

- 接口类型：`Mutation`
- 返回类型：`WidebandJammer`
- 接口描述：切换定向宽带干扰器的启用 / 禁用状态。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `status` | `Boolean` | false | 定向宽带干扰器状态，true 表示开启，false 表示关闭 |
| `band` | `String` | - | 以字符串指定一个频段，取值可为 band4/band9/band12/band14/band15/band18/band24/band58 |
| `gain` | `Int` | constants.DEFUALT_GAIN | 定向宽带干扰器的增益 |
| `droneId` | `String` | - | 无人机的 ID |

#### 返回值定义

- 返回值说明：宽带干扰器实体（已弃用）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `band4` | Int | 433M 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band9` | Int | 900M 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band12` | Int | 1.2G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band14` | Int | 1.4G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band15` | Int | 1.5G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band18` | Int | 1.8G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band24` | Int | 2.4G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band58` | Int | 5.8G 频段状态，0:不可用，1:空闲，其他:忙碌。 |


<a id="mutation-drone"></a>
### `drone`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置无人机属性。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |
| `credential` | `String` | - | - |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-drone-profile"></a>
### `drone_profile`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：添加或移除无人机属性配置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `drone_link_id` | `String` | - | 用于与其他无人机合并的 ID |
| `drone_type` | `String` | - | 无人机自定义类型 |
| `drone_description` | `String` | - | 无人机描述 |
| `visible` | `Boolean` | true | true 表示显示无人机，false 表示隐藏无人机，默认值为 true |
| `extra_data` | `String` | - | 包含额外配置数据的 JSON 字符串 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-droneadsb"></a>
### `droneAdsB`

- 接口类型：`Mutation`
- 返回类型：`Boolean`
- 接口描述：启用或禁用 ADS-B（航空器飞行信息）功能。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `switch` | `Boolean` | - | true：开启，false：关闭 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-droneprofilealias"></a>
### `droneProfileAlias`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：为指定无人机类型添加或移除别名。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `action` | `String` | - | 操作，可为添加或删除 |
| `id` | `String` | - | 无人机的 ID |
| `drone_type` | `String` | - | 无人机类型 |
| `alias` | `String` | - | 给定无人机类型的别名 |
| `description` | `String` | - | 无人机类型与匹配模式描述 |
| `visible` | `Boolean` | true | true 表示显示无人机，false 表示隐藏无人机，默认值为 true |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-droneprofilepattern"></a>
### `droneProfilePattern`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：添加或移除无人机正则匹配模式。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `action` | `String` | - | 操作，可为添加或删除 |
| `pattern` | `String` | - | 无人机模式 |
| `new_pattern` | `String` | - | 当 action 为 'add' 且该参数不为 null 时，旧模式将被该新模式替换 |
| `drone_type` | `String` | - | 无人机自定义类型 |
| `description` | `String` | - | 无人机类型与匹配模式描述 |
| `visible` | `Boolean` | true | true 表示显示无人机，false 表示隐藏无人机，默认值为 true |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-dronesub"></a>
### `droneSub`

- 接口类型：`Mutation`
- 返回类型：`Boolean`
- 接口描述：订阅无人机属性更新。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `attribute` | `String` | - | 无人机属性，支持列表："截图" |
| `enable` | `Boolean` | false | 启用或禁用订阅 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-falsealarminvalid"></a>
### `falseAlarmInvalid`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将摄像头事件标记为无效。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 摄像头的 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gfsk"></a>
### `gfsk`

- 接口类型：`Mutation`
- 返回类型：`Boolean`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `cmd` | `String` | - | 添加、删除、修改 |
| `data` | `jsonStrType` | - | GFSK 数据 |
| `option` | `jsonStrType` | {} | GFSK 数据 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsautocalibration"></a>
### `gvsAutoCalibration`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 自动校准。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `action` | `String` | - | 校准动作：开始、停止、应用 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsautocalibrationadjust"></a>
### `gvsAutoCalibrationAdjust`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 自动校准。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `sequence` | `Int` | - | 自动校准后摄像头序号，范围为 1 到 9 |
| `wbox` | `jsonStrType` | - | 广视角摄像头边界框 |
| `nbox` | `jsonStrType` | - | 窄视角摄像头边界框 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsautotrain"></a>
### `gvsAutoTrain`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 自动训练。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `action` | `String` | - | 动作：开始、停止、应用 |
| `file` | `String` | - | 模型文件 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsbglearning"></a>
### `gvsBgLearning`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：切换背景学习模式。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `bgMode` | `Boolean` | - | - |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvscalibrationcheck"></a>
### `gvsCalibrationCheck`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：执行 GVS 校准检查。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `action` | `String` | - | 校准检查动作：开始、停止 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvscalibrationcheckcheck"></a>
### `gvsCalibrationCheckCheck`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 校准检查。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `xTop` | `Float` | - | 摄像头画面中选区左上角的 x 坐标 |
| `yTop` | `Float` | - | 摄像头画面中选区左上角的 y 坐标 |
| `xBottom` | `Float` | - | 摄像头画面中选区右下角的 x 坐标 |
| `yBottom` | `Float` | - | 摄像头画面中选区右下角的 y 坐标 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvscalibrationcheckselect"></a>
### `gvsCalibrationCheckSelect`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 校准检查时选择图像。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `image` | `String` | - | 选择摄像头图像 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsfocuscalibration"></a>
### `gvsFocusCalibration`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：对 GVS 设备执行焦距校准。<br>该操作用于控制指定摄像头（带索引的广角（wide）或窄角（narrow）摄像头）的焦距校准流程。<br>在样本采集期间，系统会以摄像头 SN 和温度作为键记录焦距数据；如果未提供温度，则使用配置中的设备当前温度。<br>预置位动作要求存在且仅存在一个距离超过 500 米的地标，生成的预置位会被保存为校准参考。<br>Orient 动作会将 PTZ 转向该校准后的预置位方向。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | GVS 设备 ID |
| `action` | `String` | - | 校准动作：开始 \| 停止 \| 开始采集 \| 停止采集 \| 查询 \| 预置位 \| 定向 |
| `camType` | `String` | - | 摄像头类型：wide \| narrow |
| `camId` | `Int` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `temperature` | `Int` | -1000 | 当前温度 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsheadingcalibration"></a>
### `gvsHeadingCalibration`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 航向校准。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `action` | `String` | - | 校准动作：开始、停止、定向、应用 |
| `bearing` | `Float` | 0 | 方位参数定义从正北顺时针到校准目标的偏移量，有效范围为 (0°, 360°]，仅用于 apply 操作。 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsmanualcalibration"></a>
### `gvsManualCalibration`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 手动校准。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `action` | `String` | - | 校准动作：开始、停止、应用 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsmanualcalibrationadvanced"></a>
### `gvsManualCalibrationAdvanced`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：GVS 手动校准。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `camId` | `String` | - | 摄像头 ID，广角摄像头范围：0、1、2，窄角摄像头范围：0 |
| `action` | `String` | - | 校准动作：校准、重新校准、跳转 |
| `sequence` | `Int` | - | 摄像头位置 0、1、2，从左到右 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-gvsworkmode"></a>
### `gvsWorkMode`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `mode` | `String` | - | 工作模式，取值范围：校准（CALI）、扫描（SCAN）、手动（MANUAL）、自动训练（AUTOTRAIN） |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-markfalsealarm"></a>
### `markFalseAlarm`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将无人机事件标记为误报。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `sequence` | `[Int]` | - | 要标记的事件序号列表 |
| `type` | `String` | other | 误报类型 [背景,鸟类,飞机,直升机,其他] |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-markfalsealarmbyid"></a>
### `markFalseAlarmByID`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将无人机事件标记为误报。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `all` | `Boolean` | - | 是否删除所有事件 |
| `drone_id` | `String` | - | 待查询的无人机 ID |
| `drone_type` | `String` | - | 待查询的无人机类型 |

#### 返回值定义

标量类型，无字段定义。

<a id="mutation-node"></a>
### `node`

- 接口类型：`Mutation`
- 返回类型：`Boolean`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `cmd` | `String` | - | 添加、删除、修改、采用、丢弃、重置、日志清理、日志上传 |
| `id` | `String` | - | 节点 ID |
| `name` | `String` | - | 节点名称 |
| `info` | `String` | - | 关于命令的附加信息 |

#### 返回值定义

标量类型，无字段定义。

<a id="mutation-powermode"></a>

### `powerMode`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置电源模式，仅适用于便携设备。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `mode` | `String` | - | "performance": CRPC+DroneID+RemoteID，默认；<br>"balanced": DroneID+RemoteID；<br>"powersaving": RemoteID |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-pulldronevideo"></a>
### `pullDroneVideo`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：播放无人机模拟图传（FPV）视频。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `status` | `Boolean` | false | 如果设置，则播放模拟图传视频 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-remove-fake-drone"></a>
### `remove_fake_drone`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：移除伪目标无人机。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `uuid` | `String` | - | 检测到的目标 ID |
| `type` | `String` | other | 误报类型 [背景,鸟类,飞机,直升机,其他] |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-reset"></a>
### `reset`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：重置设备。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 设备的 ID |
| `class` | `String` | - | 设备类别 |
| `reason` | `String` | - | 重置原因（字符串形式） |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-rollbackpatch"></a>
### `rollbackPatch`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：切换或升级 UI 版本。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `class` | `String` | - | 补丁类型，当前仅支持：控制器、引擎、UI |
| `version` | `Int` | - | 0: 默认版本，1: 上一版本。 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-savelogs"></a>
### `saveLogs`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `deviceId` | `String` | - | 节点 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-sendskysegmenterresults"></a>
### `sendSkySegmenterResults`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：发送分割结果。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | GVS 设备 ID |
| `msg` | `String` | - | 内容 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-set-gvs-conf"></a>
### `set_gvs_conf`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | - |
| `cont` | `String` | - | - |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-set-pan-tilt"></a>
### `set_pan_tilt`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：摄像头云台参数设置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 设备的 ID |
| `pstart` | `Int` | - | 云台姿态起始值 |
| `prange` | `Int` | - | 云台姿态范围 |
| `tstart` | `Int` | - | 采集起始时间戳 |
| `trange` | `Int` | - | 时间范围 |
| `lat` | `Float` | - | 纬度 |
| `lng` | `Float` | - | 经度 |
| `t2` | `Float` | - | 第二时间参数 |
| `x2` | `Float` | - | 辅助水平参数 |
| `heading` | `Float` | - | 航向 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-set-sensor-mode"></a>
### `set_sensor_mode`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：传感器模式设置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `mode` | `String` | - | 模式 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-set-vsg-license"></a>
### `set_vsg_license`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置传感器许可证。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 设备的 ID |
| `license` | `String` | - | 设备的许可证 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-setcontrollerlicense"></a>
### `setControllerLicense`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置控制器许可证。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `license` | `String` | - | 控制器的许可证 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-setgeolocation"></a>
### `setGeoLocation`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置设备位置，不做持久化。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `lat` | `Float` | - | 纬度 |
| `lng` | `Float` | - | 经度 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-settime"></a>
### `setTime`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置系统时间。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `time` | `String` | - | 设置时间值 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-signalcap"></a>
### `signalCap`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：信号采集功能。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `msg` | `String` | - | 信号采集消息 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-signalrec"></a>
### `signalRec`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：信号录制功能。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 引擎的 ID |
| `cmd` | `String` | - | 信号录制命令 |
| `droneTypes` | `[String]` | - | 信号录制的无人机类型 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-sigparse"></a>
### `sigParse`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：启动信号解析任务。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `sensorId` | `String` | - | 传感器的 ID |
| `bands` | `[String]` | - | 信号分析频段列表，指定要分析的频段 |
| `extFreq` | `Int` | 0 | 信号分析的额外频率(MHz)，0 表示空 |
| `antenna` | `Int` | -1 | 信号来源天线: [0 ~ 7], 默认(-1) 表示所有 |
| `short` | `Boolean` | false | 时长设置。false（normal）：21ms，true（short）：10ms |
| `brief` | `Boolean` | false | 简洁模式。true：开启，false：关闭 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-spd"></a>
### `spd`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：频谱显示设置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `action` | `String` | - | "添加" 或 "更新" 或 "删除" |
| `sensor_id` | `String` | - | SPD 传感器的 ID |
| `req_id` | `Int` | - | 该 SPD 会话的请求 ID |
| `freq_start` | `Int` | - | 频谱跨度起始频率，单位 kHz |
| `freq_stop` | `Int` | - | 频谱扫描结束频率，单位 kHz |
| `span_points` | `Int` | - | 频谱扫描点数 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-spoofer-switch"></a>
### `spoofer_switch`

- 接口类型：`Mutation`
- 返回类型：`spoofStatus`
- 接口描述：诱骗器设置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 诱骗器 ID，Null 表示自动选择 |
| `action` | `Int` | - | 诱骗器开关，0：关闭，1：开启，2：降落，3：驱离 |
| `timeout` | `Int` | 0 | 诱骗器开启超时时间（秒），0 表示无限制 |
| `direction` | `Int` | -1 | 诱骗驱离方向，-1 表示自动选择 |

#### 返回值定义

- 返回值说明：诱骗器状态

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `switch` | Int | 开关状态，0: 关闭，1: 开启，2: 降落，3: 驱离。 |


<a id="mutation-stagereset"></a>
### `stageReset`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：重置定向干扰器转台位置。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 定向干扰器 ID，默认值为 null；如果 ID 为空，则复位所有定向干扰器云台 |
| `direction` | `Float` | float64(0) | 期望方位角，默认值 0，取值范围：0≤值≤360 |
| `elevation` | `Float` | float64(0) | 期望俯仰角，默认值 0，取值范围：-60≤值≤90 |
| `track_enable` | `Boolean` | true | 为 true 时，转台复位后继续跟踪无人机；为 false 时，转台复位后停止跟踪无人机 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-starttracking"></a>
### `startTracking`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：按无人机 ID 开始跟踪。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 用于跟踪的无人机 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-starttrackingtarget"></a>
### `startTrackingTarget`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：按目标 ID 开始跟踪。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 检测到的目标 ID |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-stoptrackingbycamid"></a>
### `stopTrackingByCamId`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：停止指定摄像头 ID 对应的 GVS 无人机跟踪。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 摄像头设备的 ID |
| `camName` | `String` | all | 摄像头名称，例如 narrow、wide_0、wide_1、wide_2 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-stoptrackingbydroneid"></a>
### `stopTrackingByDroneId`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：停止指定无人机 ID 的跟踪任务。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 如果未设置，则取消跟踪目标无人机 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-takeover"></a>
### `takeover`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：接管指定无人机控制权。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `action` | `String` | - | 开始、停止 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-tdoa-track"></a>
### `tdoa_track`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：启用或禁用对无人机的 TDOA 跟踪。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `enable` | `Boolean` | true | 如果设置，则启动对目标无人机的 TDOA 跟踪 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-time"></a>
### `time`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置时间；当存在 auto 参数时，setTime 参数无效。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `setTime` | `Int` | - | - |
| `auto` | `Boolean` | - | true 表示通过 GPS 自动同步时间，false 表示由用户手动配置 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-timezone"></a>
### `timeZone`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：设置时区。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `setTimeZone` | `String` | - | 时区，当 auto 为 false 时必填 |
| `auto` | `Boolean` | false | true 表示按 GPS 位置自动配置，false 表示由用户手动配置 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-toa-measure"></a>
### `toa_measure`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：启用或禁用对无人机的 TOA 测量。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | - | 无人机的 ID |
| `reqid` | `Int` | - | 测量报告使用的 Request ID |
| `timeslots` | `[Int]` | - | 本次 TOA 测量的时隙 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-unknownwifi"></a>
### `unknownWifi`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：为未知 WiFi 无人机添加标签。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `mac` | `String` | - | 无人机的 MAC 地址 |
| `tag` | `String` | - | 设置当前无人机标签：'热点'、'无人机'、'未知' |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-upgradedefaultdronemodellibrary"></a>
### `upgradeDefaultDroneModelLibrary`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：将无人机模型库回滚到默认版本。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-upgradedronemodellibrary"></a>
### `upgradeDroneModelLibrary`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：升级无人机库。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-upgradeonline"></a>
### `UpgradeOnline`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：在线升级到最新版本。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-upgradepatch"></a>
### `upgradePatch`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：升级补丁包。

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-upgradeto"></a>
### `upgradeTo`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：升级到一个已存在的本地版本。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `versionName` | `String` | - | 已有本地版本的名称 |
| `upgradeBy` | `String` | - | 升级方式 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-versionpackage"></a>
### `versionPackage`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：从文件中解包版本包。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `filename` | `String` | - | 已上传更新包的文件名 |
| `password` | `String` | - | 已上传升级安装包的密码 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-vsgcollect"></a>
### `vsgCollect`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：VSG 采集。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `id` | `String` | 1 | GVS 设备 ID |
| `cmd` | `String` | - | 开始\|停止\|查询 |
| `param` | `String` | - | 采集字符串 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-wideband-attack"></a>
### `wideband_attack`

- 接口类型：`Mutation`
- 返回类型：`WidebandJammer`
- 接口描述：切换宽带干扰器的启用 / 禁用状态。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `band` | `String` | - | 以字符串指定一个频段，取值可为 band4/band9/band12/band14/band15/band18/band24/band58。 |
| `wb_status` | `Boolean` | false | 宽带干扰器状态，true 表示开启，false 表示关闭 |
| `gain` | `Int` | constants.DEFUALT_GAIN | 宽带干扰器的增益 |
| `direction` | `Float` | -1.0 | 宽带干扰器的方向 |
| `elevation` | `Float` | constants.DEFUALT_ELEV | 宽带干扰器的俯仰角 |
| `directional` | `Boolean` | false | 使用定向打击 |
| `jammer_list` | `[String]` | []interface{}{} | 打击使用的干扰器列表，例如：wideband_attack(jammer_list:["1"],band:"band12") |

#### 返回值定义

- 返回值说明：宽带干扰器实体（已弃用）

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `band4` | Int | 433M 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band9` | Int | 900M 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band12` | Int | 1.2G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band14` | Int | 1.4G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band15` | Int | 1.5G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band18` | Int | 1.8G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band24` | Int | 2.4G 频段状态，0:不可用，1:空闲，其他:忙碌。 |
| `band58` | Int | 5.8G 频段状态，0:不可用，1:空闲，其他:忙碌。 |


<a id="mutation-wifibglearning"></a>
### `wifiBgLearning`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：开始或停止对背景 WiFi 信号的学习。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enable` | `Boolean` | - | true 表示开始学习，false 表示停止 |
| `reset` | `Boolean` | - | true 表示删除当前数据并重新创建 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-wificonnect"></a>
### `wifiConnect`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `ssid` | `String` | - | WiFi 的 SSID |
| `password` | `String` | - | WiFi 密码 |
| `action` | `String` | connect | 操作：连接或断开连接 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-wifirescan"></a>
### `wifiRescan`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

无参数。

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-wifistatus"></a>
### `wifiStatus`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：-

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `enabled` | `Boolean` | - | 更新 WiFi 设备状态：true 表示启用；false 表示禁用 |

#### 返回值定义

标量类型，无字段定义。


<a id="mutation-withdrawfalsealarm"></a>
### `withdrawFalseAlarm`

- 接口类型：`Mutation`
- 返回类型：`String`
- 接口描述：撤回误报事件。

#### 参数定义

| 参数 | 类型 | 默认值 | 说明 |
| --- | --- | --- | --- |
| `drone_id` | `String` | - | 待查询的无人机 ID |
| `drone_type` | `String` | - | 待查询的无人机类型 |

#### 返回值定义

标量类型，无字段定义。
