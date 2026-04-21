package graphql

import (
	"bytes"
	"encoding/json"
	"fmt"
	"io"
	"net/http"
	"strings"
	"text/template"
)

// Client GraphQL API 客户端
type Client struct {
	BaseURL string
	Token   string
	client  *http.Client
}

// NewClient 创建客户端
func NewClient(baseURL string) *Client {
	return &Client{
		BaseURL: baseURL,
		client:  &http.Client{},
	}
}

// Login 登录获取 Token
func (c *Client) Login(username, password string) (map[string]interface{}, error) {
	query := renderTemplate(LoginMutation, map[string]interface{}{
		"Username": username,
		"Password": password,
	})
	result, err := c.execute(query)
	if err != nil {
		return nil, err
	}
	if data, ok := result["data"].(map[string]interface{}); ok {
		if login, ok := data["login"].(map[string]interface{}); ok {
			if token, ok := login["token"].(string); ok {
				c.Token = token
			}
		}
	}
	return result, nil
}

// renderTemplate 渲染模板
func renderTemplate(tmpl string, data map[string]interface{}) string {
	// 将布尔值转换为 Go 的 true/false 格式
	for k, v := range data {
		if b, ok := v.(bool); ok {
			data[k] = fmt.Sprintf("%v", b)
		}
	}

	t, err := template.New("query").Parse(tmpl)
	if err != nil {
		return tmpl
	}
	var buf bytes.Buffer
	t.Execute(&buf, data)
	return buf.String()
}

// execute 执行 GraphQL 请求
func (c *Client) execute(query string) (map[string]interface{}, error) {
	body := map[string]string{"query": query}
	jsonBody, _ := json.Marshal(body)

	req, err := http.NewRequest("POST", c.BaseURL, bytes.NewBuffer(jsonBody))
	if err != nil {
		return nil, err
	}

	req.Header.Set("Content-Type", "application/json")
	if c.Token != "" {
		req.Header.Set("Authorization", "Bearer "+c.Token)
	}

	// 忽略 SSL 证书验证（内网环境）
	resp, err := c.client.Do(req)
	if err != nil {
		return nil, err
	}
	defer resp.Body.Close()

	respBody, err := io.ReadAll(resp.Body)
	if err != nil {
		return nil, err
	}

	var result map[string]interface{}
	json.Unmarshal(respBody, &result)
	return result, nil
}

// ==================== 查询接口 ====================

// GetDrone 查询单个无人机
func (c *Client) GetDrone(droneID string) (map[string]interface{}, error) {
	query := renderTemplate(DroneQuery, map[string]interface{}{"DroneID": droneID})
	return c.execute(query)
}

// GetAllDrones 查询所有无人机
func (c *Client) GetAllDrones() (map[string]interface{}, error) {
	return c.execute(DronesAllQuery)
}

// GetBlacklist 查询黑名单
func (c *Client) GetBlacklist() (map[string]interface{}, error) {
	return c.execute(BlacklistQuery)
}

// GetWhitelist 查询白名单
func (c *Client) GetWhitelist() (map[string]interface{}, error) {
	return c.execute(WhitelistQuery)
}

// GetDevices 查询设备信息
func (c *Client) GetDevices(deviceID string) (map[string]interface{}, error) {
	query := renderTemplate(DevicesQuery, map[string]interface{}{"DeviceID": deviceID})
	return c.execute(query)
}

// GetSensor 查询传感器信息
func (c *Client) GetSensor(sensorID string) (map[string]interface{}, error) {
	query := renderTemplate(SensorQuery, map[string]interface{}{"SensorID": sensorID})
	return c.execute(query)
}

// GetEvents 查询事件
func (c *Client) GetEvents(droneID, droneType, beginTime, endTime string, from int) (map[string]interface{}, error) {
	query := renderTemplate(EventsQuery, map[string]interface{}{
		"DroneID":   droneID,
		"DroneType": droneType,
		"BeginTime": beginTime,
		"EndTime":   endTime,
		"From":      from,
	})
	return c.execute(query)
}

