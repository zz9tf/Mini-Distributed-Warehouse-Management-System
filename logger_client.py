#!/usr/bin/env python3
"""
LoggerClient - 日志客户端
供其他服务调用来记录日志
"""

import grpc
import json
from typing import Dict, Any, Optional

import warehouse_pb2
import warehouse_pb2_grpc


class LoggerClient:
    """
    日志客户端
    供其他服务调用来记录日志
    """
    
    def __init__(self, host='logger-service', port=50055):
        """
        初始化日志客户端
        
        Args:
            host: 日志服务主机
            port: 日志服务端口
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self._connect()
    
    def _connect(self):
        """连接到日志服务"""
        try:
            self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
            self.stub = warehouse_pb2_grpc.LoggerServiceStub(self.channel)
            print(f"📊 Connected to LoggerService at {self.host}:{self.port}")
        except Exception as e:
            print(f"❌ Failed to connect to LoggerService: {e}")
            self.channel = None
            self.stub = None
    
    def log_operation(self, 
                     service_name: str, 
                     operation: str, 
                     request_data: Dict[str, Any], 
                     response_data: Dict[str, Any], 
                     client_ip: str = "unknown",
                     success: bool = True,
                     error_message: Optional[str] = None):
        """
        记录操作日志
        
        Args:
            service_name: 服务名称
            operation: 操作类型
            request_data: 请求数据
            response_data: 响应数据
            client_ip: 客户端IP
            success: 操作是否成功
            error_message: 错误信息（如果有）
        """
        if not self.stub:
            print("❌ LoggerService not available, skipping log")
            return
        
        try:
            request = warehouse_pb2.LogRequest(
                service_name=service_name,
                operation=operation,
                client_ip=client_ip,
                success=success,
                request_data=json.dumps(request_data),
                response_data=json.dumps(response_data),
                error_message=error_message or ""
            )
            
            response = self.stub.LogOperation(request)
            if not response.success:
                print(f"❌ Failed to log operation: {response.message}")
                
        except Exception as e:
            print(f"❌ Error logging operation: {e}")
    
    def query_logs(self, service_name: str = "", operation: str = "", limit: int = 50):
        """
        查询日志
        
        Args:
            service_name: 服务名称过滤（可选）
            operation: 操作类型过滤（可选）
            limit: 返回记录数量限制
            
        Returns:
            日志列表
        """
        if not self.stub:
            print("❌ LoggerService not available")
            return []
        
        try:
            request = warehouse_pb2.QueryLogsRequest(
                service_name=service_name,
                operation=operation,
                limit=limit
            )
            
            response = self.stub.QueryLogs(request)
            return response.logs
            
        except Exception as e:
            print(f"❌ Error querying logs: {e}")
            return []
    
    def get_stats(self):
        """
        获取统计信息
        
        Returns:
            统计信息字典
        """
        if not self.stub:
            print("❌ LoggerService not available")
            return None
        
        try:
            request = warehouse_pb2.StatsRequest()
            response = self.stub.GetStats(request)
            
            return {
                'total_operations': response.total_operations,
                'successful_operations': response.successful_operations,
                'failed_operations': response.failed_operations,
                'success_rate': response.success_rate,
                'service_stats': [
                    {
                        'service_name': stat.service_name,
                        'total': stat.total,
                        'success': stat.success,
                        'failed': stat.failed,
                        'success_rate': stat.success_rate
                    } for stat in response.service_stats
                ],
                'operation_stats': [
                    {
                        'operation': stat.operation,
                        'total': stat.total,
                        'success': stat.success,
                        'failed': stat.failed,
                        'success_rate': stat.success_rate
                    } for stat in response.operation_stats
                ]
            }
            
        except Exception as e:
            print(f"❌ Error getting stats: {e}")
            return None
    
    def close(self):
        """关闭连接"""
        if self.channel:
            self.channel.close()


# 全局日志客户端实例
logger_client = LoggerClient()
