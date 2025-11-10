# DingTalk Gateway HA 集成安装指南

## 📦 安装步骤

### 方法一：手动安装（推荐）

1. **下载文件**
   
   将整个 `custom_components/dingtalk_gateway` 目录复制到你的 Home Assistant 配置目录下：

   ```
   <你的HA配置目录>/
   └── custom_components/
       └── dingtalk_gateway/
           ├── __init__.py
           ├── client.py
           ├── config_flow.py
           ├── const.py
           ├── manifest.json
           ├── sensor.py
           ├── services.yaml
           ├── strings.json
           └── translations/
               └── zh-Hans.json
   ```

2. **重启 Home Assistant**

   通过界面或命令行重启 HA：
   ```bash
   ha core restart
   ```

3. **添加集成**

   - 进入 **配置** → **设备与服务**
   - 点击右下角 **+ 添加集成**
   - 搜索 **"DingTalk Gateway"**
   - 填写配置信息

### 方法二：通过 HACS（未来支持）

_待 HACS 商店收录后，可以通过 HACS 一键安装。_

## ⚙️ 配置要求

### 必需信息

- **Gateway 服务地址**: 运行中的 dingtalk-ha-gateway 服务地址
  - 示例：`http://192.168.1.100:8099`
  - 本地：`http://localhost:8099`
  
- **访问令牌**（可选）: 如果 Gateway 配置了 `GATEWAY_TOKEN`，需要填写相同的令牌

### Gateway 服务准备

在安装 HA 集成之前，确保：

1. ✅ dingtalk-ha-gateway 服务已安装
2. ✅ Gateway 服务正在运行
3. ✅ 可以访问 Gateway 的健康检查端点：
   ```bash
   curl http://<gateway-address>:8099/health
   # 应返回: {"status": "ok", "channel": "dingtalk"}
   ```

## 🔧 配置步骤

### 1. 添加集成

进入 Home Assistant:

1. **配置** → **设备与服务**
2. 点击 **+ 添加集成**
3. 搜索框输入：`DingTalk`
4. 选择 **"DingTalk Gateway"**

### 2. 填写配置

**Gateway 服务地址：**
- 如果 Gateway 和 HA 在同一台机器：`http://localhost:8099`
- 如果在不同机器：`http://192.168.1.xxx:8099`（替换为实际 IP）
- 使用域名：`http://gateway.yourdomain.com:8099`

**访问令牌（可选）：**
- 如果 Gateway 的 `.env` 中设置了 `GATEWAY_TOKEN=xxx`
- 则这里填写相同的 token
- 如果 Gateway 未设置 token，此处留空

### 3. 验证安装

配置完成后，检查：

#### 3.1 实体检查

进入 **开发者工具** → **状态**：

- 应该看到：`sensor.dingtalk_gateway_last_message`
- 初始状态：`等待消息...`

#### 3.2 服务检查

进入 **开发者工具** → **服务**：

应该看到两个服务：
- `dingtalk_gateway.send_message`
- `dingtalk_gateway.send_markdown`

#### 3.3 连接检查

查看 Home Assistant 日志（**配置** → **日志**）：

应该看到：
```
[custom_components.dingtalk_gateway.client] Gateway WebSocket connected
```

## 🧪 测试功能

### 测试 1：发送消息

在 **开发者工具** → **服务** 中执行：

```yaml
service: dingtalk_gateway.send_message
data:
  target: "your_userid_here"  # 替换为你的钉钉 userid
  message: "测试消息：Hello from HA!"
```

**如何获取 userid？**

1. 方法一：在钉钉开放平台"通讯录管理"中查看员工信息
2. 方法二：先让同事发消息给机器人，从 sensor 属性中看到 `sender`
3. 方法三：查看 Home Assistant 日志，发消息后会显示 sender ID

### 测试 2：接收消息

1. 在钉钉中找到你的应用机器人
2. 给机器人发送消息："测试"
3. 检查 HA 中的 sensor：
   - `sensor.dingtalk_gateway_last_message` 的状态应该变为"测试"
4. 查看 sensor 的属性，应该包含：
   - `sender`: 发送者 ID
   - `sender_name`: 发送者名称
   - `timestamp`: 时间戳

### 测试 3：事件触发

创建一个简单的自动化：

```yaml
automation:
  - alias: "测试钉钉事件"
    trigger:
      - platform: event
        event_type: dingtalk_gateway_message
    action:
      - service: persistent_notification.create
        data:
          title: "收到钉钉消息"
          message: "来自 {{ trigger.event.data.sender_name }}: {{ trigger.event.data.content }}"
```

给机器人发消息，HA 界面应该弹出通知。

## 🔧 高级配置

### 启用调试日志

如果遇到问题，启用详细日志：

```yaml
# configuration.yaml
logger:
  default: info
  logs:
    custom_components.dingtalk_gateway: debug
```

重启 HA 后，日志会显示更多详细信息。

### 多个 Gateway 实例

如果需要连接多个 Gateway（例如不同的钉钉应用）：

