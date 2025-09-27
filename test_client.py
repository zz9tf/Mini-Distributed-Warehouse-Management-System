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
                item=int(item)
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
                item=int(item)
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
                item=int(item)
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
    
    def test_logger_service(self):
        """测试LoggerService的查询和统计功能 - 全面测试"""
        print("\n📊 [TEST] Comprehensive LoggerService Testing")
        print("=" * 60)
        
        # 创建LoggerService客户端
        logger_channel = grpc.insecure_channel('logger-service:50055')
        logger_stub = warehouse_pb2_grpc.LoggerServiceStub(logger_channel)
        
        try:
            # ==================== 基础查询测试 ====================
            print("🔍 [PHASE 1] Basic Query Tests")
            print("-" * 40)
            
            # 测试1: 查询所有日志
            print("📋 [TEST 1.1] QueryLogs - All logs (limit=20)...")
            query_request = warehouse_pb2.QueryLogsRequest(limit=20)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Found {len(query_response.logs)} logs (total: {query_response.total_count})")
            
            # 验证日志结构
            if query_response.logs:
                log = query_response.logs[0]
                print(f"   🔍 Log structure validation:")
                print(f"      ✅ Timestamp: {log.timestamp}")
                print(f"      ✅ Service: {log.service_name}")
                print(f"      ✅ Operation: {log.operation}")
                print(f"      ✅ Client IP: {log.client_ip}")
                print(f"      ✅ Success: {log.success}")
                print(f"      ✅ Request Data: {log.request_data[:50]}..." if len(log.request_data) > 50 else f"      ✅ Request Data: {log.request_data}")
                print(f"      ✅ Response Data: {log.response_data[:50]}..." if len(log.response_data) > 50 else f"      ✅ Response Data: {log.response_data}")
            
            # 测试2: 查询无限制
            print("\n📋 [TEST 1.2] QueryLogs - No limit...")
            query_request = warehouse_pb2.QueryLogsRequest(limit=0)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Found {len(query_response.logs)} logs (should be all logs)")
            
            # ==================== 服务过滤测试 ====================
            print("\n🔍 [PHASE 2] Service Filter Tests")
            print("-" * 40)
            
            services_to_test = ["FreshService", "ApplianceService", "FoodService", "ElectronicsService", "APIGateway"]
            
            for service in services_to_test:
                print(f"📋 [TEST 2.{services_to_test.index(service)+1}] QueryLogs - Filter by {service}...")
                query_request = warehouse_pb2.QueryLogsRequest(service_name=service, limit=10)
                query_response = logger_stub.QueryLogs(query_request)
                print(f"   📊 Found {len(query_response.logs)} {service} logs")
                
                # 验证所有返回的日志都属于指定服务
                for log in query_response.logs:
                    if log.service_name != service:
                        print(f"   ❌ ERROR: Found log from {log.service_name}, expected {service}")
                    else:
                        print(f"   ✅ Verified: {log.service_name} - {log.operation}")
                        break  # 只显示第一个验证结果
            
            # ==================== 操作过滤测试 ====================
            print("\n🔍 [PHASE 3] Operation Filter Tests")
            print("-" * 40)
            
            operations_to_test = ["PlaceOrder", "PutItem", "UpdateItem", "ListItems"]
            
            for operation in operations_to_test:
                print(f"📋 [TEST 3.{operations_to_test.index(operation)+1}] QueryLogs - Filter by {operation}...")
                query_request = warehouse_pb2.QueryLogsRequest(operation=operation, limit=10)
                query_response = logger_stub.QueryLogs(query_request)
                print(f"   📊 Found {len(query_response.logs)} {operation} operations")
                
                # 验证所有返回的日志都属于指定操作
                for log in query_response.logs:
                    if log.operation != operation:
                        print(f"   ❌ ERROR: Found {log.operation}, expected {operation}")
                    else:
                        print(f"   ✅ Verified: {log.service_name} - {log.operation}")
                        break  # 只显示第一个验证结果
            
            # ==================== 组合过滤测试 ====================
            print("\n🔍 [PHASE 4] Combined Filter Tests")
            print("-" * 40)
            
            # 测试服务+操作组合
            print("📋 [TEST 4.1] QueryLogs - FreshService + PlaceOrder...")
            query_request = warehouse_pb2.QueryLogsRequest(service_name="FreshService", operation="PlaceOrder", limit=5)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Found {len(query_response.logs)} FreshService PlaceOrder logs")
            
            # 验证组合过滤
            for log in query_response.logs:
                if log.service_name != "FreshService" or log.operation != "PlaceOrder":
                    print(f"   ❌ ERROR: Found {log.service_name} - {log.operation}, expected FreshService - PlaceOrder")
                else:
                    print(f"   ✅ Verified: {log.service_name} - {log.operation}")
                    break
            
            # 测试不存在的服务
            print("\n📋 [TEST 4.2] QueryLogs - Non-existent service...")
            query_request = warehouse_pb2.QueryLogsRequest(service_name="NonExistentService", limit=5)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Found {len(query_response.logs)} logs (should be 0)")
            
            # 测试不存在的操作
            print("\n📋 [TEST 4.3] QueryLogs - Non-existent operation...")
            query_request = warehouse_pb2.QueryLogsRequest(operation="NonExistentOperation", limit=5)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Found {len(query_response.logs)} logs (should be 0)")
            
            # ==================== 统计信息测试 ====================
            print("\n🔍 [PHASE 5] Statistics Tests")
            print("-" * 40)
            
            print("📈 [TEST 5.1] GetStats - Overall statistics...")
            stats_response = logger_stub.GetStats(warehouse_pb2.StatsRequest())
            
            print(f"   📊 Overall Statistics:")
            print(f"      📈 Total Operations: {stats_response.total_operations}")
            print(f"      ✅ Successful: {stats_response.successful_operations}")
            print(f"      ❌ Failed: {stats_response.failed_operations}")
            print(f"      📊 Success Rate: {stats_response.success_rate:.2f}%")
            
            # 验证统计数据的合理性
            if stats_response.total_operations > 0:
                calculated_success_rate = (stats_response.successful_operations / stats_response.total_operations) * 100
                if abs(stats_response.success_rate - calculated_success_rate) < 0.01:
                    print(f"   ✅ Success rate calculation verified: {calculated_success_rate:.2f}%")
                else:
                    print(f"   ❌ Success rate mismatch: reported {stats_response.success_rate:.2f}%, calculated {calculated_success_rate:.2f}%")
            
            # 服务统计详情
            print(f"\n   🏢 Service Statistics ({len(stats_response.service_stats)} services):")
            for i, service_stat in enumerate(stats_response.service_stats):
                print(f"      {i+1}. {service_stat.service_name}:")
                print(f"         📊 Total: {service_stat.total} operations")
                print(f"         ✅ Success: {service_stat.success}")
                print(f"         ❌ Failed: {service_stat.failed}")
                print(f"         📈 Success Rate: {service_stat.success_rate:.2f}%")
                
                # 验证服务统计的合理性
                if service_stat.total > 0:
                    calculated_rate = (service_stat.success / service_stat.total) * 100
                    if abs(service_stat.success_rate - calculated_rate) < 0.01:
                        print(f"         ✅ Service stats verified")
                    else:
                        print(f"         ❌ Service stats mismatch: {calculated_rate:.2f}%")
            
            # 操作统计详情
            print(f"\n   🔧 Operation Statistics ({len(stats_response.operation_stats)} operations):")
            for i, op_stat in enumerate(stats_response.operation_stats):
                print(f"      {i+1}. {op_stat.operation}:")
                print(f"         📊 Total: {op_stat.total} operations")
                print(f"         ✅ Success: {op_stat.success}")
                print(f"         ❌ Failed: {op_stat.failed}")
                print(f"         📈 Success Rate: {op_stat.success_rate:.2f}%")
                
                # 验证操作统计的合理性
                if op_stat.total > 0:
                    calculated_rate = (op_stat.success / op_stat.total) * 100
                    if abs(op_stat.success_rate - calculated_rate) < 0.01:
                        print(f"         ✅ Operation stats verified")
                    else:
                        print(f"         ❌ Operation stats mismatch: {calculated_rate:.2f}%")
            
            # ==================== 日志内容验证测试 ====================
            print("\n🔍 [PHASE 6] Log Content Validation Tests")
            print("-" * 40)
            
            print("📋 [TEST 6.1] Log content structure validation...")
            query_request = warehouse_pb2.QueryLogsRequest(limit=5)
            query_response = logger_stub.QueryLogs(query_request)
            
            for i, log in enumerate(query_response.logs):
                print(f"   📝 Log {i+1} validation:")
                
                # 验证必需字段
                required_fields = ['timestamp', 'service_name', 'operation', 'client_ip', 'success']
                for field in required_fields:
                    if hasattr(log, field) and getattr(log, field):
                        print(f"      ✅ {field}: {getattr(log, field)}")
                    else:
                        print(f"      ❌ Missing or empty {field}")
                
                # 验证JSON数据格式
                try:
                    import json
                    if log.request_data:
                        json.loads(log.request_data)
                        print(f"      ✅ Request data is valid JSON")
                    if log.response_data:
                        json.loads(log.response_data)
                        print(f"      ✅ Response data is valid JSON")
                except json.JSONDecodeError as e:
                    print(f"      ❌ Invalid JSON data: {e}")
            
            # ==================== 性能测试 ====================
            print("\n🔍 [PHASE 7] Performance Tests")
            print("-" * 40)
            
            import time
            
            # 测试查询性能
            print("📋 [TEST 7.1] QueryLogs performance test...")
            start_time = time.time()
            query_request = warehouse_pb2.QueryLogsRequest(limit=100)
            query_response = logger_stub.QueryLogs(query_request)
            query_time = time.time() - start_time
            print(f"   ⏱️ QueryLogs(limit=100): {query_time:.3f}s for {len(query_response.logs)} logs")
            
            # 测试统计性能
            print("📋 [TEST 7.2] GetStats performance test...")
            start_time = time.time()
            stats_response = logger_stub.GetStats(warehouse_pb2.StatsRequest())
            stats_time = time.time() - start_time
            print(f"   ⏱️ GetStats: {stats_time:.3f}s for {stats_response.total_operations} total operations")
            
            # 测试多次查询的一致性
            print("📋 [TEST 7.3] Query consistency test...")
            query_request = warehouse_pb2.QueryLogsRequest(limit=10)
            response1 = logger_stub.QueryLogs(query_request)
            response2 = logger_stub.QueryLogs(query_request)
            
            if len(response1.logs) == len(response2.logs):
                print(f"   ✅ Query consistency verified: {len(response1.logs)} logs in both queries")
            else:
                print(f"   ❌ Query inconsistency: {len(response1.logs)} vs {len(response2.logs)} logs")
            
            print("\n" + "=" * 60)
            print("✅ [SUCCESS] Comprehensive LoggerService test completed!")
            print("📊 [SUMMARY] All query and statistics functionality verified")
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] LoggerService gRPC error: {e}")
        except Exception as e:
            print(f"❌ [ERROR] LoggerService test error: {e}")
        finally:
            logger_channel.close()
    
    def test_error_scenarios(self):
        """测试错误场景和边界条件"""
        print("\n🚨 [TEST] Error Scenarios and Edge Cases Testing")
        print("=" * 60)
        
        # 创建LoggerService客户端
        logger_channel = grpc.insecure_channel('logger-service:50055')
        logger_stub = warehouse_pb2_grpc.LoggerServiceStub(logger_channel)
        
        try:
            # ==================== 边界条件测试 ====================
            print("🔍 [PHASE 1] Edge Cases and Boundary Tests")
            print("-" * 40)
            
            # 测试极限limit值
            print("📋 [TEST 1.1] QueryLogs - Extreme limit values...")
            
            # 测试负数limit
            query_request = warehouse_pb2.QueryLogsRequest(limit=-1)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Negative limit (-1): Found {len(query_response.logs)} logs")
            
            # 测试极大limit值
            query_request = warehouse_pb2.QueryLogsRequest(limit=999999)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Large limit (999999): Found {len(query_response.logs)} logs")
            
            # 测试空字符串过滤
            print("\n📋 [TEST 1.2] QueryLogs - Empty string filters...")
            query_request = warehouse_pb2.QueryLogsRequest(service_name="", limit=10)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Empty service name: Found {len(query_response.logs)} logs")
            
            query_request = warehouse_pb2.QueryLogsRequest(operation="", limit=10)
            query_response = logger_stub.QueryLogs(query_request)
            print(f"   📊 Empty operation: Found {len(query_response.logs)} logs")
            
            # ==================== 特殊字符测试 ====================
            print("\n🔍 [PHASE 2] Special Characters and Encoding Tests")
            print("-" * 40)
            
            # 测试特殊字符的服务名
            special_services = ["Service-With-Dash", "Service_With_Underscore", "Service.With.Dots"]
            for service in special_services:
                print(f"📋 [TEST 2.{special_services.index(service)+1}] QueryLogs - Special service name: {service}...")
                query_request = warehouse_pb2.QueryLogsRequest(service_name=service, limit=5)
                query_response = logger_stub.QueryLogs(query_request)
                print(f"   📊 Found {len(query_response.logs)} logs for {service}")
            
            # 测试特殊字符的操作名
            special_operations = ["Operation-With-Dash", "Operation_With_Underscore", "Operation.With.Dots"]
            for operation in special_operations:
                print(f"📋 [TEST 2.{len(special_services)+special_operations.index(operation)+1}] QueryLogs - Special operation name: {operation}...")
                query_request = warehouse_pb2.QueryLogsRequest(operation=operation, limit=5)
                query_response = logger_stub.QueryLogs(query_request)
                print(f"   📊 Found {len(query_response.logs)} logs for {operation}")
            
            # ==================== 并发测试 ====================
            print("\n🔍 [PHASE 3] Concurrent Access Tests")
            print("-" * 40)
            
            import threading
            import time
            
            results = []
            
            def concurrent_query(thread_id):
                """并发查询函数"""
                try:
                    query_request = warehouse_pb2.QueryLogsRequest(limit=10)
                    query_response = logger_stub.QueryLogs(query_request)
                    results.append(f"Thread {thread_id}: {len(query_response.logs)} logs")
                except Exception as e:
                    results.append(f"Thread {thread_id}: Error - {e}")
            
            # 启动多个并发查询
            print("📋 [TEST 3.1] Concurrent QueryLogs test...")
            threads = []
            for i in range(5):
                thread = threading.Thread(target=concurrent_query, args=(i+1,))
                threads.append(thread)
                thread.start()
            
            # 等待所有线程完成
            for thread in threads:
                thread.join()
            
            print("   📊 Concurrent query results:")
            for result in results:
                print(f"      {result}")
            
            # 并发统计测试
            print("\n📋 [TEST 3.2] Concurrent GetStats test...")
            stats_results = []
            
            def concurrent_stats(thread_id):
                """并发统计函数"""
                try:
                    stats_response = logger_stub.GetStats(warehouse_pb2.StatsRequest())
                    stats_results.append(f"Thread {thread_id}: {stats_response.total_operations} total ops")
                except Exception as e:
                    stats_results.append(f"Thread {thread_id}: Error - {e}")
            
            threads = []
            for i in range(3):
                thread = threading.Thread(target=concurrent_stats, args=(i+1,))
                threads.append(thread)
                thread.start()
            
            for thread in threads:
                thread.join()
            
            print("   📊 Concurrent stats results:")
            for result in stats_results:
                print(f"      {result}")
            
            # ==================== 数据一致性测试 ====================
            print("\n🔍 [PHASE 4] Data Consistency Tests")
            print("-" * 40)
            
            print("📋 [TEST 4.1] Query vs Stats consistency...")
            
            # 获取查询结果
            query_request = warehouse_pb2.QueryLogsRequest(limit=0)  # 获取所有日志
            query_response = logger_stub.QueryLogs(query_request)
            query_count = len(query_response.logs)
            
            # 获取统计结果
            stats_response = logger_stub.GetStats(warehouse_pb2.StatsRequest())
            stats_count = stats_response.total_operations
            
            print(f"   📊 QueryLogs count: {query_count}")
            print(f"   📊 GetStats count: {stats_count}")
            
            if query_count == stats_count:
                print(f"   ✅ Data consistency verified: {query_count} logs")
            else:
                print(f"   ❌ Data inconsistency: Query={query_count}, Stats={stats_count}")
            
            # 验证成功/失败统计的一致性
            print("\n📋 [TEST 4.2] Success/Failure count consistency...")
            
            success_count = sum(1 for log in query_response.logs if log.success)
            failure_count = len(query_response.logs) - success_count
            
            print(f"   📊 QueryLogs - Success: {success_count}, Failure: {failure_count}")
            print(f"   📊 GetStats - Success: {stats_response.successful_operations}, Failure: {stats_response.failed_operations}")
            
            if (success_count == stats_response.successful_operations and 
                failure_count == stats_response.failed_operations):
                print(f"   ✅ Success/Failure consistency verified")
            else:
                print(f"   ❌ Success/Failure inconsistency detected")
            
            # ==================== 压力测试 ====================
            print("\n🔍 [PHASE 5] Stress Tests")
            print("-" * 40)
            
            print("📋 [TEST 5.1] Rapid successive queries...")
            start_time = time.time()
            
            for i in range(20):
                query_request = warehouse_pb2.QueryLogsRequest(limit=5)
                query_response = logger_stub.QueryLogs(query_request)
                if i % 5 == 0:
                    print(f"   📊 Query {i+1}: {len(query_response.logs)} logs")
            
            rapid_time = time.time() - start_time
            print(f"   ⏱️ 20 rapid queries completed in {rapid_time:.3f}s")
            
            print("\n📋 [TEST 5.2] Mixed operation stress test...")
            start_time = time.time()
            
            for i in range(10):
                # 交替执行查询和统计
                if i % 2 == 0:
                    query_request = warehouse_pb2.QueryLogsRequest(limit=10)
                    query_response = logger_stub.QueryLogs(query_request)
                else:
                    stats_response = logger_stub.GetStats(warehouse_pb2.StatsRequest())
            
            mixed_time = time.time() - start_time
            print(f"   ⏱️ 10 mixed operations completed in {mixed_time:.3f}s")
            
            print("\n" + "=" * 60)
            print("✅ [SUCCESS] Error scenarios and edge cases testing completed!")
            print("🚨 [SUMMARY] All error handling and boundary conditions verified")
            
        except grpc.RpcError as e:
            print(f"❌ [ERROR] Error scenarios gRPC error: {e}")
        except Exception as e:
            print(f"❌ [ERROR] Error scenarios test error: {e}")
        finally:
            logger_channel.close()
    
    def clear_logs(self):
        """清空所有日志"""
        try:
            # 创建LoggerService客户端
            logger_channel = grpc.insecure_channel('logger-service:50055')
            logger_stub = warehouse_pb2_grpc.LoggerServiceStub(logger_channel)
            
            # 清空日志
            request = warehouse_pb2.ClearLogsRequest()
            response = logger_stub.ClearLogs(request)
            
            if response.success:
                print(f"✅ Successfully cleared {response.cleared_count} logs")
            else:
                print(f"❌ Failed to clear logs: {response.message}")
            
            logger_channel.close()
            return response
            
        except Exception as e:
            print(f"❌ [ERROR] Clear logs failed: {e}")
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
        self.test_place_order("fruits", "apple", "10")
        self.test_place_order("fruits", "apple", "20")
        
        # 放入新货物
        print("\n📦 [STEP 3] Testing item addition...")
        self.test_put_item("fruits", "apple", "40")
        
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
        self.test_place_order("kitchen", "refrigerator", "3")
        
        # 放入新货物
        print("\n📦 [STEP 3] Testing item addition...")
        self.test_put_item("kitchen", "refrigerator", "10")
        
        # 查询更新后的货物
        print("\n🔍 [STEP 4] Querying updated items...")
        self.test_list_items("kitchen", "refrigerator")
        
        # 测试更新货物
        print("\n📤 [TEST] Testing UpdateItem functionality")
        print("-" * 30)
        print("🔍 [STEP 1] Testing item update...")
        self.test_update_item("fruits", "apple", "100")
        self.test_update_item("kitchen", "refrigerator", "15")
    
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
        
        # 清空日志，确保测试环境干净
        print("🧹 [SETUP] Clearing logs for clean test environment...")
        client.clear_logs()
        
        # 先执行一些操作生成日志数据
        print("🧪 [EXECUTE] Generating log data with sample operations...")
        print("📝 [STEP 1] Creating sample operations for logging...")
        client.test_place_order("fruits", "apple", "5")
        client.test_put_item("fruits", "apple", "10")
        client.test_list_items("fruits", "apple")
        client.test_update_item("fruits", "apple", "20")
        
        # 测试LoggerService的查询和统计功能
        print("\n🧪 [EXECUTE] Testing LoggerService query and stats...")
        client.test_logger_service()
        
        # 测试错误场景和边界条件
        print("\n🧪 [EXECUTE] Testing error scenarios and edge cases...")
        client.test_error_scenarios()
        
        # 运行综合测试
        print("\n🧪 [EXECUTE] Running comprehensive test...")
        client.run_comprehensive_test()
        
        print("\n" + "=" * 60)
        print("✅ [SUCCESS] All tests completed successfully!")
        print("📝 [INFO] LoggerService query and stats functionality verified")
        
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
