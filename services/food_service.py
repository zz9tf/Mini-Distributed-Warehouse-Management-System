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
from logger_client import logger_client
from warehouse_logger import get_logger


class FoodService(warehouse_pb2_grpc.OrderServiceServicer):
    """
    FoodService - 食品服务
    处理食品类别的请求，转发给FreshService
    """
    
    def __init__(self, fresh_service_host='fresh-service', fresh_service_port=50053):
        """Initialize FoodService"""
        self.logger = get_logger('FoodService')
        self.fresh_service_channel = grpc.insecure_channel(f'{fresh_service_host}:{fresh_service_port}')
        self.fresh_service_stub = warehouse_pb2_grpc.OrderServiceStub(self.fresh_service_channel)
        self.logger.print_success("FoodService initialized")
    
    def PlaceOrder(self, request, context):
        """处理下单请求 - 转发给FreshService"""
        try:
            self.logger.print_debug("PlaceOrder request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}, Item: {request.item}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            self.logger.print_debug("Forwarding to FreshService")
            
            # 转发给FreshService
            response = self.fresh_service_stub.PlaceOrder(request)
            
            self.logger.print_debug(f"Response from FreshService: status={response.status}, left={response.left}")
            self.logger.print_debug("PlaceOrder completed successfully")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="PlaceOrder",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"status": response.status, "left": response.left},
                client_ip=context.peer(),
                success=True
            )
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"PlaceOrder gRPC error: {e}")
            response = warehouse_pb2.OrderResponse(
                status="service unavailable",
                left=0
            )
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="PlaceOrder",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"status": response.status, "left": response.left},
                client_ip=context.peer(),
                success=False,
                error_message=f"gRPC error: {str(e)}"
            )
            
            return response
        except Exception as e:
            self.logger.print_debug(f"PlaceOrder error: {e}")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="PlaceOrder",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"status": response.status, "left": response.left},
                client_ip=context.peer(),
                success=False,
                error_message=f"Error: {str(e)}"
            )
            
            return response
    
    def PutItem(self, request, context):
        """放入货物 - 转发给FreshService"""
        try:
            self.logger.print_debug("PutItem request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}, Item: {request.item}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            self.logger.print_debug("Forwarding to FreshService")
            
            # 转发给FreshService
            response = self.fresh_service_stub.PutItem(request)
            
            self.logger.print_debug(f"Response from FreshService: success={response.success}, message={response.message}")
            self.logger.print_debug("PutItem completed successfully")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="PutItem",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=response.success
            )
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"PutItem gRPC error: {e}")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message="Service unavailable"
            )
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="PutItem",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=f"gRPC error: {str(e)}"
            )
            
            return response
        except Exception as e:
            self.logger.print_debug(f"PutItem error: {e}")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="PutItem",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=f"Error: {str(e)}"
            )
            
            return response
    
    def UpdateItem(self, request, context):
        """更新货物 - 转发给FreshService"""
        try:
            self.logger.print_debug("UpdateItem request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}, Item: {request.item}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            self.logger.print_debug("Forwarding to FreshService")
            
            # 转发给FreshService
            response = self.fresh_service_stub.UpdateItem(request)
            
            self.logger.print_debug(f"Response from FreshService: success={response.success}, message={response.message}")
            self.logger.print_debug("UpdateItem completed successfully")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="UpdateItem",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=response.success
            )
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"UpdateItem gRPC error: {e}")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message="Service unavailable"
            )
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="UpdateItem",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=f"gRPC error: {str(e)}"
            )
            
            return response
        except Exception as e:
            self.logger.print_debug(f"UpdateItem error: {e}")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="UpdateItem",
                request_data={"category": request.category, "subcategory": request.subcategory, "item": request.item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=f"Error: {str(e)}"
            )
            
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库 - 转发给FreshService"""
        try:
            self.logger.print_debug("ListItems request received")
            self.logger.print_debug(f"Category: {request.category}, Subcategory: {request.subcategory}")
            self.logger.print_debug(f"Client IP: {context.peer()}")
            self.logger.print_debug("Forwarding to FreshService")
            
            # 转发给FreshService
            response = self.fresh_service_stub.ListItems(request)
            
            self.logger.print_debug(f"Response from FreshService: {len(response.items)} items")
            for i, item in enumerate(response.items):
                self.logger.print_debug(f"Item {i+1}: {item}")
            self.logger.print_debug("ListItems completed successfully")
            
            # 记录操作日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="ListItems",
                request_data={"category": request.category, "subcategory": request.subcategory},
                response_data={"items_count": len(response.items), "items": [{"name": item.name, "count": item.count} for item in response.items]},
                client_ip=context.peer(),
                success=True
            )
            
            return response
            
        except grpc.RpcError as e:
            self.logger.print_debug(f"FoodService ListItems gRPC error: {e}")
            self.logger.print_debug("Sending empty response due to service unavailable")
            response = warehouse_pb2.ListItemsResponse(items=[])
            self.logger.print_debug(f"Response: {len(response.items)} items")
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="ListItems",
                request_data={"category": request.category, "subcategory": request.subcategory},
                response_data={"items_count": 0, "items": []},
                client_ip=context.peer(),
                success=False,
                error_message=f"gRPC error: {str(e)}"
            )
            
            return response
        except Exception as e:
            self.logger.print_debug(f"FoodService ListItems error: {e}")
            self.logger.print_debug("Sending empty response due to error")
            response = warehouse_pb2.ListItemsResponse(items=[])
            self.logger.print_debug(f"Response: {len(response.items)} items")
            
            # 记录错误日志
            logger_client.log_operation(
                service_name="FoodService",
                operation="ListItems",
                request_data={"category": request.category, "subcategory": request.subcategory},
                response_data={"items_count": 0, "items": []},
                client_ip=context.peer(),
                success=False,
                error_message=f"Error: {str(e)}"
            )
            
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
    
    logger = get_logger('FoodServiceMain')
    logger.print_success(f"FoodService started on port {port}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logger.print_info("Stopping FoodService...")
        food_service.close()
        server.stop(0)


if __name__ == "__main__":
    run_food_service()