1. 重复"添加集成"步骤
2. 使用不同的 Gateway 地址
3. 每个实例会创建独立的 sensor 和服务

### 自定义 Sensor 名称

可以通过 HA 界面重命名 sensor：

1. 进入 **配置** → **设备与服务**
2. 找到 **DingTalk Gateway**
3. 点击进入设备详情
4. 点击实体名称旁的设置图标
5. 修改"实体 ID"和"名称"

## 🔍 故障排查

### 问题 1: 找不到集成

**症状**：在"添加集成"中搜索不到 DingTalk Gateway

**解决方法**：
1. 确认 `custom_components/dingtalk_gateway` 目录结构正确
2. 检查文件权限（Linux 需要 HA 用户可读）
3. 重启 Home Assistant
4. 清除浏览器缓存

### 问题 2: WebSocket 连接失败

**症状**：日志中出现 "Gateway connection failed"

**解决方法**：
1. 确认 Gateway 服务正在运行
   ```bash
   curl http://<gateway-address>:8099/health
   ```
2. 检查网络连接和防火墙设置
3. 确认 Gateway 地址填写正确
4. 如果设置了 token，确认 token 正确

### 问题 3: 发送消息失败

**症状**：调用服务时报错

**解决方法**：
1. 检查 Gateway 日志，查看具体错误
2. 确认 userid 格式正确
3. 确认 Gateway 的钉钉配置正确
4. 测试 Gateway API：
   ```bash
   curl -X POST http://<gateway-address>:8099/send_message \
     -H "Content-Type: application/json" \
     -d '{"target":"userid","content":"test"}'
   ```

### 问题 4: 收不到消息

**症状**：给机器人发消息，HA 没有响应

**解决方法**：
1. 检查钉钉应用配置：
   - 应用已发布
   - 可见范围包含发送者
   - Stream 推送已开启
   - 订阅了"机器人接收消息"事件
2. 检查 Gateway 日志，看是否收到消息
3. 确认 WebSocket 连接正常（查看 HA 日志）

## 📝 配置文件示例

### 完整的自动化示例

```yaml
# automations.yaml
- alias: "钉钉控制灯光"
  trigger:
    - platform: event
      event_type: dingtalk_gateway_message
  condition:
    - condition: template
      value_template: >
        {{ trigger.event.data.content in ['开灯', '关灯'] }}
  action:
    - choose:
        - conditions:
            - condition: template
              value_template: "{{ trigger.event.data.content == '开灯' }}"
          sequence:
            - service: light.turn_on
              target:
                entity_id: light.living_room
            - service: dingtalk_gateway.send_message
              data:
                target: "{{ trigger.event.data.sender }}"
                message: "✅ 已开启客厅灯"
        - conditions:
            - condition: template
              value_template: "{{ trigger.event.data.content == '关灯' }}"
          sequence:
            - service: light.turn_off
              target:
                entity_id: light.living_room
            - service: dingtalk_gateway.send_message
              data:
                target: "{{ trigger.event.data.sender }}"
                message: "✅ 已关闭客厅灯"

- alias: "每日状态报告"
  trigger:
    - platform: time
      at: "08:00:00"
  action:
    - service: dingtalk_gateway.send_markdown
      data:
        target: "your_userid"
        title: "早安！今日家居状态"
        content: |
          # 🏠 智能家居状态
          
          **室内温度**: {{ states('sensor.temperature') }}°C  
          **室内湿度**: {{ states('sensor.humidity') }}%  
          **灯光状态**: {{ states('light.living_room') }}
          
          ---
          _{{ now().strftime('%Y年%m月%d日 %H:%M') }}_
```

### Lovelace 卡片示例

```yaml
# ui-lovelace.yaml
- type: entities
  title: 钉钉消息
  entities:
    - entity: sensor.dingtalk_gateway_last_message
      name: 最新消息
    - type: attribute
      entity: sensor.dingtalk_gateway_last_message
      attribute: sender_name
      name: 发送者
    - type: attribute
      entity: sensor.dingtalk_gateway_last_message
      attribute: received_at
      name: 接收时间
```

## ✅ 安装验收清单

- [ ] 集成已添加到 Home Assistant
- [ ] Sensor 实体显示正常
- [ ] 服务可以在开发者工具中找到
- [ ] WebSocket 连接成功（查看日志）
- [ ] 测试发送消息成功
- [ ] 测试接收消息成功
- [ ] 事件触发正常工作
- [ ] 自动化按预期执行

## 🎉 安装完成

恭喜！钉钉 Gateway 集成已成功安装。现在你可以：

- 通过钉钉控制智能家居设备
- 接收 Home Assistant 的通知和警报
- 创建复杂的自动化场景
- 远程查询设备状态

## 📚 下一步

- 查看 [README.md](./README.md) 了解更多使用示例
- 查看 [部署指南](../dingtalk-ha-gateway/DEPLOYMENT_GUIDE.md) 了解 Gateway 配置
- 加入社区分享你的使用经验

---

**祝你使用愉快！** 🚀
