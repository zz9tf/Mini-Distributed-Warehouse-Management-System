#!/usr/bin/env python3
"""
FreshService - 底层服务
处理新鲜食品相关的库存管理
端口: 50053
"""

import grpc
import time
import signal
import sys
from concurrent import futures

import warehouse_pb2
import warehouse_pb2_grpc


class FreshService(warehouse_pb2_grpc.OrderServiceServicer):
    """
    FreshService - 新鲜食品服务
    处理食品类别的库存管理
    """
    
    def __init__(self):
        """Initialize FreshService"""
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
        print("🥬 FreshService initialized")
    
    def PlaceOrder(self, request, context):
        """处理下单请求"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            item = request.item.lower()
            
            print(f"🥬 [RECEIVED] FreshService - PlaceOrder Request:")
            print(f"   📥 Category: {category}")
            print(f"   📥 Subcategory: {subcategory}")
            print(f"   📥 Item: {item}")
            print(f"   📥 Client IP: {context.peer()}")
            
            # 检查库存
            if (category in self.inventory and 
                subcategory in self.inventory[category] and 
                item in self.inventory[category][subcategory]):
                
                current_stock = self.inventory[category][subcategory][item]
                print(f"   📊 Current stock: {current_stock}")
                
                if current_stock > 0:
                    # 减少库存
                    self.inventory[category][subcategory][item] -= 1
                    new_stock = self.inventory[category][subcategory][item]
                    
                    print(f"   ✅ [SENDING] Order successful - Stock reduced to: {new_stock}")
                    response = warehouse_pb2.OrderResponse(
                        status="ok",
                        left=new_stock
                    )
                    print(f"   📤 Response: status={response.status}, left={response.left}")
                    return response
                else:
                    print(f"   ❌ [SENDING] Out of stock")
                    response = warehouse_pb2.OrderResponse(
                        status="out of stock",
                        left=0
                    )
                    print(f"   📤 Response: status={response.status}, left={response.left}")
                    return response
            else:
                print(f"   ❌ [SENDING] Item not found in inventory")
                response = warehouse_pb2.OrderResponse(
                    status="item not found",
                    left=0
                )
                print(f"   📤 Response: status={response.status}, left={response.left}")
                return response
                
        except Exception as e:
            print(f"❌ [ERROR] FreshService PlaceOrder error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.OrderResponse(
                status="error",
                left=0
            )
            print(f"   📤 Response: status={response.status}, left={response.left}")
            return response
    
    def PutItem(self, request, context):
        """放入货物"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            item = request.item.lower()
            
            print(f"🥬 [RECEIVED] FreshService - PutItem Request:")
            print(f"   📥 Category: {category}")
            print(f"   📥 Subcategory: {subcategory}")
            print(f"   📥 Item: {item}")
            print(f"   📥 Client IP: {context.peer()}")
            
            if category not in self.inventory:
                self.inventory[category] = {}
                print(f"   📝 Created new category: {category}")
            if subcategory not in self.inventory[category]:
                self.inventory[category][subcategory] = {}
                print(f"   📝 Created new subcategory: {subcategory}")
            
            old_count = self.inventory[category][subcategory].get(item, 0)
            if item in self.inventory[category][subcategory]:
                self.inventory[category][subcategory][item] += 1
                print(f"   📈 Incremented existing item: {item} ({old_count} → {self.inventory[category][subcategory][item]})")
            else:
                self.inventory[category][subcategory][item] = 1
                print(f"   🆕 Added new item: {item} (count: 1)")
            
            print(f"   ✅ [SENDING] PutItem successful")
            response = warehouse_pb2.PutItemResponse(
                success=True,
                message=f"Added {item} to {category}/{subcategory}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
            
        except Exception as e:
            print(f"❌ [ERROR] FreshService PutItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.PutItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
    
    def GetItem(self, request, context):
        """取出货物"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            item = request.item.lower()
            
            print(f"🥬 [RECEIVED] FreshService - GetItem Request:")
            print(f"   📥 Category: {category}")
            print(f"   📥 Subcategory: {subcategory}")
            print(f"   📥 Item: {item}")
            print(f"   📥 Client IP: {context.peer()}")
            
            if (category in self.inventory and 
                subcategory in self.inventory[category] and 
                item in self.inventory[category][subcategory] and
                self.inventory[category][subcategory][item] > 0):
                
                old_count = self.inventory[category][subcategory][item]
                self.inventory[category][subcategory][item] -= 1
                new_count = self.inventory[category][subcategory][item]
                
                print(f"   📊 Stock before: {old_count}, after: {new_count}")
                print(f"   ✅ [SENDING] GetItem successful")
                response = warehouse_pb2.GetItemResponse(
                    success=True,
                    message=f"Retrieved {item} from {category}/{subcategory}"
                )
                print(f"   📤 Response: success={response.success}, message={response.message}")
                return response
            else:
                print(f"   ❌ [SENDING] Item not available")
                response = warehouse_pb2.GetItemResponse(
                    success=False,
                    message="Item not available"
                )
                print(f"   📤 Response: success={response.success}, message={response.message}")
                return response
                
        except Exception as e:
            print(f"❌ [ERROR] FreshService GetItem error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.GetItemResponse(
                success=False,
                message=f"Error: {str(e)}"
            )
            print(f"   📤 Response: success={response.success}, message={response.message}")
            return response
    
    def ListItems(self, request, context):
        """查询当前仓库"""
        try:
            category = request.category.lower()
            subcategory = request.subcategory.lower()
            
            print(f"🥬 [RECEIVED] FreshService - ListItems Request:")
            print(f"   📥 Category: {category}")
            print(f"   📥 Subcategory: {subcategory}")
            print(f"   📥 Client IP: {context.peer()}")
            
            items = []
            print(self.inventory[category][subcategory])
            if (category in self.inventory and 
                subcategory in self.inventory[category]):
                items.append(str(self.inventory[category][subcategory]))
            
            print(f"   ✅ [SENDING] ListItems successful")
            response = warehouse_pb2.ListItemsResponse(items=items)
            print(f"   📤 Response: {len(response.items)} items")
            return response
            
        except Exception as e:
            print(f"❌ [ERROR] FreshService ListItems error: {e}")
            print(f"   📤 [SENDING] Error response")
            response = warehouse_pb2.ListItemsResponse(items=[])
            print(f"   📤 Response: {len(response.items)} items")
            return response


def run_fresh_service(port=50053):
    """运行FreshService"""
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    warehouse_pb2_grpc.add_OrderServiceServicer_to_server(FreshService(), server)
    server.add_insecure_port(f'[::]:{port}')
    server.start()
    
    print(f"🥬 FreshService started on port {port}")
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping FreshService...")
        server.stop(0)


if __name__ == "__main__":
    run_fresh_service()
