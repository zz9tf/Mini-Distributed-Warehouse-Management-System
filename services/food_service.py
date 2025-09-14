#!/usr/bin/env python3
"""
FoodService - 中层服务
处理食品相关的请求，转发给FreshService
端口: 50052
"""

import grpc
import time
import signal
import sys
from concurrent import futures

import warehouse_pb2
import warehouse_pb2_grpc


class FoodService(warehouse_pb2_grpc.OrderServiceServicer):
    """
    FoodService - 食品服务
    处理食品类别的请求，转发给FreshService
    """
    
    def __init__(self, fresh_service_host='fresh-service', fresh_service_port=50053):
        """Initialize FoodService"""
        self.fresh_service_channel = grpc.insecure_channel(f'{fresh_service_host}:{fresh_service_port}')
        self.fresh_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.fresh_service_channel)
        print("🍎 FoodService initialized")
    
    def PlaceOrder(self, request, context):
        """处理下单请求 - 转发给FreshService"""
        try:
            print(f"🍎 [RECEIVED] FoodService - PlaceOrder Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to FreshService...")
            
            # 转发给FreshService
            response = self.fresh_service_stub.PlaceOrder(request)
            
            print(f"   📨 [RECEIVED] Response from FreshService:")
            print(f"   📨 Status: {response.status}")
            print(f"   📨 Left in stock: {response.left}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] FoodService PlaceOrder gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.OrderResponse(
                status="service unavailable",
                left=0
            )
            print(f"   📤 Response: status={response.status}, left={response.left}")
            return response
        except Exception as e:
            print(f"❌ [ERROR] FoodService PlaceOrder error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            print(f"   📤 Response: status={response.status}, left={response.left}")
            return response
    
    def PutItem(self, request, context):
        """放入货物 - 转发给FreshService"""
        try:
            print(f"🍎 [RECEIVED] FoodService - PutItem Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to FreshService...")
            
            # 转发给FreshService
            response = self.fresh_service_stub.PutItem(request)
            
            print(f"   📨 [RECEIVED] Response from FreshService:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] FoodService PutItem gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message="Service unavailable"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
        except Exception as e:
            print(f"❌ [ERROR] FoodService PutItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
    
    def UpdateItem(self, request, context):
        """更新货物 - 转发给FreshService"""
        try:
            print(f"🍎 [RECEIVED] FoodService - UpdateItem Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to FreshService...")
            
            # 转发给FreshService
            response = self.fresh_service_stub.UpdateItem(request)
            
            print(f"   📨 [RECEIVED] Response from FreshService:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] FoodService UpdateItem gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message="Service unavailable"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
        except Exception as e:
            print(f"❌ [ERROR] FoodService UpdateItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库 - 转发给FreshService"""
        try:
            print(f"🍎 [RECEIVED] FoodService - ListItems Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Client IP: {context.peer()}")
            print(f"   🔄 [FORWARDING] Sending to FreshService...")
            
            # 转发给FreshService
            response = self.fresh_service_stub.ListItems(request)
            
            print(f"   📨 [RECEIVED] Response from FreshService:")
            print(f"   📨 Items count: {len(response.items)}")
            for i, item in enumerate(response.items):
                print(f"   📨 Item {i+1}: {item}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] FoodService ListItems gRPC error: {e}")
            print(f"   📤 [SENDING] Empty response due to service unavailable")
            response = warehouse_pb2.ListItemsResponse(items=[])
            print(f"   📤 Response: {len(response.items)} items")
            return response
        except Exception as e:
            print(f"❌ [ERROR] FoodService ListItems error: {e}")
            print(f"   📤 [SENDING] Empty response due to error")
            response = warehouse_pb2.ListItemsResponse(items=[])
            print(f"   📤 Response: {len(response.items)} items")
            return response
    
    def close(self):
        """关闭连接"""
        if self.fresh_service_channel:
            self.fresh_service_channel.close()


def run_food_service(port=50052):
    """运行FoodService"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    food_service = FoodService()
    warehouse_pb2_grpc.add_OrderServiceServicer_to_server(food_service, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print(f"🍎 FoodService started on port {port}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping FoodService...")
        food_service.close()
        server.stop(0)


if __name__ == "__main__":
    run_food_service()