// GetEventsAggregation 事件聚合查询
func (c *Client) GetEventsAggregation(offset, limit int, beginTime, endTime, order, orderBy string) (map[string]interface{}, error) {
	query := renderTemplate(EventsAggregationQuery, map[string]interface{}{
		"Offset":    offset,
		"Limit":     limit,
		"BeginTime": beginTime,
		"EndTime":   endTime,
		"Order":     order,
		"OrderBy":   orderBy,
	})
	return c.execute(query)
}

// GetDroneTraces 查询历史轨迹
func (c *Client) GetDroneTraces(from, to int) (map[string]interface{}, error) {
	query := renderTemplate(DroneTracesQuery, map[string]interface{}{"From": from, "To": to})
	return c.execute(query)
}

// GetReport 查询统计报告
func (c *Client) GetReport(fromTime, toTime string) (map[string]interface{}, error) {
	query := renderTemplate(ReportQuery, map[string]interface{}{
		"FromTime": fromTime,
		"ToTime":   toTime,
	})
	return c.execute(query)
}

// GetDetectingBands 查询检测频段状态
func (c *Client) GetDetectingBands() (map[string]interface{}, error) {
	return c.execute(DetectingBandsQuery)
}

// GetWidebandJammer 查询宽频干扰状态
func (c *Client) GetWidebandJammer(directional bool) (map[string]interface{}, error) {
	query := renderTemplate(WidebandJammerQuery, map[string]interface{}{"Directional": directional})
	return c.execute(query)
}

// GetJammerCooldown 查询干扰器冷却状态
func (c *Client) GetJammerCooldown() (map[string]interface{}, error) {
	return c.execute(JammerCooldownQuery)
}

// GetAutoAttackStatus 查询无人值守状态
func (c *Client) GetAutoAttackStatus() (map[string]interface{}, error) {
	return c.execute(AutoAttackQuery)
}

// GetAutoAttackConfig 查询无人值守配置
func (c *Client) GetAutoAttackConfig() (map[string]interface{}, error) {
	return c.execute(AutoAttackConfigQuery)
}

// GetAirDefenceArea 查询防空区
func (c *Client) GetAirDefenceArea() (map[string]interface{}, error) {
	return c.execute(AirDefenceAreaQuery)
}

// GetSpoofStatus 查询诱骗器状态
func (c *Client) GetSpoofStatus() (map[string]interface{}, error) {
	return c.execute(SpoofStatusQuery)
}

// GetVersion 查询设备版本
func (c *Client) GetVersion() (map[string]interface{}, error) {
	return c.execute(VersionQuery)
}

// GetTime 查询系统时间
func (c *Client) GetTime() (map[string]interface{}, error) {
	return c.execute(TimeQuery)
}

// GetTimezone 查询系统时区
func (c *Client) GetTimezone() (map[string]interface{}, error) {
	return c.execute(TimezoneQuery)
}

// GetStorage 查询存储空间
func (c *Client) GetStorage() (map[string]interface{}, error) {
	return c.execute(StorageQuery)
}

// GetNodes 查询组网节点
func (c *Client) GetNodes(nodeID string) (map[string]interface{}, error) {
	query := renderTemplate(NodesQuery, map[string]interface{}{"NodeID": nodeID})
	return c.execute(query)
}

// ==================== 操作接口 ====================

// AddBlacklist 添加黑名单
func (c *Client) AddBlacklist(droneID, droneType, alias string) (map[string]interface{}, error) {
	query := renderTemplate(AddBlacklistMutation, map[string]interface{}{
		"DroneID":   droneID,
		"DroneType": droneType,
		"Alias":     alias,
	})
	return c.execute(query)
}

// DeleteBlacklist 移除黑名单
func (c *Client) DeleteBlacklist(droneID string) (map[string]interface{}, error) {
	query := renderTemplate(DeleteBlacklistMutation, map[string]interface{}{"DroneID": droneID})
	return c.execute(query)
}

