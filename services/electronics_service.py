#!/usr/bin/env python3
"""
ElectronicsService - 中层服务
处理电子产品相关的请求，转发给ApplianceService
端口: 50051
"""

import grpc
import time
import signal
import sys
from concurrent import futures

import warehouse_pb2
import warehouse_pb2_grpc
from logger_client import logger_client
from warehouse_logger import get_logger


class ElectronicsService(warehouse_pb2_grpc.OrderServiceServicer):
    """
    ElectronicsService - 电子产品服务
    处理电子产品类别的请求，转发给ApplianceService
    """
    
    def __init__(self, appliance_service_host='appliance-service', appliance_service_port=50054):
        """Initialize ElectronicsService"""
        self.logger = get_logger('ElectronicsService')
        self.appliance_service_channel = grpc.insecure_channel(f'{appliance_service_host}:{appliance_service_port}')
        self.appliance_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.appliance_service_channel)
        self.logging_enabled = True  # Enable logging by default
        self.logger.print_success("ElectronicsService initialized")
    
    def PlaceOrder(self, request, context):
        """处理下单请求 - 转发给ApplianceService"""
        try:
            self.logger.print_debug("PlaceOrder request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}, Item: {request.item}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            self.logger.print_debug("Forwarding to ApplianceService")
            
            # Forward to ApplianceService
            response = self.appliance_service_stub.PlaceOrder(request)
            
            self.logger.print_debug(f"Response from ApplianceService: status={response.status}, left={response.left}")
            self.logger.print_debug("PlaceOrder completed successfully")
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"ElectronicsService PlaceOrder gRPC error: {e}")
            self.logger.print_debug(f"Sending Service unavailable response")
            response = warehouse_pb2.OrderResponse(
                status="service unavailable",
                left=0
            )
            self.logger.print_debug(f"Response: status={response.status}, left={response.left}")
            
            return response
        except Exception as e:
            self.logger.print_debug(f" ElectronicsService PlaceOrder error: {e}")
            self.logger.print_debug(f"Sending Error response")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            self.logger.print_debug(f"Response: status={response.status}, left={response.left}")
            
            
            
            return response
    
    def PutItem(self, request, context):
        """放入货物 - 转发给ApplianceService"""
        try:
            self.logger.print_debug(f"📱 [RECEIVED] ElectronicsService - PutItem Request:")
            self.logger.print_debug(f"   📥 Category: {request.category}")
            self.logger.print_debug(f"   📥 Subcategory: {request.subcategory}")
            self.logger.print_debug(f"   📥 Item: {request.item}")
            self.logger.print_debug(f"   📥 Client IP: {context.peer()}")
            self.logger.print_debug(f"   🔄 [FORWARDING] Sending to ApplianceService...")
            
            # Forward to ApplianceService
            response = self.appliance_service_stub.PutItem(request)
            
            self.logger.print_debug(f"   📨 [RECEIVED] Response from ApplianceService:")
            self.logger.print_debug(f"   📨 Success: {response.success}")
            self.logger.print_debug(f"   📨 Message: {response.message}")
            self.logger.print_debug(f"   ✅ [SENDING] Forwarding response to client")
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"ElectronicsService PutItem gRPC error: {e}")
            self.logger.print_debug(f"Sending Service unavailable response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message="Service unavailable"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            return response
        except Exception as e:
            self.logger.print_debug(f" ElectronicsService PutItem error: {e}")
            self.logger.print_debug(f"Sending Error response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            return response
    
    def UpdateItem(self, request, context):
        """更新货物 - 转发给ApplianceService"""
        try:
            self.logger.print_debug(f"📱 [RECEIVED] ElectronicsService - UpdateItem Request:")
            self.logger.print_debug(f"   📥 Category: {request.category}")
            self.logger.print_debug(f"   📥 Subcategory: {request.subcategory}")
            self.logger.print_debug(f"   📥 Item: {request.item}")
            self.logger.print_debug(f"   📥 Client IP: {context.peer()}")
            self.logger.print_debug(f"   🔄 [FORWARDING] Sending to ApplianceService...")
            
            # Forward to ApplianceService
            response = self.appliance_service_stub.UpdateItem(request)
            
            self.logger.print_debug(f"   📨 [RECEIVED] Response from ApplianceService:")
            self.logger.print_debug(f"   📨 Success: {response.success}")
            self.logger.print_debug(f"   📨 Message: {response.message}")
            self.logger.print_debug(f"   ✅ [SENDING] Forwarding response to client")
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"ElectronicsService UpdateItem gRPC error: {e}")
            self.logger.print_debug(f"Sending Service unavailable response")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message="Service unavailable"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            return response
        except Exception as e:
            self.logger.print_debug(f" ElectronicsService UpdateItem error: {e}")
            self.logger.print_debug(f"Sending Error response")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库 - 转发给ApplianceService"""
        try:
            self.logger.print_debug(f"📱 [RECEIVED] ElectronicsService - ListItems Request:")
            self.logger.print_debug(f"   📥 Category: {request.category}")
            self.logger.print_debug(f"   📥 Subcategory: {request.subcategory}")
            self.logger.print_debug(f"   📥 Client IP: {context.peer()}")
            self.logger.print_debug(f"   🔄 [FORWARDING] Sending to ApplianceService...")
            
            # Forward to ApplianceService
            response = self.appliance_service_stub.ListItems(request)
            
            self.logger.print_debug(f"   📨 [RECEIVED] Response from ApplianceService:")
            self.logger.print_debug(f"   📨 Items count: {len(response.items)}")
            for i, item in enumerate(response.items):
                self.logger.print_debug(f"   📨 Item {i+1}: {item}")
            self.logger.print_debug(f"   ✅ [SENDING] Forwarding response to client")
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"ElectronicsService ListItems gRPC error: {e}")
            self.logger.print_debug(f"Sending Empty response due to service unavailable")
            response = warehouse_pb2.ListItemsResponse(items=[])
            self.logger.print_debug(f"Response: {len(response.items)} items")
            
            return response
        except Exception as e:
            self.logger.print_debug(f" ElectronicsService ListItems error: {e}")
            self.logger.print_debug(f"Sending Empty response due to error")
            response = warehouse_pb2.ListItemsResponse(items=[])
            self.logger.print_debug(f"Response: {len(response.items)} items")
            
            return response
    
    def ConfigureLogging(self, request, context):
        """配置日志记录状态"""
        try:
            self.logging_enabled = request.enable_logging
            status = "enabled" if self.logging_enabled else "disabled"
            self.logger.print_info(f"Logging has been {status}")
            
            return warehouse_pb2.ConfigureLoggingResponse(
                success=True,
                message=f"Logging has been {status}"
            )
        except Exception as e:
            self.logger.print_error(f"Failed to configure logging: {e}")
            return warehouse_pb2.ConfigureLoggingResponse(
                success=False,
                message=f"Configuration failed: {str(e)}"
            )
    
    def close(self):
        """关闭连接"""
        if self.appliance_service_channel:
            self.appliance_service_channel.close()


def run_electronics_service(port=50051):
    """运行ElectronicsService"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    electronics_service = ElectronicsService()
    warehouse_pb2_grpc.add_OrderServiceServicer_to_server(electronics_service, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger = get_logger('ElectronicsServiceMain')
    logger.print_success(f"ElectronicsService started on port {port}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.print_info("Stopping ElectronicsService...")
        electronics_service.close()
        server.stop(0)


if __name__ == "__main__":
    run_electronics_service()
