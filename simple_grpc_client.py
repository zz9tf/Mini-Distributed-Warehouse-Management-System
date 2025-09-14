#!/usr/bin/env python3
"""
Simple gRPC Client Example
For testing custom proto-generated services
"""

import grpc
import time
import sys
import os


class SimpleGRPCClient:
    """
    Simple gRPC client class
    Can connect and test custom services
    """
    
    def __init__(self, host='localhost', port=50051):
        """
        Initialize client
        
        Args:
            host: Server host address
            port: Server port
        """
        self.host = host
        self.port = port
        self.channel = None
        self.stub = None
    
    def connect(self, service_stub_class):
        """
        Connect to gRPC service
        
        Args:
            service_stub_class: Proto-generated service stub class
        """
        try:
            # Create gRPC channel
            self.channel = grpc.insecure_channel(f'{self.host}:{self.port}')
            
            # Create service stub
            self.stub = service_stub_class(self.channel)
            
            print(f"✅ Connected to service: {self.host}:{self.port}")
            return True
            
        except Exception as e:
            print(f"❌ Connection failed: {e}")
            return False
    
    def test_health_check(self, health_request_class):
        """
        Test health check functionality
        
        Args:
            health_request_class: Health check request class
            health_response_class: Health check response class
        """
        if not self.stub:
            print("❌ Please connect to service first")
            return
        
        try:
            print("🏥 Testing health check...")
            
            # Create health check request
            request = health_request_class()
            
            # Call health check method
            response = self.stub.HealthCheck(request)
            
            print(f"   Status: {response.message}")
            print(f"   Service Status: {response.status}")
            
        except grpc.RpcError as e:
            print(f"❌ gRPC Error: {e}")
        except Exception as e:
            print(f"❌ Health check failed: {e}")
    
    def test_custom_method(self, method_name, request, response_processor=None):
        """
        Test custom method
        
        Args:
            method_name: Method name
            request: Request object
            response_processor: Response processing function (optional)
        """
        if not self.stub:
            print("❌ Please connect to service first")
            return
        
        try:
            print(f"🔧 Testing method: {method_name}")
            
            # Get method and call it
            method = getattr(self.stub, method_name)
            response = method(request)
            
            print(f"   Request: {request}")
            print(f"   Response: {response}")
            
            # Call response processor if provided
            if response_processor:
                response_processor(response)
            
        except grpc.RpcError as e:
            print(f"❌ gRPC Error: {e}")
        except Exception as e:
            print(f"❌ Method call failed: {e}")
    
    def close(self):
        """Close client connection"""
        if self.channel:
            self.channel.close()
            print("🔌 Client connection closed")


def example_usage():
    """
    Usage example
    Shows how to test custom services
    """
    print("🎯 Simple gRPC Client Example")
    print("=" * 40)
    
    # Create client
    client = SimpleGRPCClient(host='localhost', port=50051)
    
    try:
        # Replace with your actual service stub class
        # Example:
        # from your_proto import your_service_pb2_grpc
        # from your_proto import your_service_pb2
        
        # Connect to service
        # client.connect(your_service_pb2_grpc.YourServiceStub)
        
        # Test custom method
        # request = your_service_pb2.YourRequest(message="Hello from client!")
        # client.test_custom_method("YourMethod", request)
        
        print("💡 Please replace with your actual service code")
        print("📝 Refer to example_usage.py file")
        
    except Exception as e:
        print(f"❌ Client error: {e}")
    finally:
        client.close()


def main():
    """Main function"""
    print("🚀 Starting gRPC client test")
    print()
    
    # Run example
    example_usage()
    
    print("\n" + "=" * 40)
    print("✅ Client test completed")


if __name__ == "__main__":
    main()
