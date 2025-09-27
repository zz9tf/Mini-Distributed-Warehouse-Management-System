# 📊 操作日志系统

## 功能概述

这个日志系统可以按时间线记录所有服务的操作历史，包括：

- ✅ **操作记录**: 记录所有 gRPC 操作（PlaceOrder, PutItem, UpdateItem, ListItems）
- 📅 **时间线**: 按时间顺序显示所有操作
- 📈 **统计信息**: 显示成功率、服务统计、操作统计
- 🔍 **过滤查询**: 按服务、操作类型过滤日志
- 💾 **持久化**: 日志保存到 JSON 文件

## 文件结构

```
├── operation_logger.py      # 日志记录器核心模块
├── log_viewer.py           # 日志查看器工具
├── test_logging.py         # 日志功能测试
├── add_logging.py          # 自动添加日志记录脚本
└── operation_log.json      # 日志数据文件（自动生成）
```

## 使用方法

### 1. 查看时间线日志

```bash
# 显示最近20条操作记录
python log_viewer.py --timeline

# 显示最近50条操作记录
python log_viewer.py --timeline --limit 50
```

### 2. 查看统计信息

```bash
# 显示操作统计
python log_viewer.py --stats
```

### 3. 按服务过滤

```bash
# 查看 FreshService 的日志
python log_viewer.py --service FreshService

# 查看 APIGateway 的日志
python log_viewer.py --service APIGateway
```

### 4. 按操作类型过滤

```bash
# 查看所有 PlaceOrder 操作
python log_viewer.py --operation PlaceOrder

# 查看所有 UpdateItem 操作
python log_viewer.py --operation UpdateItem
```

### 5. 测试日志功能

```bash
# 运行日志功能测试
python test_logging.py
```

## 日志格式

每条日志记录包含以下信息：

```json
{
  "timestamp": "2024-01-01T12:00:00.000000",
  "service": "FreshService",
  "operation": "PlaceOrder",
  "client_ip": "127.0.0.1:12345",
  "success": true,
  "request": {
    "category": "fruits",
    "subcategory": "apple",
    "item": 1
  },
  "response": {
    "status": "ok",
    "left": 49
  },
  "error": null
}
```

## 在 Docker 中使用

### 1. 启动服务

```bash
docker compose up --build
```

### 2. 查看日志

```bash
# 进入容器查看日志
docker exec -it <container_name> python log_viewer.py --timeline

# 或者将日志文件复制到主机
docker cp <container_name>:/app/operation_log.json ./operation_log.json
```

### 3. 实时监控

```bash
# 在另一个终端中实时查看日志
docker exec -it <container_name> python log_viewer.py --timeline --limit 10
```

## 日志记录的服务

- 🥬 **FreshService**: 新鲜食品服务
- 🏠 **ApplianceService**: 家电服务
- 🍎 **FoodService**: 食品服务（转发层）
- 📱 **ElectronicsService**: 电子产品服务（转发层）
- 🌐 **APIGateway**: API 网关（路由层）

## 日志记录的操作

- 🛒 **PlaceOrder**: 下单操作
- 📦 **PutItem**: 放入货物操作
- 📤 **UpdateItem**: 更新货物操作
- 📋 **ListItems**: 查询货物操作

## 示例输出

### 时间线日志

```
📊 OPERATION TIMELINE LOG
================================================================================
 1. ✅ [2024-01-01T12:00:00] FreshService - PlaceOrder
    📍 Client: 127.0.0.1:12345
    📥 Request: {'category': 'fruits', 'subcategory': 'apple', 'item': 1}
    📤 Response: {'status': 'ok', 'left': 49}

 2. ✅ [2024-01-01T12:00:01] APIGateway - UpdateItem
    📍 Client: 127.0.0.1:12346
    📥 Request: {'category': 'kitchen', 'subcategory': 'refrigerator', 'item': 15}
    📤 Response: {'success': True, 'message': 'Updated kitchen/refrigerator to 15'}
```

### 统计信息

```
📈 OPERATION STATISTICS
================================================================================
📊 Total Operations: 25
✅ Successful: 23
❌ Failed: 2
📈 Success Rate: 92.0%

🏢 Service Statistics:
  FreshService: 10 total, 9 success, 1 failed (90.0%)
  APIGateway: 15 total, 14 success, 1 failed (93.3%)

🔧 Operation Statistics:
  PlaceOrder: 8 total, 7 success, 1 failed (87.5%)
  UpdateItem: 5 total, 5 success, 0 failed (100.0%)
```

## 注意事项

1. **日志文件大小**: 系统自动保持最近 1000 条记录，避免文件过大
2. **性能影响**: 日志记录是异步的，不会影响服务性能
3. **错误处理**: 即使日志记录失败，也不会影响正常的服务操作
4. **文件权限**: 确保应用有写入日志文件的权限

## 故障排除

### 日志文件无法创建

```bash
# 检查文件权限
ls -la operation_log.json

# 手动创建日志文件
touch operation_log.json
chmod 666 operation_log.json
```

### 日志记录不完整

```bash
# 检查服务是否正确导入日志模块
grep -r "operation_logger" services/
```

### 查看详细错误

```bash
# 查看服务日志
docker logs <container_name>
```
