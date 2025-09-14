#!/usr/bin/env python3
"""
Simple gRPC Server Framework
Supports custom proto-generated code
Provides two ports: 50051 and 50052
"""

import grpc
import time
import signal
import sys
from concurrent import futures


class SimpleGRPCServer:
    """
    Simple gRPC server class
    Can accept custom proto-generated code
    """
    
    def __init__(self):
        """Initialize server"""
        self.servers = {}
        self.running = False
        
        # Set up signal handling
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
    
    def _signal_handler(self, signum, frame):
        """Handle system signals"""
        print(f"\n🛑 Received signal {signum}, shutting down services...")
        self.stop_all_servers()
        sys.exit(0)
    
    def add_service(self, port, service_servicer, service_adder_func, max_workers=10):
        """
        Add gRPC service
        
        Args:
            port: Service port
            service_servicer: Service implementation instance
            service_adder_func: Service registration function (add_XXXServicer_to_server)
            max_workers: Maximum worker threads
        """
        try:
            # Create gRPC server
            server = grpc.server(
                futures.ThreadPoolExecutor(max_workers=max_workers)
            )
            
            # Register service
            service_adder_func(service_servicer, server)
            
            # Bind port
            listen_addr = f'[::]:{port}'
            server.add_insecure_port(listen_addr)
            
            # Start service
            server.start()
            
            # Save server reference
            self.servers[port] = server
            
            print(f"✅ Service started - Port: {port}")
            print(f"   📍 Service address: localhost:{port}")
            print(f"   🔧 Max workers: {max_workers}")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to start service (port {port}): {e}")
            return False
    
    def start_all_servers(self):
        """Start all servers"""
        print("🚀 Starting gRPC servers...")
        print("=" * 40)
        
        # You can add your custom services here
        # Example:
        # self.add_service(50051, your_service_instance, your_adder_func)
        # self.add_service(50052, your_another_service_instance, your_another_adder_func)
        
        if not self.servers:
            print("⚠️ No services configured")
            print("💡 Please use add_service() method to add your services")
            return
        
        self.running = True
        print("=" * 40)
        print("✅ All services started!")
        print("🎯 Server ready to accept client connections")
        print("\n📋 Available ports:")
        for port in self.servers.keys():
            print(f"   🔌 Port: {port}")
        print("\n💡 Use Ctrl+C to stop services")
        print("=" * 40)
    
    def stop_all_servers(self):
        """Stop all servers"""
        if not self.running:
            return
        
        print("\n🛑 Stopping all services...")
        
        for port, server in self.servers.items():
            try:
                server.stop(grace=5)
                print(f"✅ Port {port} service stopped")
            except Exception as e:
                print(f"⚠️ Error stopping port {port} service: {e}")
        
        self.servers.clear()
        self.running = False
        print("✅ All services stopped")
    
    def run(self):
        """Run server"""
        try:
            self.start_all_servers()
            
            # Keep services running
            while self.running:
                time.sleep(1)
                
        except KeyboardInterrupt:
            print("\n🛑 Received interrupt signal")
        except Exception as e:
            print(f"❌ Server runtime error: {e}")
        finally:
            self.stop_all_servers()


def main():
    """Main function"""
    print("🎯 Simple gRPC Server Framework")
    print("📦 Supports custom proto-generated code")
    print("🔧 Provides two ports: 50051 and 50052")
    print()
    
    # Create server instance
    server = SimpleGRPCServer()
    
    # Add your custom services here
    # Example:
    # from your_proto_generated_code import your_service_pb2_grpc
    # from your_service_implementation import YourServiceImplementation
    # 
    # server.add_service(
    #     port=50051,
    #     service_servicer=YourServiceImplementation(),
    #     service_adder_func=your_service_pb2_grpc.add_YourServiceServicer_to_server
    # )
    
    # Run server
    server.run()


if __name__ == "__main__":
    main()
