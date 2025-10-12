#!/usr/bin/env python3
"""
性能测试客户端
仅围绕 API Gateway 的延迟（latency）与吞吐量（throughput）进行测试
"""

import grpc
import time
import statistics
import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import warehouse_pb2
import warehouse_pb2_grpc
from warehouse_logger import get_logger


class WarehouseTestClient:
    """仓库性能测试客户端"""
    
    def __init__(self, host='api-gateway', port=50050):
        """初始化客户端
        
        Args:
            host: 网关主机名
            port: 网关端口
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
        self.logger = get_logger('TestClient')
        
        # Store test results
        self.latency_results = {}
        self.throughput_results = {}
    
    def connect(self):
        """建立到 API Gateway 的连接"""
        try:
            self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
            self.stub = warehouse_pb2_grpc.OrderServiceStub(self.channel)
            self.logger.print_success(f"Connected to API Gateway: {self.host}:{self.port}")
            return True
        except Exception as e:
            self.logger.print_error(f"Connection failed: {e}")
            return False
    
    def close(self):
        """关闭连接"""
        if self.channel:
            self.logger.print_debug("Closing client connection...")
            self.channel.close()
            self.logger.print_success("Client connection closed")
    
    def clear_logs(self):
        """清空 LoggerService 日志（保持测试环境干净）"""
        try:
            logger_channel = grpc.insecure_channel('logger-service:50055')
            logger_stub = warehouse_pb2_grpc.LoggerServiceStub(logger_channel)
            response = logger_stub.ClearLogs(warehouse_pb2.ClearLogsRequest())
            if response.success:
                self.logger.print_debug(f"Cleared {response.cleared_count} logs")
            else:
                self.logger.print_warning(f"Clear logs failed: {response.message}")
            logger_channel.close()
        except Exception as e:
            self.logger.print_warning(f"Clear logs error: {e}")

    # ========= Basic request methods =========
    def _call_list_items(self, category: str, subcategory: str):
        """调用只读接口 ListItems"""
        request = warehouse_pb2.ListItemsRequest(category=category, subcategory=subcategory)
        return self.stub.ListItems(request)
    
    def _call_place_order(self, category: str, subcategory: str, item_count: int = 1):
        """调用下单接口 PlaceOrder"""
        request = warehouse_pb2.OrderRequest(category=category, subcategory=subcategory, item=item_count)
        return self.stub.PlaceOrder(request)
    
    def _call_put_item(self, category: str, subcategory: str, item_count: int = 1):
        """调用添加商品接口 PutItem"""
        request = warehouse_pb2.PutItemRequest(category=category, subcategory=subcategory, item=item_count)
        return self.stub.PutItem(request)
    
    def _call_update_item(self, category: str, subcategory: str, item_count: int = 1):
        """调用更新商品接口 UpdateItem"""
        request = warehouse_pb2.UpdateItemRequest(category=category, subcategory=subcategory, item=item_count)
        return self.stub.UpdateItem(request)

    # ========= Statistics utilities =========
    @staticmethod
    def _percentile(values, p):
        """计算分位数，p 取值 0-100"""
        if not values:
            return 0.0
        values_sorted = sorted(values)
        k = (len(values_sorted) - 1) * (p / 100.0)
        f = int(k)
        c = min(f + 1, len(values_sorted) - 1)
        if f == c:
            return float(values_sorted[int(k)])
        d0 = values_sorted[f] * (c - k)
        d1 = values_sorted[c] * (k - f)
        return float(d0 + d1)

    def _print_latency_stats(self, latencies_us, label: str):
        """打印延迟统计"""
        if not latencies_us:
            self.logger.print_debug(f"{label}: no samples")
            return
        avg = statistics.mean(latencies_us)
        p50 = WarehouseTestClient._percentile(latencies_us, 50)
        p90 = WarehouseTestClient._percentile(latencies_us, 90)
        p95 = WarehouseTestClient._percentile(latencies_us, 95)
        p99 = WarehouseTestClient._percentile(latencies_us, 99)
        mn = min(latencies_us)
        mx = max(latencies_us)
        self.logger.print_info(f"{label} -> count={len(latencies_us)}, avg={avg:.2f}µs, min={mn:.2f}µs, p50={p50:.2f}µs, p90={p90:.2f}µs, p95={p95:.2f}µs, p99={p99:.2f}µs, max={mx:.2f}µs")

    # ========= Latency tests =========
    def latency_test(self, operation: str, category: str = 'fruits', subcategory: str = 'apple', iterations: int = 100, warmup: int = 5, sleep_between: float = 0.0):
        """顺序请求延迟测试

        Args:
            operation: 操作类型 ('ListItems', 'PlaceOrder', 'PutItem', 'UpdateItem')
            category: 测试用品类
            subcategory: 测试用子品类
            iterations: 测试请求次数（采样数）
            warmup: 预热请求次数（不计入统计）
            sleep_between: 每次请求之间的休眠秒数（可用于避免突刺）
        """
        self.logger.print_debug(f"Latency Test (sequential, {operation})")
        
        # Choose operation function
        if operation == 'ListItems':
            call_func = lambda: self._call_list_items(category, subcategory)
        elif operation == 'PlaceOrder':
            call_func = lambda: self._call_place_order(category, subcategory, 1)
        elif operation == 'PutItem':
            call_func = lambda: self._call_put_item(category, subcategory, 1)
        elif operation == 'UpdateItem':
            call_func = lambda: self._call_update_item(category, subcategory, 1)
        else:
            self.logger.print_error(f"Unknown operation: {operation}")
            return
        
        # Warm up
        for _ in range(max(0, warmup)):
            try:
                call_func()
            except Exception:
                pass
            if sleep_between > 0:
                time.sleep(sleep_between)

        latencies_us = []
        successes = 0
        failures = 0
        for i in range(iterations):
            start = time.perf_counter_ns()
            try:
                call_func()
                elapsed_us = (time.perf_counter_ns() - start) / 1000  # Convert nanoseconds to microseconds
                latencies_us.append(elapsed_us)
                successes += 1
            except Exception as e:
                elapsed_us = (time.perf_counter_ns() - start) / 1000
                latencies_us.append(elapsed_us)
                failures += 1
                self.logger.print_warning(f"error@{i+1}: {e}")
            if sleep_between > 0:
                time.sleep(sleep_between)

        self._print_latency_stats(latencies_us, label=f"Latency({operation})")
        self.logger.print_debug(f"success={successes}, failure={failures}")
        
        # Store latency test results
        if latencies_us:
            result_key = f"{self.host}_{operation}"
            self.latency_results[result_key] = {
                'count': len(latencies_us),
                'avg': sum(latencies_us) / len(latencies_us),
                'min': min(latencies_us),
                'p50': WarehouseTestClient._percentile(latencies_us, 50),
                'p90': WarehouseTestClient._percentile(latencies_us, 90),
                'p95': WarehouseTestClient._percentile(latencies_us, 95),
                'p99': WarehouseTestClient._percentile(latencies_us, 99),
                'max': max(latencies_us),
                'success': successes,
                'failure': failures
            }

    # ========= Throughput tests =========
    def throughput_test(self, operation: str, category: str = 'fruits', subcategory: str = 'apple', concurrency: int = 20, duration_sec: int = 10):
        """并发吞吐量测试（稳定压力，在持续时间内尽可能多完成请求）

        Args:
            operation: 操作类型 ('ListItems', 'PlaceOrder', 'PutItem', 'UpdateItem')
            category: 测试用品类
            subcategory: 测试用子品类
            item: 测试用商品名
            concurrency: 并发工作线程数
            duration_sec: 持续压测时长（秒）
        """
        self.logger.print_debug(f"Throughput Test (concurrent, {operation})")
        
        # Choose operation function
        if operation == 'ListItems':
            call_func = lambda: self._call_list_items(category, subcategory)
        elif operation == 'PlaceOrder':
            call_func = lambda: self._call_place_order(category, subcategory, 1)
        elif operation == 'PutItem':
            call_func = lambda: self._call_put_item(category, subcategory, 1)
        elif operation == 'UpdateItem':
            call_func = lambda: self._call_update_item(category, subcategory, 1)
        else:
            self.logger.print_error(f"Unknown operation: {operation}")
            return

        stop_at = time.time() + max(1, duration_sec)
        latencies_us = []
        successes = 0
        failures = 0
        lock = threading.Lock()

        skip_time = 7
        def worker(worker_id: int):
            nonlocal successes, failures
            # Reusing the same stub per thread is safe (gRPC Channel/Stub is thread-safe)
            while time.time() < stop_at:
                if time.time() - start_wall <= skip_time:
                    try:
                        call_func()
                    except Exception:
                        pass
                    continue
                start = time.perf_counter()
                try:
                    call_func()
                    elapsed_us = (time.perf_counter() - start) * 1_000_000.0
                    with lock:
                        latencies_us.append(elapsed_us)
                        successes += 1
                except Exception:
                    elapsed_us = (time.perf_counter() - start) * 1_000_000.0
                    with lock:
                        latencies_us.append(elapsed_us)
                        failures += 1

        threads = []
        start_wall = time.time()
        for i in range(max(1, concurrency)):
            t = threading.Thread(target=worker, args=(i+1,))
            t.daemon = True
            threads.append(t)
            t.start()
        for t in threads:
            t.join()
        end_wall = time.time()

        elapsed = max(1e-9, end_wall - start_wall)
        total = successes + failures
        qps = total / (elapsed - skip_time)

        self.logger.print_info(f"{operation} - Workers={concurrency}, duration={elapsed:.2f}s, total={total}, success={successes}, failure={failures}, QPS={qps:.2f}")
        self._print_latency_stats(latencies_us, label=f"Latency({operation})")
        
        # Store throughput test results
        self.throughput_results[f"{self.host}_{operation}"] = {
            'workers': concurrency,
            'duration': elapsed,
            'total': total,
            'success': successes,
            'failure': failures,
            'qps': qps,
            'latency_avg': statistics.mean(latencies_us) if latencies_us else 0,
            'latency_p50': WarehouseTestClient._percentile(latencies_us, 50) if latencies_us else 0,
            'latency_p90': WarehouseTestClient._percentile(latencies_us, 90) if latencies_us else 0,
            'latency_p95': WarehouseTestClient._percentile(latencies_us, 95) if latencies_us else 0,
            'latency_p99': WarehouseTestClient._percentile(latencies_us, 99) if latencies_us else 0
        }

def run_service_tests_concurrently(service_configs, test_type, logger):
    """并发运行多个服务的测试
    
    Args:
        service_configs: 服务配置列表，每个配置包含 (name, host, port, operations)
        test_type: 测试类型 ('latency' 或 'throughput')
        logger: 日志记录器
    """
    def run_single_service_test(config):
        name, host, port, operations = config
        client = WarehouseTestClient(host=host, port=port)
        
        if not client.connect():
            logger.print_error(f"❌ Failed to connect to {name}")
            return None
        
        logger.print_info(f"🚀 {name} {test_type} test started (concurrent)")
        
        total_ops = len(operations)
        for i, (operation, category, subcategory) in enumerate(operations, 1):
            logger.print_info(f"  📋 [{i}/{total_ops}] Testing operation: {operation}")
            if test_type == 'latency':
                client.latency_test(
                    operation=operation,
                    category=category,
                    subcategory=subcategory,
                    iterations=30,
                    warmup=2
                )
            else:  # throughput
                client.throughput_test(
                    operation=operation,
                    category=category,
                    subcategory=subcategory,
                    concurrency=5,
                    duration_sec=3
                )
            logger.print_info(f"  ✅ [{i}/{total_ops}] {operation} completed")
        
        logger.print_success(f"🎉 {name} {test_type} test completed")
        client.close()
        return client
    
    # Execute concurrently with a thread pool
    logger.print_info(f"🔄 Starting concurrent {test_type} tests for {len(service_configs)} services...")
    with ThreadPoolExecutor(max_workers=len(service_configs)) as executor:
        futures = [executor.submit(run_single_service_test, config) for config in service_configs]
        
        results = []
        completed = 0
        for future in as_completed(futures):
            result = future.result()
            completed += 1
            if result:
                results.append(result)
            logger.print_info(f"📊 Progress: {completed}/{len(service_configs)} services finished")
    
    logger.print_success(f"🏁 All {test_type} tests finished! Success: {len(results)}/{len(service_configs)}")
    return results


def get_service_name(host):
    """简化服务名称映射"""
    name_map = {
        'fresh-service': 'FreshService',
        'appliance-service': 'ApplianceService', 
        'food-service': 'FoodService',
        'electronics-service': 'ElectronicsService',
        'api-gateway': 'APIGateway'
    }
    return name_map.get(host, host)


# Global result collectors
global_latency_results = {}
global_throughput_results = {}

def collect_results(client, test_name):
    """收集客户端测试结果到全局结果中"""
    global global_latency_results, global_throughput_results
    
    for key, value in client.latency_results.items():
        global_latency_results[f"{test_name}_{key}"] = value
    
    for key, value in client.throughput_results.items():
        global_throughput_results[f"{test_name}_{key}"] = value

def print_global_latency_table(logger):
    """打印全局延迟测试结果表格"""
    logger.print_info("=" * 120)
    logger.print_info("📊 Global Latency Test Results")
    logger.print_info("=" * 120)
    
    
    # Table header
    header = f"{'Test Scenario':<20} {'Service':<15} {'Operation':<12} {'Count':<8} {'Avg(µs)':<10} {'Min(µs)':<10} {'P50(µs)':<10} {'P90(µs)':<10} {'P95(µs)':<10} {'P99(µs)':<10} {'Max(µs)':<10} {'Success':<8} {'Failure':<8}"
    logger.print_info(header)
    logger.print_info("-" * 120)
    
    # Sort by test scenario
    sorted_results = sorted(global_latency_results.items())
    for key, stats in sorted_results:
        parts = key.split('_', 2)
        test_scenario = parts[0] if len(parts) > 0 else 'Unknown'
        service = parts[1] if len(parts) > 1 else 'Unknown'
        operation = parts[2] if len(parts) > 2 else 'Unknown'
        
        # Simplify service names
        service_name = get_service_name(service)
        
        row = f"{test_scenario:<20} {service_name:<15} {operation:<12} {stats['count']:<8} {stats['avg']:<10.2f} {stats['min']:<10.2f} {stats['p50']:<10.2f} {stats['p90']:<10.2f} {stats['p95']:<10.2f} {stats['p99']:<10.2f} {stats['max']:<10.2f} {stats['success']:<8} {stats['failure']:<8}"
        logger.print_info(row)
    
    logger.print_info("=" * 120)

def print_global_throughput_table(logger):
    """打印全局吞吐量测试结果表格"""
    logger.print_info("=" * 120)
    logger.print_info("📈 Global Throughput Test Results")
    logger.print_info("=" * 120)
    
    # Table header
    header = f"{'Test Scenario':<20} {'Service':<15} {'Operation':<12} {'Workers':<8} {'Duration(s)':<12} {'Total':<8} {'Success':<8} {'Failure':<8} {'QPS':<10} {'LatAvg(µs)':<12} {'LatP50(µs)':<12} {'LatP90(µs)':<12} {'LatP95(µs)':<12} {'LatP99(µs)':<12}"
    logger.print_info(header)
    logger.print_info("-" * 120)
    
    # Sort by test scenario
    sorted_results = sorted(global_throughput_results.items())
    for key, stats in sorted_results:
        parts = key.split('_', 2)
        test_scenario = parts[0] if len(parts) > 0 else 'Unknown'
        service = parts[1] if len(parts) > 1 else 'Unknown'
        operation = parts[2] if len(parts) > 2 else 'Unknown'
        
        # Simplify service names
        service_name = get_service_name(service)
        
        row = f"{test_scenario:<20} {service_name:<15} {operation:<12} {stats['workers']:<8} {stats['duration']:<12.2f} {stats['total']:<8} {stats['success']:<8} {stats['failure']:<8} {stats['qps']:<10.2f} {stats['latency_avg']:<12.2f} {stats['latency_p50']:<12.2f} {stats['latency_p90']:<12.2f} {stats['latency_p95']:<12.2f} {stats['latency_p99']:<12.2f}"
        logger.print_info(row)
    
    logger.print_info("=" * 120)

def test_single_bottom_container(client, logger):
    """测试单个底层容器（直接访问一个底层服务）"""
    logger.print_info("=" * 80)
    logger.print_info("🎯 1. Single Bottom Container Test")
    logger.print_info("=" * 80)
    
    # Only test one base-layer service
    service_configs = [
        ("FreshService", "fresh-service", 50053, [
            ('ListItems', 'fruits', 'apple'),
            ('PlaceOrder', 'fruits', 'apple'),
            ('PutItem', 'fruits', 'apple'),
            ('UpdateItem', 'fruits', 'apple'),
        ])
    ]
    
    # Run latency tests concurrently
    logger.print_info("⏱️  Starting latency test...")
    latency_results = run_service_tests_concurrently(service_configs, 'latency', logger)
    
    # Run throughput tests concurrently
    logger.print_info("📈 Starting throughput test...")
    throughput_results = run_service_tests_concurrently(service_configs, 'throughput', logger)
    
    # Collect results
    for result in latency_results:
        collect_results(result, "SingleBottom")
    for result in throughput_results:
        collect_results(result, "SingleBottom")
    
    logger.print_success("✅ Single bottom container test complete!")

def test_two_bottom_containers(client, logger):
    """测试两个底层容器（同时访问两个底层服务）"""
    logger.print_info("=" * 80)
    logger.print_info("🎯 2. Two Bottom Containers Test")
    logger.print_info("=" * 80)
    
    # Test two base-layer services simultaneously
    service_configs = [
        ("FreshService", "fresh-service", 50053, [
            ('ListItems', 'fruits', 'apple'),
            ('PlaceOrder', 'fruits', 'apple'),
            ('PutItem', 'fruits', 'apple'),
            ('UpdateItem', 'fruits', 'apple'),
        ]),
        ("ApplianceService", "appliance-service", 50054, [
            ('ListItems', 'kitchen', 'refrigerator'),
            ('PlaceOrder', 'kitchen', 'refrigerator'),
            ('PutItem', 'kitchen', 'refrigerator'),
            ('UpdateItem', 'kitchen', 'refrigerator'),
        ])
    ]
    
    # Run latency tests concurrently
    logger.print_info("⏱️  Starting concurrent latency test...")
    latency_results = run_service_tests_concurrently(service_configs, 'latency', logger)
    
    # Run throughput tests concurrently
    logger.print_info("📈 Starting concurrent throughput test...")
    throughput_results = run_service_tests_concurrently(service_configs, 'throughput', logger)
    
    # Collect results
    for result in latency_results:
        collect_results(result, "TwoBottom")
    for result in throughput_results:
        collect_results(result, "TwoBottom")
    
    logger.print_success("✅ Two bottom containers test complete!")

def test_two_middle_containers(client, logger):
    """测试两个中层容器（分别对应一个底层）"""
    logger.print_info("=== 3. Two Middle Containers Test ===")
    
    # Test two middle-layer services simultaneously
    service_configs = [
        ("FoodService", "food-service", 50052, [
            ('ListItems', 'fruits', 'apple'),
            ('PlaceOrder', 'fruits', 'apple'),
            ('PutItem', 'fruits', 'apple'),
            ('UpdateItem', 'fruits', 'apple'),
        ]),
        ("ElectronicsService", "electronics-service", 50051, [
            ('ListItems', 'kitchen', 'refrigerator'),
            ('PlaceOrder', 'kitchen', 'refrigerator'),
            ('PutItem', 'kitchen', 'refrigerator'),
            ('UpdateItem', 'kitchen', 'refrigerator'),
        ])
    ]
    
    # Run latency tests concurrently
    logger.print_info("⏱️  Starting concurrent latency test...")
    latency_results = run_service_tests_concurrently(service_configs, 'latency', logger)
    
    # Run throughput tests concurrently
    logger.print_info("📈 Starting concurrent throughput test...")
    throughput_results = run_service_tests_concurrently(service_configs, 'throughput', logger)
    
    # Collect results
    for result in latency_results:
        collect_results(result, "TwoMiddle")
    for result in throughput_results:
        collect_results(result, "TwoMiddle")

def test_single_middle_container(client, logger):
    """测试单个中层容器（直接访问一个中层服务）"""
    logger.print_info("=" * 80)
    logger.print_info("🎯 3. Single Middle Container Test")
    logger.print_info("=" * 80)
    
    # Only test one middle-layer service
    service_configs = [
        ("FoodService", "food-service", 50052, [
            ('ListItems', 'fruits', 'apple'),
            ('PlaceOrder', 'fruits', 'apple'),
            ('PutItem', 'fruits', 'apple'),
            ('UpdateItem', 'fruits', 'apple'),
        ])
    ]
    
    # Run latency tests concurrently
    logger.print_info("⏱️  Starting latency test...")
    latency_results = run_service_tests_concurrently(service_configs, 'latency', logger)
    
    # Run throughput tests concurrently
    logger.print_info("📈 Starting throughput test...")
    throughput_results = run_service_tests_concurrently(service_configs, 'throughput', logger)
    
    # Collect results
    for result in latency_results:
        collect_results(result, "SingleMiddle")
    for result in throughput_results:
        collect_results(result, "SingleMiddle")
    
    logger.print_success("✅ Single middle container test complete!")

def test_api_gateway_performance(client, logger, enable_logging=True):
    """测试API Gateway性能（通过API Gateway访问所有服务）
    
    Args:
        client: 测试客户端
        logger: 日志记录器
        enable_logging: 是否启用日志记录 (True/False)
    """
    logging_status = "Logging enabled" if enable_logging else "Logging disabled"
    logger.print_info("=" * 80)
    logger.print_info(f"🎯 API Gateway Performance Test - {logging_status}")
    logger.print_info("=" * 80)
    
    # Set logging state for all services
    _configure_logging_for_all_services(enable_logging, logger)
    
    # Test all operations through the API Gateway
    logger.print_info("⏱️  Starting API Gateway latency test...")
    
    # Iterate through all operation types
    operations = [
        ('ListItems', 'kitchen', 'refrigerator'),
        ('PlaceOrder', 'kitchen', 'refrigerator'),
        ('PutItem', 'kitchen', 'refrigerator'),
        ('UpdateItem', 'kitchen', 'refrigerator'),
    ]
    
    for operation, category, subcategory in operations:
        logger.print_info(f"  📋 Testing operation: {operation}")
        client.latency_test(
            operation=operation,
            category=category,
            subcategory=subcategory,
            iterations=50,
            warmup=20
        )
    
    logger.print_info("📈 Starting API Gateway throughput test...")
    
    for operation, category, subcategory in operations:
        logger.print_info(f"  📋 Testing operation: {operation}")
        client.throughput_test(
            operation=operation,
            category=category,
            subcategory=subcategory,
            concurrency=5,
            duration_sec=10
        )
    
    # Collect results，使用不同的标签区分日志状态
    test_label = f"APIGateway_{'WithLog' if enable_logging else 'NoLog'}"
    collect_results(client, test_label)
    
    logger.print_success(f"✅ API Gateway performance test complete! ({logging_status})")

def _configure_logging_for_all_services(enable_logging, logger):
    """配置所有服务的日志状态
    
    Args:
        enable_logging: 是否启用日志记录
        logger: 日志记录器
    """
    services = [
        ('api-gateway', 50050),
        ('food-service', 50052),
        ('electronics-service', 50051),
        ('fresh-service', 50053),
        ('appliance-service', 50054)
    ]
    
    for service_name, port in services:
        try:
            channel = grpc.insecure_channel(f'{service_name}:{port}')
            stub = warehouse_pb2_grpc.OrderServiceStub(channel)
            
            # Send configuration request
            request = warehouse_pb2.ConfigureLoggingRequest(enable_logging=enable_logging)
            response = stub.ConfigureLogging(request)
            
            if response.success:
                status = "enabled" if enable_logging else "disabled"
                logger.print_debug(f"✅ {service_name}: Logging {status} succeeded")
            else:
                logger.print_warning(f"⚠️ {service_name}: Logging configuration failed - {response.message}")
                
            channel.close()
        except Exception as e:
            logger.print_warning(f"⚠️ {service_name}: Error configuring logging - {e}")

def test_logger_service_operations(logger):
    """测试LoggerService的操作"""
    logger.print_info("=" * 80)
    logger.print_info("🎯 4. LoggerService Operations Test")
    logger.print_info("=" * 80)
    
    try:
        logger_channel = grpc.insecure_channel('logger-service:50055')
        logger_stub = warehouse_pb2_grpc.LoggerServiceStub(logger_channel)
        
        # Test LogOperation
        logger.print_info("⏱️  LogOperation latency test...")
        latencies_us = []
        for i in range(30):
            start = time.perf_counter()
            try:
                request = warehouse_pb2.LogRequest(
                    service_name="TestService",
                    operation="TestOperation",
                    client_ip="127.0.0.1",
                    success=True,
                    request_data='{"test": "data"}',
                    response_data='{"result": "success"}',
                    error_message=""
                )
                response = logger_stub.LogOperation(request)
                elapsed_us = (time.perf_counter() - start) * 1_000_000.0
                latencies_us.append(elapsed_us)
            except Exception as e:
                logger.print_warning(f"LogOperation error@{i+1}: {e}")
        
        if latencies_us:
            avg = statistics.mean(latencies_us)
            p50 = WarehouseTestClient._percentile(latencies_us, 50)
            p90 = WarehouseTestClient._percentile(latencies_us, 90)
            p95 = WarehouseTestClient._percentile(latencies_us, 95)
            p99 = WarehouseTestClient._percentile(latencies_us, 99)
            mn = min(latencies_us)
            mx = max(latencies_us)
            logger.print_info(f"LogOperation -> count={len(latencies_us)}, avg={avg:.2f}µs, min={mn:.2f}µs, p50={p50:.2f}µs, p90={p90:.2f}µs, p95={p95:.2f}µs, p99={p99:.2f}µs, max={mx:.2f}µs")
        
        # Test QueryLogs
        logger.print_info("⏱️  QueryLogs latency test...")
        latencies_us = []
        for i in range(30):
            start = time.perf_counter()
            try:
                request = warehouse_pb2.QueryLogsRequest(limit=10)
                response = logger_stub.QueryLogs(request)
                elapsed_us = (time.perf_counter() - start) * 1_000_000.0
                latencies_us.append(elapsed_us)
            except Exception as e:
                logger.print_warning(f"QueryLogs error@{i+1}: {e}")
        
        if latencies_us:
            avg = statistics.mean(latencies_us)
            p50 = WarehouseTestClient._percentile(latencies_us, 50)
            p90 = WarehouseTestClient._percentile(latencies_us, 90)
            p95 = WarehouseTestClient._percentile(latencies_us, 95)
            p99 = WarehouseTestClient._percentile(latencies_us, 99)
            mn = min(latencies_us)
            mx = max(latencies_us)
            logger.print_info(f"QueryLogs -> count={len(latencies_us)}, avg={avg:.2f}µs, min={mn:.2f}µs, p50={p50:.2f}µs, p90={p90:.2f}µs, p95={p95:.2f}µs, p99={p99:.2f}µs, max={mx:.2f}µs")
        
        logger_channel.close()
        logger.print_success("✅ LoggerService tests complete!")
        
    except Exception as e:
        logger.print_error(f"❌ LoggerService test failed: {e}")

def main():
    """入口：运行服务组合性能测试"""
    logger = get_logger('Main')
    logger.print_debug("Starting Warehouse Performance Test Client")

    client = WarehouseTestClient(host='api-gateway', port=50050)
    try:
        logger.print_debug("Connecting to API Gateway...")
        if not client.connect():
            logger.print_error("Failed to connect. Ensure services are up: api_gateway + all backends + logger_service")
            return
        
        # Clear logs
        client.clear_logs()
        
        logger.print_info("🚀 Starting service combination performance tests")
        logger.print_info("📋 Test plan: len(test_scenarios) scenarios")
        logger.print_info("")
        
        # API Gateway performance tests - compare logging enabled vs disabled
        test_scenarios = [
            ("API Gateway Performance Test (Logging Enabled)", lambda: test_api_gateway_performance(client, logger, enable_logging=True)),
            ("API Gateway Performance Test (Logging Disabled)", lambda: test_api_gateway_performance(client, logger, enable_logging=False)),
        ]
        
        for i, (name, test_func) in enumerate(test_scenarios, 1):
            logger.print_info(f"🔄 [{i}/{len(test_scenarios)}] Starting {name}...")
            test_func()
            logger.print_info(f"✅ [{i}/{len(test_scenarios)}] {name} complete")
            logger.print_info("")
        
        logger.print_success("🎉 All test scenarios complete!")
        
        # Print summary tables
        logger.print_info("")
        logger.print_info("🎯 Test results summary")
        logger.print_info("")
        
        # Print latency results table
        print_global_latency_table(logger)
        
        logger.print_info("")
        
        # Print throughput results table
        print_global_throughput_table(logger)
        
        logger.print_success("=== All service combination performance tests complete ===")
        
    except KeyboardInterrupt:
        logger.print_warning("Interrupted by user")
    finally:
        client.close()

if __name__ == "__main__":
    main()
