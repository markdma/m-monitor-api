# NetworkSpecialLineController 返回数据结构

## 返回格式

```json
{
    "count": 10,
    "data": [
        {
            // if_wan 表字段
            "id": "wan_001",
            "name": "专线名称",
            "local_address": "192.168.1.1",
            "hardware_serial_num": "SW001",
            "upload_bandwidth_mb": "100",
            "download_bandwidth_mb": "100",
            "remote_address": "10.0.0.1",
            "remote_hardware_serial_num": "SW002",
            "local_hardware_interface_name": "GigabitEthernet0/1",
            "remote_hardware_interface_name": "GigabitEthernet0/1",
            "type": "专线类型",
            "uptime": "2024-01-01T00:00:00",
            "line_code": "线路编码",
            "access_point": "接入点",
            "isp": "运营商",
            "enabled": 1,
            "create_time": "2024-01-01T00:00:00",
            "netline_type": 1,
            "measure_address": "测量地址",
            "is_use_vpn": 0,
            
            // sw_iprange 关联对象（summary 级别字段）
            "sw_iprange": {
                "iprange": "192.168.1.0/24",
                "serial_num": "SW001",
                "name": "网络设备名称",
                "state": "正常",
                "catalog": "交换机",
                "model": "Cisco-2960",
                "owner_name": "负责人",
                "owner_phone": "13800138000",
                "mc": "模块ID",
                "brand": "品牌",
                "pod": "POD",
                "rack_code": "机架编码",
                "module": null,  // relationship，可能为 null 或对象
                "env": "yslm",
                "enabled": 1,
                "environment": null,  // relationship，可能为 null 或对象
                "community": "public",
                "snmp_port": 161,
                "network_group": "网络组",
                "is_tor": 0,
                "snmp_enabled": 1
            },
            
            // 从 Redis 动态添加的字段
            "ping": "10.5",  // 延迟（毫秒），可能为 null
            "status": 1,     // 状态，默认 0
            "net_in_octet": "1234567890",   // 入流量（字节），可能为 null
            "net_out_octet": "9876543210"   // 出流量（字节），可能为 null
        }
    ]
}
```

## 字段说明

### 1. if_wan 表字段（主表字段）

| 字段名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `id` | String(100) | 专线ID（主键） | `IFWanManage.id` |
| `name` | String(50) | 专线名称 | `IFWanManage.name` |
| `local_address` | String(100) | 本地地址 | `IFWanManage.local_address` |
| `hardware_serial_num` | String | 硬件序列号（外键） | `IFWanManage.hardware_serial_num` |
| `upload_bandwidth_mb` | String(50) | 上传带宽（MB） | `IFWanManage.upload_bandwidth_mb` |
| `download_bandwidth_mb` | String(50) | 下载带宽（MB） | `IFWanManage.download_bandwidth_mb` |
| `remote_address` | String(100) | 远程地址 | `IFWanManage.remote_address` |
| `remote_hardware_serial_num` | String(100) | 远程硬件序列号 | `IFWanManage.remote_hardware_serial_num` |
| `local_hardware_interface_name` | String(100) | 本地硬件接口名称 | `IFWanManage.local_hardware_interface_name` |
| `remote_hardware_interface_name` | String(100) | 远程硬件接口名称 | `IFWanManage.remote_hardware_interface_name` |
| `type` | String(50) | 专线类型 | `IFWanManage.type` |
| `uptime` | DateTime | 更新时间 | `IFWanManage.uptime` |
| `line_code` | String(100) | 线路编码 | `IFWanManage.line_code` |
| `access_point` | String(100) | 接入点 | `IFWanManage.access_point` |
| `isp` | String(50) | 运营商 | `IFWanManage.isp` |
| `enabled` | INT | 是否启用（0/1） | `IFWanManage.enabled` |
| `create_time` | DateTime | 创建时间 | `IFWanManage.create_time` |
| `netline_type` | INT | 专线类型 | `IFWanManage.netline_type` |
| `measure_address` | String(100) | 测量地址 | `IFWanManage.measure_address` |
| `is_use_vpn` | INT | 是否使用VPN（0/1） | `IFWanManage.is_use_vpn` |

### 2. sw_iprange 关联对象字段

