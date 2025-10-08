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
from warehouse_logger import get_logger


class APIGateway(warehouse_pb2_grpc.OrderServiceServicer):
    """
    API Gateway - 顶层网关服务
    根据请求类别路由到相应的服务
    """
    
    def __init__(self, 
                 food_service_host='food-service', food_service_port=50052,
                 electronics_service_host='electronics-service', electronics_service_port=50051):
        """Initialize API Gateway"""
        self.logger = get_logger('APIGateway')
        
        # 连接中层服务
        self.food_service_channel = grpc.insecure_channel(f'{food_service_host}:{food_service_port}')
        self.food_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.food_service_channel)
        
        self.electronics_service_channel = grpc.insecure_channel(f'{electronics_service_host}:{electronics_service_port}')
        self.electronics_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.electronics_service_channel)
        
        self.logger.print_success("API Gateway initialized")
        self.logger.print_info(f"FoodService: {food_service_host}:{food_service_port}")
        self.logger.print_info(f"ElectronicsService: {electronics_service_host}:{electronics_service_port}")
    
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
            self.logger.print_debug("PlaceOrder request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}, Item: {request.item}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            self.logger.print_debug(f"Routing to {service_name}")
            
            response = target_service.PlaceOrder(request)
            
            self.logger.print_debug(f"Response from {service_name}: status={response.status}, left={response.left}")
            self.logger.print_debug("PlaceOrder completed successfully")
            return response
            
        except grpc.RpcError as e:
            self.logger.print_error(f"PlaceOrder gRPC error: {e}")
            response = warehouse_pb2.OrderResponse(
                status="service unavailable",
                left=0
            )
            return response
        except Exception as e:
            self.logger.print_error(f"PlaceOrder error: {e}")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            return response
    
    def PutItem(self, request, context):
        """放入货物 - 路由到相应服务"""
        try:
            self.logger.print_debug("PutItem request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}, Item: {request.item}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            self.logger.print_debug(f"Routing to {service_name}")
            
            response = target_service.PutItem(request)
            
            self.logger.print_debug(f"Response from {service_name}: success={response.success}, message={response.message}")
            self.logger.print_debug("PutItem completed successfully")
            return response
            
        except grpc.RpcError as e:
            self.logger.print_error(f"PutItem gRPC error: {e}")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message="Service unavailable"
            )
            return response
        except Exception as e:
            self.logger.print_error(f"PutItem error: {e}")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            return response
    
    def UpdateItem(self, request, context):
        """更新货物 - 路由到相应服务"""
        try:
            self.logger.print_debug("UpdateItem request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}, Item: {request.item}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            self.logger.print_debug(f"Routing to {service_name}")
            
            response = target_service.UpdateItem(request)
            
            self.logger.print_debug(f"Response from {service_name}: success={response.success}, message={response.message}")
            self.logger.print_debug("UpdateItem completed successfully")
            return response
            
        except grpc.RpcError as e:
            self.logger.print_error(f"UpdateItem gRPC error: {e}")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message="Service unavailable"
            )
            return response
        except Exception as e:
            self.logger.print_error(f"UpdateItem error: {e}")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库 - 路由到相应服务"""
        try:
            self.logger.print_debug("ListItems request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            
            # 路由到相应服务
            target_service = self._route_request(request)
            service_name = "FoodService" if target_service == self.food_service_stub else "ElectronicsService"
            self.logger.print_debug(f"Routing to {service_name}")
            
            response = target_service.ListItems(request)
            
            self.logger.print_debug(f"Response from {service_name}: {len(response.items)} items")
            for i, item in enumerate(response.items):
                self.logger.print_debug(f"Item {i+1}: {item}")
            self.logger.print_debug("ListItems completed successfully")
            return response
            
        except grpc.RpcError as e:
            self.logger.print_error(f"ListItems gRPC error: {e}")
            response = warehouse_pb2.ListItemsResponse(items=[])
            return response
        except Exception as e:
            self.logger.print_error(f"ListItems error: {e}")
            response = warehouse_pb2.ListItemsResponse(items=[])
            return response
    
    def close(self):
        """关闭连接"""
        if self.food_service_channel:
            self.food_service_channel.close()
        if self.electronics_service_channel:
            self.electronics_service_channel.close()


def run_api_gateway(port=50050):
    """运行API Gateway"""
    logger = get_logger('APIGateway')
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    api_gateway = APIGateway()
    warehouse_pb2_grpc.add_OrderServiceServicer_to_server(api_gateway, server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger.print_success(f"API Gateway started on port {port}")
    logger.print_info("Ready to accept client requests")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.print_warning("Stopping API Gateway...")
        api_gateway.close()
        server.stop(0)


if __name__ == "__main__":
    run_api_gateway()
