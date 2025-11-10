# DingTalk Gateway - Home Assistant 集成

Home Assistant 自定义集成，用于连接钉钉（DingTalk）Gateway 服务。

## ✨ 特性

- ✅ **实时消息接收** - 通过 WebSocket 接收钉钉消息
- ✅ **消息发送** - 通过自定义服务发送消息
- ✅ **Markdown 支持** - 发送富文本 Markdown 消息
- ✅ **Sensor 实体** - 显示最新收到的消息
- ✅ **事件触发** - 消息触发 HA 自动化
- ✅ **高性能** - 优化的异步架构
- ✅ **私聊和群聊** - 支持私聊和群组消息

## 📋 版本

**当前版本：v0.1.0**

### 核心功能
- WebSocket 实时消息接收
- 文本和 Markdown 消息发送
- 完整的事件和 Sensor 支持
- 智能重连机制

## 🚀 快速开始

### 1. 安装

将 `custom_components/dingtalk_gateway` 目录复制到您的 Home Assistant 配置目录：

```
<config_dir>/custom_components/dingtalk_gateway/
```

### 2. 重启 Home Assistant

### 3. 添加集成

1. **配置** → **设备与服务** → **添加集成**
2. 搜索 **"DingTalk Gateway"**
3. 填写配置：
   - **Gateway 服务地址**: 如：`http://192.168.1.100:8099`
   - **访问令牌**: 可选，如果 Gateway 配置了令牌

### 4. 使用服务发送消息

```yaml
service: dingtalk_gateway.send_message
data:
  target: "userid123"  # 钉钉用户ID
  message: "Hello from Home Assistant!"
```

## 🎯 使用示例

### 发送文本消息

```yaml
service: dingtalk_gateway.send_message
data:
  target: "manager001"
  message: "门铃已响"
```

### 发送 Markdown 消息

```yaml
service: dingtalk_gateway.send_markdown
data:
  target: "manager001"
  title: "系统状态"
  content: |
    # 智能家居状态报告
    
    **温度**: 22°C  
    **湿度**: 60%  
    **灯光**: 已关闭
```

### 自动化回复

```yaml
automation:
  - alias: "钉钉自动回复"
    trigger:
      - platform: event
        event_type: dingtalk_gateway_message
    condition:
      - condition: template
        value_template: "{{ trigger.event.data.content == '状态' }}"
    action:
      - service: dingtalk_gateway.send_message
        data:
          target: "{{ trigger.event.data.sender }}"
          message: "系统运行正常！当前温度：{{ states('sensor.temperature') }}°C"
```

### 智能家居控制

```yaml
automation:
  - alias: "钉钉控制灯光"
    trigger:
      - platform: event
        event_type: dingtalk_gateway_message
    condition:
      - condition: template
        value_template: "{{ '开灯' in trigger.event.data.content }}"
    action:
      - service: light.turn_on
        target:
          entity_id: light.living_room
      - service: dingtalk_gateway.send_message
        data:
          target: "{{ trigger.event.data.sender }}"
          message: "✅ 已开启客厅灯光"
```

### 门铃通知

```yaml
automation:
  - alias: "门铃通知到钉钉"
    trigger:
      - platform: state
        entity_id: binary_sensor.doorbell
        to: "on"
    action:
      - service: dingtalk_gateway.send_markdown
        data:
          target: "userid123"
          title: "🔔 门铃提醒"
          content: |
            # 有人按门铃
            
            **时间**: {{ now().strftime('%Y-%m-%d %H:%M:%S') }}  
            **位置**: 前门
```

## 🔌 可用服务

### `dingtalk_gateway.send_message`

发送文本消息到钉钉用户或群组。

**参数：**
- `target` (必填): 目标用户ID
- `message` (必填): 消息内容
- `at_list` (可选): 群聊中@的用户列表

### `dingtalk_gateway.send_markdown`

发送 Markdown 格式消息。

**参数：**
- `target` (必填): 目标用户ID
- `title` (可选): 消息标题，默认"通知"
- `content` (必填): Markdown 内容

## 📊 实体

### Sensor

- `sensor.dingtalk_gateway_last_message` - 最新收到的消息

**属性：**
- `sender`: 发送者用户ID
- `sender_name`: 发送者名称
- `room_id`: 群聊ID（如果适用）
- `timestamp`: 消息时间戳
- `received_at`: HA 接收时间
- `is_group`: 是否群聊消息

### 事件

- `dingtalk_gateway_message` - 收到新消息时触发

**事件数据：**
```json
{
  "msg_id": "消息ID",
  "sender": "userid123",
  "sender_name": "张三",
  "content": "消息内容",
  "is_group": false,
  "timestamp": 1699999999
}
```

## 🏗️ 架构

```
钉钉 ←→ Gateway ←→ HA 集成
                    ├─ WebSocket 连接（消息接收）
                    ├─ REST API（消息发送）
                    ├─ Sensor 实体
                    ├─ 事件触发
                    └─ 自定义服务
```

## 🔧 调试

启用详细日志：

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.dingtalk_gateway: debug
```

## 🤝 配套项目

- [dingtalk-ha-gateway](../dingtalk-ha-gateway) - Gateway 服务

## ⚙️ 要求

- Home Assistant 2023.x 或更高版本
- Python 3.11+
- [dingtalk-ha-gateway](../dingtalk-ha-gateway) 服务运行中

## 📝 许可证

MIT License

## 🙏 致谢

感谢 Home Assistant 社区和开源贡献者。

---

**享受您的智能家居钉钉集成！** 🏠📱