`sw_iprange` 是一个嵌套对象，包含关联的网络设备信息。字段来自 `SWIprangeManage.summary_attributes`：

| 字段名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `iprange` | String(50) | IP范围 | `SWIprangeManage.iprange` |
| `serial_num` | String(50) | 序列号（主键） | `SWIprangeManage.serial_num` |
| `name` | String(100) | 设备名称 | `SWIprangeManage.name` |
| `state` | String(20) | 状态 | `SWIprangeManage.state` |
| `catalog` | String(50) | 分类 | `SWIprangeManage.catalog` |
| `model` | String(50) | 型号 | `SWIprangeManage.model` |
| `owner_name` | String(50) | 负责人姓名 | `SWIprangeManage.owner_name` |
| `owner_phone` | String(50) | 负责人电话 | `SWIprangeManage.owner_phone` |
| `mc` | String | 模块ID | `SWIprangeManage.mc` |
| `brand` | String(50) | 品牌 | `SWIprangeManage.brand` |
| `pod` | String(50) | POD | `SWIprangeManage.pod` |
| `rack_code` | String(50) | 机架编码 | `SWIprangeManage.rack_code` |
| `module` | Object/null | 模块对象（relationship） | `SWIprangeManage.module` |
| `env` | String | 环境ID（外键） | `SWIprangeManage.env` |
| `enabled` | INT | 是否启用（0/1） | `SWIprangeManage.enabled` |
| `environment` | Object/null | 环境对象（relationship） | `SWIprangeManage.environment` |
| `community` | String(100) | SNMP社区 | `SWIprangeManage.community` |
| `snmp_port` | INT | SNMP端口 | `SWIprangeManage.snmp_port` |
| `network_group` | String(50) | 网络组 | `SWIprangeManage.network_group` |
| `is_tor` | INT | 是否为TOR | `SWIprangeManage.is_tor` |
| `snmp_enabled` | INT | SNMP是否启用（0/1） | `SWIprangeManage.snmp_enabled` |

**注意**：
- `module` 和 `environment` 是 relationship 字段，如果关联对象存在，会调用 `to_summary_dict()` 返回嵌套对象
- 如果关联对象不存在或未加载，值为 `null`

### 3. Redis 动态字段

这些字段在 `on_get` 方法中从 Redis 动态添加（第186-191行）：

| 字段名 | 类型 | 说明 | 来源 |
|--------|------|------|------|
| `ping` | String/Number/null | 延迟（毫秒） | Redis: `netline.ping` |
| `status` | INT | 状态（默认0） | Redis: `netline.status` |
| `net_in_octet` | String/null | 入流量（字节） | Redis: `netline.in.octet` |
| `net_out_octet` | String/null | 出流量（字节） | Redis: `netline.out.octet` |

**注意**：
- 这些字段的值通过 `wan_id`（即 `if_wan.id`）从 Redis Hash 中获取
- 如果 Redis 中不存在对应的 key，值为 `null`（`status` 默认为 `0`）
- 这些字段是否返回取决于请求参数中的 `fields` 字段（如果指定了 `fields`，只有包含的字段才会返回）

## 字段来源说明

### 数据库字段
- 来自 `IFWanManage.attributes` 列表（第712-715行）
- 通过 `to_dict()` 方法序列化

### 关联对象字段
- `sw_iprange` 来自 `IFWanManage.attributes` 中的 relationship 字段
- 通过 `SWIprangeManage.to_summary_dict()` 序列化
- 包含 `SWIprangeManage.summary_attributes` 中的所有字段（第680-682行）

### 动态字段
- 在 `on_get` 方法的第186-191行动态添加
- 从 Redis Hash 中获取，key 为 `wan_id`（即 `if_wan.id`）

## 字段过滤

可以通过请求参数 `fields` 控制返回的字段：

```python
# 示例：只返回指定字段
GET /api/v1/monitor/network_special_line?fields=id,name,ping,status

# 返回结果中只包含 id, name, ping, status 字段
```

## 排序字段

支持对以下字段进行排序：
- `ping` - 延迟（从 Redis 获取）
- `net_in_octet` - 入流量（从 Redis 获取）
- `net_out_octet` - 出流量（从 Redis 获取）
- 其他数据库字段（通过 `orders` 参数）

默认排序：`name DESC`（专线名称降序）









