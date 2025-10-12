#!/usr/bin/env python3
"""
FreshService - 底层服务
处理新鲜食品相关的库存管理
端口: 50053
"""

import grpc
import time
from concurrent import futures

import warehouse_pb2
import warehouse_pb2_grpc
from logger_client import logger_client
from warehouse_logger import get_logger


class FreshService(warehouse_pb2_grpc.OrderServiceServicer):
    """
    FreshService - 新鲜食品服务
    处理食品类别的库存管理
    """
    
    def __init__(self):
        """Initialize FreshService"""
        self.logger = get_logger('FreshService')
        self.inventory = {
            "fruits": {
                "apple": 50,
                "banana": 30,
                "orange": 25
            },
            "vegetables": {
                "carrot": 40,
                "tomato": 35,
                "lettuce": 20
            }
        }
        self.logging_enabled = True  # Enable logging by default
        self.logger.print_debug("🥬 FreshService initialized")
    
    def _log_operation(self, service_name, operation, request_data, response_data, client_ip, success=True, error_message=None):
        """条件日志记录方法"""
        if self.logging_enabled:
            logger_client.log_operation(
                service_name=service_name,
                operation=operation,
                request_data=request_data,
                response_data=response_data,
                client_ip=client_ip,
                success=success,
                error_message=error_message
            )
    
    def PlaceOrder(self, request, context):
        """处理下单请求"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            item = int(request.item)
            
            self.logger.print_debug(f"🥬 [RECEIVED] FreshService - PlaceOrder Request:")
            self.logger.print_debug(f"   📥 Category: {category}")
            self.logger.print_debug(f"   📥 Subcategory: {subcategory}")
            self.logger.print_debug(f"   📥 Item: {item}")
            self.logger.print_debug(f"   📥 Client IP: {context.peer()}")
            
            # Check inventory
            if (category in self.inventory and 
                subcategory in self.inventory[category]):
                
                current_stock = self.inventory[category][subcategory]
                self.logger.print_debug(f"   📊 Current stock: {current_stock}")
                
                if current_stock >= item:
                    # Decrease inventory
                    self.inventory[category][subcategory] -= item
                    new_stock = self.inventory[category][subcategory]
                    
                    self.logger.print_debug(f"   ✅ [SENDING] Order successful - Stock reduced to: {new_stock}")
                    response = warehouse_pb2.OrderResponse(
                        status="ok",
                        left=new_stock
                    )
                    self.logger.print_debug(f"Response: status={response.status}, left={response.left}")
                    
                    # Record operation log
                    self._log_operation(
                        service_name="FreshService",
                        operation="PlaceOrder",
                        request_data={"category": category, "subcategory": subcategory, "item": item},
                        response_data={"status": response.status, "left": response.left},
                        client_ip=context.peer(),
                        success=True
                    )
                    
                    return response
                else:
                    self.logger.print_debug(f"   ❌ [SENDING] Out of stock")
                    response = warehouse_pb2.OrderResponse(
                        status="out of stock",
                        left=item
                    )
                    self.logger.print_debug(f"Response: status={response.status}, left={response.left}")
                    
                    # Record operation log
                    self._log_operation(
                        service_name="FreshService",
                        operation="PlaceOrder",
                        request_data={"category": category, "subcategory": subcategory, "item": item},
                        response_data={"status": response.status, "left": response.left},
                        client_ip=context.peer(),
                        success=False,
                        error_message="Out of stock"
                    )
                    
                    return response
            else:
                self.logger.print_debug(f"   ❌ [SENDING] Item not found in inventory")
                response = warehouse_pb2.OrderResponse(
                    status="item not found",
                    left=0
                )
                self.logger.print_debug(f"Response: status={response.status}, left={response.left}")
                
                # Record operation log
                self._log_operation(
                    service_name="FreshService",
                    operation="PlaceOrder",
                    request_data={"category": category, "subcategory": subcategory, "item": item},
                    response_data={"status": response.status, "left": response.left},
                    client_ip=context.peer(),
                    success=False,
                    error_message="Item not found in inventory"
                )
                
                return response
                
        except Exception as e:
            self.logger.print_debug(f" FreshService PlaceOrder error: {e}")
            self.logger.print_debug(f"Sending Error response")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            self.logger.print_debug(f"Response: status={response.status}, left={response.left}")
            
            # Record operation log
            self._log_operation(
                service_name="FreshService",
                operation="PlaceOrder",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', ''), "item": getattr(request, 'item', '')},
                response_data={"status": response.status, "left": response.left},
                client_ip=context.peer(),
                success=False,
                error_message=str(e)
            )
            
            return response
    
    def PutItem(self, request, context):
        """放入货物"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            item = int(request.item)
            
            self.logger.print_debug(f"🥬 [RECEIVED] FreshService - PutItem Request:")
            self.logger.print_debug(f"   📥 Category: {category}")
            self.logger.print_debug(f"   📥 Subcategory: {subcategory}")
            self.logger.print_debug(f"   📥 Item: {item}")
            self.logger.print_debug(f"   📥 Client IP: {context.peer()}")
            
            if category not in self.inventory:
                self.inventory[category] = {}
                self.logger.print_debug(f"   📝 Created new category: {category}")
            if subcategory not in self.inventory[category]:
                self.inventory[category][subcategory] = 0
                self.logger.print_debug(f"   📝 Created new subcategory: {subcategory}")
            
            old_count = self.inventory[category][subcategory]
            self.inventory[category][subcategory] += item
            self.logger.print_debug(f"   📈 Incremented existing {category}/{subcategory}: {old_count} → {self.inventory[category][subcategory]}")
            
            self.logger.print_debug(f"   ✅ [SENDING] PutItem successful")
            response = warehouse_pb2.PutItemResponse(
                success=True,
                message=f"Added {item} to {category}/{subcategory}, now {self.inventory[category][subcategory]}"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            # Record operation log
            self._log_operation(
                service_name="FreshService",
                operation="PutItem",
                request_data={"category": category, "subcategory": subcategory, "item": item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=True
            )
            
            return response
            
        except Exception as e:
            self.logger.print_debug(f" FreshService PutItem error: {e}")
            self.logger.print_debug(f"Sending Error response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            # Record operation log
            self._log_operation(
                service_name="FreshService",
                operation="PutItem",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', ''), "item": getattr(request, 'item', '')},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=str(e)
            )
            
            return response
    
    def UpdateItem(self, request, context):
        """更新货物"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            item = int(request.item)
            
            self.logger.print_debug(f"🥬 [RECEIVED] FreshService - UpdateItem Request:")
            self.logger.print_debug(f"   📥 Category: {category}")
            self.logger.print_debug(f"   📥 Subcategory: {subcategory}")
            self.logger.print_debug(f"   📥 Item: {item}")
            self.logger.print_debug(f"   📥 Client IP: {context.peer()}")
            
            if category not in self.inventory:
                self.inventory[category] = {}
                self.logger.print_debug(f"   📝 Created new category: {category}")
            if subcategory not in self.inventory[category]:
                self.inventory[category][subcategory] = 0
                self.logger.print_debug(f"   📝 Created new subcategory: {subcategory}")
            
            if item < 0:
                del self.inventory[category][subcategory]
                self.logger.print_debug(f"   📝 Deleted subcategory: {subcategory} as it is now empty")
            else:
                old_count = self.inventory[category][subcategory]
                self.inventory[category][subcategory] = item
                self.logger.print_debug(f"   📈 Updated {category}/{subcategory}: {old_count} → {item}")
            
            self.logger.print_debug(f"   ✅ [SENDING] UpdateItem successful")
            response = warehouse_pb2.UpdateItemResponse(
                success=True,
                message=f"Updated {category}/{subcategory} to {item}"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            # Record operation log
            self._log_operation(
                service_name="FreshService",
                operation="UpdateItem",
                request_data={"category": category, "subcategory": subcategory, "item": item},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=True
            )
            
            return response
            
        except Exception as e:
            self.logger.print_debug(f" FreshService UpdateItem error: {e}")
            self.logger.print_debug(f"Sending Error response")
            response = warehouse_pb2.UpdateItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            self.logger.print_debug(f"Response: success={response.success}, message={response.message}")
            
            # Record operation log
            self._log_operation(
                service_name="FreshService",
                operation="UpdateItem",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', ''), "item": getattr(request, 'item', '')},
                response_data={"success": response.success, "message": response.message},
                client_ip=context.peer(),
                success=False,
                error_message=str(e)
            )
            
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            
            self.logger.print_debug(f"🥬 [RECEIVED] FreshService - ListItems Request:")
            self.logger.print_debug(f"   📥 Category: {category}")
            self.logger.print_debug(f"   📥 Subcategory: {subcategory}")
            self.logger.print_debug(f"   📥 Client IP: {context.peer()}")
            
            items = []
            if (category in self.inventory and 
                subcategory in self.inventory[category]):
                items.append(str(self.inventory[category][subcategory]))
            
            self.logger.print_debug(f"   ✅ [SENDING] ListItems successful")
            response = warehouse_pb2.ListItemsResponse(items=items)
            self.logger.print_debug(f"Response: {len(response.items)} items")
            
            # Record operation log
            self._log_operation(
                service_name="FreshService",
                operation="ListItems",
                request_data={"category": category, "subcategory": subcategory},
                response_data={"items_count": len(response.items), "items": list(response.items)},
                client_ip=context.peer(),
                success=True
            )

            return response
            
        except Exception as e:
            self.logger.print_debug(f" FreshService ListItems error: {e}")
            self.logger.print_debug(f"Sending Error response")
            response = warehouse_pb2.ListItemsResponse(items=[])
            self.logger.print_debug(f"Response: {len(response.items)} items")
            
            # Record operation log
            self._log_operation(
                service_name="FreshService",
                operation="ListItems",
                request_data={"category": getattr(request, 'category', ''), "subcategory": getattr(request, 'subcategory', '')},
                response_data={"items_count": len(response.items), "items": list(response.items)},
                client_ip=context.peer(),
                success=False,
                error_message=str(e)
            )
            
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


def run_fresh_service(port=50053):
    """运行FreshService"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_OrderServiceServicer_to_server(FreshService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    logger = get_logger('FreshServiceMain')
    logger.print_success(f"FreshService started on port {port}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        self.logger.print_debug("\n🛑 Stopping FreshService...")
        server.stop(0)


if __name__ == "__main__":
    run_fresh_service()
