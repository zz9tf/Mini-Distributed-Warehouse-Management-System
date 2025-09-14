#!/usr/bin/env python3
"""
Frontend Test Client
测试分层架构的gRPC服务
"""

import grpc
import time
import sys

import warehouse_pb2
import warehouse_pb2_grpc


class WarehouseTestClient:
    """
    仓库测试客户端
    测试分层架构的gRPC服务
    """
    
    def __init__(self, host='api-gateway', port=50050):
        """
        初始化客户端
        
        Args:
            host: 服务器主机地址
            port: 服务器端口
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
    
    def connect(self):
        """连接到gRPC服务"""
        try:
            # 创建gRPC通道
            self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
            
            # 创建服务stub
            self.stub = warehouse_pb2_grpc.OrderServiceStub(self.channel)
            
            print(f"✅ Connected to API Gateway: {self.host}:{self.port}")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_place_order(self, category, subcategory, item):
        """测试下单功能"""
        try:
            print(f"\n🛒 [SENDING] TestClient - PlaceOrder Request:")
            print(f"   📤 Category: {category}")
            print(f"   📤 Subcategory: {subcategory}")
            print(f"   📤 Item: {item}")
            
            # 创建下单请求
            request = warehouse_pb2.OrderRequest(
                category=category,
                subcategory=subcategory,
                item=item
            )
            
            print(f"   🔄 [CALLING] Sending request to API Gateway...")
            # 调用下单方法
            response = self.stub.PlaceOrder(request)
            
            print(f"   📨 [RECEIVED] Response from API Gateway:")
            print(f"   📨 Status: {response.status}")
            print(f"   📨 Left in stock: {response.left}")
            print(f"   ✅ [SUCCESS] PlaceOrder completed")
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] gRPC Error: {e}")
            print(f"   📨 [FAILED] PlaceOrder failed due to gRPC error")
            return None
        except Exception as e:
            print(f"❌ [ERROR] PlaceOrder failed: {e}")
            print(f"   📨 [FAILED] PlaceOrder failed due to exception")
            return None
    
    def test_put_item(self, category, subcategory, item):
        """测试放入货物功能"""
        try:
            print(f"\n📦 [SENDING] TestClient - PutItem Request:")
            print(f"   📤 Category: {category}")
            print(f"   📤 Subcategory: {subcategory}")
            print(f"   📤 Item: {item}")
            
            # 创建放入货物请求
            request = warehouse_pb2.PutItemRequest(
                category=category,
                subcategory=subcategory,
                item=item
            )
            
            print(f"   🔄 [CALLING] Sending request to API Gateway...")
            # 调用放入货物方法
            response = self.stub.PutItem(request)
            
            print(f"   📨 [RECEIVED] Response from API Gateway:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SUCCESS] PutItem completed")
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] gRPC Error: {e}")
            print(f"   📨 [FAILED] PutItem failed due to gRPC error")
            return None
        except Exception as e:
            print(f"❌ [ERROR] PutItem failed: {e}")
            print(f"   📨 [FAILED] PutItem failed due to exception")
            return None
    
    def test_update_item(self, category, subcategory, item):
        """测试更新货物功能"""
        try:
            print(f"\n📤 [SENDING] TestClient - UpdateItem Request:")
            print(f"   📤 Category: {category}")
            print(f"   📤 Subcategory: {subcategory}")
            print(f"   📤 Item: {item}")
            
            # 创建更新货物请求
            request = warehouse_pb2.UpdateItemRequest(
                category=category,
                subcategory=subcategory,
                item=item
            )
            
            print(f"   🔄 [CALLING] Sending request to API Gateway...")
            # 调用更新货物方法
            response = self.stub.UpdateItem(request)
            
            print(f"   📨 [RECEIVED] Response from API Gateway:")
            print(f"   📨 Success: {response.success}")
            print(f"   📨 Message: {response.message}")
            print(f"   ✅ [SUCCESS] UpdateItem completed")
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] gRPC Error: {e}")
            print(f"   📨 [FAILED] UpdateItem failed due to gRPC error")
            return None
        except Exception as e:
            print(f"❌ [ERROR] UpdateItem failed: {e}")
            print(f"   📨 [FAILED] UpdateItem failed due to exception")
            return None
    
    def test_list_items(self, category, subcategory):
        """测试查询货物功能"""
        try:
            print(f"\n📋 [SENDING] TestClient - ListItems Request:")
            print(f"   📤 Category: {category}")
            print(f"   📤 Subcategory: {subcategory}")
            
            # 创建查询货物请求
            request = warehouse_pb2.ListItemsRequest(
                category=category,
                subcategory=subcategory
            )
            
            print(f"   🔄 [CALLING] Sending request to API Gateway...")
            # 调用查询货物方法
            response = self.stub.ListItems(request)
            
            print(f"   📨 [RECEIVED] Response from API Gateway:")
            print(f"   📨 Items found: {len(response.items)}")
            for i, item in enumerate(response.items):
                print(f"   📨 Item {i+1}: {item}")
            print(f"   ✅ [SUCCESS] ListItems completed")
            
            return response
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] gRPC Error: {e}")
            print(f"   📨 [FAILED] ListItems failed due to gRPC error")
            return None
        except Exception as e:
            print(f"❌ [ERROR] ListItems failed: {e}")
            print(f"   📨 [FAILED] ListItems failed due to exception")
            return None
    
    def run_comprehensive_test(self):
        """运行综合测试"""
        print("🎯 [START] Warehouse Test Client - Comprehensive Test")
        print("=" * 60)
        
        # 测试食品类
        print("\n🍎 [TEST] Testing Food Category (FoodService → FreshService)")
        print("-" * 50)
        
        # 查询现有货物
        print("🔍 [STEP 1] Querying existing items...")
        self.test_list_items("fruits", "apple")
        
        # 下单测试
        print("\n🛒 [STEP 2] Testing order placement...")
        self.test_place_order("fruits", "apple", "apple")
        self.test_place_order("fruits", "apple", "apple")
        
        # 放入新货物
        print("\n📦 [STEP 3] Testing item addition...")
        self.test_put_item("fruits", "apple", "grape")
        
        # 查询更新后的货物
        print("\n🔍 [STEP 4] Querying updated items...")
        self.test_list_items("fruits", "apple")
        
        # 测试电子产品类
        print("\n📱 [TEST] Testing Electronics Category (ElectronicsService → ApplianceService)")
        print("-" * 50)
        
        # 查询现有货物
        print("🔍 [STEP 1] Querying existing items...")
        self.test_list_items("kitchen", "refrigerator")
        
        # 下单测试
        print("\n🛒 [STEP 2] Testing order placement...")
        self.test_place_order("kitchen", "refrigerator", "refrigerator")
        
        # 放入新货物
        print("\n📦 [STEP 3] Testing item addition...")
        self.test_put_item("kitchen", "refrigerator", "oven")
        
        # 查询更新后的货物
        print("\n🔍 [STEP 4] Querying updated items...")
        self.test_list_items("kitchen", "refrigerator")
        
        # 测试更新货物
        print("\n📤 [TEST] Testing UpdateItem functionality")
        print("-" * 30)
        print("🔍 [STEP 1] Testing item update...")
        self.test_update_item("fruits", "apple", 100)
        self.test_update_item("kitchen", "refrigerator", 15)
    
    def close(self):
        """关闭客户端连接"""
        if self.channel:
            print("🔌 [CLOSING] Closing client connection...")
            self.channel.close()
            print("✅ [CLOSED] Client connection closed")


def main():
    """主函数"""
    print("🚀 [START] Starting Warehouse Test Client")
    print("📦 [INFO] Testing Layered gRPC Architecture")
    print()
    
    # 创建客户端
    print("🔧 [INIT] Creating test client...")
    client = WarehouseTestClient(host='api-gateway', port=50050)
    
    try:
        # 连接到API Gateway
        print("🔗 [CONNECT] Attempting to connect to API Gateway...")
        if not client.connect():
            print("❌ [FAILED] Failed to connect to API Gateway")
            print("💡 [HELP] Make sure all services are running:")
            print("   - API Gateway: python api_gateway.py")
            print("   - FoodService: python services/food_service.py")
            print("   - ElectronicsService: python services/electronics_service.py")
            print("   - FreshService: python services/fresh_service.py")
            print("   - ApplianceService: python services/appliance_service.py")
            return
        
        # 运行综合测试
        print("🧪 [EXECUTE] Running comprehensive test...")
        client.run_comprehensive_test()
        
        print("\n" + "=" * 60)
        print("✅ [SUCCESS] Test completed successfully!")
        
    except KeyboardInterrupt:
        print("\n🛑 [INTERRUPTED] Test interrupted by user")
    except Exception as e:
        print(f"❌ [ERROR] Test error: {e}")
    finally:
        # 关闭连接
        print("\n🧹 [CLEANUP] Cleaning up resources...")
        client.close()


if __name__ == "__main__":
    main()