// AddWhitelist 添加白名单
func (c *Client) AddWhitelist(droneID, droneType, alias, timeRange string) (map[string]interface{}, error) {
	query := renderTemplate(AddWhitelistMutation, map[string]interface{}{
		"DroneID":   droneID,
		"DroneType": droneType,
		"Alias":     alias,
		"TimeRange": timeRange,
	})
	return c.execute(query)
}

// DeleteWhitelist 移除白名单
func (c *Client) DeleteWhitelist(droneID string) (map[string]interface{}, error) {
	query := renderTemplate(DeleteWhitelistMutation, map[string]interface{}{"DroneID": droneID})
	return c.execute(query)
}

// Attack 精准打击
func (c *Client) Attack(droneID string, cancel bool) (map[string]interface{}, error) {
	query := renderTemplate(AttackMutation, map[string]interface{}{
		"DroneID": droneID,
		"Cancel":  cancel,
	})
	return c.execute(query)
}

// CtrlLanding 迫降
func (c *Client) CtrlLanding(droneID string, enable bool) (map[string]interface{}, error) {
	query := renderTemplate(CtrlLandingMutation, map[string]interface{}{
		"DroneID": droneID,
		"Enable":  enable,
	})
	return c.execute(query)
}

// SetAutoAttack 设置无人值守
func (c *Client) SetAutoAttack(on, saEnabled, wbEnabled, dirWbEnabled, spfEnabled, protectWhite bool) (map[string]interface{}, error) {
	query := renderTemplate(AutoAttackMutation, map[string]interface{}{
		"On":          on,
		"SaEnabled":   saEnabled,
		"WbEnabled":   wbEnabled,
		"DirWbEnabled": dirWbEnabled,
		"SpfEnabled":  spfEnabled,
		"ProtectWhite": protectWhite,
	})
	return c.execute(query)
}

// WidebandAttack 宽频干扰
func (c *Client) WidebandAttack(band string, wbStatus bool, gain, direction, elevation int, directional bool, jammerList string) (map[string]interface{}, error) {
	query := renderTemplate(WidebandAttackMutation, map[string]interface{}{
		"Band":       band,
		"WbStatus":   wbStatus,
		"Gain":       gain,
		"Direction":  direction,
		"Elevation":  elevation,
		"Directional": directional,
		"JammerList": jammerList,
	})
	return c.execute(query)
}

// DirectionalAttack 定向打击
func (c *Client) DirectionalAttack(status bool, band string, gain int, droneID string) (map[string]interface{}, error) {
	query := renderTemplate(DirectionalWBAttackMutation, map[string]interface{}{
		"Status":   status,
		"Band":     band,
		"Gain":     gain,
		"DroneID":  droneID,
	})
	return c.execute(query)
}

// SpooferSwitch 诱骗设置
func (c *Client) SpooferSwitch(action, timeout, direction int, spooferID string) (map[string]interface{}, error) {
	query := renderTemplate(SpooferSwitchMutation, map[string]interface{}{
		"SpooferID": spooferID,
		"Action":    action,
		"Timeout":   timeout,
		"Direction": direction,
	})
	return c.execute(query)
}

// SetAirDefenceArea 绘制防空区
func (c *Client) SetAirDefenceArea(areaData string) (map[string]interface{}, error) {
	query := renderTemplate(AirDefenceAreaMutation, map[string]interface{}{"AreaData": areaData})
	return c.execute(query)
}

// SetDetectingBand 检测频段开关
func (c *Client) SetDetectingBand(band string, enable bool) (map[string]interface{}, error) {
	query := renderTemplate(DetectingBandsMutation, map[string]interface{}{
		"Band":   band,
		"Enable": enable,
	})
	return c.execute(query)
}

// DeleteEvents 删除事件
func (c *Client) DeleteEvents(sequenceList []int) (map[string]interface{}, error) {
	listStr := fmt.Sprintf("%v", sequenceList)
	query := strings.Replace(DeleteEventsMutation, "{{.SequenceList}}", listStr, 1)
	return c.execute(query)
}

