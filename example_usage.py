#!/usr/bin/env python3
"""
Usage Example: How to add custom proto-generated services and client testing
"""

from simple_grpc_server import SimpleGRPCServer
from simple_grpc_client import SimpleGRPCClient

# Assume you have generated custom proto code
# from your_custom_proto import your_service_pb2_grpc
# from your_custom_proto import your_service_pb2
# from your_custom_service import YourCustomService

def run_server_example():
    """Server-side example: How to add custom services"""
    
    print("🖥️ Server-side Example")
    print("-" * 30)
    
    # Create server instance
    server = SimpleGRPCServer()
    
    # Example 1: Add service on port 50051
    # server.add_service(
    #     port=50051,
    #     service_servicer=YourCustomService(),
    #     service_adder_func=your_service_pb2_grpc.add_YourServiceServicer_to_server,
    #     max_workers=10
    # )
    
    # Example 2: Add another service on port 50052
    # server.add_service(
    #     port=50052,
    #     service_servicer=YourAnotherService(),
    #     service_adder_func=your_service_pb2_grpc.add_YourAnotherServiceServicer_to_server,
    #     max_workers=10
    # )
    
    print("💡 Please uncomment and replace with your actual service code")
    print("🚀 Then run: python example_usage.py")
    
    # Run server
    # server.run()


def run_client_example():
    """Client-side example: How to test custom services"""
    
    print("\n📱 Client-side Example")
    print("-" * 30)
    
    # Create client
    client = SimpleGRPCClient(host='localhost', port=50051)
    
    try:
        # Connect to service
        # client.connect(your_service_pb2_grpc.YourServiceStub)
        
        # Test health check
        # client.test_health_check(
        #     your_service_pb2.HealthCheckRequest,
        #     your_service_pb2.HealthCheckResponse
        # )
        
        # Test custom method
        # request = your_service_pb2.YourRequest(message="Hello from client!")
        # client.test_custom_method("YourMethod", request)
        
        print("💡 Please uncomment and replace with your actual service code")
        print("🔧 Then run client tests")
        
    except Exception as e:
        print(f"❌ Client error: {e}")
    finally:
        client.close()


def main():
    """Main function: Run server and client examples"""
    
    print("🎯 gRPC Server and Client Usage Examples")
    print("=" * 50)
    
    # Run server example
    run_server_example()
    
    # Run client example
    run_client_example()
    
    print("\n" + "=" * 50)
    print("📚 For more information, see README.md")
    print("🔧 Use simple_grpc_server.py to start server")
    print("📱 Use simple_grpc_client.py to test client")


if __name__ == "__main__":
    main()
