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


class ElectronicsService(warehouse_pb2_grpc.OrderServiceServicer):
    """
    ElectronicsService - 电子产品服务
    处理电子产品类别的请求，转发给ApplianceService
    """
    
    def __init__(self, appliance_service_host='appliance-service', appliance_service_port=50054):
        """Initialize ElectronicsService"""
        self.appliance_service_channel = grpc.insecure_channel(f'{appliance_service_host}:{appliance_service_port}')
        self.appliance_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.appliance_service_channel)
        print("📱 ElectronicsService initialized")
    
    def PlaceOrder(self, request, context):
        """处理下单请求 - 转发给ApplianceService"""
        try:
            print(f"📱 [RECEIVED] ElectronicsService - PlaceOrder Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to ApplianceService...")
            
            # 转发给ApplianceService
            response = self.appliance_service_stub.PlaceOrder(request)
            
            print(f"   📨 [RECEIVED] Response from ApplianceService:")
            print(f"   📨 Status: {response.status}")
            print(f"   📨 Left in stock: {response.left}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="ElectronicsService",
                operation="PlaceOrder",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"status": response.status, "left": response.left},
                client_ip=context.peer(),
                success=True
            )
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] ElectronicsService PlaceOrder gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.OrderResponse(
                status="service unavailable",
                left=0
            )
            print(f"   📤 Response: status={response.status}, left={response.left}")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="ElectronicsService",
                operation="PlaceOrder",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', ''), "item": getattr(request, 'item', '')},
                response_data={"status": response.status, "left": response.left},
                client_ip=context.peer(),
                success=False,
                error_message=f"gRPC error: {str(e)}"
            )
            
            return response
        except Exception as e:
            print(f"❌ [ERROR] ElectronicsService PlaceOrder error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            print(f"   📤 Response: status={response.status}, left={response.left}")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="ElectronicsService",
                operation="PlaceOrder",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', ''), "item": getattr(request, 'item', '')},
                response_data={"status": response.status, "left": response.left},
                client_ip=context.peer(),
                success=False,
                error_message=str(e)
            )
            
            return response
    
    def PutItem(self, request, context):
        """放入货物 - 转发给ApplianceService"""
        try:
            print(f"📱 [RECEIVED] ElectronicsService - PutItem Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to ApplianceService...")
            
            # 转发给ApplianceService
            response = self.appliance_service_stub.PutItem(request)
            
            print(f"   📨 [RECEIVED] Response from ApplianceService:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="ElectronicsService",
                operation="PutItem",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=True
            )
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] ElectronicsService PutItem gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message="Service unavailable"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="ElectronicsService",
                operation="PutItem",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', ''), "item": getattr(request, 'item', '')},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=f"gRPC error: {str(e)}"
            )
            
            return response
        except Exception as e:
            print(f"❌ [ERROR] ElectronicsService PutItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="ElectronicsService",
                operation="PutItem",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', ''), "item": getattr(request, 'item', '')},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=str(e)
            )
            
            return response
    
    def UpdateItem(self, request, context):
        """更新货物 - 转发给ApplianceService"""
        try:
            print(f"📱 [RECEIVED] ElectronicsService - UpdateItem Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to ApplianceService...")
            
            # 转发给ApplianceService
            response = self.appliance_service_stub.UpdateItem(request)
            
            print(f"   📨 [RECEIVED] Response from ApplianceService:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] ElectronicsService UpdateItem gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message="Service unavailable"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
        except Exception as e:
            print(f"❌ [ERROR] ElectronicsService UpdateItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库 - 转发给ApplianceService"""
        try:
            print(f"📱 [RECEIVED] ElectronicsService - ListItems Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to ApplianceService...")
            
            # 转发给ApplianceService
            response = self.appliance_service_stub.ListItems(request)
            
            print(f"   📨 [RECEIVED] Response from ApplianceService:")
            print(f"   📨 Items count: {len(response.items)}")
            for i, item in enumerate(response.items):
                print(f"   📨 Item {i+1}: {item}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] ElectronicsService ListItems gRPC error: {e}")
            print(f"   📤 [SENDING] Empty response due to service unavailable")
            response = warehouse_pb2.ListItemsResponse(items=[])
            print(f"   📤 Response: {len(response.items)} items")
            return response
        except Exception as e:
            print(f"❌ [ERROR] ElectronicsService ListItems error: {e}")
            print(f"   📤 [SENDING] Empty response due to error")
            response = warehouse_pb2.ListItemsResponse(items=[])
            print(f"   📤 Response: {len(response.items)} items")
            return response
    
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
    
    print(f"📱 ElectronicsService started on port {port}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping ElectronicsService...")
        electronics_service.close()
        server.stop(0)


if __name__ == "__main__":
    run_electronics_service()
