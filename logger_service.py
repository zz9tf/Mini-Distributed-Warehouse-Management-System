#!/usr/bin/env python3
"""
LoggerService - 日志服务容器
接收其他服务的日志请求并执行相应的操作
端口: 50055
"""

import grpc
import time
import signal
import sys
import json
from concurrent import futures
from datetime import datetime
from typing import Dict, List, Any
import threading

import warehouse_pb2
import warehouse_pb2_grpc


class LoggerService(warehouse_pb2_grpc.LoggerServiceServicer):
    """
    LoggerService - 日志服务
    接收其他服务的日志请求并执行相应的操作
    """
    
    def __init__(self):
        """Initialize LoggerService"""
        self.logs: List[Dict[str, Any]] = []
        self.lock = threading.Lock()
        self.log_file = "operation_log.json"
        
        # 加载现有日志
        self._load_logs()
        print("📊 LoggerService initialized")
    
    def _load_logs(self):
        """加载现有日志文件"""
        try:
            with open(self.log_file, 'r', encoding='utf-8') as f:
                self.logs = json.load(f)
            print(f"📂 Loaded {len(self.logs)} existing logs")
        except (FileNotFoundError, json.JSONDecodeError):
            self.logs = []
            print("📂 No existing logs found, starting fresh")
    
    def _save_logs(self):
        """保存日志到文件"""
        with self.lock:
            with open(self.log_file, 'w', encoding='utf-8') as f:
                json.dump(self.logs, f, ensure_ascii=False, indent=2)
    
    def LogOperation(self, request, context):
        """记录操作日志"""
        try:
            timestamp = datetime.now().isoformat()
            
            # 解析请求和响应数据
            try:
                request_data = json.loads(request.request_data) if request.request_data else {}
            except json.JSONDecodeError:
                request_data = {"raw": request.request_data}
            
            try:
                response_data = json.loads(request.response_data) if request.response_data else {}
            except json.JSONDecodeError:
                response_data = {"raw": request.response_data}
            
            log_entry = {
                "timestamp": timestamp,
                "service": request.service_name,
                "operation": request.operation,
                "client_ip": request.client_ip,
                "success": request.success,
                "request": request_data,
                "response": response_data,
                "error": request.error_message if request.error_message else None
            }
            
            with self.lock:
                self.logs.append(log_entry)
                # 保持最近1000条记录
                if len(self.logs) > 1000:
                    self.logs = self.logs[-1000:]
            
            # 异步保存，避免阻塞
            threading.Thread(target=self._save_logs, daemon=True).start()
            
            # 打印到控制台
            status_emoji = "✅" if request.success else "❌"
            print(f"📝 {status_emoji} [{timestamp}] {request.service_name} - {request.operation}")
            if request_data:
                print(f"   📥 Request: {request_data}")
            if response_data:
                print(f"   📤 Response: {response_data}")
            if request.error_message:
                print(f"   ❌ Error: {request.error_message}")
            
            return warehouse_pb2.LogResponse(
                success=True,
                message=f"Log recorded successfully"
            )
            
        except Exception as e:
            print(f"❌ [ERROR] LoggerService LogOperation error: {e}")
            return warehouse_pb2.LogResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
    
    def QueryLogs(self, request, context):
        """查询日志"""
        try:
            with self.lock:
                filtered_logs = self.logs.copy()
            
            # 按服务过滤
            if request.service_name:
                filtered_logs = [log for log in filtered_logs if log['service'] == request.service_name]
            
            # 按操作过滤
            if request.operation:
                filtered_logs = [log for log in filtered_logs if log['operation'] == request.operation]
            
            # 按时间排序（最新的在前）
            filtered_logs = sorted(filtered_logs, key=lambda x: x['timestamp'], reverse=True)
            
            # 限制数量
            limit = request.limit if request.limit > 0 else 50
            filtered_logs = filtered_logs[:limit]
            
            # 转换为 protobuf 格式
            log_entries = []
            for log in filtered_logs:
                entry = warehouse_pb2.LogEntry(
                    timestamp=log['timestamp'],
                    service_name=log['service'],
                    operation=log['operation'],
                    client_ip=log['client_ip'],
                    success=log['success'],
                    request_data=json.dumps(log['request']),
                    response_data=json.dumps(log['response']),
                    error_message=log['error'] or ""
                )
                log_entries.append(entry)
            
            print(f"📊 QueryLogs: Found {len(log_entries)} logs")
            return warehouse_pb2.QueryLogsResponse(
                logs=log_entries,
                total_count=len(filtered_logs)
            )
            
        except Exception as e:
            print(f"❌ [ERROR] LoggerService QueryLogs error: {e}")
            return warehouse_pb2.QueryLogsResponse(
                logs=[],
                total_count=0
            )
    
    def GetStats(self, request, context):
        """获取统计信息"""
        try:
            with self.lock:
                total_operations = len(self.logs)
                successful_operations = sum(1 for log in self.logs if log['success'])
                failed_operations = total_operations - successful_operations
                success_rate = (successful_operations / total_operations * 100) if total_operations > 0 else 0
                
                # 按服务统计
                service_stats = {}
                for log in self.logs:
                    service = log['service']
                    if service not in service_stats:
                        service_stats[service] = {'total': 0, 'success': 0, 'failed': 0}
                    service_stats[service]['total'] += 1
                    if log['success']:
                        service_stats[service]['success'] += 1
                    else:
                        service_stats[service]['failed'] += 1
                
                # 按操作统计
                operation_stats = {}
                for log in self.logs:
                    operation = log['operation']
                    if operation not in operation_stats:
                        operation_stats[operation] = {'total': 0, 'success': 0, 'failed': 0}
                    operation_stats[operation]['total'] += 1
                    if log['success']:
                        operation_stats[operation]['success'] += 1
                    else:
                        operation_stats[operation]['failed'] += 1
                
                # 转换为 protobuf 格式
                service_stats_pb = []
                for service, data in service_stats.items():
                    service_success_rate = (data['success'] / data['total'] * 100) if data['total'] > 0 else 0
                    service_stats_pb.append(warehouse_pb2.ServiceStats(
                        service_name=service,
                        total=data['total'],
                        success=data['success'],
                        failed=data['failed'],
                        success_rate=service_success_rate
                    ))
                
                operation_stats_pb = []
                for operation, data in operation_stats.items():
                    operation_success_rate = (data['success'] / data['total'] * 100) if data['total'] > 0 else 0
                    operation_stats_pb.append(warehouse_pb2.OperationStats(
                        operation=operation,
                        total=data['total'],
                        success=data['success'],
                        failed=data['failed'],
                        success_rate=operation_success_rate
                    ))
                
                print(f"📈 GetStats: {total_operations} total operations, {success_rate:.1f}% success rate")
                return warehouse_pb2.StatsResponse(
                    total_operations=total_operations,
                    successful_operations=successful_operations,
                    failed_operations=failed_operations,
                    success_rate=success_rate,
                    service_stats=service_stats_pb,
                    operation_stats=operation_stats_pb
                )
                
        except Exception as e:
            print(f"❌ [ERROR] LoggerService GetStats error: {e}")
            return warehouse_pb2.StatsResponse(
                total_operations=0,
                successful_operations=0,
                failed_operations=0,
                success_rate=0.0,
                service_stats=[],
                operation_stats=[]
            )


def run_logger_service(port=50055):
    """运行LoggerService"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_LoggerServiceServicer_to_server(LoggerService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print(f"📊 LoggerService started on port {port}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping LoggerService...")
        server.stop(0)


if __name__ == "__main__":
    run_logger_service()