// DeleteEventsByID 根据ID删除事件
func (c *Client) DeleteEventsByID(droneID, droneType string, all bool) (map[string]interface{}, error) {
	query := renderTemplate(DeleteEventsByIDMutation, map[string]interface{}{
		"DroneID":   droneID,
		"DroneType": droneType,
		"All":       all,
	})
	return c.execute(query)
}

// MarkFalseAlarm 标记误报
func (c *Client) MarkFalseAlarm(sequenceList []int) (map[string]interface{}, error) {
	listStr := fmt.Sprintf("%v", sequenceList)
	query := strings.Replace(MarkFalseAlarmMutation, "{{.SequenceList}}", listStr, 1)
	return c.execute(query)
}

// WithdrawFalseAlarm 还原误报
func (c *Client) WithdrawFalseAlarm(droneType, droneID string) (map[string]interface{}, error) {
	query := renderTemplate(WithdrawFalseAlarmMutation, map[string]interface{}{
		"DroneType": droneType,
		"DroneID":   droneID,
	})
	return c.execute(query)
}

// TdoaTrack TDOA跟踪
func (c *Client) TdoaTrack(droneID string, enable bool) (map[string]interface{}, error) {
	query := renderTemplate(TdoaTrackMutation, map[string]interface{}{
		"DroneID": droneID,
		"Enable":  enable,
	})
	return c.execute(query)
}

// Tracking 视觉跟踪
func (c *Client) Tracking(deviceID, droneUUID string) (map[string]interface{}, error) {
	query := renderTemplate(TrackingMutation, map[string]interface{}{
		"DeviceID":  deviceID,
		"DroneUUID": droneUUID,
	})
	return c.execute(query)
}

// StageReset 定向复位
func (c *Client) StageReset(jammerID string, direction, elevation float64, trackEnable bool) (map[string]interface{}, error) {
	query := renderTemplate(StageResetMutation, map[string]interface{}{
		"JammerID":    jammerID,
		"Direction":   direction,
		"Elevation":   elevation,
		"TrackEnable": trackEnable,
	})
	return c.execute(query)
}

// ResetDevice 重启设备
func (c *Client) ResetDevice(deviceID, deviceClass, reason string) (map[string]interface{}, error) {
	query := renderTemplate(ResetMutation, map[string]interface{}{
		"DeviceID":    deviceID,
		"DeviceClass": deviceClass,
		"Reason":      reason,
	})
	return c.execute(query)
}

// SetTime 设置系统时间
func (c *Client) SetTime(timestamp int64) (map[string]interface{}, error) {
	query := strings.Replace(TimeMutation, "{{.Timestamp}}", fmt.Sprintf("%d", timestamp), 1)
	return c.execute(query)
}

// SetTimezone 设置时区
func (c *Client) SetTimezone(timezone string, auto bool) (map[string]interface{}, error) {
	query := renderTemplate(TimezoneMutation, map[string]interface{}{
		"TimeZone": timezone,
		"Auto":     auto,
	})
	return c.execute(query)
}

// SetGeoLocation 设置设备位置
func (c *Client) SetGeoLocation(lat, lng float64) (map[string]interface{}, error) {
	query := renderTemplate(SetGeoLocationMutation, map[string]interface{}{
		"Lat": lat,
		"Lng": lng,
	})
	return c.execute(query)
}

// ClearStorage 清除存储
func (c *Client) ClearStorage() (map[string]interface{}, error) {
	return c.execute(ClearStorageMutation)
}

// UpgradeTo 版本升级
func (c *Client) UpgradeTo(versionName, upgradeBy string) (map[string]interface{}, error) {
	query := renderTemplate(UpgradeToMutation, map[string]interface{}{
		"VersionName": versionName,
		"UpgradeBy":   upgradeBy,
	})
	return c.execute(query)
}