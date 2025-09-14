#!/usr/bin/env python3
"""
启动所有服务的脚本
按照分层架构顺序启动服务
"""

import subprocess
import time
import signal
import sys
import os


class ServiceManager:
    """服务管理器"""
    
    def __init__(self):
        self.processes = []
        self.running = False
        
        # 设置信号处理
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """处理系统信号"""
        print(f"\n🛑 Received signal {signum}, shutting down all services...")
        self.stop_all_services()
        sys.exit(0)
    
    def start_service(self, name, command, port, delay=2):
        """启动单个服务"""
        try:
            print(f"🚀 Starting {name} on port {port}...")
            
            # 启动服务进程
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.processes.append({
                'name': name,
                'process': process,
                'port': port,
                'command': command
            })
            
            # 等待服务启动
            time.sleep(delay)
            
            # 检查服务是否正常启动
            if process.poll() is None:
                print(f"✅ {name} started successfully on port {port}")
                return True
            else:
                print(f"❌ Failed to start {name}")
                return False
                
        except Exception as e:
            print(f"❌ Error starting {name}: {e}")
            return False
    
    def start_all_services(self):
        """按照分层架构启动所有服务"""
        print("🎯 Starting Layered Warehouse Services")
        print("=" * 50)
        
        # 1. 启动底层服务
        print("\n📦 Starting Bottom Layer Services...")
        self.start_service("FreshService", "python services/fresh_service.py", 50053)
        self.start_service("ApplianceService", "python services/appliance_service.py", 50054)
        
        # 2. 启动中层服务
        print("\n🏢 Starting Middle Layer Services...")
        self.start_service("FoodService", "python services/food_service.py", 50052)
        self.start_service("ElectronicsService", "python services/electronics_service.py", 50051)
        
        # 3. 启动顶层服务
        print("\n🌐 Starting Top Layer Service...")
        self.start_service("APIGateway", "python api_gateway.py", 50050)
        
        self.running = True
        print("\n" + "=" * 50)
        print("✅ All services started successfully!")
        print("🎯 System ready to accept requests")
        print("\n📋 Service Architecture:")
        print("   🌐 API Gateway (50050) → Routes requests")
        print("   ├── 🍎 FoodService (50052) → 🥬 FreshService (50053)")
        print("   └── 📱 ElectronicsService (50051) → 🏠 ApplianceService (50054)")
        print("\n💡 Use Ctrl+C to stop all services")
        print("=" * 50)
    
    def stop_all_services(self):
        """停止所有服务"""
        if not self.running:
            return
        
        print("\n🛑 Stopping all services...")
        
        for service in self.processes:
            try:
                service['process'].terminate()
                service['process'].wait(timeout=5)
                print(f"✅ {service['name']} stopped")
            except subprocess.TimeoutExpired:
                service['process'].kill()
                print(f"⚠️ {service['name']} force stopped")
            except Exception as e:
                print(f"⚠️ Error stopping {service['name']}: {e}")
        
        self.processes.clear()
        self.running = False
        print("✅ All services stopped")
    
    def run(self):
        """运行服务管理器"""
        try:
            self.start_all_services()
            
            # 保持服务运行
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Received interrupt signal")
        except Exception as e:
            print(f"❌ Service manager error: {e}")
        finally:
            self.stop_all_services()


def main():
    """主函数"""
    print("🎯 Layered Warehouse Service Manager")
    print("📦 Manages 5 services in hierarchical architecture")
    print()
    
    # 检查Python环境
    if sys.version_info < (3, 8):
        print("❌ Python 3.8+ required")
        sys.exit(1)
    
    # 检查依赖
    try:
        import grpc
        import warehouse_pb2
        import warehouse_pb2_grpc
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("💡 Run: pip install -r requirements.txt")
        sys.exit(1)
    
    # 创建并运行服务管理器
    manager = ServiceManager()
    manager.run()


if __name__ == "__main__":
    main()

