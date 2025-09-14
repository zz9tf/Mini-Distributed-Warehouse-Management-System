#!/usr/bin/env python3
"""
API Gateway - 顶层服务
根据请求类别路由到相应的服务
端口: 50050
"""

import grpc
import time
import signal
import sys
from concurrent import futures

import warehouse_pb2
import warehouse_pb2_grpc


class APIGateway(warehouse_pb2_grpc.OrderServiceServicer):
    """
    API Gateway - 顶层网关服务
    根据请求类别路由到相应的服务
    """
    
    def __init__(self, 
                 food_service_host='food-service', food_service_port=50052,
                 electronics_service_host='electronics-service', electronics_service_port=50051):
        """Initialize API Gateway"""
        # 连接中层服务
        self.food_service_channel = grpc.insecure_channel(f'{food_service_host}:{food_service_port}')
        self.food_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.food_service_channel)
        
        self.electronics_service_channel = grpc.insecure_channel(f'{electronics_service_host}:{electronics_service_port}')
        self.electronics_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.electronics_service_channel)
        
        print("🌐 API Gateway initialized")
        print("   📍 FoodService: food-service:50052")
        print("   📍 ElectronicsService: electronics-service:50051")
    
    def _route_request(self, request):
        """根据请求类别路由到相应服务"""
        category = request.category.lower()
        
        if category in ['food', 'fruits', 'vegetables', 'fresh']:
            return self.food_service_stub
        elif category in ['electronics', 'appliance', 'kitchen', 'living']:
            return self.electronics_service_stub
        else:
            # 默认路由到ElectronicsService
            return self.electronics_service_stub
    
    def PlaceOrder(self, request, context):
        """处理下单请求 - 路由到相应服务"""
        try:
            print(f"🌐 [RECEIVED] API Gateway - PlaceOrder Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            print(f"   🎯 [ROUTING] Selected service: {service_name}")
            print(f"   🔄 [FORWARDING] Sending to {service_name}...")
            
            response = target_service.PlaceOrder(request)
            
            print(f"   📨 [RECEIVED] Response from {service_name}:")
            print(f"   📨 Status: {response.status}")
            print(f"   📨 Left in stock: {response.left}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] API Gateway PlaceOrder gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.OrderResponse(
                status="service unavailable",
                left=0
            )
            print(f"   📤 Response: status={response.status}, left={response.left}")
            return response
        except Exception as e:
            print(f"❌ [ERROR] API Gateway PlaceOrder error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            print(f"   📤 Response: status={response.status}, left={response.left}")
            return response
    
    def PutItem(self, request, context):
        """放入货物 - 路由到相应服务"""
        try:
            print(f"🌐 [RECEIVED] API Gateway - PutItem Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            print(f"   🎯 [ROUTING] Selected service: {service_name}")
            print(f"   🔄 [FORWARDING] Sending to {service_name}...")
            
            response = target_service.PutItem(request)
            
            print(f"   📨 [RECEIVED] Response from {service_name}:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] API Gateway PutItem gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message="Service unavailable"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
        except Exception as e:
            print(f"❌ [ERROR] API Gateway PutItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
    
    def GetItem(self, request, context):
        """取出货物 - 路由到相应服务"""
        try:
            print(f"🌐 [RECEIVED] API Gateway - GetItem Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Item: {request.item}")
            print(f"   📥 Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            print(f"   🎯 [ROUTING] Selected service: {service_name}")
            print(f"   🔄 [FORWARDING] Sending to {service_name}...")
            
            response = target_service.GetItem(request)
            
            print(f"   📨 [RECEIVED] Response from {service_name}:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] API Gateway GetItem gRPC error: {e}")
            print(f"   📤 [SENDING] Service unavailable response")
            response = warehouse_pb2.GetItemResponse(
                success=False,
                message="Service unavailable"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
        except Exception as e:
            print(f"❌ [ERROR] API Gateway GetItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.GetItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库 - 路由到相应服务"""
        try:
            print(f"🌐 [RECEIVED] API Gateway - ListItems Request:")
            print(f"   📥 Category: {request.category}")
            print(f"   📥 Subcategory: {request.subcategory}")
            print(f"   📥 Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            print(f"   🎯 [ROUTING] Selected service: {service_name}")
            print(f"   🔄 [FORWARDING] Sending to {service_name}...")
            
            response = target_service.ListItems(request)
            
            print(f"   📨 [RECEIVED] Response from {service_name}:")
            print(f"   📨 Items count: {len(response.items)}")
            for i, item in enumerate(response.items):
                print(f"   📨 Item {i+1}: {item}")
            print(f"   ✅ [SENDING] Forwarding response to client")
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] API Gateway ListItems gRPC error: {e}")
            print(f"   📤 [SENDING] Empty response due to service unavailable")
            response = warehouse_pb2.ListItemsResponse(items=[])
            print(f"   📤 Response: {len(response.items)} items")
            return response
        except Exception as e:
            print(f"❌ [ERROR] API Gateway ListItems error: {e}")
            print(f"   📤 [SENDING] Empty response due to error")
            response = warehouse_pb2.ListItemsResponse(items=[])
            print(f"   📤 Response: {len(response.items)} items")
            return response
    
    def close(self):
        """关闭连接"""
        if self.food_service_channel:
            self.food_service_channel.close()
        if self.electronics_service_channel:
            self.electronics_service_channel.close()


def run_api_gateway(port=50050):
    """运行API Gateway"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_gateway = APIGateway()
    warehouse_pb2_grpc.add_OrderServiceServicer_to_server(api_gateway, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print(f"🌐 API Gateway started on port {port}")
    print("🎯 Ready to accept client requests")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping API Gateway...")
        api_gateway.close()
        server.stop(0)


if __name__ == "__main__":
    run_api_gateway()
